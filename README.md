# SSAI

SSAI is a local AI conversation system designed for a Raspberry Pi 5. It uses
Ollama to run a local language model and provides a simple Tkinter interface for
conversation and system monitoring.

## Status

This project is an active prototype. The current configuration targets a Linux
system with a local Ollama server and the `phi3.5:latest` model.

## Features

- Local conversation with a language model.
- Streaming model responses in the graphical interface.
- Optional conversation history.
- CPU, RAM, and temperature monitoring.
- A separate terminal control view for hardware and model status.

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

- Linux.
- Python 3.
- Tkinter (optional — without it, `main.py` runs in console mode).
- The Python packages `requests` and `psutil`.
- Ollama running locally at `http://127.0.0.1:11434`.
- The model `phi3.5:latest` installed in Ollama.

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

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
