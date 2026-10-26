#!/usr/bin/env python3
"""safe-prune-guard — block capability deletion that has live dependents.

consumer: skill-mesh step-16/19 ("Move is a migration") + every future prune lane;
          run BEFORE rm/mv of any canonical skill body.
failure class: 48052198 (2026-10-18 autonomous "acah2 skill pruning" deleted the
          F13-forged pdf-federation package while 5 live tombstones routed every
          PDF job to it; no dependents sweep, no archive, no rollback).
usage:    python3 safe-prune-guard.py /root/AAA/skills/<pkg> [--json]
verdict:  ALLOW  = no live dependents found (still archive + manifest the removal)
          BLOCK  = dependents exist; migrate or get F13 first
limits:   grep-level static scan; dynamic/cron/plugin references may exist that no
          scan can prove absent — "zero dependents" from this tool is NOT proof.
"""
import os, re, sys, json

TARGET = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ""
SCAN_ROOTS = ["/root/AAA/skills", "/root/.hermes/skills", "/root/.opencode/skills",
              "/root/.agents/skills", "/root/.claude/skills", "/root/.arifos",
              "/root/HERMES", "/root/AAA/instructions"]
EXCL = {".git", "__pycache__", "node_modules", "venv", ".venv"}

def dependents(target):
    name = os.path.basename(target.rstrip("/"))
    hits = {"view_links": [], "tombstone_refs": [], "text_refs": [], "cron_refs": []}
    for root in SCAN_ROOTS:
        if not os.path.exists(root):
            continue
        for dp, dns, fns in os.walk(root, followlinks=False):
            dns[:] = [d for d in dns if d not in EXCL]
            for n in dns + fns:
                p = os.path.join(dp, n)
                if os.path.islink(p):
                    try:
                        if os.path.realpath(p) == os.path.realpath(target):
                            hits["view_links"].append(p)
                    except OSError:
                        pass
                elif n.endswith((".md", ".json", ".yaml", ".yml", ".toml")) and os.path.isfile(p):
                    try:
                        txt = open(p, encoding="utf-8", errors="replace").read(200000)
                    except Exception:
                        continue
                    if name in txt and os.path.realpath(p) != os.path.join(os.path.realpath(target), n):
                        if re.search(r"canonical_owner:|absorbed_into:|do_not_select:", txt):
                            hits["tombstone_refs"].append(p)
                        elif "skill" in n.lower() or n in ("jobs.json",):
                            hits["cron_refs"].append(p)
                        else:
                            hits["text_refs"].append(p)
    return hits

if __name__ == "__main__":
    if not TARGET or not os.path.exists(TARGET):
        print("usage: safe-prune-guard.py <canonical skill path>"); sys.exit(2)
    d = dependents(TARGET)
    total = sum(len(v) for v in d.values())
    verdict = "BLOCK" if total else "ALLOW"
    if "--json" in sys.argv:
        print(json.dumps({"target": TARGET, "verdict": verdict, "dependents": d}, indent=1))
    else:
        print(f"verdict={verdict}  target={TARGET}  dependents={total}")
        for k, v in d.items():
            for x in v[:10]:
                print(f"  [{k}] {x}")
        if verdict == "BLOCK":
            print("→ migrate dependents or take F13 first. Removal without this = 48052198 class.")
        else:
            print("→ ALLOW is not proof: archive the body + write the rollback manifest anyway.")
    sys.exit(1 if verdict == "BLOCK" else 0)
