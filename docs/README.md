# CommonsClaw — documentation

This folder is the deep-dive library for the CommonsClaw project: a
solar-powered local AI node ("kami") that gives a place a voice, senses it,
remembers it, and will one day consolidate its memories into a shared
_narrative_ with neighboring kami. First site: Kashiwa Campus, University of
Tokyo. Reference hardware: Raspberry Pi 5 today, Jetson Orin next.

## How to read this

| Chapter                                                    | What it is                                                                                          |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [01-vision.md](01-vision.md)                               | **What CommonsClaw is** — the people's AI network: the levels, the narrative                        |
| [02-architecture.md](02-architecture.md)                   | The layered architecture: core / channels / sensors / memory — and the one-vs-many-process decision |
| [03-interaction-and-voice.md](03-interaction-and-voice.md) | The flawless front-end: canonical state machine, voice pipeline, robustness                         |
| [04-channels.md](04-channels.md)                           | Channel-agnostic adapters: web, voice, Telegram, WhatsApp, Matrix, CLI                              |
| [05-sensor-harness.md](05-sensor-harness.md)               | Sensor registry, loggers, the reports pipeline, MCP exposure                                        |
| [06-memory-and-narrative.md](06-memory-and-narrative.md)   | OpenClaw-style memory extended to a place: consolidation into narrative                             |
| [07-roadmap.md](07-roadmap.md)                             | Phases and milestones, with hardware gates                                                          |
| [ROBUSTNESS_PLAN.md](ROBUSTNESS_PLAN.md)                   | The original demo post-mortem (appendix; folded into 02/03/07)                                      |
| [research/](research/)                                     | Verified external research: voice-assistant architectures, channels + MCP, OpenClaw memory          |

## Where the living documents live

The project's operational documents remain at the repo root and stay
authoritative for day-to-day work:

- [../README.md](../README.md) — what this is, quick start
- [../PLAN.md](../PLAN.md) — the living plan (phases, decisions)
- [../ARCHITECTURE.md](../ARCHITECTURE.md) — how the current code is shaped
- [../DEVELOPMENT_LOG.md](../DEVELOPMENT_LOG.md) — dated work log
- [../COMMONSCLAW_VS_OPENCLAW.md](../COMMONSCLAW_VS_OPENCLAW.md) — the
  philosophical positioning
- [../TOWARDS_HIERARCHICAL_CIVIC_AI.md](../TOWARDS_HIERARCHICAL_CIVIC_AI.md)
  — the civic AI vision

This folder is the _scaffold_ for the long project: the architecture and the
research that will guide the coming builds. When a decision is made here, it
is recorded in PLAN.md.

## Status (2026-09-28)

Working prototype on the Pi 5, publicly demoed: web chat + voice (Silero
VAD → faster-whisper → llama3.2:1b) with live answer streaming, memory
categories, sensor digest, Wi-Fi AP. Robustness phase in progress (see
chapter 03 and 07); the Jetson Orin migration and the hierarchical work
follow.
