---
name: wealth-mcp-debug
description: Diagnose WEALTH MCP transport and tool execution failures — distinguishes schema discovery (works) from tool invocation (broken), identifies ToolResult serialization bug, and traces Starlette routing vs FastMCP native transport
tags: [WEALTH, MCP, debug, fastmcp, JSON-RPC]
last_updated: 2026-05-06
---

# WEALTH MCP Debug — External Diagnosis Protocol

## Trigger
WEALTH MCP tools are visible in schema (`tools/list` works) but tool calls fail with:
- `"Object of type ToolResult is not JSON serializable"`
- `"Method not found"` on `initialize`
- HTTP 400/404 on POST `/mcp`

## Key Distinction
```
tools/list → WORKS (HTTP 200, returns tool schema)
tools/call → FAILS (ToolResult serialization error)
```

Discovery intelligence present. Execution integrity blocked. This means transport layer is UP but the tool execution handler has a serialization bug.

## Step 1 — Probe the live endpoint

```bash
# Test discovery (should work)
curl -s -X POST https://wealth.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Test health (should work)
curl -s https://wealth.arif-fazil.com/health

# Test tool call (FAILS with ToolResult error)
curl -s -X POST https://wealth.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mcp_health_check","arguments":{}},"id":2}'

# Test initialize (FAILS with Method not found)
curl -s -X POST https://wealth.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{}},"id":0}'
```

## Step 2 — Check HTTP response headers

```bash
curl -si https://wealth.arif-fazil.com/mcp
```

**Expected (broken):** HTTP 200, `Content-Type: application/json`
**For comparison — GEOX (correct):** HTTP 405 `Allow: POST, DELETE`

## Step 3 — Find the root cause in monolith.py

The bug is at `monolith.py` lines ~4268-4269:

```python
# BROKEN:
result = await mcp.call_tool(name, arguments)
return _JR({"jsonrpc": "2.0", "id": response_id, "result": result})

# FIXED:
result = await mcp.call_tool(name, arguments)
if hasattr(result, 'content'):
    result = result.content  # Unwrap FastMCP ToolResult
return _JR({"jsonrpc": "2.0", "id": response_id, "result": result})
```

`mcp.call_tool()` returns a FastMCP `ToolResult` object — not a dict. JSONResponse cannot serialize it directly. Must unwrap `.content` first.

## Step 4 — Check the routing architecture

In `monolith.py` lines ~4278-4287:

```python
# FastMCP's working HTTP transport — mounted at /
mcp_app = mcp.http_app(path="/", transport="streamable-http", stateless_http=True)

# Custom legacy handler — intercepts /mcp BEFORE FastMCP
app = Starlette(routes=[
    Route("/mcp", legacy_mcp_handler, methods=["GET", "POST"]),  # ← broken
    Route("/health", health_handler, methods=["GET"]),
    Mount("/", app=mcp_app),  # ← working, but never reached from outside
])
```

The proxy routes `/mcp` → `legacy_mcp_handler` (broken). The working FastMCP is at `/` but never reached.

## Two-Endpoint Architecture (verified 2026-05-07)

WEALTH exposes two MCP endpoints on the same port 8082:

| Endpoint | Handler | Protocol Version |
|----------|---------|-----------------|
| `/` | FastMCP native `streamable-http` | `2025-03-26` |
| `/mcp` | `legacy_mcp_handler` (Starlette custom) | `2024-11-05` |

Both handle `initialize` correctly. OpenClaw gateway uses `/mcp` (protocol 2024-11-05). Both return proper handshake responses.

## CRITICAL Diagnostic Step — Container Restart Before Code Analysis (2026-05-07)

**Before assuming code is missing or broken, ALWAYS restart the WEALTH container first.**

Common pattern in arifOS: source files are already fixed, but the running container has a stale image. The `initialize` handler existed in `monolith.py` lines 4294-4303 all along — the running container just needed `docker restart wealth-organ`.

```bash
# Step 0: Restart container FIRST, then test
docker restart wealth-organ
sleep 3

# Now test initialize
curl -s -X POST http://127.0.0.1:8082/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' \
  --max-time 5

# Expected: {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05",...}}
```

## Root Causes Found (2026-05-05/06/07)

### Root Cause A — 502 from External Clients (e.g. ChatGPT) — Updated 2026-05-06

**Symptom:** External callers (ChatGPT, etc.) get `502 Bad Gateway` when calling `wealth_reason_agent`.

**Chain of failure:**
```
External call → Caddy proxy → wealth-organ:8082
→ HTTP 500 from /mcp handler (ValidationError)
→ Caddy surfaces as 502
```

**Root cause 1:** `agent_budget()` at `monolith.py:2300` has 5 required positional params (no defaults). External callers use `wealth_reason_agent` (alias) with `{}` → Pydantic ValidationError.

**Root cause 2:** `legacy_mcp_handler` returns HTTP 500 for any exception. Caddy turns 5xx into 502.

**Fix 1 — defaults on agent_budget (monolith.py:2300):**
```python
def agent_budget(
    compute_budget_usd: float = 1.0,
    token_budget: float = 1000.0,
    time_deadline_hours: float = 1.0,
    expected_value_of_information: float = 0.0,
    actions: List[dict] = None,  # handle None in body
    scale_mode: str = "agentic",
):
    if actions is None:
        actions = []
    # ...
```

**Fix 2 — HTTP 200 for JSON-RPC errors (monolith.py:4270-4273):**
```python
try:
    result = await mcp.call_tool(name, arguments)
    return _JR({"jsonrpc": "2.0", "id": response_id, "result": _serialize_result(result)})
except Exception as e:
    # Return JSON-RPC error as HTTP 200 — clients expect error in body, not 5xx
    return _JR({"jsonrpc": "2.0", "id": response_id, "error": {"code": -32603, "message": str(e)}}, status_code=200)
```

### Root Cause B — ToolResult Serialization — Updated 2026-05-06

**Symptom:** `{"Object of type ToolResult is not JSON serializable"}` — FastMCP `call_tool()` returns Pydantic model, not dict.

**Fix — full `_serialize_result` helper (monolith.py:4237-4251):**
```python
def _serialize_result(result):
    """Convert FastMCP ToolResult to JSON-serializable dict."""
    if result is None:
        return None
    if hasattr(result, "model_dump"):
        d = result.model_dump()
        if "content" in d and isinstance(d["content"], list):
            serialized_content = []
            for item in d["content"]:
                if hasattr(item, "model_dump"):
                    serialized_content.append(item.model_dump())
                else:
                    serialized_content.append(dict(item) if isinstance(item, dict) else str(item))
            d["content"] = serialized_content
        return d
    return result  # Already serializable (dict, str, etc.)
```

### Root Cause C — wealth_reason_agent alias mapping (monolith.py:414)
```python
"wealth_reason_agent": "wealth_agent_budget",  # V2_CANONICAL_MAP
```
`wealth_reason_agent` is a v2 alias that maps to `agent_budget` via `V2_CANONICAL_MAP`. The tool is registered as `wealth_reason_agent` in tools/list but the underlying function is `agent_budget`.

| Priority | Bug | Location | Fix |
|----------|-----|---------|-----|
| P0 | `agent_budget()` 5 required params → ValidationError on empty `{}` | `monolith.py:2300-2305` | Add defaults; handle `None` for `actions` |
| P0 | Exception → HTTP 500 → Caddy 502 | `monolith.py:4270` | Return HTTP 200 for JSON-RPC errors |
| P0 | `ToolResult` not unwrapped before JSON serialization | `monolith.py:4268-4269` | `_serialize_result()` helper |
| P0 | `GET /mcp` returns JSON info instead of 405 | `monolith.py:4237-4244` | Return 405 on GET |
| P1 | Custom handler intercepts `/mcp` before FastMCP native | `monolith.py:4282` | Remove legacy_mcp_handler, route `/mcp` → FastMCP |
| P2 | No `attention_trace` or `resource_allocation` metadata | Tool response layer | Add routing and compute metadata |

## Verification After Fix

```bash
# After fix — tool call should return valid JSON
curl -s -X POST https://wealth.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mcp_health_check","arguments":{}},"id":2}'

# Should return HTTP 200 with JSON result — NOT error about ToolResult

# Also test wealth_reason_agent (alias for agent_budget) with empty {}
curl -s -X POST http://localhost:8082/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"wealth_reason_agent","arguments":{}},"id":7}'

# Should return HTTP 200 + SEAL verdict, NOT 500/502
```

## Important Note

The `legacy_mcp_handler` was likely added to handle a specific client that couldn't use FastMCP's native streamable-http transport. Before removing it, check what client depends on it. If no clients depend on it, the cleanest fix is to remove the custom handler and let FastMCP handle everything at `/mcp`.

## Resolution Summary (2026-05-07)

All P0 bugs fixed and deployed:
- ✅ `agent_budget()` defaults added
- ✅ HTTP 200 for JSON-RPC errors (no more 502)
- ✅ `_serialize_result()` helper for ToolResult → dict
- ✅ `GET /tools` endpoint added — 50 tools, full danger taxonomy, schema `wealth-federation-v2026.05.07`
- ✅ Image pushed: `ghcr.io/ariffazil/wealth:phase1-tools` → `:latest`
- ✅ Container restarted on VPS

## OpenClaw Bundle Registration

WEALTH in OpenClaw bundle (`~/.openclaw/openclaw.json`):
```json
"wealth": {
  "url": "http://127.0.0.1:8082/mcp",
  "description": "WEALTH capital intelligence MCP"
}
```

Verify registration: `openclaw mcp list` — should show `wealth` in the list.

If OpenClaw reports `Method not found` on WEALTH after a code change: **restart the container first** (`docker restart wealth-organ`), then restart the gateway (`sudo systemctl restart openclaw-gateway`).

## File Locations
- `/root/WEALTH/internal/monolith.py` — canonical WEALTH implementation
- `/root/WEALTH/server.py` — thin wrapper, just imports `mcp.run()` from monolith
- `/root/WEALTH/fastmcp.json` — FastMCP config (transport: http, path: /mcp, port: 8082)
