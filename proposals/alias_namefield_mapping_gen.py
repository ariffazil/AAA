#!/usr/bin/env python3
"""Phase 2 of the re-anchor: semantic namefield mapping for dead adapters.

Reads ALIAS-RERESOLVE-WORKLIST-DRAFT, for each dead_adapter row derives the
RETARGET target from current_path (normalizing through the AAA symlink),
verifies the target SKILL.md exists on disk, and emits a proposal artifact.

Read-only. Does NOT mutate SKILL_ALIAS_TABLE.json.
"""
import json, os, sys
from collections import defaultdict

WORKLIST = "/root/AAA/proposals/ALIAS-RERESOLVE-WORKLIST-DRAFT-20260923.json"
ALIAS = "/root/AAA/skills/SKILL_ALIAS_TABLE.json"
OUT_JSON = "/root/AAA/proposals/ALIAS-RERESOLVE-MAPPING-20260923.json"
OUT_MD = "/root/AAA/proposals/ALIAS-RERESOLVE-MAPPING-20260923.md"

def norm(p):
    if not p: return None
    return p.replace("/root/.agents/skills", "/root/AAA/skills", 1)

wl = json.load(open(WORKLIST))
rows = wl.get("worklist", [])

retargets = []
true_tombstones = []
others = defaultdict(list)

for r in rows:
    v3 = r.get("skill") or r.get("v3_name")
    verdict = r.get("verdict")
    path = norm(r.get("current_path") or r.get("resolved_path"))
    if verdict == "TOMBSTONE":
        if path and os.path.isdir(path):
            # find SKILL.md under path or direct
            candidates = []
            for pth in (path, os.path.dirname(path)):
                cand = os.path.join(pth, "SKILL.md")
                if os.path.isfile(cand):
                    candidates.append(cand)
            if candidates:
                retargets.append({
                    "v3_name": v3,
                    "target_disk_name": os.path.basename(path),
                    "target_path": path,
                    "skill_md": candidates[0],
                    "verdict": "RETARGET",
                })
            else:
                true_tombstones.append({"v3_name": v3, "path": path, "reason": "path-exists-but-no-SKILL.md"})
        else:
            # no path or path missing — check if the basename exists anywhere
            base = os.path.basename(path or "")
            found = None
            if base:
                # search canonical tree
                for root, dirs, files in os.walk("/root/AAA/skills"):
                    if base in dirs and os.path.isfile(os.path.join(root, base, "SKILL.md")):
                        found = os.path.join(root, base)
                        break
            if found:
                retargets.append({"v3_name": v3, "target_disk_name": base, "target_path": found,
                                  "skill_md": os.path.join(found, "SKILL.md"), "verdict": "RETARGET"})
            else:
                true_tombstones.append({"v3_name": v3, "path": path, "reason": "no-disk-truth"})
    elif verdict in ("CREATE_ROW", "FLAG_REVIEW", "FLAG_PHANTOM"):
        others[verdict].append({"skill": v3, "path": path})

result = {
    "generated": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    "phase": "2-namefield-mapping",
    "mode": "proposal-only / read-only",
    "canonical_source": ALIAS,
    "retarget_count": len(retargets),
    "true_tombstone_count": len(true_tombstones),
    "retargets": retargets,
    "true_tombstones": true_tombstones,
    "others": {k: v for k, v in others.items()},
}
json.dump(result, open(OUT_JSON, "w"), indent=2, default=str)

# markdown summary
lines = ["# ALIAS RERESOLVE — Namefield Mapping Proposal", ""]
lines.append(f"Generated: {result['generated']}")
lines.append(f"RETARGET candidates: {len(retargets)} · true tombstones: {len(true_tombstones)}")
lines.append("")
lines.append("## RETARGETS (rename-mapped, disk-verified)")
lines.append("")
lines.append("| V3 name | → target (disk) | SKILL.md |")
lines.append("|---|---|---|")
for r in retargets:
    lines.append(f"| `{r['v3_name']}` | `{r['target_disk_name']}` | `{r['skill_md'].replace('/root/AAA/skills/','')}` |")
lines.append("")
lines.append("## TRUE TOMBSTONES (no disk truth)")
lines.append("")
lines.append("| V3 name | reason |")
lines.append("|---|---|")
for r in true_tombstones:
    lines.append(f"| `{r['v3_name']}` | {r['reason']} |")
lines.append("")
open(OUT_MD, "w").write("\n".join(lines))

print(f"RETARGET: {len(retargets)}   TOMBSTONE: {len(true_tombstones)}")
print(f"OUT: {OUT_JSON}")
print(f"OUT: {OUT_MD}")
