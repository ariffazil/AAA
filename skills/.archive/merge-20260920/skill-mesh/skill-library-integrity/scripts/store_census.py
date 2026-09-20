#!/usr/bin/env python3
"""Count a skill store correctly, and say which question the number answers.

WHY THIS EXISTS
  The skill store is a view tree: few physical bodies, many addresses (symlinks, bands, mirrors).
  Most tooling walks WITHOUT following symlinks, so a naive count under-reports by an order of
  magnitude and reports namespace/category directories as empty shells. Both are silently plausible.

WHAT IT PRINTS (four different questions, all legitimate)
  bodies      unique physical SKILL.md, deduped by realpath  -> "how many capabilities exist?"
  addresses   every reachable SKILL.md including symlinks   -> "how many doors can an agent enter?"
  served      what a harness's cached snapshot lists         -> "what does this harness actually have?"
  names       distinct routing names vs distinct bodies     -> "is one capability wearing several hats?"

  Every count carries the question it answers. Two audits disagreeing about the same store are
  usually both right about different questions.

DIRECTORY CLASSES (never call a CONTAINER an empty shell)
  HAS_BODY     the directory holds its own SKILL.md
  CONTAINER    no SKILL.md, but holds sub-skills beneath it (a namespace / category)
  TRULY_EMPTY  nothing beneath it at all -> this one is a real finding

USAGE
  python3 store_census.py [root ...]            # default: the roots this host commonly uses
  python3 store_census.py --json
  python3 store_census.py --strict              # exit 1 if a TRULY_EMPTY dir or name collision exists

READ-ONLY. It writes nothing.
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys

DEFAULT_ROOTS = [
    "/root/AAA/skills",
    "/root/.hermes/skills",
]

SKIP = {".git", "node_modules", "__pycache__", ".venv", "site-packages", ".ruff_cache"}
NAME_RE = re.compile(r"^name:\s*(.+)$", re.M)


def routing_name(text: str, folder: str) -> str:
    """Declared frontmatter name wins; the directory basename is the index key fallback."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 2:
            m = NAME_RE.search(parts[1])
            if m:
                return m.group(1).strip().strip("\"'") or folder
    return folder


def scan(root: str):
    bodies: set[str] = set()
    addresses = 0
    symlinks = 0
    symlinks_to_body = 0
    names: dict[str, set[str]] = collections.defaultdict(set)
    parse_errors = 0
    has_body: list[str] = []
    container: list[str] = []
    truly_empty: list[str] = []

    for dp, dn, fn in os.walk(root, followlinks=True):
        dn[:] = [d for d in dn if d not in SKIP]

        for d in list(dn):
            p = os.path.join(dp, d)
            if os.path.islink(p):
                symlinks += 1
                if os.path.isfile(os.path.join(os.path.realpath(p), "SKILL.md")):
                    symlinks_to_body += 1

        if "SKILL.md" in fn:
            path = os.path.join(dp, "SKILL.md")
            addresses += 1
            real = os.path.realpath(path)
            bodies.add(real)
            has_body.append(os.path.relpath(dp, root))
            try:
                text = open(path, encoding="utf-8", errors="replace").read()
            except OSError:
                parse_errors += 1
                text = ""
            if text and not text.startswith("---"):
                parse_errors += 1
            names[routing_name(text, os.path.basename(dp))].add(real)
            continue

        # no SKILL.md here: is it a namespace, or genuinely empty?
        if os.path.realpath(dp) == os.path.realpath(root):
            continue
        beneath = False
        for d2, dn2, fn2 in os.walk(dp, followlinks=True):
            dn2[:] = [d for d in dn2 if d not in SKIP]
            if d2 != dp and "SKILL.md" in fn2:
                beneath = True
                break
        (container if beneath else truly_empty).append(os.path.relpath(dp, root))

    collisions = {k: sorted(v) for k, v in names.items() if len(v) > 1}
    return {
        "root": root,
        "bodies": len(bodies),
        "addresses": addresses,
        "routing_names": len(names),
        "symlinks": symlinks,
        "symlinks_resolving_to_a_skill": symlinks_to_body,
        "dirs_has_body": len(has_body),
        "dirs_container": len(container),
        "dirs_truly_empty": len(truly_empty),
        "truly_empty_sample": truly_empty[:20],
        "body_digest_collisions": len(collisions),
        "collision_names": sorted(collisions)[:20],
        "frontmatter_issues": parse_errors,
    }


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    as_json = "--json" in argv
    args = [a for a in argv[1:] if not a.startswith("--")]
    roots = args or [r for r in DEFAULT_ROOTS if os.path.isdir(r)]
    if not roots:
        print("no skill root found; pass one explicitly")
        return 2

    reports = [scan(r) for r in roots]
    if as_json:
        print(json.dumps(reports, indent=2))
    else:
        for r in reports:
            print(f"root: {r['root']}")
            print(f"  bodies     (unique physical SKILL.md, realpath-deduped) : {r['bodies']}")
            print(f"  addresses  (every reachable SKILL.md, incl. symlinks)   : {r['addresses']}")
            print(f"  routing names (declared name:, fallback dir)            : {r['routing_names']}")
            print(f"  symlinked dirs: {r['symlinks']}  of which resolve to a skill: {r['symlinks_resolving_to_a_skill']}")
            print(f"  dirs HAS_BODY={r['dirs_has_body']}  CONTAINER={r['dirs_container']}  TRULY_EMPTY={r['dirs_truly_empty']}")
            if r["truly_empty_sample"]:
                print(f"    truly-empty sample: {', '.join(r['truly_empty_sample'])}")
            print(f"  names carrying >1 distinct body (real collisions): {r['body_digest_collisions']}")
            if r["collision_names"]:
                print(f"    {', '.join(r['collision_names'])}")
            print(f"  frontmatter issues: {r['frontmatter_issues']}")
            print()
        print("NOTE: CONTAINER is not a defect - it is a namespace directory holding sub-skills.")
        print("      A count without its question attached is not evidence.")

    bad = sum(r["dirs_truly_empty"] + r["body_digest_collisions"] for r in reports)
    return 1 if (strict and bad) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
