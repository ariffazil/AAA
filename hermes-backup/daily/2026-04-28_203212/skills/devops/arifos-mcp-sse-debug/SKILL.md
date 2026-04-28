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

## Pitfalls

- Don't test SSE with `curl` without `-H "Accept: text/event-stream"` — you'll get a 406 even when MCP is healthy
- Don't assume container being "up" means MCP is initialized — the Python process may start while FastAPI routes fail to register
- Health endpoint can return 200 while the MCP component is partially broken — check for `"status":"degraded"` not just HTTP status
- The SSE route in arifOS MCP is registered by the MCP component, not a separate FastAPI route — if import fails, `/sse` returns 404 even though the HTTP server is running
- Container restart with uptime `1 second` means health check caught a degraded/crashed state — always check logs for the `Shutting down` signal
- `POST /mcp` with only `application/json` Accept header returns 406 even when healthy — must include `text/event-stream`