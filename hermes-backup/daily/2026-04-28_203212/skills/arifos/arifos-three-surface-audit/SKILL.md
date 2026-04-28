---
name: arifos-three-surface-audit
description: Audit and build the three public surfaces — arif-fazil.com (human root), arifos.arif-fazil.com (MCP Observatory), aaa.arif-fazil.com (A2A gateway). Verify protocol contracts, Caddyfile routing, and documentation drift.
triggers: ["arifOS surface", "three surfaces", "MCP Observatory", "A2A gateway", "documentation drift", "Caddyfile", "server card", "agent card"]
---

# arifOS Three-Surface Architecture Audit & Build

## When to use
Audit or build the three public surfaces: `arif-fazil.com`, `arifos.arif-fazil.com`, `aaa.arif-fazil.com`. Run this when deploying new endpoints, checking for documentation drift, or verifying protocol compliance.

## What each surface owns

| Surface | Canonical job | Must have |
|---------|--------------|-----------|
| `arif-fazil.com` | Human identity root | `/`, `/000`, `/999`, `/llms.txt`, cross-links to MCP + A2A |
| `arifos.arif-fazil.com` | MCP Observatory + Streamable HTTP `/mcp` | `/mcp` (POST+GET), `/mcp-server-card.json`, `/observatory/`, `/api/catalog/{tools,resources,prompts}`, `/api/status/summary` |
| `aaa.arif-fazil.com` | A2A Agent Gateway | `/.well-known/agent-card.json`, `/skills`, `/validator`, `message:send` + `message:stream` endpoints |
| `mcp.arif-fazil.com` | Migration alias only | 308 redirect to `arifos.arif-fazil.com/mcp/` |

## Caddyfile locations (in priority order)
1. `/root/arifOS/Caddyfile` — active on VPS (arifOS compose stack)
2. `/root/compose/Caddyfile` — federation stack
3. `/root/Caddyfile` — standalone

## Caddyfile patterns

### Subdomain with static files + API routes
```caddy
arifos.arif-fazil.com {
    root * /var/www/html/arif/observatory
    file_server

    @arifosAPI {
        header Authorization *Bearer*
        header Content-Type application/json
    }
    handle /api/* {
        reverse_proxy localhost:8888
    }
}
```

### AAA subdomain (A2A gateway)
```caddy
aaa.arif-fazil.com {
    root * /var/www/html/aaa
    file_server

    @a2aRPC {
        header Content-Type application/json
    }
    handle /message:send* {
        reverse_proxy localhost:9999
    }
    handle /message:stream* {
        reverse_proxy localhost:9999
    }
}
```

### Migration alias (redirect, no static files)
```caddy
mcp.arif-fazil.com {
    redir https://arifos.arif-fazil.com/mcp/ 308
}
```

## Critical Caddyfile gotcha
`handle PATH` matches **exactly** — `handle /api` does NOT match `/api/foo`. Use named matchers with `header` conditions instead:
```caddy
@myapi {
    path /api/*
}
handle @myapi {
    reverse_proxy localhost:8888
}
```

## Root problem: documentation drift
Hand-curated tool counts, protocol versions, and capability lists drift from live runtime. **Every catalog endpoint must be generated from runtime, never hand-written.**

The minimum live-generated endpoints needed:
- `GET /api/catalog/tools` — from `tools/list` MCP call
- `GET /api/catalog/resources` — from `resources/list` MCP call
- `GET /api/catalog/prompts` — from `prompts/list` MCP call
- `GET /api/status/summary` — from `/health` + runtime vitals

## A2A version discrepancy check
The blueprint flagged: `federation-health.json` says "A2A v0.3.0" but `mcp.arif-fazil.com` says "Planned". If `/federation-health.json` returns HTML, it means the static JSON file is missing from the doc root. Check:
```bash
curl -s "https://arif-fazil.com/federation-health.json" | jq .
```

## Build order
1. Create doc root: `mkdir -p /var/www/html/aaa /var/www/html/arif/observatory/api`
2. Write static files (Agent Card, homepage, skills page, validator)
3. Write runtime catalog server (Python HTTP sidecar for `/api/` endpoints)
4. Update Caddyfile with subdomain blocks
5. `docker exec caddy caddy reload` or `docker restart caddy`
6. Purge Cloudflare cache if Cloudflare is proxying
7. Verify all endpoints with curl (no `--max-time` suppress errors, check exit codes)

## Verification commands
```bash
# All three surfaces
curl -s https://aaa.arif-fazil.com/ -o /dev/null -w "%{http_code}\n"
curl -s https://arifos.arif-fazil.com/observatory/ -o /dev/null -w "%{http_code}\n"
curl -s https://mcp.arif-fazil.com/ -o /dev/null -w "%{http_code} %{redirect_url}\n"

# Protocol contracts
curl -s https://aaa.arif-fazil.com/.well-known/agent-card.json | jq .
curl -s https://arifos.arif-fazil.com/mcp-server-card.json | jq .

# Runtime catalogs
curl -s https://arifos.arif-fazil.com/api/mcp/tools.json | jq '.tools | length'
curl -s https://arifos.arif-fazil.com/api/catalog/resources | jq .
curl -s https://arifos.arif-fazil.com/api/status/summary | jq .

# A2A endpoints
curl -s https://aaa.arif-fazil.com/a2a -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"message:send","params":{...},"id":1}' \
  -w "\nHTTP %{http_code}"
```

## Cloudflare cache purge
If Cloudflare is proxying and returning stale 404s after Caddy reload:
```bash
# Get Cloudflare Zone ID from dashboard, then:
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"files":["https://arifos.arif-fazil.com/observatory/","https://arifos.arif-fazil.com/mcp-server-card.json"]}'
```
If token lacks purge rights, use Cloudflare dashboard → Caching → Purge Everything.
