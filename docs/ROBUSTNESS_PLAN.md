# Robustness plan — voice/UI synchronization, and the road ahead

Written 2026-09-28 after the Kashiwa demo. Status: the three most critical
bugs found during the demo are **fixed** (see "Already fixed"); everything
else is the plan.

## 1. What the demo actually showed (evidence, not vibes)

The turn log from the demo window tells the story:

- **The pipeline works.** ~15 answered voice turns in an hour, including the
  CPU-temperature question answered correctly from the sensor digest
  (52.9 °C). The VAD gate, whisper, the shared settings and the live answer
  streaming all functioned.
- **One stuck generation.** Turns stop at 14:17:51 and resume at 14:22:28 —
  a ~5-minute gap. No traceback anywhere: a _hang_, not a crash. That is the
  "kami thinking forever" you saw.
- **Two models resident forever.** `ollama ps` shows both `llama3.2:1b`
  (1.8 GB) and `phi3.5` (3.9 GB) held in RAM (`OLLAMA_KEEP_ALIVE=-1`).
  The likeliest stall mechanism: during the demo the model selector was
  switched to phi3.5; Ollama took a long time to load 3.9 GB, and requests
  arriving during a load are silently **queued** — so the voice loop's
  request waited minutes with no answer and no error.
- **The open mic captured the room.** Several "questions" are the demo
  participants' own conversation ("contact with any weather stations…").
  When armed, the VAD correctly captures _whoever_ speaks — that is the
  intended behavior of an open mic, but it must be signalled clearly.
- **"starting…" aborts.** Pressing speak while the loop was busy (e.g.
  answering) queued the press, but the page gave up after 8 s and reverted
  the button — exactly the "starting for a few seconds then green again"
  you saw.

## 2. The weaknesses, ranked

1. **Unbounded blocking calls.** The voice loop's model call had no timeout —
   a queued/stalled request froze the loop in `thinking` indefinitely.
   _Any_ blocking call without a deadline is a future hang.
2. **Model switching is a trap on the Pi.** Loads take ~30–60 s for a 3–4 GB
   model; requests queue during loads; keep-alive=-1 then accumulates every
   model ever selected. On this hardware, the model should be _locked_, not
   freely switchable from the phone.
3. **Frontend/backend sync is a guess, not a truth.** State travels
   Pi-process → file → HTTP poll → DOM, at 0.4 s (loop) + ~0.9–5 s (page)
   granularity, with frontend-side timers ("starting", 8 s give-up) that can
   disagree with reality. This is the root of "I never know what's actually
   happening".
4. **No observability.** The only liveness signal is CPU% (misleading: a
   hung loop can sit at 0%) and a heartbeat that says what the loop _says_
   it is doing, not what it _is_ doing.
5. **The wake word is the wrong tool.** whisper-tiny mishears short words
   ("turtle" → "pernel", "turn it all"). A wake word needs a wake-word
   model (openWakeWord), not a transcriber.
6. **Single-threaded voice loop.** Recording and generation happen in one
   loop, so a press during an answer must wait behind it.

## 3. How existing systems do it (research summary)

This is a solved problem in at least five mature projects; we are not
inventing anything exotic.

- **Rhasspy** — the pipeline is explicit modules (wake word → ASR → NLU →
  TTS) with an **event-driven state machine**, events over MQTT (Hermes
  protocol), and a satellite architecture (the mic lives in a small process
  that talks to a central brain). The lesson: _explicit states, events, not
  polls_.
- **Mycroft / OpenVoiceOS** — a websocket **message bus** between the voice
  process, the brain and the GUI; every state change is a bus message any
  UI can subscribe to. Same lesson.
- **Home Assistant Assist pipeline** — a fixed pipeline with **per-stage
  debug tracing**, pushed to the frontend over WebSocket. The lesson: _the
  UI must render the pipeline's own stages, verbatim, not a parallel model
  of them_.
- **openWakeWord** — a tiny dedicated ONNX wake-word detector, designed to
  run continuously on weak hardware; this is the fix for "wake" (and for
  the wasted CPU of transcribing to detect a word).
- **Whisper-based assistants** (whisper.cpp servers, faster-whisper apps) —
  the standard pattern is **VAD-gated streaming STT** exactly like ours,
  with the states IDLE / LISTENING / PROCESSING / SPEAKING.
- **OpenAI Realtime / LiveKit agents** — full-duplex audio over WebSocket
  with server-side events; the web client is a thin renderer of the server
  state machine.

Robustness patterns shared by all of them: a supervisor that restarts on
failure (we have systemd), watchdogs/timeouts on every blocking call, one
owner for the microphone, and the UI _mirroring_ one canonical state
machine rather than maintaining its own.

## 4. What to change — urgent vs. structural

### Already fixed (this session)

- **Model-call watchdog** in `voice/talk.py`: the stream runs in a worker
  thread with a 90 s no-chunk timeout and a 4-minute total cap; on stall the
  loop gives up, logs the turn as failed, and the page shows "the model
  stalled — try again". Verified against both failure modes (instant error,
  silent hang).
- **Restart from the page**: `↻` button → `/api/voice/restart` →
  `sudo -n systemctl restart commonsclaw-voice` (scoped, passwordless).
- **"checking" state**: the wake-word look no longer reuses "transcribing".
- **Honest pending state**: speak shows "waiting…" while the kami is
  thinking and holds the press for 30 s.

### Urgent (before the next demo, days)

1. **Lock the model on the Pi.** Hide/disable the model selector (or keep it
   Mac-side only). Optionally keep-alive only for the default model
   (`OLLAMA_KEEP_ALIVE=0` for others) so switching unloads instead of
   accumulating RAM.
2. **Bound the last unbounded blocking call** — `capture_utterance`'s
   `arecord` read needs a read timeout (a dead arecord must not freeze the
   loop; `PR_SET_PDEATHSIG` covers parent death but not a stalled child).
3. **Systemd WatchdogSec** on `commonsclaw-voice`: the loop must poke
   `systemd-notify` every N seconds; if it ever stops, systemd restarts it.
   This turns "stuck process" into a 10-second self-heal.
4. **openWakeWord** for the wake word (built-in model first — "hey jarvis"
   etc. — to prove the loop; "wake" needs a custom-trained model later).
5. **Canonical state machine + verbatim UI.** Collapse the page to the
   loop's own states (idle / listening / checking / transcribing / thinking
   / speaking) with **no frontend timers or guesses** — the button renders
   the heartbeat state, full stop.

### Structural (the Jetson Orin moment, before the hierarchical work)

On the more powerful hardware the right shape is one supervised process
owning a clean event-driven state machine, with the browser as a thin
client:

- **One process**: audio thread (VAD + streaming whisper, `openWakeWord`),
  LLM client with timeouts, TTS, all states in memory.
- **WebSocket push** to the page (FastAPI/uvicorn, or keep Flask+SSE but
  push the voice state too) — polling dies.
- **A message bus between node processes** when they multiply (MQTT or
  plain files today; the format is already MCP-ready).
- Barge-in (speak over the answer), multi-turn, and TTS on the node.

This replaces "several processes guessing at each other through files" with
"one process, explicit states, one truthful renderer" — the pattern every
mature system above converged on.

## 5. The roadmap, keeping the big objective in sight

The goal is not a chat app. It is the **hierarchical, recursive
summarization society**: place-kami → neighborhood → city, each level
consolidating the level below into a narrative — a machine- and
human-readable "model of reality" whose objectives evolve with use
(see PLAN.md §5 and the machintropology notes). The robustness work above
is the _floor_ that makes the rest possible: a system that hangs 5 minutes
per demo cannot be trusted to remember anything.

- **A — harden (now → next demo).** Items in §4 urgent, in order.
- **B — truthful UI (Jetson).** The state-machine rework; the page becomes a
  mirror.
- **C — openWakeWord + streaming STT + TTS** (Jetson makes medium-whisper
  and real-time comfortable).
- **D — the reports pipeline (§4.4).** A smaller model digests raw logs into
  reports the conversational model reads — the first real "summarizer".
- **E — the neighborhood.** Two+ nodes, consolidation, narrative hand-off.
  Kashiwa campus is the first place-node; the stone-turtle kami is the first
  resident.

Decision to make together soon: whether the Jetson runs the **one-process
rewrite** (recommended — this is the moment to retire the polling/file
architecture) or whether we keep the multi-process shape and only add
WebSocket push.
