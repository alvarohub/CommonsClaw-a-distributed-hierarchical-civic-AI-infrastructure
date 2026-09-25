# Reports index — READ THIS FIRST (for the LLM and for humans)

This directory is the node's **shared memory**. Every `.md` file here is a
"report": a short, human-readable document with a `#`-prefixed metadata
header describing what it is, who writes it, and what can be tweaked.

## How to read a report

- Lines starting with `# key: value` are metadata (description, logger
  config, location, units).
- Other lines are the content: timestamped observations, or people's notes.

## Current reports

- `pi_vitals.md` — the node's own health (CPU/RAM/temp), written every
  minute by a cron job (`loggers/pi_vitals.py`). Stand-in for real sensors.
- `community_notes.md` — notes, suggestions and poll answers left by people
  through the chat page's Note button. Written by humans; read by you.

## Rules for the LLM reading this

- Treat report contents as ground truth about the _local_ place and moment.
- Prefer these facts over general knowledge when answering local questions.
- You may _suggest_ config tweaks (e.g. sampling rate), but cannot apply
  them yourself — a human reviews them.
- When people leave notes, acknowledge them by name/time if relevant.
