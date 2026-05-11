---
name: mcp-transport-debug
description: Debug MCP transport mismatches on arifOS federation — config-vs-runtime drift, streamable-http vs SSE vs legacy http_app, Accept header enforcement. Use when an MCP endpoint returns 406, 400, or "Method not found" from OpenClaw bundle but curl to localhost works.
category: devops
tags: ["mcp", "fastmcp", "transport", "streamable-http", "arifOS", "vps"]
---

# MCP Transport Debug — Config vs Runtime Mismatch

## The Core Trap

**fastmcp.json says one thing; the running container does another.**

`/app/entrypoint.sh` in the container often hardcodes the transport and overrides the config. The fastmcp.json file is stale. Always inspect **live container state** first.

## Diagnostic Sequence

### Step 1 — Probe all 4 federation MCP endpoints

```bash
python3 -c "
import urllib.request, json
endpoints = [
    ('arifOS', 'http://127.0.0.1:8080/mcp'),
    ('WELL',   'http://127.0.0.1:8083/mcp'),
    ('WEALTH', 'http://127.0.0.1:8082/mcp'),
    ('GEOX',   'http://127.0.0.1:8081/mcp'),
]
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list', 'params': {}}).encode()
for name, url in endpoints:
    try:
        req = urllib.request.Request(url, data=body, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=5) as r:
            resp = json.loads(r.read())
            tools = resp.get('result', {}).get('tools', [])
            print(f'{name}: OK ({len(tools)} tools)')
    except Exception as e:
        print(f'{name}: FAIL ({type(e).__name__}: {e}')
"
```

### Step 2 — Inspect container entrypoint (NOT fastmcp.json)

```bash
# WEALTH
docker exec wealth-organ cat /app/entrypoint.sh

# GEOX
docker exec geox_eic grep -n 'transport=' /app/server.py

# WELL
docker exec well cat /app/server.py | grep -A5 'http_app\|streamable'

# arifOS
docker exec arifosmcp cat /app/server.py | grep -A2 'http_app'
```

### Step 3 — Check container logs for 406 source

```bash
docker logs <container_name> --tail 30
```

## The 3 Transport Types in arifOS Federation

| Transport | How to identify | Accept header | Session | MCP spec |
|-----------|----------------|--------------|---------|----------|
| `streamable-http` | `mcp.run(transport="streamable-http")` or `http_app(transport="streamable-http")` | **Required** (`Accept: application/json` or `text/event-stream`) | Yes — `MCP-Session-Id` header | ✅ Standard for remote servers |
| `http` (legacy) | `mcp.run(transport="http")` or `mcp.http_app()` | Not enforced | No | ⚠️ Pre-1.0 FastMCP pattern |
| `sse` | `mcp.run(transport="sse")` | Server pushes events | SSE stream | ⚠️ Legacy, not streamable-http compatible |

## Accept Header Behavior by Transport

```python
# streamable-http — requires Accept header (FastMCP 3.2.4)
# Without Accept → 406 Not Acceptable
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# http_app (legacy arifOS pattern) — behaves OPPOSITE
# Without Accept → 406; WITH Accept → 200
# arifOS uses http_app: works with both with/without Accept

# SSE — needs text/event-stream Accept
headers = {'Content-Type': 'application/json', 'Accept': 'text/event-stream'}
```

## Common Failure Patterns

### 1. WEALTH: entrypoint.sh hardcodes SSE
```
# Wrong (SSE — not streamable-http):
exec python -c "from internal.monolith import mcp; mcp.run(transport='sse', ...)"

# Correct (streamable-http):
exec python -c "from internal.monolith import mcp; mcp.run(transport='streamable-http', ...)"
```

Fix:
```bash
docker exec wealth-organ sed -i "s/transport='sse'/transport='streamable-http'/g" /app/entrypoint.sh
docker restart wealth-organ
```

### 2. GEOX: still on legacy HTTP transport
```
# Wrong:
mcp.run(transport="http")

# Correct:
mcp.run(transport="streamable-http")
```

### 3. WELL: streamable-http but OpenClaw bundle sends wrong Accept
OpenClaw bundle layer must send:
```
Accept: application/json, text/event-stream
Content-Type: application/json
```
And handle `MCP-Session-Id` response header for subsequent requests.

### 4. WEALTH: legacy_mcp_handler blocks `initialize` handshake

**Symptom:** OpenClaw bundle reports `Method not found` for WEALTH, then drops it from bundle. `curl http://127.0.0.1:8082/mcp` with `{"method":"initialize"}` → `{"error":{"code":-32601,"message":"Method not found"}}`. But `{"method":"tools/list"}` works fine.

**Root cause:** WEALTH's `internal/monolith.py` defines a `legacy_mcp_handler` at `Route("/mcp", legacy_mcp_handler)` that intercepts ALL requests to `/mcp` before FastMCP's native handler. The `legacy_mcp_handler` only implements `tools/list` and `tools/call` — it returns `"Method not found"` for `initialize`.

OpenClaw's bundle-mcp subsystem requires the standard MCP `initialize` handshake before it can list or call tools on a server. Without it, the bundle marks the server as failed and removes it.

**Discovery:**
```bash
curl -s -X POST http://127.0.0.1:8082/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":0}'
# → {"jsonrpc":"2.0","id":0,"error":{"code":-32601,"message":"Method not found"}} ❌

curl -s -X POST http://127.0.0.1:8082/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}'
# → OK (50 tools) ✅ — tools/list works because legacy_mcp_handler handles it
```

**Fix:** Add `initialize` handling to `legacy_mcp_handler`. In `internal/monolith.py`, find the `legacy_mcp_handler` function and add before the final `return _JR({"error": ...})`:

```python
if method == "initialize":
    return _JR({
        "jsonrpc": "2.0",
        "id": response_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {"listChanged": True}},
            "serverInfo": {"name": "WEALTH", "version": __version__},
        }
    })
```

Then copy to container and restart:
```bash
docker cp /root/WEALTH/internal/monolith.py wealth-organ:/app/internal/monolith.py
docker restart wealth-organ && sleep 8
# Verify:
curl -s -X POST http://127.0.0.1:8082/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":0}'
# Should return protocolVersion + capabilities ✅
```

**Key diagnostic rule:** If `tools/list` works but OpenClaw bundle can't use the server, check if `initialize` is missing. OpenClaw bundle needs `initialize` before `tools/list`.

## HTTP Status Code Meanings

| Code | Meaning |
|------|---------|
| 200 | Transport works, tools accessible |
| 400 | Request malformed or missing session ID |
| 406 | Accept header missing/wrong (streamable-http) OR wrong transport |
| 404 | Wrong path — endpoint doesn't exist |
| 500 | Server error in MCP handler |

## Verified Working Configs (2026-05-05)

| Node | Transport in container | fastmcp.json | Status |
|------|----------------------|--------------|--------|
| arifOS | `http_app(stateless_http=True)` | N/A | ✅ Works |
| WEALTH | `transport='streamable-http'` (fixed) | `"streamable-http"` | ✅ 50 tools |
| GEOX | `transport="streamable-http"` (line 687) | `"streamable-http"` | ✅ 15 tools |
| WELL | `transport="streamable-http"` | `"streamable-http"` | ❌ 406 — bundle layer issue |

## Verification After Fix

```bash
# Check bundle init in OpenClaw logs
openclaw logs 2>&1 | grep -E 'wealth|well|bundle' | tail -10

# Direct probe
curl -s -X POST http://127.0.0.1:8082/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  | python3 -c "import json,sys; r=json.load(sys.stdin); print(len(r.get('result',{}).get('tools',[])),'tools')"
```
