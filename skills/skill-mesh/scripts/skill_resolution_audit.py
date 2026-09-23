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
            folder = os.path.basename(dirpath)
            f = os.path.join(dirpath, "SKILL.md")
            # ROUTING identity = frontmatter `name:`, folder only as fallback (rule 10).
            # Keying collisions on the folder basename produced false positives: two
            # different skills that merely live in a same-named dir (e.g. .../hermes/)
            # were reported as one unresolvable name.
            declared = frontmatter_name(f, folder)
            key = declared
            hits[key]["paths"].append(f)
            hits[key]["reals"].add(os.path.realpath(f))
            if declared != folder:
                mismatches.append((folder, declared, f))
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
        print(f"\nINFO  DIR-BASENAME vs frontmatter name MISMATCH: {len(mismatches)}"
              f"  (benign for routing — frontmatter `name:` is present, so the folder"
              f" is only the fallback)")
        for dirname, declared, f in sorted(mismatches):
            print(f"    dir '{dirname}' declares name '{declared}'  ({f})")
    if collisions:
        print("\nFIX: keep ONE physical copy reachable per name inside a scanned root. Delete"
              " the stray REAL copy; keep the symlink. Never rename the skill to match a"
              " typo'd directory - the name is the trigger the agent matches on. Then prove"
              " the repair with a real skill_view(name=...); a file count proves nothing.")
    if mismatches:
        print("\nNOTE (mismatch): the directory name is NOT the routing key when a frontmatter"
              " `name:` exists (frontmatter_name() falls back to the folder, so every reported"
              " mismatch proves one is present). Cosmetic only — do NOT mass-rename: a path"
              " dependency would break, and rule 16 requires a dependents sweep first.")
    # FAIL only on a name that cannot resolve. Cosmetic folder/name drift is INFO
    # (severity ladder rule 13) — conflating them under one exit code made a healthy
    # library report EXIT=1 and stopped the real signal from being read.
    return 1 if collisions else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", action="append", default=None)
    a = ap.parse_args()
    sys.exit(report(*scan(a.root or DEFAULT_ROOTS)))
