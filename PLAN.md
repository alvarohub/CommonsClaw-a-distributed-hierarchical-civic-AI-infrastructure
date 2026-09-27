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

- `identity/` + `sensors/` + `community/ = the node's shared memory, all plain
  markdown readable by cron, the LLM, and humans.
  - `community/` — `notes.md` (people's 📝 notes: suggestions, polls,
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

### 3.1 Hardware — DECIDED (2026-09-27)

- **Mic: ReSpeaker USB Mic Array v2.1** (already owned). USB audio class →
  appears as a sound card, no drivers. The onboard XMOS does beamforming,
  noise suppression, AEC, and DOA _in hardware_ — the Pi receives clean,
  voice-focused audio, which matters more for Whisper accuracy than compute.
  Bonus: DOA tells the kami _where_ the speaker stands (embodiment flourish).
- **Speaker:** any small USB/HDMI speaker (Pi 5 has no 3.5 mm jack). TBD
  what's on hand.
- **Trigger:** start with push-to-talk over SSH, then a GPIO button on the
  turtle. Wake word (openWakeWord) and barge-in are stretch goals.

### 3.2 Software stack — DECIDED

- **STT:** `faster-whisper` (CTranslate2, int8) with `tiny` or `base` model —
  fastest CPU path on Pi 5 (~2-4× realtime for tiny), Python-native (drops
  into our pipeline), multilingual (Japanese+English). Alternative:
  `whisper.cpp` with ARM NEON build. Benchmark both.
- **TTS:** `piper` (Home Assistant voice stack) — faster than realtime on
  Pi 5, small voices, has Japanese. Fallback: `espeak-ng` (robotic, instant).
- **Sequencing** (his correct instinct): STT → LLM → TTS never compete —
  total added CPU per turn is seconds. Memory check: whisper tiny (~150 MB)
  - piper voice (~50 MB) + llama3.2 (~800 MB) ≈ fine in 16 GB.

### 3.3 Pipeline

```
button → record (ReSpeaker, clean beamformed audio)
       → faster-whisper tiny (~1-2 s for a short question)
       → text into LLMManager.stream_response()  (same path as everything)
       → TTS starts on first sentence, speaks while the rest streams
```

Voice answers also flow to the phone page as usual (web UI keeps working;
phone TTS and Pi TTS are independent outputs).

### 3.4 Latency budget (measured baseline in hand)

llama3.2:1b ≈ 8 tok/s. Voice turn = record (2-4 s) + STT (1-2 s) + TTFT
(~1-5 s warm) + answer (~10-15 s at 50 words, TTS overlapping). Realistic
total to first spoken word: ~5-8 s. The kami as a _slow, calm presence_ is a
design feature here, not a bug — but the two-tier model idea (decision 9)
becomes more attractive for voice chit-chat.

### 3.5 Build order (each step independently testable)

1. ✅ ReSpeaker visible as ALSA device; `arecord` captures clean audio
   (2026-09-27: card 3, gain 90, peak >4000).
2. ✅ `faster-whisper` tiny transcribes a recorded clip (0.8 s for a 4 s
   clip — ~5× realtime, correct on first try).
3. ✅ Push-to-talk over SSH: Enter to record, Enter → transcript + kami
   answer (`voice/talk.py`), turn published to status store and shown in the
   web UI (`/api/status` carries the latest turn; page dedupes by turn id).
4. ✅ Full loop: voice question → kami text answer (printed + on web).
   Wake-word mode: `voice/talk.py --wake kami`.
5. ⬜ Piper on the Pi speaks the answer (sentence-chunked, while streaming).
6. ⬜ GPIO button on the turtle; LED/sound feedback for listening/thinking.
7. ⬜ Stretch: openWakeWord, DOA "the kami turns toward you", barge-in.

**Acceptance criteria:**

- [ ] Button press → spoken question → spoken answer, fully offline.
- [ ] Round-trip time measured and recorded (target: <10 s to first spoken
      word for a short question).
- [ ] Runs unattended for a day without audio drift/crashes.
- [ ] Benchmark table gains rows: STT (seconds per 3 s clip), TTS (RTF).

---

## Phase 4 — The node as an agent (design sketch, 2026-09-25)

The system is converging on "an agent with skills and memory" — deliberately
**pro-social / pro-environmental / pro-community**: it serves no individual
and not even "all humans" — it represents _the community and the ecosystem_,
and talks to other agents with other knowledge in other places.

### 4.1 Self-observation (the node knows its own metabolism)

The node's identity (`identity/identity.md`) should carry _measured_ facts
about itself, updated by loggers:

- Energy: solar input, battery, consumption, duty cycle (dark hours policy).
- Traffic: requests/day, category mix, peak hours (from the status store).
- Request typology: what people actually ask (recurring topics → cache
  candidates or fine-tuning data).
- Uptime / health / thermal history.

**Mechanics (built 2026-09-27):** `sensors.json` = the machine-readable
registry (per sensor: id, logger script, log file, interval, active flag,
params); `sensors_boot.py` spawns one supervisor per active entry at boot
(`commonsclaw-sensors.service`). Each completed turn is also appended to
`identity/turn_log.jsonl` (machine-readable), and `journal_writer.py` (cron
23:55) folds the day into `identity/journal.md`: world half = per-sensor
min/max/mean; talk half = question count + top topic words.

**Deferred by design (the LLM consolidation layer):** per-sensor _analytic_
reports by Level-0 agents (trend extraction) and a global "state of the
place" synthesis across sensors — real pattern discovery over days — require
a bigger model than this Pi can host. That consolidation is a Level-2+ job
reading the journal, and the journal format is designed for that handoff.
(OpenClaw does the same shape: files + periodic consolidation by a larger
model.)

### 4.2 Adaptive behavior from self-observation

- **Caching**: frequent question types get cached/canned answers (huge
  energy saving; measured first via 4.1).
- **Tunnels to other nodes**: when a request type exceeds local competence,
  a link to a more specialized node or a bigger datacenter is established
  — negotiated, logged, revocable. This is the level-2+ interface.
- **Power-aware degradation**: low battery → switch to the tiny model,
  shorter answers, sleep between interactions.

### 4.3 What this changes in the architecture

- The status store becomes a first-class _self-report_ (not just a debug
  dashboard feed): a logger writes it into `sensors/node_metabolism.md`.
- Request logging gains a category field (we already have categories from
  the memory routing — reuse them for traffic statistics).
- `identity.md` gains a "metabolism" section written by loggers, not by hand.

---

## Phase 5 — Consolidation, and the neighborhood tier (design, not built)

### 5.0 The levels, precisely

| Level | Who                  | What it does                                                        | Hardware                     |
| ----- | -------------------- | ------------------------------------------------------------------- | ---------------------------- |
| **0** | the loggers          | sense and record; at most tiny ML pattern recognition (classic AIoT) | MCU / the Pi's own processes |
| **1** | the **place** kami   | converses, holds the place's memory _(this repo)_                    | Pi 5 — see the caveat below  |
| **2** | the **neighborhood** | gathers and consolidates across _several_ kami in several places     | a real machine               |
| 3+    | city → nation → world| answers what no neighborhood can                                      | shared datacenters           |

Level 2 is **not** "the city": it is the first tier that sees more than one
place. A neighborhood kami talks to the park turtle, the greenhouse, the
riverbank — and only what survives that consolidation travels further up.

### 5.1 What consolidation actually is

Accumulation is what we built: logs grow, notes pile up, one journal block
per day. Consolidation is the opposite motion — reading a lot and writing a
little:

1. **Per-sensor trends** (Level 0 → 1): a month of `temp=27.4C` lines
   becomes "runs 2–3 °C warmer after rain; coldest hour is 05:00".
2. **Cross-sensor state of the place** (Level 1): the sensor trends plus
   the community notes become "the pond is recovering; people ask about
   the fish again".
3. **Identity promotion** (Level 1): recurring, corroborated facts graduate
   from the journal into `identity/identity.md` — the kami's stable
   self-knowledge. This is the dangerous one: a bad promotion poisons every
   later answer.
4. **Across places** (Level 2): several kami's consolidations become the
   neighborhood's picture, and it writes back what each place should know.

### 5.2 The honest hardware finding

Consolidation is conceptually the kami's own metabolism — a Level-1 job. But
it is exactly the workload a 1 B model on a CPU is worst at (read much,
write little, be right). **So either a place-node that reflects needs more
than a Pi 5, or Level 1 borrows a bigger mind from Level 2.** The current
plan borrows. Recording this as a finding: _the Pi 5 is sufficient for a
conversing node, insufficient for a reflecting one._

### 5.3 What to borrow from OpenClaw

Their nightly "dreaming" sweep is the most mature file-based implementation
(verified 2026-09-28 — details and URLs in
[OPENCLAW_MEMORY_RESEARCH.md](OPENCLAW_MEMORY_RESEARCH.md)):

- markdown is the source of truth; SQLite only ever a **derived index**
- a nightly cron sweep (`0 3 * * *`), phased light → REM → deep; only the
  deep phase may rewrite the curated core
- a **deterministic score gate before any model call** (relevance,
  frequency, query diversity, recency, consolidation, richness) — the model
  is asked only about candidates that already passed
- the model returns **merge/supersede operations, not prose**, validated
  against a ≤25% prior-entry-loss rule, mandatory `Source:` anchors and a
  budget; on failure it falls back to plain append; writes are atomic renames
- retrieval with **zero query-time model calls** (ranked search + injection)

All of that transfers. What does not: OpenClaw scopes memory **per agent /
per user** — "a gateway is one trust domain", and group sessions are
explicitly excluded from durable memory. Nothing there knows what a _place_
is, or how many authors share one identity. That is the part CommonsClaw has
to invent: whose voice counts, and how a commons resists capture by its
loudest visitor.

### 5.4 Acceptance criteria (when we get there)

- [ ] A month of sensor data produces a per-sensor trend paragraph a human
      agrees with.
- [ ] Identity promotion is loss-bounded, source-anchored, and reversible
      (git history of `identity/`).
- [ ] A second node exists and the two consolidate through a Level-2 tier.
- [ ] Nothing crosses a community boundary without a logged, revocable
      decision.

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
10. Agent-framework question: are we reinventing OpenClaw et al.? (Answered
    for now in [COMMONSCLAW_VS_OPENCLAW.md](COMMONSCLAW_VS_OPENCLAW.md) —
    mechanics overlap, politics/topology opposite. Revisit when we need
    channels, sandboxing, or a plugin ecosystem.)
11. Node-to-node protocol: what crosses a boundary (context? summary?
    embeddings?), who consents, what is logged, is there retribution.
12. Community analytics (machintropology): which agent reads the communal
    memory to surface the community's recurring needs — and where does it
    run (too heavy for the Pi; a Level-2 role?).

## Change log

- **2026-09-25** — Phase 2A+2B complete on emotionpi (AP, phone chat, portal,
  autostart, benchmarks, memory categories with toggles + keyword routing).
  Project renamed CommonsClaw; vision + OpenClaw comparison + references
  documented. Phase 4 (agent self-observation, caching, node links) sketched.
- **2026-09-17** — Plan created alongside [SETUP_RPI5.md](SETUP_RPI5.md).
  Baseline fork established at `alvarohub/rpi5-local-llm-node-with-wifi-api`.
- **2026-09-17 (2)** — No LCD available. Phase 1 redefined as screenless:
  added `console.py` and automatic console fallback in `main.py` (Tkinter
  GUI unchanged when a monitor is attached). Phase 2 split into 2A (web
  chat on the local network, testable with the temporarily attached
  monitor) and 2B (Wi-Fi access point + phones). LCD "how to join" panel
  idea dropped (decision 5).
