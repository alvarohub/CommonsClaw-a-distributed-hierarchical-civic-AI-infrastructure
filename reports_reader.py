"""Reads the reports/ directory into a prompt-ready digest.

The kami node's Level-0/1 input: short human-readable reports written by
sensor loggers (cron) and by people (the Note button). The LLM's system
prompt gets this digest prepended so it speaks *from* the place.

Deliberately simple: whole files, truncated per-file, newest content kept.
No MCP server, no database — plain files both humans and the LLM can read.
(A full MCP interface, e.g. @modelcontextprotocol/server-filesystem, can
replace this later without changing the report format.)
"""

from __future__ import annotations

from pathlib import Path

REPORTS_DIR = Path(__file__).parent / "reports"
MAX_CHARS_PER_FILE = 1500  # keep the prompt small; reports are short by design
MAX_TOTAL_CHARS = 4000


def read_reports(reports_dir: Path = REPORTS_DIR) -> str:
    """Return a compact digest of all reports, or "" if none exist."""
    if not reports_dir.is_dir():
        return ""

    parts: list[str] = []
    total = 0
    for path in sorted(reports_dir.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if not text:
            continue
        # Keep the header + the NEWEST content (reports append at the end).
        if len(text) > MAX_CHARS_PER_FILE:
            head, _, tail = text.partition("\n\n")
            keep = MAX_CHARS_PER_FILE - len(head) - 40
            text = head + "\n[...older entries omitted...]\n" + tail[-keep:]
        if total + len(text) > MAX_TOTAL_CHARS:
            break
        parts.append(f"--- {path.name} ---\n{text}")
        total += len(text)

    return "\n\n".join(parts)
