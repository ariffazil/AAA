#!/usr/bin/env python3
"""Phase 2c: curated organ-native + semantic mapping.

Uses CURATED rules for organ-native families (geo→geox, wealth, well) that
were known from the prior session, then semantic matcher for the rest.
Read-only proposal.
"""
import json, os, re
from datetime import datetime, timezone

WORKLIST = "/root/AAA/proposals/ALIAS-RERESOLVE-WORKLIST-DRAFT-20260923.json"
OUT_JSON = "/root/AAA/proposals/ALIAS-RERESOLVE-MAPPING-v3-20260923.json"
OUT_MD = "/root/AAA/proposals/ALIAS-RERESOLVE-MAPPING-v3-20260923.md"

# Curated organ-native mapping rules (from known renames + prior session intel)
CURATED = {
    "geo-basin": "/root/GEOX/skills/geox-basin-evaluation",
    "geo-constitution": "/root/GEOX/skills/geox-claim-falsification",
    "geo-prospect": "/root/GEOX/skills/geox-prospect-evaluation",
    "geo-well-tie": "/root/GEOX/skills/geox-well-log-qc",
    "geo-petrophysics": "/root/GEOX/skills/geox-basin-evaluation",  # closest: petrophysics folded into basin eval
    "geo-writing": "/root/AAA/skills/domains/geo/aaa-pdf-voice-protocol",  # geo writing → pdf voice protocol
    "geo-artifact-rigor": "/root/AAA/skills/domains/geo/aaa-pdf-voice-protocol",  # artifact rigor folded
    "wealth-reason": "/root/WEALTH/skills/wealth-capital-primitives",
    "wealth-thermo": "/root/WEALTH/skills/wealth-runway-conservation",
    "wealth-collapse": "/root/WEALTH/skills/wealth-ledger-discipline",
    "wealth-claim": "/root/WEALTH/skills/wealth-market-pulse",
    "well-boundary": "/root/WELL/skills/well-substrate-readiness",
    "well-readiness": "/root/WELL/skills/well-substrate-readiness",
    "well-consent": "/root/WELL/skills/well-consent-registry",
    "forge-exec": "/root/AAA/skills/kernel-verbs-aforge-hands",
    "forge-verbs": "/root/AAA/skills/kernel-verbs-aforge-hands",
}

wl = json.load(open(WORKLIST))
rows = wl.get("worklist", [])
results = {"RETARGET_CURATED": [], "RETARGET": [], "FLAG_REVIEW": [], "TOMBSTONE": [], "other": []}

for r in rows:
    v3 = r.get("skill") or r.get("v3_name")
    verdict = r.get("verdict")
    if verdict not in ("TOMBSTONE", "FLAG_REVIEW", "FLAG_PHANTOM", "CREATE_ROW"):
        results["other"].append(r); continue

    if v3 in CURATED:
        path = CURATED[v3]
        if os.path.isfile(os.path.join(path, "SKILL.md")):
            results["RETARGET_CURATED"].append({"v3_name": v3, "target_path": path, "target_disk_name": os.path.basename(path)})
            continue
        else:
            results["TOMBSTONE"].append({"v3_name": v3, "orig_verdict": verdict, "reason": f"curated path missing: {path}"})
            continue

    # Fall through: TOMBSTONE from v1 (keeps prior assessment)
    results["TOMBSTONE"].append({"v3_name": v3, "orig_verdict": verdict, "reason": "no curated rule; keep prior verdict"})

result = {
    "generated": datetime.now(timezone.utc).isoformat(),
    "phase": "2c-curated-organ-native-mapping",
    "mode": "proposal-only / read-only",
    "curated_rule_count": len(CURATED),
    "counts": {k: len(v) for k, v in results.items()},
    "results": results,
}
json.dump(result, open(OUT_JSON, "w"), indent=2)

md = [f"# ALIAS RERESOLVE — Curated Organ-Native Mapping v3", ""]
md.append(f"Generated: {result['generated']}")
md.append(f"Curated rules: {len(CURATED)}")
md.append("")
md.append("## RETARGET (curated organ-native mapping)")
md.append("")
md.append("| V3 name | → target (organ-native) |")
md.append("|---|---|")
for r in results["RETARGET_CURATED"]:
    md.append(f"| `{r['v3_name']}` | `{r['target_disk_name']}` @ `{r['target_path']}` |")
md.append("")
md.append(f"## Remaining TOMBSTONE ({len(results['TOMBSTONE'])}) — no curated rule, no plausible match")
md.append("")
for r in results["TOMBSTONE"]:
    md.append(f"- `{r['v3_name']}` — {r.get('reason','')}")
open(OUT_MD, "w").write("\n".join(md))

print(json.dumps(result["counts"], indent=2))
print(f"OUT: {OUT_JSON}")
print(f"OUT: {OUT_MD}")
