---
title: "Skill: Site Architecture"
created: 2026-05-17
updated: 2026-05-17
version: 1.1.0
type: skill
category: federation
tags: [site-architecture, caddy, docker, compose, static-sites, arif-fazil.com, subdomain]
confidence: high
contested: false
floors: [F1, F7, F11]
risk_band: MEDIUM
sources: [/root/.kimi/skills/site-architecture/SKILL.md]
---

# Skill: Site Architecture — arifOS Estate Design

> **Source:** `/root/.kimi/skills/site-architecture/SKILL.md`
> **Agent:** Kimi (Constitutional Clerk)
> **Forged:** 2026-05-17

---

## Trigger Conditions

Load this skill when the task involves:
- Designing a new subdomain or service for `arif-fazil.com`
- Auditing the existing site estate for structural coherence
- Refactoring Caddy routes, Docker compose, or static site layouts
- Adding a new site to the federation surface
- Keywords: subdomain, caddy, site, estate, static-site, docker-compose, route

---

## Doctrine

The `arif-fazil.com` estate is a **constitutional federation of surfaces**. Every site is an organ with a defined role, boundary, and governance contract.

### The Four-Surface Model

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                            │
│  Browser (Human) │ AI Hosts │ External Agents               │
└──────┬───────────┴──────────┬────────────┴────────┬──────────┘
       │                      │                     │
       ▼                      ▼                     ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────────┐
│   SITE      │      │   WebMCP    │      │  MCP / A2A      │
│  (Static)   │◄────►│  (Browser)  │      │  (Agent Tools)  │
│             │      │             │      │                 │
│ • Landing   │      │ • Manifest  │      │ • Tools         │
│ • Docs      │      │ • Session   │      │ • Resources     │
│ • Wiki      │      │ • Prompts   │      │ • Prompts       │
└─────────────┘      └─────────────┘      └─────────────────┘
       │
       ▼
┌─────────────┐
│   Caddy     │  ← Reverse proxy, TLS termination
│  (:80/:443) │
└─────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│         SERVICE LAYER                 │
│  Docker Compose / VPS localhost       │
│  • arifOS (:8080)  • GEOX (:8081)    │
│  • WEALTH (:8082)  • WELL (:8083)    │
│  • A-FORGE (:7071) • apex (:3002)    │
└──────────────────────────────────────┘
```

---

## Canonical Subdomains

| Subdomain | Type | Build | Deploy | Repo Path |
|-----------|------|-------|--------|-----------|
| `arif-fazil.com` | React 19 + Vite | `npm run build` | **VPS / Caddy origin** | `sites/arif-fazil.com/` |
| `aaa.arif-fazil.com` | React cockpit + A2A API | `npm run build` | **VPS / Caddy origin** | `sites/aaa.arif-fazil.com/` |
| `arifos.arif-fazil.com` | Static HTML + MCP proxy | None | **VPS / Caddy origin** | `sites/arifos.arif-fazil.com/` |
| `forge.arif-fazil.com` | Static HTML | None | Cloudflare Pages | `sites/forge.arif-fazil.com/` |
| `geox.arif-fazil.com` | Static HTML + MCP proxy | None | VPS / Caddy | `sites/geox.arif-fazil.com/` |
| `wiki.arif-fazil.com` | Static HTML | None | VPS / Caddy | `sites/wiki.arif-fazil.com/` |

> **⚠️ Discrepancy Warning:** `domains.yml` and CI workflow comments claim Cloudflare Pages is the primary deploy for `arif-fazil.com`, `aaa`, and `arifos`. Live runtime evidence (Caddyfile, `Last-Modified` headers matching VPS file mtimes, `cf-cache-status: DYNAMIC`) proves the VPS is the active origin. Always verify runtime state before answering deployment questions.

### Dynamic Services (VPS Docker)

| Service | Port | Compose Name | Image |
|---------|------|--------------|-------|
| arifOS MCP | 8080 | `arifosmcp` | `ghcr.io/ariffazil/arifos:*` |
| GEOX | 8081 | `geox_eic` | `ghcr.io/ariffazil/geox:*` |
| WEALTH | 8082 | `wealth-organ` | `ghcr.io/ariffazil/wealth:*` |
| WELL | 8083 | `well` | `ghcr.io/ariffazil/well:*` |
| A-FORGE | 7071 | `af-bridge-prod` | `ghcr.io/ariffazil/a-forge:*` |
| apex-prime | 3002 | `apex-prime` | `apex-prime:v1.0.5` |
| graphiti-mcp | 8000 | `graphiti-mcp` | `zepai/knowledge-graph-mcp:latest` |
| aaa-a2a | 3001 | `aaa-a2a` | `aaa-a2a:phase3-reforge` |

---

## CRITICAL: SPA Route Integrity Check

For ANY domain running a React/Vite SPA, Caddy handles can **hijack React routes**.

**Before adding a Caddy `handle` block:**
1. List all React routes: `grep -o 'path="[^"]*"' src/App.tsx`
2. List all `public/` files (Vite copies these verbatim to `dist/`)
3. Build and check `dist/` for path collisions
4. Check Caddyfile for overlapping handles

**Any overlap = ARCHITECTURAL CONFLICT.** The static file server will always win over the React router.

**Example of route hijacking (DON'T DO THIS):**
```caddy
@genesis path /000/*
handle @genesis {
    root * /var/www/html/arif/000
    file_server
}
```
If React has `<Route path="/000" element={<Genesis />} />`, the React component becomes **dead code** — Caddy serves the static file before React ever sees the request.

**Dead Source Detection:**
For every site, verify `curl https://{site}/` matches the repo source. If Caddy returns text/redirect/proxy instead of the source HTML, the source is dead code.

## Workflow: Add New Subdomain

```
1. Decide: static site or dynamic service?
2. If static:
   a. Create directory in `sites/{subdomain}.arif-fazil.com/`
   b. Add Caddy route in `/root/Caddyfile` or compose labels
   c. Build (if React) and deploy
3. If dynamic:
   a. Add service to `compose/docker-compose.yml`
   b. Add Caddy reverse proxy route
   c. docker compose up -d
4. SPA ONLY: Run Route Integrity Check (React routes vs Caddy handles vs public/ files)
5. Verify: curl -s https://{subdomain}.arif-fazil.com/ | head
6. Document in this skill and [[federation-entities]]
```

---

## Caddy Route Pattern

```caddy
{subdomain}.arif-fazil.com {
    reverse_proxy localhost:{port}
    tls /etc/ssl/certs/arif-fazil.com.crt /etc/ssl/private/arif-fazil.com.key
}
```

---

## Related

- [[federation-entities]] — Service registry with ports and health
- [[skill-caddy-cloudflare]] — Caddy + Cloudflare TLS specifics
- [[skill-vps-management]] — VPS operations
- [[mcp-architecture-mapping]] — MCP surface topology

---

*DITEMPA BUKAN DIBERI — Every subdomain is a constitutional surface.*
