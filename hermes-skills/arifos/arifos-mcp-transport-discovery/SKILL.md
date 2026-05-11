---
name: arifos-mcp-transport-discovery
description: Diagnose and wire MCP servers on arifOS VPS — identifying transport type (streamable-http/SSE/stdio), session requirements, and correct Hermes config entries. Active 2026-05-05.
triggers:
  - MCP server not connecting to Hermes
  - 405 Method Not Allowed on /mcp
  - 400 Missing session ID on MCP endpoint
  - 406 Not Acceptable on MCP endpoint
  - arifOS MCP server wiring
  - WEALTH WELL MCP discovery
---

# arifos-mcp-transport-discovery

## Live MCP Servers on VPS (af-forge / arifOS Federation)

| Service | Port | Transport | Tools | MCP Endpoint | Auth |
|---------|------|-----------|-------|--------------|------|
| **arifOS** | 8080 | streamable-http | 13 | GET `/mcp` → metadata, POST `/mcp` → 406 without Accept | Bearer (ARIFOS_API_KEY) |
| **GEOX** | 8081 | streamable-http | 118 | POST `/mcp` | Bearer |
| **WEALTH** | 8082 | streamable-http | 50 | POST `/mcp` — works without Accept header | None |
| **WELL** | 8083 | streamable-http | 45 | POST `/mcp` — works without Accept header | None |
| **VAULT999** | 8100 | REST | — | NOT MCP — direct REST | None |
| **A-FORGE** | 7071 | streamable-http | — | GET `/health`, POST `/mcp` | None |

## Critical: arifOS 406 Without Accept Header

arifOS FastMCP returns HTTP 406 when client sends `Accept: */*` or no Accept header. GEOX, WEALTH, and WELL do NOT have this issue — they work without any Accept header.

**Root cause:** GEOX and WELL both have a monkey-patch in server.py that overrides `StreamableHTTPServerTransport._check_accept_headers` to return `(True, True)` when `json_response=True`. arifOS is missing this patch.

**Diagnosis:**
```bash
# arifOS fails without Accept
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/mcp \
  -X POST -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{}}'
# → 406

# WEALTH/GEOX/WELL work without Accept
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8082/mcp \
  -X POST -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{}}'
# → 200
```

**Two fixes (apply both):**

### Fix 1: OpenClaw transport header (immediate — already applied)
Add to `~/.openclaw/openclaw.json` for the arifOS entry:
```json
{
  "url": "http://127.0.0.1:8080/mcp",
  "transport": "streamable-http",
  "headers": {"Accept": "application/json"}
}
```

### Fix 2: Monkey-patch arifOS server.py (defense-in-depth)
Insert before `if __name__ == "__main__":` in `/root/arifOS/arifosmcp/server.py`:
```python
# --- Monkey-patch: Fix 406 from Accept header ---
from mcp.server.streamable_http import StreamableHTTPServerTransport
_orig_check = StreamableHTTPServerTransport._check_accept_headers
def _patched_check(self, request):
    if getattr(self, 'is_json_response_enabled', False): return True, True
    return _orig_check(self, request)
StreamableHTTPServerTransport._check_accept_headers = _patched_check
```

Apply via SSH (idempotent — safe to re-run):
```bash
ssh root@af-forge "python3 -c \"
path = '/root/arifOS/arifosmcp/server.py'
with open(path) as f: c = f.read()
patch = '''# --- Monkey-patch: Fix 406 from Accept header ---
from mcp.server.streamable_http import StreamableHTTPServerTransport
_orig_check = StreamableHTTPServerTransport._check_accept_headers
def _patched_check(self, request):
    if getattr(self, 'is_json_response_enabled', False): return True, True
    return _orig_check(self, request)
StreamableHTTPServerTransport._check_accept_headers = _patched_check
'''
if 'Monkey-patch: Fix 406' not in c:
    c = c.replace('if __name__ == \\\"__main__\\\":', patch + '\nif __name__ == \\\"__main__\\\":')
    open(path,'w').write(c)
    print('PATCHED')
else:
    print('Already patched')
\""
ssh root@af-forge "docker restart arifosmcp"
```

### Why both fixes?
- **openclaw.json header**: fixes OpenClaw bundle transport only
- **monkey-patch**: fixes ALL direct callers (curl, Postman, other agents) — defense-in-depth

## Transport Discovery Protocol

### Step 1: Check container health
```bash
curl -s http://127.0.0.1:PORT/health
```

### Step 2: Probe /mcp with GET (arifOS only returns metadata here)
```bash
# arifOS: returns server metadata
curl -s http://127.0.0.1:8080/mcp

# WEALTH: returns 405 Method Not Allowed
# GEOX:   returns 405 Method Not Allowed  
# WELL:   returns 405 Method Not Allowed
```

### Step 3: Probe POST with plain application/json
```bash
curl -s -X POST http://127.0.0.1:PORT/mcp \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

**Expected responses by transport type:**
| Transport | Success Response | Error Response |
|----------|----------------|----------------|
| streamable-http | `{"jsonrpc":"2.0","id":1,"result":{"tools":[...]}}` | various |
| SSE (session-based) | `{"jsonrpc":"2.0","id":"server-error","error":{"code":-32600,"message":"Not Acceptable: Client must accept text/event-stream"}}` | needs SSE Accept header |
| Requires session | `{"jsonrpc":"2.0","id":"server-error","error":{"code":-32600,"message":"Bad Request: Missing session ID"}}` | needs session init |

### Step 4: For SSE servers — probe with SSE Accept header
```bash
curl -s -X POST http://127.0.0.1:PORT/mcp \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

If still `Missing session ID` → server requires explicit session initialization handshake before tools/list.

## Hermes MCP Config Entry Patterns

### arifOS (streamable-http) — CRITICAL: requires Accept header
```yaml
arifosmcp:
  name: arifosmcp
  url: http://127.0.0.1:8080/mcp
  transport: streamable-http
  timeout: 30
  headers:
    Accept: application/json
```

### GEOX (streamable-http) — no extra headers needed
```yaml
geox:
  name: geox
  url: http://127.0.0.1:8081/mcp
  transport: streamable-http
  timeout: 30
```

### WEALTH (streamable-http) — no extra headers needed (has monkey-patch)
```yaml
wealth:
  name: wealth
  url: http://127.0.0.1:8082/mcp
  transport: streamable-http
  timeout: 30
```

### WELL (streamable-http) — no extra headers needed (has monkey-patch)
```yaml
well:
  name: well
  url: http://127.0.0.1:8083/mcp
  transport: streamable-http
  timeout: 30
```

## Tool Discovery — List All Tools
```bash
# For streamable-http servers
curl -s -X POST http://127.0.0.1:PORT/mcp \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); [print(t['name']) for t in d.get('result',{}).get('tools',[])]"

# For SSE servers (may need session first)
curl -s -X POST http://127.0.0.1:PORT/mcp \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

## Key Findings (2026-05-05)

1. **arifOS (port 8080):** streamable-http, 13 tools, **requires `Accept: application/json`** header — 406 without it. Fix: openclaw.json header + monkey-patch in server.py
2. **WEALTH (port 8082):** streamable-http (NOT SSE), 50 tools, works without Accept header because of monkey-patch
3. **GEOX (port 8081):** streamable-http, 118 tools, works without Accept header because of monkey-patch
4. **WELL (port 8083):** streamable-http (NOT SSE), 45 tools, works without Accept header because of monkey-patch
5. **All four servers:** healthy, all respond to POST /mcp with correct JSON-RPC
6. **GEOX/WELL monkey-patch location:** immediately before `if __name__ == "__main__":` in server.py — `StreamableHTTPServerTransport._check_accept_headers` override
7. **A-FORGE (port 7071):** TypeScript/Node.js runtime — NOT Python. All TS issues defer to Claude Code

## arifOS Tool Call Conventions — TWO PATHS (Critical Discovery 2026-05-11)

arifOS exposes tools via TWO distinct HTTP interfaces with DIFFERENT calling conventions:

### Path A: REST-style `/tools/TOOL_NAME` (HTTP GET/POST, query params)
- **Endpoint:** `POST http://127.0.0.1:8080/tools/arif_sense_observe`
- **Body:** JSON as request body (NOT JSON-RPC)
- **Auth:** Requires `Accept: application/json` header — 406 without it
- **Session binding:** Pass `session_id` in body
- **Behavior with bad mode:** Returns HTTP 200 with nine_signal `RETAK` + `"Unknown mode: X"` in reasons[]
- **Schema differences from docs:** Parameter names may differ (e.g., tool may expect `surface` not `query`)

### Path B: JSON-RPC `/mcp` with `tools/call` method (Preferred)
- **Endpoint:** `POST http://127.0.0.1:8080/mcp`
- **Body:** `{"jsonrpc":"2.0","method":"tools/call","id":N,"params":{"name":"TOOL_NAME","arguments":{...}}}`
- **Auth:** Requires `Accept: application/json` header
- **Behavior with bad args:** Returns `{"isError":true,"content":[{"type":"text","text":"2 validation errors..."}]}` inside result
- **Response wrapped in:** `{"jsonrpc":"2.0","id":N,"result":{"content":[{"type":"text","text":"..."}]}}` where text is a JSON string
- **Tool execution result:** Parse `result.content[0].text` as JSON to get the actual tool response with nine_signal envelope

### Correct JSON-RPC call structure (all arifOS tools)
```bash
curl -s -X POST http://127.0.0.1:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":1,"params":{"name":"arif_sense_observe","arguments":{}}}' \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
text=d['result']['content'][0]['text']
content=json.loads(text)
print('Status:', content.get('status'))
print('Nine signal:', content.get('nine_signal',{}).get('overall'))
print('Output policy:', content.get('output_policy'))
"
```

### Session init required before authenticated tools
```bash
# Step 1: init session
SESSION=$(curl -s -X POST http://127.0.0.1:8080/tools/arif_session_init \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"mode":"init","actor_id":"test-agent","ack_irreversible":false}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['result']['result']['session']['session_id'])")

# Step 2: use session_id in subsequent calls
curl -s -X POST http://127.0.0.1:8080/mcp \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"id\":2,\"params\":{\"name\":\"arif_sense_observe\",\"arguments\":{\"session_id\":\"\$SESSION\"}}}"
```

### Auth-gated tools (888/999) behavior when called without auth
- `arif_judge_deliberate` (888): Returns empty HTTP body — silent, no error
- `arif_vault_seal` (999): Returns empty HTTP body — silent, no error
- `arif_heart_critique` (666): Returns VOID with nine_signal=null when args missing
- These tools require proper session-bound actor identity — calling without auth produces empty response, not an error

### arifOS tool schemas differ from docs (verified working parameters)
| Tool | Working arguments |
|------|------------------|
| `arif_sense_observe` | `{}` (no args = search mode) |
| `arif_mind_reason` | `{"query": "..."}` |
| `arif_kernel_route` | `{}` (no args) |
| `arif_memory_recall` | `{"query": "...", "session_id": "SEAL-..."}` |
| `arif_ops_measure` | `{}` (no args) |
| `arif_heart_critique` | `{}` → returns VOID (auth gate, not error) |

## Verification After Config Change
```bash
# Restart Hermes gateway
hermes gateway restart

# Check gateway state
curl http://127.0.0.1:18000/health 2>/dev/null || \
cat /root/.hermes/gateway_state.json

# List connected tools
hermes tools list 2>/dev/null || \
curl -s http://127.0.0.1:8080/.well-known/mcp/server.json | python3 -m json.tool | grep name
```
