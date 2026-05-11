---
name: fastmcp-streamable-http-sse-gateway
description: Fix FastMCP streamable-http SSE transport behind Starlette ASGI — 405/400/500 on GET /mcp
tags: [fastmcp, mcp, sse, starlette, streamable-http]
last_updated: 2026-05-04
---

# FastMCP Streamable-HTTP SSE Gateway Fix

## Context
When mounting FastMCP's `http_app(transport="streamable-http")` inside a Starlette ASGI app for multi-endpoint routing (e.g., `/mcp` + `/`), GET requests to `/mcp` with `Accept: text/event-stream` fail with 400 or 405 depending on configuration.

## Root Causes (3 layers)

### Layer 1: `stateless_http=True` explicitly removes GET
FastMCP 3.2.4 sets `methods=["POST", "DELETE"]` when `stateless_http=True`. This was the immediate 405 cause.

### Layer 2: Missing lifespan = 500 "Task group is not initialized"
When `stateless_http=False`, the session manager runs inside an async task group. That task group is born from `mcp_app.lifespan()`. If the outer Starlette app doesn't pass the correct lifespan, the task group is never initialized → 500 on every request.

### Layer 3: `lifespan` must match the specific handler's session manager
The `mcp_http_handler` (at `/mcp`) and `mcp_app` (at `/`) each have their own session manager. Wiring `lifespan=mcp_app.lifespan` doesn't start `mcp_http_handler`'s session manager → 500.

## Solution

```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator

# Each handler needs its own session manager lifespan
@asynccontextmanager
async def combined_lifespan(app: Starlette) -> AsyncGenerator[None, None]:
    async with mcp_http_handler.lifespan(mcp_http_handler):
        async with mcp_app.lifespan(mcp_app):
            yield

app = Starlette(
    routes=[
        Route("/mcp", mcp_http_handler, methods=["GET", "POST"]),
        # ...
    ],
    lifespan=combined_lifespan,
)
```

Key parameters:
```python
mcp_http_handler = mcp.http_app(
    path="/mcp",
    transport="streamable-http",
    json_response=True,       # Required for JSON-RPC fallback
    stateless_http=False,     # MUST be False — enables GET for SSE initialization
)
```

## 400 "Missing session ID" on GET — Is It Working?

Yes, possibly. In FastMCP 3.2.4 with `stateless_http=False`:
- GET `/mcp` initiates SSE handshake
- Server assigns a session ID and sends it as `mcp-session-id` header in the SSE stream
- Client must then POST with that session ID header

**curl will always fail with 400** because it doesn't implement the MCP transport protocol. Use the actual MCP SDK client to test.

## Trigger Conditions
- FastMCP 3.2.x with `stateless_http=False`
- MCP endpoint mounted inside a parent Starlette app
- GET `/mcp` returns 405, 400, or 500

## Standalone Server 406 Fix (FastMCP 3.2.4 — WELL/GEOX Pattern)

When FastMCP 3.2.4 runs as a standalone server (not behind a parent Starlette app) with `transport="streamable-http"` and `json_response=True`, clients may still get **HTTP 406** because `StreamableHTTPServerTransport._check_accept_headers` rejects non-SSE Accept headers even when `is_json_response_enabled` is True.

**Symptoms:**
- `curl -X POST -H "Accept: application/json" -H "Content-Type: application/json"` → 406
- MCP SDK clients → 406
- Direct probe `tools/list` via POST → works in logs but fails in bundle init

**Root cause:** `_check_accept_headers` checks the raw Accept header before checking `is_json_response_enabled`.

**Solution — monkey-patch before server start:**
```python
# Patch FastMCP 3.2.4 accept-header enforcement
import os as _os
from mcp.server.fastmcp import FastMCP
from mcp.server.transport.streamable_http import StreamableHTTPServerTransport

_orig_check = StreamableHTTPServerTransport._check_accept_headers

def _patched_check(self, request):
    if getattr(self, 'is_json_response_enabled', False):
        return True, True
    return _orig_check(self, request)

StreamableHTTPServerTransport._check_accept_headers = _patched_check

# Then create the app with json_response=True
mcp = FastMCP("WELL")
app = mcp.http_app(
    path="/mcp",
    transport="streamable-http",
    json_response=True,    # Required
    stateless_http=True,   # Required for standalone
)
```

**Minimal working config for standalone streamable-http server:**
```python
app = mcp.http_app(
    path="/mcp",
    transport="streamable-http",
    json_response=True,
    stateless_http=True,
)
```

Without `json_response=True` → 406 on JSON Accept headers.
Without `stateless_http=True` → session management overhead on standalone.
Without monkey-patch → 406 even with flags set (FastMCP 3.2.4 bug).

## Verification
```bash
# curl only proves JSON works — MCP SDK proves SSE works:
mcp dev https://geox.arif-fazil.com/mcp \
  --header "Authorization: Bearer YOUR_TOKEN"
```

## VPS Deploy Pattern (GEOX)
```bash
ssh root@af-forge "docker stop geox_eic && docker rm geox_eic"
ssh root@af-forge "docker run -d \
  --name geox_eic \
  --restart unless-stopped \
  -p 127.0.0.1:8081:8000 \
  -e GEOX_HOST=0.0.0.0 \
  -e GEOX_PORT=8000 \
  -e GEOX_PROFILE=full \
  -e GEOX_SECRET_TOKEN=... \
  --memory=512m \
  ghcr.io/ariffazil/geox:b70c2ea5 \
  python server.py --host 0.0.0.0 --port 8000"
```
