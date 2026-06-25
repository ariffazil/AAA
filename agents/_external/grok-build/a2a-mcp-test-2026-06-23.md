# A2A Dialogue Test — Grok Build Consuming Narrow MCP Surfaces

**Date:** 2026-06-23
**Participants:** grok-build (as consumer/llm principal) → AAA A2A → arifos-mcp-federation or direct MCP bridge → mcp-repo-read + mcp-memory
**Purpose:** Validate discovery and use of the sovereign narrow MCPs via the mesh, with constitutional injection.

## Test Scenario (Pagi Pulse Style)

Grok Build (after receiving research from multi-agent mode):

"Using arifos-mcp-federation skill and A2A, discover and query mcp-repo-read for latest ADR on boundaries, then mcp-memory for recent cooling entry on model fragility. Summarize with F7 humility and route to arifOS if 888 needed."

## Expected Flow

1. Grok Build calls A2A discover or uses arifos-mcp-federation.
2. Routes to `mcp-repo-read` (via stdio or registered).
3. Calls `get_adr(latest)` or search.
4. Then `mcp-memory` `recall_cooling_ledger` or `search_governance`.
5. Returns structured evidence.
6. If change implied: escalate "888_HOLD required per mcp-repo-write policy".
7. Telemetry emitted.

## Verification Criteria (F2/F11)

- Correct server_label and description used for routing.
- Outputs include "status", "telemetry", "path" with real data.
- No overclaim; humility in summary.
- Escalation path explicit.
- Trace logged to Cooling Ledger.

## Sample Output (simulated from wired servers)

From mcp-repo-read get_adr:
{"status": "ok", "adr": "ADR_001_BOUNDARIES.md", ...}

From mcp-memory search_governance("model"):
{"results": [{"floor": "F7", "note": "..."}, ...]}

## Next

After live run: update daily-pulse context chain with results.

**Sealed in context of 999_SEAL.** 

Use via Grok Build config + A2A gateway.
