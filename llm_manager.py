from dataclasses import dataclass
import json
import time
from typing import Callable, Iterator

import requests

import config


@dataclass
class ModelMetrics:
    model_name: str = config.MODEL_NAME
    ttft_seconds: float | None = None
    total_response_seconds: float | None = None
    prompt_tokens: int | None = None
    output_tokens: int | None = None
    tokens_per_second: float | None = None
    active: bool = False
    available: bool = False


class LLMManager:
    def __init__(self):
        self.model_name = config.MODEL_NAME
        self.api_base = config.OLLAMA_API_BASE.rstrip("/")
        self.history_enabled = config.CONVERSATION_HISTORY
        self.messages: list[dict[str, str]] = []
        self.metrics = ModelMetrics(model_name=self.model_name)

    def check_availability(self) -> tuple[bool, str]:
        try:
            response = requests.get(
                f"{self.api_base}/tags",
                timeout=config.REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            self.metrics.available = False
            return False, f"Ollama API unavailable: {exc}"

        model_names = {
            item.get("name") or item.get("model")
            for item in data.get("models", [])
        }

        if self.model_name not in model_names:
            self.metrics.available = False
            return False, f"Model '{self.model_name}' is not installed in Ollama"

        self.metrics.available = True
        return True, ""

    def clear_history(self) -> None:
        self.messages.clear()

    def stream_response(
        self,
        prompt: str,
        on_metrics_update: Callable[[ModelMetrics], None] | None = None,
        model: str | None = None,
        memory_categories: set[str] | None = None,
    ) -> Iterator[str]:
        # `model` overrides the configured default for this call only
        # (used by the web UI's per-request model selector).
        # `memory_categories` limits which memory sections enter the prompt
        # (None = all on, as before; empty set = bare prompt).
        model_name = model or self.model_name
        self._reset_current_metrics()
        self.metrics.model_name = model_name
        self.metrics.active = True
        if on_metrics_update:
            on_metrics_update(self.metrics)

        request_messages = self._build_request_messages(prompt, memory_categories)
        payload = {
            "model": model_name,
            "messages": request_messages,
            "stream": True,
            "options": {
                "num_predict": config.NUM_PREDICT,
            },
        }

        start_time = time.perf_counter()
        first_token_time: float | None = None
        response_parts: list[str] = []
        final_data: dict = {}

        try:
            with requests.post(
                f"{self.api_base}/chat",
                json=payload,
                stream=True,
                timeout=None,
            ) as response:
                response.raise_for_status()

                for raw_line in response.iter_lines(decode_unicode=True):
                    if not raw_line:
                        continue

                    try:
                        data = json.loads(raw_line)
                    except json.JSONDecodeError:
                        continue

                    message = data.get("message") or {}
                    chunk = message.get("content") or ""

                    if chunk:
                        if first_token_time is None:
                            first_token_time = time.perf_counter()
                            self.metrics.ttft_seconds = first_token_time - start_time
                            if on_metrics_update:
                                on_metrics_update(self.metrics)

                        response_parts.append(chunk)
                        yield chunk

                    if data.get("done"):
                        final_data = data

            end_time = time.perf_counter()
            self.metrics.total_response_seconds = end_time - start_time
            self._apply_final_metrics(final_data)

            assistant_text = "".join(response_parts)
            if self.history_enabled:
                self.messages.append({"role": "user", "content": prompt})
                self.messages.append({"role": "assistant", "content": assistant_text})

        except requests.RequestException:
            self.metrics.available = False
            raise
        finally:
            self.metrics.active = False
            if on_metrics_update:
                on_metrics_update(self.metrics)

    def _build_request_messages(self, prompt: str, memory_categories: set[str] | None) -> list[dict[str, str]]:
        system_message = {
            "role": "system",
            "content": self._system_prompt_with_reports(memory_categories),
        }
        if self.history_enabled:
            return [system_message, *self.messages, {"role": "user", "content": prompt}]
        return [system_message, {"role": "user", "content": prompt}]

    # Slash keywords force a memory category on for this question
    # (e.g. "/sensors how warm is it?"). Auto-detect keywords below do the
    # same without the user knowing.
    SLASH_KEYWORDS = {
        "/identity": "identity",
        "/sensors": "sensors",
        "/community": "community",
        "/notes": "community",
    }
    AUTO_KEYWORDS = {
        "sensors": {"sensor", "temperature", "temp", "solar", "battery",
                    "panel", "humidity", "weather", "hot", "cold", "warm",
                    "cpu", "ram", "feeling", "body"},
        "community": {"note", "notes", "remember", "suggestion", "poll",
                      "vote", "people", "community", "said", "told"},
        "identity": {"yourself", "who are you", "your name", "personality",
                     "remember about yourself", "kami"},
    }

    @classmethod
    def resolve_categories(cls, prompt: str, toggles: set[str] | None) -> set[str]:
        """Final active categories = UI toggles + slash keywords + auto-detect."""
        active = set(toggles) if toggles is not None else set()
        low = prompt.lower()
        for kw, cat in cls.SLASH_KEYWORDS.items():
            if low.startswith(kw):
                active.add(cat)
        for cat, words in cls.AUTO_KEYWORDS.items():
            if any(w in low for w in words):
                active.add(cat)
        return active

    @staticmethod
    def _system_prompt_with_reports(categories: set[str] | None = None) -> str:
        """System prompt + the node's shared memory digest for the ACTIVE
        categories only (empty set = bare prompt = full speed)."""
        if categories is not None and not categories:
            return config.SYSTEM_PROMPT
        try:
            from reports_reader import read_reports
            digest = read_reports(categories)
        except Exception:
            digest = ""
        if not digest:
            return config.SYSTEM_PROMPT
        return (
            config.SYSTEM_PROMPT
            + "\n\nYou are the voice of a specific place. Below are its current"
            " reports (sensor logs and community notes). Treat them as ground"
            " truth about the local place and moment; prefer them over general"
            " knowledge for local questions, and acknowledge people's notes.\n\n"
            + digest
        )

    def _reset_current_metrics(self) -> None:
        self.metrics.ttft_seconds = None
        self.metrics.total_response_seconds = None
        self.metrics.prompt_tokens = None
        self.metrics.output_tokens = None
        self.metrics.tokens_per_second = None

    def _apply_final_metrics(self, data: dict) -> None:
        self.metrics.prompt_tokens = data.get("prompt_eval_count")
        self.metrics.output_tokens = data.get("eval_count")

        eval_duration_ns = data.get("eval_duration")
        output_tokens = self.metrics.output_tokens

        if output_tokens is not None and eval_duration_ns:
            eval_seconds = eval_duration_ns / 1_000_000_000
            if eval_seconds > 0:
                self.metrics.tokens_per_second = output_tokens / eval_seconds
