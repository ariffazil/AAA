# Agentic Discovery Deployment — ARD v0.91 / Lighthouse 13.5

> Reference for `forge-agentic-web-builder`. Covers ARD manifest structure,
> Caddy vhost patterns, Cloudflare caching, and verification.

## ARD v0.91 Spec Summary

Agentic Resource Discovery (ARD) is how AI agents find tools, MCP servers, skills,
and other callable services at runtime. Publishers describe capabilities in a JSON
file on their own domain; registries crawl those files and answer plain-language queries.

**Spec:** v0.91 (August 2026) — Authors: Junjie Bu (Google), R.V. Guha (Microsoft),
Shaun Smith (Hugging Face). Still a Proposal, not a ratified standard.

**Key distinction:** ARD is discovery, not execution. MCP defines how to call a tool.
ARD defines how to find out the tool exists.

## The 4 Lighthouse 13.5 Discovery Vectors

Lighthouse probes four vectors to find ARD catalogs. All 4 must pass for full compliance:

| Vector | Mechanism | Caddy Implementation |
|--------|-----------|---------------------|
| 1. robots.txt | `Agentmap: <url>` directive | Static file in organ web root |
| 2. HTML DOM | `<link rel="ard" href="/.well-known/ard.json" />` | Injected in shell generator or index.html |
| 3. HTTP Header | `Link: <...>; rel="ard"` | `tls_origin` snippet header directive |
| 4. Direct Fallback | `/.well-known/ard.json` (v0.91) or `/.well-known/ai-catalog.json` (v0.9) | Static file served from `.well-known/` |

If a site provides no pointer and no catalog, Lighthouse marks Not Applicable.
If a catalog is declared but has schema errors or is unloadable, it fails.

## ARD Manifest Structure

```json
{
  "$schema": "https://agenticresourcediscovery.org/schemas/v0.91/ard-manifest.json",
  "specVersion": "0.91",
  "name": "<domain> Agentic Resource Discovery Catalog",
  "description": "...",
  "updatedAt": "<ISO 8601>",
  "publisher": {
    "name": "...",
    "displayName": "...",
    "identifier": "did:web:<domain>",
    "url": "https://<domain>",
    "contact": "..."
  },
  "trustManifest": {
    "identity": "did:web:<domain>",
    "identityType": "did:web",
    "verificationMethod": "https://<domain>/.well-known/did.json#key-1",
    "governance": "...",
    "license": "..."
  },
  "entries": [
    {
      "identifier": "urn:air:<domain>:<type>:<name>",
      "displayName": "...",
      "type": "application/mcp-server+json",
      "url": "https://<mcp-endpoint>",
      "documentation": "https://<docs-page>",
      "description": "...",
      "tags": ["..."],
      "capabilities": ["..."],
      "representativeQueries": [
        "natural language query 1",
        "natural language query 2"
      ]
    }
  ]
}
```

**Required per entry:** identifier (URN), displayName, type (IANA media type),
either `url` or inline artifact data.

**Critical field:** `representativeQueries` — 2-5 natural-language phrases.
Per the ARD glossary, an entry without representative queries "cannot be found by search".

**URN format:** `urn:air:<publisher-domain>:<namespace>:<agent-name>`
Publisher domain must be verifiable (anti-squatting).

**Media types (de facto, IANA registration pending):**
- `application/mcp-server+json` — MCP servers
- `application/a2a-agent-card+json` — A2A agents
- `application/ai-skill` — Skills

## Caddy Vhost Patterns

### Pattern 1: robots.txt with no-cache (MANDATORY for all organs)

```caddy
handle /robots.txt {
    root * /var/www/html/<organ>
    header Cache-Control "no-cache, no-store, must-revalidate"
    file_server
}
```

**Why no-cache:** Cloudflare aggressively caches static files. Without no-cache,
a newly deployed robots.txt with Agentmap directives can be stale for hours.
This makes all 4 Lighthouse vectors appear broken from CDN while origin is correct.

### Pattern 2: .well-known files from static root

```caddy
handle /.well-known/* {
    root * /var/www/html/<organ>
    file_server
}
```

If the organ has a catch-all `reverse_proxy` for `/.well-known/*` (e.g., arifOS kernel),
add specific handlers BEFORE the catch-all:

```caddy
handle /constitution.json {
    root * /var/www/html/arifos
    file_server
}
handle /.well-known/* {
    reverse_proxy 127.0.0.1:8088
}
```

### Pattern 3: Exclusion from root redirect

If the vhost has a `@not_telegram_webhook` or similar exclusion matcher that
catches most paths and redirects them, static files like `/constitution.json`
must be added to the exclusion list:

```caddy
@not_telegram_webhook not path /telegram/webhook /health /api/* ... /constitution.json /_shared/*
```

### Pattern 4: HTTP Link header (in tls_origin snippet)

Already deployed in `/etc/caddy/Caddyfile` shared snippet:
```caddy
Link "</llms.txt>; rel=\"llms\", </.well-known/ard.json>; rel=\"ard\", </.well-known/ai-catalog.json>; rel=\"ai-catalog\""
```
This applies to ALL vhosts that import `tls_origin`.

## Host → Web Root Map

| Organ | Live web root | robots.txt handler |
|-------|--------------|--------------------|
| arif-fazil.com | /var/www/html/arif (static) + /var/www/html (root_static) | `handle /robots.txt` in vhost |
| mcp | /var/www/html/mcp | embedded in vhost |
| geox | /var/www/html/geox | embedded in vhost |
| wealth | /var/www/html/wealth | embedded in vhost |
| well | /var/www/html/well | embedded in vhost |
| wellness | /var/www/html/well | `handle /robots.txt` (added 2026-09-22) |
| aaa | /var/www/html/aaa | embedded in vhost |
| arifos | /var/www/html/arifos | `handle /robots.txt` + no-cache (added 2026-09-22) |
| chron | /var/www/html/chron | `handle /robots.txt` |

**Note:** arif-fazil.com has a split root. `@root_static` serves from `/var/www/html/`.
Other paths serve from `/var/www/html/arif/`. robots.txt is in `@root_static`.

## Cloudflare Cache Pitfall

**Problem:** Deploying new robots.txt or .well-known files to origin does NOT
immediately update what Cloudflare serves. Cloudflare respects the origin's
`Cache-Control` header — if origin says `max-age=14400` (default), CDN caches
for up to 4 hours.

**Diagnosis:**
```bash
# Check what origin actually serves (bypass Cloudflare)
curl -s --resolve "DOMAIN:443:72.62.71.199" https://DOMAIN/robots.txt | grep agentmap

# Check what Cloudflare serves
curl -sI https://DOMAIN/robots.txt | grep -i "cache-control\|cf-cache-status"
```

If origin is correct but CDN is stale:
1. Add `Cache-Control: no-cache, no-store, must-revalidate` to the Caddy handler
2. Reload Caddy: `caddy reload --config /etc/caddy/Caddyfile --adapter caddyfile`
3. Wait for Cloudflare TTL expiry, or purge manually via Cloudflare dashboard

**API token limitation:** The `CLOUDFLARE_API_TOKEN` in `/root/.secrets/kunci-root.env`
may not have `Cache Purge` permission. If the API returns `Authentication error`
for purge requests, use the Cloudflare dashboard instead.

**Never fix CDN staleness by hand-editing the live tree.** Fix the Caddy config.

## Verification Procedure

After deploying ARD files to any organ:

```bash
# 1. Verify origin serves all 4 vectors
echo "=== robots.txt ==="
curl -s --resolve "DOMAIN:443:72.62.71.199" https://DOMAIN/robots.txt | grep -i agentmap
curl -sI --resolve "DOMAIN:443:72.62.71.199" https://DOMAIN/robots.txt | grep -i cache-control

echo "=== ard.json ==="
curl -s --resolve "DOMAIN:443:72.62.71.199" https://DOMAIN/.well-known/ard.json | head -5

echo "=== ai-catalog.json ==="
curl -s --resolve "DOMAIN:443:72.62.71.199" https://DOMAIN/.well-known/ai-catalog.json | head -5

echo "=== HTTP Link header ==="
curl -sI --resolve "DOMAIN:443:72.62.71.199" https://DOMAIN/ | grep -i "link:.*ard"

# 2. Verify Caddy config is valid
caddy validate --config /etc/caddy/Caddyfile 2>&1 | grep -E "Valid|Error"

# 3. Cross-check all 9 organ domains (batch)
for domain in arif-fazil.com mcp geox wealth well wellness aaa arifos chron; do
  d="${domain%%.*}.arif-fazil.com"
  [ "$domain" = "arif-fazil.com" ] && d="arif-fazil.com"
  has=$(curl -s --resolve "$d:443:72.62.71.199" "https://$d/robots.txt" 2>/dev/null | grep -ci agentmap)
  echo "$d: Agentmap=$has"
done
```

## Deployment Checklist (per organ)

1. [ ] `/.well-known/ard.json` exists and is valid JSON
2. [ ] `/.well-known/ai-catalog.json` exists (can be identical copy)
3. [ ] `robots.txt` has `Agentmap:` directives for both manifests
4. [ ] robots.txt handler has `Cache-Control: no-cache`
5. [ ] HTTP Link header includes `rel="ard"` and `rel="ai-catalog"`
6. [ ] HTML `<link>` tags present in page `<head>`
7. [ ] Caddy config validates: `caddy validate --config /etc/caddy/Caddyfile`
8. [ ] Origin verified via direct IP: `curl -s --resolve "DOMAIN:443:72.62.71.199"`
9. [ ] trustManifest URLs resolve to valid JSON (not redirects)
10. [ ] All `representativeQueries` are present (entries without them are invisible to search)