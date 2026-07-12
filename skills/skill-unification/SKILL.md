---
name: skill-unification
description: >
  Multi-harness skill catalog unity — AAA catalog, Grok/Claude/Codex views, alias table (V3 short→disk),
  mesh-sync, BOOT gate, Hermes bridge. Load when auditing skill mesh, resolving dual names, rebinding
  harness skills, or before claiming skill inventory complete.
version: 1.0.0
owner: AAA / F13 SOVEREIGN
risk_tier: low
autonomy_tier: T1
floor_scope: [F2, F4, F11]
tags: [aaa, meta, skills, mesh, grok, unification, alias]
forged: 2026-07-12
updated: 2026-07-12
---

# Skill Unification — AAA Catalog × Harness Views

## Iron rule

**AAA is the catalog. Harnesses are views.**  
Doctrine bodies may live under `/root/AAA/skills` *or* `/root/.agents/skills` (doctrine_core).  
Do not invent a second Grok-only catalog.

## Always load first (BOOT gate)

`AAA/skills/BOOTSTRAP_MANIFEST.json` — 9 universals (substrate + knowledge) through READY, then domain skills.

## Canonical artifacts (AAA)

| Artifact | Path |
|----------|------|
| Alias table (63/63) | `/root/AAA/skills/SKILL_ALIAS_TABLE.json` |
| Mesh sync | `/root/AAA/skills/scripts/skill-mesh-sync.sh` |
| V3 registry | `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml` |
| Meta atlas | `meta-mesa-skill-atlas` (this organ’s sister skill) |
| Complete receipt | `/root/AAA/skills/docs/SKILL-UNIFICATION-COMPLETE-2026-07-12.md` |
| Hermes bridge | `/root/A-FORGE/forge_work/2026-07-12/HERMES-V3-DOMAIN-BRIDGE.md` |

## Resolve a V3 short name

```bash
python3 -c "import json;d=json.load(open('/root/AAA/skills/SKILL_ALIAS_TABLE.json'));
print([a for a in d['aliases'] if a['v3_name']=='meta-atlas'][0])"
```

Prefer `primary_path` / `primary_resolved`. Never invent paths from short names alone.

## Mesh hygiene

```bash
# dry-run
bash /root/AAA/skills/scripts/skill-mesh-sync.sh
# apply missing links (Grok natives preserved)
bash /root/AAA/skills/scripts/skill-mesh-sync.sh --apply
# CI / pre-seal
bash /root/AAA/skills/scripts/skill-mesh-sync.sh --check
```

Harnesses synced: `~/.grok/skills`, `~/.claude/skills`, `~/.codex/skills`.

## Grok native keepers (not AAA bodies)

`arif-governed-autonomous-execution` · `grok-zen-aaa-substrate` · `grok-federation-skill-upgrader` · `orthogonal-skill-update` · `create-skill` · `check-work` · `help` · `imagine`

Pruned: `docx` `pptx` `xlsx` `code-review` → `~/.grok/skills/.deprecated/`

## Pre-seal checklist

1. `skill-mesh-sync.sh --check` exit 0  
2. Alias `resolved == v3_mapped == 63` and `unresolved == []`  
3. No live `TOMBSTONE.json` on V3 primaries (use `RESTORED_LIVE.json` if re-hydrated)  
4. Grok office skills not live top-level  
5. meta-mesa §0 matches live maturity  

## Companion

Load **`meta-mesa-skill-atlas`** for routing and gap detection. This skill is the **ops contract** for unity.
