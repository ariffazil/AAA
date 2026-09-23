#!/usr/bin/env python3
"""Phase 3: Apply musyawarah-resolved mapping to SKILL_ALIAS_TABLE.json.

Per sovereign "B A" directive:
  B = musyawarah resolved FLAG_REVIEW (42 rows → 24 RETARGET + 18 TOMBSTONE)
  A = apply canonical write

Safety: backup original, atomic write (tmp+rename), round-trip verify.
"""
import json, shutil, os, tempfile
from datetime import datetime, timezone

ALIAS = "/root/AAA/skills/SKILL_ALIAS_TABLE.json"
BACKUP = "/root/AAA/skills/SKILL_ALIAS_TABLE.backup-20260923-pre-reresolve.json"
OUT = ALIAS  # canonical, in-place with backup

# ---- RETARGET rows (55 total = 31 Phase-2d + 24 musyawarah-resolved) ----
# Phase-2d 31 (from ALIAS-RERESOLVE-MAPPING-FINAL-20260923.json)
p2d = json.load(open("/root/AAA/proposals/ALIAS-RERESOLVE-MAPPING-FINAL-20260923.json"))
retarget_31 = {r["v3_name"]: r["target_path"] for r in p2d["results"]["RETARGET"]}

# Musyawarah-resolved 24 (from constitutional ruling; paths verified on disk)
retarget_24 = {
    "FORGE-mcp-federation-ops": "/root/AAA/skills/FORGE-federation-manifest",
    "youtube-extraction-datacenter-ip": "/root/AAA/skills/media/youtube-eureka",
    "WELL-boundary-sense": "/root/AAA/skills/forge-well-boundary-repair",
    "a2a-spawn": "/root/AAA/skills/a2a-task-delegator",
    "dev-issue-triage": "/root/AAA/skills/forge-issue-triage",
    "dev-pr-governance": "/root/AAA/skills/engineering/pr-governance",
    "meta-plan": "/root/AAA/skills/agi-plan-dag",
    "ops-health": "/root/AAA/skills/core/governance/verify-runtime",
    "ops-mcp-probe": "/root/.config/opencode/skills/FORGE-mcp-probe",
    "AUDIT-post-seal-sweep": "/root/AAA/skills/substrate/audit-seal",
    "CLAIM-receipt-v1": "/root/AAA/skills/domains/general/court/court-audit/claim-receipt-discipline",
    "CLAIM-verification-gate": "/root/AAA/skills/domains/general/court/court-audit/synthesis-verification-gate",
    "kernel-eureka": "/root/AAA/skills/APEX-quantum-eureka",
    "meta-atlas": "/root/AAA/skills/meta-mesa",
    "meta-rsi": "/root/AAA/skills/rsi-federation-mesh",
    "meta-rsi-audit": "/root/AAA/skills/core/governance/recursive-audit",
    "meta-skill-create": "/root/AAA/skills/.system/skill-creator",
    "meta-skill-lint": "/root/AAA/skills/skill-mesh",
    "meta-skill-unification": "/root/HERMES/skills/AGI-skill-unification",
    "ops-infra": "/root/AAA/skills/forge-infra-guardian",
    "ops-model-monitor": "/root/AAA/skills/forge-model-monitor",
    "ops-spatial": "/root/AAA/skills/forge-spatial-grounding",
    "ops-vps": "/root/AAA/skills/engineering/vps-ops",
    "research-summarize": "/root/AAA/skills/asi-summarize",
}

# Merge: musyawarah ruling wins over Phase-2d when same name
merged_retarget = dict(retarget_31)
merged_retarget.update(retarget_24)

# ---- TOMBSTONE rows (61 total = 43 Phase-2d + 18 musyawarah) ----
tomb_43 = {r["v3_name"] for r in p2d["results"]["TOMBSTONE"]}
tomb_18 = {
    # RATIFIED-8
    "AGI-prospect-maturation", "ASI-knowledge-writeback", "FORGE-init-intent-classify",
    "FORGE-search", "FORGE-seek", "FORGE-grok-profile", "WELL-somatic-kernel", "kernel-superposition",
    # RULED-10
    "FORGE-phase-escalation", "forge-exec", "forge-verbs", "meta-evals", "meta-rsi-cool",
    "meta-trust-map", "ops-transport", "research-search", "mcp-context-compression", "ops-incident",
}
merged_tombstone = tomb_43 | tomb_18
# Remove any overlap (RETARGET wins)
merged_tombstone -= set(merged_retarget.keys())

def home_of(path):
    if "/root/GEOX/skills" in path: return "geox"
    if "/root/WEALTH/skills" in path: return "wealth"
    if "/root/WELL/skills" in path: return "well"
    if "/root/.config/opencode/skills" in path: return "opencode"
    if "/root/HERMES/skills" in path: return "hermes"
    return "aaa"

def rel(path):
    return path.replace("/root/AAA/skills/", "")

# ---- load canonical, backup, mutate ----
data = json.load(open(ALIAS))
shutil.copy2(ALIAS, BACKUP)
aliases = data.get("aliases", [])
print(f"original rows: {len(aliases)}")

applied_retarget = 0
applied_tombstone = 0
seen = set()

for row in aliases:
    v3 = row.get("v3_name")
    seen.add(v3)
    if v3 in merged_retarget:
        p = merged_retarget[v3]
        row["primary_disk_name"] = os.path.basename(p)
        row["primary_path"] = p
        row["primary_resolved"] = p
        row["primary_home"] = home_of(p)
        row["related"] = [{"name": os.path.basename(p), "path": p, "home": home_of(p)}]
        row["status"] = "RETARGETED"
        row["tombstone"] = False
        row["restored_live"] = True
        applied_retarget += 1
    elif v3 in merged_tombstone:
        row["status"] = "TOMBSTONED"
        row["tombstone"] = True
        row["restored_live"] = False
        applied_tombstone += 1

# New rows for any v3 not already present
for v3, p in merged_retarget.items():
    if v3 in seen: continue
    aliases.append({
        "v3_name": v3,
        "layer": "unclassified",
        "primary_disk_name": os.path.basename(p),
        "primary_path": p,
        "primary_resolved": p,
        "primary_home": home_of(p),
        "related": [{"name": os.path.basename(p), "path": p, "home": home_of(p)}],
        "status": "RETARGETED",
        "tombstone": False,
        "restored_live": True,
        "created_by": "musyawarah-20260923",
    })
    applied_retarget += 1

for v3 in merged_tombstone:
    if v3 in seen: continue
    aliases.append({
        "v3_name": v3,
        "layer": "unclassified",
        "primary_disk_name": None,
        "primary_path": None,
        "primary_resolved": None,
        "primary_home": None,
        "related": [],
        "status": "TOMBSTONED",
        "tombstone": True,
        "restored_live": False,
        "created_by": "musyawarah-20260923",
    })
    applied_tombstone += 1

data["version"] = "1.2.0"
data["status"] = "SEALED_TABLE_AUDITED_RENAMED_RERESOLVED_20260923"
data["rereshape_audit"] = {
    "applied_at": datetime.now(timezone.utc).isoformat(),
    "applied_by": "333-AGI (Class B, sovereign 'B A' directive)",
    "musyawarah_peers": ["333-AGI (Architect)", "555-ASI (Auditor)", "888-APEX (Constitutional Ruling, materialized by 333-AGI)"],
    "retarget_count": applied_retarget,
    "tombstone_count": applied_tombstone,
    "source_artifacts": [
        "/root/AAA/proposals/ALIAS-RERESOLVE-MAPPING-FINAL-20260923.json",
        "/root/AAA/proposals/ALIAS-MUSYAWARAH-CONSTITUTIONAL-RULING-20260923.md",
        "/root/AAA/proposals/ALIAS-MUSYAWARAH-AUDITOR-POSITION-20260923.md",
        "/root/AAA/proposals/ALIAS-MUSYAWARAH-ARCHITECT-POSITION-20260923.md",
    ],
    "backup": BACKUP,
}
data["aliases"] = aliases

# ---- atomic write ----
tmp = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json", dir="/root/AAA/skills")
json.dump(data, tmp, indent=2)
tmp.flush(); os.fsync(tmp.fileno()); tmp.close()
os.replace(tmp.name, ALIAS)

# ---- round-trip verify ----
rt = json.load(open(ALIAS))
rt_aliases = rt["aliases"]
n_retarget = sum(1 for a in rt_aliases if a.get("status") == "RETARGETED")
n_tombstone = sum(1 for a in rt_aliases if a.get("status") == "TOMBSTONED")
n_other = len(rt_aliases) - n_retarget - n_tombstone
print(f"applied RETARGET: {applied_retarget} (verify {n_retarget})")
print(f"applied TOMBSTONE: {applied_tombstone} (verify {n_tombstone})")
print(f"untouched rows: {n_other}")
print(f"total rows: {len(rt_aliases)}")
print(f"backup: {BACKUP}")
assert os.path.isfile(BACKUP), "backup missing!"
assert n_retarget == applied_retarget, "round-trip mismatch retarget"
assert n_tombstone == applied_tombstone, "round-trip mismatch tombstone"
print("ROUND-TRIP VERIFY: PASS")
