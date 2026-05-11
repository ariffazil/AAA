---
name: cloudflare-dns-ops
description: Cloudflare DNS operations on arifOS VPS — token scopes, record management, Caddyfile debugging
triggers:
  - "cloudflare"
  - "arifosmcp.arif-fazil.com"
  - "DNS record"
  - "caddy reload"
---

# Cloudflare DNS Operations — arifOS VPS

> **DEPRECATED:** For new Cloudflare work, use `cloudflare-agents` instead. This skill is kept for DNS-specific operations only.

## Token Types (Critical)

| Token | Location | Prefix | Scope | Can Purge Cache? |
|-------|----------|--------|-------|-----------------|
| DNS-only | `/root/.cloudflare_token` | `cfut_` | DNS records only | No |
| Full API | env `CLOUDFLARE_API_TOKEN` | `cfat_` | All CF API | Yes |

**Rule: `cfut_` cannot purge cache. Use `cfat_` for cache operations.**

Zone ID (arif-fazil.com): `6e837d3be53b37dcf79e0f09a1e14faa`

## Common Operations

### List all arifOS DNS records
```bash
curl -s "https://api.cloudflare.com/client/v4/zones/6e837d3be53b37dcf79e0f09a1e14faa/dns_records?per_page=50" \
  -H "Authorization: Bearer <token>" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for r in d.get('result',[]):
    print(f\"{r['name']} | {r['type']} | TTL:{r['ttl']} | Proxied:{r['proxied']}\")
"
```

### Delete a DNS record
```bash
curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/6e837d3be53b37dcf79e0f09a1e14faa/dns_records/<record_id>" \
  -H "Authorization: Bearer <cfut_token>" \
  -H "Content-Type: application/json"
```

### Purge cache (requires cfat_ token)
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/6e837d3be53b37dcf79e0f09a1e14faa/purge_cache" \
  -H "Authorization: Bearer <cfat_token>" \
  -H "Content-Type: application/json" \
  -d '{"files":["https://domain.arif-fazil.com/*"]}'
```

## Caddyfile Debugging (VPS)

### Find where Caddy reads its config inside container
```bash
docker inspect caddy --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}'
docker exec caddy ls /etc/caddy/
```

### Reload Caddy (after editing the volume-mounted config)
```bash
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
```

### Verify Caddyfile content inside container
```bash
docker exec caddy cat /etc/caddy/Caddyfile | grep -n "domain.name"
```

**Common mistake:** Editing `/root/arifOS/Caddyfile` or `/root/compose/Caddyfile` and reloading, but the container is using a different volume mount. Always verify which file the container actually uses FIRST.

## arifOS Relevant Domains
- `mcp.arif-fazil.com` — canonical MCP surface (working)
- `arifosmcp.arif-fazil.com` — removed 2026-04-29 (DNS deleted)
- `arifos.arif-fazil.com` — federation hub with MCP
- `arif-fazil.com` — apex redirect
