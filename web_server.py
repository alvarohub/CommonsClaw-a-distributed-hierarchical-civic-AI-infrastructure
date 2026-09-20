from __future__ import annotations

import json
import queue
import threading
import time
from typing import Iterator

import requests
from flask import Flask, Response, jsonify, request, send_file

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

        self._generation_lock = threading.Lock()
        self._question_cond = threading.Condition()
        self._pending_question: str | None = None

    # ------------------------------------------------------------------
    # lifecycle
    # ------------------------------------------------------------------

    def run(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        self.llm_manager.check_availability()
        self.status_store.update_model(self.llm_manager.metrics)
        self._start_background_thread()
        app = self._build_app()
        try:
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

    def _submit_question(self, question: str) -> None:
        self.status_store.submit_question(question)
        with self._question_cond:
            self._pending_question = question
            self._question_cond.notify()

    def _stream_question(self, question: str) -> Iterator[dict]:
        """Yield SSE event dicts for one question."""
        if not self.llm_manager.metrics.available:
            self.llm_manager.check_availability()
            self.status_store.update_model(self.llm_manager.metrics)
        if not self.llm_manager.metrics.available:
            self.status_store.complete_turn(
                answer=None, success=False, error="model_unavailable",
            )
            yield {"event": "error", "data": "Model unavailable"}
            return

        with self._generation_lock:
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
            self._submit_question(question)
            return jsonify({"ok": True})

        @app.get("/api/stream")
        def stream():
            def generate():
                # Heartbeat comment so proxies/browsers don't idle-timeout.
                yield ": connected\n\n"
                while not self.stop_event.is_set():
                    with self._question_cond:
                        self._question_cond.wait(timeout=0.5)
                        question = self._pending_question
                        self._pending_question = None
                    if question is None:
                        continue
                    # Single-slot: if a generation is already running, tell
                    # this client to show "busy" and drop the question.
                    if self._generation_lock.locked():
                        busy = {"event": "busy", "data": "Answering another question…"}
                        yield f"event: {busy['event']}\ndata: {busy['data']}\n\n"
                        continue
                    for event in self._stream_question(question):
                        yield f"event: {event['event']}\ndata: {event['data']}\n\n"

            return Response(
                generate(),
                mimetype="text/event-stream",
                headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
            )

        return app


def main() -> None:
    WebApplication().run()


if __name__ == "__main__":
    main()
