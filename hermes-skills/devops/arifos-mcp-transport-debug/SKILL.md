---
name: arifos-mcp-transport-debug
description: Debug and fix MCP transport issues across arifOS federation — 406 errors, SSE vs streamable-http, Accept header enforcement in FastMCP 3.2.4
category: devops
---

# arifOS MCP Transport Debug & Fix

## When to Use

- MCP endpoint returns HTTP 406 Not Acceptable
- OpenClaw bundle fails to initialize a federated MCP server
- Federation MCP probe succeeds but bundle init fails with "Method not found"
- Transport mismatch between config file and running container

## MCP Transport Taxonomy (FastMCP 3.2.4)

| Transport | Config | Accept Header | Session | Use Case |
|-----------|--------|---------------|---------|----------|
| `http_app(stateless_http=True)` | `stateless_http=True` | Not required | None | arifOS legacy |
| `http_app(transport="streamable-http", json_response=True, stateless_http=True)` + patch | `streamable-http` | Required (patched) | None | WELL, GEOX (fixed) |
| `transport='sse'` | N/A | SSE events | Stateful | WEALTH legacy |
| `transport='streamable-http'` | FastMCP settings | Required | Required | Standard remote MCP |

## Diagnostic Commands

```bash
# 1. Probe all 4 endpoints
ssh root@af-forge "python3 -c \"
import urllib.request, json
endpoints = [('arifOS','http://127.0.0.1:8080/mcp'),('WELL','http://127.0.0.1:8083/mcp'),('WEALTH','http://127.0.0.1:8082/mcp'),('GEOX','http://127.0.0.1:8081/mcp')]
h = {'Content-Type': 'application/json', 'Accept': 'application/json'}
for name, url in endpoints:
    body = json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/list','params':{}}).encode()
    req = urllib.request.Request(url, data=body, headers=h, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            resp = json.loads(r.read())
            tools = resp.get('result',{}).get('tools',[])
            print(name + ': OK (' + str(len(tools)) + ' tools)')
    except Exception as e:
        print(name + ': FAIL ' + str(type(e).__name__))
\""

# 2. Check container entrypoint / server.py transport config
ssh root@af-forge "docker exec <container> grep -n 'http_app\|transport=' /app/server.py | head -10"
ssh root@af-forge "docker exec <container> cat /app/entrypoint.sh 2>/dev/null"

# 3. Check fastmcp.json (may be stale — entrypoint overrides it)
ssh root@af-forge "docker exec <container> cat /app/fastmcp.json 2>/dev/null"

# 4. Check container logs
ssh root@af-forge "docker logs <container> --tail 20 2>&1"
```

## FastMCP 3.2.4 — The 406 Root Cause

FastMCP's `StreamableHTTPServerTransport._check_accept_headers` returns 406 if the request's Accept header doesn't explicitly include `application/json` or `text/event-stream`. Generic HTTP clients (curl, urllib, some MCP bundles) send `Accept: */*` or no Accept header → 406.

**Two fix patterns:**

### Pattern A — Fix the server (recommended)
Add monkey-patch + set flags in `http_app()`:

```python
# In server.py, before if __name__ == "__main__":
from mcp.server.streamable_http import StreamableHTTPServerTransport
_orig_check = StreamableHTTPServerTransport._check_accept_headers
def _patched_check(self, request):
    if getattr(self, 'is_json_response_enabled', False):
        return True, True  # Accept both JSON and SSE
    return _orig_check(self, request)
StreamableHTTPServerTransport._check_accept_headers = _patched_check

# In http_app() call:
app = mcp.http_app(
    path="/mcp",
    transport="streamable-http",
    json_response=True,      # Required for patch to work
    stateless_http=True      # Avoids session ID validation
)
```

### Pattern B — Fix WEALTH entrypoint (SSE → streamable-http)

WEALTH entrypoint uses `transport='sse'` which is incompatible with OpenClaw bundle:
```bash
# In /app/entrypoint.sh:
# Before:
exec python -c "from internal.monolith import mcp; mcp.run(transport='sse', show_banner=False)"
# After:
exec python -c "from internal.monolith import mcp; mcp.run(transport='streamable-http', show_banner=False)"
```

## Apply Fix and Restart

```bash
# Fix server.py (use sed or python inline)
ssh root@af-forge "docker exec <container> sed -i 's|http_app(path=\"/mcp\", transport=\"streamable-http\")|http_app(path=\"/mcp\", transport=\"streamable-http\", json_response=True, stateless_http=True)|' /app/server.py"

# Restart
ssh root@af-forge "docker restart <container> && sleep 3 && docker ps --filter name=<container> --format '{{.Names}}: {{.Status}}'"
```

## Transport Map (Current State — May 2026)

| Node | Container | Transport | Fix Applied | Tools | Accept Header |
|------|-----------|-----------|-------------|-------|--------------|
| arifOS | arifosmcp | `stateless_http=True` (legacy http_app) | openclaw.json header workaround | 18 | ✅ 200 with `Accept: application/json` |
| WELL | well | `streamable-http` + patch | ✅ json_response + stateless + monkey-patch | 45 | ✅ 200 even with `*/*` |
| WEALTH | wealth-organ | `streamable-http` (was SSE) | ✅ entrypoint.sh fixed | 50 | ✅ 200 |
| GEOX | geox_eic | `streamable-http` + patch | ✅ already correct | 15 | ✅ 200 even with `*/*` |

**Critical insight:** arifOS has `json_response=True` in http_app() but STILL returns 406 without Accept header. The monkey-patch (which GEOX and WELL have) is what makes `Accept: */*` work. arifOS lacks the patch — hence the openclaw.json workaround.

**httpx verification test (from af-forge host):**
```bash
ssh root@af-forge "python3 -c \"
import httpx, asyncio
async def test():
    for url, accept in [('http://127.0.0.1:8080/mcp','none'),('http://127.0.0.1:8080/mcp','json'),('http://127.0.0.1:8082/mcp','none')]:
        h = {'Content-Type':'application/json'}
        if accept == 'json': h['Accept'] = 'application/json'
        r = await httpx.AsyncClient().post(url, json={'jsonrpc':'2.0','method':'initialize','id':1,'params':{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'test','version':'1.0'}}}, headers=h, timeout=5)
        print(f'{url} Accept={accept}: {r.status_code}')
asyncio.run(test())
\""
# Expected: arifOS no Accept→406, arifOS with Accept→200, WEALTH no Accept→200
```

## Key Files

- WELL server.py: `/app/server.py` (container), backed up as `/app/server.py.bak`
- WEALTH entrypoint: `/app/entrypoint.sh`
- OpenClaw config: `~/.openclaw/openclaw.json`

## Verification

After fix, all 4 should return 200 with tool lists:
```bash
# Full federation probe
ssh root@af-forge "for port in 8080 8081 8082 8083; do curl -s -m 3 http://127.0.0.1:$port/mcp -H 'Content-Type: application/json' -H 'Accept: application/json' -X POST -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/list\",\"params\":{}}' 2>&1 | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get(\"result\",{}).get(\"tools\",[]).__len__())' 2>/dev/null || echo \"FAIL\"; done"
```

## Troubleshooting: When Curl Hangs but Port is Open

**Symptom:** `curl http://127.0.0.1:PORT/mcp` hangs indefinitely even though `docker ps` shows the container running.

**Root cause:** The MCP server is healthy but the request/response cycle is slow or stuck (HTTP pipeline issue, server-side hang, or KeepAlive mismatch).

**Workaround chain (in order):**

```bash
# Step 1: Verify port is actually listening
nc -z -w3 127.0.0.1 8082 && echo "port open" || echo "port closed"

# Step 2: Try with explicit short timeout and no KeepAlive
curl -s --max-time 8 --noproxy '*' -H "Content-Type: application/json" -H "Accept: application/json" \
  -X POST http://127.0.0.1:8082/mcp \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' | head -c 200

# Step 3: Inspect container files directly (bypass network entirely)
docker exec <container> cat /app/entrypoint.sh
docker exec <container> grep -n 'transport\|http_app\|mcp.run' /app/server.py | head -10

# Step 4: Check container health status
docker ps --format "{{.Names}} {{.Status}}" | grep -E 'WEALTH|GEOX|WELL|arifOS'
```

## Critical Insight: Local Source Files vs Running Container

Local source files (e.g., `/root/WEALTH/entrypoint.sh`, `/root/geox/fastmcp.json`) are frequently **stale** compared to what's actually running in containers. A container might be running the correct fixed code even though the local source file still shows the old buggy version.

**Always verify runtime state inside the container, not from local files:**

```bash
# Inspect what's ACTUALLY running (authoritative)
docker exec wealth-organ cat /app/entrypoint.sh
docker exec geox_eic grep 'transport=' /app/server.py

# Then compare with local source
cat /root/WEALTH/entrypoint.sh
cat /root/geox/fastmcp.json
```

The transport shown by `docker exec` is ground truth. The local file is the plan that may not have been applied yet.

## Gateway /mcp Returns 404 — Normal Behavior

The OpenClaw gateway (port 18789) WebSocket endpoint (`/mcp`) returning `404 Not Found` when called with plain HTTP POST is **expected**. The gateway routes MCP over WebSocket, not over HTTP. The 404 means the HTTP path doesn't have an MCP handler — which is correct behavior.

To probe the gateway's aggregated MCP bundle, use the OpenClaw CLI:
```bash
openclaw mcp list  # list all known MCP servers
openclaw bundle list  # list bundle configurations
```

Do NOT use `curl -X POST http://127.0.0.1:18789/mcp` to test — it will always 404. Use the OpenClaw CLI or test the individual container endpoints directly.
