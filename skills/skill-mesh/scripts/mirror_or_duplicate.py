#!/usr/bin/env python3
"""mirror_or_duplicate.py - classify a skill-name collision: mirror drift, or two real owners?

WHY
  Sweep findings (profile_stale_mirror / name collisions) get summarised in receipts as
  "two live owners -> human merge decision". That label is frequently wrong, and the label
  decides the remedy:
      stale mirror        -> mechanical re-sync, the agent may do it
      duplicate owner     -> split sovereignty, a human judgement, never auto-merge
  Classify by PATH SHAPE and by hash, never by the wording of the report.

USAGE
  python3 mirror_or_duplicate.py                     # every colliding name, all roots
  python3 mirror_or_duplicate.py SKILL-A SKILL-B     # named skills only
  python3 mirror_or_duplicate.py --json              # machine form

VERDICTS
  IDENTICAL        all copies hash the same -> not a collision at all
  MIRROR_DRIFT     exactly one authored path + flat leftover(s) -> re-sync the flat copy
  DUPLICATE_OWNER  two or more authored paths, hashes differ -> HOLD for the human

READ-ONLY. It never creates, moves, renames or relinks anything.
Exit 1 when any DUPLICATE_OWNER is found (safe to gate on), else 0.
"""
import glob
import hashlib
import json
import os
import sys

ROOTS = [
    "/root/AAA/skills",
    "/root/.hermes/skills",
    "/root/.forge/skills",
]
ROOTS += sorted(glob.glob("/root/.hermes/profiles/*/skills"))

# Trees that are snapshots, not live views. Counting them manufactures collisions.
SKIP_MARKERS = ("skills-retired", "skills-deprecated", "skills-archive", ".archive",
                ".quarantine", "-snapshots", "backups", ".tmp", "__pycache__")


def declared_name(path):
    """Identity is the frontmatter name:, not the folder basename."""
    try:
        txt = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    head = txt.split("---", 2)[1] if txt.startswith("---") else txt[:400]
    for line in head.splitlines():
        s = line.strip()
        for key in ("name:", "id:"):
            if s.startswith(key):
                return s.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def sha_prefix(path, n=12):
    try:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()[:n]
    except OSError:
        return None


def shape(root, path):
    """flat = <root>/<name>/SKILL.md ; authored = at least one category level below that."""
    rel = os.path.relpath(path, root)
    parts = rel.split(os.sep)
    return "flat" if len(parts) <= 2 else "authored"


def collect():
    names = {}
    for root in ROOTS:
        for path in glob.glob(os.path.join(root, "**", "SKILL.md"), recursive=True):
            if any(m in path for m in SKIP_MARKERS):
                continue
            real = os.path.realpath(path)
            name = declared_name(path) or os.path.basename(os.path.dirname(path))
            names.setdefault(name, {})[real] = {
                "path": path, "real": real, "root": root, "shape": shape(root, path),
            }
    return names


def classify(name, copies):
    rows = [dict(v, sha=sha_prefix(v["real"])) for v in copies.values()]
    roots = {r["root"] for r in rows}
    authored = [r for r in rows if r["shape"] == "authored" and r["root"] == "/root/AAA/skills"]
    if not authored:  # live view tree only, no canonical writer involved
        authored = [r for r in rows if r["shape"] == "authored"]
    hashes = {r["sha"] for r in rows}
    if len(rows) < 2 or len(roots) < 2:
        verdict = "IDENTICAL" if len(hashes) == 1 else "SINGLE_ROOT_VARIANT"
    elif len(hashes) == 1:
        verdict = "IDENTICAL"
    elif len(authored) >= 2:
        verdict = "DUPLICATE_OWNER"
    else:
        verdict = "MIRROR_DRIFT"
    return verdict, sorted(rows, key=lambda r: (r["shape"], r["path"]))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    names = collect()
    out = {}
    for name, copies in sorted(names.items()):
        if args and name not in args:
            continue
        if len(copies) < 2 and not args:
            continue
        verdict, rows = classify(name, copies)
        out[name] = {"verdict": verdict,
                     "copies": [{"shape": r["shape"], "sha": r["sha"], "path": r["path"]} for r in rows]}
    if as_json:
        print(json.dumps(out, indent=2))
    else:
        for name, v in out.items():
            print(f"{v['verdict']:16s} {name}")
            for c in v["copies"]:
                print(f"    {c['shape']:9s} {c['sha']}  {c['path']}")
        tally = {}
        for v in out.values():
            tally[v["verdict"]] = tally.get(v["verdict"], 0) + 1
        print("\n" + "  ".join(f"{k}={v}" for k, v in sorted(tally.items())) or "no collisions")
    return 1 if any(v["verdict"] == "DUPLICATE_OWNER" for v in out.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
