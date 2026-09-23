#!/usr/bin/env python3
"""Phase 2b: agentic semantic namefield mapping across ALL roots.

Indexes SKILL.md entries from: /root/AAA/skills (canonical),
/root/.config/opencode/skills, /root/HERMES/skills, /root/GEOX/skills,
/root/WEALTH/skills, /root/WELL/skills.

For each dead_adapter V3 name, scores semantic match against every disk skill.
Emits: RETARGET (best match above threshold), FLAG_REVIEW (ties/low confidence),
TOMBSTONE (no plausible match).
Read-only proposal. Does NOT mutate SKILL_ALIAS_TABLE.json.
"""
import json, os, re
from datetime import datetime, timezone
from difflib import SequenceMatcher

WORKLIST = "/root/AAA/proposals/ALIAS-RERESOLVE-WORKLIST-DRAFT-20260923.json"
OUT_JSON = "/root/AAA/proposals/ALIAS-RERESOLVE-MAPPING-v2-20260923.json"
OUT_MD = "/root/AAA/proposals/ALIAS-RERESOLVE-MAPPING-v2-20260923.md"

ROOTS = [
    "/root/AAA/skills",
    "/root/.config/opencode/skills",
    "/root/HERMES/skills",
    "/root/GEOX/skills",
    "/root/WEALTH/skills",
    "/root/WELL/skills",
]
EXCLUDE = re.compile(r"\.frozen|retired|archive|backup|\.bak")

def index_disk():
    """Return [(name, path)] for every SKILL.md across all roots."""
    out = []
    for root in ROOTS:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not EXCLUDE.search(d)]
            if "SKILL.md" in filenames:
                name = os.path.basename(dirpath)
                out.append((name, dirpath))
    return out

def tokens(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))

def score(v3, disk):
    a, b = tokens(v3), tokens(disk)
    if not a or not b: return 0.0
    # token overlap (Jaccard-ish)
    inter = a & b
    union = a | b
    tok_score = len(inter) / len(union) if union else 0.0
    # exact name bonus
    name_bonus = 1.0 if v3 == disk else 0.0
    # prefix family bonus (geo->geox, forge, well, wealth, meta, ops, dev, research, a2a, kernel)
    prefix_a = v3.split("-")[0]
    prefix_b = disk.split("-")[0]
    prefix_bonus = 0.2 if prefix_a == prefix_b else 0.0
    # family transform: geo->geox counts
    if prefix_a == "geo" and disk.startswith("geox"): prefix_bonus = 0.2
    # substring containment bonus
    sub_bonus = 0.0
    for t in a:
        if len(t) > 3 and t in disk.lower(): sub_bonus += 0.05
    seq = SequenceMatcher(None, v3.lower(), disk.lower()).ratio()
    return min(1.0, tok_score * 0.5 + name_bonus * 0.3 + prefix_bonus + sub_bonus + seq * 0.3)

THRESHOLD = 0.45
wl = json.load(open(WORKLIST))
rows = wl.get("worklist", [])
disk = index_disk()
print(f"indexed {len(disk)} SKILL.md across {len(ROOTS)} roots")

results = {"RETARGET": [], "FLAG_REVIEW": [], "TOMBSTONE": [], "other": []}

for r in rows:
    v3 = r.get("skill") or r.get("v3_name")
    verdict = r.get("verdict")
    if verdict not in ("TOMBSTONE", "FLAG_REVIEW", "FLAG_PHANTOM", "CREATE_ROW"):
        results["other"].append(r); continue

    scored = []
    for name, path in disk:
        s = score(v3, name)
        if s > 0.0:
            scored.append((s, name, path))
    scored.sort(reverse=True)

    if not scored:
        results["TOMBSTONE"].append({"v3_name": v3, "orig_verdict": verdict, "reason": "no plausible disk match"})
        continue
    top = scored[:3]
    best_score, best_name, best_path = top[0]
    # ties: second is within 0.02 of first
    tie = len(top) > 1 and (top[1][0] - top[0][0]) > -0.02

    if best_score >= THRESHOLD and not tie:
        results["RETARGET"].append({
            "v3_name": v3, "target_disk_name": best_name, "target_path": best_path,
            "score": round(best_score, 3), "orig_verdict": verdict,
        })
    elif best_score >= THRESHOLD and tie:
        results["FLAG_REVIEW"].append({
            "v3_name": v3, "orig_verdict": verdict,
            "candidates": [{"name": n, "path": p, "score": round(s,3)} for s, n, p in top],
        })
    else:
        results["TOMBSTONE"].append({"v3_name": v3, "orig_verdict": verdict, "reason": f"best score {round(best_score,3)} < {THRESHOLD}"})

result = {
    "generated": datetime.now(timezone.utc).isoformat(),
    "phase": "2b-semantic-namefield-mapping",
    "mode": "proposal-only / read-only",
    "threshold": THRESHOLD,
    "indexed_skills": len(disk),
    "counts": {k: len(v) for k, v in results.items()},
    "results": results,
}
json.dump(result, open(OUT_JSON, "w"), indent=2)

md = [f"# ALIAS RERESOLVE — Semantic Namefield Mapping v2", ""]
md.append(f"Generated: {result['generated']}")
md.append(f"Indexed: {len(disk)} SKILL.md · Threshold: {THRESHOLD}")
md.append("")
for k in ("RETARGET", "FLAG_REVIEW", "TOMBSTONE"):
    md.append(f"## {k} ({len(results[k])})")
    md.append("")
    for r in results[k]:
        if k == "RETARGET":
            md.append(f"- `{r['v3_name']}` → `{r['target_disk_name']}` (score {r['score']}) — `{r['target_path'].replace('/root/AAA/skills/','')}`")
        elif k == "FLAG_REVIEW":
            cands = ", ".join(f"`{c['name']}` ({c['score']})" for c in r["candidates"])
            md.append(f"- `{r['v3_name']}` — tie: {cands}")
        else:
            md.append(f"- `{r['v3_name']}` — {r.get('reason','')}")
    md.append("")
open(OUT_MD, "w").write("\n".join(md))
print(json.dumps(result["counts"], indent=2))
print(f"OUT: {OUT_JSON}")
print(f"OUT: {OUT_MD}")
