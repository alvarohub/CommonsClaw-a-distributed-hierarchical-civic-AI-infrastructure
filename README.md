# HCA_PublicPlace

**A "kami" node: a solar-powered, sensor-laden Raspberry Pi 5 that gives a
voice to a public place** — visitors chat with the spirit of the park itself
over a Wi-Fi access point, no internet needed.

First steps toward the **Floating Solar Hydrogen Data Centers** vision
spearheaded by [Cesar Harada](https://github.com/cesarharada/Floating-Solar-Hydrogen-Data-Center),
and a sustainable, distributed **Hierarchical Civic AI: the people's AI
network** infrastructure by **Alvaro Cassinelli**, in a recent collaboration
with DLX, University of Tokyo. Part of the tech development is happening in a
sister repository at DLX, University of Tokyo (Ido Hoffmann et al.).
See [Credits](#credits) at the end.

## The hierarchy

This repo is **Level 2** of the hierarchy — a small local LLM (Ollama) that
converses, remembers the community's topics, and knows its local telemetry:

| Level | What it is                                                        | Example                               |
| ----- | ----------------------------------------------------------------- | ------------------------------------- |
| 0     | Engineered AIoT: pattern recognition, ML without language         | greenhouse control, anomaly detection |
| 1     | "Basic trigger" sub-1B models: formatting, classification, intent | gemma3:270m, qwen2.5:0.5b             |
| **2** | **Local conversational LLM (this node)** — the kami's voice       | **llama3.2:1b on a Pi 5**             |
| 3+    | City / nation / world-scale models, queried only when needed      | routed upward                         |

Design principle: use the _smallest sufficient scale_ — energy proportional
to the question, privacy firewalls between tiers, local knowledge stays
local. See [TOWARDS_HIERARCHICAL_CIVIC_AI.md](TOWARDS_HIERARCHICAL_CIVIC_AI.md)
for the full vision.

## Status

Active prototype, functional end-to-end: phone joins the Pi's Wi-Fi AP →
opens a chat page → talks to a local model. The default model is
`llama3.2:1b` (fastest of the conversational models measured; set in
`config.py:MODEL_NAME`). Roadmap in [PLAN.md](PLAN.md). Setup in
[SETUP_RPI5.md](SETUP_RPI5.md).

## Benchmarks (measured on emotionpi, Pi 5 16 GB, CPU-only)

| Model                     | tok/s   | warm TTFT | 100-token answer |
| ------------------------- | ------- | --------- | ---------------- |
| gemma3:270m               | 35.7    | 0.05 s    | ~1 s             |
| qwen2.5:0.5b              | 26.0    | 0.04 s    | ~2.6 s           |
| **llama3.2:1b** (default) | **8.1** | 0.13 s    | ~11 s            |
| phi3.5 (3.8B)             | 5.0     | 0.20 s    | ~20 s            |

Sub-1B models are ~7x faster but too shallow for real conversation — they
are Level-1 candidates (triggers/formatting). Full runs + future Hailo
AI HAT+ numbers: [BENCHMARKS.md](BENCHMARKS.md). Reproduce with
`python3 benchmark.py --all`.

## Features

- Local conversation with a language model (Ollama, fully offline). Default
  `llama3.2:1b`; switch in `config.py:MODEL_NAME`.
- Wi-Fi access point + phone web chat (streaming answers).
- Phone-side STT (Web Speech API) and TTS (speechSynthesis) — the Pi needs
  no internet.
- Screenless console mode (auto-fallback when no display).
- CPU, RAM, and temperature monitoring + terminal control view.
- Model benchmark harness with shareable results table.
- Unattended autostart (systemd + AP + boot-to-console).

## Project structure

- `main.py` - Starts the application, coordinates the main components, and
  falls back to console mode when no display is available.
- `console.py` - Screenless terminal chat frontend (used over SSH or when
  Tkinter/a display is missing); shares the status store with `control.py`.
- `web_server.py` - Serves the phone/browser chat (waitress + SSE).
- `benchmark.py` - Benchmarks Ollama models (tok/s, TTFT) and appends rows
  to `BENCHMARKS.md`.
- `ap_up.sh` / `ap_down.sh` - Bring the Wi-Fi access point up/down.
- `install_autostart.sh` - Installs systemd autostart (web server at boot,
  boot-to-console, AP autoconnect).
- `gui.py` - Implements the Tkinter conversation interface.
- `llm_manager.py` - Checks Ollama availability and streams model responses.
- `hardware_monitor.py` - Reads CPU, RAM, and temperature data.
- `status_store.py` - Writes shared status data to a JSON file.
- `control.py` - Displays shared status in a terminal view.
- `config.py` - Contains application, model, GUI, and hardware settings.
- `DEVELOPMENT_LOG.md` - Daily development log describing completed work.
- `LICENSE` - MIT license.

## Requirements

The current implementation requires:

- Linux (developed on Raspberry Pi OS Bookworm, Pi 5 16 GB).
- Python 3 (≥ 3.10).
- Tkinter (optional — without it, `main.py` runs in console mode).
- The Python packages `requests`, `psutil`, `flask`, `waitress`.
- Ollama running locally at `http://127.0.0.1:11434`.
- An Ollama model installed (default `llama3.2:1b`; see
  [BENCHMARKS.md](BENCHMARKS.md) for alternatives measured on the Pi 5).

The repository does not currently include a dependency manifest such as
`requirements.txt` or `pyproject.toml`.

## Setup

1. Install Python 3 and Tkinter for the operating system.
2. Install the Python packages `requests` and `psutil`.
3. Install and start Ollama.
4. Make sure the `phi3.5:latest` model is available in Ollama.
5. Review [config.py](config.py) if the model name or Ollama address needs to
   change.

The exact package-manager commands are intentionally not documented yet because
the repository does not define a specific Linux distribution or installation
method.

## Running

Start the main application:

```bash
python3 main.py
```

If a display is available it opens the fullscreen Tkinter interface; if not
(headless Pi, SSH session), it automatically starts a console chat instead.
You can also force the console frontend directly with `python3 console.py`.
The application checks Ollama, and periodically writes hardware and model
status to `/tmp/ssai_status.json` in both modes.

### Web interface (Phase 2A/2B)

A phone/browser chat is served by:

```bash
python3 web_server.py
```

Then open `http://<pi-host-or-ip>:8080` on a phone or laptop. With the Wi-Fi
access point up (Phase 2B, `sudo bash ap_up.sh`), a phone joins the `SSAI`
network and opens `http://10.42.0.1:8080`. Requires `flask` and, for
stability, `waitress` (`sudo apt install python3-flask python3-waitress`).

#### How voice works (all on the phone, none on the Pi)

- **STT (🎤 mic button):** uses the browser's **Web Speech API**. The phone's
  browser does the speech-to-text (Chrome/Android uses Google's servers) and
  sends plain _text_ to the Pi. **The Pi needs no internet connection** — this
  is the whole point of the design.
- **Phone internet while on the AP:** the `SSAI` network has no internet, but
  a phone stays online over its **cellular (LTE) SIM** at the same time —
  both Android and iOS do this automatically ("smart network switch" /
  "Wi-Fi Assist"). So STT audio goes out over LTE while the page talks to the
  Pi over Wi-Fi.
- **Offline STT:** some phones transcribe fully on-device (recent iPhones via
  on-device Siri dictation, Pixels/newer Android with on-device speech
  models), so on capable hardware even STT is local.
- **TTS (🔊 speaker toggle):** answers are spoken with the browser's
  `speechSynthesis` — also on the phone, also needing nothing from the Pi.

#### Secure-context caveat for the mic button

The Web Speech API generally requires a **secure context (HTTPS)**. Over plain
`http://10.42.0.1:8080` the in-page 🎤 button may be blocked in Chrome/Safari.
The **fallback always works**: the phone keyboard's own dictation mic types
into the chat field (no permissions needed). Enabling the in-page mic means
adding a self-signed HTTPS cert — see open decision 2 in [PLAN.md](PLAN.md).

In a separate terminal, start the control view:

```bash
python3 control.py
```

### Benchmarking models

```bash
python3 benchmark.py --all        # every installed model
python3 benchmark.py gemma2:2b    # a specific model
```

Results are appended to [BENCHMARKS.md](BENCHMARKS.md) (shareable table).

### Unattended operation

```bash
sudo bash install_autostart.sh
```

Installs a systemd service that starts the web server at boot (after Ollama),
sets boot-to-console, and makes the AP autoconnect. After a reboot the chat
is live at `http://10.42.0.1:8080` with no login needed. Undo with
`sudo bash install_autostart.sh --uninstall`.

The control view reads the shared status file and refreshes every 0.5 seconds.
Hardware samples are collected by the main application every 15 seconds, so
the faster control refresh also shows question and generation-state changes
promptly without increasing hardware sampling frequency. Press `Ctrl+C` to
close it.

## Configuration

The main settings are in [config.py](config.py), including:

- Ollama address and model name.
- Response generation limits.
- Conversation history.
- GUI appearance and fullscreen mode.
- Hardware and status refresh intervals.
- The technician exit shortcut.

The default technician exit shortcut in the graphical interface is
`Ctrl+Alt+Q`.

## Current limitations

- The project is currently a prototype focused on the Raspberry Pi/Linux
  environment.
- Ollama must be available locally before model responses can be generated.
- The GUI is configured for fullscreen operation by default; on a headless
  system the console frontend is used instead.
- Hardware temperature monitoring uses the Linux path configured in
  `config.py`.
- The repository does not currently include automated tests or a CI workflow.
- Installation is not yet captured in a dependency or environment manifest.

## Credits

Concept and lead development: **Alvaro Cassinelli** — with **GitHub Copilot**
(AI pair-programmer). Seed code ("SSAI"): **Ido Hoffmann** et al., DLX,
University of Tokyo. Solar floating datacenter concept: **Cesar Harada**.
Full history and credits: [CREDITS.md](CREDITS.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
