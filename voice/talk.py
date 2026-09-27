#!/usr/bin/env python3
"""Push-to-talk / wake-word voice loop for the kami node (Phase 3, steps 3-4).

Run ON THE PI with the voice venv (needs faster-whisper + requests):
    ~/voice-venv/bin/python voice/talk.py

Controls (default: push-to-talk):
    Enter        — start recording; Enter again — stop; the kami answers.
    Ctrl+C       — exit.

Wake-word mode:
    ~/voice-venv/bin/python voice/talk.py --wake kami

    The mic listens continuously in short windows; when the whisper
    transcript contains the wake word (default "kami"), recording continues
    until a pause, and the remainder after the wake word becomes the
    question. Saying just "kami" wakes it for the NEXT utterance.

Design: this is a FRONTEND, exactly like console.py — it captures the
question (by voice instead of keyboard) and hands it to the same
LLMManager.stream_response(). The answer prints token by token, and the
turn is published to the status store, so the web dashboard sees it too.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))  # repo root on sys.path

import config
from llm_manager import LLMManager
from status_store import StatusStore
from voice.mic_setup import find_capture_card

MODEL_SIZE = "tiny"
WHISPER: object | None = None  # lazy-loaded on first use


def get_whisper():
    global WHISPER
    if WHISPER is None:
        from faster_whisper import WhisperModel
        print(f"(loading whisper '{MODEL_SIZE}' — first time takes a moment)")
        WHISPER = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    return WHISPER


def record_until_enter(card: int, dev: int, path: Path) -> None:
    """Record from the ReSpeaker until Enter is pressed."""
    proc = subprocess.Popen(
        ["arecord", "-q", "-D", f"plughw:{card},{dev}", "-f", "S16_LE",
         "-r", "16000", "-c", "1", str(path)],
    )
    input()  # block until Enter
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()


def transcribe(path: Path) -> str:
    model = get_whisper()
    segments, _info = model.transcribe(str(path))
    return " ".join(s.text for s in segments).strip()


def record_fixed(card: int, dev: int, path: Path, seconds: float) -> None:
    """Record exactly `seconds` of audio (used by wake-word listening)."""
    subprocess.run(
        ["arecord", "-q", "-D", f"plughw:{card},{dev}", "-f", "S16_LE",
         "-r", "16000", "-c", "1", "-d", str(seconds), str(path)],
        check=True,
    )


def answer(llm: LLMManager, status: StatusStore, text: str, stt_s: float) -> None:
    """One full turn: publish, stream the kami's answer, record metrics."""
    print(f'YOU (heard, {stt_s:.1f}s): {text}')
    status.submit_question(text)

    print("KAMI: ", end="", flush=True)
    parts: list[str] = []
    for chunk in llm.stream_response(text, on_metrics_update=status.update_model):
        parts.append(chunk)
        print(chunk, end="", flush=True)
    print()
    status.complete_turn("".join(parts), success=True)
    m = llm.metrics
    print(f"[stt {stt_s:.1f}s | ttft {m.ttft_seconds:.1f}s | "
          f"{m.tokens_per_second:.1f} tok/s]\n")


def push_to_talk_loop(llm, status, card, dev) -> None:
    while True:
        input(">>> press Enter and speak ")
        clip = Path(tempfile.mktemp(suffix=".wav", prefix="kami_"))
        record_until_enter(card, dev, clip)
        t0 = time.perf_counter()
        text = transcribe(clip)
        stt_s = time.perf_counter() - t0
        clip.unlink(missing_ok=True)
        if not text:
            print("(heard nothing — try again, a bit louder)\n")
            continue
        answer(llm, status, text, stt_s)


def wake_word_loop(llm, status, card, dev, wake_word: str) -> None:
    """Listen in short windows; the wake word arms the kami.

    Saying e.g. "kami, how warm is the water?" answers immediately; saying
    just "kami" makes it listen for the next utterance (up to ~8 s).
    Cheap-and-cheerful VAD: whisper on 2.5 s windows; silence = empty
    transcript.
    """
    print(f'(wake word: "{wake_word}" — say it to get the kami\'s attention)')
    armed = False
    while True:
        clip = Path(tempfile.mktemp(suffix=".wav", prefix="kami_"))
        record_fixed(card, dev, clip, 8.0 if armed else 2.5)
        t0 = time.perf_counter()
        text = transcribe(clip).lower()
        stt_s = time.perf_counter() - t0
        clip.unlink(missing_ok=True)

        if not text:
            if armed:
                print("(still listening... say something)")
            continue

        wake = wake_word.lower()
        if wake in text:
            # Everything after the wake word is the question, if any.
            after = text.split(wake, 1)[1].strip(" ,.?!")
            if after:
                answer(llm, status, after, stt_s)
                armed = False
            else:
                armed = True
                print("KAMI: yes? (listening...)\n")
        elif armed:
            answer(llm, status, text, stt_s)
            armed = False
        else:
            print(f'(ignored: "{text}")')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wake", metavar="WORD", default=None,
                    help='wake-word mode (e.g. --wake kami)')
    args = ap.parse_args()

    found = find_capture_card()
    if not found:
        sys.exit("No ReSpeaker found. Check `arecord -l`.")
    card, dev = found

    llm = LLMManager()
    status = StatusStore()
    llm.check_availability()
    status.update_model(llm.metrics)

    print(f"CommonsClaw voice loop (mic: card {card}, model: {config.MODEL_NAME})")

    try:
        if args.wake:
            wake_word_loop(llm, status, card, dev, args.wake)
        else:
            print("Enter to talk, Enter to stop, Ctrl+C to quit.\n")
            push_to_talk_loop(llm, status, card, dev)
    except KeyboardInterrupt:
        print("\nbye")
    finally:
        status.clear()


if __name__ == "__main__":
    main()
