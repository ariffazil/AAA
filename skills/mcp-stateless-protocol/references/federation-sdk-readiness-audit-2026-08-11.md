# Federation SDK Readiness Audit — 2026-08-11

Per-organ SDK version inventory, stateless capability, and session-dependency scan.
Conducted via grep of server.py / serve.ts entrypoints, pyproject.toml / package.json pins, and .venv installed versions.

## Organ Inventory

### arifOS (kernel) — ✅ FULLY STATELESS
- **SDK:** fastmcp 3.4.6 (installed), mcp 1.27.2 (installed)
- **Transport:** `stateless_http=True` (server.py:2690)
- **Protocol:** "2026-07-28" declared, injected into SUPPORTED_PROTOCOL_VERSIONS (server.py:584-585)
- **Session code:** mcp-session-id kept as backward-compat header only (deprecated in 2026-07-28)
- **Status:** Reference implementation. No changes needed.

### GEOX — ❌ NOT STATELESS (stateful transport)
- **SDK:** fastmcp 3.4.5 (pinned in pyproject.toml), 3.4.6 (installed in .venv)
- **Transport:** `stateless_http=False` (server.py:3702) — explicit comment "Stateful: session IDs validated"
- **Protocol:** "2025-06-18" hardcoded in discovery handler (server.py:3278)
- **Session deps found:**
  - `_kernel_mcp_session_id` global variable in organ_governance.py (stores/validates session ID)
  - Mcp-Session-Id header extraction and validation in organ_governance.py:164-179
  - `WellMcpSessionEnforcement` middleware pattern (session_id from headers)
- **Fix needed:**
  1. `stateless_http=False` → `stateless_http=True`
  2. protocolVersion "2025-06-18" → "2026-07-28"
  3. Remove `_kernel_mcp_session_id` global and Mcp-Session-Id extraction
  4. Append "2026-07-28" to mcp SDK SUPPORTED_PROTOCOL_VERSIONS
- **Effort:** 4-6 hours

### WEALTH — ⚠️ PARTIAL (stateless transport, session middleware still active)
- **SDK:** fastmcp 3.4.6 (pinned + installed)
- **Transport:** `stateless_http=True` (server_federated.py:190) ✅
- **Protocol:** Not declared in health/discovery endpoints
- **Session deps found:**
  - Mcp-Session-Id enforcement middleware (server_federated.py:285-335)
  - Session ID extraction from response headers (wealth_mcp/server.py:152)
- **Fix needed:**
  1. Remove Mcp-Session-Id enforcement middleware
  2. Add protocolVersion "2026-07-28" to health endpoint
  3. Append "2026-07-28" to mcp SDK SUPPORTED_PROTOCOL_VERSIONS
- **Effort:** 2-3 hours (closest to done)

### WELL — ⚠️ PARTIAL (stateless transport, two session middlewares)
- **SDK:** fastmcp 3.4.5 (pinned), 3.4.6 (installed in .venv)
- **Transport:** `stateless_http=True` (server.py:13114) ✅
- **Protocol:** Not declared
- **Session deps found:**
  - `WellSessionValidationMiddleware` — enforces session_id on every tool call (server.py:1678-1724)
  - `WellMcpSessionEnforcement` — validates Mcp-Session-Id header (server.py tail)
  - session_id extracted from kwargs AND context.session_id fallback (server.py:1716-1724)
- **Fix needed:**
  1. Remove WellSessionValidationMiddleware
  2. Remove WellMcpSessionEnforcement middleware
  3. Add protocolVersion "2026-07-28" to health endpoint
  4. Bump pyproject.toml pin from 3.4.5 to 3.4.6
- **Effort:** 3-4 hours

### A-FORGE — ❌ NOT STATELESS (sessionIdGenerator active)
- **SDK:** @modelcontextprotocol/sdk 1.29.0 (installed), ^1.9.0 (pinned)
- **Transport:** sessionIdGenerator active (serve.ts:576), NOT stateless
- **Protocol:** "2025-11-25" hardcoded (serve.ts:514, 613)
- **Session deps found:**
  - SSE session registry with cleanup timer (serve.ts:284-294)
  - Session store Map references (serve.ts:980)
  - `STATELESS_TOOLS` whitelist defined (serve.ts:53-181) but not wired to transport
  - sessionGate.ts references "stateless MCP 2026-07-28" but implementation uses session store
  - stdio-http-bridge.js IS stateless (fresh transport per request, no sessionIdGenerator)
- **Fix needed:**
  1. Remove sessionIdGenerator from StreamableHTTPServerTransport init
  2. protocolVersion "2025-11-25" → "2026-07-28"
  3. Wire STATELESS_TOOLS whitelist to reject session-gated tools without session
  4. Update sessionGate.ts to use sct_v1 tokens instead of session store
  5. Remove SSE session registry and cleanup timer
- **Effort:** 6-8 hours (most complex — hybrid transport, session gate rewrite)

## Key SDK Patterns for Stateless Migration

### FastMCP Python (3.4.5+)
```python
# Stateless mode — new transport per request, no session state
app = mcp.http_app(
    transport="streamable-http",
    stateless_http=True,
    json_response=True,
)
```
- `stateless_http=True` restricts HTTP methods to POST+DELETE (no GET/SSE)
- Global setting available: `FASTMCP_STATELESS_HTTP=true` env or `fastmcp.settings.stateless_http`

### mcp Python SDK (1.27.x)
- `SUPPORTED_PROTOCOL_VERSIONS` does NOT include "2026-07-28" by default
- Must monkey-patch at startup:
```python
from mcp.shared import version as mcp_shared_version
if "2026-07-28" not in mcp_shared_version.SUPPORTED_PROTOCOL_VERSIONS:
    mcp_shared_version.SUPPORTED_PROTOCOL_VERSIONS.append("2026-07-28")
```

### @modelcontextprotocol/sdk TypeScript (1.29.0)
```typescript
// Stateless: omit sessionIdGenerator
const transport = new StreamableHTTPServerTransport({
  enableJsonResponse: true,
  // No sessionIdGenerator = stateless mode
});
```

## Session-Dependent Code Patterns to Grep For
```bash
# Python organs
grep -rn "session_id\|Mcp-Session\|_kernel_mcp_session_id\|SessionEnforcement\|SessionValidation" --include="*.py"

# TypeScript organs
grep -rn "sessionId\|sessionIdGenerator\|sessionStore\|session.*Map" --include="*.ts" --include="*.js"
```
