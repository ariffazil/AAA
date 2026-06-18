# arifos.arif-fazil.com Site Audit — 2026-06-18

**Audited by:** OPENCLAW
**Time:** 2026-06-18 19:15 UTC
**Status:** Observatory FIXED, Cloudflare cache needs manual purge

---

## Executive Summary

| Component | Status | Notes |
|-----------|--------|-------|
| arifOS MCP kernel (:8088) | ✅ HEALTHY | build=live=1f4f04e, runtime_drift=FALSE |
| arifOS Observatory static server (:18800) | ✅ FIXED | Was dead. Now systemd-managed. |
| Cloudflare CDN | ⚠️ STALE CACHE | Serving old cached JSON from dead observatory |
| GEOX MCP (:18081) | ✅ HEALTHY | 33 tools, 11 categories |
| WEALTH MCP (:18082) | ✅ HEALTHY | 20 tools, ALIVE |
| WELL MCP (:18083) | ⚠️ EXPIRED | State expired 8h ago. Needs human injection. |
| A-FORGE (:7071) | ✅ HEALTHY | identity_hash verified |
| AAA (:3001) | ✅ HEALTHY | Express/Node, JSON API |
| Caddy reverse proxy | ✅ HEALTHY | Routes: arifos → 8088, observatory → 18800 |

---

## How arifos.arif-fazil.com Works

### Request Flow
```
User → Cloudflare CDN
           ↓
      arifos.arif-fazil.com (Cloudflare proxy)
           ↓
      Caddy (VPS reverse proxy)
           ↓
    ┌─────────────────────────────────────┐
    │  Match by path:                     │
    │                                     │
    │  /.well-known/*   → :8088 (MCP)    │
    │  /mcp*           → :8088 (MCP)    │
    │  /health          → :8088 (MCP)    │
    │  /tools*          → :8088 (MCP)    │
    │  /static/*        → :8088 (MCP)    │
    │  /api/organs/*    → respective org │
    │  /federation*     → :18800         │
    │  /assets/*        → :18800         │
    │  /               → :18800 (catch-all) │
    │  /* (other)       → file_server    │
    └─────────────────────────────────────┘
```

### Port Map (Internal)
| Port | Service | Type | Status |
|------|---------|------|--------|
| 8088 | arifOS MCP kernel | Python/uvicorn | ✅ LIVE |
| 18081 | GEOX MCP | Python/geox | ✅ LIVE |
| 18082 | WEALTH MCP | Python | ✅ LIVE |
| 18083 | WELL MCP | Python | ⚠️ STALE |
| 7071 | A-FORGE | Node.js | ✅ LIVE |
| 3001 | AAA | Node.js/Express | ✅ LIVE |
| 18800 | Observatory static | Python SimpleHTTP | ✅ FIXED |
| 8092 | MCP Telemetry proxy | Python | ✅ LIVE |

---

## The Observatory Static Server (Port 18800)

### What it is
A bare Python SimpleHTTP server serving `/var/www/html/arifos/` (the Observatory SPA + static files) on localhost:18800.

Caddy routes the catch-all `/` and `/federation*` and `/assets*` through to this port because the in-Caddy `try_files + file_server` was broken (root variables not propagating in subroutes).

### The Problem
The observatory script (`/var/www/arifOS-observatory-static.py`) was never systemd-managed. It was running as a one-off process that died at some point. No supervisor, no auto-restart. Dead = Caddy catch-all fell through to `reverse_proxy 127.0.0.1:8088` which returned MCP JSON.

### The Fix (DONE)
Created `/etc/systemd/system/arifos-observatory.service`:
```ini
[Unit] Description=arifOS Observatory Static File Server
[Service] ExecStart=/usr/bin/python3 /var/www/arifOS-observatory-static.py
         Restart=on-failure RestartSec=5
[Install] WantedBy=multi-user.target
```
Enabled and running. Survives restarts.

### Files Served at Root
- `index.html` — Observatory SPA (1689 lines, Trinity design system)
- `federation.html` — "test" placeholder (1 line)
- `federation-manifest.json` — Live federation health summary
- `llms.txt` — LLM-readable site summary
- `manifest.txt` — MCP tool manifest
- `_shared/` — Design system (tokens.css, webmcp/)
- `arifos-hostkey.pub` / `arifos-pubkey.pub` — SSH provisioning keys

---

## Cloudflare Cache Issue

### What Happened
When observatory died, `/` returned MCP JSON from port 8088. Cloudflare cached this JSON response. Observatory is back, but Cloudflare still serves the cached JSON.

### Evidence
```
# Direct to Caddy (correct — HTML):
$ curl --resolve arifos.arif-fazil.com:443:127.0.0.1 https://arifos.arif-fazil.com/
→ HTTP/2 200 content-type: text/html

# Via Cloudflare (stale — JSON):
$ curl https://arifos.arif-fazil.com/
→ HTTP/2 200 content-type: application/json
   {"service":"arifOS AAA MCP Server",...}
```

### How to Fix
Go to: https://dash.cloudflare.com → arif-fazil.com → Caching → Configuration → "Purge individual files"

Enter these URLs:
- `https://arifos.arif-fazil.com/`
- `https://arifos.arif-fazil.com/federation`

Or use the Cloudflare API (token needed):
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/purge_cache" \
  -H "Authorization: Bearer <CF_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"files":["https://arifos.arif-fazil.com/"]}'
```

### Cache Status
- `cf-cache-status: DYNAMIC` — Cloudflare respects origin Cache-Control
- No explicit Cache-Control on observatory responses → Cloudflare uses default TTL
- After purge, site will serve HTML immediately

---

## Federation Health (Live from /health endpoints)

| Organ | Endpoint | Status | Key Data |
|-------|----------|--------|----------|
| arifOS | :8088/health | ✅ GREEN | build=live=1f4f04e, drift=FALSE |
| GEOX | :18081 (no /health) | ✅ via daemons | uptime 64990s, vault_accessible |
| WEALTH | :18082/health | ✅ ALIVE | version 2026.06.15 |
| WELL | :18083/health | ⚠️ RED | expired 8h, sovereignty unknown |
| A-FORGE | :7071/health | ✅ GREEN | identity verified |
| AAA | :3001 (no /health) | ✅ Express | Node running |

### WELL Alert
```
freshness: EXPIRED (8.1 hours old)
owner_summary: RED — reasons: [sovereign_state_unknown, human_injection_required]
verdict: WELL_HOLD
```
**WELL needs Arif's input.** The body-state tracker has gone stale. Arif needs to do a `well_assess_homeostasis` call or similar to refresh.

---

## What Was Already Built (Internal FORGE)

The site already has significant infrastructure:

### 1. MCP Endpoint
`https://arifos.arif-fazil.com/mcp` — Full JSON-RPC MCP interface to arifOS kernel. 42 tools exposed (13 canonical + 29 operational).

### 2. Federation Probe
`https://arifos.arif-fazil.com/api/federation-probe` — Live cross-organ health check.

### 3. Organ Health Bypass Routes
`https://arifos.arif-fazil.com/api/organs/arifos/health` etc. — Cloudflare-bypassed organ health for API callers.

### 4. Static Constitution
`https://arifos.arif-fazil.com/static/*` — Public constitution docs, scar.json, theory files. F13#4: constitution must be publicly legible.

### 5. Observatory SPA
`https://arifos.arif-fazil.com/` — React-style SPA (1689 lines) with Trinity design system. Live when observatory is running.

### 6. Federation Manifest
`https://arifos.arif-fazil.com/federation-manifest.json` — Machine-readable snapshot of entire federation state.

### 7. SSH Provisioning
`/arifos-pubkey.pub` and `/arifos-hostkey.pub` — For Termux/edge device provisioning.

### 8. llms.txt
`https://arifos.arif-fazil.com/llms.txt` — LLM-friendly site summary for context injection.

---

## What Still Needs Work

### P0 — Immediate
1. **Cloudflare cache purge** — Manual action needed. Observatory is fixed but CDN has stale cache.
2. **WELL refresh** — Arif needs to trigger a homeostasis assessment.

### P1 — Soon
3. **Port 18800 monitoring** — Add to the 5-metric dashboard. Currently no heartbeat for the observatory.
4. **Cloudflare token fix** — The API tokens in vault.flat.env are returning authentication errors. Need fresh tokens or check permissions.
5. **federation.html** — It's literally `<h1>test</h1>`. Should be the actual federation view or removed.

### P2 — Nice to Have
6. **Observatory /federation endpoint** — Currently returns 404. The Caddy route exists but the file doesn't.
7. **Cache-Control on observatory** — Add explicit `Cache-Control` headers so Cloudflare doesn't cache HTML.

---

## Caddyfile Architecture (arifos.arif-fazil.com)

Key routes (line 117-279 of Caddyfile):
```
arifos.arif-fazil.com
  ├── /.well-known/*     → :8088 (MCP)
  ├── /mcp*             → :8088 (MCP, CORS enabled)
  ├── /health            → :8088
  ├── /tools*            → :8088
  ├── /static/*          → :8088 (constitution docs)
  ├── /inspector/*       → :8088
  ├── /api/organs/*/health → respective organ (bypasses CF)
  ├── /api/*             → :8088
  ├── /federation*       → :18800 (observatory)
  ├── /assets/*          → :18800 (observatory)
  ├── /                  → :18800 (observatory catch-all)
  ├── /arifos-pubkey.pub → file_server (static)
  └── /* (other)         → try_files {path} /index.html → file_server
```

---

## Git Commit History (Recent)

| Commit | Message | Date |
|--------|---------|------|
| 79b640021 | fix(docker): aggressive .dockerignore | 18 Jun |
| fe152e22c | chore(deps): batch-apply 6 dependabot PRs | 18 Jun |
| 1f4f04e | feat(telemetry): wire HarnessTelemetry | 18 Jun |
| d408176d5 | Merge PR #498 dependabot/pip/ml-stack | 17 Jun |

---

## Recommendations

1. **Purge Cloudflare cache now** (5 min, dashboard action)
2. **Investigate Cloudflare API token** — why auth is failing
3. **Add observatory to health cron** — check 18800 is listening
4. **WELL homeostasis assessment** — Arif runs `well_assess_homeostasis`
5. **Fix federation.html** — replace `<h1>test</h1>` with real content or 404
6. **Port 18800 into 5-metric dashboard** — Observatory uptime matters

---

*DITEMPA BUKAN DIBERI — The observatory is live. Purge the cache. Fix the WELL.*
