---
name: caddy-cloudflare-routing-debug
description: Debug Cloudflare + Caddy routing gaps — HTTP 200 with HTML 404 body, broken well-known routes, JSON serving failures, and healthcheck port mismatches on arifOS VPS.
triggers:
  - "route returns 200 but with HTML 404 content"
  - "well-known route returns 308 or HTML instead of JSON"
  - "JSON file exists but curl gets wrong content-type"
  - "container unhealthy despite server logs showing it running"
  - "nginx restart loop host not found upstream"
---

# Caddy Cloudflare Routing Debug Skill

## When to Use
When a route returns HTTP 200 but with HTML 404 body content, or when JSON/well-known routes appear broken. The Cloudflare layer can mask what Caddy is actually doing.

## Core Diagnostic Loop

### Step 1 — Establish what Cloudflare sees
```bash
curl -s -o /dev/null -w "%{http_code}" https://target-domain.com/path
```
If this differs from what you expect, check Cloudflare cache rules.

### Step 2 — Bypass Cloudflare, hit Caddy origin directly
```bash
docker exec caddy curl -s -o /dev/null -w "%{http_code}" "http://localhost/path" -H "Host: target-domain.com"
```
This is the **most important technique**. It returns the true Caddy origin response.

### Step 3 — Check if file physically exists in container
```bash
docker exec caddy cat /var/www/html/path/to/file 2>&1 | head -5
docker exec caddy ls -la /var/www/html/path/to/dir/ 2>&1
```

### Step 4 — Examine Caddyfile adapted config
```bash
docker exec caddy caddy adapt --config /etc/caddy/Caddyfile --adapter caddyfile 2>/dev/null | python3 -c "
import json, sys
cfg = json.load(sys.stdin)
servers = cfg.get('apps', {}).get('http', {}).get('servers', {})
for name, srv in servers.items():
    for r in srv.get('routes', []):
        for m in r.get('match', []):
            if 'target-host' in str(m):
                print(json.dumps(r, indent=2))
"
```

### Step 5 — Test with explicit Host header + path
```bash
docker exec caddy curl -sL --max-time 5 "http://localhost/.well-known/file.json" -H "Host: domain.com"
```

## Common Caddy v2 Routing Patterns

### `.well-known/*` not served
**Symptom:** `/.well-known/did.json` returns 308 permanent redirect or HTML 404.
**Reason:** Caddy's catch-all `try_files {path} /index.html` handles dot-path routes BEFORE the file_server sees them. The `/000/*` and `/999/*` directives set specific roots but there is no equivalent for `/.well-known/*`.
**Fix:** Add explicit handler before the catch-all:
```
handle /.well-known/* {
    root * /var/www/html/arif/.well-known
    file_server
}
```

### `handle /subdir*` exists but root-level paths return 301 instead of being proxied
**Symptom:** `https://mcp.arif-fazil.com/status.json` returns 301 → redirect to another domain, while `https://mcp.arif-fazil.com/mcp` (POST) returns 405 and works correctly.
**Reason:** Caddy's `handle /mcp*` only matches paths starting with `/mcp`. Paths like `/status.json`, `/health`, `/ready` are NOT under `/mcp` so they fall through to the next `handle` block — typically the catch-all `redir` directive that does a permanent redirect. This is Caddyfile drift: the desired config has explicit handlers for these paths, but the running container's Caddyfile (bind-mounted from host) is missing them.
**Diagnostic:**
```bash
# Step 1 — Confirm what the origin actually returns
curl -sI https://mcp.arif-fazil.com/status.json | grep -E "^HTTP|^location"

# Step 2 — Check live Caddyfile vs local file
docker exec caddy cat /etc/caddy/Caddyfile | grep -A 15 "mcp.arif-fazil.com"
diff $(docker exec caddy cat /etc/caddy/Caddyfile) /root/arifOS/Caddyfile

# Step 3 — Confirm backend is reachable from Caddy (check logs)
docker logs --tail 50 caddy 2>&1 | grep "172.19.0"  # Caddy's IP reaching backends
docker logs --tail 50 arifosmcp 2>&1 | grep "172.19.0"  # arifosmcp receiving requests

# Step 4 — If logs show 405 on /mcp from Caddy's IP, the proxy IS working — the issue is route gaps
```
**Key insight:** 405 on `/mcp` means Caddy IS successfully proxying to arifosmcp and arifosmcp is rejecting GET (correct behavior — `/mcp` is POST-only). If you see 405, the transport layer is fine. The problem is that paths NOT under `/mcp*` are not matched by any `handle` block, so they fall through to the catch-all `redir`.
**Fix:** Add explicit handlers in the site block:
```
mcp.arif-fazil.com {
    handle /mcp* {
        reverse_proxy arifosmcp:8080
    }
    handle /status.json {
        reverse_proxy arifosmcp:8080
    }
    handle /health {
        reverse_proxy arifosmcp:8080
    }
    handle /ready {
        reverse_proxy arifosmcp:8080
    }
    handle {
        redir https://arifos.arif-fazil.com/mcp{uri} permanent
    }
}
```
Then validate and reload:
```bash
docker exec caddy caddy validate --config /etc/caddy/Caddyfile
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
```
**Counterintuitive lesson:** When debugging a proxy that returns 301/308, the instinct is to check network connectivity. But if `handle /mcp*` works (405 on GET = arifosmcp is receiving and rejecting), the backend is reachable. The issue is purely route matching. Check `handle` block coverage before checking `ss`/`netstat`/`iptables`.

### `/*.json` files served as HTML
**Symptom:** `/.well-known/arif-human.json` returns HTTP 200 but with HTML "404: Not Found" body.
**Reason:** File doesn't physically exist on disk at the expected path, so `try_files {path} /index.html` returns `index.html` content — but with HTTP 200.
**Fix:** Either create the JSON file at the correct path, or add a dedicated `handle_path` route that returns the JSON with correct Content-Type.

### `/.well-known/*` returns HTTP 404 from Cloudflare with no cache headers
**Symptom:** `curl -sI https://domain.com/.well-known/file.json` returns `server: cloudflare`, no `cf-ray` → actually this DOES have cf-ray, but NO `cf-cache-status`. Body is "Not Found" from CF edge.
**Distinction:**
- **Cached 404** → has `cf-cache-status: EXPIRED/HIT/MISS`, `age: N` headers. Origin returned 404, CF cached it.
- **Generated 404** → has `server: cloudflare`, NO `cf-cache-status` header. Cloudflare itself is producing the 404 before reaching origin.
**Common causes:**
  - Cloudflare WAF Custom Rule blocking `.well-known` path or any `.json` in dot-folders
  - Page Rule with "Disable Security" not applied to `/.well-known/*`
  - Cloudflare Bot Management / Super Bot Fight Mode blocking dot-file paths
  - CF Zona settings "Always Online" serving stale cached 404
**Fix:** Cloudflare Dashboard → Security → WAF → Custom Rules → look for rules matching `/.well-known/*` or patterns like `*.json` in dotdirs → disable or set to Log. Also check Security → Bots → Bot Fight Mode (can block `.json` paths silently).
**Diagnostic:**
```bash
# Check if Cloudflare is generating or caching the 404
curl -sI "https://domain.com/.well-known/file.json" --max-time 8 | grep -iE "server:|cf-ray|cf-cache-status|age"

# Test origin directly (bypass Cloudflare proxy)
curl -sI "https://72.62.71.199/.well-known/file.json" -H "Host: domain.com" --max-time 8
# If origin returns 200 and CF returns 404 → CF is generating the 404
```

### Nginx upstream DNS name mismatch
**Symptom:** Nginx container in restart loop, logs show `host not found in upstream "container-name:port"`.
**Reason:** Compose `container_name` differs from the hostname referenced in nginx config.
**Fix:** Align nginx upstream host with the actual `container_name` in docker-compose.yml.

## Diagnostic Command Cheatsheet
```bash
# Check container health
docker inspect <container> --format '{{json .State.Health}}' | python3 -m json.tool

# Check live Caddy routes for a host
docker exec caddy caddy adapt --config /etc/caddy/Caddyfile 2>/dev/null | python3 -c "
import json,sys; cfg=json.load(sys.stdin)
for n,s in cfg.get('apps',{}).get('http',{}).get('servers',{}).items():
    for r in s.get('routes',[]):
        for m in r.get('match',[]):
            if 'hostname' in str(m): print(json.dumps(r,indent=2))
"

# Test Caddy origin with Host header
docker exec caddy curl -sL -o /dev/null -w "%{http_code}" "http://localhost/path" -H "Host: domain.com"

# Test Caddy HTTPS origin (from inside container)
docker exec caddy curl -sk -o /dev/null -w "%{http_code}" "https://localhost/path" -H "Host: domain.com"

# Check file exists in container www root
docker exec caddy ls -la /var/www/html/arif/.well-known/
docker exec caddy cat /var/www/html/arif/.well-known/file.json | wc -c
```

## Key Insight
Caddy's `try_files {path} /index.html` silently returns the `index.html` content with HTTP 200 even when the requested file doesn't exist — it never produces an actual 404 status code for missing files under served paths. This is why "HTTP 200 but HTML 404 body" is the signature of a routing gap, not a missing file.

- **arifOS MCP server port**: Container internal is **8080** (Uvicorn), NOT 3000. Docker host maps 3000→3000 AND 8080→8080 in some compose variants, but the container process itself listens on 8080.
- **Caddyfile proxy port**: Must be `arifosmcp:8080` — pointing to `arifosmcp:3000` produces 502 from Caddy.
- **Active vs desired compose**: `/root/compose/docker-compose.yml` is desired state. `/root/arifOS/deployments/af-forge/docker-compose.yml` is what Docker used to launch the live containers. Find which compose created the running container: `docker inspect arifosmcp --format '{{index .Config.Labels "com.docker.compose.project.config_files"}}'`

## Notes
- Docker mount source `/root/sites` → destination `/var/www/html` in the caddy container.
- Always test origin first before checking Cloudflare settings.
- HTTP 308 from `docker exec caddy curl` means the route exists but is doing a permanent redirect. Use `-L` to follow it and see the final destination.
