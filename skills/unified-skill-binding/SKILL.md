---
id: unified-skill-binding
name: Unified Skill Binding (Orthogonal + Cross-Organ)
version: 1.0.0
description: Discover, bind, and compose skills across all federation organs using
  AAA_SKILL_BINDING.md orthogonal axes (Trinitarian Δ/Ω/ΦΙ + Functional). Enforces
  subagent contracts, evidence gates, F1-F13. Meta-skill for agentic elevation.
owner: AAA
risk_tier: medium
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
dependencies:
  skills:
  - arifos-mcp-federation
  - skill-creator
  - arifos-recursive-audit
  servers:
  - arifos
  - geox
  - wealth
  - well
  - aforge
  tools:
  - discover
  - bind
  - compose
  - verify_floors
examples:
- Bind GEOX evidence skills + WEALTH compute for basin NPV under uncertainty
- Compose subagent swarm for FFF-loop across organs with orthogonal tags
- Audit skill surface for missing ΦΙ audit skills in 888-APEX card
tests:
- All returned skills have orthogonal tags + floor_scope
- Subagent contract present for high-risk compositions
- Evidence bundle produced with provenance to VAULT999
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Δ
  - Ω
  - ΦΙ
  functional:
  - Governance
  - Routing
  layer: HEXAGON
  autonomy_tier: T2
floor_scope:
- F2
- F3
- F4
- F8
- F11
---

# Unified Skill Binding

## Overview

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

This meta-skill provides the single entry point for any agent (grok-build, Hermes roles, FI citizens) to interact with the federation's skill surface in a constitutionally governed way. It implements the unified contract in /root/AAA/contracts/AAA_SKILL_BINDING.md.

It turns fragmented organ skills (AAA 31, GEOX ~15, WEALTH 20+, WELL 21, arifOS 13, Hermes 236 catalog, A-FORGE auto-discovered) into a composable, orthogonal, subagent-aware system.

## When to Use
- Cross-organ synthesis tasks (e.g., GEOX evidence + WEALTH valuation + WELL readiness).
- Subagent orchestration requiring isolation, evidence, and floor gates.
- Skill surface audits, drift detection, recursive self-forge.
- Any delegation that must respect Trinitarian + Functional orthogonal mapping.

## When NOT to Use
- Single-organ direct MCP call (use the organ's MCP directly).
- Irreversible actions without explicit 888_HOLD + F13 (T3).
- Bypassing organ lanes (GEOX is EVIDENCE_ONLY, WELL is REFLECT_ONLY, WEALTH is advisory).

## Inputs
- intent: string (natural language task)
- organs: list (optional filter: ["GEOX", "WEALTH", "WELL", "arifOS", "A-FORGE", "Hermes-Ω"])
- autonomy_tier: "T1" | "T2" | "T3"
- max_parallel: int (default 3)
- required_evidence: bool

## Procedure
1. Probe capability surfaces via arifos-mcp-federation + organ MCPs.
2. Map intent to orthogonal axes (Trinitarian + Functional).
3. Retrieve candidate skills with full contracts (subagent spawn schema, evidence_required, risk_band, floor_scope).
4. Compose DAG or subagent swarm:
   - Use A-FORGE ParallelPlanner + arifos-plan-dag.
   - Enforce isolation (worktree for code, container for compute).
   - Bind personas (researcher for Δ, forger for ΦΙ, etc.).
5. Verify floors (F1 reversible-first, F7 humility via godel-humility-lock, F11 audit receipt).
6. Return bound plan + evidence bundle (link to VAULT999 if sealed).

## Allowed Tools
- MCP federation discovery (arifos, geox, wealth, well, aforge)
- plan-dag, subagent-spawn (with capability_mode + isolation)
- constitutional self-audit (arifos-recursive-audit)
- skill-creator (for meta extension)
- evidence tagging + provenance tools

## Forbidden Actions
- Direct organ execution without binding + lease.
- Omitting orthogonal tags or subagent contract in output.
- T3 actions without 888_HOLD + F13.
- Fabricating epistemic labels (must come from organ or HF gold).

## Output Format
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

## Escalation Path
- Floor violation or high risk → arifOS kernel / 888-APEX.
- Irreversible or sovereign → F13 (Arif).
- Drift detected → AAA sentinel + HF contrast dataset.

## References
- contracts/AAA_SKILL_BINDING.md (full orthogonal + subagent contract spec)
- contracts/hermes-role-binding.md (polymorphic runtime)
- skills/arifos-mcp-federation/SKILL.md
- skills/arifos-plan-dag/SKILL.md
- skills/skill-creator/SKILL.md
- HF datasets (AAA gold benchmarks for floors)

**This skill is the lever for agentic elevation while keeping the constitutional spine intact.**

*Forged 2026-06-22 under grok-build autonomy.*