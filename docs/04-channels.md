# 04 — Channels: the kami is agnostic

The kami is one mind; web, voice, Telegram, WhatsApp are just doors. The
door never changes who's inside.

## The adapter contract

Following the Rasa pattern ([research/channels-and-mcp.md](research/channels-and-mcp.md) §A5)
and OpenClaw's Gateway/channels split (§A6):

- **Inbound**: every channel produces `turn(user_id, text, channel_name)`.
  The core has no idea the text came from a phone keyboard or a Telegram
  message.
- **Outbound**: the core emits generic events (`llm.token`, `speaking`,
  `error`); each adapter renders them in its medium (DOM, TTS audio, bot
  message) and streams through a `chunk-start/chunk/end` seam.
- **Identity**: `channel_name` is a plain string used for routing, logging
  and per-channel response tuning. Nothing else leaks into the core.
- **Turn handling**: one generation slot in the core; adapters get
  `queued`/`cancel` semantics instead of parallel model calls.

## The channels, in priority order

| Channel               | Transport on the Pi                                                                              | Notes                                           |
| --------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| **Web** (now)         | HTTP + heartbeat JSON → move to WebSocket mirror                                                 | the demo surface; must be flawless (chapter 03) |
| **Voice** (now)       | own process, shared settings file → folds into the core                                          | VAD+whisper pipeline                            |
| **CLI/console** (now) | stdin/stdout                                                                                     | debug and operations                            |
| **Telegram**          | long polling (`getUpdates`) — outbound HTTPS only, ideal for NAT                                 | self-host friendly; the natural next channel    |
| **Matrix**            | `sync_forever` long polling                                                                      | same outbound property; E2EE via matrix-nio     |
| **WhatsApp**          | Cloud API (webhooks + Meta account + templates + 24 h window) or Baileys (unofficial, ToS-risky) | a compromise, always behind one adapter         |

Rules learned from the research:

- Prefer **outbound-pull** transports on the Pi — no public IP, no tunnels
  (Telegram/Matrix long polling).
- Keep legally risky adapters (Baileys) isolated and clearly labelled.
- Every adapter is one small process subscribing to the bus; adding a
  channel must never touch the core.

## Message-bot details worth recording

- **Telegram**: `getUpdates` with `offset` (recompute after each response to
  avoid duplicates), `timeout` long-poll; inline keyboards →
  `callback_query` → must call `answerCallbackQuery` (else the client shows
  a progress spinner). One mechanism at a time (polling XOR webhook).
- **Matrix**: `AsyncClient.sync_forever()` + `add_event_callback(...,
RoomMessageText)`; send with `room_send()`.
- **WhatsApp Cloud**: inbound only via webhook (needs public HTTPS);
  message templates outside the 24 h window; 80 msg/s default throughput.
- **OpenClaw reference**: Gateway = "control plane for sessions, tools,
  events, and channel connections"; channels are plugins; DM channels
  require pairing approval; inbound messages treated as untrusted. Our
  neighbor tier will eventually look like an OpenClaw gateway — but scoped
  to places, not persons.

## When to build each

Now: web + voice (existing). With the Jetson core: CLI debug channel +
Telegram (cheap, high value for the lab). Later: Matrix for the university
community; WhatsApp only if a real demand appears.
