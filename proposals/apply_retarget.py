#!/usr/bin/env python3
"""Apply verified retargets to SKILL_ALIAS_TABLE.json (SEAL-authorized 2026-09-23).

Guards (each allowlisted skill must pass ALL):
  1. skill is in the curated allowlist (semantic verification by FI-008).
  2. target path exists AND is a DIRECTORY AND contains SKILL.md (matches the
     live-row convention: 40/40 live rows are dirs).
  3. target path differs from the current primary_path (no no-op writes).

Dry-run by default. Pass --apply to write (atomic os.replace, mode preserved).
Backup already taken: SKILL_ALIAS_TABLE.json.bak-20260923-074629-seal-pre.
"""
import json, os, sys

ALIAS = "/root/AAA/skills/SKILL_ALIAS_TABLE.json"
MAPPING = "/root/AAA/proposals/NAME-MAPPING-DRAFT-20260923.json"

# Curated semantic allowlist — skill names whose rename FI-008 verified by hand.
# (8 of the 17 high-score matches were REJECTED: file targets docker.sh / receipt .md,
#  and concept mismatches well-boundary, dev-repo-audit, ops-vps, ops-mcp-builder,
#  ops-mcp-probe, ops-health, meta-skill-unification.)
ALLOWLIST = [
    # high-confidence, semantic-clean
    "geo-artifact-rigor",
    "well-readiness",
    "ops-infra",
    "ops-incident",
    "ops-spatial",
    "ops-mcp-lifeguard",
    "apex-quantum-eureka",
    "ops-google",
    "meta-skill-create",
    # medium-confidence, semantic-clean (basin/prospect/well/etc.)
    "geo-basin",
    "geo-well-tie",
    "geo-prospect",
    "dev-ci-diagnose",
    "dev-issue-triage",
    "dev-pr-governance",
    "dev-analysis",
    "ops-model-monitor",
    "ops-compress",
    "meta-skill-lint",
    "meta-plan",
    "a2a-kimi",
    "a2a-spawn",
    "research-summarize",
]

def home_of(path):
    for root, h in [
        ("/root/AAA/skills", "aaa"),
        ("/root/.agents/skills", "agents"),
        ("/root/.kimi-code/skills", "kimi"),
        ("/root/.arifos/agents/opencode/skills", "opencode"),
        ("/root/HERMES/skills", "hermes"),
        ("/root/GEOX/skills", "geox"),
        ("/root/WELL/skills", "well"),
        ("/root/WEALTH/skills", "wealth"),
        ("/root/arifOS/skills", "arifos"),
        ("/root/.codex/skills-curated", "codex"),
        ("/root/.codex/skills", "codex"),
        ("/root/.forge/skills", "forge"),
    ]:
        if path.startswith(root):
            return h
    return "aaa"

mapping = json.load(open(MAPPING))
best = {}
for tier in ("high", "medium", "low"):
    for e in mapping["confidence"][tier]:
        best[e["skill"]] = e["path"]

alias = json.load(open(ALIAS))
rows = alias["aliases"]

apply_flag = "--apply" in sys.argv
changes, skipped = [], []
for r in rows:
    name = r.get("v3_name")
    if name not in ALLOWLIST:
        continue
    target = best.get(name)
    if not target or not os.path.isdir(target) or not os.path.exists(os.path.join(target, "SKILL.md")):
        skipped.append((name, "not a DIR with SKILL.md", target))
        continue
    old = r.get("primary_path") or r.get("primary_resolved")
    if old == target:
        skipped.append((name, "no-op (already points there)", target))
        continue
    new_home = home_of(target)
    changes.append((name, old, target, new_home, r.get("primary_home")))
    if apply_flag:
        r["primary_disk_name"] = os.path.basename(target)
        r["primary_path"] = target
        r["primary_resolved"] = target
        r["primary_home"] = new_home
        r["status"] = "RESOLVED"

print(f"allowlist: {len(ALLOWLIST)} | would-apply: {len(changes)} | skipped: {len(skipped)}")
for name, old, target, nh, oh in changes:
    print(f"  RETARGET {name}: {old} -> {target}  [home {oh}->{nh}]")
for name, why, t in skipped:
    print(f"  SKIP {name}: {why}  ({t})")

if apply_flag:
    tmp = ALIAS + ".tmp"
    with open(tmp, "w") as f:
        json.dump(alias, f, indent=2)
        f.write("\n")
    os.chmod(tmp, 0o644)
    os.replace(tmp, ALIAS)
    # re-validate
    json.load(open(ALIAS))
    print(f"\nAPPLIED {len(changes)} retargets to {ALIAS}")
else:
    print("\nDRY-RUN — no write. Re-run with --apply to commit.")
