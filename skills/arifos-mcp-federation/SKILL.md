---
name: arifos-mcp-federation
description: Route tasks across MCP servers, choose server/tool sequence, and define fallbacks when one substrate fails. Load when work spans multiple tools in GEOX, WEALTH, WELL, or external APIs.
---

# arifos-mcp-federation (O_Ω Orchestration Layer)

## Purpose
Route tasks across MCP servers, coordinate server/tool sequences, and define fallbacks when one substrate fails.

## Use When
1. A complex task spans multiple distinct organ environments (e.g. retrieving geologic data in GEOX, verifying networth impact in WEALTH, and checking systemd status).
2. Coordinating sequential multi-tool calls across different MCP stdio or SSE servers.
3. Defining fallback routes when an active MCP server goes offline or returns an error response.
4. Auditing active FastMCP server registries and checking remote connection states.
5. Verifying cross-organ constitutional floors (F8) during A2A mesh communication.

## Do Not Use When
1. Executing a task that is entirely contained within a single local directory or filesystem boundary.
2. Writing standard localized Javascript/React components for the cockpit.
3. The task requires structural changes to a specific tool's internal database code.

## Inputs
*   **Intended Action Sequence:** The high-level pipeline task requested by the user.
*   **MCP Server Registry:** Current active MCP endpoints (`/root/.mcp.json` or custom FastMCP registries).
*   **Client Connections:** Active SSE or stdio transport channels.

## Procedure
1.  **Intent Mapping:** Resolve the user's intent to identify which MCP servers hold the required tools (e.g., geox, wealth, well, or chrome-devtools).
2.  **Tool Sequence Plan:** Construct a clear tool sequence graph. Specify inputs, outputs, and dependencies for each sequential call.
3.  **F8 Cross-Organ Gating:** Enforce Floor F8 (Genius/Systemic Health) constraints for any cross-organ or external internet communication.
4.  **Sequential Execution & Verification:** Execute the planned sequence step-by-step. Verify the output of each tool before piping it to the next.
5.  **Fallback Routing:** If a server fails or times out:
    *   Identify equivalent alternative tools (e.g., falling back from Supabase pg connection to local sqlite, or using local command line instead of MCP wrappers).
    *   Gracefully degrade the execution loop, log the failure trace, and notify `arifos-observability`.
6.  **Telemetry Serialization:** Record the cross-organ connection path and tool success counts in the telemetry log.

## Postconditions
1.  All sequential tool outputs are verified and validated prior to piping.
2.  Alternative backup routes are executed automatically if primary substrates fail.
3.  The complete cross-server trace is recorded for F11 auditability.

## Failure Modes & Escalation
*   **Substrate Collapse:** All mapped MCP servers for a critical element are unreachable. *Action:* Degrade immediately, log `ERR_MCP_SUBSTRATE_COLLAPSE`, halt high-stakes decisions, and prompt the user for manual server restart.
*   **Data Pipeline Mismatch:** Output format of tool A does not match required input schema of tool B. *Action:* Invoke `arifos-governance` holding protocol, refuse to pipe corrupted data, and alert the developer.

## Telemetry per Run
```json
{
  "skill_name": "arifos-mcp-federation",
  "version": "1.0.0",
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
