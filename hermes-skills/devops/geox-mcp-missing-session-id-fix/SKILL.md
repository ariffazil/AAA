---
name: geox-mcp-missing-session-id-fix
description: Fix HTTP 400 "Missing session ID" on GEOX/streamable-http MCP when using FastMCP 3.2.4 stateful mode. Chicken-and-egg session validation bug in MCP SDK.
tags: [fastmcp, mcp, geox, debug, streamable-http, session]
version: 1.0.0
author: Hermes
license: AGPL-3.0
product: arifOS Constitutional Federation
---

# GEOX MCP "Missing session ID" Fix — FastMCP Stateful Mode Bug

## When This Skill Activates

When a GEOX/streamable-http MCP endpoint returns:
```
HTTP 400 — "Missing session ID"
```
And the transport is FastMCP 3.2.4 + MCP SDK, running in **stateful mode** (stateless_http=False).

## The Bug — MCP SDK Stateful Session Chicken-and-Egg

In stateful mode (stateless_http=False), the MCP SDK flow is:

```
1. POST /mcp → create_new_session() → creates session, assigns self.mcp_session_id
2. → immediately calls handle_request() to process the request
3. handle_request() → _validate_session() → checks self.mcp_session_id is not None
4. → requires MCP-Session-Id header in request
5. CLIENT HASN'T RECEIVED SESSION ID YET — server created it but never sent it
→ HTTP 400 "Missing session ID"
```

This is a bug in MCP SDK's stateful flow. The session ID is generated server-side but the client hasn't seen it to echo it back on the first request.

Reference: mcp/server/streamable_http.py line ~844 in MCP SDK package.

## The Fix

Switch to **stateless mode** — stateless_http=True — which sets mcp_session_id=None and skips session validation entirely.

```python
# WRONG — causes "Missing session ID" in FastMCP 3.2.4 + MCP SDK:
mcp_app = FastMCP("GEOX")
app = mcp_app.http_app(
    stateless_http=False,  # stateful mode — BROKEN
    json_response=True,
)

# CORRECT — arifOS pattern:
mcp_app = FastMCP("GEOX")
app = mcp_app.http_app(
    stateless_http=True,   # stateless mode — WORKS
    json_response=True,
)
```

## Full Correct server.py APP_CREATION Pattern

```python
def create_app():
    mcp_app = FastMCP("GEOX")

    # Register tools on mcp_app directly:
    @mcp_app.tool()
    def my_tool(...):
        ...

    # Wire to Starlette
    app = Starlette(
        routes=[
            Route("/mcp", endpoint=mcp_app.http_handler(
                json_response=True,
                stateless_http=True,
            )),
        ],
        lifespan=lifespan,  # if needed
    )
    return app
```

## What Was Removed After Stateless Fix

- mcp_app registered with path='/' and stateless=True — redundant
- Mount('/', mcp_app) — caused path-stripping conflicts
- combined_lifespan — only needed for dual stateful+stateless coexistence

## Note on GET /mcp in Stateless Mode

In stateless mode, GET /mcp returns 405 Method Not Allowed. FastMCP stateless mode only supports POST/DELETE. SSE streaming via GET requires stateful mode, which has the session bug. MCP clients using POST-based JSON-RPC (Claude Code, OpenClaw, etc.) work fine.

## Verification Commands

```bash
# Test POST — should return tools list:
curl -s -X POST http://127.0.0.1:8081/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# Test GET — returns 405 in stateless mode (expected):
curl -s http://127.0.0.1:8081/mcp \
  -H "Accept: application/json, text/event-stream"

# Full federation sweep:
for url in \
  "https://arifos.arif-fazil.com/mcp" \
  "https://geox.arif-fazil.com/mcp" \
  "https://wealth.arif-fazil.com/mcp" \
  "https://well.arif-fazil.com/mcp"; do
  echo -n "$url: "
  curl -s -o /dev/null -w "%{http_code}" -X POST "$url" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
  echo
done
```

## Key Files

- /root/geox/server.py — APP_CREATION section
- /root/arifOS/arifosmcp/runtime/server.py:560 — arifOS reference (stateless_http=True)
- MCP SDK: mcp/server/streamable_http.py (~line 844) — _validate_session source

## Related Skills

- arifos-mcp-surface-debug — MCP surface debugging protocol
- arifos-mcp-streamable-http-debug — Accept-header transport debugging
