# CommonsClaw — Plan of Record

Living document. Decisions are recorded here (not in chat). Update the dated
log at the bottom as phases progress; tweak phases freely as we learn.

**Goal:** a self-contained local-LLM conversation node on a Raspberry Pi 5.
Interaction evolves from (1) a screenless console baseline over SSH, to
(2) any smartphone over the Pi's own Wi-Fi access point, to (3) fully
self-contained voice (microphone + speaker on the Pi).

**Starting point:** fork of `dlx-designlab/ssai` V4 — Tkinter fullscreen GUI +
Ollama (`phi3.5:latest`) + terminal status dashboard. `LLMManager`,
`StatusStore` and `HardwareMonitor` are UI-independent and get reused in
every phase. There is **no LCD** in this setup; a monitor + keyboard can be
attached temporarily for the GUI and for Phase 2A browser testing.

---

## Phase 1 — Replication and baseline (screenless)

**Scope:** get the repo running on the Pi and measure a baseline before
touching anything. **No LCD:** the Pi runs headless and is operated over
SSH. Done: `console.py` (screenless chat frontend) + automatic console
fallback in `main.py` when Tkinter or the display is missing — the Tkinter
GUI still works unchanged when a monitor is attached.

**Steps:** follow [SETUP_RPI5.md](SETUP_RPI5.md).

**Acceptance criteria:**

- [x] Ollama serves `phi3.5:latest`; console chat answers questions over SSH
      (verified 2026-09-25 on `emotionpi`, 16 GB).
- [ ] With a monitor attached, `python3 main.py` opens the GUI as before.
- [ ] `control.py` over SSH shows live hardware + per-turn metrics.
- [ ] Baseline metrics recorded below (5 sample questions, after warm-up).

**Baseline measurements (2026-09-25, emotionpi):**

| Metric                     | Value              |
| -------------------------- | ------------------ |
| Pi RAM (4/8/16 GB)         | 16 GB              |
| Model                      | llama3.2:1b        |
| TTFT (warm)                | ~0.8 s             |
| TTFT (cold, model load)    | ~8.5 s             |
| Tokens/s (raw Ollama)      | ~8.4 (phi3.5: 5.2) |
| Time for a ~50-word answer | ~15–30 s           |
| RAM used with model loaded | ~4.1 GB            |
| CPU temp after 5 turns     | ~54 °C             |
| Boot-to-ready time         |                    |

Note: 5.2 tok/s confirmed as the hardware ceiling (memory bandwidth), not a
code/config issue — `OLLAMA_NUM_THREAD=4` unchanged. Smaller model or
accelerator is a Phase 3 decision.

---

## Phase 2 — Web chat interface (split into 2A local and 2B access point)

**Goal:** no keyboard, no app, no internet. A simple chat-like web page
served by the Pi replaces the LCD + keyboard. Split into two steps so each
is testable on its own:

### Phase 2A — Web chat on the local network (LAN first)

The Pi serves the chat page over the existing home network — no access
point yet. Testable immediately with the temporarily attached
monitor + keyboard (Pi's own browser at `http://localhost:8080`) and from
the laptop (`http://commonsclaw.local:8080`). Functionally this **is** the whole
interaction upgrade; 2B is "just" the networking around it.

### 2A.1 Web server on the Pi — BUILT (`web_server.py`)

- Flask + SSE, served by **waitress** (production WSGI; dev server proved
  unstable with dropping phone clients). Routes: `GET /` (page),
  `POST /api/ask` (submit **and** stream that question's answer as SSE:
  start/chunk/done/busy/error), `GET /api/status`.
- **Per-request streaming:** the answer travels on the asker's own POST
  response — no shared broadcast, so a phone reconnect can't lose an answer.
- Reuses `LLMManager` (Ollama streaming), `HardwareMonitor`, `StatusStore`
  unchanged → `control.py` keeps working; `console.py` remains as the
  debug frontend.
- **Framework decision: Flask + SSE** (chosen — minimal deps, matches style).
- **Concurrency:** single generation slot (`_generation_lock`); a second
  asker gets an inline `busy` event instead of a parallel generation.

### 2A.2 Chat web page — BUILT

- `static/chat.html`: vanilla single-page chat, dark phone-first UI,
  `ME:` / `MODEL:` transcript, streaming token render, per-turn metrics line,
  live status bar (model + CPU/RAM/temp).
- **STT:** 🎤 button via the Web Speech API (`SpeechRecognition`) — the
  browser transcribes (Chrome uses Google's servers; phone's LTE covers the
  internet leg), text lands in the input and auto-sends. Auto-disabled where
  unsupported (Firefox). **TTS:** 🔊 toggle speaks answers via
  `speechSynthesis`. Neither needs a Pi internet connection.

**Acceptance criteria (2A):**

- [x] Page + API routes verified (`/`, `/api/status`, `/api/ask`, `/api/stream`)
- [ ] Pi's own browser (attached monitor) and a laptop browser both complete
      a streamed Q→A round trip at `http://emotionpi.local:8080`.
- [ ] Second client gets a clean "busy" state, not an error.
- [ ] `control.py` and `console.py` still work alongside.

### Phase 2B — Wi-Fi access point (visitor phones)

The Pi broadcasts its own network; a visitor joins it and opens the same
2A page. Speech-to-text and text-to-speech use the **phone's**
capabilities, so this phase needs no new Pi hardware.

#### 2B.1 Access point mode — scripts ready (Option A)

- Implemented as `ap_up.sh` / `ap_down.sh` (nmcli `shared`-mode AP on `wlan0`,
  profile ). Run on the Pi: `sudo bash ap_up.sh [SSID] [PASSWORD]`
  (defaults `CommonsClaw` / `emotionpi`). Pi serves DHCP and is reachable at
  `10.42.0.1`; chat at `http://10.42.0.1:8080`.
- **eth0 (Mac dev link) is untouched** → SSH/rsync keep working while the AP
  runs. This is why the Ethernet setup was worth it.
- Make persistent across reboots (profile has autoconnect) and disable Wi-Fi
  power save; set Wi-Fi country once: `sudo raspi-config nonint do_wifi_country FR`.
- **Gotcha:** in AP mode the Pi's wlan0 has no internet — do `apt`/`ollama
pull` before AP-up (or over eth0 sharing).
- Captive portal (Option B: auto-popup on join via dnsmasq wildcard DNS)
  confirmed needed later — see 2B.3.

#### 2B.2 Phone-side voice

- **STT v0 (zero code):** the phone keyboard's built-in dictation mic types
  into the chat field. Works on iOS and Android, no permissions needed.
  This is the Phase-2 baseline — do not skip it.
- **STT v1 (enhancement):** in-page mic button via the Web Speech API.
  Requires a **secure context** in practice → self-signed HTTPS on the Pi
  (visitor accepts the warning once) or a pinned cert. Decision deferred;
  v0 may be enough for an installation.
- **TTS:** `speechSynthesis` speaks each completed answer; simple on/off
  toggle in the page. Works over plain HTTP, no permissions.

#### 2B.3 Optional extras — BUILT (2026-09-25)

- **Captive portal**: `portal_up.sh` / `portal_down.sh` — dnsmasq wildcard
  DNS via `/etc/NetworkManager/dnsmasq-shared.d/commonsclaw-portal.conf` +
  probe-answer routes in `web_server.py` (`/generate_204`,
  `/hotspot-detect.html`, `/ncsi.txt`, ...). Joining `CommonsClaw` should pop the
  chat open automatically. Needs an on-phone test.
- **HTTPS (for the in-page 🎤 mic)**: `make_cert.sh` generates a self-signed
  cert; `python3 web_server.py --https` serves on 8443. (Note: HTTPS uses the
  Flask server — waitress does no TLS. Fine for the low-traffic portal.)
- QR code (printed card or shown at boot) encoding `http://10.42.0.1:8080`.

**Acceptance criteria (2B):**

- [x] Phone joins `CommonsClaw` network, opens the page, full Q→A round trip with
      streaming (verified 2026-09-25 evening, country `HK`).
- [x] Keyboard dictation works as STT (verified). TTS default-on toggle built.
      In-page 🎤 needs HTTPS (`make_cert.sh` + `--https`) — optional.
- [ ] Works after an unattended reboot (AP + web server autostart).
      (`install_autostart.sh` ready; needs a reboot test.)
- [ ] Captive portal pops the chat on join (built; needs on-phone test).

---

## Phase 2C — Shared memory: reports, sensors, community notes (scaffolded 2026-09-25)

**Goal:** the kami is aware of its environment and its community, through
plain-text "reports" both machines and people can write.

### Architecture (as built)

- `reports/` + `sensors/` + `memory/` = the node's shared memory, all plain
  markdown readable by cron, the LLM, and humans.
  - `reports/` — `community_notes.md` (people's 📝 notes: suggestions, polls,
    comments), `pi_vitals.md` (node health log).
  - `sensors/` — one file per sensor (self-describing header + appended
    readings) + `SENSOR_REPORT.md` (dashboard: trends, anomalies, kami notes).
  - `memory/` — `identity.md` (who the kami is: personality, learned facts,
    skills — read at boot, edited rarely) + `journal.md` (dated continuity).
- `reports_reader.py` compiles a truncated digest (identity → sensors →
  reports) injected into the system prompt on EVERY question.
- Loggers are separate processes (cron/daemon) that collect automatically;
  the kami may suggest config tweaks via the `# logger_config:` header, and
  loggers can be queried directly (`--once`) — later, Level-1 loggers answer
  in words. Deliberately **not** MCP for now: zero extra services; MCP
  (e.g. server-filesystem) can replace the reader without format changes.

### Still to do in 2C

- [x] Memory category toggles (🧠/📡/📝) + slash keywords + auto-detect
      (2026-09-25 evening; fixes the 45 s prompt-eval penalty by keeping
      the prompt bare unless a category is active).
- [ ] Cron entry: `* * * * * /usr/bin/python3 /home/admin/commonsclaw/loggers/sensor_pivitals.py`
- [ ] First real sensor logger (e.g. BME280 on I2C, or meshtastic ingest)
      following the same report format.
- [ ] Let the LLM _suggest_ logger-config tweaks (it can already read the
      `logger_config` header; applying them stays human-gated).
- [ ] Polls/decisions: a note type the kami tallies when asked.

---

## Phase 3 — On-device voice (microphone + speaker on the Pi)

**Goal:** the Pi listens and speaks by itself; the phone becomes optional.
_This phase is for later — decisions below are starting points, to be
revisited with Phase 1 measurements in hand._

### 3.1 Hardware decision (pick one, record choice here)

| Option                         | Pros                                     | Cons                                   |
| ------------------------------ | ---------------------------------------- | -------------------------------------- |
| USB speakerphone (Jabra-style) | Zero drivers, built-in echo cancellation | Bulky, looks like office gear          |
| ReSpeaker 2-Mic HAT (WM8960)   | Cheap, speaker + mic, GPIO passthrough   | Driver overlay fiddly; no hardware AEC |
| ReSpeaker 4-Mic Array          | Far-field mics, LED ring                 | More setup; overkill for near-field    |
| USB mic + Pi HDMI/USB audio    | Simplest mic                             | Separate speaker path; no AEC          |

Note: the Pi 5 has **no 3.5 mm jack** — audio out is HDMI, USB, or HAT.

### 3.2 Software stack

- **STT:** Vosk (small English model, offline, proven on Pi, streaming
  partials) as default; `faster-whisper` tiny/base as quality alternative —
  benchmark both on the Pi 5.
- **TTS:** Piper (natural, fast on Pi 5) as default; eSpeak-ng as
  zero-dependency fallback.
- **Turn-taking:** start with **push-to-talk** (a physical button on GPIO —
  installation-proof, no echo problem). Wake word (openWakeWord) and
  barge-in are stretch goals.
- **Pipeline:** button → record → STT → `LLMManager` → sentence-chunked TTS
  while the answer is still streaming → speaker. Echo cancellation only
  becomes critical if the mic stays open during playback.

### 3.3 Latency reality check

phi3.5 on Pi 5 CPU ≈ 1–3 tok/s → a 50-word answer takes 30–60 s to
generate fully. For voice this dominates everything else. Options, to be
decided with Phase 1 numbers:

- Switch to a 1–2 B model (e.g. `llama3.2:1b`, `qwen2.5:1.5b`) for ~2–3×
  speed at lower answer quality.
- Keep phi3.5 and design the interaction around the pause (LED, sound,
  personality of a slow thinker).
- Start TTS on the first sentence so speaking begins early.

**Acceptance criteria:**

- [ ] Button press → spoken question → spoken answer, fully offline.
- [ ] Round-trip time measured and recorded; compared against Phase 1
      baseline.
- [ ] Runs unattended for a day without audio drift/crashes.

---

## Open decisions (numbered for easy reference in discussion)

1. Phase 2 web framework: Flask (default) vs FastAPI.
2. In-page mic (Web Speech API + self-signed HTTPS) vs phone-keyboard
   dictation only.
3. Captive portal: yes/no for the installation context.
4. Multi-visitor UX: strict queue vs "read-only while busy".
5. ~~LCD in Phase 2~~ — no LCD in this setup; dropped. (Old GUI stays as a
   debug fallback when a monitor is attached.)
6. Phase 3 audio hardware: USB speakerphone vs ReSpeaker HAT.
7. Phase 3 model: stay on phi3.5 vs smaller/faster model for voice.
8. Languages: English only, or multilingual STT/TTS/models?
9. Two-tier on-node model: tiny always-on (gemma3:270m/qwen2.5:0.5b) +
   deeper tier (llama3.2:1b) with a router — see
   [TOWARDS_HIERARCHICAL_CIVIC_AI.md](TOWARDS_HIERARCHICAL_CIVIC_AI.md).

## Change log

- **2026-09-17** — Plan created alongside [SETUP_RPI5.md](SETUP_RPI5.md).
  Baseline fork established at `alvarohub/rpi5-local-llm-node-with-wifi-api`.
- **2026-09-17 (2)** — No LCD available. Phase 1 redefined as screenless:
  added `console.py` and automatic console fallback in `main.py` (Tkinter
  GUI unchanged when a monitor is attached). Phase 2 split into 2A (web
  chat on the local network, testable with the temporarily attached
  monitor) and 2B (Wi-Fi access point + phones). LCD "how to join" panel
  idea dropped (decision 5).
