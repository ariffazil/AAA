---
name: fastmcp-container-restart-debug
description: Debug and fix FastMCP container restart loops in Docker Compose — stdio vs SSE transport, healthcheck pitfalls
tags: [docker, fastmcp, debugging, container]
---

# FastMCP Container Restart Loop Debug

## Problem
WEALTH MCP container enters restart loop in Docker Compose. App crashes within seconds of start.

## Root Cause
FastMCP's `mcp.run()` defaults to **stdio transport** — it reads from stdin. When Docker starts the container without a TTY, stdin immediately receives EOF and the process exits cleanly. Docker interprets this as a crash and restarts the container. Loop.

Secondary issue: Compose healthcheck using `pg_isready` or `ss` commands that don't exist inside the WEALTH image.

## Diagnostic Steps

1. **Check if container is restarting**
```bash
docker ps --filter name=<container> --format '{{.Names}} {{.Status}}'
# Look for: "Restarting (N) X seconds ago"
```

2. **Check exit reason**
```bash
docker logs <container> --tail 50
# stdio loop: no output or "INFO: Application startup complete" then silent exit
```

3. **Verify app is running at all**
```bash
docker exec <container> sh -c "cat /proc/1/cmdline" | tr '\0' ' '
docker exec <container> sh -c "which ss 2>/dev/null || which netstat 2>/dev/null"
```

4. **Test transport in isolation**
```bash
docker run --rm --network=host <image> python -c "from internal.monolith import mcp; mcp.run(transport='sse', show_banner=False)" &
sleep 3
curl http://localhost:8000/sse  # should return something (SSE stream or 405)
kill %1 2>/dev/null
```

## The Fix

**Patching `if __name__ == "__main__"` in the monolith/server entrypoint:**

```python
if __name__ == "__main__":
    import os
    if os.isatty(0):
        mcp.run()  # stdio for local dev
    else:
        mcp.run(transport="sse", show_banner=False)  # SSE for container
```

This replaces the original `mcp.run()` call. FastMCP's `transport="sse"` makes it bind to HTTP instead of stdio — critical for containers.

## Docker Compose Healthcheck (correct pattern)

After fixing the transport, the healthcheck should test an actual HTTP endpoint:

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -sf http://localhost:8000/sse -o /dev/null || exit 1"]
  interval: 10s
  timeout: 5s
  retries: 5
```

Note: `curl` must be available in the container. If not, remove healthcheck entirely and rely on `restart: unless-stopped` — the process staying alive is sufficient evidence of health.

## Anti-patterns to Avoid

- **healthcheck: `pg_isready`** — not in the app container
- **healthcheck: `ss -ltn | grep`** — `ss`/`netstat` often not installed in slim images
- **compose `command:` override for transport** — escaping `import` statements in YAML is fragile
- **`network_mode: service:X`** — too blunt, breaks container networking

## Key Insight

FastMCP defaults to stdio. Container environments have no TTY → stdin closes → process exits → restart loop. Always explicitly set `transport="sse"` when deploying FastMCP containers.
