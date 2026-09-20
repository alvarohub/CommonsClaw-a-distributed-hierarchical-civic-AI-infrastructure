# Development Log

This document records the main work completed on SSAI, organized by date.

## 2026-09-20

- Built Phase 2A: `web_server.py` (Flask + SSE) serving `static/chat.html`.
  Routes: `GET /`, `POST /api/ask`, `GET /api/stream` (chunk/done/error/busy),
  `GET /api/status`. Single generation slot; second client gets a "busy" event.
  Reuses `LLMManager`/`HardwareMonitor`/`StatusStore` so `control.py` and
  `console.py` still work alongside.
- Web page: dark phone-first chat, streaming token render, per-turn metrics,
  live status bar. 🎤 Web Speech API dictation (browser transcribes, text sent
  to the Pi — the Pi needs no internet) and 🔊 TTS toggle via speechSynthesis.
- Verified all routes with a Flask test client (`/` 200, `/api/status` 200,
  `/api/ask` 200/400). Requires `flask` (installed for the project's Python).
- Added `ENVIRONMENT_LOG.md`: hardware (Pi 5, 16 GB, fan, headless), identity
  (`admin@emotionpi`), network topology (Ethernet+Internet Sharing preferred,
  Wi-Fi LAN fallback), and connection-status findings.
- Note: `emotionpi.local` did not resolve on 2026-09-20 — Internet Sharing was
  not active on the Mac and the Pi was not on the network. See
  `ENVIRONMENT_LOG.md` for diagnosis and next actions.

## 2026-09-17

- Added `SETUP_RPI5.md`: step-by-step replication guide for a fresh
  Raspberry Pi 5 (64-bit OS, SSH setup, Ollama install, pulling the
  `phi3.5:latest` model that is not in the repo, apt-based Python deps,
  optional autostart, troubleshooting).
- Added `PLAN.md`: three-phase roadmap — (1) replicate and measure a
  performance baseline, (2) web chat interface, then Wi-Fi access point
  with phone-side STT/TTS, (3) on-device microphone + speaker for fully
  local voice interaction. Open decisions are numbered in the plan.
- Added `console.py`: screenless chat frontend (stdin/stdout, streaming
  answers, per-turn metrics line) sharing `LLMManager`, `HardwareMonitor`
  and `StatusStore`, so `control.py` works alongside it.
- `main.py` now falls back to console mode when Tkinter or a display is
  unavailable (headless/SSH use) instead of crashing; the Tkinter GUI is
  unchanged when a monitor is attached. No LCD in this setup, so console
  mode is the Phase 1 default; verified with a no-display smoke test.
- Updated `README.md` (console mode, optional Tkinter) and reworked
  `SETUP_RPI5.md` / `PLAN.md` for the screenless default; Phase 2 split
  into 2A (web chat on LAN) and 2B (Wi-Fi AP + phone voice).

## 2026-09-15

- Reviewed all Python modules for syntax and consistency.
- Verified that every Python source file compiles successfully with
  `python3 -m compileall`.
- Fixed generation state cleanup so a communication or generation error cannot
  leave the application stuck with new questions blocked.
- Improved the terminal control dashboard so completed turns remain visible
  while the live hardware section is refreshed.
- Kept hardware sampling at 15-second intervals while allowing the control
  dashboard to refresh every 0.5 seconds.
- Updated the control-view documentation to describe the separate hardware
  sampling and dashboard refresh intervals.
- Ran a startup smoke test for `control.py` and verified the final diff with
  `git diff --check`.

Add a new dated section at the top of this file for future work days.
