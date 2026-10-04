# Caddy webroot map — which `root *` applies to which path

arif-fazil.com has **multiple Caddy handlers with different `root *` values**. The most common mistake is deploying to `/var/www/html/arif/<path>/` when Caddy is actually serving from a different root. This file is the canonical map.

## The four roots (verified 2026-08-11)

| Caddy handler block | `root *` value | What it serves | Live path for `<path>` |
|---|---|---|---|
| `@static_dirs` handle | `/var/www/html/arif` | most static pages | `/var/www/html/arif/<path>/index.html` |
| `@agent_shells` handle | `/var/www/html/arif` | hub agent shells | `/var/www/html/arif/<path>/index.html` |
| `handle /words/*` | **`/var/www/html`** | /words subtree | **`/var/www/html/words/<path>/index.html`** ← different! |
| `handle /work/*` | **`/var/www/html`** | /work subtree | **`/var/www/html/work/<path>/index.html`** ← different! |
| `handle /canon/*` | `/var/www/html` | /canon evidence surface | `/var/www/html/canon/<path>/index.html` |
| `handle /_shared/*` | `/var/www/html/_shared` (after strip_prefix) | design system CSS | `/var/www/html/_shared/...` |
| `handle /assets/*` | (no root, default file_server) | React bundle | `/var/www/html/arif/assets/...` |
| `handle /world/makcikgpt/` (bare) | `/var/www/html/arif/makcikgpt-md` | MakcikGPT landing | `/var/www/html/arif/makcikgpt-md/index.html` |
| `handle /world/makcikgpt/*` (slug) | `/var/www/html/arif/makcikgpt-md` (bot UA) OR `/var/www/html/arif` (browser SPA) | bot gets static .html, browser gets SPA shell | bot: `makcikgpt-md/<slug>.html` · browser: SPA fallback to `index.html` |

## Why `/words/*` differs

```
redir /words /words/ 308
handle /words/* {
    root * /var/www/html           ← different from @static_dirs
    try_files {path} {path}/index.html =404
    file_server
}
```

This was added 2026-08-10 as a "root fix" to align with sibling pages that live at `/var/www/html/<path>/` rather than under `/arif/`. After the change, **everything under `/words/*` is served from `/var/www/html/words/<subpath>/`**, NOT from `/var/www/html/arif/words/<subpath>/`.

## Reproduction (verified 2026-08-11)

Patched `/constitution/` page META in:
1. `/root/arif-fazil.com/sites/arif-fazil.com/public/constitution/index.html` ✅ (CANON source)
2. Copied to `/var/www/html/arif/constitution/index.html` ❌ **wrong webroot**
3. Live curl: returned OLD content because the actual route is `/constitution/` → 308 → `/words/constitution/` → served from `/var/www/html/words/constitution/index.html`
4. Fixed: `cp ... /var/www/html/words/constitution/index.html` ✅

## Probe recipe — determine the live webroot BEFORE patching

```bash
# 1. Follow redirects to the canonical URL
URL=$(curl -sIL "https://arif-fazil.com/<path>/" | grep -i '^location:' | tail -1 | awk '{print $2}' | tr -d '\r')
echo "Canonical: $URL"

# 2. Find which handler catches the canonical path
grep -nE "handle /$(echo $URL | sed 's|.*://[^/]*||;s|/.*||')" /etc/caddy/Caddyfile
# or
grep -nE "handle /${URL##*/}\*" /etc/caddy/Caddyfile

# 3. Read the root directive in that handler block
grep -A5 "handle <the matching block>" /etc/caddy/Caddyfile | grep "root \*"
```

Then write to the resolved path:

- `root * /var/www/html/arif` → `/var/www/html/arif/<canonical>/index.html`
- `root * /var/www/html` → `/var/www/html/<canonical>/index.html`
- `root * /var/www/html/_shared` (after strip_prefix) → `/var/www/html/_shared/...`

## Common traps

- **`/constitution/` vs `/words/constitution/`** — same content, different file paths. `constitution/` is the original; `words/constitution/` is the canonical redirect target that Caddy actually serves.
- **`/999/verify`** — NOT a static file; reverse-proxied to `127.0.0.1:8088`. Don't write to it.
- **`/world/vitals/`** — webroot `/var/www/html/arif` (via `@static_dirs`); legacy `/var/www/html/arif/vitals/` and `/var/www/html/arif/wealth/vitals/` are orphan mirrors, never edit them.
- **`/_shared/design-system/*.css`** — webroot `/var/www/html/_shared/`; `/var/www/html/arif/_shared/` is a legacy mirror that doesn't serve the live CSS (already documented in SKILL.md "Shared design-system assets").
- **`/assets/*.js`** — webroot defaults to `/var/www/html/arif/` (the global site root, not `/arif/`); correct path is `/var/www/html/arif/assets/<hash>.js`.

## Mental model

The site has a layered filesystem where the SAME URL maps to a DIFFERENT disk path depending on which Caddy handler matches first. The handler with the most specific path match wins; among equals, the first one declared in the Caddyfile wins. `@static_dirs` covers most paths, but `/words/*`, `/work/*`, `/canon/*`, and `/_shared/*` have their own roots. If you only check `/var/www/html/arif/<path>/`, you may be patching a file Caddy never reads.