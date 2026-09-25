# CivicClaw vs OpenClaw — a comparison

_2026-09-25. Written after reviewing [openclaw/openclaw](https://github.com/openclaw/openclaw)
(390k★, MIT, by Peter Steinberger et al., stewarded by the OpenClaw
Foundation). This document exists because the overlap is real enough to be
worth mapping precisely — and the differences are the actual contribution of
HCA._

## What OpenClaw is

A **personal** AI assistant gateway: one person, one assistant, serving that
person across their chat channels (WhatsApp, Telegram, Slack, iMessage, 20+
more). It runs on your own hardware, keeps state/memory/credentials local,
and swaps model providers as plugins. Well-governed (independent foundation,
no token, no paid tier), impressively engineered, and explicitly _not_ the
"servile superintelligence in someone else's cloud" pattern — it is the good
version of the individualistic assistant.

So the question "is HCA reinventing OpenClaw?" deserves a careful answer.

## Where the mechanics overlap

| Mechanic                   | OpenClaw               | HCA node                             |
| -------------------------- | ---------------------- | ------------------------------------ |
| Local model / local state  | ✅ on your devices     | ✅ on the node                       |
| Persistent memory as files | ✅ workspace files     | ✅ `memory/`, `reports/`, `sensors/` |
| Tool/skill extensibility   | ✅ plugin SDK, ClawHub | ✅ logger processes, report format   |
| Open source, self-hostable | ✅ MIT                 | ✅ (tiered licenses)                 |
| No phone-home              | ✅ opt-out telemetry   | ✅ nothing to phone home to          |

## Where the politics and topology are opposite

|                        | OpenClaw                                       | HCA                                                                                                                     |
| ---------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Whose memory?**      | One person's assistant                         | A **place and its community** — everyone who talks to the node shares one accumulating identity and journal             |
| **Topology**           | One agent + plugins, flat                      | **Hierarchy of levels** (0 AIoT → 1 kami → 2+ city/nation/world), each summarizing at its own scale                     |
| **Between nodes**      | Team deployments = shared config               | **Negotiated transactions** — permission, possibly retribution, when a query crosses a community boundary               |
| **Relationship**       | Meets you in your chat channels                | **Embodiment-first**: the node _is_ the place; its sensors are its body; its personality grows from the place's history |
| **Scale logic**        | Bigger model if you want                       | Smallest sufficient scale, always; energy proportional to the question                                                  |
| **Selection pressure** | Assistant competes for its user's satisfaction | The node belongs to no one; it is accountable to a community, not a customer                                            |

**The mechanics overlap; the politics and topology are opposite.** The worry
about reinvention is actually a good sign: the infrastructure primitives
(local LLM, file-based memory, tool use) are converging across the field.
HCA's contribution is the **civic layer** on top of those primitives.

## Could we use OpenClaw code?

Worth a serious look, with eyes open:

- **Tempting pieces**: the gateway/channel plumbing (if the kami should ever
  answer on Telegram _and_ its AP), the plugin SDK pattern, their
  memory-file conventions, the pairing/trust model for unknown senders
  (maps to "unknown visitor asks the node").
- **Costs**: it is a large TypeScript/pnpm workspace — a different toolchain
  from our small pure-Python codebase, and heavy for a Pi 5. Importing it
  wholesale would pull the node's center of gravity toward "assistant
  infrastructure" and away from "place with a voice".
- **The likely right move**: _patterns, not code_. Read their memory and
  tool architecture when we build ours further (journal promotion into
  identity, skill acquisition, tool permissioning). Their trust model is
  directly relevant when queries start crossing node boundaries. If a real
  channel need appears (e.g. the neighborhood wants the kami on WhatsApp),
  run an OpenClaw instance as a _gateway in front of_ the node — the node
  stays the civic artifact; OpenClaw becomes one of its mouths.

## What HCA still has to invent (that OpenClaw does not have)

1. **Communal memory with plural authorship** — notes from many people,
   synthesized into one place-identity, with care for whose voice dominates.
2. **Level negotiation protocol** — how a Level-1 node asks Level-2 for help:
   what context crosses the boundary (privacy firewall), what the transaction
   costs, who consents. This is the heart of HCA and exists nowhere yet.
3. **Analyst agents (machintropology link)** — specialized agents reading the
   communal memory to identify the community's recurring needs and
   preoccupations; too heavy for the Pi, so they live at Level 2+ and read
   _reports_, not raw logs.
4. **Embodied personality grounded in sensorium** — the kami's character
   shaped by what the place actually does over seasons.
