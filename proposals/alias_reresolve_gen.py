#!/usr/bin/env python3
"""Alias re-resolve worklist generator — Phase 1b of the re-anchor.

Read-only. Indexes every skill location across all view roots, then resolves
each logical skill (dead adapters, orphan alias rows, and no-alias skills) to
disk truth and proposes a per-row verdict: RETARGET / TOMBSTONE / CREATE_ROW / FLAG.

Emits a proposal only. Does NOT mutate SKILL_ALIAS_TABLE.json.
"""
import json, os, yaml
from collections import defaultdict

V3 = "/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml"
ALIAS = "/root/AAA/skills/SKILL_ALIAS_TABLE.json"
OUT = "/root/AAA/proposals/ALIAS-RERESOLVE-WORKLIST-DRAFT-20260923.json"

ROOTS = [
    "/root/GEOX/skills",
    "/root/WELL/skills",
    "/root/WEALTH/skills",
    "/root/arifOS/skills",
    "/root/HERMES/skills",
    "/root/AAA/skills",
    "/root/.agents/skills",
    "/root/.kimi-code/skills",
    "/root/.arifos/agents/opencode/skills",
    "/root/.codex/skills",
    "/root/.codex/skills-curated",
    "/root/.forge/skills",
    "/root/.grok/skills",
]

# --- index basename -> [full paths] ---
index = defaultdict(list)
root_report = {}
for root in ROOTS:
    if not os.path.isdir(root):
        root_report[root] = "MISSING"
        continue
    n = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for d in dirnames:
            index[d].append(os.path.join(dirpath, d)); n += 1
        for f in filenames:
            index[f].append(os.path.join(dirpath, f)); n += 1
    root_report[root] = f"{n} entries"

def best(locs):
    """Pick the recommended retarget path: organ-native > AAA > others."""
    order = ["/root/GEOX/", "/root/WELL/", "/root/WEALTH/", "/root/arifOS/", "/root/HERMES/", "/root/AAA/", "/root/.agents/"]
    for pref in order:
        for l in locs:
            if l.startswith(pref):
                return l
    return locs[0]

# --- load authority + alias ---
v3 = yaml.safe_load(open(V3))
rows = json.load(open(ALIAS)).get("aliases", [])
by_name = defaultdict(list)
for r in rows:
    by_name[r.get("v3_name")].append(r)

# referenced skills (logical registry)
referenced = set()
layers = v3.get("layers", {})
for layer in ("substrate", "knowledge"):
    referenced.update(layers.get(layer, {}).get("skills", []))
for dom, skills in (layers.get("domain", {}).get("domains") or {}).items():
    referenced.update(skills or [])

worklist = []

# class 1: dead adapters (referenced, in alias, path doesn't exist)
# class 2: orphans (non-tombstone alias row, NOT referenced)
# class 3: no-alias (referenced, no alias row)

seen = set()
for r in rows:
    name = r.get("v3_name")
    if r.get("tombstone"):
        continue
    if name in referenced:
        p = r.get("primary_path") or r.get("primary_resolved")
        if p and os.path.exists(p):
            continue  # live, skip
        locs = index.get(name, [])
        entry = {
            "skill": name,
            "class": "dead_adapter",
            "current_path": p,
            "home": r.get("primary_home"),
            "found_locations": locs,
            "recommended": best(locs) if locs else None,
            "verdict": "RETARGET" if locs else "TOMBSTONE",
        }
        worklist.append(entry); seen.add(name)
    else:
        # orphan: not referenced by V3
        p = r.get("primary_path") or r.get("primary_resolved")
        locs = index.get(name, [])
        entry = {
            "skill": name,
            "class": "orphan",
            "current_path": p,
            "home": r.get("primary_home"),
            "found_locations": locs,
            "recommended": best(locs) if locs else None,
            "verdict": "FLAG_REVIEW" if locs else "TOMBSTONE",
        }
        worklist.append(entry); seen.add(name)

# class 3: no-alias
for name in sorted(referenced):
    if name in seen or name in by_name:
        continue
    locs = index.get(name, [])
    entry = {
        "skill": name,
        "class": "no_alias",
        "current_path": None,
        "home": None,
        "found_locations": locs,
        "recommended": best(locs) if locs else None,
        "verdict": "CREATE_ROW" if locs else "FLAG_PHANTOM",
    }
    worklist.append(entry)

from collections import Counter
tally = Counter(e["verdict"] for e in worklist)

result = {
    "generated": "2026-09-23",
    "mode": "PROPOSAL_ONLY (no mutation)",
    "roots": root_report,
    "tally": dict(tally),
    "total_rows_proposed": len(worklist),
    "worklist": worklist,
}
json.dump(result, open(OUT, "w"), indent=2)
print("ROOTS:")
for k, v in root_report.items():
    print(f"  {k}: {v}")
print("\nTALLY:", dict(tally))
print("TOTAL:", len(worklist))
print("OUT:", OUT)
