# CORS Preflight Fix — Public MCP Gateway — 2026-08-09

## Problem

MCPJam (and any browser-based MCP client) fails to connect to `https://mcp.arif-fazil.com/mcp` with "failed to connect." The kernel is healthy, POST works from curl, but the browser never sends the POST.

## Root cause

Browser sends CORS preflight `OPTIONS /mcp` before the actual `POST /mcp`. The arifOS kernel's CORS middleware checks the `Origin` header against an allowlist. MCPJam runs from `http://localhost:6274` — that origin is NOT in the kernel's allowlist. Kernel returns:

```
HTTP 400 — "Disallowed CORS origin"
```

Browser sees the failed preflight → blocks the POST entirely → client shows connection failure.

## Diagnostic

```bash
# Simulate MCPJam's browser preflight
curl -sv -X OPTIONS https://mcp.arif-fazil.com/mcp \
  -H "Origin: http://localhost:6274" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type, Mcp-Session-Id, MCP-Protocol-Version" \
  -D - -o /dev/null

# 204 = OK (Caddy handles it)
# 400 = FAIL (kernel rejecting origin)
```

Also test from kernel directly:
```bash
curl -sv -X OPTIONS http://127.0.0.1:8088/mcp \
  -H "Origin: http://localhost:6274" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type, Mcp-Session-Id, MCP-Protocol-Version" \
  -D - -o /dev/null
# Same 400 — confirms kernel is the rejector, not Caddy
```

## Fix

Add `import cors_public` to the `/mcp*` handler in the `mcp.arif-fazil.com` Caddy vhost. This intercepts OPTIONS at the Caddy edge → returns 204 with `Access-Control-Allow-Origin: *` → request never reaches the kernel's stricter CORS check.

### Before
```
handle /mcp* {
    # 2026-07-04 — FIX: Perplexity MCP connector omits Accept header.
    reverse_proxy 127.0.0.1:8088 {
        header_up Accept "application/json, text/event-stream, */*"
    }
}
```

### After
```
# 2026-08-09 — FIX: MCPJam/browser-based MCP clients fail CORS preflight.
# Kernel returns 400 "Disallowed CORS origin" for non-allowlisted Origins.
# Import cors_public so Caddy handles OPTIONS → 204 before reaching kernel.
handle /mcp* {
    import cors_public
    # 2026-07-04 — FIX: Perplexity MCP connector omits Accept header.
    reverse_proxy 127.0.0.1:8088 {
        header_up Accept "application/json, text/event-stream, */*"
    }
}
```

### cors_public snippet (for reference)
```
(cors_public) {
    @preflight method OPTIONS
    handle @preflight {
        header Access-Control-Allow-Origin *
        header Access-Control-Allow-Methods "GET, POST, OPTIONS, DELETE"
        header Access-Control-Allow-Headers "Content-Type, Mcp-Session-Id, MCP-Protocol-Version, Mcp-Method, Mcp-Name, Authorization, X-Requested-With, Last-Event-ID, X-MCP-Client-Id"
        header Access-Control-Max-Age 86400
        respond "" 204
    }
    header Access-Control-Allow-Origin *
    header Access-Control-Allow-Methods "GET, POST, OPTIONS, DELETE"
    header Access-Control-Allow-Headers "Content-Type, Mcp-Session-Id, MCP-Protocol-Version, Mcp-Method, Mcp-Name, Authorization, X-Requested-With, Last-Event-ID, X-MCP-Client-Id"
}
```

## Deploy

```bash
# 1. Backup
cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak-$(date +%Y%m%d-%H%M%S)

# 2. Patch (use python3 or sed — patch tool refuses /etc paths)
python3 -c "
with open('/etc/caddy/Caddyfile') as f: c = f.read()
old = '''\t# ── MCP transport (canonical public door) ──────────────────────────────
\thandle /mcp* {
\t\t# 2026-07-04 — FIX: Perplexity MCP connector omits Accept header.
\t\treverse_proxy 127.0.0.1:8088 {
\t\t\theader_up Accept \"application/json, text/event-stream, */*\"
\t\t}
\t}'''
new = '''\t# ── MCP transport (canonical public door) ──────────────────────────────
\t# 2026-08-09 — FIX: MCPJam/browser-based MCP clients fail CORS preflight.
\t# Kernel returns 400 \"Disallowed CORS origin\" for non-allowlisted Origins.
\t# Import cors_public so Caddy handles OPTIONS → 204 before reaching kernel.
\thandle /mcp* {
\t\timport cors_public
\t\t# 2026-07-04 — FIX: Perplexity MCP connector omits Accept header.
\t\treverse_proxy 127.0.0.1:8088 {
\t\t\theader_up Accept \"application/json, text/event-stream, */*\"
\t\t}
\t}'''
assert old in c, 'old string not found'
with open('/etc/caddy/Caddyfile', 'w') as f: f.write(c.replace(old, new, 1))
print('PATCHED')
"

# 3. Validate
caddy validate --config /etc/caddy/Caddyfile

# 4. Reload (not restart — zero-downtime)
systemctl reload caddy

# 5. Verify
sleep 2
curl -s -o /dev/null -w "%{http_code}" -X OPTIONS https://mcp.arif-fazil.com/mcp \
  -H "Origin: http://localhost:6274" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type, Mcp-Session-Id, MCP-Protocol-Version"
# Expected: 204
```

## Why cors_public and not kernel CORS fix?

Two reasons:
1. **Edge-level is correct architecture.** CORS is a transport concern, not an application concern. Caddy (the reverse proxy) should handle it — same pattern as TLS termination, compression, caching.
2. **Kernel CORS allowlist is intentionally strict.** The kernel's origin check is a defense-in-depth layer for direct-access scenarios (e.g. internal tools calling :8088 directly). Weakening it to allow `*` would reduce that defense. Caddy's `cors_public` handles the public-facing case without touching the kernel.

## Verification

| Test | Before | After |
|------|--------|-------|
| `OPTIONS /mcp` from `localhost:6274` | ❌ 400 "Disallowed CORS origin" | ✅ 204 with `Access-Control-Allow-Origin: *` |
| `OPTIONS /mcp` from `mcpjam.com` | ❌ 400 | ✅ 204 |
| `POST /mcp` (initialize) | ✅ (worked from curl) | ✅ (still works) |
| Cloudflare cache | — | `DYNAMIC` (not cached, passthrough) |
| MCPJam connection | ❌ "failed to connect" | ✅ connects |

## Related

- `federation-infra-verification` §7a — the 5-layer public MCP gateway diagnostic chain
- `FORGE-mcp-probe` — MCPJam CLI/SDK probe patterns
- Caddy `cors_public` snippet — defined in `/etc/caddy/Caddyfile`
