#!/usr/bin/env python3
"""
ORTHOGONAL DISCOVERY LAYER — SKILLS INDEX GENERATOR (Opsi-B)
=============================================================
Build step: crawl /root/AAA/skills for SKILL.md files and emit
/root/AAA/skills_index.json — a bridge so TREE777 can resolve
tree777://skills/{category}/{name} without mutating tree777.py
or the AAA/skills topology.

F1 constraints:
  - READ-ONLY: never writes to AAA/skills, never deletes.
  - Deterministic output (sorted, stable JSON).
  - No LLM in the gate.
  - Fails safely on permission errors (skip + warn, not crash).

Category inference: the skill's directory IS the category (AAA/skills/{name}/SKILL.md
is flat by default); if a skill dir itself contains a `category:` frontmatter field
we honour it, else we bucket by its top-level dir name. Because AAA/skills is flat
({skill_name}/SKILL.md), category defaults to the owning top-level subdir OR "general".

Federation mode (v1.1.0):
  python3 skills_index_gen.py --federation [--out /root/AAA/skills_index.json]
    crawls all five federation roots (order = dedupe precedence, AAA is
    canonical), dedupes by normalized skill name, and emits a merged index
    with `root: "<federation:5-organs>"` and per-skill `source_organ`.

Usage:
  python3 skills_index_gen.py [--out /root/AAA/skills_index.json] [--dry-run]
                             [--root PATH] [--federation]

DITEMPA BUKAN DIBERI.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

DEFAULT_SKILLS_ROOT = Path("/root/AAA/skills")
DEFAULT_OUT = Path("/root/AAA/skills_index.json")

# ── federation roots (order = dedupe precedence; AAA is canonical) ────
FEDERATION_ROOTS: list[tuple[str, Path]] = [
    ("AAA", Path("/root/AAA/skills")),
    ("arifOS", Path("/root/arifOS/skills")),
    ("HERMES", Path("/root/HERMES/skills")),
    ("A-FORGE", Path("/root/A-FORGE/skills")),
    ("kimi-code", Path("/root/.kimi-code/skills")),
]
FEDERATION_ROOT_LABEL = "<federation:5-organs>"
FEDERATION_SCHEMA_VERSION = "1.1.0-federation"

# ── frontmatter extraction ─────────────────────────────────────────────
_FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    """Best-effort frontmatter parse. Never throws. Empty dict on no YAML."""
    m = _FM_RE.match(text)
    if not m:
        return {}
    data: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("-"):
            k, _, v = line.partition(":")
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def infer_category(meta: dict, skill_dir: Path) -> str:
    """Category = explicit frontmatter `category:` else infer from name prefix
    (AGI-/FORGE-/APEX-/ASI-/AUDIT-/...) else 'general'."""
    if meta.get("category"):
        return meta["category"].strip().lower()
    name = meta.get("name") or skill_dir.name
    if "-" in name:
        prefix = name.split("-", 1)[0].strip().lower()
        if prefix and len(prefix) <= 12:  # avoid long doc-titles as categories
            return prefix
    return "general"


def _crawl_root(organ: str, root: Path) -> tuple[list[dict], list[str]]:
    """Crawl one organ root for SKILL.md files.

    READ-ONLY. Full recursive walk (rglob) so nested skill trees
    (HERMES, kimi-code, deep AAA categories) are all seen; `_retired`
    subtrees are excluded. Fails safely on permission errors (skip +
    warn, not crash). Returns (skills_list, errors_list); every kept
    entry carries `source_organ`.
    """
    skills: list[dict] = []
    errors: list[str] = []
    for sk_file in sorted(root.rglob("SKILL.md")):
        if "_retired" in sk_file.parts:
            continue
        skill_dir = sk_file.parent
        try:
            text = sk_file.read_text(encoding="utf-8", errors="replace")
        except (PermissionError, OSError) as e:
            errors.append(f"{skill_dir.name}: {e}")
            continue
        meta = parse_frontmatter(text)
        name = meta.get("name") or skill_dir.name
        skills.append(
            {
                "name": name,
                "category": infer_category(meta, skill_dir),
                "path": str(sk_file),
                "dir": str(skill_dir),
                "frontmatter": meta,
                "has_sk": True,
                "source_organ": organ,
            }
        )
    return skills, errors


def build_index(root: Path) -> dict:
    """Single-root index (backward compat — AAA-only behavior preserved)."""
    t0 = time.time()
    skills, errors = _crawl_root("AAA", root)

    index = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "root": str(root),
        "schema_version": "1.0.0-orthogonal-discovery",
        "count": len(skills),
        "elapsed_ms": int((time.time() - t0) * 1000),
        "errors": errors,
        "skills": skills,
    }
    return index


def build_federation_index(roots: list[tuple[str, Path]]) -> dict:
    """Crawl all federation roots and merge into one deduped index.

    Dedupe key: normalized skill name (lowercased, stripped). The first
    organ in `roots` priority order that claims a name is canonical
    (AAA > arifOS > HERMES > A-FORGE > kimi-code); later duplicates are
    skipped. Every kept entry carries `source_organ`.
    """
    t0 = time.time()
    seen: dict[str, dict] = {}
    errors: list[str] = []
    organ_counts: dict[str, int] = {organ: 0 for organ, _ in roots}
    duplicates = 0

    for organ, root in roots:
        if not root.is_dir():
            errors.append(f"{organ}: skills root not found: {root}")
            continue
        root_skills, root_errors = _crawl_root(organ, root)
        errors.extend(f"{organ}: {e}" for e in root_errors)
        for skill in root_skills:
            key = skill["name"].strip().lower()
            if key in seen:
                duplicates += 1
                continue  # first organ in priority order is canonical
            seen[key] = skill
            organ_counts[organ] = organ_counts.get(organ, 0) + 1

    skills = list(seen.values())
    index = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "root": FEDERATION_ROOT_LABEL,
        "schema_version": FEDERATION_SCHEMA_VERSION,
        "count": len(skills),
        "duplicates_skipped": duplicates,
        "organ_counts": organ_counts,
        "elapsed_ms": int((time.time() - t0) * 1000),
        "errors": errors,
        "skills": skills,
    }
    return index


def main() -> int:
    ap = argparse.ArgumentParser(description="Skills index generator (Opsi-B bridge)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--root", type=Path, default=DEFAULT_SKILLS_ROOT,
                    help="single-root mode (backward compat); ignored with --federation")
    ap.add_argument("--federation", action="store_true",
                    help="crawl all 5 federation roots, dedupe (AAA canonical), merged index")
    ap.add_argument("--dry-run", action="store_true", help="print summary, don't write")
    args = ap.parse_args()

    if args.federation:
        index = build_federation_index(FEDERATION_ROOTS)
    else:
        if not args.root.is_dir():
            print(f"ERROR: skills root not found: {args.root}", file=sys.stderr)
            return 1
        index = build_index(args.root)

    if args.dry_run:
        print(
            f"DRY-RUN: {index['count']} skills | {len(index['errors'])} errors "
            f"| {index['elapsed_ms']}ms"
        )
        for c in sorted({s["category"] for s in index["skills"]}):
            cnt = sum(1 for s in index["skills"] if s["category"] == c)
            print(f"  [{c}] {cnt}")
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.out.with_suffix(".tmp")
    tmp.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(args.out)  # atomic
    print(f"[ACT] skills index written: {args.out}")
    print(f"      skills={index['count']} errors={len(index['errors'])} elapsed={index['elapsed_ms']}ms")
    if args.federation:
        print(f"      duplicates_skipped={index.get('duplicates_skipped', 0)} "
              f"organ_counts={json.dumps(index.get('organ_counts', {}), sort_keys=True)}")
    for e in index["errors"][:10]:
        print(f"  ⚠ {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())