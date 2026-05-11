---
name: cf-pages-spa-static-json-fix
description: Fix Cloudflare Pages SPA routing so static JSON/data files are served correctly instead of falling through to index.html. Applied when arif-fazil.com/data/* returns HTML instead of JSON.
tags: [cloudflare, spa, routing, static-files, pages, fix]
category: devops
last_updated: 2026-05-05
---

# Cloudflare Pages SPA Static JSON Fix

## Problem

arif-fazil.com uses React Router (SPA) deployed on Cloudflare Pages. When fetching `/data/wealth/latest.json`, the request returns `text/html` (the SPA index.html) instead of the JSON file.

**Root cause:** Cloudflare Pages SPA mode routes ALL unknown paths to `index.html`. Even with `_redirects` or `_routes.json`, the SPA catch-all takes precedence for `/*`.

## Symptoms

```bash
# Returns HTML instead of JSON:
curl -s "https://arif-fazil.com/data/wealth/latest.json"
# → <!doctype html><html lang="en">...  (SPA index.html)

curl -si "https://arif-fazil.com/data/wealth/latest.json" | grep content-type
# → content-type: text/html; charset=utf-8
```

## What DOESN'T Work

### 1. `_redirects` with 200 status
```redirects
# This looks right but SPA routing still wins
/data/*   /data/:splat   200
```
CF Pages processes redirects AFTER the SPA fallback decides to serve index.html.

### 2. `_routes.json` exclusion patterns
```json
{
  "version": 1,
  "include": ["/*"],
  "exclude": ["/data/*"]
}
```
Does not work for SPA-based Cloudflare Pages deployments. The SPA catch-all is processed before route matching.

### 3. GitHub raw CDN
Requires `dist/` to be committed to git. In arifOS repos, `dist/` is gitignored (correct practice). Un-ignoring build artifacts is not acceptable.

## What WORKS

### Solution: Backend REST Endpoint

Add a REST endpoint to the VPS runtime server that serves the JSON file directly. The frontend fetches from the VPS endpoint, not from the static site.

**Step 1 — Add handler to Starlette/FastMCP app** (`WEALTH/internal/monolith.py`):

```python
BRIEFING_PATH = "/root/arif-sites/sites/arif-fazil.com/public/data/wealth/latest.json"

async def briefing_handler(request):
    """Serve static JSON from filesystem, bypassing CF Pages SPA routing."""
    try:
        with open(BRIEFING_PATH) as f:
            data = json.load(f)
        return _JR(data)
    except FileNotFoundError:
        return _JR({"error": "Briefing not available."}, status_code=404)
    except Exception as e:
        return _JR({"error": str(e)}, status_code=500)

app = Starlette(routes=[
    Route("/briefing", briefing_handler, methods=["GET"]),  # ← add this
    # ...existing routes...
])
```

**Step 2 — Frontend fetches from VPS endpoint:**

```typescript
const BASE = "https://mcp.arif-fazil.com";
const response = await fetch(`${BASE}/briefing`);
const data = await response.json();
```

**Why this works:** The request goes directly to the VPS (port 8082 via `mcp.arif-fazil.com`), which has direct filesystem access. No Cloudflare Pages SPA routing involved.

### Alternative: Cloudflare Pages Functions

If you don't control the backend, use a Cloudflare Pages Function at `functions/data/[path].ts`:

```typescript
export async function onRequestGet(context: {
  request: Request;
  next: () => Promise<Response>;
  env: { ASSETS: Fetcher };
}): Promise<Response> {
  if (!new URL(context.request.url).pathname.startsWith("/data/")) {
    return context.next();
  }
  const response = await context.env.ASSETS.fetch(context.request);
  if (response.status !== 404) return response;
  return context.next();
}
```

Note: This requires Cloudflare Pages Functions to be enabled on the project, which may not be configured for all arifOS deployments.

## Key Files Changed

- `WEALTH/internal/monolith.py` — added `/briefing` route + handler
- `arif-sites/sites/arif-fazil.com/src/pages/Wealth.tsx` — fetches from `https://mcp.arif-fazil.com/briefing`

## Verification

```bash
# Should return JSON:
curl https://mcp.arif-fazil.com/briefing | python3 -c "import sys,json; d=json.load(sys.stdin); print('DATE:', d['meta']['date'])"

# Should return HTML (confirming SPA still catches /data/*):
curl -sI https://arif-fazil.com/data/wealth/latest.json | grep content-type
```

## Prevention

When adding new data-fetching pages to arif-sites, always fetch from a VPS backend endpoint (e.g., `mcp.arif-fazil.com`, `arifOS:8080`, etc.) rather than relying on static files served through Cloudflare Pages SPA routing.
