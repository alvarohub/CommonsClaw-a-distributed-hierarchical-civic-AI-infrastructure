"""Reads the node's plain-text memory into a prompt-ready digest.

Three category folders, all plain markdown readable by humans and the LLM:

- identity/   — who the kami is (identity.md) + its journal
- sensors/    — one file per sensor + index.md (the cross-sensor dashboard)
- community/  — notes.md (people's 📝 notes: suggestions, polls, comments)

Deliberately simple: whole files, truncated per-file, newest content kept.
No MCP server, no database. (A full MCP interface, e.g.
@modelcontextprotocol/server-filesystem, can replace this later without
changing the file formats.)
"""

from __future__ import annotations

from pathlib import Path

BASE = Path(__file__).parent
IDENTITY_DIR = BASE / "identity"
SENSORS_DIR = BASE / "sensors"
COMMUNITY_DIR = BASE / "community"

MAX_CHARS_PER_FILE = 900  # keep the prompt small; files are short by design
MAX_TOTAL_CHARS = 4000

# The three memory categories, toggleable per request from the web UI and/or
# force-enabled with slash keywords (/identity, /sensors, /community).
CATEGORIES = ("identity", "sensors", "community")


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


def read_reports(categories: set[str] | None = None) -> str:
    """Return the digest for the given categories, or "" if none active.

    categories ⊆ {"identity", "sensors", "community"}; None means all on.
    """
    if categories is None:
        categories = set(CATEGORIES)

    sections: list[str] = []

    if "identity" in categories:
        identity = _digest_dir(IDENTITY_DIR, skip={"journal.md"})
        if identity:
            sections.append("## Who you are\n" + "\n\n".join(identity))

    if "sensors" in categories:
        sensors = _digest_dir(SENSORS_DIR)
        if sensors:
            sections.append("## Sensor readings\n" + "\n\n".join(sensors))

    if "community" in categories:
        reports = _digest_dir(COMMUNITY_DIR)
        if reports:
            sections.append("## Community notes\n" + "\n\n".join(reports))

    digest = "\n\n".join(sections)
    return digest[:MAX_TOTAL_CHARS]
