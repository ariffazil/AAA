#!/usr/bin/env python3
"""
regenerate_tree777_index.py (v2.0)
Regenerates AAA/wiki/index.md and tree-manifest.json from actual filesystem.

v2.0 changes:
  - Imports scanner from tree777 MCP server (single source of truth)
  - Manifest uses schema_version 2.0 with sha256, tags, slug, uri per entry
  - No host paths leaked in manifest
  - Coverage warnings for thin categories
  - Backward-compatible index.md still generated for human readers

DITEMPA BUKAN DIBERI — Forged, not given.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow importing from the tree777 server package
TREE777_DIR = Path("/root/AAA/mcp/tree777")
sys.path.insert(0, str(TREE777_DIR))

from server import cache, WIKI_ROOT  # noqa: E402

OUTPUT_INDEX = WIKI_ROOT / "index.md"
OUTPUT_MANIFEST = WIKI_ROOT / "tree-manifest.json"

# ── Manifest generator (v2.0) ────────────────────────────────────────────────

def build_manifest() -> dict:
    """Build v2.0 tree-manifest.json with no host paths."""
    entries = cache.entries
    pages: dict[str, dict] = {}

    for e in entries:
        pages[e.uri] = {
            "slug": e.slug,
            "title": e.title,
            "kind": e.kind,
            "category": e.category,
            "tags": e.tags,
            "confidence": e.confidence,
            "summary": e.summary[:200] if e.summary else "",
            "sha256": e.sha256,
            "size": e.size,
            "word_count": e.word_count,
            "updated_at": e.updated_at,
        }

    return {
        "schema_version": "2.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_entries": len(entries),
        "totals_by_kind": cache.totals,
        "categories": cache.categories,
        "coverage_warning": cache.coverage_warnings,
        "template": "tree777://{kind}/{category}/{slug}",
        "entries": pages,
    }


# ── index.md generator (human-readable, backward-compatible) ─────────────────

KIND_ORDER = [
    "axiom", "concept", "skill", "scar", "entity",
    "arifos", "workflow", "infrastructure", "nine-signal",
    "playbook", "raw",
]

KIND_HEADERS = {
    "axiom":          "Axioms — Foundational Invariants",
    "concept":        "Concepts",
    "skill":          "Skills — Reusable Capability Documents",
    "scar":           "Scars — Lessons Sealed as Doctrine",
    "entity":         "Entities",
    "arifos":         "arifOS Federation",
    "workflow":       "Workflows",
    "infrastructure": "Infrastructure",
    "nine-signal":    "Nine-Signal",
    "playbook":       "Playbooks",
    "raw":            "Raw Sources — Immutable Input Material",
}


def build_index_md() -> str:
    """Generate human-readable index.md grouped by kind."""
    entries = cache.entries
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

    lines = [
        "---",
        "title: AAA Wiki Index",
        f"created: 2026-05-17",
        f"updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        "type: index",
        "tags: [federation, wiki, index]",
        "confidence: high",
        "---",
        "",
        "# AAA Wiki — Federation Knowledge Base Index",
        "",
        f"> Content catalog. Every wiki page listed under its type with a one-line summary.",
        f"> Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')} | "
        f"Total entries: {len(entries)}",
        "",
        f"> **MCP Server:** `tree777://index` — use the tree777 MCP server for "
        f"programmatic access with `wiki_search` and `wiki_read` tools.",
        "",
    ]

    by_kind: dict[str, list] = {}
    for e in entries:
        by_kind.setdefault(e.kind, []).append(e)

    for kind in KIND_ORDER:
        if kind not in by_kind:
            continue
        kind_entries = sorted(by_kind[kind], key=lambda e: (e.category, e.slug))
        header = KIND_HEADERS.get(kind, kind.title())
        lines.append(f"## {header}")
        lines.append("")
        lines.append("| URI | Title | Category | Summary |")
        lines.append("|-----|-------|----------|---------|")
        for e in kind_entries:
            summary = e.summary[:80] if e.summary else ""
            lines.append(f"| `{e.uri}` | {e.title} | {e.category} | {summary} |")
        lines.append("")

    # Unclassified kinds
    for kind, kind_entries in sorted(by_kind.items()):
        if kind in KIND_ORDER:
            continue
        lines.append(f"## {kind.title()}")
        lines.append("")
        lines.append("| URI | Title | Summary |")
        lines.append("|-----|-------|---------|")
        for e in sorted(kind_entries, key=lambda e: e.slug):
            summary = e.summary[:80] if e.summary else ""
            lines.append(f"| `{e.uri}` | {e.title} | {summary} |")
        lines.append("")

    lines.append(f"_Generated: {now} UTC_")
    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"[TREE777] Scanning {WIKI_ROOT} ...")
    cache.refresh()
    entries = cache.entries
    print(f"[TREE777] Found {len(entries)} entries")

    # Generate index.md
    index_content = build_index_md()
    OUTPUT_INDEX.write_text(index_content)
    print(f"[TREE777] Regenerated {OUTPUT_INDEX}")

    # Generate tree-manifest.json (v2.0)
    manifest = build_manifest()
    OUTPUT_MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False)
    )
    print(f"[TREE777] Regenerated {OUTPUT_MANIFEST}")

    # Report
    print(f"[TREE777] Schema version: {manifest['schema_version']}")
    print(f"[TREE777] Totals by kind: {manifest['totals_by_kind']}")
    print(f"[TREE777] Categories: {len(manifest['categories'])}")
    if manifest["coverage_warning"]:
        print(f"[TREE777] Coverage warnings: {manifest['coverage_warning']}")


if __name__ == "__main__":
    main()
