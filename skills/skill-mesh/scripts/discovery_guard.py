#!/usr/bin/env python3
"""discovery_guard.py — the pre-retirement check that enforces the hard rule:

    A MERGE MUST NOT LOSE DISCOVERY.

WHY THIS EXISTS
  A consolidation can be perfect on content and still kill a capability: if the merged body no longer
  contains the phrases a caller would search for, the next agent cannot find the capability, assumes it
  is missing, and authors a new skill. The duplication returns through the front door, wearing a new
  name — and the store is now one skill LARGER than before the cleanup. Removing duplication without
  proving discovery survived is how a cleanup raises entropy.

  So the rule is not "did the content land" (that is merge_completeness) but "will the OLD NAME still
  land somewhere". Two things must survive every retirement:
    1. every distinct trigger phrase from each source description / triggers list, and
    2. the source's own NAME, present in the merged body (normally in the old-name -> new-mode table).

USAGE
  python3 discovery_guard.py <merged_skill_dir> <source_dir> [<source_dir> ...]
  python3 discovery_guard.py --ledger <LEDGER.json> <merged_skill_dir>
      LEDGER.json entries may carry {"orig_path"|"rel", "successor"} — sources are taken from it.

  Read-only. Exit 0 = discovery preserved. Exit 1 = a GAP was found (the merge is not safe to ship),
  and the gap is named so it can be repaired before the source leaves the tree.
"""
from __future__ import annotations

import json
import os
import re
import sys

STOP = {
    "use", "when", "the", "a", "an", "and", "or", "for", "to", "of", "in", "on", "with", "that",
    "this", "is", "are", "be", "by", "as", "at", "it", "its", "from", "into", "any", "all", "not",
    "load", "skill", "skills", "see", "instead", "then", "than", "so", "if", "you", "your", "they",
    "them", "his", "her", "their", "before", "after", "over", "under", "but", "was", "were", "will",
    "one", "two", "own", "who", "whom", "what", "which", "how", "why", "where", "can", "may", "must",
}


def frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[1]
    return ""


def phrases_from(source_md: str) -> list[str]:
    """Distinctive multi-word phrases a caller might search for: quoted strings in the description,
    plus explicit triggers entries, plus title-cased frontmatter term phrases."""
    fm = frontmatter(source_md)
    out: list[str] = []

    for m in re.finditer(r'description:\s*("([^"]+)"|\'([^\']+)\'|(.+?)(?=\n[a-z_]+:|\n---|\Z))',
                         fm, re.S):
        desc = (m.group(2) or m.group(3) or m.group(4) or "").strip()
        for q in re.findall(r'["\u201c]([^"\u201d]{8,80})["\u201d]', desc):
            out.append(q.strip())
        out.append(desc)

    tm = re.search(r'triggers:\s*\n((?:\s*-\s*.+\n)+)', fm)
    if tm:
        for line in tm.group(1).splitlines():
            v = line.strip().lstrip("-").strip().strip('"\'')
            if v:
                out.append(v)

    clean = []
    for p in out:
        p = re.sub(r"\s+", " ", p).strip()
        if len(p) < 8:
            continue
        clean.append(p)
    return clean


def key_terms(phrase: str) -> list[str]:
    """Terms that must each be findable in the merged body for this phrase to still match."""
    toks = re.findall(r"[a-z0-9][a-z0-9._/-]{3,}", phrase.lower())
    return sorted({t for t in toks if t not in STOP})


def check(merged_dir: str, source_dirs: list[str]) -> int:
    merged_path = os.path.join(merged_dir, "SKILL.md")
    if not os.path.isfile(merged_path):
        print(f"FAIL: no SKILL.md at {merged_path}")
        return 1
    merged = open(merged_path, encoding="utf-8", errors="replace").read().lower()

    gaps = 0
    for sd in source_dirs:
        sp = os.path.join(sd, "SKILL.md")
        name = os.path.basename(sd.rstrip("/"))
        if not os.path.isfile(sp):
            print(f"  SKIP {name}: no SKILL.md in {sd}")
            continue
        src = open(sp, encoding="utf-8", errors="replace").read()

        missing_name = name.lower() not in merged
        ph = phrases_from(src)
        lost = []
        for p in ph:
            terms = key_terms(p)
            if not terms:
                continue
            hit = sum(1 for t in terms if t in merged)
            if hit / len(terms) < 0.6:
                lost.append(p[:70])

        status = "PASS" if (not missing_name and not lost) else "GAP "
        print(f"  {status} {name}"
              + ("  [name absent from merged body]" if missing_name else "")
              + (f"  [{len(lost)} phrase(s) lost]" if lost else ""))
        for l in lost[:4]:
            print(f"        lost phrase: {l!r}")
        if missing_name or lost:
            gaps += 1

    return 1 if gaps else 0


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args:
        print(__doc__)
        return 2

    if args[0] == "--ledger":
        ledger = json.load(open(args[1]))
        merged_dir = args[2]
        srcs = []
        for it in ledger.get("items", ledger if isinstance(ledger, list) else []):
            p = it.get("orig_path") or it.get("rel")
            if p:
                srcs.append(p if os.path.isabs(p) else os.path.join(
                    ledger.get("canon", "/root/AAA/skills"), p))
        return check(merged_dir, srcs)

    merged_dir, srcs = args[0], args[1:]
    print(f"discovery_guard: {merged_dir}  <-  {len(srcs)} source(s)")
    rc = check(merged_dir, srcs)
    print("VERDICT:", "DISCOVERY PRESERVED" if rc == 0 else "DISCOVERY GAP — do not retire yet")
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
