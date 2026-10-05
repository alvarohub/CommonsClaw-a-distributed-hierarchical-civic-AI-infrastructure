# 03 — Interaction & voice: the flawless front-end

Interaction is the kami's face. "Flawless" means concrete, testable
properties:

- **Perceived feedback < 150 ms** on every press (button state changes
  immediately, truth follows).
- **Zero guessed states**: the UI renders exactly what the core emits.
- **Recovery ≤ 10 s**: a hung stage is detected, reported, and healed.
- **Honest errors**: "I didn't hear that", "the model stalled" — never
  silence, never a phantom state.

## The canonical state machine

One machine, owned by the interaction core, emitted as typed events. Every
state has a single mandated UI rendering.

| State             | Meaning                                            | UI must show                                             |
| ----------------- | -------------------------------------------------- | -------------------------------------------------------- |
| `IDLE`            | waiting, wake off                                  | "press speak", button enabled                            |
| `WAKING`          | wake word armed, listening                         | subtle "waiting for the word"                            |
| `LISTENING`       | recording the question                             | red pulsing button + banner                              |
| `CHECKING`        | was that the wake word? (transcribing a candidate) | "checking…" (never "transcribing" — that confused users) |
| `TRANSCRIBING`    | converting the question                            | "transcribing…"                                          |
| `THINKING`        | model generating                                   | streaming token display                                  |
| `SPEAKING`        | TTS playing                                        | speaker indicator                                        |
| `EMPTY` / `ERROR` | nothing heard / model stalled                      | "I didn't hear that — try again" / "the model stalled"   |

Every transition is an event with timings (`run-start`, `stt-end` with text,
`llm.token`, `error` with a code) — Home Assistant Assist's pipeline-event
model, which is the reference for "where did it get stuck" debugging
([research/voice-assistants.md](research/voice-assistants.md) §3). The
phone page is a consumer of these events, nothing more.

## The voice pipeline (current, Pi 5)

```
ReSpeaker mic (card 3, fixed gain)
  → Silero VAD (onnxruntime; the gate — whisper never sees silence)
  → capture one utterance (auto-stop ~1 s silence, 20 s cap)
  → faster-whisper tiny (int8; padded 0.5 s both ends — whisper clips
    first words and hallucinates on silence, both learned the hard way)
  → shared settings + LLM (llama3.2:1b, watchdog: 90 s no-chunk, 4 min cap)
  → answer streamed to the heartbeat file → phone renders live
  → browser speechSynthesis TTS (until the node has its own)
```

## What the demo taught (post-mortem, 2026-09-28)

1. **The 5-minute "thinking"** = a model request queued behind a phi3.5
   load, with _no timeout_ in the voice loop. Fixed: worker-thread stream
   with deadlines; the turn is marked failed and the page says so.
2. **"starting…" then abort** = the page's own 8 s timer giving up while the
   loop was busy. Fixed: honest "waiting…" while thinking, 30 s hold.
3. **Wake word unreliable** = whisper-tiny mishears short words ("wake" →
   who knows). A transcription model is the wrong tool; see urgent #4.
4. **Model switching is a trap** on the Pi: loads queue requests and
   keep-alive accumulates every model ever selected (5.7 GB held after the
   demo).
5. **No observability** — CPU% misleads (a hung loop sits at 0%).

## Urgent fixes (before the next demo)

1. **Lock the model** on the Pi (hide the selector; keep-alive only for the
   default model — unload the rest).
2. **Bound the last unbounded call**: `arecord` stdout reads need a
   deadline, so a dead recorder can't freeze the loop.
3. **systemd WatchdogSec** on the voice service: the loop pokes
   `systemd-notify` every N seconds; a stuck loop is restarted in ~10 s.
   This is the self-healing answer to "is it alive or stuck?".
4. **openWakeWord** for the wake word — built-in model first (e.g.
   "hey jarvis") to prove the loop; a custom "wake" model later (100%
   synthetic training is feasible; see research §4).
5. **Push, not poll**: the heartbeat already carries live state and
   token deltas; move the page to an SSE/WebSocket subscription of the
   _same_ events (small step on the Pi, full version on the Jetson).

## The Jetson rewrite (target shape)

On the Orin: one supervised core process (audio thread with openWakeWord +
VAD + streaming whisper; LLM client with deadlines; TTS) emitting the state
machine over WebSocket; the page becomes a pure mirror; barge-in (speak
over the answer) and node-side TTS land here. Options to adopt wholesale:
**Wyoming**-speaking services (inherits the ecosystem) and an
**MQTT** local bus (Rhasspy's pattern) — see research §1, §5.

## Definition of done for "flawless"

- [ ] Every press acknowledged in <150 ms; every state change visible in
      <1 s.
- [ ] A hung stage is reported within its deadline and the node self-heals.
- [ ] The debug view replays any turn's event timeline (HA-style).
- [ ] A stranger at the demo never wonders "is it listening?".
