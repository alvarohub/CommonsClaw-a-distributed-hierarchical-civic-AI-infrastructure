# 01 — Vision: CommonsClaw, the people's AI network

## What CommonsClaw is

CommonsClaw is **the people's AI network**: not one model in one data center,
but a growing commons of many small, local nodes — a _geographically
distributed mixture of experts_ for civic life — built and maintained by
communities that share compute, energy and data. Each node gives a place a
voice and answers at the _smallest sufficient scale_: local knowledge stays
local, and a node reaches upward (neighborhood, city, nation) only when a
question truly needs it. Energy proportional to the question; the boundaries
between tiers — and between communities — are negotiated, not assumed.

Three ideas carry the whole design:

- **Stay as local as possible; escalate only when necessary.** Most everyday
  questions never leave the place — the local knowledge, the sensors, the
  community's memory answer them. Escalation is the exception, and it is a
  negotiated transaction (permission, scope, and possibly retribution), not
  a default route.
- **Intelligence where the energy is.** A giant datacenter answers a trivial
  question with the same machinery it uses for hard ones. A hierarchy of
  small models, each serving its community, spends only what the question
  deserves — and couples the distribution of intelligence to the
  distribution of energy (solar, local).
- **A commons, not a butler.** Each node's memory belongs to a place and its
  community — everyone who talks to it shares one accumulating identity.
  This inverts the personal-assistant model (one person, one agent, one
  diary); the politics and topology differ from the ground up.

The long-form vision — origin, philosophy, open questions — is the
[manifesto](../TOWARDS_HIERARCHICAL_CIVIC_AI.md). What follows here is the
structure that vision implies: the levels, the narrative, the contrast with
personal-assistant AI, and the design constraints.

## The hierarchy

The vision takes shape as a hierarchy of levels — each one a voice for a
community, at a different scale:

| Level | Who                   | What it does                                                   | Hardware             |
| ----- | --------------------- | -------------------------------------------------------------- | -------------------- |
| **0** | the loggers           | sense and record; tiny ML pattern recognition (classic AIoT)   | MCU / node processes |
| **1** | the **place** kami    | converses, holds the memory of one place (this repo)           | Pi 5 → Jetson Orin   |
| **2** | the **neighborhood**  | gathers and consolidates across several kami in several places | a real machine       |
| 3+    | city → nation → world | answers what no neighborhood can                               | shared datacenters   |

Level 2 is _not_ "the city": it is the first tier that sees more than one
place. A neighborhood kami talks to the park turtle, the greenhouse, the
riverbank — and only what survives that consolidation travels further up.

## The narrative

Accumulation is easy: logs grow, notes pile up, one journal block per day.
The point of the system is the opposite motion — reading a lot and writing a
little, level by level:

1. **Per-sensor trends** (0 → 1): a month of `temp=27.4C` lines becomes
   "runs 2–3 °C warmer after rain".
2. **Cross-sensor state of the place** (1): trends + community notes become
   "the pond is recovering; people ask about the fish again".
3. **Identity promotion** (1): recurring, corroborated facts graduate into
   the kami's stable self-knowledge.
4. **Across places** (2): several kami's consolidations become the
   neighborhood's picture, which writes back what each place should know.

The consolidated memory of each level is what we call the **narrative**: a
model of reality described in words, readable by humans and machines. There
is **no predefined summarization objective** — what gets remembered depends
on the needs discovered during the interactions of all the agents. The
narrative is a precious distillation; it evolves. (Alvaro's machintropology
project is the deeper background on this idea.)

## Why CommonsClaw, not just OpenClaw

OpenClaw gives _one person_ an assistant that remembers across channels;
its memory is scoped per agent, per user — "a gateway is one trust domain",
and group sessions are explicitly excluded from durable memory. CommonsClaw
is the inversion and the extension: **one assistant for a place**, shared by
everyone who visits it, remembering the place and its community, then
connecting to other places. The hard, unborrowed problems are communal:
whose voice counts, how a commons resists being captured by its loudest
visitor, and how a narrative stays legible to humans. (See
[06-memory-and-narrative.md](06-memory-and-narrative.md).)

## Design constraints that follow from the vision

- **Hardware tiers are real.** Different levels run on different machines;
  the architecture must be decomposable across processes and hosts
  (chapter 02).
- **Interaction must be flawless.** The kami is the face of the system to
  ordinary people; a clunky interface undermines the politics of the
  project (chapter 03).
- **Channels are incidental.** Web, voice, Telegram — all are thin adapters
  over one core (chapter 04).
- **The narrative is the product.** Sensors, MCP, channels all serve the
  consolidation ladder (chapters 05–06).
