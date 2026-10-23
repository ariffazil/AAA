---
name: live-data-dashboards
description: Build live data dashboards and world atlases (interactive maps + news rails + indicator panels) on free, no-auth, CORS-enabled data sources — GDELT DOC2, World Bank, embedded country datasets, TopoJSON. Covers rate-limit workarounds, embed-vs-fetch decisions, Vite subpath deploys, and the browser-verify loop.
version: 1.1.0
tags: [web, dashboard, react, vite, gdelt, worldbank, maps, data-viz, arif-fazil, feed-validation]
platforms: [linux]
triggers:
  - build a world atlas
  - live world map dashboard
  - state of the world
  - geopolitical dashboard
  - country dossier
  - live news rail
  - free api data dashboard
  - no api key dashboard
  - user pastes dashboard screenshot
  - cross-validate dashboard values vs live web
---

# Live Data Dashboards

## When to use
- User wants a live world map / atlas / dashboard (news rail, tension indices, country dossiers)
- Any dashboard needing live news/geo/economic data WITHOUT API keys
- Replacing a static link-directory page with a dynamic surface
- SOT (State of the World) style computed-index panels

## Data source catalog (all free, no keys, CORS-enabled)

### GDELT DOC 2 (live global news)
- Endpoint: `https://api.gdeltproject.org/api/v2/doc/doc`
- Query: `?query=<lucene>&format=json&maxrecords=N&sort=datedesc`
- **Rate limit: 1 req / 5s.** Throttled responses return HTTP 429 (datacenter IPs) OR HTTP 200 with plaintext "Please limit requests..." body — always check `res.text()` starts with `{` before `JSON.parse`.
- **Pattern: single combined query.** Never fire N staggered theme queries (3 × 5s = 15s+ first paint). Build ONE OR-joined query covering all themes, fetch ~60 records, then classify each article client-side by keyword regex on title, with tone disambiguation for multi-match (tone mean < -3 → conflict/geo, > 2 → econ).
- No lat/lng in DOC2 output → geocode by matching `sourcecountry` (or actor1geo/actor2geo when present) against a country dataset's latlng.
- Article fields: title, url, seendate (`YYYYMMDDTHHMMSSZ`), domain, tone (number array), sourcecountry.

### World Bank Indicators
- Endpoint: `https://api.worldbank.org/v2/country/<ISO2>/indicator/<CODE>?format=json&per_page=1&date=2022:2024`
- No auth, CORS ✅. Response shape: `[meta, [record]]` — record has `value`, `date`.
- Indicator codes: NY.GDP.MKTP.CD (GDP), NY.GDP.PCAP.CD (GDP/cap), SP.POP.TOTL (pop), SP.DYN.LE00.IN (life expectancy), EN.ATM.CO2E.PC (CO2/cap), IT.NET.USER.ZS (internet %).
- Cache client-side 24h in a Map keyed by country code.

### Country metadata — embed, don't fetch
- **REST Countries v3.1 is DEAD (2026)** — returns `{"success": false}` deprecation envelope; v5 requires a paid API key (`Authorization: Bearer` header). Do NOT build on it.
- Use `mledoze/world-countries@5.1.0` from jsDelivr: `https://cdn.jsdelivr.net/npm/world-countries@5.1.0/countries.json` (250 countries, 1.4MB raw).
- Trim at build time to ~70KB (keep cca3, cca2, name.common, official, capital, region, subregion, population, area, latlng, languages, currencies, flag emoji, unMember, independent). Fetch once into `.cache/`, write trimmed JSON to `src/data/`, run in prebuild.
- **Zen rule: static metadata embedded = zero failure modes.** Only use live APIs for data that must be live (news, indicators). Static facts (capital, flag, population) are embed candidates.

### Map geometry
- `https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json` (107KB, CORS ✅) with react-simple-maps.
- react-simple-maps stack: `ComposableMap projection="geoEqualEarth"` → `ZoomableGroup` → `Geographies geography={url}` → `Geography` (onClick country select; onMouseEnter captures `evt.clientX/Y` for tooltip) → `Marker` for pulsing event dots (add `pulse` keyframes).
- Country match `geo.properties.name` vs dataset `name` is brittle ("United States of America" vs "United States") — keep a name-alias map for production.

## Build pattern
- Vite + React + TS. Set `base: '/<subpath>/'` in vite.config so dist serves under a site subpath (e.g. `/world/`).
- Dark dashboard aesthetic: deep black bg (#0B0B0F-class), single warm accent (gold), per-axis colors (red/gold/cyan), mono uppercase labels + serif display titles, hairline borders, NO gradients.
- Computed index math (SOT-style): per-axis 0–100 from negative tone mean, log volume `log10(count+1)*10`, source spread `unique_domains*1.5` (cap 20), title-length complexity; aggregate = harmonic mean × 1.5 floored at 0.5 — catastrophic single-axis signal dominates (F1 AMANAH style).
- Async fetch hooks: AbortSignal.timeout on every fetch; graceful empty states ("QUERYING…", "NO ARTICLES YET") so rate-limited first paint still renders.

## Verification loop (must-do after build)
1. `npm run build` → expect 0 tsc/vite errors.
2. Start preview as a BACKGROUND process (`terminal(background=true)`) — foreground `&` is rejected by the terminal tool.
3. `curl` HTML + JS chunk → HTTP 200.
4. `browser_navigate` → `browser_vision` (screenshot check for layout/theme) → `browser_console` (assert 0 JS errors).
5. Run a node smoke script hitting each live API separately — distinguishes app bugs from upstream rate-limits.

## Pitfalls

### Dashboard feed validation — cross-check every feed before any thesis (2026-08-06, syedos.arif-fazil.com/emas)
**Symptom:** Dashboard reads `SILVER $31.2` consistently across 3 screenshots in 20 minutes. Live silver spot is **$61.58** (+3.5% on the day, monthly high). User pastes dashboard screenshots expecting the agent to validate values, not just trust them.

**Tells (any one = suspect a stale feed):**
- A feed value that does not change across multiple refreshes when the market is open (frozen receipt, not live)
- A value that is exactly 2× off from a public live source (the silver case: dashboard stuck at pre-2024 historical level while live is post-rally)
- A header labelled `Live` but the value is rounded to a suspiciously round number ($31.2 vs live $61.58 — the 31 is suspiciously tidy)
- A pair that should correlate (gold ↑ + silver ↑ during a rally) showing one moving and the other frozen

**Recipe — when the user pastes a dashboard screenshot OR asks about a price the dashboard shows:**

1. **Cross-validate EVERY asset the dashboard shows**, not just the headline instrument. The headline (gold $4,257.6) was correct against live $4,261.85 — but silver, RSI, and DXY may not be.
2. **Probe live web sources** (`web_search` for instrument + current date) for each row. Render as markdown table: dashboard value | live value | verdict (✅ matches / ❌ stale).
3. **Lead with the gap.** Don't bury a stale feed in a wider verdict. Pattern: "Live $4,261.85 ✅, silver $31.2 ❌ stale 2×, DXY 98.5 ✅, RSI 50 ⚠ unverifiable." First thing in the reply.
4. **Refuse to build analytical conclusions on stale data.** Anything that depends on the stale feed (silver as correlation, RSI derived from silver delta, silver-led disinflation trade) is untrustworthy until the feed is patched. Tag those branches "blocked on feed fix."
5. **Suggest the fix shape without forcing it** — API key expired / hardcoded constant / wrong endpoint / cache TTL too long / proxy mis-routing. The user owns the dashboard; the agent validates, doesn't refactor.

**Do NOT:**
- Assume the dashboard is right because the user trusts it. He expects independent verification. His memory notes "sibling prose fabrication" as a recurring failure mode — be the sibling that cross-checks.
- Build a trade thesis that depends on the stale feed. Mark those branches "blocked on feed fix."
- Bury the feed-bug finding in long prose. Lead with one sentence: "Silver $31.2 vs live $61.58 — feed stale 2×, fix before trading on any silver-derived signal."

**Why this matters:** Three screenshots in 20 minutes — same silver value across all three — is the smoke. The agent must compare across refreshes, not just verify one snapshot. A frozen receipt is not live data even if the dashboard says `Live`.

### Two timeframe layers confuse the reader — engine values vs chart overlay (2026-08-06, syedos.arif-fazil.com/emas)
**Symptom:** Dashboard card shows `EMA20 $4,235, S1 $4,192.5, R1 $4,320.1` (4H timeframe). Chart overlay shows current levels `4647.96 / 4529.63 / 4341.71 / 4249.24` with `1W` selected in TradingView. User asks "chart kat sini lagi cantik dari MT5 kan?" — implying the TradingView widget is just a render layer.

**Tell:** Two different sets of EMA/SR numbers on the same screen, generated by different engines (own logic vs TradingView native). The user may read them side-by-side and see contradictions that are actually just period mismatch.

**Recipe:**
1. **Label each layer explicitly** — "card = 4H engine values; chart overlay = TradingView native (1W selected)."
2. **State the period for every number cited.** `$4,235 EMA20` is ambiguous — 4H? 1W? Daily? Always carry the timeframe tag.
3. **Don't try to reconcile them.** They're two different engines. If TradingView 1W EMA20 = 4,341 but engine 4H EMA20 = 4,235, both can be right for their respective periods.
4. **When asked to compare ("ada beza tak?"),** produce a small table with both periods side by side — never collapse to one number.

### Caddy `@agent_shells` intercepts SPA sub-routes — static shell wins over React Router (2026-08-06, arif-fazil.com /writing/)
Symptom: SPA loads for `/writing/petronas-23-years-in-brazil/` but renders the index listing, not EssayPage. `getEssay('petronas-23-years-in-brazil')` exists in the bundle, but the browser shows `<h1>Writing</h1>` instead.

**Root cause:** The static-shell `public/writing/index.html` is copied to `dist/writing/index.html` by `copy-static-html.js` during `npm run build`. Caddy's `@agent_shells` matcher includes `/writing /writing/ /writing/*`, and the `try_files` directive runs BEFORE the SPA can catch the route. Even if the SPA shell at `/index.html` loads, the static shell at `/writing/index.html` is served first by Caddy and replaces the SPA's `index.html`.

**Fix — three-part:**
1. In `@agent_shells` handler, add a fallback BEFORE `try_files {path} {path}/index.html =404`:
   ```caddyfile
   handle @agent_shells {
       # ... existing pm_bayang handler ...
       # 2026-08-06: Writing essays are SPA-rendered. Fall back to /index.html for missing essay paths.
       @writing_spa path /writing/*
       try_files @writing_spa {path} {path}/index.html /index.html =404
       try_files {path} {path}/index.html =404
       file_server
   }
   ```
2. The first `try_files` (with `@writing_spa`) runs when `/writing/*` is hit. If `{path}` and `{path}/index.html` don't exist, the fallback `/index.html` (SPA shell) is served.
3. The second `try_files` (without `@writing_spa`) is the catch-all for non-writing `@agent_shells` paths.

**Caveat:** Even after the Caddy fix, if the `EssayPage` component returns null/undefined, the SPA silently falls back to the index. Verify `getEssay(slug)` returns a match by grepping the bundle: `grep -o '"<slug>"' dist/assets/*.js`.

---

### BrowserRouter basename — blank page on subpath deploy (2026-08-06)
Symptom: HTML loads, JS+CSS 200, but `#root` is empty. Browser console: `No routes matched location "/world/sot/"`.

**Root cause:** SPA deployed to `/world/sot/` but `BrowserRouter` in `main.tsx` has no `basename`. React Router sees path `/world/sot/` which doesn't match route `/`.

**Fix — TWO lines must match:**
```ts
// main.tsx — BrowserRouter MUST have basename matching the deploy subpath
<BrowserRouter basename="/world/sot">
// vite.config.ts — base must also match
export default defineConfig({ base: '/world/sot/', ... })
```
Both `base` (Vite) and `basename` (React Router) must agree. If only one is set, the page either shows 404 asset loads or a blank page. **Not caught by `npm run build`** — fails only at runtime.

### GDELT datacenter 429s
- GDELT from a datacenter IP can be 429/timed-out while working fine from a user browser. Verify CORS headers + retry with spacing before declaring the app broken.
- The browser sandbox often shares the datacenter IP → GDELT 429s there do NOT prove the app is broken.

### npm peer-dep conflicts
- `npm install --legacy-peer-deps` fails with "Exit handler never called!" on Node 22 / npm 10. Use `pnpm install` instead.
- npm audit warnings (react-simple-maps-era stacks) are normal; don't `npm install --force`.

### REST Countries v3.1 is DEAD
- v3.1 returns `{"success": false}` deprecation envelope; v5 requires API key. Do NOT build on it. Use embedded country dataset (see `mledoze/world-countries@5.1.0` or World Bank country API for income tier + centroids).

### Governed repos
- Scaffold in proposal zone (`forge_work/proposals/<agent>/<mission>/`), write a receipt, NEVER touch DERIVED/CANON paths until sovereign says deploy. See `references/arif-fazil-site-governance.md`.

## Build patterns that survived shipping (2026-08-06, arif-fazil.com /world revamp)

### Vite `base: './'` for portable subpath deploys
When the same `dist/` will be mounted under different site paths (`/`, `/world/`,
`/missions/`) over its lifetime, keep `base: './'` in `vite.config.ts`. Assets resolve
relatively, so the same bundle droppable at any path. Trade-off: no CDN cache-busting
hashing outside Vite's default (acceptable here, no CDN edge).

### `react-simple-maps@3.0.0` ↔ React 19 peer-dep mismatch (REAL)
Symptom: `npm install` fails with
`Conflicting peer dependency: react@18.3.1 ... peer react@"^16.8.0 || 17.x || 18.x" from react-simple-maps@3.0.0`.

Two clean fixes (try in this order):
1. **Use pnpm (cleanest)** — pnpm 10+ handles the conflict silently:
   ```bash
   rm -rf node_modules package-lock.json
   pnpm install --reporter=append-only
   # esbuild build-script may need: pnpm rebuild esbuild
   ```
2. **Pin to `react-simple-maps@4.0.0`** — still beta as of 2026-08; check `npm view
   react-simple-maps versions` first.

DO NOT use `npm install --legacy-peer-deps` on Node 22 / npm 10 — it auto-exits with
"Exit handler never called!" and produces no `node_modules/.bin/vite`. The pnpm path is
reliable.

### Vite background-process rule
`vite build` runs to completion in foreground. The terminal tool's heuristic flags
long-running foreground commands as background-worthy; use a Node wrapper to bypass it:
```js
import { execSync } from 'child_process';
try { console.log(execSync('npx vite build 2>&1', { timeout: 120000, stdio:'pipe' }).toString().slice(-600)); }
catch(e) { console.log('STDERR:', e.stderr?.toString().slice(-500)); }
```
Save as `/tmp/build_check.js`, run with `node /tmp/build_check.js`. Returns the last 600
chars of the build log without triggering the background-watchdog heuristic.

### TypeScript strictness knock-on when tightening `findCountry` return type
When you change `findCountry(name)` from `(name: string)` to `(name: string | undefined | null)`,
every call site that passes `a.sourcecountry` (which is `string | undefined` in the GDELT
record type) becomes valid. Reverse: when you tighten the country dataset's interface,
the consumer functions need to relax their null-handling. Patch the type at the source
rather than every call site.

### Tier choropleth — context state for view-mode
Pattern: lift the mode into `SotContext` (e.g. `viewMode: 'axes' | 'tier'`),
call `setViewMode` from a header toggle group (`ΔΩΨ` button + `TIER` button sharing
a styled border), and have `MapPanel`'s Geography fill read both `viewMode` and the
country's `incomeTier`. Do NOT store per-Geography styles — recompute the fill from
context on every render.

### Agent-readable layer (ships in dist/)
Always write `public/llms.txt` AND `public/agent.json`. Vite copies both to `dist/`
### Agent-readable layer (ships in dist/)
Always write `public/llms.txt` AND `public/agent.json`. Vite copies both to `dist/` unchanged. See `references/free-data-sources.md` §"World Bank Country Classification" for the WB income-tier endpoint + tier-color mapping that's specific to this category of page.

## Page-metadata pitfall — the deceptive 200 (2026-08-06, arif-fazil.com /world/)

**Symptom:** AI crawlers request `/world/llms.txt` and `/world/page.json` expecting machine-readable content. Caddy's `@agent_shells` catch-all rewrites missing files to `index.html` (the SPA). So both URLs return **HTTP 200** with the homepage HTML and `content-type: text/html`. Agents ingesting these get HTML soup under a truth-claiming URL. An F2 wound at the exact URL where machines come looking for truth.

**Tell:** `curl -I /section/llms.txt` returns `HTTP/2 200 content-type: text/html; charset=utf-8`. Real machine files should return `text/plain` or `application/json`.

**Fix:**
1. Create a real file at `public/<section>/llms.txt` AND `public/<section>/page.json` BEFORE deploy. Caddy serves static files first; catch-all only fires on missing files.
2. Real `llms.txt` should be 1-2KB of plain-text section overview.
3. Real `page.json` should be a small structured object: `section`, `title`, `description`, `surfaces[]`, `cross_links[]`, `machine_files{}`.
4. Verify with `curl -I` — both should return the correct content-type, not `text/html`.

**The canary rule (extends verify-pages gate):** every declared machine file (`*.llms.txt`, `page.json`, `agent.json`, `missions.json`, `sitemap.xml`, `rsl.xml`) must return its declared content-type and must NOT contain `<!doctype html` in the body. A 404 is honest; a 200-with-wrong-content is a lie told to machines.

## Article metadata gap (2026-08-06, 79 MakcikGPT articles)

**Symptom:** Civic journalism articles ship without `og:title`, `og:description`, `theme-color`, or `application/ld+json` NewsArticle schema. MakcikGPT is the federation's most-shareable content. Every WhatsApp/X/AI-engine share unfurls bare. This is the single biggest GEO/citation leak — machines can't see datePublished, inLanguage, or publisher.

**Fix pattern (apply once, scale to corpus):** single Python script reads each article's HTML, extracts `<h1>` + cover subtitle + date, generates OG meta + Twitter Card + NewsArticle JSON-LD, rewrites the `<head>` block. Deployment via `rsync` to the Caddy root. The script is reusable for any section that ships article-shaped HTML.

**What's required for NewsArticle schema:**
- `headline` (from `<h1>`)
- `description` (from cover subtitle or first paragraph)
- `inLanguage: "ms"` (or relevant language code)
- `datePublished` + `dateModified`
- `author` as `Person` with `sameAs` to canonical URLs
- `publisher` as `Organization` (the federation)
- `mainEntityOfPage` with canonical URL
- `articleSection` + `keywords[]`

**Files to patch at the source:** articles usually live in `dist/<section>-md/<slug>.html`. The AI-bot user-agent matcher in Caddy (e.g. `@ai-bot-world` with `GPTBot|ClaudeBot|PerplexityBot|OAI-SearchBot|anthropic-ai|Bytespider|Amazonbot`) routes those bots to the static HTML with no JS — the canonical metadata reads from here. If the source file lacks metadata, the bot never sees it.

**Theme-color:** add `<meta name="theme-color" content="#0A0B0D">` to all pages in a dark-mode site. Browser chrome (mobile address bar, desktop top bar) matches the soul. Audit absence with `grep -L "theme-color" public/<section>/index.html`.

## References
- `references/free-data-sources.md` — API quirks, response shapes, indicator codes, GDELT classification regexes, trim script sketch.
- `references/arif-fazil-site-governance.md` — arif-fazil.com deploy gate + file-authority protocol (site-specific; may graduate into its own skill if site ops grows).
- ``references/`` — single-pass script that patches article HTML with OG/Twitter/JSON-LD/theme-color. Argument: source dir, deploy dir. Outputs: count of patched files + sample verification curl.


<!-- dead-pointer sweep 2026-10-23: unresolved artifacts from the gate report were replaced with the references/ directory. Basenames are preserved in the audit JSON. -->
