---
name: arif-sites-ops
description: "Use when deploying, editing, routing or diagnosing any arif-fazil.com page. The single canonical owner for the site — serving path, sanctioned additive deploy, human-first design gate, dead-URL trace, nav canon — with the merged pitfall ledger behind it."
version: 2.0.0
tags: [arifos, arif-fazil, deploy, caddy, vite, static-site, human-first, nav-canon, canonical-owner]
triggers:
  - "add a page to arif-fazil.com"
  - "deploy arif-fazil.com"
  - "site is 404 / dead url"
  - "verify-pages gate"
  - "nav canon"
  - "site design human-first audit"
floor_scope: [F1, F2, F4, F11]
autonomy_tier: T2
---

# arif-sites-ops — canonical owner of arif-fazil.com

**One problem, one owner, one path (LAW 8).** This skill owns operating the arif-fazil.com
surface. Three former owners are now pointer stubs that route here:
`arif-fazil-web-ops`, `arif-fazil-site-ops`, `arif-sites-content-ops`. Their content is
preserved verbatim in `references/` — nothing was deleted.

**Current rule (2026-10-13, wins over any older copy).** Later `caddy reload`,
`systemctl reload caddy`, `make deploy`, `deploy-site.sh --apply` and
`rsync -a dist/ /var/www/html/arif/` are historical scars. Live vhost: 
`/etc/caddy/vhosts/arif-fazil.com.conf`; `/etc/caddy/Caddyfile` only imports vhosts. Ship with
skill `arifos-site-patch-without-caddy-reload`: additive per-route, `rsync -av --update` of new
assets, **no `--delete`, no reload**. A full-tree rsync without `--delete` still overwrites
live-only HTML — count live HTML naming a hashed file the new dist lacks; `--delete` only when
that count is zero (it was 74 on 2026-10-13; re-count). `/propa/` 301s to `/vitals/`;
`/malaysia/` 308s to `/wealth/malaysia/` — do not reverse. Queue: `/root/work/tasks.json`.

---

## HUMAN-FIRST DOCTRINE (applies to every surface)

Arif: *"serve human first for human cognitive limit and then we do all agentic backend."*
Order: **human first · agentic backend second · both layers fail-closed.**

Three tests before any landing page or hub ships: **human at 2am** (find it in 10s on a phone) ·
**agent at scale** (crawler extracts headline + 5 facts + nav in one pass) · **sovereign at noon**
(he glances 30s and says "yes, that's it"). Any "no" = broken; patch before deploy.

| Filter | Rule |
|---|---|
| Navigation | ≤7±2 choices at once (Miller); group or paginate |
| Colour | ≤3 accent colours per page |
| First 100px | brand + nav + breadcrumb + kicker + h1 + lede — no status codes, F-codes, organ acronyms, SEAL/HOLD stamps |
| Metadata | byline, date, tags, read-time, provenance go in the FOOTER |
| Verbs | "Read the analysis", not "Analysis Page" |
| Answers | WHERE AM I / WHY CARE / WHAT NEXT within 3 seconds |
| Jargon | F-codes and organ names are internal; public surfaces are plain language |
| Footer | always carries "Ditempa bukan diberi" |
| Media | no autoplay; respect `prefers-reduced-motion` |

---

## ARCHITECTURE MAP (probe live; never trust prose)

| Layer | Path | Role |
|---|---|---|
| SPA source | `/root/arif-fazil.com/sites/arif-fazil.com/src/` | routes in `App.tsx`, pages in `src/pages/` |
| Static shells | `.../public/<route>/index.html` | content-first no-JS pages; `public/_redirects` = clean-URL rewrites |
| Build | `npm run build` = prebuild → `tsc -b` → `vite build` → `copy-static-html.js` | `dist/` is DERIVED, never hand-edit |
| Registry | `infra/runtime-overlays.json` | site defs, webroots, preserve-live overlays |
| Deploy | `scripts/deploy-site.sh <site> --dry-run \| --validate-build \| --apply` | atomic swap + rollback + JSON receipt (`--apply` = T3) |
| Live webroot | `/var/www/html/arif/` | what Caddy actually serves |
| Caddy | `/etc/caddy/vhosts/arif-fazil.com.conf` | matcher order: `@static_dirs` → `handle /words/*` · `/work/*` → `@agent_shells` → `@spa_routes` → SPA fallback. **`/words/*` and `/work/*` root at `/var/www/html` (NOT `/arif/`)**; `/999/verify|health|flow` are reverse-proxied; `/` is static-first |
| Gate | `scripts/verify-pages.sh` (`make verify-pages`) | probes every `dist/*/index.html` against live; any gap → HOLD |

Split-root trap: `/world/*` roots at `/var/www/html/arif`, `/world/politics/*` at
`/var/www/html`, `/world/makcikgpt/*` has its own handler. Read the handler's `root *` before
patching any page; mirrored copies must both be patched or stale nav resurrects.

---

## DEAD URL — trace the missing layer

A path can be registered in Caddy and still 404 when the file was never built.

1. `curl -sL -o /dev/null -w "%{http_code}" https://arif-fazil.com/<path>/`
2. `grep -n "<path>" /etc/caddy/vhosts/arif-fazil.com.conf` → matcher + `try_files`
3. `ls /var/www/html/arif/<path>/` (live) · `.../dist/<path>/` (build) · `.../public/<path>/` (source)
4. `grep -n "<path>" src/App.tsx` (SPA route)

Phantom 200: the SPA fallback answers 200 with the shell title for never-built routes — probe
`<title>`, not the status code. Fix = build the shell, add a `_redirects` 301, or drop the matcher.

## ADDING A PAGE (sanctioned path)

1. Build in proposal zone first: `forge_work/proposals/<agent-id>/<mission>/`
   (`file-authority.yaml` is FAIL-CLOSED; `src/**` = CANON, `public/**/*.html` = DERIVED).
2. Static shell → `public/<route>/index.html` + assets, then `npm run build`.
3. Vite sub-app → `base: '/<route>/'`, build, copy `dist/*` into `public/<route>/`.
4. Gate: `bash scripts/verify-pages.sh` — must pass; declare pre-existing gaps, never silently bypass.
5. `deploy-site.sh --dry-run`, then additive rsync of the one route, no `--delete`, verify live,
   receipt in `receipts/<agent-id>/`.
6. Keep `index.html.bak-*` before replacing a live page.

---

## USER DOCTRINE (Arif, verbatim intent)

**"Don't simply replace. I want upgraded."** An upgrade preserves existing content; never
wholesale-replace a page. **Alignment before deploy** — "check dulu segala benda aligned".
Deploy signals: *"X deploy lagi"* = HOLD · *"deploy ja la bila ready"* = green light.
Top-bar brand = **ARIF FAZIL** exactly, no suffix.

**His words are the only acceptable words.** Never paraphrase his vocabulary ("BANGANG and
stupid is different meaning"); when he flags a term, propagate to `.ts` title → `<h1>` →
`<title>` → meta description → essays.json → index cards → llms.txt in one pass.
**Zero tolerance for invented content** — no fabricated quotes, references or added analysis
attributed to him; pages were rejected twice for exactly this.

Header = brand + breadcrumb + kicker + h1 + lede + hr, nothing else; byline/date/tags/read-time
pills go in the footer. Pairs-with is series-derived (each links to the others in its series,
never itself); a wrong pair breaks the canon graph.

---

## TOP PITFALLS

1. **Archive archaeology first.** Before mutating a landing page compare live vs
   `forge_work/deployments/.../previous/`, `/root/_archive`, git history — design drift mostly
   comes from writing without reading the archive.
2. **Full-tree rsync overwrites live-only HTML.** Additive per-route, `--delete` only after the
   orphan count is zero.
3. **Phantom 200** from the SPA fallback on never-built routes — probe `<title>`.
4. **Zombie links**: a deleted child `index.html` makes `try_files` serve the hub at the child
   URL; restore from `.bak` or drop the link.
5. **Split-root trap** — `/world/*` and `/world/politics/*` have different Caddy roots; patch
   the copy that serves.
6. **Surfaces.json / verify-pages trust gap** — the gate is content-thin; drift hides behind a PASS.
7. **CSP iframe trap** and **orphaned CSS classes** (markup has classes, stylesheet is gone).
8. **Partial rsync** = built-but-not-served bundle; check `dist` → webroot, not just build green.
9. **Cloudflare caches 404s** — purge before declaring a deploy dead.
10. **Parallel subagents collide** on `public/words/`; one writer per surface.

Merged ledger, all four skills, verbatim with worked cases: `references/pitfalls.md`.

---

## REFERENCES

`references/pitfalls.md` (merged, 92KB) · `references/nav-canon-v7.md` ·
`references/transmission-engine-viz.md` (29KB) · `references/build-deploy.md` (from
`arif-fazil-site-ops`) · `references/web-surfaces.md` (from `arif-fazil-web-ops`: archive
archaeology, `/words/` sections, makcikgpt-md mirror, atlas, live-data wiring) ·
`references/content-ops.md` (from `arif-sites-content-ops`: essays, route pages, design gates) ·
plus 14 pre-existing dated references (caddy webroot map, design canon, makcikgpt rec…).

Related: `arifos-site-patch-without-caddy-reload` (the ship path), `makcikgpt-article-forging`
(article content), `arif-fazil-site-deploy`, `forge-komda-color-law`.

## CHANGELOG

| Version | Date | Change |
|---|---|---|
| 2.0.0 | 2026-10-23 | Becomes the single canonical owner of arif-fazil.com (F13 consolidation). Merged pitfall ledger from four skills (deduped), nav canon v7, transmission-engine viz, build/deploy and content-ops history into `references/`. Static 28KB "Support files" dump dropped. `arif-fazil-web-ops`, `arif-fazil-site-ops`, `arif-sites-content-ops` converted to pointer stubs with `alternative_to: arif-sites-ops`. |
