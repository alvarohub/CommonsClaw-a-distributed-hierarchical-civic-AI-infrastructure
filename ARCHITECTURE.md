# Architecture — how a question becomes an answer

*A reading guide to the codebase, following one question through the system.
Written 2026-09-26; keep updated as the system evolves.*

## The one-paragraph version

A person talks to the kami through a web page served by the node itself.
The page POSTs the question to `web_server.py`, which hands it to
`llm_manager.py` — the only file that talks to the model. The LLM manager
assembles a system prompt (personality + active memory categories), POSTs it
to Ollama's `/api/chat` with `stream=True`, and yields each token chunk back
as a generator. The web server forwards chunks to the browser as SSE events;
the browser appends them to the page. Meanwhile every frontend also publishes
live status (hardware, model metrics, current question) to a single JSON file
via `status_store.py`, which `control.py` renders over SSH. Separate logger
processes (cron) append sensor readings to plain-text files; those files are
read back into the system prompt on the next question.

## The cast

```
PRESENTATION (per visitor)          CORE (one per process)          THE MODEL
──────────────────────────          ──────────────────────          ─────────
static/chat.html (browser)          llm_manager.py ──────────────►  Ollama
static/dashboard.html                    │   (only file that        (llama.cpp,
console.py  (SSH chat)                   │    talks to the model)    127.0.0.1:11434)
main.py + lcd_gui.py (monitor)           │
                                         ├─ reports_reader.py  ◄── memory/, sensors/, reports/
                                         │     (plain-text memory digest into the prompt)
                                         │
                                         ├─ config.py (all settings, one place)
                                         └─ status_store.py ──► /tmp/commonsclaw_status.json
                                                                   ▲ (atomic writes; live pulse,
                                                                     ephemeral — NOT the memory)

SEPARATE PROCESSES                    OPS
─────────────────                     ───
loggers/sensor_*.py (cron)  ──► sensors/ + reports/   (persistent, plain text)
control.py (SSH dashboard)  ◄── reads the status file
                                  benchmark.py → BENCHMARKS.md
                                  ap_up/portal_up/install_autostart/make_cert/push_to_pi.sh
```

## Following one question (web path)

1. **Browser** — `static/chat.html`: `send()` collects the question, the
   selected model, and the active memory toggles (🧠/📡/📝) and POSTs to
   `/api/ask`. It then reads the response body as a Server-Sent-Events stream
   with a hand-rolled parser (`readSSE`), appending each `chunk` event to the
   transcript. A watchdog covers the "connection died before any chunk" case;
   mid-answer pauses are legal and not treated as errors.

2. **Web server** — `web_server.py`: the `ask` route validates the question,
   resolves memory categories (`toggles + slash keywords + auto-detect` via
   `LLMManager.resolve_categories`), and — under a single-slot lock (the Pi
   can only generate one answer at a time) — streams `_stream_question()`'s
   events back on the *same* HTTP response. The asker always gets its own
   answer; a second concurrent asker gets a `busy` event. This same process
   also serves `/api/status`, `/api/models`, `/api/note`, the dashboard's
   `/api/files`, and the captive-portal probe answers.

3. **LLM manager** — `llm_manager.py`: `stream_response()` builds the
   message list — system prompt (personality from `config.SYSTEM_PROMPT`
   + the active memory digest from `reports_reader`) + in-RAM conversation
   history + the question — and POSTs to Ollama. Ollama answers with one JSON
   object per line (NDJSON); each `content` chunk is yielded immediately.
   The final line carries Ollama's own counters (prompt tokens, eval count,
   eval duration) → metrics. The turn is then appended to history.

4. **Ollama / llama.cpp** — the actual model (default `llama3.2:1b`), running
   as a systemd service, loaded in RAM, quantized, CPU-only. Two phases per
   request: *prompt evaluation* (reading everything — dominates wall time
   when the prompt is large) and *generation* (the tok/s we benchmark).

5. **Status store** — `status_store.py`: alongside the answer path, the web
   server publishes every stage (question submitted, model metrics updates,
   turn completed) to `/tmp/commonsclaw_status.json` using temp-file +
   atomic rename. `control.py` polls it from an SSH session. Ephemeral by
   design — it is a pulse, not a memory.

## The memory loop (what makes it a kami)

```
  sensors ──(cron: loggers/sensor_*.py)──► sensors/*.md, reports/*_log.md
  people  ──(💾 button: /api/note)──────► reports/community_notes.md
  humans  ──(hand edits)────────────────► memory/identity.md, journal.md
        │
        ▼  reports_reader.py digest, filtered by category toggles/keywords
  next question's system prompt
```

The kami reads its world through files and writes nothing itself (yet) —
identity curation stays human-gated on purpose.

## Design rules worth knowing before changing anything

- **One model door**: only `llm_manager.py` talks to Ollama. Frontends never do.
- **Files are the memory**: plain markdown, readable by humans, cron, and the
  LLM. No database, no broker, no MCP server (yet — the format is MCP-ready).
- **Ephemeral vs persistent**: `/tmp/commonsclaw_status.json` = live pulse;
  `memory/` `sensors/` `reports/` = the persistent commons.
- **Single-slot generation**: one answer at a time; concurrency is handled by
  refusing gracefully, not by queueing magic.
- **Every push restarts**: `./push_to_pi.sh` rsyncs and restarts
  `commonsclaw-web` — the Pi always runs what's on your Mac.
