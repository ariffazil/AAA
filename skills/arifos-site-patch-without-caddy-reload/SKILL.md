---
name: arifos-site-patch-without-caddy-reload
description: Patch live arif-fazil surface without caddy reload.
---

# arifOS Site Patch — Caddy-Safe Procedure

The arif-fazil.com site has **three live surface types** and each mutates differently. Mis-identifying the surface = wrong mutation = webroot drift.

## Surface identification (always probe first)

Run a 2-minute probe before any mutation. Wrong surface = wrong mutation.

| Surface | Probe signature | Mutation path |
|---|---|---|
| **React SPA route** (routes that still fall through `@spa_routes` to the arif shell) | `curl -sI` returns 200 and the body is the SPA shell | Edit the matching `.tsx`, `npm run build`, then additive rsync of that shell and the new asset. No `--delete`. |
| **Commodity boards `/oil/` `/gas/` `/gold/` (measured 2026-10-13)** | Origin oil and gas bytes equalled `/var/www/html/arif/{oil,gas}/index.html`. Caddy file roots are `/var/www/html/{oil,gas,gold}`. | Static HTML. Do not treat them as `CommodityPage.tsx`. Do not whole-file-copy. Do not reload Caddy to reconcile the two roots. Re-probe before editing either copy. |
| **Single-file static HTML** (syedos/emas/, legacy `.bak-reseal`) | Single 27-50KB file at `/var/www/html/<path>/index.html` with inline CSS+JS | Source tree at `/root/WEALTH/site/src/<surface>/` → `python3 build.py` → atomic write to webroot |
| **Direct organ backend** (`/wealth/{slug}/api/*`) | Caddy reverse_proxy to `localhost:3456-3458` | Edit Python at `/root/WEALTH/wealth_mcp/tools/<endpoint>.py`. Restart requires Arif F13 approval (T3 HOLD) |

**Probe commands** (always run before edit):
- `curl -sI https://<host>/<path>/` → confirm 200, content-type, last-modified
- `curl -s https://<host>/<path>/ | head -c 500` → SPA shell (150KB+) vs static content
- `ls -la /var/www/html/<path>/` → dist or single-file structure
- `grep -E '@spa_routes|@wealth_<slug>_api|handle /<path>/' /etc/caddy/vhosts/<host>.conf` → confirm Caddy routing

## Two non-negotiable rules

**Rule 1 — NEVER run `make deploy`, `npm run deploy`, `caddy reload`, or restart Caddy.** Per `/root/arif-fazil.com/AGENTS.md` these are T3 HOLD boundaries. Caddy reload changes the route layer and can strand static files at pre-deploy versions.

**Rule 2 — Probe live, then trust nothing.** Local files and live URL can disagree. Caddy serves from `/var/www/html/arif/`, build outputs go to `/root/arif-fazil.com/sites/arif-fazil.com/dist/`. Always confirm by curl after every mutation.

## React SPA patch procedure

1. **Backup**: `cp <source> <source>.bak-pre-<YYYYMMDD>` — one per session.
2. **Edit** the React/TSX file. Preserve imports, types, component structure. Add new sections AFTER existing ones. Do NOT remove unused state declarations — bundler may catch what lint misses.
3. **Build**: `cd /root/arif-fazil.com/sites/arif-fazil.com && npm run build 2>&1 | tail -40`. Pre/post scripts run automatically — expect 30-60s. Exit 0 = success. Lint = non-fatal; type errors = fatal.
4. **Sync** (bounded write, no `--delete` on root):
   ```
   rsync -av --update <dist>/index.html /var/www/html/arif/index.html
   rsync -av --update <dist>/assets/ /var/www/html/arif/assets/
   ```
   Do not add `--delete` while any live HTML file still names a hashed file that the new `dist/assets/` does not contain. Count those HTML files first. `--delete` is safe only after that count is zero. A hashed file a page still names is not a leak.
5. **Probe**: `curl -sI` confirm `last-modified` recent. Then `curl -s https://arif-fazil.com/assets/<Page>-*.js | grep -c '<marker>'` to confirm chunk contains your additions.
6. **Receipt**: `/root/AAA/VAULT999/receipts/<surface>-deploy-<YYYYMMDD>.json` with sha256 of source + deployed + live state at probe time. Skip this = no audit trail.

## Single-file static HTML rebuild

1. **Source tree pattern** (per `/root/WEALTH/site/src/`):
   ```
   src/<surface>/
   ├── template.html       # single-file with {{PLACEHOLDER}}s
   ├── <asset>.json        # config (data endpoints, stance vocab, calibration gate)
   ├── build.py            # reads template + json, emits to webroot
   └── .backup-*.html      # pre-rebuild backup
   ```
2. **Atomic write**: write to `<out>.tmp` then `os.rename()` — prevents partial-write corruption.
3. **Cross-origin API**: when vhost has no `/api/*` route (e.g. `syedos.arif-fazil.com`), use absolute URL `https://<main-domain>/<organ>/api/*`. CSP must allowlist the main domain on `connect-src`. Verify upstream serves `access-control-allow-origin: *`.

## Deployment gate checklist

Before claiming deploy done:
- [ ] `curl -sI` returns 200, `last-modified` <= 60s old
- [ ] `curl -s` content contains your key markers
- [ ] All JSON endpoints the page calls return 200 (probe each)
- [ ] No new Caddy reload needed
- [ ] Receipt written with sha256

## Common pitfalls

- **`*.bak-reseal` filename is intentional** — it means "previous version, before reseal" and is BLOCKED by Caddy `@bak_files` regex from public serving. Do NOT delete these — they are the audit trail of the previous version.
- **Caddy route order matters**: `@wealth_gold_api` (path `/wealth/gold/api/*`) must come BEFORE generic `/wealth/*` handler, otherwise the generic handler captures it and returns 404. Read the vhost conf, don't assume.
- **Cloudflare cache**: live URL may return `cf-cache-status: HIT`. `last-modified` is the truth. New chunk filenames don't get cache hits; old ones do.
- **Tirith approval gate**: `python3 -c "..."` for inline scripts gets blocked as HIGH-risk for nested-encoded bodies. Write logic to a `.py` file and run the file.
- **Vite content-hashed chunks**: `CommodityPage-BcuuLmdL.js` — the suffix changes every build. Don't hardcode the suffix in skill rules or receipts. Grep for the marker inside the chunk, not the filename.
- **Do not `--delete` assets while old shells still name them.** On 2026-10-13, 74 HTML files under `/var/www/html/arif` still named the 12 Oct bundle, and those asset files were still on disk. A site-audit preview that says the files will be deleted is not an order. Re-count before acting. Do not trust the number 74 as a later fact.

## Reciprocal: what an audit must catch

When a second agent probes your deploy, they will check: (a) `curl -sI` last-modified freshness, (b) content markers in the served HTML/JS, (c) JSON endpoints return correct schemas. If any of these are off, the audit returns `UNRESOLVED` regardless of how clean your build was. Treat the audit as a separate actor with its own state — don't claim success on your own probe alone.