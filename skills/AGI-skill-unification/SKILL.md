---
name: AGI-skill-unification
description: >
  Multi-harness skill catalog unity — AAA catalog, Grok/Claude/Codex views, alias table (V3 short→disk),
  mesh-sync, BOOT gate, Hermes bridge. Load when auditing skill mesh, resolving dual names, rebinding
  harness skills, or before claiming skill inventory complete.
version: 1.0.1
owner: AAA / F13 SOVEREIGN
risk_tier: low
autonomy_tier: T1
floor_scope: [F2, F4, F11]
tags: [aaa, meta, skills, mesh, grok, unification, alias]
forged: 2026-07-12
updated: 2026-07-15
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
| Alias table (133 rows: 104 active + 29 tombstone) | `/root/AAA/skills/SKILL_ALIAS_TABLE.json` |
| Mesh sync | `/root/AAA/skills/scripts/skill-mesh-sync.sh` |
| V3 registry (64 logical) | `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml` |
| Meta atlas | `AUDIT-skill-atlas` |
| Historical receipt | `/root/AAA/skills/docs/SKILL-UNIFICATION-COMPLETE-2026-07-12.md` |
| Current receipt | `/root/forge_work/2026-07-15/AAA-SKILL-TOOL-RECONCILIATION.json` |
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

1. `skill-mesh-sync.sh --check` exits 0.  
2. V3 logical count is 64; alias rows remain separately classified as active or tombstone/history.  
3. No live primary resolves through a tombstone row.  
4. No source-less broken alias remains active; quarantine instead of fabricating a body.  
5. Harness-native keepers remain real directories and profile views match their declared packs.  
6. `AUDIT-skill-atlas` §0 points to a dated live receipt.  

## Bounded Independent Audit Protocol

Subagents are optional, scope-bounded evidence collectors. They do not inherit authority, cannot validate one another recursively, and never replace a live source-of-truth probe.

### Use

```python
# Split only independent questions with explicit evidence contracts:
task(description="Audit registry semantics", subagent_type="auditor", prompt="Return file paths, counts, and contradictions only.")
task(description="Check runtime health", subagent_type="ops", prompt="Return live endpoints, status, and timestamp only.")
```

### Rules

1. Route uncertainty to the owning evidence source first: filesystem, live MCP registry, VAULT999, or the correct domain organ.
2. Spawn only when scopes are independent and the handoff cost is lower than direct inspection.
3. Do not ask one model to recursively agree with copies of itself; that is consensus theatre, not external witness.
4. The root agent compares evidence, labels contradictions/UNKNOWNs, and stops when the verification criterion is met.
5. Irreversible SEAL still requires the real human/external witness path; agent count never raises authority.

### Pre-seal evidence flow

```
ROOT AGENT → live source probes + optional bounded independent audits
           → compare evidence and contradictions
           → arif_judge
           → human/external witness if required
```

### Gates

- All spawned tasks are time-limited and read-only unless separately authorized.
- F1 AMANAH: parent worktree and execution state are not mutated by auditors.
- F11 AUDIT: each audit returns paths, timestamps, commands/tools, and pass criteria.
- F13 SOVEREIGN: no agent or ensemble self-grants irreversible authority.

## Companion

Load **`AUDIT-skill-atlas`** for routing and gap detection. This skill is the ops contract for unity.
