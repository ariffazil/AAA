---
name: arifos-mcp-federation
description: Route tasks across two or more federation MCP servers, sequence tool calls, and define fallbacks when an organ substrate fails. Load only when work spans multiple organs (GEOX, WEALTH, WELL, A-FORGE, AAA, external APIs).
version: 1.1.0
last_verified: 2026-06-12
license: Proprietary
agents: claude | opencode | kimi | codex
---

# arifos-mcp-federation (O_Ω Orchestration Layer)

## Purpose
Runtime orchestration across multiple MCP servers in the arifOS federation. This skill governs how tool outputs from one organ are validated and piped into tools of another organ, and how to degrade when a substrate fails.

## Use When
1. A task requires sequential calls across ≥2 federation organs (e.g. GEOX → WEALTH → WELL).
2. A fallback route is needed because the primary organ is offline or returned non-ok.
3. Output from one organ must be transformed into input for another organ's tool.

## Do Not Use When
1. Single MCP tool call — use `mcporter`.
2. MCP server build, deploy, or health audit — use `fastmcp`, `mcp-ops`, or `mcp-unified`.
3. Registry inspection only — use `mcporter list` or `mcp-ops`.
4. Constitutional floor judgment — use `arifos-governance`.
5. Irreversible cross-organ state changes (writes, seals, restarts) — route through `arifos-governance` / 888_HOLD.

## Prefer These Sibling Skills
| Task | Skill |
|------|-------|
| Single tool call / discovery | `mcporter` |
| Build/refactor MCP server | `fastmcp` or `mcp-unified` |
| Health check / runtime audit | `verify-runtime` or `mcp-ops` |
| Constitutional gating | `arifos-governance` |
| Telemetry logging | `arifos-observability` |

## Inputs
*   **Intended Action Sequence:** The high-level pipeline task requested by the user.
*   **MCP Server Registry:** Current active MCP endpoints (`/root/.mcp.json` or `mcporter list`).
*   **Client Connections:** Active SSE or stdio transport channels.

## Procedure
1.  **Intent Mapping:** Resolve the user's intent to identify which organs hold the required tools. Prefer canonical public tools over internal helpers.
2.  **Tool Sequence Plan:** Draw a sequence graph. For each step record: tool selector, required input keys, expected output keys, downstream consumer.
3.  **F8 Cross-Organ Gating:** Enforce Floor F8 (Genius/Systemic Health) constraints for any cross-organ or external internet communication. If F8 is unclear, call `arifos-governance`.
4.  **Sequential Execution & Verification:** Execute step-by-step. A step output is valid only if:
    *   The response contains `ok: true` or equivalent success marker, and
    *   All required keys for the next step are present.

    If either check fails, halt the pipe and invoke fallback.
5.  **Fallback Routing:** If a server fails or times out:
    *   Identify equivalent alternative tools or local CLI equivalents.
    *   Degrade gracefully, log the failure trace, and notify `arifos-observability`.
6.  **Telemetry Serialization:** Record the cross-organ connection path and tool success counts in the telemetry log.

## Example Pipeline
```text
User: "Evaluate a new well, check if it strains Arif's capital, and confirm WELL readiness."

Step 1: GEOX.geox_well_analyze_log(well_id=MAHA-1)
Step 2: WEALTH.wealth_position_size(entry=..., stop=..., account_balance=...)
        input: capital_at_risk derived from GEOX output
Step 3: WELL.well_validate_vitality(mode="readiness")
        input: decision_class = "C4" if position size > 1% risk

Fallback: If GEOX is down, use local well_* CLI or return 888_HOLD.
```

## Postconditions
1.  All sequential tool outputs are verified before piping.
2.  Fallback routes are executed automatically if primary substrates fail.
3.  The complete cross-server trace is recorded for F11 auditability.

## 888_HOLD Triggers
*   Any cross-organ action that writes state, seals to VAULT999, or restarts a production service.
*   Any pipeline where F8 systemic-health check returns DEGRADED or CRITICAL.
*   Any fallback that requires exposing secrets or altering network boundaries.

## Failure Modes & Escalation
*   **Substrate Collapse:** All mapped MCP servers for a critical element are unreachable. *Action:* Degrade immediately, log `ERR_MCP_SUBSTRATE_COLLAPSE`, halt high-stakes decisions, and prompt the user for manual server restart.
*   **Data Pipeline Mismatch:** Output format of tool A does not match required input schema of tool B. *Action:* Invoke `arifos-governance` holding protocol, refuse to pipe corrupted data, and alert the developer.
*   **Unauthorized Cross-Organ Write:** A tool attempts a write outside its organ boundary. *Action:* Block, log `ERR_CROSS_ORGAN_WRITE`, escalate to 888_HOLD.

## Telemetry per Run
```json
{
  "skill_name": "arifos-mcp-federation",
  "version": "1.1.0",
  "trigger_phrase": "{{trigger_phrase}}",
  "selected_reason": "{{selected_reason}}",
  "latency_ms": 0,
  "token_in": 0,
  "token_out": 0,
  "commands_run": 0,
  "artifacts_written": 0,
  "postcondition_pass": false,
  "human_approval_required": false,
  "hold_code": "{{hold_code}}"
}
```

## Recursive Scorecard
*   **Activation Precision:** [0.0 - 1.0] (Target: >0.95)
*   **Task Completion Rate:** [0.0 - 1.0] (Target: >0.98)
*   **Rollback Safety:** [0.0 - 1.0] (Target: 1.00)
*   **Context Efficiency:** [0.0 - 1.0] (Target: >0.90)
*   **Doc Freshness:** [0.0 - 1.0] (Target: 1.00)
*   **Cross-Skill Collision Rate:** [0.0 - 1.0] (Target: <0.02)
*   **Human Trust Score:** [0.0 - 1.0] (Target: >0.98)
