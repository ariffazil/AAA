---
name: skill-drift
id: skill-drift
version: 2.0.0
description: >
  Drift detection, skill binding, and federated architecture management.
  Real-time drift detection across tool manifests, agent cards, skill registries, and runtime-injected files.
  Discover, bind, and compose skills across all federation organs using orthogonal axes.
  Design, validate, and manage skills across a multi-agent federation with 3-layer architecture.
owner: AAA
risk_tier: medium
autonomy_tier: T1
floor_scope: [F2, F3, F4, F8, F11]
tags: [drift, audit, registry, manifest, binding, architecture, federation, skill-binding, federated, F2, F11]
capability_tier: fed-long-context
ecology_state: WARM
---

# Skill Drift — Detection, Binding & Federated Architecture

> **DITEMPA BUKAN DIBERI** — Drift is invisible until it causes a bug.

## What This Skill Is

A unified skill covering three concerns:

1. **Drift Detection** — compares live state against saved baselines and reports mismatches across tool manifests, agent cards, skill registries, and runtime-injected files
2. **Skill Binding** — discover, bind, and compose skills across all federation organs using AAA_SKILL.md orthogonal axes (Trinitarian Δ/Ω/ΦΙ + Functional)
3. **Federated Architecture** — design, validate, and manage skills with 3-layer architecture, 3-axis manifests, veto-generator separation, bootstrap signing, and CI validation gates

## When to Use

- "Check drift", "verify registry", "detect manifest drift", "tool surface audit", "runtime injection detection"
- Cross-organ synthesis tasks requiring skill composition
- Subagent orchestration requiring isolation, evidence, and floor gates
- Skill surface audits, drift detection, recursive self-forge
- Designing or validating skill architecture across a multi-agent federation
- "Skill architecture", "skill registry", "skill naming", "federated registry drift"

## When NOT to Use

- Single-organ direct MCP call (use the organ's MCP directly)
- Irreversible actions without explicit 888_HOLD + F13 (T3)
- Bypassing organ lanes (GEOX is EVIDENCE_ONLY, WELL is REFLECT_ONLY, WEALTH is advisory)
- Creating a single new skill from scratch (use `skill-creator`)

## §1. DRIFT DETECTION

### Drift Dimensions

1. **Build vs Runtime Manifest Drift** — Canonical drift check via `arifOS/runtime/manifest.py` (`build_manifest` vs `runtime_manifest`)
2. **Tool Manifest Drift** — Live MCP tools vs registered tools vs agent card references
3. **Skill Registry Drift** — SKILL_ALIAS_TABLE vs actual directories vs agent card skill IDs
4. **Agent Card Drift** — Card skill IDs vs existing skill directories
5. **Schema Drift** — Tool input schemas vs documented schemas
6. **Floor Drift** — Declared floor_scope vs actual floor enforcement
7. **Verdict Taxonomy Drift** — Verdict emissions vs closed 6-value set (OBSERVE_ONLY|SEAL|SABAR|VOID|HOLD|888_HOLD)

### Detection Pipeline

1. **Snapshot** — Capture current state of all registries
2. **Compare** — Diff against saved baseline (or last-known-good)
3. **Classify** — Each mismatch: CRITICAL (breaks routing), WARNING (orphan), INFO (cosmetic)
4. **Report** — Structured drift report with fix recommendations
5. **Escalate** — CRITICAL drift → 888_HOLD before any SEAL operation

### Runtime-Injected Files

Some organ services modify files at runtime. Known patterns:
- **WELL `index.html`**: WebMCP adapter injected on service start → dirty after commit
- **arifOS session-state**: Runtime state files that change during operation

When dirty after clean commit: check if injected content was already committed → if yes, re-commit; if no, actual drift.

### Baselines

- **Canonical drift check**: `arifOS/runtime/manifest.py`
- Tool registry: `/root/arifOS/tool_registry.json`
- Agent cards: `/root/AAA/a2a-server/agent-cards/`
- Skill alias: `/root/AAA/skills/SKILL_ALIAS_TABLE.json`
- MCP surface: Live `tools/list` from each organ
- Verdict taxonomy: `arifOS/runtime/verdict.py`

## §2. SKILL BINDING

### Overview

This meta-skill provides the single entry point for any agent to interact with the federation's skill surface in a constitutionally governed way. It implements the unified contract in `/root/AAA/contracts/AAA_SKILL.md`.

### Inputs

- intent: string (natural language task)
- organs: list (optional filter: ["GEOX", "WEALTH", "WELL", "arifOS", "A-FORGE", "Hermes-Ω"])
- autonomy_tier: "T1" | "T2" | "T3"
- max_parallel: int (default 3)
- required_evidence: bool

### Procedure

1. Probe capability surfaces via arifos-mcp-federation + organ MCPs
2. Map intent to orthogonal axes (Trinitarian + Functional)
3. Retrieve candidate skills with full contracts (subagent spawn schema, evidence_required, risk_band, floor_scope)
4. Compose DAG or subagent swarm with isolation (worktree for code, container for compute)
5. Verify floors (F1 reversible-first, F7 humility, F11 audit receipt)
6. Return bound plan + evidence bundle

### Output Format

```json
{
  "orthogonal_map": {"trinitarian": "Δ|Ω|ΦΙ", "functional": ["Governance", "Evidence", ...]},
  "skills_bound": [{"id": "...", "organ": "...", "floor_scope": [...], "subagent_contract": {...}}],
  "composed_plan": "DAG or subagent list",
  "evidence_bundle": {"provenance": "...", "uncertainty": "P50: ..."},
  "floor_receipt": "F1 pass, F7 humility applied, F11 auditable",
  "escalation": "none | 888_HOLD | F13"
}
```

### Forbidden Actions

- Direct organ execution without binding + lease
- Omitting orthogonal tags or subagent contract in output
- T3 actions without 888_HOLD + F13
- Fabricating epistemic labels

## §3. FEDERATED ARCHITECTURE

### The 3-Layer Architecture

```
Layer 1: SUBSTRATE (how agents think) — always loaded, agent-agnostic
Layer 2: KNOWLEDGE (what agents know) — always loaded, veto layer
Layer 3: DOMAIN (where agents operate) — load on demand, per-agent
```

### The 3-Axis Manifest

Every skill must declare three axes:

| Axis | Question | Test |
|---|---|---|
| **Invariant** | What's timeless? | Survives tool/org changes? |
| **Bridge** | What connects? | Linked to kernel verbs + other skills? |
| **Contrast** | What is this NOT? | Clear boundaries with neighbors? |

**Anti-drift rule:** If a skill has no invariant → kill. No bridge → isolate. No contrast → merge.

### Veto-Generator Separation

- **Domain skills = GENERATOR** — produce hypotheses. Authority: ADVISORY.
- **Universal skills = VETO** — enforce boundary conditions. Authority: BINDING.
- **Sovereign = TRUTH** — ratifies axioms the framework cannot verify.

Rule: Domain generates, universal vetoes. Never invert.

### Naming Convention: `{domain}-{verb}`

All lowercase kebab-case. Max 3 words. Domain prefix mandatory.

Domains: `kernel`, `geo`, `wealth`, `well`, `forge`, `a2a`, `meta`, `mem`, `sec`, `ops`, `dev`, `research`

### CI Validation Gates

1. **manifest_schema** — validate against schema
2. **skill_hash_integrity** — recompute hashes, compare to manifest
3. **three_axis_completeness** — invariant/bridge/contrast all present
4. **dependency_acyclicity** — no circular dependencies
5. **veto_generator_separation** — substrates don't generate, domains don't veto
6. **adversarial_contradiction** — inject contradictions, verify veto catches
7. **bootstrap_self_host** — deterministic self-host test
8. **signature_present** — at least 1 valid signature
9. **skill_count_bounds** — flag if growing beyond threshold
10. **entropy_budget** — verify entropy non-increasing across boot phases

### EUREKA-ZEN Workflow: Federation-Wide Skill Lifecycle

**Phase 1 — Deep Scan & Chaos Purge:** Map ALL surfaces, identify duplicates, archive by renaming, update alias table.

**Phase 2 — Architectural Alignment:** Refactor skills to the cognitive engine that will execute them (Claude Code / Codex / Hermes).

**Phase 3 — Forge Gaps:** Cross-reference agent-card skill IDs against skills on disk. Missing = architectural gaps.

**Phase 4 — KERNEL Substrate Injection:** Every agent card must inherit arifOS baseline physics.

**Phase 5 — Seal:** Verify alias table synced, federation health green, write seal payload to VAULT999.

### Agent Loading Matrix

| Agent | Substrates | Knowledge | Domains |
|---|---|---|---|
| Full (Hermes) | 6 | 3 | research, meta, geo, wealth, well |
| Coder (Claude) | 6 | 3 | dev, forge, ops, meta |
| Metabolizer (OpenClaw) | 4 | 3 | mem, ops, a2a |
| Executor (Codex) | 6 | 3 | dev, forge, ops |
| Minimal (Kimi) | 6 | 3 | dev, forge, ops, meta, a2a |

### Three Gödelian Paradoxes

| Paradox | Mitigation |
|---|---|
| **Bootstrapping** — loader needs skills, skills need loader | Firmware primitive + signed manifest |
| **Compression** — universal ≠ derivable from domain | Veto pattern: universal constrains, domain generates |
| **Authority** — framework validates structure, not truth | External ratification: sovereign signs the truth |

### Pitfalls

1. **Same-content skills with different names** — choose FORGE-* as canonical
2. **Agent cards rot silently** — audit cards against live config monthly
3. **SKILL_ALIAS_TABLE has 3 copies** — always verify hash match
4. **Granularity gap** — registry says 64 skills but manifest has 209. Use registry for layer classification, manifest for per-agent counts
5. **Sibling-agent file conflicts** — use `skill_manage(action='patch')` for targeted edits
6. **Behavioral vs Enforcement confusion** — behavioral governance alone is "vibe-based"; enforcement layer must survive a system prompt rewrite

## Floors

- F2 TRUTH: Report only what is actually observed
- F3 PEACE: No unnecessary disruption during drift correction
- F4 CLARITY: Drift report must be actionable, not noise
- F8 GENIUS: Skill binding must optimize for capability, not convenience
- F11 AUDITABILITY: Every drift check logged with timestamp and findings
