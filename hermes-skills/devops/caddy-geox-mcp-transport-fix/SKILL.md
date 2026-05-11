---
name: caddy-geox-mcp-transport-fix
description: Fix Caddy proxy for FastMCP streamable-http transport — POST returns 405 due to shorthand reverse_proxy directive
triggers:
  - "Caddy reverse_proxy only GET working POST 405"
  - "FastMCP MCP client returns 406 Not Acceptable or 405 Method Not Allowed"
  - "geox.arif-fazil.com MCP endpoint 405 but health works"
  - "MCP SSE transport working but POST tool calls fail"
---

# Caddy + FastMCP Streamable-HTTP Proxy Fix

## The Problem
MCP client probe to `https://geox.arif-fazil.com/mcp`:
- `GET /mcp` → 200 (but FastMCP returns `400 Missing session ID` because no session established)
- `POST /mcp` → **405 Method Not Allowed**

Root cause: Caddy's shorthand `reverse_proxy /path host:port` only matches GET by default.

## The Fix

```caddy
# WRONG — only GET works
reverse_proxy /mcp* geox_eic:8081 {
    header_up Host {host}
}

# CORRECT — GET and POST both work
handle /mcp* {
    reverse_proxy geox_eic:8081 {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
        flush_interval 100ms
    }
}
```

Reload: `docker exec caddy caddy reload --config /etc/caddy/Caddyfile`

## Why This Matters for FastMCP
FastMCP streamable-http transport:
1. **POST** → sends JSON-RPC, returns SSE session stream with `mcp-session-id` cookie
2. **GET** → polls SSE stream using session ID from cookie
3. `mcp-session-id` comes as a **cookie** in POST response headers

Without POST support, MCP clients can't initialize sessions or call tools.

## Additional Caddy Gotchas
- `flush_interval 100ms` — helps SSE streaming responsiveness
- `handle_path` is NOT a path rewrite — it strips the prefix. Never use `handle_path /mcp* { reverse_proxy geox_eic:8081/mcp/stream }` unless FastMCP is mounted at `/mcp/stream` on the backend
- Verify with `docker exec caddy grep -n "handle /mcp\|reverse_proxy /mcp" /etc/caddy/Caddyfile`
- Compare hash: `md5sum /root/arifOS/Caddyfile` vs `docker exec caddy md5sum /etc/caddy/Caddyfile`

## FastMCP Architecture: Two Patterns

**Pattern A — Broken (GEOX before fix):** Two separate apps
```python
mcp_app = mcp.http_app(path="/mcp/stream", transport="streamable-http")
app = Starlette(routes=[
    Route("/health", health_handler),
    Route("/mcp", legacy_json_handler),  # different app!
])
```

**Pattern B — Working (arifOS):** Single app, FastMCP at root
```python
mcp_app = mcp.http_app()  # FastMCP mounted at /
app = mcp_app  # custom routes added to mcp_app.routes
```

When fixing GEOX, restructured from Pattern A to Pattern B.

## Cloudflare 403 When Testing from CLI
Cloudflare blocks requests without a browser-like User-Agent. When testing MCP endpoints from CLI (curl/Python), always include:

```
-H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
```

Without this, Cloudflare returns `403 Forbidden` even though the endpoint is healthy.

## Test Commands
```bash
# Test POST from inside Caddy network
docker exec caddy curl -s --max-time 10 -i \
  "http://geox_eic:8081/mcp" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}'

# Expected: HTTP 200, content-type: text/event-stream, mcp-session-id in headers

# Test public endpoint (Cloudflare needs browser-like UA)
curl -s --max-time 15 \
  "https://geox.arif-fazil.com/mcp" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}'
```

## Files Modified
- `/root/arifOS/Caddyfile` — line ~218: added `handle /mcp*` block for GEOX
- `/root/geox/contracts/tools/unified_13.py` — added geox_well_correlation_panel tool + fixed hashlib import
- `/root/geox/geox/engines/correlation_panel.py` — new file (correlation panel renderer engine)
