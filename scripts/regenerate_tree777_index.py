#!/usr/bin/env python3
"""
regenerate_tree777_index.py
Regenerates AAA/wiki/index.md and tree-manifest.json from actual filesystem.
DITEMPA BUKAN DIBERI — Forged, not given.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

WIKI_ROOT = Path("/root/AAA/wiki")
OUTPUT_INDEX = WIKI_ROOT / "index.md"
OUTPUT_MANIFEST = WIKI_ROOT / "tree-manifest.json"

# ── Frontmatter parser (YAML-aware) ───────────────────────────────────────────

FRONT_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

def parse_frontmatter(text: str) -> dict[str, Any]:
    """Extract YAML frontmatter from a markdown file using PyYAML."""
    m = FRONT_RE.match(text)
    if not m:
        return {}
    try:
        fm = yaml.safe_load(m.group(1))
        if not isinstance(fm, dict):
            return {}
        return fm
    except yaml.YAMLError:
        return {}

def infer_type_from_path(rel: Path) -> str:
    """Infer page type from path when frontmatter type is missing/unknown."""
    parts = rel.parts
    stem = rel.stem.lower()

    # Root-level special documents (key = filename without .md)
    root_special = {
        "AGENT_IDENTITY_MATRIX": "entity",
        "MEMORY_EUREKA_DOSSIER": "concept",
        "arif-fazil-metabolized": "entity",
        "hermes-arifos-integration-spec": "concept",
        "post-task-update-prompt-contract": "skill",
        "arif-fazil-complete-map": "entity",
    }
    stem = rel.stem  # filename without extension
    if stem in root_special:
        return root_special[stem]

    # Directory-based inference
    if any(p.startswith("axiom") for p in parts):
        return "axiom"
    if any(p.startswith("concept") for p in parts):
        return "concept"
    if any(p.startswith("skill") for p in parts):
        return "skill"
    if any(p.startswith("workflow") for p in parts):
        return "workflow"
    if any(p.startswith("entity") for p in parts):
        return "entity"
    if any(p.startswith("scar") for p in parts):
        return "scar"
    if any(p.startswith("raw") for p in parts):
        return "raw"
    if any(p.startswith("playbook") for p in parts):
        return "workflow"
    if "log" == stem:
        return "log"
    if "schema" == stem:
        return "schema"
    if "index" == stem:
        return "index"

    # Filename-based inference
    if stem.startswith("skill-"):
        return "skill"
    if stem.startswith("scar-") or "-scar-" in stem:
        return "scar"
    if stem.startswith("concept-"):
        return "concept"
    if stem.startswith("workflow-"):
        return "workflow"
    if stem.startswith("axiom-"):
        return "axiom"
    if stem.startswith("entity-"):
        return "entity"

    return "unknown"

# ── File scanner ──────────────────────────────────────────────────────────────

def scan_wiki(root: Path) -> list[dict[str, Any]]:
    """Return list of page dicts for every .md file under root."""
    pages = []
    for md in sorted(root.rglob("*.md")):
        # Skip backups, _runtime cache, generated script
        skip_dirs = {"_runtime", "backups", ".git"}
        if any(s in md.parts for s in skip_dirs):
            continue
        rel = md.relative_to(root)
        slug = str(rel.with_suffix("")).replace("/", ".")
        text = md.read_text(errors="ignore")
        fm = parse_frontmatter(text)

        # Title: frontmatter title, else first H1 in body, else slug
        title = str(fm.get("title", "")) if fm.get("title") else ""
        if not title:
            h1 = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
            if h1:
                title = h1.group(1).strip()
            else:
                title = rel.stem.replace("-", " ").replace("_", " ").title()

        # Type: frontmatter type, else infer from path
        page_type = fm.get("type", "")
        if not page_type or page_type == "unknown":
            page_type = infer_type_from_path(rel)

        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip().strip('"').strip("'") for t in tags.split(",")]
        elif not isinstance(tags, list):
            tags = []

        confidence = str(fm.get("confidence", "medium"))
        updated_raw = fm.get("updated")
        updated = str(updated_raw) if updated_raw else datetime.fromtimestamp(md.stat().st_mtime).strftime("%Y-%m-%d")
        created_raw = fm.get("created")
        created = str(created_raw) if created_raw else "2026-05-17"
        summary = _extract_summary(text, fm)

        pages.append({
            "slug": slug,
            "path": str(rel),
            "title": title,
            "type": page_type,
            "tags": tags,
            "confidence": confidence,
            "updated": updated,
            "created": created,
            "summary": summary,
            "word_count": len(text.split()),
        })
    return pages

def _extract_summary(text: str, fm: dict) -> str:
    """Extract first meaningful paragraph as summary.
    Strategy:
    1. Look for first H2 heading (## heading) as primary summary
    2. Otherwise use first non-blank, non-H1, non-YAML, non-quote line > 20 chars
    """
    body = FRONT_RE.split(text)
    if len(body) < 2:
        return ""
    lines = body[1].splitlines()
    h2_lines = []  # collect H2 lines

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Collect H2 headings for later
        if line.startswith("## "):
            h2_lines.append(line[3:].strip())
            continue
        # Skip H1 headings
        if line.startswith("# "):
            continue
        # Skip blockquotes
        if line.startswith(">"):
            continue
        # Skip lines that look like YAML key-value at the start
        # Pattern: word characters, optional spaces, then colon (with or without value)
        if re.match(r"^[\w\-]+(\s*\([^)]*\))?\s*:", line):
            continue
        if len(line) > 20:
            return line[:140]

    # Fallback: use first H2 if available
    if h2_lines:
        return h2_lines[0][:140]
    return ""

# ── index.md generator ───────────────────────────────────────────────────────

TYPE_ORDER = ["schema", "index", "axiom", "concept", "skill", "workflow", "entity", "scar", "raw", "log", "canon", "governance", "human-map", "scar-terrain", "unknown"]

SECTION_HEADERS = {
    "schema": "Schemas",
    "index": "Indexes",
    "axiom": "Axioms — Dimension 0: Foundational Invariants",
    "concept": "Concepts",
    "skill": "Skills — Reusable Capability Documents",
    "workflow": "Workflows",
    "entity": "Entities",
    "scar": "Scars — Lessons Sealed as Doctrine",
    "raw": "Raw Sources — Immutable Input Material",
    "log": "Logs",
    "canon": "Canonical Records",
    "governance": "Governance Documents",
    "human-map": "Human Maps",
    "scar-terrain": "Terrain Scars",
    "unknown": "Unclassified",
}

def build_index(pages: list[dict]) -> str:
    lines = [
        "---",
        "title: AAA Wiki Index",
        f"created: 2026-05-17",
        f"updated: {datetime.now().strftime('%Y-%m-%d')}",
        "type: index",
        "tags: [federation, wiki, index]",
        "confidence: high",
        "---",
        "",
        "# AAA Wiki — Federation Knowledge Base Index",
        "",
        f"> Content catalog. Every wiki page listed under its type with a one-line summary.",
        f"> Last updated: {datetime.now().strftime('%Y-%m-%d')} | Total markdown pages: {len(pages)}",
        "",
    ]

    by_type: dict[str, list[dict]] = {}
    for p in pages:
        by_type.setdefault(p["type"], []).append(p)

    for ptype in TYPE_ORDER:
        if ptype not in by_type:
            continue
        entries = by_type[ptype]
        header = SECTION_HEADERS.get(ptype, ptype.title() + "s")
        lines.append("")
        lines.append(f"## {header}")
        lines.append("")

        if ptype == "axiom":
            lines.append("| # | Axiom | File | Role |")
            lines.append("|---|-------|------|------|")
            for i, p in enumerate(entries, 1):
                role = p.get("summary", "")[:80]
                lines.append(f"| {i} | **{p['title']}** | [[{p['slug']}]] | {role} |")
        elif ptype == "skill":
            lines.append("| Page | Confidence | Summary |")
            lines.append("|------|------------|---------|")
            for p in entries:
                conf = p.get("confidence", "medium").upper()
                summary = p.get("summary", "")[:80]
                lines.append(f"| [[{p['slug']}]] | {conf} | {summary} |")
        elif ptype == "concept":
            lines.append("| Page | Confidence | Summary |")
            lines.append("|------|------------|---------|")
            for p in entries:
                conf = p.get("confidence", "medium").upper()
                summary = p.get("summary", "")[:80]
                lines.append(f"| [[{p['slug']}]] | {conf} | {summary} |")
        elif ptype == "scar":
            lines.append("| Scar | Date | Summary |")
            lines.append("|------|------|---------|")
            for p in entries:
                date = p.get("created", "")
                summary = p.get("summary", "")[:80]
                lines.append(f"| [[{p['slug']}]] | {date} | {summary} |")
        elif ptype == "workflow":
            lines.append("| Workflow | Updated | Summary |")
            lines.append("|----------|---------|---------|")
            for p in entries:
                updated = p.get("updated", "")
                summary = p.get("summary", "")[:80]
                lines.append(f"| [[{p['slug']}]] | {updated} | {summary} |")
        else:
            lines.append("| Page | Updated | Summary |")
            lines.append("|------|---------|---------|")
            for p in entries:
                updated = p.get("updated", "")
                summary = p.get("summary", "")[:80]
                lines.append(f"| [[{p['slug']}]] | {updated} | {summary} |")

    lines.append("")
    lines.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")
    return "\n".join(lines)

# ── tree-manifest.json generator ──────────────────────────────────────────────

def build_manifest(pages: list[dict]) -> str:
    manifest = {
        "schema_version": "1.1",
        "generated": datetime.now().isoformat(),
        "total_pages": len(pages),
        "pages": {},
    }
    for p in pages:
        manifest["pages"][p["slug"]] = {
            "path": p["path"],
            "title": p["title"],
            "type": p["type"],
            "tags": p["tags"],
            "confidence": p["confidence"],
            "updated": p["updated"],
            "created": p["created"],
            "word_count": p["word_count"],
            "update_class": _update_class(p),
        }
    return json.dumps(manifest, indent=2, ensure_ascii=False)

def _update_class(p: dict) -> str:
    """Classify update urgency based on type and metadata."""
    t = p["type"]
    c = p.get("confidence", "medium")
    if t in ("schema", "axiom", "index"):
        return "CRITICAL"
    if t == "skill" and c == "high":
        return "HIGH"
    if t == "scar":
        return "HIGH"
    updated_val = p.get("updated", "")
    if isinstance(updated_val, str) and updated_val < "2026-06-01":
        return "STALE"
    return "NORMAL"

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"[TREE777] Scanning {WIKI_ROOT} ...")
    pages = scan_wiki(WIKI_ROOT)
    print(f"[TREE777] Found {len(pages)} pages")

    index_content = build_index(pages)
    OUTPUT_INDEX.write_text(index_content)
    print(f"[TREE777] Regenerated {OUTPUT_INDEX}")

    manifest_content = build_manifest(pages)
    OUTPUT_MANIFEST.write_text(manifest_content)
    print(f"[TREE777] Regenerated {OUTPUT_MANIFEST}")

    # Report by type
    by_type: dict[str, int] = {}
    for p in pages:
        by_type[p["type"]] = by_type.get(p["type"], 0) + 1
    print("[TREE777] Pages by type:")
    for t, c in sorted(by_type.items()):
        print(f"  {t}: {c}")

    unknown = [p for p in pages if p["type"] == "unknown"]
    if unknown:
        print(f"[TREE777] Unknown types ({len(unknown)}):")
        for p in unknown[:5]:
            print(f"  {p['slug']} -> {p['path']}")

if __name__ == "__main__":
    main()
