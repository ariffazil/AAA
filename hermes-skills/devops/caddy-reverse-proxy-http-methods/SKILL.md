---
name: caddy-reverse-proxy-http-methods
description: Caddy reverse_proxy directive defaults to GET-only for path patterns — POST requires handle block wrapper
tags: [caddy, reverse-proxy, http-methods, fastmcp, mcp]
last_updated: 2026-05-01
---

# Caddy `reverse_proxy /path*` Defaults to GET Only

## Symptom
```
HTTP 405 Method Not Allowed
```
When calling `POST /mcp` through Caddy, but `GET /mcp` works fine.

## Root Cause
Caddy's `reverse_proxy /path* destination` shorthand only matches GET by default. POST/PUT/DELETE are rejected with 405.

## The Fix
Wrap in a `handle` block:
```
handle /mcp* {
    reverse_proxy geox_eic:8081 {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
    }
}
```
NOT:
```[truncated]
```

## Where This Hit arifOS
- `geox.arif-fazil.com/mcp` returned 405 on POST
- `arifOS/mcp` also had this pattern — required same fix
- The `handle` block tells Caddy to handle all HTTP methods at that path

## Verification
```bash
# POST should return 200 (or SSE content), not 405
curl -X POST https://geox.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize",...}'
```
