---
name: arifos-caddyfile-debug
description: "Debug and hot-patch Caddyfile on arifOS VPS. Handles bind-mounted Caddyfile (RO inside container), handle_path vs handle gotchas, .well-known root path bugs, MCP llms-full.txt 500 fix, Cloudflare 200+body-404 detection, and AAA container static-server vs proxy routing. Full surface audit workflow included."
tags: [caddy, vps, routing, web, arifos, deploy, mcp]
version: 2.1.0
author: arifOS AAA
license: AGPL-3.0
---

# arifOS Caddyfile Debug & Hot-Patch Workflow

## ⚠️ CRITICAL: The Caddyfile is Bind-Mounted Read-Only

**`/etc/caddy/Caddyfile` inside the container is mounted `ro` (read-only).** You cannot write to it from inside the container. All edits must use the pipe-in workaround.

## Step 1: Extract Current Caddyfile
```bash
docker exec caddy sh -c "cat /etc/caddy/Caddyfile" > /tmp/Caddyfile.backup
```

## Step 2: Edit locally (patch, write_file, etc.)

## Step 3: Format + Validate (MUST do before reload)
```bash
# Pipe into container temp location — NOT the mounted path
cat /tmp/Caddyfile.backup | docker exec -i caddy sh -c "cat > /tmp/Caddyfile.new"

# Format + validate
docker exec caddy sh -c "caddy fmt /tmp/Caddyfile.new --overwrite"
docker exec caddy sh -c "caddy validate --config /tmp/Caddyfile.new" 2>&1 | tail -3
```

## Step 4: Reload Running Caddy
```bash
docker exec caddy sh -c "caddy reload --config /tmp/Caddyfile.new --adapter caddyfile"
```
If output says `"config is unchanged"` — run `caddy fmt --overwrite` first, then reload.

---

## Debugging 404 on MCP Endpoints

**Check which route is matching:**
```bash
docker exec caddy caddy adapt --config /tmp/Caddyfile.new --adapter caddyfile 2>&1 | python3 -c "
import sys,json
d=json.load(sys.stdin)
http = d.get('apps',{}).get('http',{})
srv = http.get('servers',{}).get('srv0',{})
routes = srv.get('routes',[])
for i,r in enumerate(routes):
    text = json.dumps(r)
    if 'mcp.arif' in text or '.well-known' in text:
        print(f'Route {i}:', text[:400])
"
```

**Test from inside container (bypasses Cloudflare cache):**
```bash
docker exec caddy sh -c "wget -O- -q --header 'Host: mcp.arif-fazil.com' http://localhost/.well-known/mcp/server.json"
```

---

## handle_path vs handle + uri strip_prefix

**`handle_path` automatically strips the matched prefix from the URI before serving files.**

```
# CORRECT — strips /apex from path before looking in /var/www/html/apex
handle_path /apex/* {
    root * /var/www/html/apex
    try_files {path} /index.html
    file_server
}

# WRONG — handle + uri strip_prefix does NOT affect {path} in try_files
# {path} still contains the original URI prefix
handle @apex {
    uri strip_prefix /apex
    root * /var/www/html/apex
    try_files {path} /index.html
    file_server
}
```

---

## Two Critical Routing Bugs + Fixes

### Bug 1: `.well-known` root path resolution
```
# WRONG — file_server looks for /var/www/html/arifos/.well-known/mcp/.well-known/mcp/server.json
handle /.well-known/mcp/* {
    root * /var/www/html/arifos/.well-known/mcp
    file_server
}

# CORRECT — root = parent dir, file_server resolves request_path relative to it
# Request /.well-known/mcp/server.json → /var/www/html/arifos + /.well-known/mcp/server.json
handle /.well-known/mcp/* {
    root * /var/www/html/arifos
    file_server
}
```

### Bug 2: Redirect losing URI path
```
# WRONG — redirects to root, losing full path
handle {
    redir https://arifos.arif-fazil.com permanent
}

# CORRECT — {uri} preserves the matched path
handle {
    redir https://arifos.arif-fazil.com{uri} permanent
}
```

---

## Web Root Structure

| Domain | Web Root | Content Source |
|--------|----------|----------------|
| `arif-fazil.com` | `/var/www/html/arif/dist` | Built React (canonical) |
| `arifos.arif-fazil.com` | `/var/www/html/arifos` | `/root/arifOS/static/` |
| `aaa.arif-fazil.com` | `/var/www/html/aaa` | arif-sites |
| `mcp.arif-fazil.com` | Proxy only | → arifosmcp:8080 + .well-known |

---

## Observatory Landing Page Deployment

`/root/arifOS/static/` has two key landing pages:

| File | Size | Purpose |
|------|------|---------|
| `dashboard/index.html` | 26KB | Basic health/status page |
| `landing/dynamic-index.html` | 44KB | Full thermodynamic ΔΩΨ landing |

Deploy the richer landing page:
```bash
cp /root/arifOS/static/landing/dynamic-index.html /var/www/html/arifos/index.html
```

Update deploy-vps.sh to use landing page (not dashboard):
```bash
# CORRECT
cp /root/arifOS/static/landing/dynamic-index.html $WEB_ROOT/arifos.arif-fazil.com/index.html

# WRONG (old)
cp /root/arifOS/static/dashboard/index.html $WEB_ROOT/arifos.arif-fazil.com/index.html
```

---

## arifOS Kernel MCP Verified Endpoints (2026-05-01)

| Endpoint | URL | Status |
|----------|-----|--------|
| MCP JSON-RPC | `https://mcp.arif-fazil.com/mcp` | ✅ |
| Health | `https://mcp.arif-fazil.com/health` | ✅ |
| Tools list | `https://mcp.arif-fazil.com/tools` | ✅ |
| Server card | `https://mcp.arif-fazil.com/.well-known/mcp/server.json` | ✅ (fixed) |
| Observatory | `https://arifos.arif-fazil.com/` | ✅ (landing v2) |

---

## New Findings (2026-05-01 Surface Audit)

### Bug 1: `handle_path` for `.well-known/*` with file_server doubles the path
```
# WRONG — handle_path strips /.well-known, then file_server appends it again
# Request for /.well-known/arifos.json:
#   → strip /.well-known → /
#   → root + /.well-known/arifos.json = /var/www/html/arifos/.well-known/arifos.json (MISSING)
handle_path /.well-known/* {
    root * /var/www/html/arifos/.well-known
    file_server
}

# CORRECT for proxying (preserve full path):
handle /.well-known/* {
    reverse_proxy arifosmcp:8080
}

# CORRECT for static files if you want handle_path:
handle_path /.well-known/* {
    root * /var/www/html/arifos     # NOT /var/www/html/arifos/.well-known
    file_server
}
```

### Bug 2: MCP `llms-full.txt` returns 500 — Starlette vs FastMCP
- **Symptom**: `curl https://arifOS-site/llms-full.txt` → HTTP 500, `{'error': "'StarletteWithLifespan' object has no attribute 'list_tools'"}`
- **Root cause**: In `rest_routes.py`, `mcp` is the Starlette app (`app = mcp.http_app()`) not the FastMCP server instance. Calling `mcp.list_tools()` on it fails.
- **Fix in** `/root/arifOS/arifosmcp/runtime/rest_routes.py`:
  ```python
  # WRONG:
  tools = await mcp.list_tools()
  
  # CORRECT (use public registry, no async needed):
  specs = public_tool_specs()
  tool_entries = [(s.name, s.description) for s in specs]
  ```
- **After fix**: Restart arifOS MCP container to pick up new code
  ```bash
  docker compose -f /root/arifOS/docker-compose.yml restart arifosmcp
  ```

### Bug 3: AAA container is NOT a Caddy reverse proxy
- `aaa` container (`compose-aaa:v1.0.0`) is a static file server — no Caddy inside
- No `/.well-known/` directory inside `aaa` container
- **Fix**: Caddyfile for `aaa.arif-fazil.com` must proxy `/.well-known/*` to `arifosmcp:8080`

### Bug 4: Cloudflare returns HTTP 200 with "404: Not Found" in body
- Detection: `curl -s -w "\nHTTP:%{http_code}" https://domain/path`
- If output shows `HTTP:200` but body contains `404: Not Found` → Cloudflare cached a 404 response
- **Fix**: Purge Cloudflare cache for affected URL, or wait for TTL expiry

---

### Bug 5: Reverse-Proxy Path Doubling (MCP 404 / Cloudflare 502)

**Symptom:** MCP server works from inside Docker (`curl http://geox_eic:8081/mcp/stream` returns 200) but external calls get 404, or Cloudflare returns 502.

**Root cause:** Adding a path suffix to the upstream in Caddyfile's `reverse_proxy` doubles the URI.

```
# WRONG — Caddy appends the request path to the upstream, doubling it
# Request to /mcp/stream → proxy to geox_eic:8081/mcp/stream + /mcp/stream = /mcp/stream/mcp/stream
reverse_proxy geox_eic:8081/mcp/stream {
    # ... Caddy 404s because uvicorn has no route for /mcp/stream/mcp/stream
}
```

**Fix:** Proxy to the root upstream (no path suffix). Let Caddy preserve and forward the original request URI:

```
# CORRECT — Caddy forwards the request path as-is
handle /mcp* {
    reverse_proxy geox_eic:8081 {
        header_up Accept "application/json, text/event-stream"
        flush_interval -1
    }
}
```

**When you NEED path rewriting:** Use `handle_path` (which strips the matched prefix) OR `uri` directive inside `handle`, NOT a suffix on the upstream address.

## Gotchas

1. **Bind-mount is RO** — never `docker exec caddy cat > /etc/caddy/Caddyfile`. Always pipe IN.
2. **Caddyfmt required** — unformatted Caddyfiles silently rejected or "config unchanged" on reload.
3. **Route order matters** — more specific paths must come BEFORE catch-all `handle`.
4. **Cloudflare caches 404** — always use `curl -sI` (not browser) to check true HTTP status.
5. **`config is unchanged`** — means the in-memory config equals new config. Run `caddy fmt --overwrite` on temp file to ensure diff.
