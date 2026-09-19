#!/usr/bin/env python3
"""Repoint resolution aliases whose target was retired in the 2026-09-19 namespace collapse.
Alias -> surviving canonical where one exists; alias deleted where the name itself is retired.
Evidence: /root/AAA/skills-retired/2026-09-19-namespace-collapse/LEDGER.json"""
import os, json

CANON = "/root/AAA/skills"
APPLY = "--apply" in __import__("sys").argv

# alias path -> (survivor relpath | None to delete)
MAP = {
 "capabilities/coding/mcp-testing":                 "domains/general/forge/mcp-ops/mcp-testing",
 "domains/forge/skill-creator":                     "domains/general/aaa/skill-mesh/skill-creator",
 "domains/capital/wealth-claim-state":              None,
 "workflows/core/help":                             None,
 "primitives/think/causal555-pywhy":                None,
 "primitives/memory/wisdom-scar-session-audit":     "governance-core/scar-integration",
 "primitives/think/reflective/sovereign-recognize": "human-interface/audience-scoped-disclosure",
 "help":                                            None,
 "wisdom-scar-session-audit":                       None,
}

# verify survivors exist on disk
ok = {}
for a, s in MAP.items():
    if s is None:
        ok[a] = None
        continue
    cand = os.path.join(CANON, s)
    if os.path.isdir(cand):
        ok[a] = s
    else:
        # search by folder name
        name = os.path.basename(s)
        hits = []
        for dp, dn, fn in os.walk(CANON):
            if "/." in dp.replace(CANON, ""):
                continue
            if os.path.basename(dp) == name and "SKILL.md" in fn:
                hits.append(os.path.relpath(dp, CANON))
        ok[a] = hits[0] if len(hits) == 1 else ("AMBIGUOUS:" + str(hits) if hits else "MISSING")

for a, s in sorted(ok.items()):
    print(f"{a:50s} -> {s}")

if not APPLY:
    print("DRY RUN — pass --apply")
    raise SystemExit(0)

for a, s in ok.items():
    p = os.path.join(CANON, a)
    if not os.path.islink(p):
        continue
    if isinstance(s, str) and s.startswith(("AMBIGUOUS", "MISSING", "")) and s == "":
        pass
    if s is None or (isinstance(s, str) and (s.startswith("AMBIGUOUS") or s == "MISSING")):
        os.unlink(p)
        print("removed retired alias:", a)
    else:
        rel = os.path.relpath(os.path.join(CANON, s), os.path.dirname(p))
        os.unlink(p)
        os.symlink(rel, p)
        print("repointed:", a, "->", rel)

# dangling links anywhere in canon pointing into the freeze root
FREEZE = "/root/AAA/skills-retired"
for dp, dn, fn in os.walk(CANON):
    for n in list(dn) + list(fn):
        p = os.path.join(dp, n)
        if os.path.islink(p) and not os.path.exists(p):
            tgt = os.readlink(p)
            if FREEZE in tgt or tgt.startswith("/root/AAA/skills-retired"):
                os.unlink(p)
                print("removed link into freeze root:", os.path.relpath(p, CANON))
