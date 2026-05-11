---
name: arifos-deployment-surface-diagnosis
description: Diagnose and fix arifOS web surface outages — dual-layer Caddy/VPS vs Cloudflare Pages architecture. Activates when sites go down after git push or when deploying arif-sites.
tags: [arifOS, deployment, cloudflare, caddy, web-surfaces]
version: 2026.05.02
---

# arifOS Deployment Surface Diagnosis

## Context
When diagnosing or deploying arifOS web surfaces (arif-fazil.com, apex.arif-fazil.com, aaa.arif-fazil.com), the terminal backend is LOCAL (I run ON the VPS). This means direct filesystem access to the web root — no SSH needed.

## CRITICAL DISCOVERY (2026-05-02)

**The terminal backend is `local` — I run ON the VPS.** File operations (`rsync`, `cp`, `ls /var/www/`) happen DIRECTLY, not over SSH.

This changes everything:
- `ls /var/www/html/arif/dist/` = live site files
- `rsync -av --delete /root/arif-sites/sites/arif-fazil.com/dist/ /var/www/html/arif/dist/` = DEPLOY
- No SSH, no SCP, no remote execution needed

## Canonical Serving Architecture

### Layer 1 — Caddy/VPS (PRIMARY live serving)
- Caddy (Docker) serves from `/var/www/html/{site}/`
- arif-fazil.com lives at `/var/www/html/arif/dist/`
- aaa.arif-fazil.com lives at `/var/www/html/aaa/`
- Check with: `ls -la /var/www/html/`
- Verify: `curl -sI --max-time 5 https://arif-fazil.com` → `last-modified` header shows file age

### Layer 2 — Cloudflare (CDN proxy only, NOT Pages)
- Cloudflare proxies to VPS Caddy — `server: cloudflare` in response headers
- `cf-cache-status: DYNAMIC` = CF is NOT caching, VPS is live
- `cf-ray` present = CF is proxying

**Important:** Cloudflare Pages is NOT the serving layer. `ariffazil.pages.dev` has NEVER worked (DNS returns nothing). The GitHub Actions "Build — Trinity Sites" workflow has been failing since ~2026-04-14 (jobs complete in 2 seconds — pre-checkout failure, not a build issue). Do NOT trust CF Pages for auto-deploy.

## Source vs Build vs Live paths

```
GitHub repo:    github.com/ariffazil/arif-sites
Source build:   /root/arif-sites/sites/arif-fazil.com/
Built output:   /root/arif-sites/sites/arif-fazil.com/dist/
LIVE site:      /var/www/html/arif/dist/         ← Caddy serves this
```

The `dist/` subdirectory is the built static output (not the raw source).

## Deploy Workflow (Pattern A — ACTIVE)

Since GitHub Actions is broken AND I run locally on VPS:

### Step 1 — Build locally
```bash
cd /root/arif-sites/sites/arif-fazil.com
npm ci && CI=false npm run build
```

### Step 2 — Sync to live site
```bash
rsync -av --delete /root/arif-sites/sites/arif-fazil.com/dist/ /var/www/html/arif/dist/
```

### Step 3 — Verify
```bash
curl -sI https://arif-fazil.com | grep last-modified
# Should show today's timestamp
```

## Diagnostic Checklist

### Step 1 — Check live serving layer (ALWAYS do this first)
```bash
curl -sI https://arif-fazil.com
# Look for: server: cloudflare, last-modified, cf-ray
```

### Step 2 — Check what files are on the live site
```bash
ls -la /var/www/html/arif/dist/
# Compare timestamp to expected build date
```

### Step 3 — Check what the local build has
```bash
ls -la /root/arif-sites/sites/arif-fazil.com/dist/
```

### Step 4 — Identify the gap
- `last-modified` on live site < `ls -la` timestamp of local build → files are stale → sync with rsync

### Step 5 — GitHub Actions (if needed to fix auto-deploy)
```bash
# Check workflow status
curl -sL "https://api.github.com/repos/ariffazil/arif-sites/actions/runs?per_page=3" | python3 -c "..."

# Workflow has been failing since ~2026-04-14
# Jobs complete in 2 seconds = pre-checkout failure (not a build issue)
# Usually: missing dependency, bad matrix config, or repo state issue
```

## If Site Goes Down After Git Push
1. `curl -sI https://arif-fazil.com` — if 404 and `cf-cache-status: DYNAMIC` = VPS is serving 404
2. `ls -la /var/www/html/arif/dist/` — check if dist/ exists and has content
3. If dist/ is empty or missing: `rsync -av --delete /root/arif-sites/sites/arif-fazil.com/dist/ /var/www/html/arif/dist/`
4. Verify: `curl -sI https://arif-fazil.com | grep last-modified`
