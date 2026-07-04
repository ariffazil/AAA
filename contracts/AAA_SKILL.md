# AAA_SKILL_BINDING — Unified Constitutional Skill Binding Contract

**Forged:** 2026-06-22 (autonomous by grok-build per Arif directive + 333-AGI synthesis)  
**Version:** 1.0.0  
**Status:** Canonical for AAA control plane  
**Aligned with:** arifOS F1–F13, orthogonal mapping (Trinitarian Δ/Ω/ΦΙ + Functional axes), Adat Agentik, Ditempa Bukan Diberi  
**Scope:** All federation organs (AAA, arifOS, A-FORGE, GEOX, WEALTH, WELL, Hermes roles, HF datasets)

## 1. Purpose

This contract unifies skill definitions, bindings, and visibility across the federation so that:
- Every organ declares its skills with orthogonal tags.
- AAA cockpit and A2A gateway have a single source for discovery, binding, and governance.
- Subagents, workflows, and MCP federation respect constitutional gates.
- Skills evolve from "tool wrappers" to first-class, evidence-gated, recursive, meta-capable playbooks.

Current state (pre-forge): Fragmented (AAA 32+ skills in packages, GEOX 15-20 canonical MCP as "skills", WEALTH 20+ internal, WELL 21+, arifOS 13-15, Hermes 130-236 catalog, A-FORGE partial discovery). No unified orthogonal binding or cross-organ visibility.

## 2. Orthogonal Mapping Framework

All skills MUST be tagged with at least one from each axis:

### Trinitarian Axis (Core Decision Triangle)
- **Δ (MIND / Reasoning / 333-AGI)**: Evidence synthesis, multi-source analysis, epistemic tagging, paradox resolution, federation routing.
- **Ω (HEART / Memory / Ethics / 555-ASI)**: Deep memory synthesis, sovereignty/entropy guards, tiered memory, dream-engine, human-model reflection, scar-forge.
- **ΦΙ (JUDGE / 888-APEX / arifOS kernel)**: Floor arbitration (F1–F13), verdict issuance (SEAL/PARTIAL/SABAR/VOID/888_HOLD), trinity witness, hold-protocol, constitutional audit.

### Functional Axis
- **Governance / Audit**: Floor enforcement, F11 audit, humility (F7), truth (F9), drift detection, self-audit.
- **Routing / Ops**: A2A dispatch, MCP federation, health-probe, closing-router-discipline, agent-landscape.
- **Forge / Execution**: Implement loops, plan-DAG, subagent spawn, code gen, deployment, FFF-loop-protocol.
- **Evidence / Witness (GEOX primary)**: Seismic/well/basin/physics9/vision, epistemic (CLAIM→UNKNOWN, P10/50/90), provenance.
- **Compute / Capital (WEALTH primary)**: NPV/IRR/EMV/MonteCarlo, 12-domain thermo, game theory, epistemic bands.
- **Vitality / Reflection (WELL primary)**: Homeostasis, metabolic, dignity, entropy, REFLECT_ONLY.
- **Interface / Relay (Hermes / AAA cockpit)**: Human relay, Telegram/A2A, world-model brief, polymorphic role binding.

### Layer / State Axis
- **Layer**: HEXAGON | RUNTIME (hermes-asi/openclaw) | CODING/FI (grok-build etc.) | ORGANS (GEOX/WEALTH/WELL/arifOS/A-FORGE) | HF-DATASETS.
- **Binding State**: DECLARED | BOUND (per card) | LEASED | ACTIVE | ATTESTED | REVOKED.
- **Autonomy Tier**: T1 (auto-do, read/plan/test), T2 (announce + proceed), T3 (888_HOLD + F13).

Skills also carry:
- floor_scope: list of F1–F13.
- riskClass: low/medium/high/critical.
- executionAllowed: bool.
- approval_policy: auto | 888_HOLD | human | kernel.
- reversibility_class: reversible | irreversible (requires VAULT999 + 888).
- subagent_contract: {maxParallel, isolation (worktree|container), capability_mode (read|write|execute|all), resume_from}.
- evidence_required: bool.
- output_schema, time_budget, allowed_tools, forbidden_tools.

## 3. Unified Registry Pattern

AAA will maintain:
- `/root/AAA/contracts/AAA_SKILL.md` (this doc — source of truth for mapping).
- `/root/AAA/registries/skills.yaml` (expanded with orthogonal tags + organ bindings).
- `/root/AAA/contracts/skills/packages.yaml` (packaged with cross-organ refs).
- Dynamic discovery via A2A `discover_a2a_skills` + MCP federation bridge.

Each organ exposes:
- arifOS: 13 canonical (judge, vault_seal, kernel_route, forge_execute...) mapped primarily to ΦΙ + Governance.
- GEOX: 15 public (geox_well_*, geox_seismic_*, geox_basin, geox_vision...) → Evidence/Witness + Δ.
- WEALTH: 20+ (wealth_compute_npv, monte_carlo, stock_analysis...) → Compute/Capital + Δ/Ω.
- WELL: 21 (well_assess_*, well_guard_dignity...) → Vitality/Reflection + Ω.
- A-FORGE: Auto-discovered 62+ + orchestration skills → Forge/Execution + subagent contracts.
- Hermes roles: 130+ catalog + role-specific (see HERMES_ROLE.md) → Interface + polymorphic.
- AAA: 32+ (agent-onboarding, repo-hygiene-audit, mcp-smoke-test, arifos-*, geox-*, github-*) + meta (skill-creator, orthogonal mapping, constitutional self-audit).
- HF datasets: RAG skills for canons, benchmarks, contrast audits.

## 4. Subagent & Parallelism Elevation (Gap Closure)

To address "lacks native deep agentic substrate":

- Subagent spawn contract (standardized in A-FORGE + AAA):
  {
    "task_id": "...",
    "task_description": "...",
    "output_schema": {...},
    "time_budget_minutes": 15,
    "evidence_required": true,
    "risk_band": "T1|T2|T3",
    "allowed_tools": [...],
    "forbidden_tools": ["rm", "vault_write"],
    "isolation": "worktree|container|none",
    "capability_mode": "read|read-write|execute|all",
    "max_parallel": 3,
    "persona": "researcher|auditor|forger"
  }

- Parallelism primitives: A-FORGE ParallelPlanner + Ray/Dask controlled (sovereign). Concurrent subagents with session isolation. Background persistent (systemd leases).

- Recursive: Meta-skill "skill-creator" + "arifos-recursive-audit" for self-forge under gates.

## 5. MCP Federation & Orchestration

- Unified bridge: arifos-mcp-federation skill + A-FORGE discovery.
- Dynamic registration: Organs register via MCP; AAA indexes with orthogonal tags + capability surface.
- Workflows: Extend existing (AREP, pipelines, FFF, plan-DAG) to sovereign LangGraph-equivalent: stateful DAGs with plan-verify-execute, branching, evidence gates, cross-organ.

## 6. Governance & Maintenance

- All skills versioned, artifact_hashed, TREE777-audited.
- HF datasets (AAA gold for floors, BBB–FFF for contrast) integrated into RAG + eval.
- Drift: Sentinel queries + AAA observability.
- Binding visibility: Every agent card lists bound skills with states.

## 7. Immediate Forge Actions (Autonomous T1/T2)

1. This contract created.
2. Reference added to HERMES_ROLE.md, AAA skill packages, registries.
3. Orthogonal tags to be backfilled into existing AAA skills (via follow-on).
4. Proposal: Add "unified-skill-binding" meta-skill to AAA/skills/.

**Receipt path:** `/root/AAA/artifacts/AAA_SKILL.md`

This elevates AAA from fragmented surface to unified agentic substrate while preserving all constitutional gates. The foundation is strong; this forges the missing native depth.

**Ditempa Bukan Diberi.** 

Next ratification: Apply tags to all current skills, or expand subagent contracts in A-FORGE. Arif, your directive?