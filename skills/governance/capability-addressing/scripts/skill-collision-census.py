#!/usr/bin/env python3
"""skill-collision-census.py — deterministic capability collision census.

Separates two defects that have OPPOSITE fixes and are routinely reported as one number:

  IDENTITY collision  one concept, >=2 distinct realpaths   -> canonicalize/supersede/alias
  TRIGGER  collision  different capabilities, one request   -> disambiguate owners

Declared metadata only: no embeddings, no LLM. Symlinks are DEREFERENCED
(os.walk(followlinks=True)) because a probe that reads the symlink measures the map.

Usage:
  python3 skill-collision-census.py
  python3 skill-collision-census.py --root canonical=/path/a --root overlay=/path/b
  python3 skill-collision-census.py --min-shared 4 --out /tmp/census.json
  python3 skill-collision-census.py --json
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys

DEFAULT_SURFACES = [
    ("AAA", "/root/AAA/skills"),
    ("hermes", "/root/.hermes/skills"),
    ("opencode_overlay", "/root/.config/opencode/skills"),
    ("qwen", "/root/.qwen/skills"),
    ("kimi", "/root/.kimi-code/skills"),
    ("gemini", "/root/.gemini/skills"),
]

MAX_DEPTH = 6

# Routing metadata that may prefix a description. Tokenizing it as trigger text
# collapses every tagged skill into one phantom cluster.
META_PREFIX = re.compile(r"^\s*>?\s*\[[^\]]*\]\s*")

STOP = set(
    "use when the a an of for to in on with and or is are this that every any all its it "
    "skill load before after into from as at by not no you your we our".split()
)

FRONT = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def walk_skills(root: str) -> list:
    """Every SKILL.md under root, SYMLINKS DEREFERENCED."""
    out = []
    if not os.path.isdir(root):
        return out
    base = root.rstrip(os.sep)
    for dirpath, dirnames, filenames in os.walk(base, followlinks=True):
        if "SKILL.md" in filenames:
            out.append(os.path.join(dirpath, "SKILL.md"))
        if dirpath.count(os.sep) - base.count(os.sep) > MAX_DEPTH:
            dirnames[:] = []
    return out


def parse(path: str):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            txt = fh.read(30000)
    except OSError:
        return None
    m = FRONT.match(txt)
    front = m.group(1) if m else ""
    nm = re.search(r"^name:\s*(.+)$", front, re.M)
    name = nm.group(1).strip().strip("\"'") if nm else None
    dm = re.search(r"^description:\s*(.+?)(?=\n[a-zA-Z_]+:|\Z)", front, re.S | re.M)
    desc = " ".join(dm.group(1).split()).strip().strip("\"'") if dm else ""
    if not name:
        h = re.search(r"^#\s+(.+)$", txt, re.M)
        name = h.group(1).strip() if h else os.path.basename(os.path.dirname(path))
    d = os.path.dirname(path)
    return {
        "name": name,
        "dir": os.path.basename(d),
        "desc": desc,
        "path": path,
        "real": os.path.realpath(d),
    }


def clean(desc: str) -> str:
    """Strip leading bracket metadata (e.g. '> [fed: tier=.. floors=[..]]')."""
    prev = None
    while prev != desc:
        prev = desc
        desc = META_PREFIX.sub("", desc).strip()
    return desc


def triggers(name: str, desc: str, limit: int = 8) -> list:
    d = clean(desc).lower()
    if not d or d == name.lower():
        return []
    m = re.search(r"use when ([^.]{4,300})", d)
    seg = m.group(1) if m else d[:200]
    seg = re.sub(r"[^a-z0-9\s\-]", " ", seg)
    return [t for t in seg.split() if t not in STOP and len(t) > 2][:limit]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--root", action="append", default=[], metavar="NAME=PATH",
        help="surface to scan (repeatable). Default: the standard estate surfaces.",
    )
    ap.add_argument(
        "--min-shared", type=int, default=3,
        help="shared leading trigger tokens before two skills count as colliding (default 3)",
    )
    ap.add_argument("--limit", type=int, default=15, help="clusters shown in the summary")
    ap.add_argument("--out", help="write the full JSON here")
    ap.add_argument("--json", action="store_true", help="print JSON only, no summary")
    args = ap.parse_args(argv)

    surfaces = []
    for spec in args.root:
        if "=" not in spec:
            print("ERROR --root expects NAME=PATH, got %r" % spec, file=sys.stderr)
            return 2
        n, p = spec.split("=", 1)
        surfaces.append((n, p))
    if not surfaces:
        surfaces = DEFAULT_SURFACES

    recs = collections.defaultdict(list)
    per_surface = {}
    for surf, root in surfaces:
        files = walk_skills(root)
        per_surface[surf] = len(files)
        for p in files:
            r = parse(p)
            if r:
                r["surface"] = surf
                recs[r["name"].lower()].append(r)

    # IDENTITY collision: one lowercased name resolving to >=2 distinct realpaths.
    identity = {
        k: sorted({x["real"] for x in v})
        for k, v in recs.items()
        if len({x["real"] for x in v}) > 1
    }

    # Case-only twins (same directory name, different casing, different realpath).
    bydir = collections.defaultdict(set)
    for v in recs.values():
        for x in v:
            bydir[x["dir"]].add(x["real"])
    lower = collections.defaultdict(set)
    for d in bydir:
        lower[d.lower()].add(d)
    case_twins = {n: sorted(dirs) for n, dirs in lower.items() if len(dirs) > 1}

    # TRIGGER collision: >= min_shared leading trigger tokens in common.
    tok_idx = collections.defaultdict(set)
    for k, v in recs.items():
        for t in triggers(k, v[0]["desc"]):
            tok_idx[t].add(k)

    collide = {}
    for k, v in recs.items():
        hits = collections.Counter()
        for t in triggers(k, v[0]["desc"]):
            for other in tok_idx[t]:
                if other != k:
                    hits[other] += 1
        rivals = sorted(o for o, c in hits.items() if c >= args.min_shared)
        if rivals:
            collide[k] = rivals

    blob = {
        "per_surface_files": per_surface,
        "file_total": sum(per_surface.values()),
        "distinct_names": len(recs),
        "identity_collisions": len(identity),
        "case_twins": len(case_twins),
        "trigger_collision_skills": len(collide),
        "trigger_collision_pct": round(100 * len(collide) / max(1, len(recs)), 1),
        "identity": identity,
        "case_twins_map": case_twins,
        "collisions": collide,
    }

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(blob, fh, indent=1)

    if args.json:
        print(json.dumps(blob, indent=1))
        return 0

    print(json.dumps(
        {k: v for k, v in blob.items()
         if k not in ("identity", "case_twins_map", "collisions")},
        indent=1,
    ))

    print("\n-- identity collisions (same name, different realpath) --")
    for k, paths in list(identity.items())[: args.limit]:
        short = [p.split(os.sep + "skills" + os.sep)[-1] for p in paths]
        print("   %-40s -> %d paths  %s" % (k, len(paths), short[:3]))
    print("   (total %d; case-only twins %d)" % (len(identity), len(case_twins)))

    print("\n-- trigger collisions (>=%d shared leading tokens) --" % args.min_shared)
    for k, rivals in sorted(collide.items(), key=lambda kv: -len(kv[1]))[: args.limit]:
        shown = ", ".join(rivals[:3]) + (" ..." if len(rivals) > 3 else "")
        print("   %-40s <-> %s" % (k, shown))
    print("   (total %d of %d distinct names)" % (len(collide), len(recs)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
