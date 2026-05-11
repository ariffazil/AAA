---
name: caddyfile-arifos-debug
description: Debug Caddyfile routing issues on arifOS VPS — network separation, try_files ordering, static file 404s
tags: [caddy, docker, networking, arifOS]
version: 1.0
---

# arifOS Caddyfile Debug — Network & Routing Fixes

## Trigger
Caddy returning 404 on paths that exist on disk, or reverse proxy to arifosmcp timing out from inside Caddy container.

## Common Root Causes

### 1. Container Network Separation
Caddy (`arifos_core_network`) and arifosmcp (`af-forge_arifos-network`) are on **different Docker networks**. `reverse_proxy arifosmcp:8080` from Caddy **silently fails** (connection abort, not refused).
- **Fix**: Use `file_server` with static mount instead of reverse proxy. OR add both containers to the same network.

### 2. SPA try_files Catches .well-known Before Explicit Handler
`handle /.well-known/mcp/*` defined AFTER `handle` blocks with `try_files {path} /index.html` — Caddy's route matching is ordered, so the SPA fallback catches `/.well-known/*` requests first.
- **Fix**: Move `handle /.well-known/mcp/*` block to appear BEFORE the `try_files` directive in the Caddyfile.
- **Verify**: `docker exec caddy caddy adapt --config /etc/caddy/Caddyfile` to inspect compiled route order.

### 2b. Exact Route Must Come Before Wildcard
`handle /.well-known/mcp` (exact) must be defined BEFORE `handle /.well-known/mcp/*` (wildcard). If exact is after wildcard, exact-path requests to `/.well-known/mcp` return 404 because wildcard matches first.
- **Fix**: In Caddyfile, declare exact routes before their wildcard siblings.

### 3. Caddyfile Symlink — /compose/ and /arifOS/ Are the Same File
`/root/compose/Caddyfile` → `/root/arifOS/Caddyfile` (symlink). On VPS, edit `/root/arifOS/Caddyfile` directly.
- **Always**: `cd /root/arifOS && vim/nano Caddyfile`, then `caddy fmt --overwrite Caddyfile`, then `docker exec caddy caddy reload --config /etc/caddy/Caddyfile`
- **Validate**: `cd /root/compose && caddy validate --config Caddyfile` (fails on certs not present on dev machine — ignore TLS cert errors if they say `cert.pem: no such file`)
- **Verify**: `diff /root/arifOS/Caddyfile <(docker exec caddy cat /etc/caddy/Caddyfile)`

### 4. Cache Confusion on /health
Cloudflare may cache a stale error page during container downtime.
- **Fix**: Add `header Cache-Control "no-store"` to `/health` route. Purge Cloudflare cache.

## Debug Commands
```bash
# Format Caddyfile before reloading (prevents silent discard of malformed blocks)
cd /root/compose && caddy fmt --overwrite Caddyfile

# Validate (ignore cert.pem errors on dev machine)
cd /root/compose && caddy validate --config Caddyfile

# Which Caddyfile is active?
diff /root/arifOS/Caddyfile <(docker exec caddy cat /etc/caddy/Caddyfile)

# Inspect compiled route order
docker exec caddy sh -c "cd /etc/caddy && caddy adapt --config Caddyfile 2>/dev/null" | python3 -c "
import sys, json
d = json.loads(sys.stdin.read())
srv = d['apps']['http']['servers']['srv0']
for i, route in enumerate(srv['routes']):
    m = route.get('match',[{}])
    print(f'  [{i}] match={[(k,str(v)[:50]) for mm in m for k,v in mm.items()]}')
"

# Check container networks
docker inspect caddy --format '{{json .NetworkSettings.Networks}}' | python3 -c "import sys,json; nets=json.load(sys.stdin); print(list(nets.keys()))"
docker inspect arifosmcp --format '{{json .NetworkSettings.Networks}}' | python3 -c "import sys,json; nets=json.load(sys.stdin); print(list(nets.keys()))"

# Verify files exist inside Caddy
docker exec caddy sh -c "ls -la /var/www/html/arifos/.well-known/mcp/"

# Reload and test
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
curl -sI "https://arifos.arif-fazil.com/.well-known/mcp/server.json"
```

## Pitfalls
- `try_files {path} /index.html` in a `handle` block with `file_server` acts as SPA fallback — catches ALL unmatched paths including static files
- Edit the **source** Caddyfile, then reload — do not edit the container's in-memory copy
- Cloudflare cache TTL can make "404" persist for minutes after fixing server-side
- Duplicate `handle` blocks with the same path silently override each other — the first one wins in Caddy's route matching. Always `grep -n "handle /" Caddyfile` to find duplicates before they cause silent routing failures
