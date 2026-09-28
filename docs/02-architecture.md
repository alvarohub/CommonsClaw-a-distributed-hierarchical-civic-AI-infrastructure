# 02 — Architecture: layers, ownership, and the one-vs-many decision

## The lesson we are building on

Every mature voice/assistant system examined in
[research/voice-assistants.md](research/voice-assistants.md) converges on
the same few patterns:

1. **Each hardware resource has exactly one owning process** (mic, model,
   sensors) — isolated failure, independently restartable.
2. **One canonical, event-driven state machine** — UIs never guess; they
   _mirror_ the state the core emits, over push (WebSocket), never polling.
3. **Channels are thin adapters** in front of the same core (Rasa's
   InputChannel/OutputChannel, OpenClaw's Gateway + channels).
4. **Supervision lives outside the app** (systemd, supervisord) — restart is
   the standard recovery path.

The current implementation violates #2 hardest: state travels
Pi-process → file → HTTP poll → DOM with frontend-side timers that can
disagree with reality. That, not any single bug, is why the demo felt
"disconnected".

## The decision: one process, or many?

**Many processes, but not the current shape.** A one-process monolith would
fight the vision directly: level 2 is _another process on another machine_,
channels come and go, and sensors fail independently. What must change is
the _message layer_, not the process count:

- **Keep** process isolation (mic owner, web server, sensors, later channel
  adapters, later the neighborhood consolidator).
- **Introduce** one canonical interaction state machine, owned by the
  voice/interaction core, emitted as typed events.
- **Replace** file-polling between core and UI with push (WebSocket), and
  between processes with a local message bus (MQTT, or plain files only
  where they are genuinely the right primitive — sensors).
- **Keep** exactly one generation slot and one mic owner, enforced by the
  core, not by convention.

This is the hybrid every pro system uses: Rhasspy (stages over MQTT),
OpenVoiceOS (processes on a bus), Home Assistant (pipeline events over
WebSocket).

## The layered shape (target)

```
┌───────────────────────────────────────────────────────────────┐
│  Level 1+ clients                                              │
│   browser (WebSocket mirror)  ·  MCP clients (external agents) │
└───────────────▲──────────────────────────────▲────────────────┘
                │ typed events (push)           │ MCP (tools/resources)
┌───────────────┴──────────────────────────────┴────────────────┐
│  THE INTERACTION CORE  (one supervised process per node)      │
│   state machine (IDLE/LISTENING/PROCESSING/SPEAKING/ERROR)    │
│   audio: openWakeWord → Silero VAD → streaming STT            │
│   llm client with deadlines  ·  TTS  ·  single generation slot│
└───────▲───────────────────▲───────────────────▲───────────────┘
        │ bus messages      │ bus messages      │ bus messages
┌───────┴──────┐   ┌────────┴───────┐   ┌───────┴───────────────┐
│ channel      │   │ channel        │   │ sensor harness        │
│ adapters     │   │ adapters       │   │ (registry, loggers)   │
│ web · voice  │   │ telegram ·     │   │ crash-isolated,       │
│ · CLI        │   │ whatsapp · …   │   │ file-writers          │
└──────────────┘   └────────────────┘   └───────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│ memory & reports (files + journal + summarizer)               │
│ identity/ sensors/ community/ → digest → narrative ladder     │
└────────────────────────────────────────────────────────────────┘
```

- **The core** owns the state machine and the model slot. It emits typed
  events (`run-start`, `listening`, `stt.partial`, `llm.token`, `speaking`,
  `error` …) on the bus — the vocabulary of Home Assistant's pipeline and
  Wyoming's start/chunk/stop triplets (see research).
- **Channel adapters** translate `(user, text/audio, channel)` into core
  turns and render core events back (chapter 04).
- **The sensor harness** stays asynchronous and crash-isolated; it writes
  files, which the summarizer turns into reports (chapter 05).
- **The browser** becomes a mirror: one WebSocket subscription, zero
  guessing.

## Hardware tiers

| Tier | Hardware | Runs |
| ---- | -------- | ---- |
| now | Pi 5 (16 GB) | core (VAD+whisper-tiny+llama3.2:1b), web, sensors |
| next | Jetson Orin | core upgraded: medium-whisper, streaming STT, openWakeWord, node TTS |
| L2 | a real machine | neighborhood consolidator, narrative synthesis |
| L3+ | shared infra | what no neighborhood can answer |

The software shape is the same at every tier; only the models and the
number of hosted layers change. That is the payoff of multi-process +
bus over a monolith: the neighborhood tier is a deployment, not a rewrite.

## Migration path (from today's file-polling to the target)

1. **Now (Pi):** keep processes; add the missing robustness (chapter 03's
   urgent list) — watchdogs, model lock, canonical states already pushed.
2. **Jetson:** build the core as a supervised process with the event-driven
   state machine and WebSocket push; retire the heartbeat-file polling.
3. **Then:** add channel adapters and MCP as _separate_ consumers of the
   same events — proving the seam before the neighborhood tier exists.

## Invariants (things we do not break)

- Files remain the durable memory (identity/, sensors/, community/,
  turn_log) — append-only for anything with multiple writers.
- Every blocking call has a deadline.
- The mic has one owner; the model has one generation slot.
- The UI never guesses; if it cannot know, it says so.
