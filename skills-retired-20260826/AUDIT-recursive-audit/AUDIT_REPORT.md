# arifOS Recursive Audit — Skill Portfolio Report
**Date:** 2026-06-23T10:59:57.396173+00:00
**Auditor:** arifos-recursive-audit skill (v1.0.0)
**Scopes scanned:** Project, User, Extra
**Total SKILL.md files:** 100 (92 active, 8 quarantined)

## Executive Summary
- Active skills: 92
- Prompt-bloat flags (>500 lines): 1
- Stale/unused flags: 0
- Broken-reference (doc-rot) flags: 7
- Potential trigger collisions: 10
- Circular references detected: 0

## Active Skills by Scope

### Project (45 skills)
| Skill | Version | Owner | Lines | Age (days) | Rot Tags |
|-------|---------|-------|-------|------------|----------|
| Federation Coding Agent | 1.0.0-2026.06.23 | AAA / F13 SOVEREIGN | 236 | 0 | clean |
| aaa-doctrine-loader | unknown | unspecified | 165 | 0 | clean |
| aforge-execution-governor | unknown | unspecified | 174 | 0 | clean |
| agentic-toolcheck | unknown | unspecified | 19 | 10 | clean |
| agents-sdk | 1.0.0 | unspecified | 222 | 10 | clean |
| arifos-kernel-operator | unknown | unspecified | 177 | 0 | clean |
| arifos-plan-dag | 1.0.0 | unspecified | 73 | 10 | clean |
| arifos-untrusted-sandbox | 1.0.0 | unspecified | 84 | 16 | clean |
| auditor-validator-kutip-sampah | unknown | unspecified | 188 | 0 | clean |
| building-pydantic-ai-agents | unknown | unspecified | 278 | 6 | clean |
| cloudflare | 1.0.0 | unspecified | 241 | 10 | clean |
| cloudflare-email-service | 1.0.0 | unspecified | 105 | 6 | clean |
| durable-objects | 1.0.0 | unspecified | 187 | 10 | clean |
| federation-router | unknown | unspecified | 171 | 0 | clean |
| frontend-design | 1.0.0 | unspecified | 43 | 10 | clean |
| geox-basin-interpreter | 1.0.0 | unspecified | 95 | 0 | clean |
| geox-binary-transport | unknown | unspecified | 104 | 0 | clean |
| geox-claim-grammar | unknown | unspecified | 119 | 0 | clean |
| geox-constitution | unknown | unspecified | 103 | 0 | clean |
| geox-contradiction-engine | unknown | unspecified | 74 | 0 | clean |
| geox-drift-detector | unknown | unspecified | 81 | 0 | clean |
| geox-epistemic-ladder | unknown | unspecified | 79 | 0 | clean |
| geox-expiry-replan | unknown | unspecified | 72 | 0 | clean |
| geox-gui-alignment | unknown | unspecified | 134 | 0 | clean |
| geox-mcp-contracts | unknown | unspecified | 68 | 0 | clean |
| geox-merge-gatekeeper | unknown | unspecified | 86 | 0 | clean |
| geox-petrophysics-bounds | unknown | unspecified | 70 | 0 | clean |
| geox-redteam-hantu | unknown | unspecified | 91 | 0 | clean |
| geox-render-contracts | unknown | unspecified | 91 | 0 | clean |
| geox-sandbox-simulation | unknown | unspecified | 83 | 0 | clean |
| geox-test-forge | unknown | unspecified | 136 | 0 | clean |
| godel-humility-lock | unknown | unspecified | 88 | 3 | clean |
| logfire-instrumentation | unknown | unspecified | 272 | 6 | clean |
| logfire-query | unknown | unspecified | 203 | 6 | clean |
| logfire-ui | unknown | unspecified | 124 | 6 | clean |
| mcp-fastmcp-builder | unknown | unspecified | 162 | 0 | clean |
| pydantic-ai-harness | unknown | unspecified | 101 | 6 | clean |
| replicate-models | unknown | unspecified | 71 | 3 | clean |
| replicate-prompting | unknown | unspecified | 199 | 3 | clean |
| sandbox-sdk | 1.0.0 | unspecified | 178 | 10 | clean |
| skill-creator | 1.0.0 | unspecified | 66 | 10 | clean |
| vault999-audit-sealer | unknown | unspecified | 168 | 0 | clean |
| web-perf | 1.0.0 | unspecified | 202 | 10 | clean |
| workers-best-practices | 1.0.0 | unspecified | 128 | 10 | clean |
| wrangler | 1.0.0 | unspecified | 923 | 10 | prompt-bloat |

### User (7 skills)
| Skill | Version | Owner | Lines | Age (days) | Rot Tags |
|-------|---------|-------|-------|------------|----------|
| aaa-doctrine-loader | 1.0.0-2026.06.23 | AAA / arifOS | 163 | 0 | clean |
| aforge-execution-governor | 1.0.0-2026.06.23 | A-FORGE / AAA | 172 | 0 | clean |
| arifos-kernel-operator | 1.0.0-2026.06.23 | arifOS | 175 | 0 | clean |
| auditor-validator-kutip-sampah | 1.0.0-2026.06.23 | AAA / arifOS | 186 | 0 | clean |
| federation-router | 1.0.0-2026.06.23 | AAA | 169 | 0 | clean |
| mcp-fastmcp-builder | 1.0.0-2026.06.23 | arifOS / AAA | 160 | 0 | clean |
| vault999-audit-sealer | 1.0.0-2026.06.23 | arifOS / VAULT999 | 166 | 0 | clean |

### Extra (40 skills)
| Skill | Version | Owner | Lines | Age (days) | Rot Tags |
|-------|---------|-------|-------|------------|----------|
| AAA Agent Operating Invariants | 1.0.0 | AAA | 340 | 0 | clean |
| AAA Agentic Governance (AAA-Cockpit, canonical) | 3.0.1 | AAA | 376 | 0 | clean |
| Agent Onboarding | 1.0.0 | AAA | 218 | 0 | clean |
| Agentic Dream Engine — Federation Memory Consolidation | 1.0.0 | AAA | 322 | 0 | doc-rot |
| Code Wiki — Codebase Documentation Generator | 1.0.0 | AAA | 340 | 0 | clean |
| Docker Entropy Ops | 1.0.0 | AAA | 186 | 0 | clean |
| Drift Response | 0.1.0 | AAA | 158 | 0 | doc-rot |
| Federation Health Scan | 0.1.0 | AAA | 311 | 0 | clean |
| Federation Service Health Triage | 1.0.1 | AAA | 173 | 0 | doc-rot |
| GEOX Grounding | 0.1.0 | AAA | 76 | 0 | clean |
| GitHub CI Diagnose | 1.0.0 | AAA | 182 | 0 | clean |
| GitHub Issue Triage | 1.0.0 | AAA | 178 | 0 | clean |
| GitHub PR Governance Review | 1.0.0 | AAA | 118 | 0 | clean |
| GitHub Runbook — Federation Git & CLI Operations | 1.0.0 | AAA | 201 | 0 | clean |
| Incident Escalation Protocol | 1.0.0 | AAA | 139 | 0 | clean |
| Incident Triage | 1.0.0 | AAA | 228 | 0 | doc-rot |
| Kimi Code AAA Configuration | 1.0.0 | AAA | 150 | 0 | clean |
| MCP Federation Operations | 1.0.0 | AAA | 248 | 0 | clean |
| Multi-Discipline Critique | 1.0.0 | AAA | 207 | 0 | doc-rot |
| Nusantara Intelligence Substrate | 1.0.0 | F13 SOVEREIGN | 204 | 0 | clean |
| OpenClaw A2A Bridge | 0.1.0 | AAA | 85 | 0 | clean |
| PR Review Governance | 1.0.0 | AAA | 123 | 0 | clean |
| Parallel Authority Detection | 1.0.0 | AAA | 105 | 0 | clean |
| Precommit Gate | 1.0.0 | AAA | 183 | 0 | clean |
| README Truth Check | 1.0.0 | AAA | 114 | 0 | clean |
| Recursive Skill Forge | 1.0.0 | AAA | 420 | 0 | clean |
| Repository Hygiene Audit | 1.0.0 | AAA | 205 | 0 | clean |
| Secret Safety Scan | 1.0.1 | AAA | 163 | 0 | clean |
| Skill Trigger Linter | 1.0.0 | AAA | 134 | 0 | clean |
| Unified Skill Binding (Orthogonal + Cross-Organ) | 1.0.0 | AAA | 150 | 0 | clean |
| VPS Docker Runbook | 1.0.0 | AAA | 206 | 0 | clean |
| Vault999 Integrity — Operational Lens | 1.0.0 | AAA | 191 | 0 | clean |
| arifOS ACT — Constitutional Reflex | 3.0.0 | AAA | 284 | 0 | clean |
| arifOS Evals | 1.0.0 | AAA | 158 | 0 | clean |
| arifOS MCP Federation | 1.0.0 | AAA | 129 | 0 | clean |
| arifOS Observability | 1.0.0 | AAA | 121 | 0 | clean |
| arifOS Plan DAG | 1.0.0 | AAA | 125 | 0 | clean |
| arifOS Recursive Audit | 1.0.0 | AAA | 133 | 0 | clean |
| arifos-governance | 1.0.1 | AAA | 182 | 0 | doc-rot |
| spatial-grounding | 1.0.0 | unspecified | 109 | 8 | doc-rot |

## Quarantined / Archived Skills
| Skill | Scope | Path | Age (days) |
|-------|-------|------|------------|
| GEOX Basin Interpreter | Extra | AAA/skills/.quarantine-2026-06-23/geox-basin-interpreter/SKILL.md | 0 |
| MCP Server Smoke Test | Extra | AAA/skills/.quarantine-2026-06-23/mcp-smoke-test/SKILL.md | 0 |
| Skill Creator | Extra | AAA/skills/.quarantine-2026-06-23/skill-creator/SKILL.md | 0 |
| arifos-evals | Project | .agents/skills/.quarantine-2026-06-23/arifos-evals/SKILL.md | 10 |
| arifos-mcp-federation | Project | .agents/skills/.quarantine-2026-06-23/arifos-mcp-federation/SKILL.md | 10 |
| skill-trigger-linter | Project | .agents/skills/.quarantine-2026-06-23/skill-trigger-linter/SKILL.md | 10 |
| mcp-unified | User | .arifos/agents/kimi/skills/.quarantine-2026-06-23/_archive/mcp-unified/SKILL.md | 26 |
| site-architecture | User | .arifos/agents/kimi/skills/.quarantine-2026-06-23/_archive/site-architecture/SKILL.md | 36 |

## Rot Classification Detail

### Agentic Dream Engine — Federation Memory Consolidation (Extra)
- **Path:** `AAA/skills/agentic-dream-engine/SKILL.md`
- **Age:** 0 days
- **Rot tags:** doc-rot
- **Broken/missing references:**
  - `/var/spool/arifos/dream-proposals/opencode/`

### Drift Response (Extra)
- **Path:** `AAA/skills/drift-response/SKILL.md`
- **Age:** 0 days
- **Rot tags:** doc-rot
- **Broken/missing references:**
  - `/root/AAA/wiki/scars/scar-drift-YYYY-MM-DD.md`

### Federation Service Health Triage (Extra)
- **Path:** `AAA/skills/service-health-triage/SKILL.md`
- **Age:** 0 days
- **Rot tags:** doc-rot
- **Broken/missing references:**
  - `/root/RUNBOOK.md`

### Incident Triage (Extra)
- **Path:** `AAA/skills/incident-triage/SKILL.md`
- **Age:** 0 days
- **Rot tags:** doc-rot
- **Broken/missing references:**
  - `/root/INCIDENTS/<YYYY-MM-DD>-<slug>.md`

### Multi-Discipline Critique (Extra)
- **Path:** `AAA/skills/multi-discipline-critique/SKILL.md`
- **Age:** 0 days
- **Rot tags:** doc-rot
- **Broken/missing references:**
  - `/root/SECRETS.md`

### arifos-governance (Extra)
- **Path:** `AAA/skills/arifos-governance/SKILL.md`
- **Age:** 0 days
- **Rot tags:** doc-rot
- **Broken/missing references:**
  - `/root/.claude/hooks/f1-gate.log`

### spatial-grounding (Extra)
- **Path:** `AAA/skills/spatial-grounding/claude/SKILL.md`
- **Age:** 8 days
- **Rot tags:** doc-rot
- **Broken/missing references:**
  - `/root/.opencode/SPATIAL_LAW.md`

### wrangler (Project)
- **Path:** `.agents/skills/wrangler/SKILL.md`
- **Age:** 10 days
- **Rot tags:** prompt-bloat

## Trigger / Semantic Collision Audit
| Skill A | Skill B | Jaccard Similarity | Note |
|---------|---------|--------------------|------|
| aaa-doctrine-loader | aaa-doctrine-loader | 1.00 | shadow duplicate across scopes |
| aforge-execution-governor | aforge-execution-governor | 1.00 | shadow duplicate across scopes |
| arifos-kernel-operator | arifos-kernel-operator | 1.00 | shadow duplicate across scopes |
| arifos-plan-dag | arifOS Plan DAG | 1.00 | semantic overlap |
| auditor-validator-kutip-sampah | auditor-validator-kutip-sampah | 1.00 | shadow duplicate across scopes |
| federation-router | federation-router | 1.00 | shadow duplicate across scopes |
| mcp-fastmcp-builder | mcp-fastmcp-builder | 1.00 | shadow duplicate across scopes |
| vault999-audit-sealer | vault999-audit-sealer | 1.00 | shadow duplicate across scopes |
| Drift Response | Federation Health Scan | 0.38 | semantic overlap |
| logfire-query | logfire-ui | 0.35 | semantic overlap |

## Circular Reference Detection
No circular skill references detected.

## Cross-Scope Shadow Skills
| Skill | Scopes |
|-------|--------|
| aaa-doctrine-loader | Project, User |
| aforge-execution-governor | Project, User |
| arifos-kernel-operator | Project, User |
| auditor-validator-kutip-sampah | Project, User |
| federation-router | Project, User |
| mcp-fastmcp-builder | Project, User |
| vault999-audit-sealer | Project, User |

## Recommendations
1. **Prompt bloat:** Review 1 skill exceeding 500 lines (`wrangler`); split or summarize where possible.
2. **Doc rot:** 7 skills reference missing filesystem paths; update or remove dead references.
3. **Trigger collisions:** 10 skill pairs show semantic overlap; tighten `Use When` / `Do Not Use When` boundaries.
4. **Cross-scope shadows:** 7 skills exist in both Project and User scopes. Per federation precedence rules (Project > User > Extra), this is intentional, but verify the User-scope versions remain the authority source where intended.

## Telemetry
```json
{
  "skill_name": "arifos-recursive-audit",
  "version": "1.1.0",
  "trigger_phrase": "/skill:arifOS Recursive Audit",
  "selected_reason": "User requested portfolio audit",
  "latency_ms": 0,
  "token_in": 0,
  "token_out": 0,
  "commands_run": 1,
  "artifacts_written": 1,
  "postcondition_pass": true,
  "human_approval_required": false,
  "hold_code": "NONE",
  "active_skills": 92,
  "quarantined_skills": 8,
  "bloat_flags": 1,
  "stale_flags": 0,
  "docrot_flags": 7,
  "collision_pairs": 10,
  "circular_cycles": 0
}
```
