#!/usr/bin/env python3
"""Inbound dependents of a directory — the pre-move check that must run before ANY eviction.

WHY THIS EXISTS (and why you cannot do it with find)
  The natural-looking one-liner is WRONG:

      find -L <roots> -type l | ...        # reports zero for a directory with dozens of dependents

  `-L` makes find FOLLOW symlinks, so a link pointing at a directory is reported as a directory and
  `-type l` matches only links whose target is already unreachable. Run against a live directory it
  returns nothing, which reads as "no dependents" — the answer that is wrong exactly when the probe
  matters. Measured: three live directories were declared dependent-free and archived; 100 view
  symlinks broke.

  Walk WITHOUT following, test islink explicitly, resolve with realpath.

USAGE
  python3 dependents.py <dir> [<dir> ...]
  Read-only, exits 0. A count of 0 for a directory you KNOW has dependents means the probe is broken,
  not that the directory is free.
"""
from __future__ import annotations

import os
import sys

ROOTS = [
    "/root/AAA/skills",
    "/root/.hermes/skills",
    "/root/.hermes/profiles/aaa-hermes/skills",
    "/root/.hermes/profiles/hermes_asi/skills",
    "/root/.hermes/profiles/hermes_apex/skills",
    "/root/.hermes/profiles/hermes_forge/skills",
    "/root/.hermes/profiles/nabilah/skills",
]


def dependents(target: str) -> list[tuple[str, str]]:
    """Every symlink under any known root that resolves into `target`."""
    t = os.path.realpath(target)
    hits: list[tuple[str, str]] = []
    for root in ROOTS:
        if not os.path.isdir(root):
            continue
        for dp, dn, fn in os.walk(root, followlinks=False):   # NOT followlinks=True
            if ".git" in dp:
                continue
            for name in list(dn) + list(fn):
                p = os.path.join(dp, name)
                if not os.path.islink(p):
                    continue
                try:
                    rp = os.path.realpath(p)
                except OSError:
                    continue
                if rp == t or rp.startswith(t + os.sep):
                    hits.append((p, rp))
    return hits


def main(argv: list[str]) -> int:
    targets = argv[1:] or ["/root/AAA/skills/core"]
    for target in targets:
        hits = dependents(target)
        print(f"{target}\n  inbound dependents: {len(hits)}")
        for p, rp in hits[:10]:
            print(f"    {p.replace('/root/', '')}  ->  {rp.replace('/root/', '')}")
        if len(hits) > 10:
            print(f"    ... {len(hits) - 10} more")
        if not hits:
            print("    (none -- verify the probe against a directory you KNOW has dependents")
            print("     before trusting a zero: a predicate that can only return zero is not a check)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
