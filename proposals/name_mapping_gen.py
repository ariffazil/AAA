#!/usr/bin/env python3
"""Name-mapping generator — resolves the 56 dead adapters to their renamed
on-disk counterparts.

Chain: v3_name -> related[] (semantic hint in alias table) -> current disk path
(fuzzy-resolved against the live view roots, because `related` names are also stale).

Read-only. Emits a proposal; does not mutate SKILL_ALIAS_TABLE.json.
"""
import json, os, re, yaml
from collections import defaultdict

V3 = "/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml"
ALIAS = "/root/AAA/skills/SKILL_ALIAS_TABLE.json"
OUT = "/root/AAA/proposals/NAME-MAPPING-DRAFT-20260923.json"

ROOTS = [
    "/root/GEOX/skills", "/root/WELL/skills", "/root/WEALTH/skills",
    "/root/arifOS/skills", "/root/HERMES/skills", "/root/AAA/skills",
    "/root/.kimi-code/skills", "/root/.arifos/agents/opencode/skills",
    "/root/.codex/skills", "/root/.codex/skills-curated",
    "/root/.forge/skills",
]

# --- disk index: basename -> paths ---
index = defaultdict(list)
for root in ROOTS:
    if not os.path.isdir(root):
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for d in dirnames:
            index[d].append(os.path.join(dirpath, d))
        for f in filenames:
            index[f].append(os.path.join(dirpath, f))

def toks(s):
    return set(re.split(r"[^a-z0-9]+", s.lower())) - {""}

def fuzzy(name):
    if name in index:
        return [(100.0, name, index[name][0])]
    t = toks(name)
    out = []
    for disk, paths in index.items():
        d = toks(disk)
        # specificity: skip bare directory names (geox/wealth/prospect/forge) when query is multi-token
        if len(t) >= 2 and len(d) < 2:
            continue
        inter = t & d
        if not inter:
            continue
        contain = len(inter) / len(t)
        jac = len(inter) / len(t | d)
        s = contain * 60 + jac * 30
        if disk.lower().startswith(name.lower()) or name.lower().startswith(disk.lower()):
            s += 20
        if s >= 25:
            out.append((round(s, 1), disk, paths[0]))
    out.sort(key=lambda x: -x[0])
    return out[:5]

# --- authority + alias ---
v3 = yaml.safe_load(open(V3))
rows = json.load(open(ALIAS)).get("aliases", [])
referenced = set()
for layer in ("substrate", "knowledge"):
    referenced.update(v3["layers"][layer].get("skills", []))
for dom, skills in v3["layers"]["domain"].get("domains", {}).items():
    referenced.update(skills or [])

mapping = []
for r in rows:
    name = r.get("v3_name")
    if r.get("tombstone"):
        continue
    if name not in referenced:
        continue  # orphan — separate concern
    p = r.get("primary_path") or r.get("primary_resolved")
    if p and os.path.exists(p):
        continue  # live adapter, skip
    related = [rel.get("name") for rel in (r.get("related") or []) if rel.get("name")]
    cands = {}
    best = None
    for rel in related:
        c = fuzzy(rel)
        cands[rel] = c
        if c and (best is None or c[0][0] > best[0]):
            best = (c[0][0], rel, c[0][1], c[0][2])
    mapping.append({
        "skill": name,
        "related": related,
        "candidates": cands,
        "best_score": best[0] if best else None,
        "best_related": best[1] if best else None,
        "best_disk": best[2] if best else None,
        "best_path": best[3] if best else None,
    })

high, medium, low = [], [], []
for e in mapping:
    s = e["best_score"]
    tup = (e["skill"], e["best_related"], e["best_disk"], e["best_path"], s)
    if s is None:
        low.append((e["skill"], None, None, None, None))
    elif s >= 80:
        high.append(tup)
    elif s >= 40:
        medium.append(tup)
    else:
        low.append(tup)

result = {
    "generated": "2026-09-23",
    "mode": "PROPOSAL_ONLY",
    "method": "v3_name -> related (semantic) -> disk (fuzzy), score=token-overlap+prefix",
    "dead_adapters_total": len(mapping),
    "confidence": {
        "high": [{"skill": h[0], "via_related": h[1], "disk": h[2], "path": h[3], "score": h[4]} for h in high],
        "medium": [{"skill": m[0], "via_related": m[1], "disk": m[2], "path": m[3], "score": m[4]} for m in medium],
        "low": [{"skill": l[0], "via_related": l[1], "disk": l[2], "path": l[3], "score": l[4]} for l in low],
    },
    "mapping": mapping,
}
json.dump(result, open(OUT, "w"), indent=2)
print(f"dead adapters: {len(mapping)}")
print(f"high: {len(high)} | medium: {len(medium)} | low(needs semantic): {len(low)}")
print("\n--- HIGH (score>=80) ---")
for h in high:
    print(f"  {h[0]}  ->  {h[2]}  (via '{h[1]}', {h[4]})")
print("\n--- MEDIUM (40-79) ---")
for m in medium:
    print(f"  {m[0]}  ->  {m[2]}  (via '{m[1]}', {m[4]})")
print("\n--- LOW / NONE (needs semantic judgment) ---")
for l in low:
    print(f"  {l[0]}  ->  {l[2] or 'NO MATCH'}  (via '{l[1]}', {l[4]})")
print("\nOUT:", OUT)
