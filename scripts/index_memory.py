#!/usr/bin/env python3
"""index_memory.py — generate memory/_index.json for AAA repo memory/.

Scans every .md file under memory/, extracts first-line title, date from
filename (YYYY-MM-DD prefix if present), and tags from `#tag` markers
in content. Writes memory/_index.json. Safe to re-run any time.

CLAIM: entropy reduction per Beautiful-One invariant (4 invariants from
.github/copilot-instructions.md, §4). Without this index, agents must
parse 267 memory files cold — a behavioral-sink pattern (Anti-Calhoun §3).

Zen: simple, deterministic, no network. Idempotent.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MEMORY_DIR = REPO_ROOT / "memory"
OUTPUT = MEMORY_DIR / "_index.json"
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")
TAG_RE = re.compile(r"(?:^|\s)#([a-z][a-z0-9_-]{1,40})", re.IGNORECASE | re.MULTILINE)
SKIP_PARTS = {"node_modules", ".git", "dist", "build", "scars_archived"}


def first_nonblank_line(text: str) -> str:
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        # skip markdown headings for size — keep as title
        return line[:240]
    return ""


def extract_date(path: Path) -> str | None:
    """Filename YYYY-MM-DD prefix or parent dir name."""
    m = DATE_RE.match(path.name)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    parent = path.parent.name
    m = DATE_RE.match(parent)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None


def extract_tags(text: str) -> list[str]:
    seen = set()
    for m in TAG_RE.finditer(text):
        seen.add(m.group(1).lower())
    return sorted(seen)[:8]  # cap to 8 tags/file (strange-loop: bounded)


def build_index() -> dict:
    if not MEMORY_DIR.is_dir():
        return {"schema": "memory-index/v1", "files": [], "error": "memory/ missing"}

    files = []
    for path in sorted(MEMORY_DIR.rglob("*.md")):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        files.append(
            {
                "path": rel,
                "title": first_nonblank_line(text),
                "date": extract_date(path),
                "tags": extract_tags(text),
                "bytes": path.stat().st_size,
            }
        )

    return {
        "schema": "memory-index/v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(files),
        "files": files,
    }


def main() -> int:
    index = build_index()
    OUTPUT.write_text(json.dumps(index, indent=2, sort_keys=True), encoding="utf-8")
    print(f"✓ indexed {index['count']} memory files → {OUTPUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
