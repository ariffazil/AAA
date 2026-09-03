#!/bin/bash
# E3E Skill-Mesh Divergence Harness — 888-APEX E3E protocol, forged 2026-09-04
# Usage:
#   e3e_skill_mesh.sh emit     -> print the 5 E3E prompts (dispatch to each CCC agent)
#   e3e_skill_mesh.sh tally d/ -> tally divergence from result files d/<agent>.txt
set -u
case "${1:-emit}" in
emit)
cat <<'PROMPTS'
[E3E-001 DISCOVERY] List: (1) AAA canonical skill count (2) GEOX skills (3) WEALTH skills (4) WELL skills. For each: owner_org, canonical_home, source. No guessing — UNKNOWN if unavailable.
[E3E-002 GEOX] Use geox-prospect-evaluation. Evaluate POS=0.25, EMV=50 MMUSD, Cost=10 MMUSD. Return: workflow discovered, source location, output. No guessing.
[E3E-003 MULTIMODAL] Need image generation. Before any endpoint: query federation route, return invocation contract, endpoint selected, fallback chain. Do not call endpoint directly.
[E3E-004 OPENCLAW] Locate wealth-capital-primitives. Return owner, canonical path, mesh path, invocation path. Do not search local-only copies.
[E3E-005 FEDERATION] Generate a prospect evaluation report: discover skill, verify owner, execute workflow, produce result, return skill receipt. Report skill used, owner_org, discovery path, execution path, final output. UNKNOWN if missing.
PROMPTS
;;
tally)
DIR="${2:?result dir with <agent>.txt files}"
python3 - "$DIR" <<'PY'
import sys, os, re, collections
d = sys.argv[1]
agents = [f[:-4] for f in os.listdir(d) if f.endswith(".txt")]
print(f"agents={len(agents)}: {agents}")
excluded = []
# Divergence proxy: unique first-line answers per E3E-001 block
answers = collections.defaultdict(set)
for a in agents:
    txt = open(os.path.join(d, a + ".txt")).read()
    m = re.search(r"E3E-001(.*?)(E3E-002|$)", txt, re.S)
    if m:
        nums = re.findall(r"(\d+)\s*(?:skills|canonical|$)", m.group(1))[:4]
        answers["discovery_counts"].add(tuple(nums))
    # GUARD 2026-09-04 FI-008: error stubs are NOT answers. Classify corpses
    # (billing 402/429, config errors, trust prompts, tiny outputs) as EXCLUDED
    # so "didn't run" never counts as cognitive divergence.
    ERR_SIGNS = ("payment required", "balance exhausted", "credits are depleted",
                 "unrecognized_model", "not running in a trusted directory",
                 "--skip-git-repo-check", "reached max turns", "resource_exhausted")
    body = txt.lower()
    if len(txt) < 1500 or any(s in body for s in ERR_SIGNS):
        excluded.append(a); continue
    for skill in ("geox-prospect-evaluation", "wealth-capital-primitives"):
        if skill in txt: answers[skill].add("found")
        else: answers[skill].add("missing")
print(f"answered={len(agents)-len(excluded)} excluded_as_error_stubs={len(excluded)}: {excluded}")
for k, v in answers.items():
    print(f"{k}: {len(v)} variant(s) -> {'CONVERGENT' if len(v)==1 else 'DIVERGENT'} {sorted(v)[:3]}")
PY
;;
*) echo "usage: $0 emit | tally <dir>";;
esac
