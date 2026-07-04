---
title: "CONCEPT: TREE777 Skills → MCP Tool Map"
type: concept
version: 1.0.0
category: architecture
dimension: 2
risk_band: MEDIUM
floors: [F1, F13]
evidence_required: true
sources: [arifOS tool registry, TREE777 manifest]
confidence: high
---

# CONCEPT: TREE777 Skills → MCP Tool Map

> **Doctrine map.** Maps every TREE777 wiki skill to the MCP tool(s) it authorizes, disciplines, or gates.
> The skill is the manual. The tool is the machine. This map shows which manual governs which machine.
> **Source:** arifOS tool_registry.json + TREE777 manifest v60

---

## The Core Principle

> A skill may reference a tool, but it **must never become** the tool.
> Skill = doctrine (what should be checked before pressing)
> Tool = actuator (the button itself)

This map shows the **doctrine-to-actuator** relationship.

---

## arifOS / Governance Skills (10)

| Skill | URI | Primary Tool | Secondary Tools | Governance Role |
|-------|-----|--------------|-----------------|-----------------|
| `skill-constitutional-reasoning` | `tree777://skills/arifos/constitutional-reasoning` | — | All 13 tools | **Pre-flight doctrine** — F1–F13 check before ANY tool call |
| `skill-constitutional-advisor` | `tree777://skills/arifos/constitutional-advisor` | — | All 13 tools | F-floor advisory only (prompt/template) |
| `skill-vault-integrity` | `tree777://skills/arifos/vault-integrity` | — | `arif_vault_seal` | **VAULT999 doctrine** — when sealing is permitted |
| `skill-vault999-ops` | `tree777://skills/arifos/vault999-ops` | `arif_vault_seal` | — | VAULT999 read/write/verify/merge protocols |
| `skill-arifos-federation` | `tree777://skills/arifos/arifos-federation` | — | `arif_gateway_connect` | Federation mesh topology + A2A protocol |
| `skill-arifos-operator` | `tree777://skills/arifos/arifos-operator` | `arif_kernel_route` | `arif_gateway_connect` | Kernel routing + session management |
| `skill-scar-distill` | `tree777://skills/arifos/scar-distill` | `arif_memory_recall` | `arif_forge_execute` | Scar creation from failures |
| `skill-skill-promote` | `tree777://skills/arifos/skill-promote` | — | `arif_judge_deliberate` | Skill promotion via 888 deliberation |
| `skill-skill-reflector` | `tree777://skills/arifos/skill-reflector` | — | — | Meta-skill: skill quality auditing (read-only doctrine) |
| `skill-trace-capture` | `tree777://skills/arifos/trace-capture` | `arif_memory_recall` | — | Post-task evidence bundle emission |

---

## Federation / Multi-Agent Skills (5)

| Skill | URI | Primary Tool | Secondary Tools | Governance Role |
|-------|-----|--------------|-----------------|-----------------|
| `skill-aaa-workspace` | `tree777://skills/federation/aaa-workspace` | `arif_kernel_route` | — | AAA workspace operations |
| `skill-hermes-ops` | `tree777://skills/federation/hermes-ops` | `arif_judge_deliberate` | `arif_gateway_connect` | HERMES A2A relay + 888 deliberation |
| `skill-agent-zero` | `tree777://skills/federation/agent-zero` | `arif_forge_execute` | `arif_gateway_connect` | A-FORGE agent delegation |
| `skill-agent-onboarding` | `tree777://skills/federation/agent-onboarding` | — | `arif_session_init` | Agent spatial grounding + TREE777 bind |
| `skill-adapter-sync` | `tree777://skills/federation/adapter-sync` | — | — | Wiki-to-platform sync (planned stub) |

---

## GEOX / Earth Domain Skills (1)

| Skill | URI | Primary Tool | Secondary Tools | Governance Role |
|-------|-----|--------------|-----------------|-----------------|
| `skill-spatial-grounding` | `tree777://skills/geox/spatial-grounding` | — | `arif_sense_observe` | VPS spatial context before GEOX calls |

---

## WELL / Vitality Domain Skills (1)

| Skill | URI | Primary Tool | Secondary Tools | Governance Role |
|-------|-----|--------------|-----------------|-----------------|
| `skill-well-governance-ops` | `tree777://skills/well/well-governance-ops` | — | `arif_heart_critique` | WELL non-medical boundary doctrine |

---

## Infrastructure / Operations Skills (23)

| Skill | URI | Primary Tool | Secondary Tools | Governance Role |
|-------|-----|--------------|-----------------|-----------------|
| `skill-vps-management` | `tree777://skills/infrastructure/vps-management` | — | `arif_ops_measure` | VPS lifecycle doctrine |
| `skill-vps-docker` | `tree777://skills/infrastructure/vps-docker` | — | `arif_ops_measure` | Docker lifecycle doctrine |
| `skill-vps-audit` | `tree777://skills/infrastructure/vps-audit` | `arif_ops_measure` | `arif_stack_health_probe` | VPS health audit protocol |
| `skill-database-tuning` | `tree777://skills/infrastructure/database-tuning` | `arif_ops_measure` | — | PostgreSQL/Redis tuning doctrine |
| `skill-backup-dr` | `tree777://skills/infrastructure/backup-dr` | — | `arif_vault_seal` | Backup/restore protocol (F1 AMANAH) |
| `skill-caddy-cloudflare` | `tree777://skills/infrastructure/caddy-cloudflare` | — | `arif_sense_observe` | Caddy + Cloudflare DNS doctrine |
| `skill-claude-code-ops` | `tree777://skills/infrastructure/claude-code-ops` | — | — | Claude Code maintenance (procedure) |
| `skill-github-issues` | `tree777://skills/infrastructure/github-issues` | `arif_sense_observe` | — | GitHub issue triage doctrine |
| `skill-docker-security` | `tree777://skills/infrastructure/docker-security` | `arif_ops_measure` | — | Docker hardening + port audits (F1) |
| `skill-docker-thermodynamics` | `tree777://skills/infrastructure/docker-thermodynamics` | `arif_ops_measure` | — | Container entropy philosophy |
| `skill-database-tuning` | `tree777://skills/infrastructure/database-tuning` | `arif_ops_measure` | — | DB performance doctrine |
| `skill-secret-hygiene` | `tree777://skills/infrastructure/secret-hygiene` | — | — | Secret rotation philosophy (F1/F11) |
| `skill-secret-rotation-guide` | `tree777://skills/infrastructure/secret-rotation-guide` | — | — | **ARIF_ONLY** — secret rotation actions |
| `skill-cloudflare` | `tree777://skills/infrastructure/cloudflare` | `arif_sense_observe` | — | Cloudflare platform doctrine |
| `skill-agents-sdk` | `tree777://skills/infrastructure/agents-sdk` | `arif_forge_execute` | — | Cloudflare Workers Agent SDK |
| `skill-durable-objects` | `tree777://skills/infrastructure/durable-objects` | — | — | Durable Objects doctrine |
| `skill-sandbox-sdk` | `tree777://skills/infrastructure/sandbox-sdk` | `arif_forge_execute` | — | Sandbox SDK doctrine |
| `skill-wrangler` | `tree777://skills/infrastructure/wrangler` | `arif_forge_execute` | — | Wrangler CLI doctrine |
| `skill-workers-best-practices` | `tree777://skills/infrastructure/workers-best-practices` | — | — | Cloudflare Workers best practices |
| `skill-mcp-builder` | `tree777://skills/infrastructure/mcp-builder` | — | — | MCP server building doctrine |
| `skill-mcp-unified` | `tree777://skills/infrastructure/mcp-unified` | — | — | Cross-platform MCP workflow |
| `skill-fastmcp-deploy` | `tree777://skills/infrastructure/fastmcp-deploy` | `arif_forge_execute` | — | FastMCP VPS deployment |
| `skill-staff-engineer-review` | `tree777://skills/infrastructure/staff-engineer-review` | — | — | PR review doctrine (non-tool) |
| `skill-forge-claude-skill` | `tree777://skills/infrastructure/forge-claude-skill` | `arif_forge_execute` | — | Claude Code skill creation |
| `skill-evidence-verification` | `tree777://skills/infrastructure/evidence-verification` | `arif_evidence_fetch` | — | Anti-fabrication evidence check |

---

## MCP Tool → Skill Doctrine Summary

| Tool | Skills That Authorize/Gate It | Notes |
|------|------------------------------|-------|
| `arif_session_init` | `agent-onboarding` | Session anchor + F11 AUTH binding |
| `arif_sense_observe` | `spatial-grounding`, `caddy-cloudflare`, `github-issues`, `cloudflare` | 111 reality grounding |
| `arif_evidence_fetch` | `evidence-verification` | 222 external fetch |
| `arif_mind_reason` | `constitutional-reasoning` | 333 reasoning under F-floor |
| `arif_kernel_route` | `arifos-operator`, `aaa-workspace` | 444 routing + risk ortho |
| `arif_reply_compose` | — | 444r reply synthesis |
| `arif_memory_recall` | `trace-capture`, `scar-distill` | 555 governed memory |
| `arif_heart_critique` | `well-governance-ops` | 666 F5/F6/F9 adversarial |
| `arif_gateway_connect` | `arifos-federation`, `hermes-ops`, `agent-zero` | 666g A2A mesh |
| `arif_ops_measure` | `vps-audit`, `database-tuning`, `docker-security`, `docker-thermodynamics`, `vps-management`, `vps-docker` | 777 thermodynamic cost |
| `arif_judge_deliberate` | `skill-promote`, `hermes-ops` | **888 — Prompt-first, Tool-gated** |
| `arif_vault_seal` | `vault999-ops`, `vault-integrity`, `backup-dr` | **999 — gated actuator** |
| `arif_forge_execute` | `agent-zero`, `agents-sdk`, `sandbox-sdk`, `wrangler`, `fastmcp-deploy`, `forge-claude-skill`, `scar-distill` | 010 FORGE — SEAL-gated |
| `arif_anti_sink_check` | — | Calhoun topology diagnostic |
| `institutional_drift_check` | — | Acemoglu extractive drift |
| `arif_stack_health_probe` | `vps-audit` | Federation health |
| `federation_audit` | — | P3 readiness audit |

---

## Key Doctrine Relationships

### 888 Judgment Flow
```
SKILL_SKILL_3.md (doctrine)
  → /promote-skill (prompt, Arif-triggered)
  → arif_judge_deliberate (gated tool)
  → arif_vault_seal (if SEAL returned)
```

### VAULT999 Sealing Flow
```
SKILL_OPS.md (doctrine)
  → explicit sealing ritual (prompt)
  → arif_vault_seal (gated actuator)
  → VAULT999 immutable ledger
```

### Trace → Scar → Skill Ladder
```
SKILL_TRACE.md (post-task evidence)
  → arif_memory_recall (memory write)
  → [if failure] SKILL_SCAR.md (failure record)
  → arif_memory_recall (scar write)
  → [if pattern 2-3x] SKILL_SKILL_3.md (promotion)
  → arif_judge_deliberate (888 deliberation)
  → [if SEAL] canonical skill in wiki
```

---

*See also: [[mcp-architecture-mapping]], [[TREE777]], [[skill-constitutional-reasoning]], [[skill-vault999-ops]], [[anti-fabrication-protocol]]*
*DITEMPA BUKAN DIBERI — The skill is the manual. The tool is the machine. Read the manual before pressing.*
