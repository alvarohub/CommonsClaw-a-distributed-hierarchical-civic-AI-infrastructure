# Development Log

This document records the main work on the CommonsClaw node (formerly the
SSAI prototype), organized by date.

## 2026-09-27 (2)

- **Memory folders reorganized to match the three toggle categories**:
  `identity/` (identity.md + journal.md), `sensors/` (one file per sensor +
  `index.md` dashboard + mic_calibration.md), `community/` (notes.md).
  `reports/` and `memory/` dissolved; duplicate sensor log removed; the
  dashboard groups files into labeled, rounded category boxes (icon + title +
  one-liner), plain filenames inside.
- **Sensor registry**: `sensors.json` (machine-readable: id, logger, log
  file, interval, active flag, params) + `sensors_boot.py` (spawns one
  supervisor per active logger at boot; crash-isolated) +
  `commonsclaw-sensors.service` (in install_autostart.sh).
- **Mechanical journal**: every completed turn is appended to
  `identity/turn_log.jsonl` by the status store; `journal_writer.py` (cron
  23:55) writes the day's entry — world: per-sensor min/max/avg; talk:
  question count + top topic words. The LLM-consolidation layer (per-sensor
  analyst reports, global state-of-place synthesis) is deferred to Level 2+
  by design — the journal format is the handoff.
- Voice UX: push-to-talk is now Enter→speak→pause (silence stops recording),
  with listening/transcribing/thinking status in the console; 🙂/🐢 speaker
  icons and turtle-green answers in the web UI; voice turns render live on
  connected pages.

## 2026-09-27

- **Phase 3 steps 3-4 DONE: the full voice loop.** `voice/talk.py` — a
  frontend like console.py, but voice-first: Enter→speak→Enter, whisper
  transcribes, `LLMManager.stream_response()` answers token by token, and the
  turn is published to the status store. **Voice turns now appear in the web
  UI**: `/api/status` carries the latest completed turn + question_count id
  (read from the shared status FILE, since talk.py is a separate process);
  the page dedupes and renders them as 🎤 question / KAMI answer lines (and
  speaks them if TTS is on). **Wake-word mode**: `--wake kami` — 2.5 s
  listening windows, whisper spots the wake word, the remainder of the
  utterance (or the next one) becomes the question.
- **Phase 3 steps 1-2 DONE: the node hears.** ReSpeaker 4 Mic Array detected
  as card 3 (`ArrayUAC10`, UAC1.0 firmware — no hardware AEC/DOA in this
  variant; flashable later). `voice/mic_setup.py` written: finds the card,
  sets gain (`--gain 90`), records, judges levels, transcribes — and logs
  everything to `reports/mic_calibration.md` (tweaks never lost; the kami
  can read its own hearing history). faster-whisper `tiny` in
  `~/voice-venv`: **0.8 s for a 4 s clip (~5× realtime)**, correct English
  transcript on first try.

## 2026-09-25 (evening 3)

- **Memory categories with toggles + keyword routing.** Diagnosed a 45 s
  "hello": generation was 1.8 s (7.89 tok/s) but prompt-eval chewed the whole
  memory digest every question. Now three toggleable categories — 🧠 identity,
  📡 sensors, 📝 community — in the status bar; off = bare prompt = full
  speed. Slash keywords force one on (`/sensors how warm is the pond`), and
  auto-detect keywords ("temperature", "remember", ...) enable the matching
  category transparently. Digest also slimmed (1000 chars/file, 3000 total).
  Verified: routing unit tests, compile, JS check; pushed + service restarted.

## 2026-09-25 (evening 2)

- **De-SSAI rename, complete.** `gui.py` → `lcd_gui.py` (it is the monitor
  GUI); program name, service (`commonsclaw-web.service`), AP profile
  (`commonsclaw-ap`), Wi-Fi SSID (`CommonsClaw`), status file
  (`/tmp/commonsclaw_status.json`), Pi path (`~/commonsclaw`), thread/class
  names all renamed. Historical mentions intentionally kept in this log and
  CREDITS.md (accurate provenance). Old service removed on the Pi; new one
  installed and **verified running**.
- **Closed the dev loop:** sudoers drop-in
  (`/etc/sudoers.d/commonsclaw-restart`, scoped to only `systemctl restart
commonsclaw-web`) makes `./push_to_pi.sh` fully passwordless — rsync +
  service restart in one command. Verified end-to-end.
- Upstream-code audit (for the credits discussion): 4 of 7 upstream files
  byte-unchanged (`lcd_gui.py`, `control.py`, `hardware_monitor.py`,
  `status_store.py`); 836 new Python lines vs 1,036 upstream; all new
  capability (web chat, AP, memory, benchmarks) is ours.

## 2026-09-25 (afternoon 4)

- **Naming coherence + project-structure cleanup.** Renamed the example
  logger family to the `sensor_*` convention: `loggers/sensor_pivitals.py`
  (was pi_vitals.py), `reports/sensor_pivitals_log.md`,
  `sensors/sensor_pivitals.md` (git mv, history preserved). Added the dummy
  `loggers/sensor_solarpower.py` (simulated panel/battery day-night curve —
  placeholder until the INA219 is wired) writing `sensors/sensor_solarpower.md`.
  README project structure reorganized by function (LLM core / interfaces /
  sensors & loggers / operations / docs), with a note that
  `hardware_monitor.py` is an in-memory reader for the live status store
  while loggers are the persistent writers. Digest verified: identity,
  SENSOR_REPORT, both sensor files, community notes, sensor log all in prompt.

## 2026-09-25 (afternoon 3)

- **Sensors folder + dashboard + persistent memory.** `sensors/` holds one
  self-describing file per sensor + `SENSOR_REPORT.md` (trends/anomalies/
  kami notes dashboard). `memory/` = the node's persistent identity
  (`identity.md`: name, personality, learned facts, skills) and `journal.md`
  (continuity across reboots) — the beginnings of personality for the kami.
  `reports_reader.py` now digests all three sources (identity → sensors →
  reports) into the system prompt; `pi_vitals.py` mirrors readings into
  `sensors/pi_core_temp.md`. README gained an ASCII architecture schematic
  (people side / sensors side / memory / hierarchy) and prose explaining
  logger processes and community notes.
- Researched OpenClaw for comparison (personal assistant gateway, MIT,
  huge ecosystem) — see notes in chat: our node differs in being communal
  (shared place memory vs personal), hierarchical (levels negotiate), and
  embodiment-first (voice of a place, not a channel butler).

## 2026-09-25 (afternoon 2)

- **Web UI: speaker default-on, per-request model selector.** New
  `GET /api/models` lists installed Ollama models; `/api/ask` accepts a
  `model` override (LLMManager.stream_response gained a per-call `model`
  param; metrics track the actual model used). Dropdown in the status bar.
- **HTTPS option for the in-page mic**: `make_cert.sh` (self-signed cert with
  SANs for 10.42.0.1/192.168.2.13) + `web_server.py --https` on port 8443.
  (HTTPS falls back to the Flask server — waitress has no TLS.)
- **Captive portal (Option B)**: `portal_up.sh`/`portal_down.sh` write a
  wildcard-DNS dnsmasq snippet for nmcli shared mode; `web_server.py` answers
  OS portal probes (`/generate_204`, `/hotspot-detect.html`, `/ncsi.txt`) so
  phones pop the chat open on joining `SSAI`. Needs on-phone test.
- **Phase 2C scaffolded — shared memory via plain-text reports.**
  `reports/` (with `_INDEX.md`, `pi_vitals.md`, `community_notes.md`),
  `loggers/pi_vitals.py` (cron-able), `reports_reader.py` (truncated digest),
  injected into the system prompt on every question. 📝 button on the page →
  `POST /api/note` appends to community_notes.md. MCP deferred deliberately —
  plain files first, MCP can replace the reader without format changes.
- Verified: compile clean, JS check, note endpoint, digest, prompt injection.

## 2026-09-25 (night 2)

- **Project renamed: HCA_PublicPlace**, Level 2 of the "Hierarchical Civic AI:
  the people's AI network" project (SSAI was the intern-era prototype name).
  README rewritten with the vision, the level structure (0 = engineered AIoT,
  1 = sub-1B trigger models, 2 = this conversational node, 3+ = routed upward),
  and the design principle (smallest sufficient scale). Code will eventually
  move into an HCA_PublicPlace/ subfolder of the larger HCA repo (not yet on
  GitHub). Notion page exists but is private (Augmented Materiality workspace).
- **Full model ladder benchmarked** (benchmark.py, rigorous 100-token runs):
  gemma3:270m = 35.7 tok/s (TTFT 0.05s), qwen2.5:0.5b = 26.0 (0.04s),
  llama3.2:1b = 8.1 (0.13s), phi3.5 = 5.0 (0.20s). Sub-1B models are ~7x
  faster than phi3.5 and feel instant — confirms the internet claim.
- **Vision recorded.** Alvaro articulated the project goal: the node is a
  "kami" (spirit of a place) — solar-powered, sensor-laden, embedded in a
  public park in Japan, part of a "hierarchical civic AI datacenter"
  architecture (local tiny model → city → nation → world, energy proportional
  to the question, privacy firewalls between tiers). Verbatim statement +
  technical commentary in TOWARDS_HIERARCHICAL_CIVIC_AI.md.
- **Two-tier model idea** (fits the vision): gemma3:270m/qwen2.5:0.5b =
  always-on voice (chit-chat, sensors), llama3.2:1b = deep tier, keyword/
  complexity router between them. To be prototyped.

## 2026-09-25 (night)

- **Performance baseline established.** phi3.5 on this Pi 5 (16 GB) =
  **~5.2 tok/s generation** (raw Ollama benchmark, no SSAI code involved).
  TTFT ~0.8 s warm, ~8.5 s cold (model load). A "what is a differentiable
  manifold" answer takes ~30 s mostly due to prompt eval + length at 5 tok/s.
- **Verified the slowness is hardware, not our code:** Ollama bench gives the
  identical 5.19 tok/s directly; `OLLAMA_NUM_THREAD=4` service override made
  no difference (Ollama was already threading; the ~31% CPU seen in `ps` was
  a momentary sample). Wall = Pi 5 memory bandwidth (~17 GB/s shared). An
  accelerator, or a smaller model (llama3.2:1b / gemma2:2b) for voice latency,
  are the real levers — deferred to Phase 3 decision.
- Desktop environment (labwc) is running but idle (0% CPU) — harmless; set
  boot-to-console later for the headless installation.
- **UI: added "MODEL is thinking…" indicator** (animated dots) + pulsing
  status dot while generating, cleared on first chunk — slow no longer looks
  dead. Fixed SSE trailing-event flush and a too-aggressive 30 s watchdog
  (Ollama legally stalls >30 s mid-answer; watchdog now only fires if zero
  chunks arrive within 60 s of send).

- **Switched default model to llama3.2:1b** (config.py, one-line flip back to
  phi3.5 kept as comment). Measured on emotionpi: **llama3.2:1b ≈ 8.4 tok/s**
  vs phi3.5's 5.2 tok/s = 62% faster (smaller models gain less than parameter
  ratio suggests — memory bandwidth binds them less efficiently). Both models
  remain installed on the Pi for A/B testing.

- **Added benchmark tooling + autostart.** `benchmark.py` (warm-up + 3 timed
  runs of a fixed prompt per model; records avg/best tok/s, warm TTFT, wall,
  temp; appends rows to `BENCHMARKS.md` — shareable table for collaborators,
  incl. future Hailo AI HAT+ rows). `install_autostart.sh` + `ssai-web.service`:
  web server starts at boot (after Ollama health check), boot-to-console
  (frees ~250 MB), AP profile autoconnects. Undo with `--uninstall`.
  On config format: keeping `config.py` (imported everywhere, supports
  comments; YAML would add a dependency for no functional gain).

## 2026-09-25 (evening)

- **Phase 2B working end-to-end.** Set Wi-Fi country `HK`, ran
  `sudo bash ap_up.sh` → AP `SSAI` up, Pi at `10.42.0.1`. Phone joined the
  network and the web chat works from the phone at `http://10.42.0.1:8080`.
  Ethernet dev link to the Mac stayed up in parallel (SSH/rsync unaffected).
- **Stability fix: switched the web server to waitress.** The page/SSH
  intermittently dropped (`Connection reset by peer`, `pgrep` showed
  `web_server.py` fully dead). Hardware ruled out (`throttled=0x0`, 53 °C, no
  OOM). Root cause: Flask's built-in dev server dies on dropped client
  connections (phone sleep / AP "no internet" radio flap). Now
  `web_server.py` serves via **waitress** (production WSGI, `threads=8`) with
  a graceful fallback to the dev server + warning if waitress is absent; SSE
  generator wrapped so a generation error can't kill the stream. Requires
  `sudo apt install python3-waitress` on the Pi.
- Gotcha hit + resolved: browser initially said "refused to connect" — the
  AP was up but `web_server.py` wasn't running yet. It does not autostart.
- **Architecture fix: per-request answer streaming.** Symptom: phone showed
  `MODEL:` but no answer, Pi CPU idle. Root cause: the old design used ONE
  shared `/api/stream` EventSource + a global `_pending_question`, so an
  answer was streamed to whichever client connection was alive — a phone
  EventSource reconnect (screen lock / radio flap) made chunks go nowhere.
  Now `POST /api/ask` returns the SSE stream for its own question (fetch +
  manual SSE parse in `chat.html`); the asking client is guaranteed its own
  answer. Shared `/api/stream` and the pending-question plumbing removed;
  single-slot busy logic kept (second asker gets an inline `busy` event).
  Verified with Flask test client (status 200, empty 400, ask → SSE events).
- Open follow-up: make `web_server.py` survive SSH logout / reboot (systemd),
  and record Phase 1 baseline metrics.

## 2026-09-25

- **Phase 1 (replication) working on the Pi.** Installed Ollama on
  `emotionpi` (CPU-only mode, service active), pulled `phi3.5:latest`
  (2.2 GB), verified `ollama run` answers. rsynced the code to `~/ssai`,
  installed `flask`. `python3 console.py` runs headless and streams real
  answers (first live question: "do makers dream of electric turtles?").
- **Phase 2A (web chat) verified on the Pi.** `python3 web_server.py` serves
  the page; Mac browser at `http://192.168.2.13:8080` streams answers.
  Flask installed via `sudo apt install python3-flask` (Bookworm blocks pip —
  updated SETUP_RPI5.md to include it in the apt line).
- Networking settled: Mac↔Pi over Ethernet with Internet Sharing ON; Pi got
  DHCP lease `192.168.2.13` on `bridge100` (Mac is `192.168.2.1`). mDNS
  (`emotionpi.local`) is unreliable across the bridge → use the numeric IP.
  Monitor+keyboard attached to the Pi for direct checks.
- Added `push_to_pi.sh` (Mac-side): rsyncs the repo to the Pi incrementally
  (`./push_to_pi.sh`, override with `PI_HOST=...`). This is the dev workflow:
  edit in VS Code on the Mac, push with rsync, no git clone on the Pi.
- **Phase 2B started (Wi-Fi AP, Option A).** Added `ap_up.sh` / `ap_down.sh`:
  nmcli `shared`-mode AP on `wlan0` (Pi serves DHCP at `10.42.0.1`), eth0
  dev link untouched. Web chat then reachable from phones at
  `http://10.42.0.1:8080`. Captive portal (Option B) deferred but planned.
- Next: bring the AP up, test chat from a phone, record Phase 1 baseline
  metrics (TTFT / tok/s / temp).

## 2026-09-20

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
