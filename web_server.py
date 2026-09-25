from __future__ import annotations

import json
import queue
import threading
import time
from typing import Iterator

import requests
from flask import Flask, Response, jsonify, request, send_file

try:
    import waitress
    _HAVE_WAITRESS = True
except ImportError:
    waitress = None
    _HAVE_WAITRESS = False

import config
from hardware_monitor import HardwareMonitor
from llm_manager import LLMManager
from status_store import StatusStore


class WebApplication:
    """Serves the chat page and streams model answers to browsers.

    Shares LLMManager / HardwareMonitor / StatusStore with the other
    frontends, so control.py and console.py keep working alongside.
    Generation is single-slot (Ollama on a Pi is effectively serial); a
    second client gets a "busy" event instead of a parallel generation.
    """

    def __init__(self):
        self.stop_event = threading.Event()
        self.hardware_monitor = HardwareMonitor()
        self.llm_manager = LLMManager()
        self.status_store = StatusStore()
        self.background_thread: threading.Thread | None = None

        # Single generation slot (Ollama on a Pi is effectively serial).
        self._generation_lock = threading.Lock()

    # ------------------------------------------------------------------
    # lifecycle
    # ------------------------------------------------------------------

    def run(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        self.llm_manager.check_availability()
        self.status_store.update_model(self.llm_manager.metrics)
        self._start_background_thread()
        app = self._build_app()
        try:
            if _HAVE_WAITRESS:
                # Production WSGI server: robust against dropped/sleeping
                # clients, which is what killed the Flask dev server.
                print(f"Serving on http://{host}:{port} (waitress)")
                waitress.serve(app, host=host, port=port, threads=8)
            else:
                print("waitress not installed; falling back to Flask dev server")
                print("(sudo apt install python3-waitress for a stable server)")
                app.run(host=host, port=port, threaded=True)
        finally:
            self._shutdown()

    def _start_background_thread(self) -> None:
        self.background_thread = threading.Thread(
            target=self._background_loop,
            name="ssai-monitor-loop",
            daemon=True,
        )
        self.background_thread.start()

    def _background_loop(self) -> None:
        while not self.stop_event.is_set():
            hardware = self.hardware_monitor.read_snapshot()
            self.status_store.update_hardware(hardware)
            self.stop_event.wait(config.HARDWARE_SAMPLE_INTERVAL)

    def _shutdown(self) -> None:
        self.stop_event.set()
        if self.background_thread and self.background_thread.is_alive():
            self.background_thread.join(timeout=1.0)
        self.status_store.clear()

    # ------------------------------------------------------------------
    # generation worker (single slot)
    # ------------------------------------------------------------------

    def _stream_question(self, question: str) -> Iterator[dict]:
        """Yield SSE event dicts for one question.

        The caller holds a per-request response stream, so the client that
        asked is the client that receives the answer (no shared broadcast).
        """
        self.status_store.submit_question(question)

        # Single-slot: a second concurrent asker is told to wait rather than
        # starting a parallel generation the Pi can't sustain.
        if not self._generation_lock.acquire(blocking=False):
            yield {"event": "busy", "data": "Answering another question…"}
            return

        try:
            if not self.llm_manager.metrics.available:
                self.llm_manager.check_availability()
                self.status_store.update_model(self.llm_manager.metrics)
            if not self.llm_manager.metrics.available:
                self.status_store.complete_turn(
                    answer=None, success=False, error="model_unavailable",
                )
                yield {"event": "error", "data": "Model unavailable"}
                return

            yield {"event": "start", "data": ""}
            response_parts: list[str] = []
            try:
                for chunk in self.llm_manager.stream_response(
                    question,
                    on_metrics_update=self.status_store.update_model,
                ):
                    response_parts.append(chunk)
                    yield {"event": "chunk", "data": chunk}

                answer = "".join(response_parts)
                self.status_store.complete_turn(answer=answer, success=True)
                yield {
                    "event": "done",
                    "data": json.dumps({
                        "answer": answer,
                        "metrics": {
                            "ttft_seconds": self.llm_manager.metrics.ttft_seconds,
                            "total_response_seconds": self.llm_manager.metrics.total_response_seconds,
                            "output_tokens": self.llm_manager.metrics.output_tokens,
                            "tokens_per_second": self.llm_manager.metrics.tokens_per_second,
                        },
                    }),
                }
            except requests.RequestException:
                self.status_store.update_model(self.llm_manager.metrics)
                self.status_store.complete_turn(
                    answer="".join(response_parts) or None,
                    success=False,
                    error="communication_error",
                )
                yield {"event": "error", "data": "Model error"}
        finally:
            self._generation_lock.release()

    # ------------------------------------------------------------------
    # Flask app
    # ------------------------------------------------------------------

    def _build_app(self) -> Flask:
        app = Flask(__name__)

        @app.get("/")
        def index():
            return send_file("static/chat.html")

        @app.get("/api/status")
        def status():
            snapshot = self.hardware_monitor.read_snapshot()
            metrics = self.llm_manager.metrics
            return jsonify({
                "model": metrics.model_name,
                "available": metrics.available,
                "active": metrics.active,
                "cpu_percent": snapshot.cpu_percent,
                "ram_percent": snapshot.ram_percent,
                "temperature_c": snapshot.temperature_c,
            })

        @app.post("/api/ask")
        def ask():
            data = request.get_json(force=True, silent=True) or {}
            question = (data.get("question") or "").strip()
            if not question:
                return jsonify({"error": "empty question"}), 400

            def generate():
                try:
                    for event in self._stream_question(question):
                        yield f"event: {event['event']}\ndata: {event['data']}\n\n"
                except Exception:
                    # Never let a generation error kill the HTTP response.
                    import traceback
                    traceback.print_exc()
                    yield "event: error\ndata: internal error\n\n"

            return Response(
                generate(),
                mimetype="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
                },
            )

        return app


def main() -> None:
    WebApplication().run()


if __name__ == "__main__":
    main()
