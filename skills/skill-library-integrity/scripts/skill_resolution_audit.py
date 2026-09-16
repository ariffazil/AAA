#!/usr/bin/env python3
"""skill_resolution_audit — can every skill actually be LOADED?

A skill whose NAME maps to more than one DISTINCT file inside one scanned root is
unloadable: the loader refuses with "Ambiguous skill name", so the skill silently
disappears while still looking present on disk. Nothing in frontmatter linting can see it,
because the fault is on the filesystem. This script is the detector.

Copies that are the same physical file (symlink/hardlink/same realpath) are FINE and
expected — mirroring the organ skill store into a profile tree is the normal pattern.

Also flags a second class: a skill directory whose basename does not match its frontmatter
`name:` — a dir named after a different skill collides with that skill's own copy and
breaks resolution for BOTH names.

Usage:
    python3 skill_resolution_audit.py                 # audit default roots
    python3 skill_resolution_audit.py --root DIR ...  # audit specific roots
Exit code 1 when anything is unreachable, 0 otherwise.
"""

from __future__ import annotations

import argparse
import collections
import os
import re
import sys

DEFAULT_ROOTS = ["/root/.hermes/skills"]
NAME_RE = re.compile(r"^name:\s*(.+)$", re.M)


def frontmatter_name(skill_md: str, fallback: str) -> str:
    try:
        head = open(skill_md, encoding="utf-8", errors="ignore").read(4000)
    except OSError:
        return fallback
    if not head.startswith("---"):
        return fallback
    m = NAME_RE.search(head)
    if not m:
        return fallback
    return m.group(1).strip().strip('"').strip("'")


def scan(roots: list[str]) -> tuple[dict[str, dict], list[tuple[str, str, str]]]:
    hits: dict[str, dict] = collections.defaultdict(lambda: {"paths": [], "reals": set()})
    mismatches: list[tuple[str, str, str]] = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            # historical copies are deliberate: never descend into archive/backup trees
            dirnames[:] = [d for d in dirnames
                           if not d.startswith((".", "backup", "archive")) and "bak" not in d]
            if "SKILL.md" not in filenames:
                continue
            name = os.path.basename(dirpath)
            f = os.path.join(dirpath, "SKILL.md")
            hits[name]["paths"].append(f)
            hits[name]["reals"].add(os.path.realpath(f))
            declared = frontmatter_name(f, name)
            if declared != name:
                mismatches.append((name, declared, f))
    return hits, mismatches


def report(hits: dict[str, dict], mismatches: list[tuple[str, str, str]]) -> int:
    collisions = {n: h for n, h in hits.items() if len(h["reals"]) > 1}
    print(f"skills with a SKILL.md: {len(hits)}")
    print(f"UNRESOLVABLE (name -> >1 distinct file): {len(collisions)}")
    for name in sorted(collisions):
        print(f"\n  {name}")
        for p in sorted(collisions[name]["paths"]):
            print(f"    {p}")
    if mismatches:
        print(f"\nDIR-BASENAME vs frontmatter name MISMATCH: {len(mismatches)}")
        for dirname, declared, f in sorted(mismatches):
            print(f"    dir '{dirname}' declares name '{declared}'  ({f})")
    if collisions:
        print("\nFIX: keep ONE physical copy reachable per name inside a scanned root. Delete"
              " the stray REAL copy; keep the symlink. Never rename the skill to match a"
              " typo'd directory - the name is the trigger the agent matches on. Then prove"
              " the repair with a real skill_view(name=...); a file count proves nothing.")
    if mismatches:
        print("\nFIX (mismatch): rename the DIRECTORY to the declared name - the directory name"
              " is the index key, so a wrong dir name makes the skill unreachable under its"
              " declared name and collides with the skill it is named after.")
    return 1 if (collisions or mismatches) else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", action="append", default=None)
    a = ap.parse_args()
    sys.exit(report(*scan(a.root or DEFAULT_ROOTS)))
