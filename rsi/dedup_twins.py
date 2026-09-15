#!/usr/bin/env python3
"""dedup_twins.py — OPEN ITEM #4 (compress): resolve 78 duplicate-name skill groups.

INPUT:  /root/work/research/skills-dedup-inventory-2026-09-15.json (333-AGI, 2026-09-15)
FACTS:  328 SKILL.md on disk, 221 unique names, 78 duplicate groups —
        ALL 78 are identical-content twins (SHA256-equal), ZERO content forks.
        → shadowing risk today = ZERO; dedup is safe mechanical cleanup.
WINNER RULE (all twins identical, so choice is cosmetic): keep the copy at the
        SHALLOWEST path (canonical top-level entries win over nested mirrors);
        tie-break lexicographic. Registry V3 + SKILL_ALIAS_TABLE unaffected
        (names unchanged — only redundant FILES removed).

MODES:
  --dry-run   (default) list planned deletions. No writes.
  --execute   delete redundant twin files (F1: identical-content verified at
              runtime AGAIN before each delete; abort on any hash mismatch).

EFFECT when executed: 328 → 221 files; advertisement tax drops ~5-6k tok/call.
"""

import json, os, sys, hashlib

STORE = "/root/AAA/skills"
INV = "/root/work/research/skills-dedup-inventory-2026-09-15.json"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def winner(copies):
    return sorted(copies, key=lambda c: (c["path"].count("/"), c["path"]))[0]


def main():
    execute = "--execute" in sys.argv
    inv = json.load(open(INV))
    groups = inv["duplicate_groups"]
    plan, deleted = [], []
    for name, copies in sorted(groups.items()):
        keep = winner(copies)["path"]
        for c in copies:
            p = c["path"]
            if p == keep:
                continue
            full = os.path.join(STORE, p)
            if not os.path.isfile(full):
                continue
            if sha(full) != sha(os.path.join(STORE, keep)):
                plan.append({"file": p, "ABORT": "content diverged since inventory"})
                continue
            plan.append({"file": p, "keep": keep})
            if execute:
                os.remove(full)
                deleted.append(p)
    print(
        json.dumps(
            {
                "mode": "execute" if execute else "dry-run",
                "groups": len(groups),
                "planned_deletions": sum(1 for p in plan if "ABORT" not in p),
                "aborted_diverged": sum(1 for p in plan if "ABORT" in p),
                "executed_deletions": len(deleted),
                "sample": plan[:5],
            },
            indent=1,
        )
    )


if __name__ == "__main__":
    main()
