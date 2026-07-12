---
id: arifos-mcp-federation
name: arifOS MCP Federation
version: 1.0.0
description: Route tasks across MCP servers, choose server/tool sequence, and define
  fallbacks when one substrate fails. Load when work spans multiple tools in GEOX,
  WEALTH, WELL, or external APIs.
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
  - arifos-act
  servers:
  - arifos-mcp
  tools: []
examples:
- Route a task requiring GEOX evidence and WEALTH valuation across organs
- Fallback to local commands when an MCP server is unreachable
tests:
- Brain/hands separation preserved (A-FORGE only after lease)
- Governance path reaches arifOS tools, not A-FORGE
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Δ
  functional:
  - Routing
  layer: RUNTIME
  autonomy_tier: T2
floor_scope:
- F2
- F3
- F4
- F8
- F11
---

# arifos-mcp-federation (O_Ω Orchestration Layer)

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


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
1.  **Intent Mapping + Brain/Hands Classification:** Resolve the user's intent and **classify every step**:
    - Governance, judgment, epistemic floors, memory mutation with blast radius, sealing, INIT/JUDGE/SEAL → **arifOS MCP (8088) first**.
    - Execution, build, shell, browser automation, jobs, proxies under bounded authority → **A-FORGE MCP (7072 or stdio)** only after lease.
    Resolve the user's intent to identify which MCP servers hold the required tools (e.g., geox, wealth, well, or chrome-devtools) **while respecting the separation**.
2.  **Tool Sequence Plan:** Construct a clear tool sequence graph that **never** collapses the contract. Always insert `arif_judge` + lease before high-risk A-FORGE actions. Specify inputs, outputs, and dependencies for each sequential call.
3.  **F8 Cross-Organ Gating + Lease/Judge Handoff:** Enforce Floor F8 (Genius/Systemic Health) **and** the brain/hands contract. Any mutate/atomic forge_* requires valid lease_id. Governance paths must reach arifOS canonical tools.
4.  **Sequential Execution & Verification:** Execute the planned sequence step-by-step. Verify the output of each tool before piping it to the next. Reject any pipe that would allow A-FORGE to issue or bypass 888/999 verdicts.
5.  **Fallback Routing:** If a server fails or times out:
    *   Identify equivalent alternative tools (e.g., falling back from Supabase pg connection to local sqlite, or using local command line instead of MCP wrappers).
    *   Gracefully degrade the execution loop, log the failure trace, and notify `arifos-observability`.
    *   On governance substrate failure: escalate to 888_HOLD; never fall back to execution-only path.
6.  **Telemetry Serialization:** Record the cross-organ connection path, **which MCP surface was used for judgment vs execution**, lease_id (if any), and tool success counts in the telemetry log. Emit to AAA for lease-compliance and seal-latency metrics.

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