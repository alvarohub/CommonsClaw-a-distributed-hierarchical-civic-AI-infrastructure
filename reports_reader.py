"""Reads the node's plain-text memory into a prompt-ready digest.

Three sources, all plain markdown files both humans and the LLM can read:

- reports/  — sensor loggers (cron) and people's notes (the 📝 button)
- sensors/  — one file per sensor + the SENSOR_REPORT.md dashboard
- memory/   — the node's persistent identity and journal (who it is)

Deliberately simple: whole files, truncated per-file, newest content kept.
No MCP server, no database. (A full MCP interface, e.g.
@modelcontextprotocol/server-filesystem, can replace this later without
changing the file formats.)
"""

from __future__ import annotations

from pathlib import Path

BASE = Path(__file__).parent
REPORTS_DIR = BASE / "reports"
SENSORS_DIR = BASE / "sensors"
MEMORY_DIR = BASE / "memory"

MAX_CHARS_PER_FILE = 1500  # keep the prompt small; files are short by design
MAX_TOTAL_CHARS = 5000


def _digest_dir(directory: Path, skip: set[str] = frozenset()) -> list[str]:
    """Digest one directory: header + newest content per file."""
    parts: list[str] = []
    if not directory.is_dir():
        return parts
    for path in sorted(directory.glob("*.md")):
        if path.name in skip:
            continue
        try:
            text = path.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if not text:
            continue
        if len(text) > MAX_CHARS_PER_FILE:
            head, _, tail = text.partition("\n\n")
            keep = MAX_CHARS_PER_FILE - len(head) - 40
            text = head + "\n[...older entries omitted...]\n" + tail[-keep:]
        parts.append(f"--- {directory.name}/{path.name} ---\n{text}")
    return parts


def read_reports() -> str:
    """Return the combined digest of memory + sensors + reports, or ""."""
    sections: list[str] = []

    # Identity first (who the kami is), then the world it senses, then people.
    identity = _digest_dir(MEMORY_DIR, skip={"journal.md"})
    if identity:
        sections.append("## Who you are\n" + "\n\n".join(identity))

    sensors = _digest_dir(SENSORS_DIR, skip={"_INDEX.md"})
    if sensors:
        sections.append("## Sensor readings\n" + "\n\n".join(sensors))

    reports = _digest_dir(REPORTS_DIR, skip={"_INDEX.md"})
    if reports:
        sections.append("## Reports and community notes\n" + "\n\n".join(reports))

    digest = "\n\n".join(sections)
    return digest[:MAX_TOTAL_CHARS]
