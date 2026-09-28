# Research: architecture of mature voice assistants & realtime AI voice

Verified 2026-09-28 against live GitHub repositories and documentation pages;
URLs are cited inline. Anything not verifiable is marked "unverified".
This file is the reference appendix for chapters 02 and 03.

## 1. Rhasspy — services over MQTT (Hermes)

Sources: <https://github.com/rhasspy/rhasspy> (archived Oct 6, 2025) ·
<https://rhasspy.readthedocs.io/en/latest/services/> ·
<https://github.com/rhasspy/rhasspy-hermes>

- **Audio flow.** Rhasspy is not one program: independent services (Audio
  Input, Wake Word, ASR, NLU, Dialogue Manager, TTS, Audio Output, Web
  Server) coordinate over MQTT using a superset of the Hermes protocol
  (originally Snips). A local mosquitto broker runs on port 12183. Audio
  Input streams raw WAV chunks on `hermes/audioServer/<siteId>/audioFrame`;
  wake detection publishes `hermes/hotword/<wakewordId>/detected`; ASR emits
  `hermes/asr/textCaptured`; NLU answers `hermes/nlu/query` with
  `hermes/intent/<intentName>`; the Dialogue Manager tracks sessions and
  intent handlers reply with `hermes/tts/say`. Docs warn that streaming mic
  audio over a shared broker can congest it — hence an optional UDP audio
  mode between mic and wake services.
- **State/UI.** State lives in the event stream, not a central store; any
  subscriber (Node-RED, Home Assistant, the web UI) can tap topics. A
  `siteId` on nearly every message makes multi-satellite setups explicit.
  The web UI mirrors everything over an HTTP + WebSocket API.
- **Robustness.** Supervision is delegated to process supervisors:
  `rhasspy-supervisor` converts the profile into a supervisord.conf or
  docker-compose.yml, so each service is independently restartable. The
  dialogue manager queues sessions (`sessionQueued`) — the prototype of
  "one conversation at a time".
- **Lesson.** Decouple every stage behind a message interface rather than
  function calls, and put a supervisor around each stage. "Replace one
  stage" is a deployment strategy, not a rewrite.

## 2. Mycroft / OpenVoiceOS — a WebSocket message bus

Sources: <https://github.com/MycroftAI/mycroft-core> (archived Sep 8, 2024) ·
<https://github.com/OpenVoiceOS/ovos-core> ·
<https://openvoiceos.github.io/ovos-technical-manual/>

- **Audio flow.** Processes connected to one bus: voice process (mic → wake
  word → STT), skills process (intents), audio process (TTS). OVOS names:
  `ovos-dinkum-listener` (mic + wake word + STT), `ovos-core` (skills),
  `ovos-audio` (TTS), `ovos-gui`, `ovos-PHAL` (hardware abstraction).
  Utterances travel as bus messages (`recognizer_loop:utterance`); skills
  reply with `speak`. Plugin interfaces exist for mic, VAD, wake word, STT,
  TTS, and "transformers".
- **State/UI.** The bus is the nervous system: a WebSocket server where each
  message is `{type, data, context}`; `context` carries a session and
  source/destination metadata. GUIs are just bus clients that render
  page/show events. Remote satellites go through HiveMind, a bus proxy.
- **Robustness.** Skills are isolated units; the bus is explicitly
  trust-local (never expose it publicly). Supervised processes (systemd) are
  the failure model.
- **Why Mycroft declined / OVOS continues.** Founders resigned (May 2022),
  layoffs (Nov 2022), Selene servers down (Feb 2024), repo archived. OVOS
  (formed Oct 2020 by ex/community devs) forked `ovos-core` (Oct 2021) and
  made the backend optional. Lesson: _optional cloud dependencies and
  community ownership are what let the stack live on._
- **Lesson.** A single WebSocket endpoint broadcasting typed events
  (`recognizer_loop:utterance`, `stt.streaming`, `llm.token`, `tts.speak`)
  with a session context is simultaneously the UI feed, the logging channel,
  and the plugin seam.

## 3. Home Assistant Assist — staged pipeline with per-stage tracing

Sources: <https://developers.home-assistant.io/docs/voice/pipelines/> ·
<https://www.home-assistant.io/voice_control/troubleshooting/>

- **Audio flow.** A formal **pipeline**: (1) wake word, (2) STT, (3) intent
  / conversation agent, (4) TTS. Clients run it over the Home Assistant
  WebSocket API (`assist_pipeline/run` with `start_stage`/`end_stage`,
  audio input params). Audio streams as binary frames prefixed with a
  handler-id byte. Any stage can be the start (text input starts at
  `intent`), so phone apps and dashboards reuse the same pipeline.
- **State/UI.** The strongest per-stage observability found: every run emits
  `run-start`, `wake_word-start/end`, `stt-start`, `stt-vad-start/end`,
  `stt-end` (with `stt_output.text`), `intent-start`, `intent-progress`
  (with `chat_log_delta` — token-level streaming to the UI), `intent-end`,
  `tts-start/end`, `error`, `run-end` over the same WebSocket. The debug UI
  replays per-run stages and lets you inject text mid-pipeline.
- **Robustness.** Per-stage enumerated error codes (`wake-word-timeout`,
  `stt-no-text-recognized`, …); whole-run `timeout` (default 300 s);
  `debug_recording_dir` saves per-command WAVs for tuning.
- **Lesson.** One run = one typed, traceable event sequence with timings,
  per-stage errors and token deltas. The UI, the debugger, and the fix for
  "why is it stuck?" all fall out of the same event log.

## 4. openWakeWord — streaming wake-word models, synthetic training

Source: <https://github.com/dscripka/openWakeWord>

- **Audio flow.** Three stacked components: a fixed mel-spectrogram frontend
  (ONNX), a frozen shared feature-extraction backbone (reimplementation of
  Google's `speech_embedding`, Apache-2.0), and a small per-word classifier.
  Audio is processed in **80 ms frames** (16 kHz); each frame yields a 0–1
  confidence, threshold default 0.5. One RPi 3 core runs 15–20 models.
  Built-ins: `alexa`, `hey mycroft`, `hey jarvis`, `hey rhasspy`, phrase
  models (`current weather`, `timers`).
- **Robustness.** Optional Speex noise suppression, a bundled Silero VAD
  gate (`vad_threshold` — a wake only counts if VAD agrees), and optional
  custom verifier models. Targets: <0.5 false-accepts/hour, <5%
  false-rejects. Custom models can be trained with 100% synthetic TTS data
  plus negatives (Colab notebook, <1 h). Licensing: code Apache-2.0,
  pretrained models CC BY-NC-SA 4.0.
- **Lesson.** Wake detection is a _separate, tiny, streaming model_, never
  the transcription model. This is the fix for "whisper can't hear 'wake'".

## 5. The Wyoming Protocol — pluggable voice services over TCP

Source: <https://github.com/rhasspy/wyoming> (now `OHF-Voice/wyoming`,
Open Home Foundation)

- **Audio flow.** "JSONL + PCM audio": a peer-to-peer TCP protocol with a
  one-line JSON header plus optional binary payload. Standardizes stages:
  audio (`audio-chunk/start/stop`), wake word (`detect` → `detection`),
  ASR (`transcribe` → `transcript`, with streaming
  `transcript-start/chunk/stop`), VAD (`voice-started/stopped`), TTS
  (`synthesize`). Service discovery: `describe` → `info`.
- **Satellites.** First-class satellite semantics (`satellite-connected`,
  `streaming-started`), and server-side pipeline control (`run-pipeline`
  with `start_stage`, `wake_word_names`, `restart_on_end`).
- **Robustness.** No auth/encryption — trusted network only (SECURITY.md).
  Its robustness contribution is _compatibility_: HA, ESPHome, Rhasspy tools
  all speak it; servers must ignore unrecognized events (forward compat).
- **Lesson.** If we expose wake/ASR/TTS as Wyoming-speaking services we
  inherit the whole ecosystem instead of writing another glue layer. Even
  without adopting it, its `start/chunk/stop` event taxonomy is the right
  shape for our own bus.

## 6. Silero VAD + faster-whisper — the standard local pairing

Sources: <https://github.com/snakers4/silero-vad> ·
<https://github.com/SYSTRAN/faster-whisper>

- **Silero VAD.** ~2 MB JIT model, <1 ms per 30+ ms chunk on one CPU thread,
  8/16 kHz, ONNX export, MIT license. Recurrent-state streaming (512-sample
  frames with a carried context — the detail that bit us on the Pi). It is
  the default gate inside openWakeWord, faster-whisper's `vad_filter`,
  LiveKit, and HA/ESPHome devices.
- **faster-whisper.** Whisper on CTranslate2: up to 4× faster than
  openai/whisper with less memory, int8 quantization, no system FFmpeg.
  `segments` is a lazy generator; built-in Silero VAD filtering
  (`vad_filter=True`). Community streaming wrappers: **WhisperLive**
  (Collabora), **whisper-streaming** (UFAL). Whisper itself is offline;
  streaming is bolted on via rolling windows/VAD segmentation.
- **Lesson.** Keep the VAD gate mandatory (we learned this the hard way —
  whisper invents sentences from quiet rooms), and treat STT output as
  _timestamped segments_ so the UI can show partial transcripts. Do not
  expect free token-level streaming from Whisper; budget segment latency.

## 7. OpenAI Realtime API + LiveKit Agents — full-duplex event sessions

Sources: <https://github.com/openai/openai-realtime-console> ·
<https://github.com/livekit/agents> · <https://docs.livekit.io/agents/>
(platform.openai.com blocked automated fetching; specifics marked below)

- **Audio/event flow.** The Realtime API is one bidirectional session
  (WebSocket or WebRTC) where audio _and_ state changes are events: the
  client appends mic audio and the server emits audio deltas and transcript
  deltas. Verified event names from OpenAI's repos: `session.update`,
  `response.text.delta`, `response.done`, `guardrail_tripped`. Server-side
  VAD decides end-of-turn. No intermediate text required — the model
  consumes audio directly; OpenAI's agents demo cites ~1.5 s+ penalty for
  stitched STT→LLM→TTS chains versus direct audio.
- **LiveKit Agents.** Server-side framework: frontend ↔ LiveKit server over
  WebRTC; an agent worker runs an `AgentSession` (VAD, STT, LLM, TTS or a
  realtime model); the framework handles turn detection (a dedicated model),
  interruptions, function calls, multi-agent handoffs, and job dispatch (one
  subprocess per room, graceful shutdown).
- **Robustness.** Full-duplex interruption cancels in-flight audio; WebRTC
  gives loss/bandwidth resilience on mobile networks.
- **Lesson.** Model _everything_ (audio + transcript + state) as one typed
  event stream a UI can subscribe to; and full-duplex turn handling
  (interruption cancels generation) is worth emulating even with a serial
  Ollama slot — our "busy" event should be able to cancel/queue, not just
  refuse.
- _Unverified this session:_ exact Realtime event names for audio-buffer
  management (`input_audio_buffer.*`, `conversation.item.created`).

## Synthesis: what mature systems converge on

1. **Stage separation with typed events** — wake/VAD/STT/NLU/TTS stages talk
   only through typed messages (Hermes topics, OVOS bus, HA pipeline events).
2. **One event stream is the UI feed** — UIs never poll stage internals;
   they subscribe to the same stream the stages emit.
3. **A named pipeline run with per-stage timing and errors is the debugging
   primitive** — HA Assist's `run-start/…/error` is the reference design.
4. **Wake word is a dedicated tiny streaming model, never the ASR.**
5. **VAD gates everything** — it triggers the pipeline and bounds
   transcription work.
6. **Supervision belongs outside the app** — restartable stage processes are
   the standard failure recovery.
7. **Sessions and context travel with the message** — `siteId`, `session`,
   `conversation_id` routing metadata.
8. **Satellite/remote = audio-at-the-edge, brains-on-the-server** — exactly
   our phone-page + Pi-node topology.
9. **Streaming is shaped as start/chunk/stop triplets** on every modality.
10. **Compatibility is a protocol, not a plugin** — Wyoming keeps Rhasspy's
    components alive inside Home Assistant after Rhasspy itself was archived.
