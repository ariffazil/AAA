---
name: arifos-site-debug
description: Systematic diagnosis of arifOS federation site/service health — arif-fazil.com subdomains, MCP endpoints, Caddyfile routing, and container health. Activate when sites appear down or returning unexpected HTTP codes.
category: devops
---

# arifos-site-debug

## Diagnostic Chain (always run in order)

### Step 1 — Check Caddyfile (on VPS)
```bash
ssh root@VPS "cat /root/Caddyfile"
```
Caddyfile is at `/root/Caddyfile` on the VPS (not in a subdirectory — check `ls /root/Caddyfile`).

Look for the subdomain block. Questions to answer:
- Does the subdomain have a `reverse_proxy` directive?
- Or only `import aasic-landing` (static file server)?

### Step 2 — Check container is running
```bash
ssh root@VPS "docker ps --format '{{.Names}} {{.Status}} {{.Ports}}' | sort"
```
Match container name to expected service. Note the port bindings: `127.0.0.1:8081->8081/tcp` means Caddy must use the IP, not the container name.

### Step 3 — Test container directly (on VPS)
```bash
ssh root@VPS "curl -s http://localhost:PORT/health"
```
If this fails → container is the problem.
If this succeeds → Caddy routing is the problem.

### Step 4 — Test public endpoint (from outside)
```bash
curl -s -o /dev/null -w "HTTP:%{http_code}" https://SUBDOMAIN.arif-fazil.com/
curl -s https://SUBDOMAIN.arif-fazil.com/ | head -5
```

### Step 5 — Check Accept header (MCP endpoints)
Many arifOS MCP servers (well, arifos) require:
```
Accept: application/json, text/event-stream
```
Without this, the server returns `406 Not Acceptable`.

Test:
```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' \
  http://localhost:PORT/mcp
```

### Step 6 — Cloudflare-specific
Cloudflare can return challenge/redirect pages when:
- A request looks like a bot
- Origin server returns non-200
- Zone has attack mode enabled

If you see Cloudflare challenge HTML in the response, the origin is likely fine — Cloudflare is the intermediary.

## Common Failure Patterns

| Pattern | HTTP Code | Cause | Fix |
|---------|-----------|-------|-----|
| Static landing only, no MCP | 200 but no `/mcp` route | Caddyfile has `file_server` only, no `reverse_proxy /mcp/*` | Add reverse_proxy directive |
| MCP requires Accept header | 406 | Client sent wrong Accept type | Fix client headers |
| Container down | 502/504 | Container not running or port wrong | Restart container |
| Cloudflare challenge | HTML page | CF intermediate, not origin | Check CF dashboard |
| Redirect to HTTPS | 301 | Caddy not handling HTTPS properly | Check Caddyfile binding |
| **well.arif-fazil.com → arifos redirect** | **301 to arifos** | **well block missing from Caddyfile OR placed incorrectly; Cloudflare catches it as catchall redirect** | **Check `docker exec caddy caddy adapt` to verify domain block loaded; validate Caddyfile structure** |
| **Caddy can't reach container** | **000 or 502** | **Container not on same Docker network as Caddy, or hostname not resolvable from Caddy container** | **Use `docker inspect CONTAINER --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'` to get actual IP, then verify route with `docker exec caddy caddy adapt`** |
| **Wrong container port** | **502** | **Assumed wrong port (geox_eic uses 8081, not 8000)** | **Always verify with actual listening port via `docker exec CONTAINER cat /proc/net/tcp6` or `ss -tlnp`** |

### Critical: Container Network Isolation
Caddy runs inside Docker and can only reach other containers on shared networks. If a container name doesn't resolve from inside Caddy:
1. `docker inspect caddy --format '{{range .NetworkSettings.Networks}}{{.NetworkID}}{{end}}'` — get Caddy's network  
2. `docker inspect TARGET --format '{{range .NetworkSettings.Networks}}{{.NetworkID}} {{.IPAddress}}{{end}}'` — get target's networks
3. If different networks → add container to Caddy's network via `docker network connect`, OR use the container's actual IP directly in the reverse_proxy directive
4. After fix: run `docker exec caddy caddy adapt` to verify the route block appears in adapted JSON

### Critical: well.arif-fazil.com Route Missing
This subdomain has repeatedly been absent from Caddyfile. When adding:
1. Place the block as a **top-level entry** in Caddyfile (not inside another block — Caddyfile is NOT whitespace-sensitive, but blocks must not be indented inside other directives)
2. Use Python to insert the block rather than `sed` to avoid indentation errors
3. After editing: `docker exec caddy caddy adapt --config /etc/caddy/Caddyfile > /tmp/caddy.json && python3 -c "import json; d=json.load(open('/tmp/caddy.json')); [print(k) for k in d['apps']['http']['servers']]"` to verify the server block appears
4. A missing domain block will fall through to Cloudflare's catchall redirect (301 to arifos)

### Critical: Diagnosing 301 Redirects (Cloudflare vs Caddy)
When a subdomain redirects unexpectedly:
1. `curl -sv https://SUBDOMAIN.arif-fazil.com/` — look at the `location:` header in the response
2. If `location: https://arifos.arif-fazil.com` → **Cloudflare** is handling this, not Caddy (Cloudflare has a catchall redirect rule)
3. If `location:` points to a different path → Caddy may have a redirect directive
4. Check Cloudflare Dashboard → Rules → Redirect Rules or Page Rules for the subdomain

## arifOS Federation Sites (canonical list)

| Subdomain | Service | Container Port | Expected Health |
|-----------|---------|----------------|-----------------|
| arif-fazil.com | Static landing | — | HTTP 200 |
| arifos.arif-fazil.com | arifOS MCP | 8080 | HTTP 200 + JSON |
| geox.arif-fazil.com | GEOX EIC container (geox_eic) | **8081** (not 8000) | HTTP 200 + JSON (needs reverse_proxy /mcp/* in Caddy) |
| well.arif-fazil.com | WELL MCP | 8083 | HTTP 200 + JSON (needs Accept header, needs own Caddyfile block — repeatedly missing from Caddyfile) |
| wealth.arif-fazil.com | WEALTH MCP | 8082 | HTTP 200 + JSON |
| aaa.arif-fazil.com | OpenClaw AAA | — | Static landing |
| forge.arif-fazil.com | A-FORGE | — | Static landing |

## Caddyfile Fix Template (R3 — needs approval)

To add MCP proxy to a subdomain that only has static landing:
```
SUBDOMAIN.arif-fazil.com {
    import constitutional-headers
    encode zstd gzip
    reverse_proxy /mcp/* CONTAINER_NAME:PORT
    import aasic-landing SUBDOMAIN
}
```

**This is R3 — always get Arif approval before editing Caddyfile on VPS.**

## Site Health Report Template

```
| Site                  | Status    | Notes                              |
| --------------------- | --------- | ---------------------------------- |
| arif-fazil.com        | ✅/⚠️/❌  | HTTP:XXX — description             |
| arifos.arif-fazil.com | ✅/⚠️/❌  | version, tools count, any issues   |
| geox.arif-fazil.com   | ✅/⚠️/❌  | /mcp route status                  |
| well.arif-fazil.com   | ✅/⚠️/❌  | Accept header handling             |
| wealth.arif-fazil.com | ✅/⚠️/❌  | service status                     |
```

## Trigger Conditions

Run this skill when:
- AGI reports site health issues
- Sites returning non-200 or unexpected codes
- New MCP endpoints not responding
- After any Caddyfile or container changes
