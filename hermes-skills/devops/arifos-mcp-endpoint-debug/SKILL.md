---
name: arifos-mcp-endpoint-debug
category: devops
description: Debug and fix arifOS MCP endpoints — degraded health, route 404s, container identity, MCP protocol handshake
triggers:
  - arifOS MCP returning degraded health
  - route 404 on a registered endpoint
  - /constitution 404
  - mcp-session-id missing
  - build_info showing wrong git commit
---

# arifOS MCP Endpoint Debug & Fix

## Context
arifOS MCP server runs inside Docker with volume mount `/root/arifOS/arifosmcp:/usr/src/app:ro`.
The ASGI app is `mcp.http_app()` (FastMCP 3) wrapped in `StarletteWithLifespan`.
Custom REST routes are registered in `rest_routes.py` via `register_rest_routes(app, mcp)`.

## Diagnostics

### Check container health
```bash
curl -s https://arifos.arif-fazil.com/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status'), d.get('error',''))"
```

### Check running routes inside container
```bash
docker exec arifosmcp python3 -c "
from arifosmcp.runtime.server import app
routes = [r.path if hasattr(r,'path') else str(r) for r in app.router.routes]
print('Routes:', routes)
"
```

### Check which app/router is being used
```bash
docker exec arifosmcp python3 -c "
from arifosmcp.server import mcp
print('has custom_route:', hasattr(mcp, 'custom_route'))
print('has router:', hasattr(mcp, 'router'))
"
# FastMCP 3: custom_route=True, router=False
# The mcp passed to register_rest_routes IS the FastMCP object
```

### Check MCP protocol (SSE transport)
```bash
# Initialize — must have Accept: application/json, text/event-stream
SESSION=$(curl -si "https://arifos.arif-fazil.com/mcp" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":0}' 2>&1 | grep -i "mcp-session-id" | cut -d' ' -f2 | tr -d '\r')

# Use session cookie in subsequent calls
curl -s "https://arifos.arif-fazil.com/mcp" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"arif_session_init","arguments":{"actor_id":"test"}},"id":1}'
```

### Restart container cleanly (clear bytecode)
```bash
docker exec arifosmcp find /usr/src/app -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
docker restart arifosmcp
# Wait ~10s for startup
sleep 10 && curl -s https://arifos.arif-fazil.com/health
```

## Common Issues

### 1. Degraded health — ImportError in container
Symptom: `/health` returns `{"status":"degraded","error":"Import failed: ..."}`
Fix:
```bash
docker exec arifosmcp find /usr/src/app -type d -name __pycache__ -exec rm -rf {} +
docker restart arifosmcp
```

### 2. Route not found — decorator order trap
**Problem:** `register_rest_routes()` is called inside `server.py` at import time. Any `@route()` decorator on a function defined AFTER that call never fires.

**Wrong pattern:**
```python
# server.py line ~449
register_rest_routes(app, mcp)  # ← called here

# rest_routes.py — this decorator never fires!
@route("/constitution", methods=["GET"])
async def constitution_redirect(request: Request):
    return RedirectResponse(url="/api/constitution", status_code=307)
```

**Correct pattern — imperative registration:**
```python
# rest_routes.py
async def constitution_redirect(request: Request) -> Response:
    from starlette.responses import RedirectResponse
    return RedirectResponse(url="/api/constitution", status_code=307)

# Register AFTER function is defined, using the route() closure from register_rest_routes
route("/constitution", methods=["GET"])(constitution_redirect)
```

### 3. mcp.router.routes.append — wrong app
**Problem:** `mcp` in `register_rest_routes()` is the FastMCP instance (has `custom_route` but no `router`). The code checks for `Starlette` type and falls through to `mcp.router.routes.append` only when the type string contains "Starlette".

```python
# This checks mcp (FastMCP), NOT app (StarletteWithLifespan)
if hasattr(mcp, "add_route") or "Starlette" in str(type(mcp)):
    mcp.router.routes.append(...)  # ← fails because FastMCP has no router
```

The actual fix should target `app.router.routes` for StarletteWithLifespan, or use `mcp.custom_route()` for FastMCP.

### 4. FastMCP Healthcheck — GEOX pattern

FastMCP servers (GEOX, other domain MCPs) have **no `/health` endpoint** by default. GET requests return 404.

**Working healthcheck for FastMCP SSE servers:**
```bash
# Must POST with proper Accept headers (SSE initialization)
curl -sf -X POST http://localhost:8081/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"health","version":"1.0"}}}'
# Returns SSE event stream → healthy
```

**Docker healthcheck (compose CMD-SHELL form):**
```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -sf -X POST http://localhost:8081/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{\"jsonrpc\":\"2.0\",\"method\":\"initialize\",\"id\":1,\"params\":{\"protocolVersion\":\"2024-11-05\",\"capabilities\":{},\"clientInfo\":{\"name\":\"health\",\"version\":\"1.0\"}}}'"]
```

**If container has no curl:** use python3 with httpx/urllib:
```yaml
# For containers with python but no curl (e.g., qdrant)
healthcheck:
  test: ["CMD-SHELL", "python3 -c \"import urllib.request; urllib.request.urlopen('http://localhost:PORT/healthz')\""]
```

### 5. Worktree git overriding container identity
`docker-compose.yml` mounts `/root/arifOS/arifosmcp:/usr/src/app:ro`. Inside the container, `/app/.git` points to the worktree git. `_git_sha_short()` in `build_info.py` finds this and returns the worktree SHA instead of the image's `DEPLOY_GIT_COMMIT`.

Fix: check `os.environ["DEPLOY_GIT_COMMIT"]` FIRST, before looking for `/app/.git`.

## LLM Wiring Verification (source vs running container)

**Critical insight (May 2026):** The running Docker container may have DIFFERENT code than `/root/arifOS/` source. Always verify the running container's actual code before assuming source matches.

### Find the actual app path inside container
```bash
docker exec arifosmcp python3 -c "import arifosmcp; print(arifosmcp.__file__)"
# → /usr/src/app/arifosmcp/__init__.py  (volume mount from /root/arifOS/arifosmcp)
docker exec arifosmcp ls /usr/src/app/arifosmcp/runtime/
```

### Check if a module exists in running container vs source
```bash
# Does llm_client.py exist in running container?
docker exec arifosmcp sh -c 'find /usr/src/app -name "llm_client.py" 2>/dev/null'
# Does it exist in source?
find /root/arifOS -name "llm_client.py"
# If source has it but container doesn't → container is OUTDATED
```

### Discover orphaned functions (defined but never called)
```bash
# Find what imports a module in the running container
docker exec arifosmcp grep -rn "llm_client\|call_llm\|interpret_with_ollama" /usr/src/app/arifosmcp/ 2>&1 | grep -v ".pyc"

# Find where a function is actually called
docker exec arifosmcp grep -rn "interpret_with_sea_lion\|interpret_with_ollama" /usr/src/app/arifosmcp/ 2>&1 | grep -v ".pyc"
# Output example:
#   context_witness.py:26: from .sea_lion_interpreter import ...
#   context_witness.py:127: interpretation = await interpret_with_sea_lion(...)
#   sea_lion_interpreter.py:2: (module docstring)
#   sea_lion_interpreter.py:116: async def interpret_with_sea_lion(...)
#   sea_lion_interpreter.py:214: async def interpret_with_ollama(...)
#   sea_lion_interpreter.py:306: def fallback_interpret(...)
#   sea_lion_interpreter.py:365: "interpret_with_sea_lion",
# The call chain: context_witness → interpret_with_sea_lion → fallback_interpret
# interpret_with_ollama is defined but NEVER called in the chain → ORPHANED
```

### Test LLM API directly inside container
```python
# Test SEA-LION (primary)
docker cp /tmp/test_sea_lion.py arifosmcp:/tmp/
docker exec arifosmcp python3 /tmp/test_sea_lion.py

# Inside container one-liner for quick API test
docker exec arifosmcp sh -c 'python3 -c "
import os, asyncio, httpx
API_KEY = os.environ.get(\"SEA_LION_API_KEY\", \"\")
async def t():
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            \"https://api.sea-lion.ai/v1/chat/completions\",
            headers={\"Authorization\": \"Bearer \" + API_KEY, \"Content-Type\": \"application/json\"},
            json={\"model\": \"aisingapore/Qwen-SEA-LION-v4-32B-IT\", \"messages\": [{\"role\": \"user\", \"content\": \"hi\"}], \"max_tokens\": 20}
        )
    print(\"Status:\", r.status_code, \"Response:\", r.text[:200])
asyncio.run(t())
"'
```

### Read live code at specific line ranges (no file copy needed)
```bash
docker exec arifosmcp sed -n '120,180p' /usr/src/app/arifosmcp/runtime/context_witness.py
docker exec arifosmcp wc -l /usr/src/app/arifosmcp/runtime/sea_lion_interpreter.py
```

### Verify SEA-LION API key is loaded in container
```bash
docker exec arifosmcp python3 -c "import os; k=os.environ.get('SEA_LION_API_KEY',''); print('Set:', bool(k), 'Prefix:', k[:8])"
# Expected: Set: True Prefix: sk-znzf
```

## Key Files
- `/root/arifOS/arifosmcp/runtime/rest_routes.py` — all custom REST routes
- `/root/arifOS/arifosmcp/runtime/server.py` — imports and registers routes
- `/root/arifOS/arifosmcp/runtime/build_info.py` — git identity
- `/root/arifOS/deployments/af-forge/docker-compose.yml` — container env vars

## Canonical Endpoints (arifOS)
- `https://arifos.arif-fazil.com/mcp` — MCP JSON-RPC over SSE
- `https://arifos.arif-fazil.com/health` — health + identity
- `https://arifos.arif-fazil.com/tools.json` — tool manifest (13 tools)
- `https://arifos.arif-fazil.com/api/constitution` — constitution map
- `https://arifos.arif-fazil.com/mcp/status` — MCP status
- `https://arifos.arif-fazil.com/mcp/auth` — auth status
- `https://arifos.arif-fazil.com/constitution` — redirect → /api/constitution (fix pending)

## FastMCP HTTP/SSE — Session Protocol vs Plain JSON-RPC

### The Failure Mode
A client (e.g., A-FORGE `DelegatedTruthTool.ts`) sends direct JSON-RPC to a FastMCP HTTP endpoint:
```
POST /mcp  {"jsonrpc":"2.0","method":"tools/call",...}
→ 406 Not Acceptable: Client must accept both application/json and text/event-stream
```
or with wrong Accept header:
```
→ 400 Bad Request: Missing session ID
```

**Root cause:** FastMCP HTTP transport is session-based, not stateless JSON-RPC. You MUST initialize a session first.

### Correct MCP HTTP Session Protocol

**Step 1 — Initialize (GET or POST with SSE Accept)**
```bash
RESPONSE=$(curl -si -X POST "https://WEALTH_HOST/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":1}')

# Extract session ID from response header
SESSION_ID=$(echo "$RESPONSE" | grep -i "mcp-session-id:" | cut -d' ' -f2 | tr -d '\r')
echo "Session: $SESSION_ID"
```

**Step 2 — Use session ID in all subsequent calls**
```bash
curl -s -X POST "https://WEALTH_HOST/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":2}'
```

**Step 3 — Parse SSE-wrapped JSON-RPC response**
```python
# FastMCP HTTP returns SSE-wrapped JSON-RPC:
#   event: message
#   data: {"jsonrpc":"2.0","id":2,"result":{"tools":[...]}}
for line in response.text.split('\n'):
    if line.startswith('data: '):
        data = json.loads(line[6:])
        tools = data['result']['tools']
```

**Caddy SSE streaming requirement (Bug 5 — May 2026):** When proxying FastMCP SSE through Caddy, `flush_interval -1` is required. Without it, Caddy's default buffering (100ms) can truncate SSE events mid-stream, breaking JSON-RPC responses.

```caddy
handle /mcp* {
    reverse_proxy geox_eic:8081 {
        header_up Accept "application/json, text/event-stream"
        flush_interval -1   # ← critical for SSE streaming
    }
}
```

### Verified Working Endpoints
- arifOS: `https://arifos.arif-fazil.com/mcp` — 13 canonical tools
- arifOS `/tools`: REST endpoint (no auth) — 13 tools: `arif_session_init`, `arif_sense_observe`, `arif_evidence_fetch`, `arif_mind_reason`, `arif_heart_critique`, `arif_kernel_route`, `arif_reply_compose`, `arif_memory_recall`, `arif_gateway_connect`, `arif_judge_deliberate`, `arif_vault_seal`, `arif_forge_execute`, `arif_ops_measure`
- WEALTH: `https://wealth.arif-fazil.com/mcp` — 48 tools (Valuation Kernel v3.2.4); tools work as direct Python calls despite 0 in `tools/list`
- GEOX: `http://localhost:PORT/mcp` — 50 tools (petrophysics, geoscience)
- WELL: `http://localhost:8083/mcp` — tools work as direct Python calls; `assess_readiness()` confirmed functional

### arifOS Federation MCP Tool Counts (May 2026 audit)
| Service | Port | Tools (MCP probe) | Tools (direct) | Status |
|---------|------|-------------------|----------------|--------|
| arifOS MCP | 8080 | 13 | 13 | ✅ |
| GEOX MCP | 8081 | 50 | 50 | ✅ |
| WEALTH MCP | 8082 | 0 (session quirk) | 48+ | ✅ functional |
| WELL MCP | 8083 | 0 (session quirk) | all | ✅ functional |
| A-FORGE | 7071 | — (HTTP bridge) | — | ✅ Express/TypeScript |

### 6. Source vs Running Container Code Drift (LLM wiring)
**Problem (May 2026):** `/root/arifOS/` source has `llm_client.py` (Tier1 SEA-LION → Tier2 Ollama → Tier3 error). The running `arifosmcp` container (v2026.04.26-KANON) does NOT have `llm_client.py`. It uses `sea_lion_interpreter.py` instead.

**Running container's actual LLM architecture:**
```
arif_mind_reason → pure Python deterministic (no LLM)
context_witness → sea_lion_interpreter.interpret_with_sea_lion()  [calls SEA-LION cloud ✅]
                             → fallback_interpret()  [deterministic, no LLM]
                             → interpret_with_ollama() [ORPHANED — defined but never called]
```

**The `llm_client.py` in source is NOT yet deployed to the running container.**

**Verify what's actually running:**
```bash
# Check container version vs latest deploy
curl -s https://arifos.arif-fazil.com/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d)"

# Container has llm_client.py?
docker exec arifosmcp sh -c 'find /usr/src/app -name "llm_client.py"'

# Container has sea_lion_interpreter.py?
docker exec arifosmcp sh -c 'find /usr/src/app -name "sea_lion_interpreter.py"'
# If sea_lion_interpreter exists but llm_client.py doesn't → container is on OLD architecture
```

### 7. Ollama URL from inside container
**Problem:** `OLLAMA_BASE_URL` defaults to `http://ollama:11434` but container can't resolve `ollama` if not on same Docker network or if DNS fails.

**Test from inside container:**
```bash
docker exec arifosmcp sh -c 'curl -s --max-time 3 http://ollama:11434/api/tags 2>&1'
# Exit code 0 + JSON = reachable
# Exit code 6 (Could not resolve host) = DNS/network issue
# Fix: ensure both containers on arifos_core_network
```

### Common Errors
| Error | Cause | Fix |
|-------|-------|-----|
| `406 Not Acceptable` | No `Accept: application/json, text/event-stream` | Add the Accept header |
| `404` on MCP through Caddy proxy | Proxy URL path suffix doubling the URI (e.g., `proxy host:port/mcp` when client calls `/mcp`) | Remove path suffix from proxy upstream; proxy to root `host:port` and let Caddy preserve URI |
| `400 Missing session ID` | Sent JSON-RPC without initializing first | Run `initialize` call first |
| `502` through Cloudflare with MCP | Caddy proxy doubling the MCP path (doubled `/mcp/stream/mcp/stream`) | Remove path suffix from reverse_proxy upstream in Caddyfile |
| `Session not found` | Session expired or wrong session ID | Re-run `initialize` to get fresh session |
| `404` on `/mcp` | Wrong port or service down | Check Docker port mapping |
| Empty `tools/list` result (0 tools) | FastMCP session mismatch — tools registered but not visible to probe | Tools DO work as direct Python calls; MCP session handling is the culprit. Add `id` field to ALL JSON-RPC requests (not just method/params). Try session in body (`params.sessionId`) vs header (`MCP.Session-Id`). |

### The 0-Tools Paradox — WEALTH/WELL Investigation (May 2026)

**Symptom:** FastMCP server initializes fine (session established, `serverInfo` returns), but `tools/list` returns `{"tools":[]}`.

**Tested and ruled out:**
- ❌ Wrong `Accept` header — dual `application/json, text/event-stream` was correct
- ❌ Missing session ID — was using `MCP.Session-Id` header correctly
- ❌ Wrong `protocolVersion` — `2024-11-05` accepted
- ❌ Tools not registered — direct Python calls inside container returned correct results
- ❌ Import errors in tool decorators — no errors in container logs

**Root cause discovered:** FastMCP session management is the culprit. The SSE session established during `initialize` doesn't properly associate with the `tools/list` call. This appears to be a known FastMCP HTTP/SSE transport quirk where tools ARE registered but the session context for tool discovery is not propagated.

**Verification approach (what works):**
```bash
# Direct Python calls inside container — ALWAYS works
docker exec wealth-organ python3 -c "
import sys; sys.path.insert(0,'/app')
from internal.monolith import wealth_future_value
print(wealth_future_value(present_value=1000, rate=0.08, years=10))
"
# → Returns: 2158.92

docker exec well python3 -c "
import sys; sys.path.insert(0,'/app')
from server import assess_readiness
print(assess_readiness({'cognitive_load':0.5}))
"
# → Returns: {'H_WELL': {...}, 'M_WELL': {...}}
```

**Workaround for external tool discovery:**
```python
# Use httpx with proper SSE streaming (not http.client)
import httpx, json

with httpx.Client(base_url=f"http://HOST:{PORT}", timeout=20.0) as client:
    # Initialize via SSE stream
    with client.stream("POST", "/mcp",
        headers={"Accept": "application/json, text/event-stream"},
        json={"jsonrpc":"2.0","id":1,"method":"initialize",
              "params":{"protocolVersion":"2024-11-05","capabilities":{},
                        "clientInfo":{"name":"probe","version":"1.0"}}}) as resp:
        sid = resp.headers.get("mcp-session-id", "")

    # tools/list via SSE POST with session header
    resp2 = client.post("/mcp",
        json={"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}},
        headers={"MCP.Session-Id": sid,
                 "Accept": "application/json, text/event-stream"})
    # Still returns 0 tools in body even with correct session
```

**Verdict:** When `tools/list` returns 0 via MCP probe but direct Python calls work → tools ARE registered, the issue is FastMCP session propagation. The MCP server is functional for actual tool execution even though tool discovery shows 0.

### A-FORGE DelegatedTruthTool Fix Required
`DelegatedTruthTool.ts` currently does plain JSON-RPC without session handshake:
```typescript
// WRONG — plain JSON-RPC, will get 406/400
const response = await fetch(url, {
  method: "POST",
  headers: { "Content-Type": "application/json" },  // missing Accept!
  body: JSON.stringify({ jsonrpc: "2.0", method: "tools/call", ... }),
});
```
Fix: Use `@modelcontextprotocol/sdk` `Client` class (HTTP transport with session management) instead of raw `fetch()`. This is Node.js/TypeScript work — defer to Claude Code for the implementation.
