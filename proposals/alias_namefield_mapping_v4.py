#!/usr/bin/env python3
"""Phase 2d: merged final proposal. Curated (v3) wins over semantic (v2).
Semantic with high confidence (>=0.7) becomes RETARGET;
0.45-0.7 becomes FLAG_REVIEW; below is TOMBSTONE.
Read-only proposal.
"""
import json, os
from datetime import datetime, timezone

V2 = "/root/AAA/proposals/ALIAS-RERESOLVE-MAPPING-v2-20260923.json"
V3 = "/root/AAA/proposals/ALIAS-RERESOLVE-MAPPING-v3-20260923.json"
OUT_JSON = "/root/AAA/proposals/ALIAS-RERESOLVE-MAPPING-FINAL-20260923.json"
OUT_MD = "/root/AAA/proposals/ALIAS-RERESOLVE-MAPPING-FINAL-20260923.md"

v2 = json.load(open(V2))
v3 = json.load(open(V3))

curated_by_name = {r["v3_name"]: r for r in v3["results"]["RETARGET_CURATED"]}
sem_retarget = {r["v3_name"]: r for r in v2["results"]["RETARGET"]}
sem_flag = {r["v3_name"]: r for r in v2["results"]["FLAG_REVIEW"]}
sem_tomb = {r["v3_name"]: r for r in v2["results"]["TOMBSTONE"]}

final = {"RETARGET": [], "FLAG_REVIEW": [], "TOMBSTONE": [], "other": []}

all_names = set(curated_by_name) | set(sem_retarget) | set(sem_flag) | set(sem_tomb)
for name in sorted(all_names):
    if name in curated_by_name:
        r = curated_by_name[name]
        final["RETARGET"].append({**r, "method": "curated-organ-native", "confidence": "HIGH"})
    elif name in sem_retarget and sem_retarget[name].get("score", 0) >= 0.70:
        r = sem_retarget[name]
        final["RETARGET"].append({**r, "method": "semantic-high", "confidence": "MEDIUM-HIGH"})
    elif name in sem_retarget:
        r = sem_retarget[name]
        final["FLAG_REVIEW"].append({**r, "method": "semantic-mid", "confidence": "MEDIUM", "reason": "score 0.45-0.7, human verify"})
    elif name in sem_flag:
        final["FLAG_REVIEW"].append({**sem_flag[name], "method": "tie", "confidence": "LOW"})
    else:
        final["TOMBSTONE"].append({**sem_tomb[name], "method": "semantic-no-match", "confidence": "HIGH"})

result = {
    "generated": datetime.now(timezone.utc).isoformat(),
    "phase": "2d-final-merged-proposal",
    "mode": "proposal-only / read-only",
    "counts": {k: len(v) for k, v in final.items()},
    "results": final,
}
json.dump(result, open(OUT_JSON, "w"), indent=2)

md = ["# ALIAS RERESOLVE — Final Namefield Mapping Proposal", ""]
md.append(f"Generated: {result['generated']}")
md.append(f"Total rows classified: {sum(result['counts'].values())}")
md.append("")
md.append("## 1. RETARGET — apply these renames to SKILL_ALIAS_TABLE.json")
md.append("")
md.append("| V3 | → target | method | confidence |")
md.append("|---|---|---|---|")
for r in final["RETARGET"]:
    md.append(f"| `{r['v3_name']}` | `{r['target_disk_name']}` | {r['method']} | {r['confidence']} |")
md.append("")
md.append("## 2. FLAG_REVIEW — human judgment needed")
md.append("")
for r in final["FLAG_REVIEW"]:
    if "candidates" in r:
        c = ", ".join(f"`{c['name']}` ({c['score']})" for c in r["candidates"])
        md.append(f"- `{r['v3_name']}` — candidates: {c}")
    else:
        md.append(f"- `{r['v3_name']}` → `{r.get('target_disk_name','-')}` (score {r.get('score','-')}) — verify semantic fit")
md.append("")
md.append("## 3. TOMBSTONE — no disk truth, remove from alias table")
md.append("")
for r in final["TOMBSTONE"]:
    md.append(f"- `{r['v3_name']}` — {r.get('reason','')}")
open(OUT_MD, "w").write("\n".join(md))

print(json.dumps(result["counts"], indent=2))
print(f"OUT: {OUT_JSON}")
print(f"OUT: {OUT_MD}")
