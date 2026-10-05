# 01 — Vision: a society of kami, and the narrative

## The hierarchy

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
