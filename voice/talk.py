#!/usr/bin/env python3
"""Push-to-talk / wake-word voice loop for the kami node (Phase 3, steps 3-4).

Run ON THE PI with the voice venv (needs faster-whisper + requests):
    ~/voice-venv/bin/python voice/talk.py --serve

`--serve` is the normal mode: the microphone does whatever the web page
says (off / wake word / press-to-talk), re-read from node_settings.json
every cycle. The two manual modes below still exist for debugging.

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
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))  # repo root on sys.path

import config
import node_settings
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


def record_until_silence(card: int, dev: int, path: Path,
                         max_seconds: float = 15.0) -> bool:
    """Record until the speaker pauses (silence) or max_seconds.

    Records in 0.5 s chunks via a long-running arecord piped through a
    silence watcher: stops after SILENCE_AFTER_S below threshold, having
    heard speech at least once. Returns False if nothing usable captured.
    """
    SILENCE_AFTER_S = 1.6
    THRESHOLD = 800  # 16-bit amplitude; quiet room < ~300

    proc = subprocess.Popen(
        ["arecord", "-D", f"plughw:{card},{dev}", "-f", "S16_LE",
         "-r", "16000", "-c", "1", "-t", "raw", str(path) + ".raw"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    raw_path = Path(str(path) + ".raw")
    heard_speech = False
    silent_for = 0.0
    t0 = time.time()
    last_size = 0
    while time.time() - t0 < max_seconds:
        time.sleep(0.25)
        if not raw_path.exists():
            continue
        size = raw_path.stat().st_size
        chunk = size - last_size
        last_size = size
        if chunk > 0:
            with raw_path.open("rb") as f:
                f.seek(size - chunk)
                data = f.read(chunk)
            samples = [int.from_bytes(data[i:i+2], "little", signed=True)
                       for i in range(0, len(data) - 1, 2)]
            if samples and max(abs(s) for s in samples) > THRESHOLD:
                heard_speech = True
                silent_for = 0.0
            else:
                silent_for += 0.25
        if heard_speech and silent_for >= SILENCE_AFTER_S:
            break
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill(); proc.wait()

    # wrap the raw PCM in a WAV header so whisper can read it
    if not heard_speech or last_size < 2000:
        raw_path.unlink(missing_ok=True)
        return False
    import wave as _wave
    with raw_path.open("rb") as f:
        pcm = f.read()
    with _wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(pcm)
    raw_path.unlink(missing_ok=True)
    return True


def transcribe(path: Path) -> str:
    model = get_whisper()
    segments, _info = model.transcribe(str(path))
    return " ".join(s.text for s in segments).strip()


def new_clip() -> Path:
    """A fresh temp .wav path. mkstemp hands back an OPEN fd; closing it is
    not optional — leaking one per recording exhausts the process in minutes."""
    fd, name = tempfile.mkstemp(suffix=".wav", prefix="kami_")
    os.close(fd)
    return Path(name)


def record_fixed(card: int, dev: int, path: Path, seconds: float) -> bool:
    """Record a fixed window (used by wake-word listening).
    Returns False if nothing usable was captured."""
    # arecord -d takes whole seconds only; 2.5 makes it exit immediately.
    subprocess.run(
        ["arecord", "-D", f"plughw:{card},{dev}", "-f", "S16_LE",
         "-r", "16000", "-c", "1", "-d", str(max(1, int(round(seconds)))),
         str(path)],
        stderr=subprocess.DEVNULL,
    )
    return path.exists() and path.stat().st_size > 1000


def answer(llm: LLMManager, status: StatusStore, text: str, stt_s: float) -> None:
    """One full turn: publish, stream the kami's answer, record metrics."""
    print(f'🙂 YOU (heard, {stt_s:.1f}s): {text}')
    status.submit_question(text)   # question visible on the web right away

    print("🐢 KAMI is thinking...", end="", flush=True)
    parts: list[str] = []
    first = True
    # Same shared settings the web page edits — one node, one behaviour.
    categories = LLMManager.resolve_categories(text, node_settings.memory_categories())
    for chunk in llm.stream_response(
        text,
        on_metrics_update=status.update_model,
        model=node_settings.model(),
        memory_categories=categories,
    ):
        if first:
            print("\r🐢 KAMI: " + chunk, end="", flush=True)
            first = False
        else:
            print(chunk, end="", flush=True)
        parts.append(chunk)
    if first:
        print("\r🐢 KAMI: (silence)")
    else:
        print()
    status.complete_turn("".join(parts), success=True)
    m = llm.metrics
    print(f"[stt {stt_s:.1f}s | ttft {m.ttft_seconds:.1f}s | "
          f"{m.tokens_per_second:.1f} tok/s]\n")


def push_to_talk_loop(llm, status, card, dev) -> None:
    while True:
        input(">>> press Enter, speak, then just pause ")
        clip = new_clip()
        print("🎤 listening...", end="", flush=True)
        ok = record_until_silence(card, dev, clip)
        print("\r🎤 (transcribing...)      ", end="", flush=True)
        if not ok:
            print("\r(no speech heard — try again)      \n")
            clip.unlink(missing_ok=True)
            continue
        t0 = time.perf_counter()
        text = transcribe(clip)
        stt_s = time.perf_counter() - t0
        clip.unlink(missing_ok=True)
        print("\r" + " " * 30 + "\r", end="")
        if not text:
            print("(heard nothing intelligible — try again)\n")
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
        clip = new_clip()
        # Short window to catch the wake word; once armed, listen for a full
        # sentence and stop on the speaker's pause.
        ok = (record_until_silence(card, dev, clip, max_seconds=12.0)
              if armed else record_fixed(card, dev, clip, 3))
        if not ok:
            clip.unlink(missing_ok=True)
            if armed:
                print("(still listening... say something)")
            continue
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


def serve_loop(llm, status, card, dev) -> None:
    """Microphone as a service: the web page decides what it does.

    Reads node_settings every cycle — off, wake-word, or button (record only
    when the page asks) — and publishes a heartbeat so the page can tell the
    difference between "idle" and "not running at all".
    """
    print("(serving — control the microphone from the web page)")
    armed = False                      # wake word heard, awaiting the question
    last_request = node_settings.load()["listen_request"]

    while True:
        settings = node_settings.load()
        voice = settings["voice"]
        requested = settings["listen_request"] > last_request

        if not voice["enabled"] and not requested:
            node_settings.publish_voice_state("off")
            armed = False
            time.sleep(0.4)
            continue

        # A press on the page always wins, in either mode.
        if requested:
            last_request = settings["listen_request"]
            armed = True

        if voice["mode"] == "button" and not armed:
            node_settings.publish_voice_state("ready", "press to talk")
            time.sleep(0.3)
            continue

        clip = new_clip()
        if armed:
            node_settings.publish_voice_state("listening", "speak now")
            ok = record_until_silence(card, dev, clip, max_seconds=12.0)
        else:
            node_settings.publish_voice_state(
                "waking", f'say "{voice["wake_word"]}"')
            ok = record_fixed(card, dev, clip, 3)
        if not ok:
            clip.unlink(missing_ok=True)
            armed = False   # one press (or one wake word) = one chance to speak
            continue

        node_settings.publish_voice_state("transcribing")
        t0 = time.perf_counter()
        text = transcribe(clip).strip()
        stt_s = time.perf_counter() - t0
        clip.unlink(missing_ok=True)
        if not text:
            armed = False
            continue

        if armed:
            question = text
        else:
            wake = voice["wake_word"].lower()
            if wake not in text.lower():
                print(f'(ignored: "{text}")')
                continue
            question = text.lower().split(wake, 1)[1].strip(" ,.?!")
            if not question:            # just the wake word: listen next round
                armed = True
                print("KAMI: yes? (listening...)\n")
                continue

        node_settings.publish_voice_state("thinking", question[:60])
        answer(llm, status, question, stt_s)
        armed = False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wake", metavar="WORD", default=None,
                    help='wake-word mode (e.g. --wake kami)')
    ap.add_argument("--serve", action="store_true",
                    help="obey the web page's voice settings (recommended)")
    args = ap.parse_args()

    found = find_capture_card()
    if not found:
        sys.exit("No ReSpeaker found. Check `arecord -l`.")
    card, dev = found

    llm = LLMManager()
    status = StatusStore(source="voice")
    llm.check_availability()
    status.update_model(llm.metrics)

    print(f"CommonsClaw voice loop (mic: card {card}, model: {config.MODEL_NAME})")

    try:
        if args.serve:
            serve_loop(llm, status, card, dev)
        elif args.wake:
            wake_word_loop(llm, status, card, dev, args.wake)
        else:
            print("Enter to talk, Enter to stop, Ctrl+C to quit.\n")
            push_to_talk_loop(llm, status, card, dev)
    except KeyboardInterrupt:
        print("\nbye")
    finally:
        node_settings.publish_voice_state("offline")
        status.clear()


if __name__ == "__main__":
    main()
