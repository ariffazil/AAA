---
name: openclaw-geox-mcp-debug
description: Diagnose and fix OpenClaw gateway slow replies caused by GEOX MCP bundling failures (404 on /mcp/stream route)
tags: [openclaw, gateway, mcp, geox, debugging, telegram]
---

# OpenClaw Gateway + GEOX MCP Bundle Debug

## Trigger
Telegram bot slow or not responding. `@AGI_ASI_bot` OpenClaw reply lag.

## Diagnosis Steps

### 1. Check Gateway Health
```bash
curl -s http://localhost:18789/health
openclaw status 2>&1 | grep -E "Gateway|Sessions|Health"
```

### 2. Check GEOX MCP Endpoint
```bash
# Local container
curl -s -o /dev/null -w "HTTP %{http_code}" http://localhost:8081/mcp/stream

# Public endpoint (simulates OpenClaw bundler)
curl -s -o /dev/null -w "HTTP %{http_code}" https://geox.arif-fazil.com/mcp/stream
```

### 3. Read Gateway Logs — Most Important
```bash
# Real-time log path
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# Key pattern: bundle-mcp failures
grep "bundle-mcp" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | tail -20

# Key pattern: geox MCP 404 errors
grep "geox.*mcp/stream\|Not Found" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | tail -10
```

### 4. Check GEOX Container
```bash
# Verify kernel/ is in running container
docker exec geox_eic ls /app/contracts/tools/canonical/kernel/

# Verify _helpers.py is thin shim
docker exec geox_eic wc -l /app/contracts/tools/canonical/_helpers.py
```

## Root Causes Found (from 2026-05-04 incident)

**Root Cause 1: MCP Route Mismatch**
- OpenClaw bundle-mcp calls `https://geox.arif-fazil.com/mcp/stream`
- GEOX FastMCP server only had `/mcp` route — no `/mcp/stream`
- Result: 404 on every bundling attempt → event loop blocked by retry backoff

**Fix:** Add route in `server.py`:
```python
Route("/mcp", legacy_mcp_handler, methods=["GET", "POST"]),
Route("/mcp/stream", legacy_mcp_handler, methods=["GET", "POST"]),  # ADD THIS
Mount("/", mcp_app),
```

**Root Cause 2: Container Using Stale Image**
- `docker compose build geox` rebuilds with new code
- Container `geox_eic` was NOT restarted — still running old image without `kernel/`
- Fix: `docker compose -f /root/compose/docker-compose.yml up -d geox`

**Root Cause 3: Event Loop Choke from Failed MCP Bundles**
- Every ~5min OpenClaw tries to re-bundle MCP tools
- GEOX 404 causes backoff timer + accumulated sessions (40+)
- SIGUSR1 restart just masks it — need container restart to fix at root

**Gateway Restart Command:**
```bash
# Correct way to restart OpenClaw gateway
systemctl --user restart openclaw-gateway.service

# If that fails and you see "already running under systemd":
openclaw gateway start  # Uses systemd, not manual process
```

**NOT this (creates double-process chaos):**
```bash
kill <pid> && nohup /usr/bin/node ... &  # WRONG
```

## Verification Checklist
- [ ] `curl http://localhost:8081/health` → 200
- [ ] `curl http://localhost:8081/mcp/stream` (POST with JSON-RPC) → 200 + tools list
- [ ] `curl https://geox.arif-fazil.com/mcp/stream` → HTTP 200
- [ ] `docker exec geox_eic ls /app/contracts/tools/canonical/kernel/` → 5 files
- [ ] `openclaw status` → Gateway: reachable, Sessions: N (should be < 10 after restart)
- [ ] `grep "bundle-mcp.*geox.*failed" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log` → should be empty (no recent failures)

## Related Files
- GEOX server: `/root/geox/server.py`
- Caddyfile: `/root/compose/Caddyfile`
- OpenClaw config: `/root/.openclaw/openclaw.json`
- Gateway logs: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
