# 06 — Memory and narrative: from OpenClaw to a place

Everything above is accumulation. This chapter is the point: turning logs
and conversations into the **narrative** — a model of the place described
in words, human- and machine-readable, whose shape evolves with use.

## What OpenClaw does (verified, the reference)

Full notes with sources: [research/openclaw-memory.md](research/openclaw-memory.md).
The mechanics worth stealing:

- Memory is **plain markdown** (`MEMORY.md` curated core, `USER.md`,
  `memory/YYYY-MM-DD.md` episodic); SQLite holds only a derived index
  (FTS5 + vectors), never the source of truth.
- Consolidation is a nightly cron sweep they call **"dreaming"**
  (light → REM → deep); only the deep phase may rewrite the curated core.
- Promotion is gated by a **deterministic score** (relevance, frequency,
  query diversity, recency, consolidation, richness) computed _before_ any
  model call — the model is asked only about what passed the gate.
- The model returns **merge/supersede operations, not prose**, validated
  against a ≤25% prior-entry-loss rule, mandatory `Source:` anchors, atomic
  renames, append-only fallback.
- Retrieval: hybrid ranked search with **zero query-time model calls**.

## What does not transfer — and what we must invent

OpenClaw scopes memory **per agent, per user**; group/channel sessions are
explicitly excluded from durable memory. There is no notion of a place, and
no notion of many authors writing one shared identity. CommonsClaw exists
in exactly that gap:

- **Per-place, not per-person.** The identity files describe the pond, not
  a user. Community notes are the place's ears.
- **Multi-author, but curated.** Visitors can suggest; promotion into the
  narrative is gated, loss-bounded, and reversible (git history of
  `identity/`).
- **The "whose voice counts" problem.** A commons resists capture by its
  loudest visitor only if promotion rules are explicit and auditable. This
  is a design problem we do not inherit a solution for.

## The consolidation ladder (borrowed mechanics per level)

| Level | Inputs | Consolidation | Output |
| ----- | ------ | ------------- | ------ |
| 0 → 1 | sensor logs | deterministic gates + small-model reports | per-sensor trends, latest reading |
| 1 | journal, turn log, notes | nightly "dreaming" with score gates, operations-not-prose, `Source:` anchors | identity promotion; the place's self-knowledge |
| 2 | several kami's narratives | cross-place dreaming | the neighborhood narrative, written back down |
| 3+ | neighborhood narratives | larger consolidations | what no neighborhood can answer |

The same file format and the same gated-promotion discipline at every
level — that is what makes the ladder recursive rather than four different
systems.

## Narrative hygiene (the rules we commit to)

- Everything durable lives in plain markdown; every derived index is
  rebuildable.
- Append-only wherever multiple writers exist.
- Every promotion carries a `Source:` anchor and is bounded (≤25% loss
  rule) and reversible (git).
- The model returns operations, never prose, when rewriting memory.
- No predefined summarization objective: the gates decide _what survives_,
  not _what it should mean_.
