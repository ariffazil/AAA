---
name: arifos-mcp-streamable-http-debug
description: Diagnose and fix MCP transport — making arifOS federation MCP servers accept plain JSON POSTs from any client (no SSE headers, no session ID required)
triggers:
  - "HTTP 406 on /mcp"
  - "HTTP 400 Bad Request: Missing session ID"
  - "Not Acceptable: Client must accept both application/json and text/event-stream"
  - "Not Acceptable: Client must accept application/json"
  - "MCP endpoint works for OpenClaw but fails with curl/Postman"
  - "curl works but browser/fetch fails with 406"
  - "MCP SSE probe returned an unsupported content type from arif-fazil.com: application/json"
---

# arifOS MCP Open-Access Transport Fix

## The Goal
Make all 4 federation MCP servers accept **plain JSON POST** from **any client** — curl, Postman, browser fetch, any language HTTP library. No SSE headers. No session tracking. No special Accept header required.

## Architecture: 3 MCP Implementations in the Federation

arifOS runs **three distinct MCP HTTP transport architectures** — not all the same:

| Service | Transport Architecture | Accept Header Bug? |
|---------|----------------------|-------------------|
| **arifOS** | FastMCP `mcp.http_app()` + monkey-patch | ✅ Fixed |
| **WEALTH** | Custom Starlette wrapper (`/mcp` → direct JSON-RPC) | ✅ Never had it (JSON-only) |
| **WELL** | FastMCP `mcp.http_app()` + monkey-patch | ✅ Fixed |
| **GEOX** | FastMCP `mcp.http_app(path="/mcp")` + monkey-patch (2026-05-04) | ✅ Fixed |

**Key insight:** WEALTH and old GEOX (Starlette wrapper) never hit the Accept-header bug
BUT they only support JSON responses — SSE-capable MCP clients get `application/json`
when they expect `text/event-stream`, causing "unsupported content type" errors.
The FastMCP `http_app()` path handles both protocols correctly.

## Root Cause A — The MCP Library Accept Header Bug

**Symptom:** HTTP 406 with messages like:
- `"Client must accept both application/json and text/event-stream"`
- `"Client must accept application/json"`

**Root cause location:** `mcp/server/streamable_http.py` — `StreamableHTTPServerTransport._check_accept_headers()`. When `is_json_response_enabled=True`, it still checks that `application/json` is explicitly present in Accept, and `*/*` (curl's default) doesn't satisfy this.

**The fix:** monkey-patch `_check_accept_headers` OR have clients send `Accept: application/json`.

## Root Cause B — The Stateful Session Lifecycle Bug (CRITICAL)

**Symptom:** HTTP 400 — `"Bad Request: Missing session ID"`

This is **NOT** an Accept header problem. It occurs when `stateless_http=False` (stateful mode), even with the Accept header fix applied.

**Root cause:** MCP SDK's stateful session handshake has a chicken-and-egg flaw:

1. Client sends POST with `Accept: text/event-stream` → no `MCP-Session-Id` header
2. `handle_request()` → `create_session()` → session created, `mcp_session_id` set on transport
3. `_is_session_valid()` called → `mcp_session_id is not None` (truthy) → requires session ID in request
4. No session ID in request (client hasn't received one yet) → **400 "Missing session ID"**

**This is the exact bug that broke GEOX (commit `4dc8a5fe`):**
```
stateless_http=False  →  mcp_session_id IS set  →  validation requires session ID
stateless_http=True   →  mcp_session_id = None  →  validation skipped entirely
```

arifOS uses `stateless_http=True` everywhere. GEOX had `stateless_http=False` on the `/mcp` route.

**The fix:** Always use `stateless_http=True` for public endpoints:

```python
# WRONG — breaks with "Missing session ID" in production:
mcp.http_app(path="/mcp", json_response=True, stateless_http=False)

# CORRECT — stateless mode, no session tracking:
mcp.http_app(path="/mcp", transport="streamable-http", json_response=True, stateless_http=True)
```

**Note on GET endpoints:** In stateless mode, `mcp.http_app()` returns 405 Method Not Allowed for GET requests. This is a FastMCP limitation — GET is used for SSE streaming initialization in stateful mode. For stateless production MCP, use POST-based JSON-RPC for all requests.

## How to Tell Which Root Cause You're Facing

| Error | Root cause | Fix |
|-------|-----------|-----|
| 406 "must accept both" | Accept header + `json_response=False` | Add `json_response=True` + patch |
| 406 "must accept application/json" | Accept header bug | Add monkey-patch OR `Accept: application/json` |
| **400 "Missing session ID"** | **`stateless_http=False`** | **Change to `stateless_http=True`** |
| 200 but `tools: []` | Wrong mount path | Check route mapping |

**Diagnosis command:**
```bash
# Inside the container — check what flags were actually passed
docker exec <container> python3 -c "
    from mcp.server.streamable_http_manager import StreamableHTTPSessionManager as M
    import inspect
    print(inspect.signature(M.__init__))
"
```
# This FAILS with HTTP 406 even with json_response=True:
curl -X POST https://arifos.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
# curl sends Accept: */* by default — MCP library rejects it

# This WORKS:
curl -X POST https://arifos.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

**Root cause location:** `mcp/server/streamable_http.py` — `StreamableHTTPServerTransport._check_accept_headers()`. When `is_json_response_enabled=True`, it still checks that `application/json` is explicitly present in Accept, and `*/*` (curl's default) doesn't satisfy this.

**The monkey-patch fix:**
```python
from mcp.server.streamable_http import StreamableHTTPServerTransport
_orig = StreamableHTTPServerTransport._check_accept_headers

def _patched_check(self, request):
    # Let */* through when json_response is enabled
    accept = request.headers.get("Accept", "")
    if accept == "*/*" and self._is_json_response_enabled:
        return  # Accept everything — skip the strict check
    return _orig(self, request)

StreamableHTTPServerTransport._check_accept_headers = _patched_check
```

Place this **before** the `http_app()` call in the server file.

## The 3-Layer FastMCP Transport Problem (for pure FastMCP services)

FastMCP's HTTP transport has **three independent layers**, each with different Accept header behavior:

| Transport | json_response | stateless_http | Accept header required | Works for plain curl? |
|-----------|---------------|----------------|----------------------|----------------------|
| `"http"` (default) | False | False | **Both** `application/json` + `text/event-stream` | ❌ |
| `"streamable-http"` | False | False | **Both** `application/json` + `text/event-stream` | ❌ |
| `"streamable-http"` | **True** | False | `application/json` + session ID in request | ❌ (needs session) |
| `"streamable-http"` | **True** | **True** | `application/json` only | ❌ (still needs explicit Accept!) |

**The critical discovery (2026-05-04):** `transport="streamable-http"` + `json_response=True` + `stateless_http=True` is still NOT sufficient for generic HTTP clients. The Accept header bug means you ALSO need the monkey-patch OR `Accept: application/json` header.

**Error messages tell you exactly which layers are broken:**
- `"Client must accept both application/json and text/event-stream"` → needs `json_response=True`
- `"Client must accept application/json"` → needs `stateless_http=True` + monkey-patch
- `"Bad Request: Missing session ID"` → still has `stateless_http=False` (session tracking required)

## Diagnosis Steps

```bash
# Step 1: Test with plain JSON POST (no Accept header — what curl sends by default)
curl -s "https://arifos.arif-fazil.com/mcp" -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' 2>&1

# Step 2: Identify which error you get
# 406 "both json and sse"       → json_response NOT set to True
# 406 "application/json only"   → json_response=True but */* not recognized → monkey-patch needed
# 400 "Missing session ID"      → stateless_http still False
# 200 with tools:0             → works but wrong Accept header (add Accept: application/json)
# 200 with tools:N             → WORKING

# Step 3: Verify the running code has the fix
docker exec <container> grep -n "StreamableHTTPServerTransport\|_check_accept_headers\|json_response" /app/server.py 2>/dev/null | head -5
```

## The 4 Services — Correct Fix

### arifOS (Python/FastMCP)
**File:** `/root/arifOS/arifosmcp/server.py` — add monkey-patch before `http_app()` call (~line 233):
```python
# ── Monkey-patch: Accept */* when json_response is enabled ───────────────
from mcp.server.streamable_http import StreamableHTTPServerTransport
_orig = StreamableHTTPServerTransport._check_accept_headers

def _patched_check(self, request):
    accept = request.headers.get("Accept", "")
    if accept == "*/*" and self._is_json_response_enabled:
        return
    return _orig(self, request)

StreamableHTTPServerTransport._check_accept_headers = _patched_check

app = mcp.http_app(
    transport="streamable-http",
    json_response=True,
    stateless_http=True,
)
```

**Dockerfile** (for future image builds):
```dockerfile
ENV AAA_MCP_TRANSPORT=streamable-http
```

After fixing the file, rebuild + restart + reconnect to network:
```bash
cd /root/arifOS && docker build --no-cache -t ghcr.io/ariffazil/arifos:<commit> .
docker push ghcr.io/ariffazil/arifos:<commit>
docker stop arifosmcp && docker rm arifosmcp
docker run -d --name arifosmcp ... ghcr.io/ariffazil/arifos:<commit>
docker network connect <caddy_network_id> arifosmcp
```

### WEALTH — Two valid approaches

**Approach A (recommended): Custom Starlette wrapper** — bypasses FastMCP HTTP entirely for `/mcp`:
```python
# File: /root/WEALTH/internal/monolith.py — in if __name__ == "__main__"
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse as _JR

async def legacy_mcp_handler(request):
    """Direct JSON-RPC handler — bypasses FastMCP Accept-header enforcement."""
    if request.method == "GET":
        return _JR({"mcp": "WEALTH", "transport": "streamable-http"})
    payload = await request.json()
    method = payload.get("method")
    params = payload.get("params", {})
    response_id = payload.get("id")

    if method == "tools/list":
        all_tools = await mcp.list_tools()
        return _JR({
            "jsonrpc": "2.0", "id": response_id,
            "result": {"tools": [{"name": t.name, "description": t.description,
              "inputSchema": getattr(t, "inputSchema", {})} for t in all_tools]}
        })
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})
        result = await mcp.call_tool(name, arguments)
        return _JR({"jsonrpc": "2.0", "id": response_id, "result": result})
    return _JR({"jsonrpc": "2.0", "id": response_id,
                 "error": {"code": -32601, "message": "Method not found"}}, status_code=404)

mcp_app = mcp.http_app(path="/", transport="streamable-http", stateless_http=True)
app = Starlette(routes=[
    Route("/mcp", legacy_mcp_handler, methods=["GET", "POST"]),
    Mount("/", app=mcp_app),
], lifespan=getattr(mcp_app, "lifespan", None))
```

**Approach B:** Same monkey-patch as arifOS if keeping FastMCP `http_app()` for `/mcp`.

### WELL (Python/FastMCP)
**File:** `/root/well/server.py` — same monkey-patch as arifOS before `http_app()` call (~line 3263):
```python
app = mcp.http_app(path="/mcp")  # WRONG: no transport params, no patch

# CORRECT:
from mcp.server.streamable_http import StreamableHTTPServerTransport
_orig = StreamableHTTPServerTransport._check_accept_headers
def _patched_check(self, request):
    accept = request.headers.get("Accept", "")
    if accept == "*/*" and self._is_json_response_enabled:
        return
    return _orig(self, request)
StreamableHTTPServerTransport._check_accept_headers = _patched_check

app = mcp.http_app(path="/mcp", transport="streamable-http", json_response=True, stateless_http=True)
```

### GEOX — Fixed (2026-05-04): `stateless_http=False` caused "Missing session ID"
GEOX had TWO problems:

1. **Wrong `stateless_http=False`:** The stateful session lifecycle creates a session internally,
   then immediately validates it before the client has received the session ID to echo back.
   Result: HTTP 400 "Bad Request: Missing session ID". This is the **Root Cause B** bug described above.
   Fix: change to `stateless_http=True`.

2. **Wrong content type:** `legacy_mcp_handler` always returns `application/json`.
   MCP clients probing with `Accept: text/event-stream` get JSON back → error.

**Fix applied** (`/root/geox/server.py`, committed `4dc8a5fe`):
```python
# ── Accept header patch (still needed for */* clients) ───────────────────────
from mcp.server.streamable_http import StreamableHTTPServerTransport
_orig_check = StreamableHTTPServerTransport._check_accept_headers

def _patched_check(self, request):
    accept = request.headers.get("Accept", "")
    if accept == "*/*" and self._is_json_response_enabled:
        return  # Skip strict Accept validation
    return _orig_check(self, request)

StreamableHTTPServerTransport._check_accept_headers = _patched_check

def create_app():
    mcp_http_handler = mcp.http_app(
        path="/mcp",
        transport="streamable-http",
        json_response=True,
        stateless_http=True,   # ← was False — caused "Missing session ID"
    )
    # ... routes mount mcp_http_handler on /mcp
```

**The key change is `stateless_http=True`** (line above). Without it, the Accept-header patch
alone does not fix the 400 error.
```python
# ── Monkey-patch: Accept */* when json_response is enabled ──────────────────
from mcp.server.streamable_http import StreamableHTTPServerTransport
_orig_check = StreamableHTTPServerTransport._check_accept_headers

def _patched_check(self, request):
    accept = request.headers.get("Accept", "")
    if accept == "*/*" and self._is_json_response_enabled:
        return  # Skip strict Accept validation
    return _orig_check(self, request)

StreamableHTTPServerTransport._check_accept_headers = _patched_check

def create_app():
    mcp_http_handler = mcp.http_app(
        path="/mcp",
        transport="streamable-http",
        json_response=True,
        stateless_http=True,
    )
    app = Starlette(routes=[
        ...
        Route("/mcp", mcp_http_handler, methods=["GET", "POST"]),   # ← was legacy_mcp_handler
        Route("/mcp/stream", mcp_http_handler, methods=["GET", "POST"]),  # ← was legacy_mcp_handler
        Mount("/", mcp_app),
    ], ...)
```

**`legacy_mcp_handler` is kept** (lines ~555–621) for other routes that still need it,
but `/mcp` now goes through proper FastMCP HTTP transport.

**Caddyfile header override** (no longer needed):
```caddy
# REMOVE if present — the FastMCP transport now handles this correctly
header_up Accept "text/event-stream, application/json"
```

**Verify the fix** (should return 200, not 406):
```bash
curl -s -i -X POST https://geox.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' | head -1
```

## Container Network — Caddy Can't Reach arifOS

Every container restart drops from the Caddy network. Always reconnect:
```bash
# Get Caddy network ID
docker network ls | grep caddy

# Reconnect after restart
docker network connect <caddy_network_id> arifosmcp
```

Verify:
```bash
docker inspect arifosmcp --format '{{json .NetworkSettings.Networks}}' | python3 -c "import sys,json; n=json.load(sys.stdin); print(list(n.keys()))"
```

## Full Verification — All 4 Endpoints

```bash
for svc in arifos geox wealth well; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 \
    -X POST "https://${svc}.arif-fazil.com/mcp" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}')
  echo "${svc^^} → HTTP $code"
done
```

**Expected:** all 4 return `200`.

## Key Insight

**Two independent bugs can cause MCP failures. They require different fixes.**

**Bug A — Accept header:** 406 errors even when all flags are correct → monkey-patch needed.

**Bug B — Stateful session lifecycle:** 400 "Missing session ID" when `stateless_http=False` → change to `True`.

Three flags must all be correct for pure FastMCP services:
1. `transport="streamable-http"` — enables HTTP transport
2. `json_response=True` — skips SSE requirement
3. `stateless_http=True` — skips session tracking (prevents Bug B)

With all three correct + the Accept-header patch → generic HTTP clients work.

**The golden rule (learned from GEOX incident 2026-05-04):**
> arifOS uses `stateless_http=True` everywhere. If you set it to `False` and deploy, you WILL get "Missing session ID" errors from Cloudflare-proxied clients because they never complete the full stateful handshake.
>
> Always use `stateless_http=True` for public-facing MCP endpoints. Only use `stateless_http=False` for dedicated internal clients that implement the full MCP session lifecycle (initialize → receive session ID → echo session ID on all subsequent requests).
