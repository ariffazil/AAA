---
name: skill-inventory
id: skill-inventory
version: 2.0.0
description: >
  Unified skill inventory, audit, mesh health, and cross-surface contrast.
  Multi-surface skill audit (10 agent homes) with cross-surface contrast, drift/orphan/dual-name detection.
  Check whether every agent in the federation has the same core skills at the same version.
  Multi-harness skill catalog unity — AAA catalog, Grok/Claude/Codex views, alias table, mesh-sync, BOOT gate.
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F2, F4, F7, F9, F11]
tags: [meta, skill-atlas, gap-detection, routing, federation, inventory, multi-harness, audit, mesh, sync, version, divergence, unification, alias]
capability_tier: fed-long-context
ecology_state: WARM
---

# Skill Inventory — Unified Audit, Atlas, Mesh Health & Unification

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.
> **The mesa above the terrain. See the whole. Find the missing. Route the right.**

## What This Skill Is

This is the **meta-skill** — a skill about skills. It provides:

1. **Inventory** — live multi-surface counts (not a frozen number)
2. **Gap detection** — missing, thin, dual-named, harness-divergent
3. **Routing** — given a task *and harness*, which skill(s) to load
4. **Health scoring** — freshness, collision, catalog vs view drift
5. **Cross-harness unification** — AAA catalog ↔ CLI agent views
6. **Mesh sync** — per-skill SYNC / DIVERGED / MISSING_FROM_X status
7. **Cross-surface contrast** — 10-agent audit with rot classification

It does NOT execute, judge, or seal. It classifies, routes, and illuminates.

**Iron rule:** AAA is the catalog. Harnesses are views. Do not invent parallel catalogs.

## When to Use

- Reviewing the overall capabilities, naming conventions, and performance of the active skill portfolio
- A new skill is drafted or proposed for installation
- An existing skill's SKILL.md is updated or modified
- Executing portfolio maintenance checks to clean up outdated APIs, dead links, or legacy documentation
- Tuning the triggering accuracy of skills when experiencing trigger drift
- Answering "are my agents in sync right now?"
- Auditing skill mesh, resolving dual names, rebinding harness skills
- Before claiming skill inventory is complete

## When NOT to Use

- Creating a single new skill from scratch (use `skill-creator`)
- Linting individual skill trigger statements (use `skill-creator` linter mode)
- The task is a general system performance audit unrelated to skills

## §0. MULTI-HARNESS UNIFICATION

### Architecture

```
BOOTSTRAP_MANIFEST (9 universals)     ← always first
        ↓
AAA/skills  (catalog + V3 registry)   ← sole named truth
   +  .agents/skills (doctrine/stage) ← shared federation core
        ↓ symlink mesh
~/.grok | ~/.claude | ~/.codex        ← views (+ harness-native)
        ↓ separate trees
Hermes categories | Kimi roles | OpenClaw owned
```

### Live inventory (OBSERVED)

| Surface | Count | Role |
|---------|-------|------|
| AAA `${AAA_HOME:-/root/AAA}/skills` | ~108 active bodies | **Catalog**; archives excluded |
| V3 registry | 64 logical | Short-name registry |
| Alias table | 133 rows | 104 active + 29 tombstone |
| `.agents/skills` | ~130 active bodies | Stage/domain doctrine |
| Grok `~/.grok/skills` | ~184 resolvable | View + native keepers |
| Claude / Codex / OpenCode | ~176 / 56 / 39 | Mesh/profile views |
| Kimi | ~7 | Role contrast/RSI skills |

### Canonical artifacts

| Artifact | Path |
|----------|------|
| Alias table | `${AAA_HOME:-/root/AAA}/skills/SKILL_ALIAS_TABLE.json` |
| Mesh sync | `${AAA_HOME:-/root/AAA}/skills/scripts/skill-mesh-sync.sh` |
| V3 registry | `${AAA_HOME:-/root/AAA}/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml` |
| Historical receipt | `${AAA_HOME:-/root/AAA}/skills/docs/SKILL-UNIFICATION-COMPLETE-2026-07-12.md` |
| Current receipt | `${FORGE_WORK:-/root/forge_work}/2026-07-15/AAA-SKILL-TOOL-RECONCILIATION.json` |
| Hermes bridge | `${AFORGE_HOME:-/root/A-FORGE}/forge_work/2026-07-12/HERMES-V3-DOMAIN-BRIDGE.md` |

### Resolve a V3 short name

```bash
python3 -c "import json;d=json.load(open('${AAA_HOME:-/root/AAA}/skills/SKILL_ALIAS_TABLE.json'));
print([a for a in d['aliases'] if a['v3_name']=='meta-atlas'][0])"
```

### Mesh hygiene

```bash
# dry-run
bash ${AAA_HOME:-/root/AAA}/skills/scripts/skill-mesh-sync.sh
# apply missing links
bash ${AAA_HOME:-/root/AAA}/skills/scripts/skill-mesh-sync.sh --apply
# CI / pre-seal
bash ${AAA_HOME:-/root/AAA}/skills/scripts/skill-mesh-sync.sh --check
```

### BOOT gate

```
BIND → GROUND → ROUTE → RECALL → VERIFY → SEAL → KNOW → READY
```

Only after **READY** may domain skills load.

## §1. CROSS-SURFACE INVENTORY (10 Surfaces)

| # | Surface | Path | Type |
|---|---------|------|------|
| 1 | AAA canonical | `/root/AAA/skills/` | SOT |
| 2 | kimi | `/root/.kimi-code/skills/` | copy |
| 3 | opencode | `/root/.arifos/agents/opencode/skills/` | symlink |
| 4 | grok | `/root/.grok/skills/` | symlink |
| 5 | claude | `/root/.claude/skills/` | symlink |
| 6 | codex | `/root/.codex/skills/` | symlink |
| 7 | hermes | `/root/.hermes/skills/` | copy |
| 8 | hermes-asi | `/usr/local/lib/hermes-agent/skills/` | copy |
| 9 | openclaw-ws | `/root/.openclaw/workspace/skills/` | copy |
| 10 | openclaw-bundled | bundled | built-in |

### Cross-surface compare

```bash
# Dump each surface
comm -23 <(ls /root/AAA/skills/ | sort) <(ls /root/.kimi-code/skills/ | sort)   # orphans: AAA has, kimi lacks
comm -13 <(ls /root/AAA/skills/ | sort) <(ls /root/.kimi-code/skills/ | sort)   # drift: kimi has, AAA lacks
```

### Classification Matrix

| Verdict | Condition | Action |
|---------|-----------|--------|
| ✅ PROMOTE | kimi/agent has it, AAA lacks, universal | Copy to AAA, register V3, add alias |
| 📦 ARCHIVE | agent has it, AAA has better version | Move to `_retired/<date>/` |
| 🔧 HARNESS-NATIVE | agent-specific | OK — don't promote |
| 🔲 NEED MIRROR | AAA has it, agent lacks | Copy/symlink to agent |
| ⚠️ DUAL-NAME | Same skill, different names | Alias table entry or symlink |
| ☠️ VOID | Zero invocations, zero evidence | SKILL.md → SKILL.md.VOID |

## §2. MESH SYNC PROTOCOL

### Compare command

```bash
find /root/AAA/skills /root/.hermes/skills /root/.kimi-code/skills -maxdepth 2 -name 'SKILL.md' | xargs grep '^version:' | sort
```

**PITFALL:** `-maxdepth 1` returns empty on this mesh — skill dirs nest one level deep. Use `-maxdepth 2`.

### Health report format

```
skill_name | AAA_version | hermes_version | kimi_version | status
```

### Status values

| Status | Meaning |
|--------|---------|
| `SYNC` | Present in all trees, same version |
| `DIVERGED` | Present in ≥2 trees with different versions |
| `MISSING_FROM_X` | Absent from tree X but present in AAA |

### Escalation protocol

| Detection | Action | Owner |
|---|---|---|
| `DIVERGED` | Flag — log the row | AUDIT agent |
| `DIVERGED` > 3 sessions | Fix — align to AAA version | A-FORGE |
| `MISSING_FROM_X` | Propagate from AAA | A-FORGE |
| `MISSING_FROM_aaa` | Flag + reverse-propagate | AUDIT → A-FORGE |

## §3. ROT CLASSIFICATION

| Rot Class | Description |
|-----------|-------------|
| `doc-rot` | References external URLs/paths no longer accessible |
| `api-rot` | SDK/CLI packages past compatibility versions |
| `trigger-rot` | Triggering criteria overlap with other skills |
| `unused-rot` | No telemetry execution within threshold |
| `archive-void-rot` | Physically archived but still discoverable |
| `drift-rot` | Exists on agent surface but NOT in AAA (or vice versa) |
| `dual-name-rot` | Same skill has different names across surfaces |

### Age thresholds

| Days Since Forge | Status | Action |
|-----------------|--------|--------|
| 0-7 | FRESH | No action |
| 8-14 | CURRENT | Review on next session |
| 15-30 | AGING | Verify references still valid |
| 30+ | STALE | Audit needed, consider archive or refresh |

## §4. ROUTING TABLE

| Intent Pattern | Skill to Load |
|---------------|---------------|
| "seismic" / "well log" / "petrophysics" / "basin" | `geox-constitution` + domain geox-* |
| "NPV" / "IRR" / "capital" / "investment" | `wealth-capital-thermodynamics` |
| "sleep" / "fatigue" / "vitality" / "dignity" | `well-substrate-readiness` |
| "build MCP tool" / "forge tool" | `mcp-mastery` |
| "GitHub PR" / "CI broken" / "issue triage" | `github-operations` |
| "create a skill" / "new skill" | `skill-creator` |
| "what skill should I load" / "skill gap" | **THIS SKILL** |

## §5. HEALTH SCORING

### Per-skill health check

```python
skill_health = {
    "name": str, "version": str, "forged_date": str,
    "days_since_forge": int, "references_count": int,
    "phantom_refs": int, "has_prompt": bool, "has_test": bool,
    "organ_coverage": float,
}
```

## §6. ANTI-PATTERNS

| Anti-Pattern | Remedy |
|-------------|--------|
| Copy skill bodies into every `~/.X/skills` | Symlink to AAA / .agents |
| Second "Grok catalog" of 100+ natives | Keep ≤12 harness keepers |
| Route by V3 short name without path | Resolve via alias table |
| Trust frozen counts | Re-probe disk |
| Skill overload (5+ for simple task) | Use this meta-skill for minimum set |
| Phantom reliance | Run gap register and forge missing |
| Stage skipping | Always start with 000-init |

## §7. PRE-SEAL CHECKLIST

1. `skill-mesh-sync.sh --check` exits 0
2. V3 logical count is 64; alias rows separately classified
3. No live primary resolves through a tombstone row
4. No source-less broken alias remains active
5. Harness-native keepers remain real directories
6. This skill points to a dated live receipt

## §8. INDEPENDENT VERIFICATION LANE (WAJIB 2)

A-FORGE planning, execution, AND verification in the same trust chain is a **primary substrate defect**. The required separation:

```
A-FORGE executes mutation
    ↓
Independent observe-lane verifier reads resulting reality
    ↓
Kernel checks evidence against original success criteria
    ↓
Only then may completion be recorded to VAULT999
```

### Verifier hard rules

The verifier MUST:
- NOT have performed the mutation
- Use independently obtained state
- Receive original success criteria, NOT executor's rewritten summary
- Be unable to modify the state it is checking
- Return: VERIFIED, MISMATCH, INCONCLUSIVE, or STALE
- NEVER issue constitutional approval — only the kernel may SEAL

### Kernel rejection rules

The kernel MUST reject "completion" when:
- Verifier identity == executor identity
- Evidence originated ONLY from the executor
- Verifier had mutation permission over the target
- Evidence is older than freshness_requirement
- Original success criteria are missing
- Results cannot be independently reproduced

## §9. BOUNDED INDEPENDENT AUDIT PROTOCOL

Subagents are optional, scope-bounded evidence collectors. They do not inherit authority, cannot validate one another recursively, and never replace a live source-of-truth probe.

### Rules

1. Route uncertainty to the owning evidence source first
2. Spawn only when scopes are independent and handoff cost < direct inspection
3. Do not ask one model to recursively agree with copies of itself
4. The root agent compares evidence, labels contradictions/UNKNOWNs
5. Irreversible SEAL still requires real human/external witness path

## References

- `contracts/AAA_SKILL.md` — full orthogonal + subagent contract spec
- `contracts/HERMES_ROLE.md` — polymorphic runtime
- `BOOTSTRAP_MANIFEST.json` — signed manifest with 9 skills
- `FEDERATED_SKILLS_REGISTRY_V3.yaml` — 64 canonical skills
- `SKILL_ALIAS_TABLE.json` — 133 rows (104 active + 29 tombstone)
