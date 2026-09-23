#!/usr/bin/env python3
"""Capability graph generator — Phase 1 of the skill-authority re-anchor.

Machine-derived, do not hand-edit. Reads the authority (Registry V3) and the
translation layer (SKILL_ALIAS_TABLE.json v1.1.0), and emits a capability graph:
capability (V3 layer/domain) -> skill (logical short name) -> adapter (disk path,
annotated with home/view + resolvability).

Model (per Arif doctrine 2026-09-23): Capability > Skill; Skill = adapter.
"""
import json, os, sys

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML missing; cannot parse Registry V3.\n")
    sys.exit(2)

V3 = "/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml"
ALIAS = "/root/AAA/skills/SKILL_ALIAS_TABLE.json"
OUT = "/root/AAA/proposals/CAPABILITY-GRAPH-DRAFT-20260923.json"

v3 = yaml.safe_load(open(V3))
alias = json.load(open(ALIAS))
rows = alias.get("aliases", [])

# index alias rows by v3 short name (keep all related rows)
by_name = {}
for r in rows:
    by_name.setdefault(r.get("v3_name"), []).append(r)

def resolve(skill):
    """Return the adapter annotation for a logical skill name."""
    rs = by_name.get(skill)
    if not rs:
        return {"skill": skill, "adapter": "NOT_IN_ALIAS_TABLE"}
    r = rs[0]
    p = r.get("primary_path") or r.get("primary_resolved")
    exists = bool(p and os.path.exists(p))
    return {
        "skill": skill,
        "home": r.get("primary_home"),
        "status": r.get("status"),
        "path": p,
        "exists": exists,
    }

summary = {
    "capabilities": 0,
    "skills_listed": 0,
    "skills_in_alias": 0,
    "skills_not_in_alias": 0,
    "live_adapters": 0,
    "dead_adapters": 0,
    "tombstone_adapters": 0,
}

capabilities = {}
layers = v3.get("layers", {})

# universal layers
for layer in ("substrate", "knowledge"):
    body = layers.get(layer, {})
    skills = body.get("skills", [])
    entries = [resolve(s) for s in skills]
    capabilities[layer] = {"load": body.get("load"), "skills": entries}
    summary["capabilities"] += 1
    summary["skills_listed"] += len(entries)

# domain groups
domain = layers.get("domain", {})
for dom, skills in (domain.get("domains") or {}).items():
    entries = [resolve(s) for s in (skills or [])]
    capabilities["domain:" + dom] = {"skills": entries}
    summary["capabilities"] += 1
    summary["skills_listed"] += len(entries)

# tally adapter states
for cap in capabilities.values():
    for e in cap.get("skills", []):
        if e.get("adapter") == "NOT_IN_ALIAS_TABLE":
            summary["skills_not_in_alias"] += 1
            continue
        summary["skills_in_alias"] += 1
        if e.get("status", "").upper().startswith("TOMBSTONE"):
            summary["tombstone_adapters"] += 1
        elif e.get("exists"):
            summary["live_adapters"] += 1
        else:
            summary["dead_adapters"] += 1

# cross-check: total non-tombstone alias rows not referenced by V3
referenced = set()
for cap in capabilities.values():
    for e in cap.get("skills", []):
        if e.get("adapter") != "NOT_IN_ALIAS_TABLE":
            referenced.add(e["skill"])
all_non_tombstone = {r.get("v3_name") for r in rows if not r.get("tombstone")}
unreferenced = sorted(all_non_tombstone - referenced)
summary["non_tombstone_rows_not_in_v3"] = len(unreferenced)

result = {
    "generated": "2026-09-23",
    "source_registry": V3,
    "source_alias": f"{ALIAS} (v{alias.get('version')}, {alias.get('status')})",
    "model": "capability (V3 layer/domain) -> skill (logical name) -> adapter (disk path, home=view)",
    "summary": summary,
    "unreferenced_non_tombstone_skills": unreferenced,
    "capabilities": capabilities,
}

json.dump(result, open(OUT, "w"), indent=2)
print(json.dumps(summary, indent=2))
print("OUT:", OUT)
