# Design & Navigation Audit (Lane B–D) — arif-fazil.com

Validated 2026-08-14. `web_zen.py` has NO `audit` subcommand (only
sense/verify/orphan/ephemeral/doctor/caddy-reload-hint), so Lane B–D audits
are manual. This file is the recipe.

## 0. Which source feeds which live surface

| Live surface | Feeder source | Notes |
|---|---|---|
| `/` (home) | React SPA `src/pages/Home.tsx` → dist → `/var/www/html/arif/index.html` | nav = navCanon primaryNav; has THE PERSON bio section (no separate /about needed) |
| `/world/makcikgpt/<slug>` | static `public/makcikgpt-md/<slug>.html` → `/var/www/html/arif/makcikgpt-md/` | Primer Dark template. `src/pages/MakcikGptArticle.tsx` + `src/data/makcikgpt/*.ts` are a parallel SPA implementation, NOT live-served; essays.json holds only 23/84 pieces |
| `/world/makcikgpt/` (hub) | static `public/makcikgpt-md/index.html` | embedded `const ARTICLES=[...]` (84 entries) = fullest ordered corpus; working filter = `.scard` series cards (role=button) + `input#q` search; SOVEREIGNTY/RESOURCES/INSTITUTIONS/TECH pills are decorative spans, NOT filters |
| Caddy routing | `/etc/caddy/vhosts/arif-fazil.com.conf` | `/world/makcikgpt/*` → makcikgpt-md `try_files {path} {path}.html {path}/index.html /spa-shell.html` |

Deploy: `deploy-makcik.sh` rsyncs public/makcikgpt-md → webroot WITH `--delete`.
Gate: `make verify-pages` (non-bypassable).

## 1. Capture protocol (avoids false findings)

- Capture with a real desktop Chrome UA:
  `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36`
  Bot/HeadlessChrome UAs get the static lane; findings from it do not describe the human surface.
- `html { scroll-behavior: smooth }` breaks `scrollIntoView` screenshots (shot lands
  mid-scroll). Use `window.scrollTo({top: y, behavior:'instant'})` then screenshot.
- Before declaring UI "dead", check handler/role: decorative span ≠ broken button.
- Compare like-with-like surfaces: home (SPA) nav vs hub (static) topbar are different
  surfaces, not "duplicate navigation".
- 2026-08-14 false findings this protocol prevents: "dead filter chips", "duplicate
  nav", "missing about page".

## 2. Dead-end fix pattern (article prev/next + related)

Generator: `sites/arif-fazil.com/scripts/inject-article-nav.cjs` (idempotent, re-runnable).
- Order/series/title from the hub's ARTICLES array (essays.json is incomplete).
- Dedupe by slug AND by title (hub lists some articles under two slugs, same title —
  readers see titles, so same-title entries must collapse or related lists repeat).
- Wrap block in `<!-- NAV-PREVNEXT v1 -->` … `<!-- /NAV-PREVNEXT v1 -->`; strip prior
  block before re-injecting.
- Anchor: before the `</div>` preceding `<footer`; legacy templates (`.footer-sig`,
  no `<footer>`) fall back to before `</body>`.
- Related list excludes current + prev + next.
- Verify: curl live + grep markers; Playwright screenshot of the nav block;
  `make verify-pages`.

## 3. Live-ahead-of-source drift heal

Symptom: `diff -rq source live` shows nearly ALL files differ AND live has orphans
absent from git (2026-08-14: 88/88 articles differed; 5 orphans). Deploying source
as-is would regress live refinements and delete orphans via `--delete`.

Recipe:
1. `cp -a live /root/backups/<tag>/` (snapshot)
2. `cp -a live/. source/` (capture live as new baseline)
3. git commit the baseline (reversible, F1)
4. do feature work on source
5. targeted `rsync -av` source→live (NO `--delete`)
6. `make verify-pages` + spot-curl; git commit feature.

## 4. API surface (har-derived-api-client result, 2026-08-14)

No private JSON XHRs — only Cloudflare `cdn-cgi/rum` + challenge-platform calls.
Real data surfaces: `/feed.xml` (RSS) and `/sitemap.xml` (all routes).
Browserless client example: `/root/work/arif-fazil-client.py` (articles / slugs / page).
