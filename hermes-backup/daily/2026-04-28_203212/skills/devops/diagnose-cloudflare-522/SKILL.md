---
name: diagnose-cloudflare-522
description: Diagnose Cloudflare error code 522 — origin connection refused — on arifOS or any public-facing service
tags: [cloudflare, networking, docker, port-mapping, 522, devops]
created: 2026-04-26
---

# diagnose-cloudflare-522

## Trigger
Any `error code: 522` response from Cloudflare — "Origin Connection Refused" — on a subdomain that should be working.

## What 522 Means
Cloudflare reached the origin IP but **nothing was listening on port 443 (HTTPS) or port 80 (HTTP)**. The origin server may be healthy internally, but the external connection path is broken.

## Diagnostic Sequence

### 1. Confirm the 522 and get full TLS handshake trace
```bash
curl -sv https://mcp.arif-fazil.com/ 2>&1 | grep -E "< HTTP|error code|subject|subjectAltName"
```
- 522 = Cloudflare cannot reach origin
- TLS cert valid + handshake succeeds = port 443 is open but something else handles it

### 2. Identify the actual origin IP (not Cloudflare proxy)
```bash
dig domain.com A +short   # Returns Cloudflare IPs, not origin
```

### 3. Test direct to origin IP
```bash
# Test port 443 directly on origin IP
timeout 5 openssl s_client -connect <origin_ip>:443 -servername domain.com

# Test port 4433 (common mis-mapping)
timeout 5 openssl s_client -connect <origin_ip>:4433 -servername domain.com
```

### 4. Check docker port bindings — THE MOST COMMON CAUSE
```bash
# What ports are mapped to the proxy container
docker port <container_name>

# What's listening on host port 443
ss -tlnp | grep ':443 '

# Compare compose vs actual
grep "ports:" /root/compose/docker-compose.yml | grep caddy
```

**The classic mistake:**
```diff
# docker-compose.yml — WRONG
ports: ["8082:80", "4433:443"]   # host 4433 → container 443, host 443 is EMPTY

# CORRECT
ports: ["8082:80", "443:443"]     # host 443 → container 443
```

### 5. Verify internal routing works
```bash
# From inside docker network
docker exec caddy sh -c "curl -s --max-time 5 http://arifosmcp:8080/health"

# From host (not inside docker)
curl -s http://localhost:8080/health
```

### 6. Check firewall
```bash
ufw status | grep 443
iptables -L INPUT -n | grep 443
```

## Fix Pattern

If the diagnosis is `"4433:443"` in compose (or similar wrong mapping):
```diff
# docker-compose.yml
- ports: ["8082:80", "4433:443"]
+ ports: ["8082:80", "443:443"]
```

Then restart:
```bash
cd /root/compose && docker compose up -d caddy
```

## MCP Route Discovery — Common Caddyfile Gap

## MCP Route Discovery — Common Caddyfile Gap

Even when 522 is fixed, MCP clients use `/tools` (GET) and `/api/tools` for tool surface discovery. The `aasic-landing` template in the Caddyfile catches all unmatched routes and serves static HTML — the request never reaches arifOS.
**Symptoms:** `/health` works (proxied), `/tools` returns empty `{}` or static HTML.

**Fix — add explicit routes in the Caddyfile:**
```diff
 mcp.arif-fazil.com {
     import aasic-landing mcp
     reverse_proxy /health arifosmcp:8080
     reverse_proxy /mcp* arifosmcp:8080
+    reverse_proxy /tools arifosmcp:8080
+    reverse_proxy /api/tools arifosmcp:8080
 }
```

**Verification:**
```bash
curl -s https://mcp.arif-fazil.com/tools | python -m json.tool | head -5
# Expected: {"tools": [{"name": "arif_session_init"...
```

## Landing Page Dynamic JS Failures — Boot() Catch Pattern

The landing page (`index.html`) at `https://mcp.arif-fazil.com/` runs a `boot()` async function that fetches live data from 4 sources on load. When any of these fail, the page shows **"LIVE · Degraded"** with `Failed to execute 'json' on 'Response': Unexpected end of JSON input`.

**Typical failure calls in boot():**
```javascript
await Promise.all([
    fetch('/health'),                          // ✅ Works
    fetch('/api/constitution'),               // ❌ 404 — missing route
    fetch('/.well-known/mcp/server.json'),   // ❌ 404 — missing route
    fetch('/mcp', { method:'POST', ... })    // ❌ 406 or tool removed
])
```

**If /api/constitution and /.well-known/mcp/server.json should exist:**
Add to Caddyfile:
```diff
+    reverse_proxy /api/constitution arifosmcp:8080
+    reverse_proxy /.well-known/mcp/server.json arifosmcp:8080
```

**If the arif_ping/arif_selftest tool was removed from surface:**
The landing page still references `arif_ping` in the boot() call. This tool may have been purged from the canonical surface. The catch block will trigger → "Unable to load live tool surface." message appears. Fix by either: (a) restoring the tool, or (b) updating the landing page JS to use `/tools` GET which always works.

**Landing page verification (from browser console or curl):**
```bash
curl -sI https://mcp.arif-fazil.com/api/constitution  # Should be 200, not 404
curl -sI https://mcp.arif-fazil.com/.well-known/mcp/server.json  # Should be 200
curl -s https://mcp.arif-fazil.com/tools | wc -c  # Should be ~68KB for 13 tools
```

## Key Signals Reference
```bash
# Confirm host port 443 is occupied
ss -tlnp | grep ':443 '

# Test from outside via Cloudflare
curl -s -o /dev/null -w "%{http_code}" https://mcp.arif-fazil.com/
curl -s -o /dev/null -w "%{http_code}" https://mcp.arif-fazil.com/health
curl -s -o /dev/null -w "%{http_code}" https://mcp.arif-fazil.com/tools
```

Expected: 200 on all three.

## Key Signals Reference

| Signal | Meaning |
|--------|---------|
| `curl` → 522 | Cloudflare cannot reach origin on 443 |
| `openssl s_client` → connection refused on `:443` but succeeds on `:4433` | Wrong port mapping in compose |
| Internal curl works, external returns 522 | Port mapping gap (not an app failure) |
| TLS handshake succeeds, then 522 | Something intercepts before reaching Caddy |
| `ss -tlnp` shows nothing on `:443` | Port not mapped — fix compose |
| Firewall `Status: active` + no 443 rule | Add `ufw allow 443/tcp` |

## Related Skills
- `arifos-mcp-sse-debug` — for MCP-specific route debugging when the proxy is working but tool surface returns wrong data
- `arifos-mcp-tool-audit` — for validating the canonical 13-tool surface post-fix