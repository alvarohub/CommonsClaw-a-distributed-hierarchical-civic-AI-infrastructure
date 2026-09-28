# OpenClaw memory & consolidation — verified research notes

_Compiled 2026-09-28 from [docs.openclaw.ai](https://docs.openclaw.ai/) and
[github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) (main branch,
around release v2026.9.6). Everything below is quoted or paraphrased from a page or
file I actually read; where I could not verify something I say so explicitly._

Scope note: memory is implemented almost entirely in a **bundled plugin called
`memory-core`**, living at [`extensions/memory-core/`](https://github.com/openclaw/openclaw/tree/main/extensions/memory-core).
The user-facing config surface is split between top-level `memory.*` (search/embeddings)
and `plugins.entries.memory-core.config.*` (dreaming, admission policy).

---

## 1. Memory architecture

### 1.1 The headline claim: files, not a database

> "OpenClaw remembers things by writing plain Markdown files in your agent's
> workspace (default `~/.openclaw/workspace`). The model only remembers what gets
> saved to disk; there is no hidden state."
> — <https://docs.openclaw.ai/concepts/memory>

The architecture page states this as design principle #1:

> "**No hidden state.** The model only remembers what is written to files in the
> agent workspace. Every memory surface is inspectable and editable with a text editor."
> — <https://docs.openclaw.ai/concepts/memory-architecture>

SQLite exists, but as a **derived index + provenance store**, not as the canonical memory.
"OpenClaw memory is a set of plain files and one SQLite index" (same page).

### 1.2 The four memory files (agent workspace)

From <https://docs.openclaw.ai/concepts/memory> and
<https://docs.openclaw.ai/concepts/agent-workspace>:

| File                                                       | Role                                                                                                                                               | Injection                                            |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `USER.md` (optional)                                       | user model: stable preferences as dated **imperative directives** with `active` / `superseded` status                                              | loaded at session start, **fixed 4,000-char budget** |
| `MEMORY.md`                                                | curated long-term memory: durable non-profile facts, standing decisions, short summaries. "not a raw transcript, daily log, or exhaustive archive" | loaded at session start, budgeted                    |
| `memory/YYYY-MM-DD.md` (and `memory/YYYY-MM-DD-<slug>.md`) | daily notes / working layer — "detailed daily notes, observations, session summaries, and raw context"                                             | **never injected**; searchable on demand             |
| `DREAMS.md` (or legacy `dreams.md`)                        | Dream Diary + consolidation sweep summaries, for human review                                                                                      | never injected                                       |

Plus the non-memory bootstrap files injected under "Project Context":
`AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `BOOTSTRAP.md` (first run only)
— <https://docs.openclaw.ai/concepts/context>.

File-name constant verified in code:
[`extensions/memory-core/src/dreaming-dreams-file.ts`](https://github.com/openclaw/openclaw/blob/main/extensions/memory-core/src/dreaming-dreams-file.ts)
— `export const DREAMS_FILENAMES = ["DREAMS.md", "dreams.md"] as const;`
and the managed-block markers `<!-- openclaw:dreaming:deep:start -->` / `:end`.

Optional extra surfaces:

- `memory/imports/codex/`, `memory/imports/claude-code/`, `memory/imports/hermes/` — imported
  memory from other assistants, indexed but **not merged** into `MEMORY.md`
  (<https://docs.openclaw.ai/concepts/memory>).
- `memory/dreaming/<phase>/YYYY-MM-DD.md` — optional per-phase report files
  (<https://docs.openclaw.ai/concepts/dreaming>).
- `memory/.dreams/` — **legacy** machine state (JSON, incl. `events.jsonl`). Now migrated
  into SQLite by Doctor; see §2.5.

### 1.3 The tier model (the important structural idea)

Verbatim table from <https://docs.openclaw.ai/concepts/memory-architecture>:

| Tier         | Surface                                                 | Written by                                          | Injected                                               |
| ------------ | ------------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------ |
| Instructions | `AGENTS.md` and workspace instruction files             | Human only                                          | Always, at session start                               |
| Curated core | `MEMORY.md`, `USER.md`                                  | Dreaming consolidation; direct user request         | At session start when provenance is eligible; budgeted |
| Episodic     | `memory/YYYY-MM-DD.md` daily notes, session transcripts | Agent during work; memory flush; transcript capture | Never; searchable on demand                            |
| Prospective  | Standing intents (SQLite) and cron jobs                 | `intent` tool; scheduled tasks                      | Only when a trigger fires                              |
| Review       | `DREAMS.md`, dreaming reports                           | Dreaming phases                                     | Never; for human reading                               |

> "The boundary that matters most is between the **curated core** and the **episodic**
> tier. … Nothing crosses from episodic to curated without passing the promotion gates."

### 1.4 Where the SQLite lives

From <https://docs.openclaw.ai/concepts/multi-agent> ("Paths") and
<https://docs.openclaw.ai/concepts/memory-builtin>:

| What                                                                            | Path                                                       |
| ------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Config                                                                          | `~/.openclaw/openclaw.json` (env `OPENCLAW_CONFIG_PATH`)   |
| State dir                                                                       | `~/.openclaw` (env `OPENCLAW_STATE_DIR`)                   |
| Default agent workspace                                                         | `<stateDir>/workspace` (env `OPENCLAW_WORKSPACE_DIR`)      |
| Other agents' workspace                                                         | `<stateDir>/workspace-<agentId>`                           |
| Agent dir                                                                       | `~/.openclaw/agents/<agentId>/agent`                       |
| **Sessions, transcripts, memory index, standing intents, auth profiles**        | `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite` |
| Shared gateway state (skill library, user preferences, personal model accounts) | `~/.openclaw/state/openclaw.sqlite`                        |
| Legacy/archive session artifacts                                                | `~/.openclaw/agents/<agentId>/sessions/`                   |

Config key: `memory.search.store.fts.tokenizer` (`unicode61` default, `trigram` for CJK);
`memory.search.store.vector.enabled` (default `true`, sqlite-vec) with automatic
fallback to in-process cosine similarity when sqlite-vec is unavailable
(<https://docs.openclaw.ai/reference/memory-config>).

> "The index shares `openclaw-agent.sqlite` with canonical sessions, transcripts, and
> other durable agent state. Never delete that database … to reset memory."
> — <https://docs.openclaw.ai/concepts/memory-builtin>

### 1.5 Indexing mechanics

From <https://docs.openclaw.ai/concepts/memory-builtin>:

- Indexes `MEMORY.md`, root `USER.md`, and `memory/*.md` into chunks of
  **400 tokens with 80-token overlap**.
- Embeddings stored as little-endian float64 BLOBs; sqlite-vec keeps a separate float32 index.
- File watching triggers a **debounced reindex (1.5 s default)**.
- Extra roots via `memory.search.extraPaths` (string or `{ path, pattern }`).
- Full reindexes build a replacement in a temp DB and publish atomically.

### 1.6 Provenance columns (the security spine)

> "Every entry in the memory index carries provenance metadata stored as SQLite
> columns the model cannot write through prose."
> — <https://docs.openclaw.ai/concepts/memory-architecture>

- **Origin class**, a closed set: `owner`, `agent`, `untrusted`, `system`.
- **Session kind**: interactive / cron / heartbeat / sub-agent.
- **Observed timestamp + supersession key**.

Two structural rules follow:

- **Session-kind gating** — cron, heartbeat and sub-agent sessions produce no durable
  memory candidates at all.
- **Recall-loop prevention** — "Content that was injected into context from memory …
  is structurally marked and never re-extracted as a new memory. A fact recalled one
  hundred times stays one fact."

Also: network-sourced tool results **taint the rest of the turn**, so assistant text
derived from a web fetch is classified `untrusted` even inside an owner turn.

### 1.7 Pluggable engines

`plugins.slots.memory` selects the engine (<https://docs.openclaw.ai/concepts/memory>):

- **Builtin** (`memory-core`, default) — SQLite FTS5 + vectors, no extra deps.
- **Honcho** — plugin, cross-session memory with user modeling.
- **LanceDB** — plugin (`/plugins/memory-lancedb`).
- **`memory-wiki`** — a _bundled additional layer_, not a replacement: compiles durable
  memory into a wiki vault with claims/evidence/contradiction tracking and its own tools
  (`wiki_status`, `wiki_search`, `wiki_get`, `wiki_apply`, `wiki_lint`).

---

## 2. Consolidation — "dreaming"

**Yes — "dreaming" is exactly what you guessed: a scheduled background job that
distils episodic material into long-term memory.** It has its own doc page:
<https://docs.openclaw.ai/concepts/dreaming>.

> "Dreaming is the background memory consolidation system in `memory-core`. It moves
> strong short-term signals into durable memory while keeping the process explainable
> and reviewable."

And from <https://docs.openclaw.ai/concepts/memory>:

> "Dreaming is the default background consolidation path for memory. It collects
> short-term recall signals, scores candidates, and promotes only qualified owner or
> agent-derived items into long-term memory (`MEMORY.md`)."

### 2.1 Three phases per sweep

| Phase | Purpose                                   | Durable write         |
| ----- | ----------------------------------------- | --------------------- |
| Light | Sort and stage recent short-term material | No                    |
| REM   | Reflect on themes and recurring ideas     | No                    |
| Deep  | Score and promote durable candidates      | **Yes (`MEMORY.md`)** |

Order is light → REM → deep, in one sweep. Light and REM write managed
`## Light Sleep` / `## REM Sleep` blocks and record reinforcement signals; neither
ever touches `MEMORY.md`.

### 2.2 The deep-phase algorithm (documented, not guessed)

Two gates in sequence (<https://docs.openclaw.ai/concepts/memory-architecture>,
<https://docs.openclaw.ai/concepts/dreaming>):

**Gate 1 — deterministic scoring.** Six weighted base signals plus phase reinforcement:

| Signal              | Weight | Description                                          |
| ------------------- | ------ | ---------------------------------------------------- |
| Relevance           | 0.30   | Average retrieval quality for the entry              |
| Frequency           | 0.24   | How many short-term signals the entry accumulated    |
| Query diversity     | 0.15   | Distinct interactive recall queries that surfaced it |
| Recency             | 0.15   | Time-decayed freshness score                         |
| Consolidation       | 0.10   | Multi-day recurrence strength                        |
| Conceptual richness | 0.06   | Concept-tag density from snippet/path                |

Thresholds `minScore`, `minRecallCount`, `minUniqueQueries` **must all pass**.
Candidates with origin class `untrusted` or `system` are removed _before the prompt is
built_ — "This is a precondition, not a score penalty: no amount of recall frequency
promotes untrusted content into the curated core."

The philosophical line worth stealing:

> "Recall behavior drives the ranking: memory graduates because it kept being useful,
> not because it was written confidently."

**Gate 2 — model consolidation.** A **tool-free completion** receives the gated
candidates plus the current `MEMORY.md` and:

> "The model returns operation decisions, not replacement memory prose. The memory
> writer applies those decisions to the existing file using each candidate's bounded,
> sourced entry."

Accepted rewrites must:

- preserve prior entries within `phases.deep.maxPriorEntryLossFraction` (default `0.25`)
- include every promoted candidate's `Source: path#Lx-Ly` reference
- stay within the `MEMORY.md` bootstrap-safe budget
- parse as the expected structured response

Failure → **append-only fallback** for that sweep.

**Write safety**: optimistic concurrency — the content hash captured when the
consolidation input was built is re-checked immediately before an atomic rename; if an
editor or another session changed the file, the rewrite is aborted and the append
fallback runs. The **pre-image of every accepted rewrite is stored in SQLite plugin
state**, and a human-readable diff summary is appended to `DREAMS.md`.

Each promoted entry gets trailing recall metadata: up to three concept tags in
`<!-- trigger: phrase one, phrase two -->` and `<!-- importance: N -->` (1–10).
`phases.deep.maxPromotedSnippetTokens` defaults to `160`.

### 2.3 Which model runs it

- **Consolidation**: a tool-free completion; the docs do not name a separate cheap model
  for it — it runs inside the `memory-core` plugin subagent budget.
- **Dream Diary narrative**: "using the workspace agent's **default model** unless
  `dreaming.model` is configured. If the configured model is unavailable, the diary run
  retries once with that agent's default model."
- Overriding requires a trust gate: `plugins.entries.memory-core.subagent.allowModelOverride: true`,
  optionally narrowed with `subagent.allowedModels`.
- Dreaming completions share the **background work budget**: "at most three runs in
  total, with up to three available to `memory-core`"
  (<https://docs.openclaw.ai/concepts/queue#background-work>).

So: it _can_ be a cheaper/local model, but the default is the agent's own model.
I found **no** documented default of "always use a cheap model for dreaming".

### 2.4 Scheduling

Config lives under `plugins.entries.memory-core.config.dreaming`
(<https://docs.openclaw.ai/reference/memory-config#dreaming>):

| Key                                     | Type        | Default                          |
| --------------------------------------- | ----------- | -------------------------------- |
| `enabled`                               | boolean     | `true`                           |
| `frequency`                             | cron string | `0 3 * * *` (03:00 daily)        |
| `timezone`                              | string      | — (e.g. `"America/Los_Angeles"`) |
| `model`                                 | string      | agent default model              |
| `phases.deep.maxPromotedSnippetTokens`  | number      | `160`                            |
| `phases.deep.maxPriorEntryLossFraction` | number      | `0.25`                           |

> "when enabled, `memory-core` auto-manages one recurring cron job for a full dreaming sweep."

Slash commands: `/dreaming status|on|off|help`.
CLI: `openclaw memory promote [--apply|--limit N]`, `openclaw memory promote-explain "<query>"`,
`openclaw memory rem-harness`, `openclaw memory rem-backfill`, `openclaw memory session-backfill`.

### 2.5 About that commit message ("preserve historical dreaming jobs until Doctor repair")

**Partially verified.** I could not retrieve the literal commit message — GitHub code
search does not index commit messages, and my PR search for the phrase returned no
readable result. I can confirm the _behaviour_ it describes, both in docs and code:

From <https://docs.openclaw.ai/concepts/dreaming> ("Scheduling"):

> "Runtime reconciliation owns only jobs declared as `memory-core:memory-dreaming-promotion`.
> It uses Doctor's read-only classifier on the active jobs already listed to report
> historical rows. **Recognized legacy or phase jobs require Doctor repair before runtime
> creates or updates the managed job.** … Jobs with historical tags and authored payloads
> remain untouched and produce a manual-review warning …
> Run `openclaw doctor --fix` to adopt historical dreaming jobs identified by ownership
> metadata and known generated payloads. … Doctor first saves a verified SQLite backup,
> then adopts one unified job in each persisted cron store partition without changing its
> ID, ordering, or runtime state. If only legacy light/REM jobs exist, it promotes the
> oldest valid phase job in place."

Code confirming the same:

- [`extensions/memory-core/src/dreaming-cron-contract.ts`](https://github.com/openclaw/openclaw/blob/main/extensions/memory-core/src/dreaming-cron-contract.ts)
  — `export const MANAGED_DREAMING_DECLARATION_KEY = "memory-core:memory-dreaming-promotion";`
  with the comment _"Stable declaration shared by runtime convergence and explicit Doctor adoption."_
- [`extensions/memory-core/src/migration/doctor-dreaming-cron.ts`](https://github.com/openclaw/openclaw/blob/main/extensions/memory-core/src/migration/doctor-dreaming-cron.ts)
  — handles `LEGACY_MEMORY_LIGHT_DREAMING_CRON_NAME` / `LEGACY_MEMORY_REM_DREAMING_CRON_NAME`
  and emits _"Repaired N historical dreaming cron row(s); survivor IDs, order, and runtime
  state preserved. SQLite backup: …"_
- [`extensions/memory-core/src/migration/dreaming-cron-classifier.ts`](https://github.com/openclaw/openclaw/blob/main/extensions/memory-core/src/migration/dreaming-cron-classifier.ts)
- [`extensions/memory-core/src/migration/doctor-dreaming-state.ts`](https://github.com/openclaw/openclaw/blob/main/extensions/memory-core/src/migration/doctor-dreaming-state.ts)

So "historical dreaming jobs" are **stale cron rows from an older three-job (light/REM/deep)
scheduling scheme**, which the runtime deliberately refuses to touch until `openclaw doctor --fix`
adopts or retires them. It is a scheduler-migration concern, not a memory-content concern.

Also relevant: legacy dreaming _state_ used to be JSON under `memory/.dreams/`; live state is
now SQLite plugin storage, and "Doctor owns migration of legacy dreaming JSON state from
`memory/.dreams/`" (<https://docs.openclaw.ai/concepts/memory>).

### 2.6 Where the material comes from (the write path)

Mermaid diagram reproduced from <https://docs.openclaw.ai/concepts/memory-architecture>:

```
Interactive sessions --(notes, flush)--> Episodic tier + index (with provenance)
Session end --(transcript ingestion)--> Episodic tier
Pre-compaction flush --(facts to daily notes)--> Episodic tier
Episodic tier --> Dreaming: gate (deterministic)
  --> gated candidates (never untrusted or system) --> Consolidation (model, bounded)
    --> merge/supersede/dedupe --> MEMORY.md / USER.md
    --> summary + pre-image --> DREAMS.md
```

> "Durable memory has exactly one primary writer: the dreaming consolidation pass.
> Everything else feeds it."

Session transcript ingestion: only **interactive** sessions are eligible; personal/sensitive
content is redacted; runtime-marked recalled context is stripped so recalled snippets
cannot be re-learned.

### 2.7 Grounded backfill (replaying old notes)

`openclaw memory rem-backfill --path ./memory [--stage-short-term]` reads historical
`memory/YYYY-MM-DD.md` as standalone day files and writes **reversible** structured review
output into `DREAMS.md`; `--stage-short-term` puts candidates into the same short-term store
the deep phase uses (it does **not** promote directly). `--rollback` / `--rollback-short-term`
undo it. `MEMORY.md` is still only written by deep promotion.

### 2.8 Research lineage cited by the docs

The docs explicitly ground the design in published work — useful for a related project's
bibliography:

- sleep-time compute — arXiv:2504.13171 (justifies offline pre-digestion)
- Generative Agents — arXiv:2304.03442 (reflection with evidence citations; relevance +
  recency + importance ranking with importance assigned at _write_ time)
- LongMemEval — arXiv:2410.10813 ("what was written matters more than how it is indexed")
- PrefEval — arXiv:2502.09597 (restating preferences as directives)
- HorizonBench — arXiv:2604.17283 (stale preference selection)
- TriggerBench — arXiv:2606.23459 (prospective recall degrades with context length)
- MINJA memory-injection attack — arXiv:2503.03704; OWASP Agentic Applications ASI06

---

## 3. Retrieval — how memory reaches the prompt

Two lanes, split by cost (<https://docs.openclaw.ai/concepts/memory-architecture>).
There **is** an explicit distinction between always-loaded and searched-on-demand.

### Lane 1 — always on, zero model calls

Three mechanisms:

1. **Bootstrap injection (full-file).** `MEMORY.md` and `USER.md` load at session start
   _when the runtime classifies their provenance as eligible_. Budgets:
   `agents.defaults.bootstrapMaxChars` = 20,000 per file, `bootstrapTotalMaxChars` = 60,000
   total, and `USER.md` has a hard 4,000-char cap that config can lower but never raise.
   Truncation keeps the on-disk file intact and injects a notice.
   Eligible files **refresh per turn**, so a long-lived session picks up consolidation results
   without restarting.

2. **Ranked search** (`memory_search`, hybrid). Formula from
   <https://docs.openclaw.ai/concepts/memory-search>:

   ```
   hybrid relevance × recency decay × importance multiplier   → then MMR diversity
   ```

   - Vector + BM25 run in parallel and merge; filename/path indexed separately.
   - Recency: **exponential decay, 30-day half-life**, applied to dated daily notes only;
     `MEMORY.md`, `USER.md` and undated `memory/` files are evergreen.
   - Importance: integer 1–10, "assigned once at write time by writers that already have a
     model in the loop"; null is neutral. No query-time model call.
   - MMR with fixed **lambda 0.7**, Jaccard overlap over snippet tokens.
   - `memory.search.query.maxResults` default `6`, `minScore` default `0.35`.

3. **Trigger injection.** Writers attach trigger phrases as trailing HTML comments on the
   same `MEMORY.md`/`USER.md` line:

   ```markdown
   - Keep the gateway on loopback. <!-- trigger: gateway setup, network safety --> <!-- importance: 9 -->
   ```

   Every inbound message runs a fast lexical + vector prefilter against those triggers;
   matches **at or above score 0.72** are injected as a compact hidden context block,
   **at most three per turn**.

   > "Auto-injection is restricted to the curated tier. Entries from `MEMORY.md` and
   > `USER.md` qualify; daily notes and transcripts **never** auto-inject, regardless of
   > match strength. This restriction is a security property, not a tuning choice."

**Project scoping** (a fourth ranking dimension): a turn inside a Git repo annotates new
memories with `<!-- project: github.com/openclaw/openclaw -->`, derived from the normalised
`origin` remote (or absolute root path when there is no origin). Each session keeps up to
**four** recently active repo keys; ranked search boosts entries from active repos, mildly
demotes others, leaves untagged memory neutral. Trigger injection is stricter: a tagged
entry is eligible only while _every_ project key on it is active. `USER.md` and standing
intents are never project-scoped.

### Lane 2 — escalation (explicit, blocking sub-agent)

**Active Memory** (<https://docs.openclaw.ai/concepts/active-memory>) runs a real agent turn
that can search and read across conversation history. Default mode `escalate` fires only when
**both** deterministic conditions hold:

1. the message shows recall intent (explicit references to the past, temporal phrasing,
   direct questions about prior decisions/conversations); **and**
2. lane 1 produced no strong hit.

`mode: "always"` = unconditional pre-reply recall; `mode: "off"` disables it.

### The agent's explicit tools

From <https://docs.openclaw.ai/concepts/memory>:

- **`memory_search`** — semantic/hybrid search over notes (and optionally session transcripts).
- **`memory_get`** — read a specific memory file or line range.
- **`intent`** — create/list/cancel event-conditioned standing intents.

"All three tools are provided by the active memory plugin (default: `memory-core`)."
Code ref: [`extensions/memory-core/src/tools.ts`](https://github.com/openclaw/openclaw/blob/main/extensions/memory-core/src/tools.ts).

For transcripts there is a separate, deliberately bounded path: `sessions_search` →
`sessions_history` (redacted, byte-capped excerpts). Session hits returned by `memory_search`
carry `sessions/...jsonl` paths that are _search references only_ — `memory_get` cannot read them.

### Standing intents — "prospective memory"

A genuinely distinct mechanism worth noting: intentions are **compiled out of the model**
rather than stored as prose.

- Time-based ("remind me Friday") → a cron job, created at the moment it is uttered.
- Event-based ("when the release comes up, mention the changelog") → a row in a per-agent
  SQLite table via the `intent` tool, with machine-checkable fields: keywords, optional
  trigger embedding, channel and sender scope, expiry, fire budget, cooldown. A deterministic
  prefilter runs on every inbound message; a hit injects hidden context. **No model call in
  the matching path.**
- Lifecycle is explicit state: pending → armed → fired → done / cancelled / expired.
  Anti-nagging is structural: 24 h default cooldown, 3-fire budget, 90-day expiry,
  max 3 intents injected per turn.

---

## 4. Session / history handling vs. context limits

**Both** sliding-window-ish retention and summarisation, plus a third lighter mechanism.

### Compaction (<https://docs.openclaw.ai/concepts/compaction>)

> "Every model has a context window… When a conversation approaches that limit, OpenClaw
> **compacts** older messages into a summary so the chat can continue."

1. Older turns are summarised into a compact entry.
2. The summary is **saved in the session transcript**.
3. Recent messages are kept intact.
4. "The full conversation history stays on disk. Compaction only changes what the model
   sees on the next turn."

Key config under `agents.defaults.compaction`:

| Key                        | Default / note                                                                                        |
| -------------------------- | ----------------------------------------------------------------------------------------------------- |
| `enabled`                  | true (auto-compaction on nearing limit, and on provider context-overflow error → compact and retry)   |
| `mode`                     | `"safeguard"` for new configs (quality audits, corrective retries); `"default"` opts out              |
| `keepRecentTokens`         | `20000` — the cut-point budget for the retained tail                                                  |
| `model`                    | optional separate summarisation model (`provider/model-id`), incl. local, e.g. `"ollama/llama3.1:8b"` |
| `identifierPolicy`         | `"strict"` — preserves opaque identifiers in summaries                                                |
| `maxActiveTranscriptBytes` | optional byte guard, e.g. `"20mb"`, forces compaction on transcript growth                            |
| `notifyUser`               | false — silent by default                                                                             |
| `provider`                 | id of a plugin-registered compaction provider                                                         |

Manual: `/compact`, optionally `/compact Focus on the API design decisions`
(operator focus capped at 800 code points and escaped as prompt data).

### The memory flush — the bridge between compaction and memory

This is the single most transferable idea in the whole system:

> "Before compaction summarizes your conversation, OpenClaw runs a **silent turn** that
> reminds the agent to save important context to memory files. This is on by default;
> set `agents.defaults.compaction.memoryFlush.enabled: false` to turn it off. The flush
> uses a private copy of the conversation, so its housekeeping messages never appear in
> later user turns … Its writes to memory files are still saved normally."
> — <https://docs.openclaw.ai/concepts/memory>

It has its own model override (`compaction.memoryFlush.model`, documented example
`"ollama/qwen3:8b"`), is skipped for sessions without writable workspace access, and a
failure never resets the session.

### Pruning (a third, lighter mechanism)

|              | Compaction                    | Pruning                          |
| ------------ | ----------------------------- | -------------------------------- |
| What it does | Summarizes older conversation | Trims old tool results           |
| Saved?       | Yes (in session transcript)   | No (in-memory only, per request) |
| Scope        | Entire conversation           | Tool results only                |

### Session lifecycle & storage bounds (<https://docs.openclaw.ai/concepts/session>)

- Reset modes: `none` (default — one rolling session, compaction handles growth),
  `daily` (`session.reset.atHour`, default 4), `idle` (`session.reset.idleMinutes`),
  or manual `/new` / `/reset`.
- `session.maintenance`: `pruneAfter: "30d"`, `maxEntries: 5000`, `archiveDashboardAfter: "7d"`,
  `preserveRecent: false`. Over the cap, the oldest _ordinary_ sessions are **archived**,
  not deleted; synthetic cron/hook/heartbeat/subagent rows are disposable.

Inspection: `/status`, `/context list`, `/context detail`, `/context map` (a WinDirStat-style
treemap of what is eating the window), `/usage tokens`.

---

## 5. Multi-agent / multi-user — memory scoping

### The blunt answer on trust

> "A gateway is one trust domain. Everyone who can message a tool-enabled agent shares
> that agent's delegated tool authority… If you need to serve mutually untrusted people
> or organizations, run one gateway per tenant."
> — <https://docs.openclaw.ai/start/teams>

> "Session ownership, visibility in the sidebar, and presence indicators are **usability
> features, not security boundaries**."
> — <https://docs.openclaw.ai/concepts/multi-user>

**This matters enormously for a communal node.** OpenClaw explicitly declines to provide
isolation between users inside one gateway; its answer to "several people, separate memory"
is "several agents" or "several gateways".

### Yes, teams are a first-class deployment

> "One Gateway runs it as a personal assistant on a laptop or as a shared team deployment;
> **configuration is the only difference**." (README / docs index)

Team surfaces that do exist (<https://docs.openclaw.ai/start/teams>,
<https://docs.openclaw.ai/concepts/multi-user>):

- Identity-backed sign-in (Tailscale Serve, Cloudflare Access, GitHub-verified accounts).
- Shared sessions with **three ownership layers**: immutable _creator_, assignable _owner_
  (GitHub-issue-style), and _participants_ history (capped at 32 identities/session).
- Live presence, typing indicators (drafts never enter the transcript or the model context).
- Named operator roles (`gateway.roles.definitions.*`) with session scope, allowed agents,
  operator scopes, and `sandbox: "required"` for guests.
- Git `Co-authored-by` credit from shared sessions.

### How memory is actually scoped

| Surface                                 | Scope                                                                                                                                          | Source                                                               |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `MEMORY.md`, `memory/*.md`, `DREAMS.md` | **per agent workspace — shared by everyone using that agent**                                                                                  | [agent-workspace](https://docs.openclaw.ai/concepts/agent-workspace) |
| `MEMORY.md` injection                   | only in eligible **private** sessions — "subagent, cron, group, and channel sessions omit root memory"                                         | [user-model](https://docs.openclaw.ai/concepts/user-model)           |
| Root `USER.md`                          | shared defaults for the agent                                                                                                                  | [user-model](https://docs.openclaw.ai/concepts/user-model)           |
| **Personal `USER.md`**                  | `users/<canonical-profile-id>/USER.md` **inside the agent workspace** — only enabled when the Gateway has ≥2 distinct unmerged person profiles | [user-model](https://docs.openclaw.ai/concepts/user-model)           |
| Session transcripts                     | per agent, in that agent's SQLite                                                                                                              | [session](https://docs.openclaw.ai/concepts/session)                 |
| Memory index                            | per agent DB; **no cross-agent search**                                                                                                        | [multi-agent](https://docs.openclaw.ai/concepts/multi-agent)         |
| Memory Wiki vault                       | global by default; `plugins.entries.memory-wiki.config.vault.scope: "agent"` splits it                                                         | [multi-agent](https://docs.openclaw.ai/concepts/multi-agent)         |
| Personal skill library                  | per authenticated profile, with explicit "share with team" / "transfer to team"                                                                | [skills](https://docs.openclaw.ai/tools/skills)                      |

The personal-`USER.md` mechanism is the closest thing to per-person memory, and it is
carefully bounded:

> "Each session selects **one** personal `USER.md`: the assigned human owner's file first,
> otherwise the authenticated human creator's file… OpenClaw loads the shared file first
> and the selected personal file second. The personal file **supplements**, rather than
> replaces, the shared file, overriding conflicting shared user preferences, not project
> rules or security policy."

and explicitly:

> "This is **prompt selection, not filesystem secrecy**."

### Session isolation knobs

- `session.dmScope`: `main` (default — **all DMs share one session**), `per-peer`,
  `per-channel-peer` (recommended for multi-user), `per-account-channel-peer`.
  The docs warn: without DM isolation "Alice's private messages would be visible to Bob".
- `session.groupScope`: `per-group` (default) or `main`.
- `memory.search.rememberAcrossConversations`: on for personal installs, **off whenever
  DM isolation is configured**. When on, the retrieval boundary excludes groups/channels
  and the current conversation, and "unknown conversation kinds fail closed".
- `tools.sessions.visibility` (`all` default / `agent` / `tree` / `self`) and
  `tools.agentToAgent` govern cross-session and cross-agent transcript reach.

### Sharing knowledge _deliberately_ between agents

Since cross-agent memory search was removed with QMD:

> "Put intentionally shared Markdown in an explicit shared `memory.search.extraPaths`
> directory when the same reference material should be indexed by multiple agents."
> "For shared notes, keep each workspace's `memory/` directory local and add the shared
> directory's canonical path to `extraPaths`."
> — <https://docs.openclaw.ai/concepts/multi-agent>, <https://docs.openclaw.ai/reference/memory-config>

That is effectively OpenClaw's answer to communal memory: **a shared read-only-ish Markdown
directory indexed by many agents, with each agent keeping its own private daily notes.**

---

## 6. Skills / AGENTS.md — the progressive-disclosure pattern

Source: <https://docs.openclaw.ai/tools/skills>.

> "Skills are markdown instruction files that teach the agent how and when to use tools.
> Each skill lives in a directory containing a `SKILL.md` file with YAML frontmatter and a
> markdown body."

OpenClaw follows the [AgentSkills](https://agentskills.io) spec.

### The loading decision — explicitly two-stage

From <https://docs.openclaw.ai/concepts/context>:

> "The system prompt includes a compact **skills list** (name + description + location).
> This list has real overhead. Skill instructions are _not_ included by default. The model
> is expected to `read` the skill's `SKILL.md` **only when needed**."

So the agent decides by reading the one-line description in an injected
`<available_skills>` XML block, then issuing a normal `read` on the path. That _is_ the
progressive-disclosure pattern, and the cost is quantified:

> "**Per skill:** ~97 characters + your `name`, `description`, and `location` field lengths…
> At ~4 chars/token, 97 chars ≈ 24 tokens per skill before field lengths."

If the block exceeds `skills.limits.maxSkillsPromptChars`, OpenClaw **degrades gracefully**:
it first preserves as many _identities_ (name + location) as fit in a description-free
compact format, then spends any remaining budget on shortened descriptions, then omits
descriptions entirely — and adds a note pointing at `openclaw skills check`.

### Discovery and precedence

| Priority    | Source                     | Path                                                 |
| ----------- | -------------------------- | ---------------------------------------------------- |
| 1 (highest) | Workspace skills           | `<workspace>/skills`                                 |
| 2           | Project agent skills       | `<workspace>/.agents/skills`                         |
| 3           | Personal agent skills      | `~/.agents/skills`                                   |
| 4           | Managed / local skills     | `<state-dir>/skills`                                 |
| 5           | Workshop skills            | `<state-dir>/agents/<agentId>/agent/workshop-skills` |
| 6           | Bundled / Custodian skills | shipped with the install                             |
| 7 (lowest)  | Extra dirs + plugin skills | `skills.load.extraDirs`                              |

`SKILL.md` is found anywhere under a root up to **6 levels deep**; finding one ends traversal
below that directory. Snapshotted at session start, refreshed on `SKILL.md` change
(250 ms debounce), Gateway restart, or new node connection.

### Gating and invocation control

- `metadata.openclaw.requires.{bins, anyBins, env, config}` and `os` filter eligibility at
  load time, so irrelevant skills never cost prompt tokens.
- `disable-model-invocation: true` hides a skill from model-initiated selection while keeping
  it available as an explicit `$name` / `/name` invocation.
- `command-dispatch: tool` lets a slash command bypass the model entirely.
- Per-agent allowlists: `agents.defaults.skills` (baseline) and `agents.entries.*.skills`
  (**replaces**, does not merge).
- A message can explicitly reference up to **eight** skills with `$name`; a new session
  selects up to **64** enabled library skills.

### Skill Workshop — the agent learning new procedures

> "[Skill Workshop] is a proposal queue between the agent and its
> `<state-dir>/agents/<agentId>/agent/workshop-skills` directory. When the agent spots
> reusable work, it **drafts a proposal instead of writing directly to `SKILL.md`**."

`openclaw skills workshop list | inspect | evaluate | apply`. There is a scheduled **weekly
collection review** that may edit Workshop `SKILL.md` files directly. Workshop skills are
per-agent and are not shared until published to the managed library.

This is the same gated-write philosophy as dreaming, applied to procedures instead of facts.

### `AGENTS.md`

`AGENTS.md` is a workspace instruction file, **human-written only** in the tier model,
always injected at session start. It holds "operating instructions for the agent **and how
it should use memory**". Template: <https://docs.openclaw.ai/reference/templates/AGENTS>.
The team-preset role contracts live in `AGENTS.md` specifically "so they also apply in
spawned sessions that do not load `SOUL.md` or `IDENTITY.md`".

---

## Things I could NOT verify

- The exact commit message `fix(memory): preserve historical dreaming jobs until Doctor repair`
  — GitHub code search does not index commit messages and my PR text search returned nothing
  readable. The behaviour is documented and the code exists (§2.5), but I did not see the commit.
- **Which model the consolidation completion uses when `dreaming.model` is unset.** The docs
  name the default model only for the _Dream Diary narrative_; for the consolidation completion
  they say "a tool-free completion" without naming the resolution order.
- **The literal values of `minScore` / `minRecallCount` / `minUniqueQueries`** for deep-phase
  promotion. The docs say "phase policy and thresholds are internal behavior, not user-facing
  config" and the CLI exposes them as override flags only. Defaults exist as
  `DEFAULT_MEMORY_DEEP_DREAMING_MIN_SCORE` etc. in
  `extensions/memory-core/src/short-term-promotion-types.ts`, but I did not read the numbers.
- Whether anything in OpenClaw supports **memory scoped to a place/room rather than a person
  or an agent**. I found no such concept. Group and channel sessions are, if anything,
  _excluded_ from root-memory injection and from durable promotion.
- The purpose of the top-level `config/` directory in the repo (it appeared in a refactor
  commit title alongside `sdk`, `state`, `skills`, but I did not open it).

---

## Patterns worth borrowing for a file-based communal-memory node

Five concrete, grounded ideas.

### 1. Split memory into tiers by _injection policy_, not by topic

The single strongest idea. OpenClaw's tiers are defined by three orthogonal properties —
**who writes it**, **whether it is injected**, and **whether it can be promoted** — and the
hard line sits between _curated core_ (small, always in context, gated writes) and
_episodic_ (large, append-friendly, search-only). A communal node maps onto this cleanly:

- `AGENTS.md` / charter → instructions tier, human-only, always loaded.
- a small `COMMONS.md` → curated core, written only by the consolidation pass.
- `journal/YYYY-MM-DD.md` → episodic, appended freely by sensors, visitors, loggers.
- `DREAMS.md`-equivalent → review tier, never injected, for the human custodians.

The payoff is that the always-loaded surface stays bounded _by construction_ regardless of
how much the place records. OpenClaw enforces this with `bootstrapMaxChars` (20k),
`bootstrapTotalMaxChars` (60k) and a hard 4k cap on `USER.md`, and by truncating the
_injected copy_ while leaving the file on disk intact — a useful trick.

### 2. A nightly consolidation cron whose model output is _decisions_, not prose

The deep phase never lets the model hand back a rewritten file. It returns
merge/supersede/add **operations**, and deterministic code composes the new `MEMORY.md` from
validated source snippets. Then three cheap structural checks decide whether to accept:
prior-entry loss ≤ 25 %, every promoted entry carries a `Source: path#Lx-Ly` anchor, output
fits the budget. Failure → append-only fallback. Plus optimistic concurrency (content hash
re-checked before an atomic rename) so a human editing the file by hand never loses work.

For a Pi-class node this is doubly attractive: a small local model can produce a short
structured decision list far more reliably than a well-formed 2,000-word file, and the
_failure mode is append_, which is always safe. `0 3 * * *` at 1–3 tok/s is entirely feasible.

### 3. Write-time metadata that makes retrieval model-free

OpenClaw stores two annotations as trailing HTML comments on the same Markdown line:

```markdown
- Keep the gateway on loopback. <!-- trigger: gateway setup, network safety --> <!-- importance: 9 -->
```

`importance` (1–10) is scored **once at write time by whoever already had a model loaded**,
and feeds a ranking formula `relevance × recency-decay × importance` with **zero query-time
model calls**. `trigger` phrases drive a lexical+vector prefilter on every inbound message,
injecting at most three entries above score 0.72. Both are plain text — greppable,
hand-editable, diff-able, and degrade to neutral when absent (null importance ranks neutrally,
so old entries need no migration).

This is exactly the right shape for a node where inference is expensive and files are cheap.
Add a `<!-- place: ... -->` or `<!-- sensor: ... -->` key and you get communal scoping the
same way OpenClaw got repo scoping with `<!-- project: ... -->`.

### 4. Provenance as unforgeable columns, with a quarantine tier

> "Origin labels live in SQLite columns written by classification code, never parsed out of
> memory text. Prose claiming to be from the owner does not make it owner content."

Four classes (`owner` / `agent` / `untrusted` / `system`); untrusted and system content can be
_stored and explicitly searched_ but is structurally barred from the curated core and from
auto-injection. Two hygiene rules ride on it: cron/heartbeat/sub-agent sessions produce no
durable candidates at all, and content that came _from_ memory is marked so it is never
re-extracted ("a fact recalled one hundred times stays one fact").

For a shared civic node where anyone in the room can talk to the machine, this is the
mechanism that lets you accept everything into the journal while requiring that promotion to
the communal core pass a trust gate. The recall-loop rule alone prevents the classic
always-on-agent failure where the file fills with restatements of its own prompt.

### 5. Flush before you compact — and keep a two-stage skill/knowledge loader

Two smaller but high-value mechanics:

- **Memory flush**: a _silent_ turn on a private copy of the conversation, run immediately
  before compaction, whose only job is "write down anything important that is not yet on disk".
  It has its own model override (the docs' own example is `"ollama/qwen3:8b"`), and its
  failure never harms the session. This is the cheapest possible insurance against a summary
  eating something the place should have remembered.
- **Progressive disclosure**: put only `name + description + location` for each knowledge
  document in the system prompt (~24 tokens each) and let the agent `read` the full file on
  demand; degrade to identities-only when over budget. Then add OpenClaw's _Skill Workshop_
  twist — when the agent notices a reusable procedure it **drafts a proposal** into a queue
  rather than writing the document itself, and a human (or a weekly review) applies it.
  For a communal artifact, that proposal queue is also the natural place for the community
  to see and contest what the node wants to learn.
