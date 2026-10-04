# Deploy-Site Assets Sync Gap — 2026-08-14

## Problem

`deploy-site.sh --apply` does NOT always sync `dist/assets/*.js` to `/var/www/html/arif/assets/`. When Vite produces a new bundle hash (e.g., `index-D2NRXIz2.js` → `index-0AuhwPzh.js`), the live `index.html` may still reference the old bundle.

**Symptom:** SPA renders stale content; server-side curl shows correct HTML but the browser loads the old JS bundle which doesn't contain the new data.

## Detection

```bash
# Compare bundle hashes
echo "=== dist bundle ==="
ls /root/arif-fazil.com/sites/arif-fazil.com/dist/assets/index-*.js
echo "=== live bundle ==="
grep -oE 'assets/index-[^"]+\.js' /var/www/html/arif/index.html
echo "=== actual files ==="
ls /var/www/html/arif/assets/index-*.js
```

If the dist bundle name differs from what live `index.html` references → **sync gap**.

## Fix (post-deploy)

```bash
rsync -av /root/arif-fazil.com/sites/arif-fazil.com/dist/assets/ /var/www/html/arif/assets/
cp /root/arif-fazil.com/sites/arif-fazil.com/dist/index.html /var/www/html/arif/index.html
```

## Why this happens

`deploy-site.sh` uses `rsync -a --delete` with overlay exclusions. The `assets/` directory is not in the overlay exclusion list, but the `index.html` (which references the bundle by hash) may come from a different source path than the assets directory. When the main `index.html` is overwritten by a sibling's version or by a Caddy-served custom page, the JS bundle reference becomes stale.

The `/var/www/html/arif/index.html` is NOT the Vite-built SPA shell — it's a custom handcrafted page with federation widgets. The Vite build output at `dist/index.html` has `<script type="module" src="/assets/index-XXX.js">` but the live page uses a different HTML structure entirely.

## Browser cache vs server cache

When user reports "not live" but server-side curl confirms content is correct:
1. `cf-cache-status: DYNAMIC` → Cloudflare not caching
2. `cache-control: no-cache, no-store, must-revalidate` → Caddy instructs no cache
3. No service worker (`/sw.js` → 404, `/service-worker.js` → 404)
4. Conclusion: **browser cache on user's device**

Resolution: user clears browser history, or appends `?v=2` cache-buster query string to URL.
