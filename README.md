# CommonsClaw: a decentralized, hierarchical civic AI infrastructre

**CommonsClaw is the people's AI network** — not one node, but a growing commons
of many small, local, solar-powered nodes, built and maintained by communities that share compute, energy, and data. Each node gives a place a voice and
answers at the _smallest sufficient scale_; local knowledge stays local, and
nodes reach upward to a larger datacenter (neighborhood, city) only when a question truly needs it. 
Energy proportional to the question; negotiated boundaries between tiers and
between communities (for more check the [manifesto](TOWARDS_HIERARCHICAL_CIVIC_AI.md)).

**Not a personal assistant.** Rather than a local-AI assistant such as OpenClaw
(one person, one butler, your chat channels), CommonsClaw is a commons:
each node's memory belongs to a **place and its community** — everyone who
talks to it shares one accumulating identity — and it is
**embodiment-first**: the node _is_ the place, its sensors are its body. The
mechanics overlap (local model, file-based memory, tool use); the politics
and topology are opposite. Full comparison:
[COMMONSCLAW_VS_OPENCLAW.md](COMMONSCLAW_VS_OPENCLAW.md).


This **decentralized, hierarchical agentic infrastructure** was inspired by the [Floating Solar Hydrogen Data Centers](https://github.com/cesarharada/Floating-Solar-Hydrogen-Data-Center) vision of sustainable, scaled-down sovereign datacenters spearheaded by **Cesar Harada** as well as previous works by **Alvaro Cassinelli and Daniel Saakes** on decentralized [Spatial Physical Computing smart sensor-actuator networks](https://alvarocassinelli.com/gluons/) supporting local governance and community making with the support of Project Ceibal in Uruguay in 2015. 


## Hierarchical Civic AI: Public Spaces (Level 1)

**This repo is Level 1 of the hierarchy — the "kami" node:** a solar-powered,
sensor-laden Raspberry Pi 5 that gives a voice to a public place. Visitors
chat with the "spirit of the place" through a voice interface (no internet needed). The node converses, remembers the community's topics (useful to explore the local usage of AIs), and can discuss and analyse its telemetry data. 
A system prototype including a floating platform, embedded LLM (RPi5), solar panels and hydrogen production is being developed in a recent collaboration with **DLX, University of Tokyo by Ido Hoffmann, Federico Trucchia and Yuri Klebanov**. 

| Level | What it is                                                                                                                                                                                                               | Example                         |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------- |
| 0     | Engineered AIoT + tiny "trigger" sub-1B models: pattern recognition, formatting, classification, intent and data collection — elemental conversation or no direct conversation at all with humans, but feeds the level 2 | greenhouse control, gemma3:270m |
| **1** | **Local conversational LLM (this node)** — the kami's voice. A bridge between humans and the environment, a member of the neighborhood, a repository of local, communal knowledge (see below).                           | **llama3.2:1b on a Pi 5**       |
| 2+    | City / nation / world-scale models, queried only when needed                                                                                                                                                             | routed upward                   |

## How it works

```
                        HIGHER LEVELS (city → nation → world models)
                                      ▲   (future: routed queries,
                                      │    negotiated per community)
                                      │
 ┌─────────────────────────── THE NODE (Raspberry Pi 5, solar) ───────────────┐
 │                                                                            │
 │   PEOPLE side                        MEMORY (plain-text files)             │
 │                                                                            │
 │   phone ──Wi-Fi AP "CommonsClaw"──► web chat ──► llm_manager ──► Ollama (LLM)     │
 │  (browser: typing, 🎤 STT,      (no        ▲   │                           │
 │   🔊 TTS — the Pi needs      internet)     │   │ reads on every question   │
 │   no internet at all)                      │   ▼                           │
 │   📝 Note button ─────────────────────►  reports/community_notes.md        │
 │                                            reports/sensor_*_log.md         │
 │   SENSORS side                             sensors/sensor_*.md (per-sensor)│
 │                                            sensors/SENSOR_REPORT.md        │
 │   sensors ──► logger processes ──────────► memory/identity.md (who it is)  │
 │  (I2C, GPIO,    (cron/daemons,            memory/journal.md (its days)     │
 │   LoRa, ...)     auto-collect; the kami                                    │
 │                  can ask for more/less)                                    │
 │                                                                            │
 │   Loggers run on their own schedule and write files automatically. They    │
 │   can also be queried directly for a single fresh reading (`--once`), or   │
 │   — when they are Level-1 agents — asked for a one-line description of     │
 │   their own data ("warm and humid, rising since noon").                    │
 └────────────────────────────────────────────────────────────────────────────┘
```

**Reports and notes** are the node's shared memory, in plain markdown both
humans and the LLM can read. Sensor reports are time-series observations with
a self-describing header (what, where, units, logger config the kami may
suggest tweaking). Community notes are whatever people leave: suggestions,
poll answers, comments, requests — the kami reads them when answering and can
tally or summarize them when asked. The persistent memory (`memory/`) is what
lets the node have continuity: a personality, things it has learned, skills
it has developed — the beginnings of a soul that persists across reboots.

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
are Level-0 candidates (triggers/formatting). Full runs + future Hailo
AI HAT+ numbers: [BENCHMARKS.md](BENCHMARKS.md). Reproduce with
`python3 benchmark.py --all`.

## Features

- Local conversation with a language model (Ollama, fully offline). Default
  `llama3.2:1b`; switchable per-question in the web UI or in
  `config.py:MODEL_NAME`.
- Wi-Fi access point + phone web chat (streaming answers), with captive
  portal (page pops open on join) and optional HTTPS for in-page mic.
- Phone-side STT (Web Speech API) and TTS (speechSynthesis, on by default) —
  the Pi needs no internet.
- **Sensor subprocesses:** independent logger processes (cron/daemon) collect
  telemetry into plain-text files — one self-describing file per sensor in
  `sensors/`, plus a `SENSOR_REPORT.md` dashboard for trends and anomalies.
  Loggers can be queried directly (`--once`) and will later be Level-0 agents
  that can describe their own data in words.
- **Community notes:** visitors leave suggestions, poll answers and comments
  via the 📝 button; the kami reads them when answering and can tally or
  summarize them on request.
- **Persistent memory:** `memory/identity.md` (personality, learned facts,
  skills) + `memory/journal.md` (day-to-day continuity) — the node's soul
  persists across reboots.
- Screenless console mode (auto-fallback when no display).
- CPU, RAM, and temperature monitoring + terminal control view.
- Model benchmark harness with shareable results table.
- Unattended autostart (systemd + AP + boot-to-console).
- **Planned:** communication with _other nodes_ — peers at the same level
  (neighboring parks, nearby greenhouses) and higher levels (city-scale
  models) — with negotiated transactions when queries cross community
  boundaries. The defining open problem of HCA; see
  [COMMONSCLAW_VS_OPENCLAW.md](COMMONSCLAW_VS_OPENCLAW.md) § what HCA must invent.

## Project structure

**LLM core** (shared by every frontend):

- `llm_manager.py` — Ollama availability, streaming responses, per-request
  model override; injects the memory digest into the system prompt.
- `reports_reader.py` — compiles `memory/` + `sensors/` + `reports/` into the
  prompt digest.
- `config.py` — application, model, GUI, and hardware settings.
- `status_store.py` — live status JSON (`/tmp/commonsclaw_status.json`, ephemeral).
- `hardware_monitor.py` — CPU/RAM/temp reader (in-memory; _not_ a logger).
- `control.py` — terminal dashboard reading the status store.

**Interfaces:**

- `main.py` — Tkinter fullscreen GUI; falls back to console mode headless.
- `console.py` — screenless terminal chat frontend.
- `web_server.py` — phone/browser chat (waitress + SSE), `/api/note`,
  captive-portal probe answers, optional `--https`.
- `static/chat.html` — the chat page (streaming, model selector, 🎤/🔊/📝).
- `gui.py` — Tkinter conversation interface (used by `main.py`).

**Sensors & loggers** (separate processes; write plain-text files):

- `loggers/sensor_pivitals.py` — node health (CPU/RAM/temp) via cron.
- `loggers/sensor_solarpower.py` — solar panel + battery (DUMMY data until
  the INA219 is wired).
- `sensors/` — one self-describing file per sensor + `SENSOR_REPORT.md`
  dashboard.
- `reports/` — community notes + running sensor logs.
- `memory/` — `identity.md` (who the kami is) + `journal.md` (continuity).

**Operations:**

- `ap_up.sh` / `ap_down.sh` — Wi-Fi access point on/off.
- `portal_up.sh` / `portal_down.sh` — captive portal on/off.
- `install_autostart.sh` + `commonsclaw-web.service` — systemd boot autostart.
- `make_cert.sh` — self-signed HTTPS cert (enables the in-page mic).
- `push_to_pi.sh` — rsync dev workflow (Mac → Pi).
- `benchmark.py` — model benchmarks → `BENCHMARKS.md`.

**Docs:** `PLAN.md` (roadmap), `SETUP_RPI5.md`, `ENVIRONMENT_LOG.md`,
`TOWARDS_HIERARCHICAL_CIVIC_AI.md` (vision), `COMMONSCLAW_VS_OPENCLAW.md`,
`BENCHMARKS.md`, `CREDITS.md`, `DEVELOPMENT_LOG.md`.

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
status to `/tmp/commonsclaw_status.json` in both modes.

### Web interface (Phase 2A/2B)

A phone/browser chat is served by:

```bash
python3 web_server.py
```

Then open `http://<pi-host-or-ip>:8080` on a phone or laptop. With the Wi-Fi
access point up (Phase 2B, `sudo bash ap_up.sh`), a phone joins the `CommonsClaw`
network and opens `http://10.42.0.1:8080`. Requires `flask` and, for
stability, `waitress` (`sudo apt install python3-flask python3-waitress`).

#### How voice works (all on the phone, none on the Pi)

- **STT (🎤 mic button):** uses the browser's **Web Speech API**. The phone's
  browser does the speech-to-text (Chrome/Android uses Google's servers) and
  sends plain _text_ to the Pi. **The Pi needs no internet connection** — this
  is the whole point of the design.
- **Phone internet while on the AP:** the `CommonsClaw` network has no internet, but
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

Solar floating datacenters concept: **Cesar Harada**. Concept and lead development of CommonsClaw : **Alvaro Cassinelli and Cesar Harada**. Seed code ("SSAI"): **Ido Hoffmann** et al., DLX,
University of Tokyo. Full history and credits: [CREDITS.md](CREDITS.md).

## License

- **Hardware:** [CERN Open Hardware Licence, Version 2 — Strongly Reciprocal (CERN-OHL-S v2)](https://github.com/cesarharada/Floating-Solar-Hydrogen-Data-Center/blob/main/LICENSE).
- **Accompanying software** (firmware, dashboards, data pipelines): see `CONTRIBUTING.md` for the compatible permissive licence (typically a copyleft-compatible OSI licence such as GPLv3) chosen per sub-directory.
- **Documentation, diagrams, and text in this README:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0), unless otherwise marked.
