---
name: wealth-sse-transport-fix
description: Fix WEALTH container restart loop caused by FastMCP stdio transport blocking on stdin when Docker starts without TTY
tags: [WEALTH, FastMCP, container-restart, SSE, docker, production]
last_updated: 2026-04-28
---

# WEALTH FastMCP SSE Transport Fix

## Problem

`wealth-organ` container enters a restart loop:
```
Up 1 second
Exited (0) 2 seconds ago
Up 1 second
Exited (0) 2 seconds ago
...
```

## Root Cause

`monolith.py` runs `mcp.run()` which defaults to **stdio transport**.
When Docker starts the container without a TTY, `stdin` closes immediately.
The stdio transport blocks waiting for input → when input never arrives, process exits
→ Docker restarts → loop.

## Fix (one-line code change)

```python
# Before (in monolith.py)
if __name__ == "__main__":
    mcp.run()

# After
if __name__ == "__main__":
    import os
    if os.isatty(0):
        mcp.run()                              # stdio for local dev
    else:
        mcp.run(transport="sse", show_banner=False)  # SSE for container
```

This makes the transport **context-aware**: stdio when run locally with a terminal, SSE when run in Docker.

## Why SSE works in Docker

- SSE binds FastMCP to an HTTP port (default 8000)
- No stdin needed — HTTP server handles connections
- Container stays alive because the HTTP server is a long-running process
- Docker `unless-stopped` restart policy handles actual crashes

## Healthcheck fix

Remove the broken `pg_isready` healthcheck from compose. FastMCP SSE doesn't have a generic `/health` endpoint — the container process itself is the health indicator.

```yaml
# Before (BROKEN — pg_isready not in WEALTH container)
healthcheck:
  test: ["CMD", "pg_isready", "-U", "arifos"]

# After — remove healthcheck entirely (unless-stopped handles crashes)
# healthcheck: (omit entirely)
```

## Deployment

```bash
# 1. Copy patched monolith.py to VPS
scp /local/monolith.py arifos:/root/WEALTH/internal/

# 2. On VPS: commit
cd /root/WEALTH
git add internal/monolith.py
git commit -m "feat(kernel): harden intelligence v2026.04.29 [SSE + SABAR + V2_ALIAS]"
git push origin main

# 3. Rebuild container
cd /root/compose
docker compose up -d wealth-organ

# 4. Verify stable
docker ps  # should show "Up X minutes" not cycling
```

## How to verify the fix worked

```bash
# Check no restart loop
docker ps  # wealth-organ: "Up N minutes"

# Check SSE port is listening inside container
docker exec wealth-organ sh -lc "curl -s --connect-timeout 2 http://localhost:8000/"
# Should return something (FastMCP SSE response or 404), not "connection refused"

# Check from Caddy network
docker exec caddy sh -lc "curl -s --connect-timeout 3 http://wealth-organ:8000/"
```

## Key Files

- `/root/wealth/internal/monolith.py` — source (SSE patch applied here)
- `/root/compose/docker-compose.yml` — WEALTH service definition
- `wealth-organ` — container name
