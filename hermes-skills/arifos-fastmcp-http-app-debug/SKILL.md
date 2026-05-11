---
name: arifos-fastmcp-http-app-debug
description: Debug why custom REST routes in rest_routes.py return HTTP 404 despite existing in the file — FastMCP http_app() called before _register(mcp) completes, causing mcp.run() fallback that bypasses Uvicorn
category: devops
tags: [fastmcp, arifOS, rest_routes, http_app, uvicorn, debug]
---

# arifOS FastMCP HTTP App Debug — Why Custom REST Routes Don't Register

## Symptom

New REST endpoints added to `arifOS/arifosmcp/runtime/rest_routes.py` exist in the file (syntax valid), return HTTP 404 from live container, but container logs show no route registration errors.

```
[arif-register] Registered: command_center OK
HTTP app not available — falling back to mcp.run()
```

## Root Cause

`server.py` calls `mcp.http_app()` (line 432) to get a Starlette app, then tries `mcp._mcp_server.app` (line 434) as fallback. Both return `None` because:

1. `mcp.http_app()` is called **before** all tools and apps are fully registered
2. FastMCP's HTTP app is constructed lazily after all `mcp.tool()` / `mcp.prompt()` calls and all `_register(mcp)` calls complete
3. When both return `None`, the server falls back to `mcp.run()` — FastMCP's native stdio/streamable transport starts instead of Uvicorn
4. Custom REST routes registered via `app.add_api_route()` in `rest_routes.py` are never in the request path

## Diagnostic Steps

```bash
# 1. Check what the container actually started
docker logs arifosmcp 2>&1 | grep -E "HTTP app not|mcp.run|registered"

# 2. Verify endpoints exist in the container image
docker exec arifosmcp grep -c "tools.json\|mcp/status" /app/arifosmcp/runtime/rest_routes.py

# 3. Test if the endpoint is reachable
curl -sv https://arifos.arif-fazil.com/mcp/status 2>&1 | grep "HTTP/"

# 4. If HTTP 404 but grep finds the code → route registration was bypassed
```

## The Fix

In `server.py`, move `app = mcp.http_app(...)` to **after** all `_register(mcp)` calls complete. Sequence:

```python
# 1. All tool registrations
for tool_fn in _CANONICAL_TOOL_FNS:
    mcp.tool(...)(tool_fn)

# 2. All app registrations
_safe_register(mcp, "arifosmcp.apps.command_center.app", "command_center")

# 3. NOW get the HTTP app — after all registrations complete
app = mcp.http_app(stateless_http=True)
if app is None:
    app = mcp._mcp_server.app  # FastMCP v3 internal

# 4. Register custom REST routes on the resolved app
register_rest_routes(app, mcp)

# 5. Run with Uvicorn
```

## Key Insight

FastMCP's `http_app()` is a **post-registration call**, not a setup call. Must be called after all `mcp.tool()`, `mcp.prompt()`, and `_register()` calls complete. The arifOS server structure currently calls it too early.

## Prevention

When adding new REST routes to `rest_routes.py`, always verify:
1. Called inside `register_rest_routes(app, mcp)`
2. `app` is the Uvicorn-served Starlette app (not `None`)
3. Container logs show `HTTP app not available` — if they do, routes won't register

Guard pattern for new endpoints:
```python
if app is None:
    return JSONResponse({"error": "REST routes unavailable — HTTP app not initialized"}, status_code=503)
```
