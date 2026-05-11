---
name: arifos-mcp-sse-debug
description: Diagnose arifOS MCP SSE 404 errors — from transport mismatch to import failure root causes
tags: [arifOS, MCP, debug, docker, openclaw]
created: 2026-04-25
---

# arifOS MCP Debug: SSE 404 → Import Failure Diagnosis

## Trigger Conditions

- `docker logs arifosmcp` shows `GET /sse HTTP/1.1 404`
- `/health` returns degraded or unhealthy
- OpenClaw `bundle-mcp` reports `failed to start server "arifos"` with SSE 404

## Primary Root Cause: Import Failure Cascade

The SSE 404 is a **symptom**, not the cause. The real failure chain:

```
arifosmcp/runtime/prompts.py → V2_PROMPT_SPECS import fails →
  → FastAPI starts (health endpoint works) →
  → MCP component fails to initialize →
  → /sse route never registered →
  → OpenClaw bundle-mcp gets 404
```

**Exact error signal:**
```
{"status":"degraded","error":"Import failed: cannot import name 'V2_PROMPT_SPECS' 
from 'arifosmcp.runtime/prompts.py' (/usr/src/app/arifosmcp/runtime/prompts.py)"}
```

When you see this — the MCP routes are NOT registered. Fix the import, rebuild the container.

## Diagnostic Sequence (in order)

### 1. Health check — determines if server is up at all
```bash
curl -s http://localhost:8080/health
```
Expected: `200 OK` with full JSON status
Degraded signal: `{"status":"degraded","error":"Import failed..."}`

### 2. SSE route test — confirms MCP initialization
```bash
curl -s -H "Accept: text/event-stream" http://localhost:8080/sse
```
Expected: SSE stream or redirect
Actual (broken): `{"detail":"Not Found"}`

### 3. MCP POST test — checks HTTP transport negotiation
```bash
curl -s -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```
If returns `406 Not Acceptable` with message about Accept header requiring both `application/json` AND `text/event-stream` — the MCP is running but correctly configured. If 404 → MCP routes not registered.

### 4. Container logs — find the actual startup error
```bash
docker logs arifosmcp --tail 50 2>&1
```
Look for: `Import failed`, `ModuleNotFoundError`, `AttributeError`, `Application shutdown complete`

### 5. Environment inspection — check transport mode
```bash
docker exec arifosmcp env | grep -E "ARIFOS|MCP|TRANSPORT|PORT"
```
Key: `AAA_MCP_TRANSPORT=http` means streamable-http (not SSE as a separate server)

### Key Diagnostic Signal: Transport vs Initialization
- `AAA_MCP_TRANSPORT=http` + `GET /sse 404` + `POST /mcp 406` → MCP component failed to initialize (import error), NOT a transport mismatch
- `AAA_MCP_TRANSPORT=http` + `POST /mcp works` + `SSE 200` → MCP healthy, SSE works via upgrade
- `AAA_MCP_TRANSPORT=sse` + SSE not working → transport misconfiguration, different fix path

### 6. POST /mcp with correct headers — the definitive health test
```bash
curl -s -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```
| Response | Meaning |
|----------|---------|
| `{"jsonrpc":"2.0","id":"server-error","error":{"code":-32600,"message":"Not Acceptable..."}}` | MCP running but client Accept header incomplete |
| `406 Not Acceptable` (raw) | MCP working, need both `application/json` AND `text/event-stream` in Accept |
| `404 Not Found` | MCP routes not registered — MCP component failed to initialize |
| `Missing Content-Type header` | Client sending wrong Content-Type |
| `"detail":"Method Not Allowed"` on GET /mcp | ✅ **HEALTHY** — POST-only endpoint, MCP routes registered correctly |

**CRITICAL:** Accept header must include **both** MIME types simultaneously. Sending just `application/json` returns `406` even when MCP is healthy.

### 7. Container restart detection — catch crash loops
```
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [1]
```
This sequence → the process exited cleanly but was then restarted by the container orchestrator. The MCP server started, crashed, and was restarted. The import failure causes this cycle.

### 8. POST /mcp with correct headers — the definitive health test
```bash
curl -s -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```
| Response | Meaning |
|----------|---------|
| `{"jsonrpc":"2.0","id":"server-error","error":{"code:-32600,"message":"Not Acceptable..."}}` | MCP running but client Accept header incomplete |
| `406 Not Acceptable` (raw) | MCP working, need both `application/json` AND `text/event-stream` in Accept |
| `404 Not Found` | MCP routes not registered — MCP component failed to initialize |
| `Missing Content-Type header` | Client sending wrong Content-Type |
| `Method Not Allowed` on GET /mcp | Normal — POST-only endpoint when MCP healthy |

### 6. Container restart detection — catch crash loops
```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep arifosmcp
```
If uptime is `1 second` → health check restarted the container after it crashed

## What Breakage Looks Like

| Signal | Meaning |
|--------|---------|
| `GET /sse HTTP/1.1 404` in logs | MCP routes not registered |
| `/health` returns degraded + import error | Code-level init failure — MCP component failed |
| Container restarting repeatedly | Health check triggering restart loop |
| `406 Not Acceptable` on POST /mcp | MCP running but client missing `Accept: text/event-stream` |
| `docker ps` shows uptime `1 second` | Health check triggered a restart after degraded state |
| `Missing Content-Type header` in logs | Client sending wrong Content-Type to POST /mcp |
| `"Method Not Allowed" on GET /mcp` | Normal — POST-only endpoint when MCP is healthy |

## Fix Protocol (APEX AUTHORIZED ONLY)

1. Identify import failure in `arifosmcp/runtime/prompts.py`
2. Fix or remove the broken import reference
3. Rebuild container image
4. Restart container
5. Verify: `curl -s http://localhost:8080/health` returns `healthy`
6. Verify: SSE stream connects

## Cross-Reference

- arifOS transport: `AAA_MCP_TRANSPORT=http` → SSE not a separate server, it's an MCP protocol feature
- OpenClaw bundle-mcp config points to `http://localhost:8080` as the MCP server
- When arifOS MCP is healthy: POST to `/mcp` with correct headers works; SSE upgrade succeeds

## CRITICAL ADDITION: Stateless vs Stateful Mode (2026-05-04)

The running arifOS MCP server uses **`stateless_http=True`** — confirmed live at `https://arifos.arif-fazil.com/mcp`.

### What stateless mode means:

| Feature | Stateful mode | Stateless mode (CURRENT) |
|---------|--------------|------------------------|
| `MCP-Session-Id` header | Server assigns on init, client echoes, server confirms | **No session headers at all** |
| Session continuity | Multiple requests share state | One-shot request-response only |
| `/sse` route | Available (server-push lane) | **HTTP 404 — not registered** |
| VAULT999 session binding | Binds to session | Stateless — no session to bind |
| Initialize response | `200 OK` + `MCP-Session-Id` header | `200 OK` + **no session header** |

### Diagnostic: Testing for session headers

```bash
# Full initialize with headers inspection
curl -s -X POST https://arifos.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' \
  -D - 2>/dev/null | grep -i "mcp-session-id\|set-cookie"
# Returns: (empty) → stateless mode confirmed
```

If you see `MCP-Session-Id` in response headers → stateful mode is active.

### Common confusion: "SSE" is not a streaming channel in stateless mode

The MCP spec uses two different streaming mechanisms:
- **SSE (Server-Sent Events):** One-directional server→client push. Used in stateful sessions for notifications.
- **Chunked Transfer Encoding (`Transfer-Encoding: chunked`):** How FastMCP streams JSON-RPC response fragments in **both** stateless and stateful modes. Each JSON-RPC message becomes an HTTP chunk.

**In stateless mode:** No SSE endpoint exists (`/sse → 404`). Streaming works via chunked encoding on the POST response. This is the correct behavior.

### `sovereign_sse` route does not exist on live server

The `server.py` line 490 reference to `sovereign_sse` is either:
- A route defined but not deployed, OR
- Removed from the current build

`GET /sse → HTTP 404` on the live endpoint. Do not reference it in documentation or client configs.

### Entry point discrepancy (harmless but confusing)

`transports.py` line 598 maps both `http` AND `streamable-http` env vars to `transport="http"` — but the running container uses `server.py` line 252 which passes `transport="streamable-http"` directly to `mcp.http_app()`. These are two different entry points. The discrepancy is **moot for production** since the container uses `server.py`, but it would matter if anyone restarts via the CLI wrapper.

### Key signals from today's verification (2026-05-04):

```
stateless_http=True       → confirmed from server.py line 252
AAA_MCP_TRANSPORT=streamable-http  → confirmed from container env
GET /sse                  → HTTP 404
POST /mcp (stateless)     → 200 OK, no session headers
```

## Pitfalls

- Don't test SSE with `curl` without `-H "Accept: text/event-stream"` — you'll get a 406 even when MCP is healthy
- Claims about `MCP-Session-Id` bidirectional lifecycle only apply to **stateful** mode — the live server is **stateless**
- The `sovereign_sse` endpoint referenced in some documentation does not exist on the live server (`/sse → 404`)
- In stateless mode, streaming works via chunked transfer encoding, NOT via SSE — SSE is not available
- Don't assume container being "up" means MCP is initialized — the Python process may start while FastAPI routes fail to register
- Health endpoint can return 200 while the MCP component is partially broken — check for `"status":"degraded"` not just HTTP status
- The SSE route in arifOS MCP is registered by the MCP component, not a separate FastAPI route — if import fails, `/sse` returns 404 even though the HTTP server is running
- Container restart with uptime `1 second` means health check caught a degraded/crashed state — always check logs for the `Shutting down` signal
- `POST /mcp` with only `application/json` Accept header returns 406 even when healthy — must include `text/event-stream`

## CRITICAL PATTERN: FastMCP Dual-Endpoint (GEOX / Well / Similar)

**Symptom:** OpenClaw reports `404 from domain.com — method not found` for a FastMCP server, but `/health` returns 200 and the container is healthy.

**Root cause:** The container exposes TWO different HTTP servers on the same port:

| Route | Handler | Methods supported |
|-------|---------|-----------------|
| `/mcp` | Legacy JSON-RPC bridge | `tools/list`, `tools/call` only |
| `/mcp/stream` | FastMCP streamable-http | Full MCP protocol (initialize, tools/list, tools/call, etc.) |
| `/health` | Health check | GET only |

OpenClaw sends `initialize` (SSE handshake) to `/mcp` → legacy handler returns `404 Method not found`.

**Discovery chain:**
```bash
# 1. Test /health — is the container alive?
curl -s https://geox.arif-fazil.com/health
# → {"status":"healthy"} ✅ container alive

# 2. Test /mcp with initialize — this is what fails
curl -s -X POST https://geox.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{...},"id":0}'
# → {"error":{"code":-32600,"message":"Method not found"}} ❌

# 3. Test /mcp/stream with initialize — this is what works
curl -s -X POST https://geox.arif-fazil.com/mcp/stream \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{...},"id":0}'
# → {"jsonrpc":"2.0","id":0,"result":{"protocolVersion":"2024-11-05",...}} ✅
```

**Fix — update OpenClaw config to use `/mcp/stream`:**

1. `/root/.openclaw/openclaw.json` — add server entry:
```json
"geox": {
  "url": "https://geox.arif-fazil.com/mcp/stream",
  "transport": "streamable-http",
  "description": "GEOX Earth coprocessor MCP"
}
```

2. `/root/.hermes/workspace/openclaw/agents/maxhermes/workspace.yaml` — fix existing entry:
```yaml
- id: geox-mcp
  url: https://geox.arif-fazil.com/mcp/stream
  enabled: true
```

3. Restart:
```bash
systemctl restart openclaw-gateway && sleep 4
openclaw mcp list  # → geox should now appear
```

**Known servers with this dual-endpoint pattern:**
| Server | `/mcp` | `/mcp/stream` | Caddy route |
|--------|--------|--------------|-------------|
| GEOX | legacy JSON-RPC (404 on initialize) | FastMCP SSE ✅ | `geox_eic:8081` |
| WELL | health/status only | FastMCP SSE | `well.arif-fazil.com` |
| (any FastMCP with legacy bridge) | limited JSON-RPC | full MCP ✅ | — |

**Key diagnostic:** If `/mcp` returns `404 Method not found` on `initialize` but `/mcp/stream` works — you have the dual-endpoint pattern. Fix the URL, not the server.