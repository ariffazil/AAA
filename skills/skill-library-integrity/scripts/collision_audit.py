#!/usr/bin/env python3
"""Routing-name collision audit for a skill store. Read-only.

WHY THIS EXISTS
  A loader indexes skills by the frontmatter `name:` (falling back to the folder basename) and dedupes
  FIRST-WINS: the first body under a name wins and every later body is skipped silently. Two different
  bodies sharing one routing name therefore means at least one capability is on disk and can never load
  — no error anywhere, so nothing reports it.

WHAT IT SEPARATES (this is the whole point)
  Most same-name groups are NOT defects: they are one body reached by several addresses (the intended
  view tree of bands over a single body). Only groups whose BODIES DIFFER are real collisions. The
  naive count "groups sharing a name" overstates the defect by an order of magnitude; this script
  prints the split so the report cannot be inflated.

USAGE
  python3 collision_audit.py [store_root]        # default: /root/AAA/skills
  python3 collision_audit.py --strict            # exit 1 when a real collision exists

Also flags canonical addresses that resolve OUTSIDE the store root (a borrowed body: the store public
what it does not hold).
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
import collections
import glob

DEFAULT_ROOT = "/root/AAA/skills"
SKIP = {"node_modules", "__pycache__", ".git", ".venv", "site-packages"}
NAME_RE = re.compile(r"^name:\s*(.+)$", re.M)


def body_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()[:12]


def routing_name(text: str, folder: str) -> str:
    if text.startswith("---"):
        head = text.split("---", 2)[1]
        m = NAME_RE.search(head)
        if m:
            return m.group(1).strip().strip("\"'") or folder
    return folder


def collect(root: str):
    groups = collections.defaultdict(list)
    for dp, dn, fn in os.walk(root, followlinks=True):
        dn[:] = [d for d in dn if not d.startswith(".") and d not in SKIP]
        if "SKILL.md" not in fn:
            continue
        p = os.path.join(dp, "SKILL.md")
        try:
            text = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        groups[routing_name(text, os.path.basename(dp))].append(
            (os.path.relpath(dp, root), body_hash(p))
        )
    return groups


def outside_root(store: str):
    """Addresses that exist in the store's namespace but resolve to another tree."""
    real_store = os.path.realpath(store)
    out = []
    for dp, dn, fn in os.walk(store, followlinks=True):
        for name in list(dn) + list(fn):
            p = os.path.join(dp, name)
            if os.path.islink(p) and os.path.exists(p):
                r = os.path.realpath(p)
                if not r.startswith(real_store + os.sep):
                    out.append((os.path.relpath(p, store), r))
    return out


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    args = [a for a in argv[1:] if not a.startswith("--")]
    store = args[0] if args else DEFAULT_ROOT
    if not os.path.isdir(store):
        print(f"no such store: {store}")
        return 2

    groups = collect(store)
    shared = {k: v for k, v in groups.items() if len(v) > 1}
    bands = {k: v for k, v in shared.items() if len({s for _, s in v}) == 1}
    collide = {k: v for k, v in shared.items() if len({s for _, s in v}) > 1}

    print(f"store: {store}")
    print(f"  skills indexed                 : {sum(len(v) for v in groups.values())}")
    print(f"  distinct routing names         : {len(groups)}")
    print(f"  same-name groups (raw count)   : {len(shared)}")
    print(f"    of which ADDRESS BANDS       : {len(bands)}   <- one body, several "
          "addresses; working as designed, do NOT touch")
    print(f"    of which REAL COLLISIONS     : {len(collide)}   <- bodies differ; the rest cannot load")

    if bands:
        print("\nADDRESS BANDS (informational — no action)")
        for k in sorted(bands):
            print(f"  [{k}] {len(bands[k])} addresses, body {bands[k][0][1]}")

    if collide:
        print("\nREAL COLLISIONS — bodies that can never load")
        for k in sorted(collide):
            print(f"  [{k}]  {len(collide[k])} different bodies")
            for rel, sha in sorted(collide[k], key=lambda x: x[1]):
                print(f"      {sha}  {rel}")

    borrowed = outside_root(store)
    if borrowed:
        print("\nBORROWED ADDRESSES — resolve outside the store root")
        for rel, target in borrowed[:40]:
            print(f"  {rel}\n      -> {target}")
        if len(borrowed) > 40:
            print(f"  ... +{len(borrowed) - 40} more")

    print(f"\nVERDICT: {len(collide)} real collision(s), {len(borrowed)} borrowed address(es)")
    return 1 if (strict and (collide or borrowed)) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
