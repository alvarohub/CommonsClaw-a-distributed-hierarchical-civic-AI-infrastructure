# 07 — Roadmap

Phases are ordered by dependence: interaction is flawless before channels
multiply, channels before the narrative ladder, the ladder before the
neighborhood. Hardware gates are marked.

## Phase A — Harden the Pi node (now → next demo)

Goal: no hangs, no guessed states, self-healing.

- [x] Model-call watchdog (90 s no-chunk, 4 min cap) — _done 2026-09-28_
- [x] Restart button + `/api/voice/restart` — _done_
- [x] Honest states: `checking`, `empty`, `error` — _done_
- [ ] Lock the model on the Pi (hide selector; keep-alive only for default)
- [ ] arecord read timeout (last unbounded blocking call)
- [ ] systemd WatchdogSec on the voice service (self-heal in ~10 s)
- [ ] openWakeWord with a built-in model to prove the loop
- [ ] Unattended-boot acceptance test

## Phase B — The truthful front-end (Pi, then Jetson)

Goal: the page mirrors the canonical state machine; no polling, no guessing.

- [ ] SSE/WebSocket push of the interaction event stream to the page
- [ ] A debug view that replays any turn's event timeline
- [ ] The Jetson core: one supervised process owning the state machine

## Phase C — Voice becomes real (Jetson Orin)

- [ ] openWakeWord custom model ("wake"), VAD-cross-checked
- [ ] Streaming STT (segment-based partial transcripts)
- [ ] Node-side TTS (Piper) — the kami speaks from the place, not the phone
- [ ] Barge-in: interruption cancels the in-flight generation

## Phase D — Channels and MCP

- [ ] Telegram adapter (long polling) — proves the channel seam
- [ ] MCP server: `get_sensor`, `read_memory`, `ask` (stdio, annotated tools)
- [ ] Matrix adapter (university community)

## Phase E — The narrative ladder

- [ ] Reports pipeline: a small model digests raw logs into reports (§4.4)
- [ ] Nightly consolidation with score gates, operations-not-prose,
      `Source:` anchors, loss-bounded promotion (OpenClaw mechanics,
      per-place)
- [ ] Two place-nodes consolidate through a Level-2 neighborhood kami
- [ ] The first narrative that survives a month, read back by a human

## Milestones that matter

1. **Next demo**: the kami never hangs, never lies about its state, and a
   stranger always knows if it is listening.
2. **Kashiwa install**: unattended boot, weeks of uptime, the reports
   pipeline producing real per-sensor trends.
3. **First neighborhood**: two kami, one consolidated narrative, the
   hierarchy proven end to end.

## Open decisions (for discussion, in order)

1. Jetson core: adopt **Wyoming** for wake/ASR/TTS services, or a private
   event vocabulary? (Wyoming inherits the ecosystem; private is simpler.)
2. Bus: MQTT on the node, or keep files for sensors and add a bus only for
   the interaction events?
3. Wake word: "wake" (custom-trained) or a built-in openWakeWord word for
   the first deployment?
4. Level-2 first host: a second Pi-class node in the lab, or the Jetson
   doubling as neighborhood consolidator?
