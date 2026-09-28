# Research: channel-agnostic assistants & MCP exposure of hardware

Verified 2026-09-28 against the pages cited. Anything not found on the
fetched page is marked "unverified". Reference appendix for chapters 04–05.

## Topic A — multi-channel AI assistant integration

### A1. Telegram Bot API

Verified: <https://core.telegram.org/bots/api>

- Two mutually exclusive update mechanisms: `getUpdates` (long polling) vs
  webhooks. Updates are queued server-side up to 24 h.
- **Long polling**: outbound `GET …/getUpdates` with `offset`, `timeout`
  (long-poll seconds), `allowed_updates`. Recalculate `offset` after each
  response to avoid duplicates.
- **Webhooks**: public HTTPS URL receiving JSON `Update` POSTs; optional
  `secret_token` header; `max_connections`; ports 443/80/88/8443; retries
  non-2xx then gives up.
- **Self-hosted Pi fit**: webhooks need a public endpoint/tunnel; long
  polling needs only outbound HTTPS — the de-facto self-hosted default.
- Update types: `message`, `callback_query` (inline buttons; clients show a
  progress bar until `answerCallbackQuery`), etc.

### A2. WhatsApp Cloud API

Verified: <https://developers.facebook.com/docs/whatsapp/cloud-api>

- Built on Meta's Graph API over HTTPS, OAuth tokens, JSON.
- **Webhook-based and cloud-hosted**: inbound messages arrive only via
  webhook — the Pi cannot receive them without a public HTTPS endpoint.
- Needs a Meta Business Portfolio, WABA and business phone number; message
  **templates** (pre-approved) outside the 24 h customer-service window;
  rate limits (80 msg/s default throughput).
- Policy: "Using unauthorized third-party tools is prohibited."

### A3. Baileys (community WhatsApp library)

Verified: <https://github.com/WhiskeySockets/Baileys>

- "A WebSockets-based TypeScript library for interacting with the WhatsApp
  Web API" (~11.2 k stars, MIT). Links a _normal_ WhatsApp number like
  WhatsApp Web does — no Meta business account — but is **unofficial**:
  explicit "not affiliated/authorized/endorsed" disclaimer; ToS risk.

### A4. Matrix bots — matrix-nio / maubot

Verified: <https://github.com/matrix-nio/matrix-nio> ·
<https://matrix-nio.readthedocs.io/en/latest/nio.html> ·
<https://github.com/maubot/maubot>

- `matrix-nio`: Matrix client library with transparent E2EE (libolm),
  `AsyncClient.sync_forever(timeout_ms)` long-polls `/sync`; react to room
  events via `add_event_callback(callback, RoomMessageText)`; send via
  `room_send()`.
- `maubot`: plugin-based Matrix bot system (AGPL-3.0, mautrix-python) —
  host one bot process, write plugins.
- Self-hosted fit: the bot is an ordinary Matrix account; outbound long-poll
  only — same property as Telegram.

### A5. The adapter/connector pattern (verified: Rasa)

Verified: <https://rasa.com/docs/rasa/connectors/custom-connectors/>

- Every channel is two classes: `InputChannel` (`name()` = webhook URL
  prefix, `blueprint()` with `/webhook` receive route) and `OutputChannel`
  (`send_text_message(recipient_id, text)` plus optional images/buttons).
- The seam is generic: the receive route builds
  `UserMessage(text, output_channel, sender_id)` → core → responses flow
  back through the `OutputChannel`. Channel identity is a `name` string.
- Streaming hooks: `supports_streaming = True` +
  `send_response_chunk_start/chunk/end`; channels dedupe chunks vs the final
  `send_text_message`.
- Rasa OSS is in maintenance mode; the pattern, not the project, is the
  reference.
- Botpress/"ChatGPT connectors" equivalents: _unverified_.

### A6. OpenClaw — one assistant across many channels

Verified: <https://github.com/openclaw/openclaw> (README)

- "OpenClaw is an open-source AI assistant that runs on your own computer
  and meets you in the channels you already use: Discord, iMessage, Slack,
  Teams, Telegram, WhatsApp, and 20+ more." MIT; ~390 k stars; OpenClaw
  Foundation; "built for Molty, a space lobster AI assistant, by Peter
  Steinberger and the community."
- **Architecture**: one local **Gateway** = "control plane for sessions,
  tools, events, and channel connections"; Control UI / CLI / TUI connect to
  the Gateway; **Channels** plug WhatsApp, Telegram, Slack, Discord, Google
  Chat, Signal, iMessage into it; models/harnesses are swappable plugins.
  Exactly "one core, per-channel adapters". Docs: docs.openclaw.ai.
- Security: inbound messages treated as untrusted; DM channels require
  pairing approval (`openclaw pairing approve`); sandboxable tools.
- "formerly Clawdbot/Moltbot": _unverified_ in the fetched page.

## Topic B — MCP and exposing local hardware/sensors

### B1. MCP specification

Verified: <https://modelcontextprotocol.io/specification/2025-06-18/basic/index>
(+ /server/tools, /server/resources, /server/prompts, /basic/transports)

- **Protocol = JSON-RPC 2.0**: requests (id, result XOR error), notifications
  (no id). Lifecycle (`initialize`/`initialized`, capability negotiation)
  mandatory.
- **Server features**: **Tools** (model-controlled: `tools/list` definitions
  with JSON-Schema `inputSchema`; `tools/call` returns `content[]` +
  optional `structuredContent`); **Resources** (application-driven context,
  each a URI: `resources/list`, `resources/read`, optional subscribe →
  `notifications/resources/updated`); **Prompts** (user templates:
  `prompts/list`, `prompts/get`).
- **Transports**: (1) **stdio** — subprocess, newline-delimited JSON-RPC;
  (2) **Streamable HTTP** — single endpoint accepting POST and GET, may
  return JSON or open an SSE stream; optional `Mcp-Session-Id`; replaces the
  older HTTP+SSE.
- **HTTP security**: validate `Origin` against DNS rebinding; bind
  localhost; implement auth. stdio should take credentials from the
  environment.

### B2. Filesystem reference server

Verified: <https://github.com/modelcontextprotocol/servers> (src/filesystem)

- Reference collection of the MCP steering group. Filesystem tools verbatim:
  `read_text_file`, `read_media_file`, `write_file`, `edit_file` (dry-run
  preview), `list_directory`, `search_files`, `directory_tree`, etc.
- **Access control**: whitelist directories via CLI args or MCP Roots; all
  operations confined to allowed dirs.
- **ToolAnnotations** per tool: `readOnlyHint`, `idempotentHint`,
  `destructiveHint`, `openWorldHint` — how clients gate risky calls.
- Repo warning: reference servers are educational, "not production-ready".

### B3. Hass-MCP — real hardware over MCP

Verified: <https://github.com/voska/hass-mcp>

- "An MCP server for Home Assistant integration" — query state and control
  entities from any MCP client. ~15 tools (`get_entity`, `list_entities`,
  `search_entities_tool`, `entity_action`, `call_service_tool`,
  `get_history`, `get_error_log`, …), prompts (`create_automation`,
  `debug_automation`, `routine_optimizer`), resources
  (`hass://entities/{entity_id}`, …).
- Config: `HA_URL` + `HA_TOKEN` env vars; default stdio; optional `--http
  --port 8000` exposing `/mcp`.
- Security posture: HTTP mode "exposes full Home Assistant control" — they
  require reverse-proxy basic-auth/bearer, VPN/zero-trust, or localhost
  binding; dry-run + automatic backups before writes.
- A second sensor-MCP server: _unverified_ (this one fully verified).

### B4. Official best practices for building an MCP server

From the MCP spec pages (tools/resources/transports), cited per item:

- **Auth/bindings**: stdio credentials from the environment; HTTP servers
  follow the MCP authorization spec; bind 127.0.0.1 by default; validate
  `Origin`; never expose unauthenticated control endpoints.
- **Hygiene**: validate all tool inputs, access-control, rate-limit,
  sanitize outputs; resources: validate URIs, check permissions, correct
  binary encoding.
- **Errors**: protocol errors as JSON-RPC errors (`-32602` unknown tool);
  _execution_ errors as tool results with `isError: true` and actionable
  text "so the model can self-correct and retry".
- **Granularity**: names 1–128 chars `[A-Za-z0-9_.-]`, unique per server;
  aggregators namespace for collisions; human-in-the-loop confirmation for
  sensitive ops.
- **State**: MCP has no protocol-level session — return an opaque handle
  from a creation tool and accept it as an argument (documented lifetime,
  expiry errors).
- **Annotations as hints**: `readOnlyHint`/`idempotentHint`/
  `destructiveHint`/`openWorldHint`.

## Synthesis: what a channel-agnostic + MCP-exposed design converges on

1. **One generic-message core, per-channel translators** — the Rasa
   InputChannel→UserMessage→OutputChannel shape and OpenClaw's
   Gateway/channels split; the core never imports channel code.
2. **Prefer outbound-pull transports on the Pi** — Telegram/Matrix long
   polling need only outbound HTTPS; WhatsApp Cloud + Telegram webhooks need
   a public endpoint or tunnel.
3. **Channels differ in reachability AND legality** — Telegram/Matrix are
   self-host friendly; Baileys (ToS-risky) and Cloud API (account +
   templates + 24 h window) are compromises kept behind one adapter.
4. **Each adapter gets an identity string, a callback surface, and a
   streaming seam** — Rasa's channel `name`, `send_text_message` contract,
   and chunk start/chunk/end hooks.
5. **MCP tools = the public API of the node** — fine-grained tools with
   JSON-Schema inputs and actionable `isError` results let any agent (not
   just chat channels) query sensors and memory identically.
6. **Capabilities are audited by annotations** — mark every tool
   `readOnlyHint`/`destructiveHint` so external agents can self-restrict to
   safe reads.
7. **State as explicit handles, not implicit sessions** — opaque ids with
   documented lifetime (e.g. a generation id for the single LLM slot).
8. **Treat the MCP server as a distinct attack surface** — stdio by default
   on the Pi; HTTP only behind reverse-proxy auth and localhost binding, as
   Hass-MCP prescribes.
