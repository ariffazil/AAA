---
id: aaa-skill-governor-runtime
name: AAA Skill Governor Runtime
version: 1.0.0
description: Operational runtime for SKILL_RUNTIME_GOVERNANCE.md — the 6-gate pre-load and lifecycle discipline. USE WHEN: 'skill validation', 'runtime governance', 'collision resolution', 'deprecation sweep', 'skill promotion review'. Covers: 6 pre-load gates (filesystem, permission, dependency, harness, model, constitutional); loading order 000-substrate → 150-harness_specific; cost classes C0-C4 with agent budgets; collision classes (DUPLICATE, OVERLAP, CHAINED, ALIAS, ORTHOGONAL — unresolved DUPLICATE >72h = both HOLD); weekly deprecation sweep (KEEP/MERGE/DEPRECATE/HOLD/VOID — broken + no owner >30d = VOID); registry declares topology, runtime is truth, never confuse them.
owner: 333-AGI
risk_tier: medium
floor_scope: [F1, F2, F7, F11]
autonomy_tier: T1
organ_domain: aaa
forged: 2026-09-04
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# AAA Skill Governor Runtime

Operational runtime for SKILL_RUNTIME_GOVERNANCE.md — the 6-gate pre-load and lifecycle discipline. USE WHEN: 'skill validation', 'runtime governance', 'collision resolution', 'deprecation sweep', 'skill promotion review'. Covers: 6 pre-load gates (filesystem, permission, dependency, harness, model, constitutional); loading order 000-substrate → 150-harness_specific; cost classes C0-C4 with agent budgets; collision classes (DUPLICATE, OVERLAP, CHAINED, ALIAS, ORTHOGONAL — unresolved DUPLICATE >72h = both HOLD); weekly deprecation sweep (KEEP/MERGE/DEPRECATE/HOLD/VOID — broken + no owner >30d = VOID); registry declares topology, runtime is truth, never confuse them.

## Provenance

Forged 2026-09-04 by 333-AGI (session SEAL-83defc585b5a4296) from live organ tool surfaces + FEDERATION_SKILL_PROFILE gap analysis. Source of truth: the organ MCP surface itself — when skill and tool surface disagree, the tool surface wins and this skill must be revised.
