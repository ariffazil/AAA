---
name: arif-fazil-web-ops
description: Operate and fix Arif's public web surfaces — arif-fazil.com market pages (/gold /oil /gas /klci /usdmyr), syedos.arif-fazil.com/emas dashboard ("Abang Sado"), and other Caddy-served static sites. Multi-copy disk layout, 308 redirect chains, Cloudflare edge caching, live WEALTH-engine data wiring. Load when the user asks to improve, fix, screenshot, or verify any of these pages, or when market data on them looks stale/wrong.
tags: []
related_skills: []
linked_files:
  references:
    - references/world-atlas-live-page-2026-08-08.md
    - references/vitals-transmission-engine-viz-2026-08-08.md
    - references/world-vitals-chart-hero-2026-08-08.md
    - references/gold-macro-context.md
    - references/makcikgpt-static-surface.md
    - references/investbrain-integration-2026-08-08.md
    - references/makcikgpt-vs-writing-architecture-2026-08-10.md
    - references/makcikgpt-design-regression-2026-08-11.md
    - references/caddy-webroot-map-2026-08-11.md
  scripts:
    - scripts/verify-writing-article.py
---

# arif-fazil-web-ops

Arif's sites: `arif-fazil.com` (federation + WEALTH market pages) and `syedos.arif-fazil.com` (personal dashboards, "Abang Sado"). Both are static HTML behind Caddy on 80/443 + Cloudflare. No build step for live pages — edit HTML in place, `systemctl reload caddy` (reload, not restart).

## Rule -2 — Archive Archaeology (BEFORE any landing-page or major-surface mutation)

**The single biggest cause of design drift on this site is agents writing to live without first checking archive.** Multiple design versions of the same surface exist across:
- `/root/forge_work/deployments/arif-fazil.com/<TS>/previous/<path>` — per-deploy snapshots, file sizes tell design age
- `/root/backups/forge_work-archive-2026-07/deployments/arif-fazil.com/<TS>/previous/<path>` — older monthly archives
- `/root/_archive/2026-08-04/backups/...` — pre-reconciliation snapshots
- `/var/www/html/makcikgpt-md.removed-20260811/` — quarantine directory
- git history (`git log --all --oneline -- <path>`)

**Mandatory pre-flight sequence (run BEFORE any write_file to a landing page, hub, or major surface):**

```bash
# 1. Discover ALL archived copies of the target file
TARGET="/var/www/html/arif/makcikgpt-md/index.html"
echo "=== Live ==="
ls -la "$TARGET"
echo "=== Archived copies ==="
find /root /var/www -name "index.html" -path "*makcikgpt*" 2>/dev/null \
  | xargs -I {} sh -c 'echo "$(stat -c%s {})B — {}"' \
  | sort -t: -k1 -nr | head -10

# 2. If multiple versions exist, compare file sizes:
#    - LARGEST = most design investment (richer CSS, more JS, animation)
#    - SMALLEST = stub or degraded
# Pick the design Arif wants (ASK if ambiguous — do NOT assume "newer = better")

# 3. If a git repo exists for the source, check `git log --all --oneline -- <path>`
#    for ALL branches, tags, and reflog entries

# 4. NEVER trust `/var/www/html/<site>/` alone — live webroot can DIVERGE from git
#    (verified 2026-08-11: SyedOS live was just `.git` + 1 stub while git had 11 files)
```

**If you find an archived version LARGER and RICHER than the live:** ask Arif before patching live. The archive may be the design he wants restored.

**Verified incident 2026-08-11 (this session):** `/world/makcikgpt/` was live-served at 14,074 bytes (degraded GitHub-dark palette), while archives held 19,638 bytes (rich red/blue/yellow palette with hero canvas). After "deep archive extraction" Arif chose the 19,638-byte design as the canonical version.

## Rule -1 — Proposal-mode for SOURCE paths (FAIL-CLOSED)

When working under `/root/arif-fazil.com/...` (vs `/var/www/html/arif/...` LIVE), the FAIL-CLOSED `canon/file-authority.yaml` applies. `dist/**` = DERIVED (`hand_edit: false`), `canon/*` = CANON (needs ARIF lease, mutators `[A-FORGE, ARIF]` only — Hermes has no default lease), new files only in `forge_work/proposals/<agent>/<mission>/`. **Always read `/root/arif-fazil.com/canon/file-authority.yaml` BEFORE dispatching any work on the SOURCE path.** "Auto execute" ≠ permission to skip governance.

Use the **3-file proposal contract**: `index.html` + `README.md` + `FORGE_RECEIPT.json` (with sha256 + MYT/UTC timestamps + predict-vs-actual ledger). Then await ARIF promotion. **Predict-before-act = keystone primitive** per external analysis 2026-08-11: write predicted outcome BEFORE the tool call, compare actual vs predicted, record delta honestly. Without prediction-error logging, no world model — just a prompt.

Full pattern, worked example (`/work/` page proposal), and the trap-to-avoid: `references/proposal-mode-fail-closed-2026-08-11.md`.

## Rule 0 — Trace the LIVE serving path before touching anything

These pages exist in **multiple disk copies**; patching the wrong one wastes a session (happened twice in one session). Always:

1. `curl -sIL "https://arif-fazil.com/gold/?cb=$(date +%s)" | grep -iE 'location|last-mod'` — follow redirects to the real URL.
2. `grep -n "world/economics\|@static_dirs\|redir /gold" /etc/caddy/Caddyfile` — find the route.
3. `find /var/www/html -name index.html -exec grep -l '<known-stale-string>' {} \;` — find EVERY copy containing the stale text.
4. **Sibling-writer check before mutation.** Run `ps aux | grep -iE "kimi|opencode|openclaw|claude" | grep -v grep` and `stat -c '%y' <target-file>`. If another worker is alive AND the target file's mtime is within the last 30 minutes, another agent is staging a draft — read the file fresh and fold their content rather than overwrite. Concurrent writers on the same page are a known pattern (kimi/opencode can write `public/.../index.html` and leave it un-deployed for hours).
5. Patch the file Caddy actually serves, then `cp` to sibling copies.

### Known layout (2026-08)
- `/gold/` → 308 → `/world/economics/gold/` → served by `@static_dirs` from **`/var/www/html/arif/world/economics/gold/index.html`** (same for oil, gas, klci, usdmyr).
- **`/words/compass/`** = 7-axis interactive compass rose (live file `/var/www/html/arif/words/compass/index.html`). Dual-lens toggle (power/meaning), SVG compass wheel with 7 clickable axis dots, inspector panel, bottom card grid. All data inline from `axisAdapter.ts` ported to vanilla JS — no React build required. Links to the two companion essays in the footer.
- **`/world/vitals/`** = Sovereign Economic Cockpit (live file `/var/www/html/arif/world/vitals/index.html`, `data-organ="wealth"`). Legacy `/vitals` + `/vitals/*` 308-redirect to `/propa/` (Caddyfile ~L262-263) — never edit there; `/world/vitals/` is the live page. Stale mirrors at `/var/www/html/arif/vitals/` and `/var/www/html/arif/wealth/vitals/` are orphan copies — ignore.
- Sibling copies to keep in sync: `/var/www/html/{asset}/`, `/var/www/html/arif/{asset}/` (may be absent), `/var/www/html/sites/arif-fazil.com/dist/{asset}/` (git dist source — often stale, not live).
- syedos subdomain → `/var/www/html/syedos/` (root) + subpages at `/<slug>/index.html`. Personal surfaces for "Abang Sado" (Syed, Telegram ID 1042200555, SADO group). **Canonical git state** (single commit `6465d50 chore(core): initial commit, F1 lockdown of live syedos vhost`, 2026-08): contains `index.html` (5-card hub — Emas/Nasi Lemak/Heal/Dashboard/Meal-Plan), `dashboard.html`, `emas/index.html` (full gold chart with lightweight-charts + EMA20/50/200), `heal/index.html` + `heal/abang-sado.mp4`, `nasilemak/index.html`, `proposal.html`, `rental-swot.html`, `syed-golden.jpg`, `welcome.ogg`, `llms.txt`. **Live webroot can DIVERGE from git** — verified 2026-08-11 when live deployed state was just `.git` and an empty `/emas/index.html` placeholder while git had 11 canonical files. Recovered via `git checkout HEAD -- .`. **ALWAYS run `git ls-tree -r HEAD --name-only` before contributing** to confirm what's canonical vs. what's just on disk. SyedOS is OUTSIDE the `/root/arif-fazil.com/` FAIL-CLOSED regime — separate git repo at `/var/www/html/syedos/.git`, single-tenant personal deploy. See `references/syedos-personal-surface.md` for layout, recipe, and color system.
- Backups: `cp index.html index.html.bak-YYYYMMDD` before editing. Rollback = copy back + reload caddy.

## Shared design-system assets (`/_shared/`) — deploy root trap + edge cache

**The `/_shared/*` URL is NOT served from the site root's `_shared/` mirror.** The Caddyfile routes `/_shared/*` with `uri strip_prefix /_shared` + `root * /var/www/html/_shared` — so the live file behind `https://arif-fazil.com/_shared/design-system/hub-words.css` is **`/var/www/html/_shared/design-system/hub-words.css`** (federation root), NOT `/var/www/html/arif/_shared/...`. Rsync'ing to `/var/www/html/arif/_shared/` changes nothing the browser can see (hit this exact trap 2026-08-09 — the fix landed only after rsync'ing to the federation root).

- Repo source: `/root/arif-fazil.com/sites/arif-fazil.com/public/_shared/design-system/*.css` (tokens.css, components.css, hub-words.css, hub-writing.css). Live `/var/www/html/_shared/` mirrors these; `/var/www/html/arif/_shared/` is a legacy mirror.
- Deploy: `rsync -a --checksum public/_shared/design-system/*.css /var/www/html/_shared/design-system/` (optionally also the `arif/` mirror for safety). Verify against the PUBLIC url after.
- Per-door accents: hub pages set `--domain-accent` on `<body>`; hub CSS references `--accent-*` vars from tokens.css. **Values must match `canon/atlas.yaml` ring families (SOUL red / MIND cyan / BODY gold / ORGAN violet) + tokens.css organ colors — NOT invented hexes.** My first pass used non-canon cyan/green/amber and had to be held for F13 review; the verified canonical mapping is in `references/design-canon-sot-2026-08-09.md`. Design identity changes = F13's call, not the agent's.

**Cloudflare edge cache for CSS is 4h and query-string busts DON'T work.** Verified 2026-08-09:
- `cf-cache-status: HIT` + `cache-control: max-age=14400` on `/_shared/design-system/*.css`; the `Last-Modified` header tells you WHICH version the edge cached (compare against origin file mtime).
- `?v=20260809`-style cache-busting on the URL **returns the stale object** — CF's default cache key strips query strings on these assets. Do not rely on it.
- Purge API (`POST /zones/<id>/purge_cache`) returned `401 Authentication error` with a token that IS valid for `GET /zones?name=...`. A valid zones-lookup token is NOT proof of `Zone.Cache Purge` permission.
- Reliable fallbacks in order: (a) purge with a token that has Zone.Cache Purge, (b) rename the asset file + update HTML refs (new URL = new cache key), (c) wait out the 4h TTL.
- After rsync: `curl -s <url> | grep <new-marker>` proves content; `curl -sI <url> | grep -i last-modified` proves edge freshness. Both, always.

## Writing articles (`/words/writing/`) — essay pages

- Live path: `/var/www/html/arif/words/writing/<slug>/index.html`. Canonical essay prose (source of truth for body text) lives in the git dist at `/root/arif-fazil.com/sites/arif-fazil.com/public/words/writing/*.md` plus rendered HTML next to them — read those before composing so the body matches the official text.
- **Source of truth for essay body HTML: `/root/arif-fazil.com/sites/arif-fazil.com/src/data/essays/<slug>.ts`** — the `html:` template-literal field. Always extract body from the `.ts` file via regex `html:\s*`(.*?)`,\s*\n\};` and strip `paper-header` + duplicate `<h1>` blocks before embedding. NEVER regenerate the body from a paraphrase — Arif edits his own .ts files and the rendered HTML must match exactly. If a subagent produced content the user rejects ("some of the article is not even true or real"), rebuild from the `.ts` source — the user owns those words.
- **HARD HEADER RULE (Arif's preference, verified 2026-08-07):** The page header chrome MUST be minimal — only:
  1. Top bar `ARIF FAZIL` brand (the user's preferred brand string, NOT "Arif Fazil" — see "ARIF FAZIL brand" pitfall)
  2. Breadcrumb `← Writing`
  3. Kicker `WORDS · [SERIES] · ENGLISH · SEALED 999` (small mono, red)
  4. Big serif `<h1>` title (the attention anchor — human + LLM first-section attention is highest here)
  5. Excerpt/lede subtitle
  6. `<hr>` divider
  7. Article body begins immediately
- **NO byline in header chrome.** No "By Arif Fazil" pill. No "Sealed 999" pill. No date pill. No read-time pill. No tag pills in header. All of that moves to the footer (Arif's explicit instruction: "Remove this at header of the articles and make it as footer").
- **HARD FOOTER RULE (Arif's preference):** Every article page MUST end with this byline footer block before the closing `</div>`:
  ```
  [By Arif Fazil] [Sealed 999] [date] · [N] min read
  [tag pills]
  Muhammad Arif bin Fazil
  Geoscientist · Architect, arifOS · Petronas Carigali · UW–Madison '13
  Penang, Malaysia
  Published: [date] · Direct Publication · /words/ context
  Epistemic Tag: INT — interpretive synthesis across AI governance, institutional economics, and systems theory
  Pairs with: [other triptych / series cross-links]
  ---
  "Ditempa bukan diberi — Forged, not given."
  [MakcikGPT · Doctrine · /feed.xml · llms.txt · missions.json · surfaces.json]
  ```
- Shared design system: `/words/writing/_shared/writing.css` (self-contained dark/gold theme). Article pages LINK this stylesheet (`href="/words/writing/_shared/writing.css"`) and must NOT carry their own inline `<style>`.
- Page pattern: ARIF FAZIL top bar → `← Writing` breadcrumb → kicker `WORDS · [SERIES] · ENGLISH · SEALED 999` → h1 → subtitle → `<hr>` → article body → byline footer (rule above) + site footer. Brand = ARIF FAZIL. Match the makcikgpt pattern exactly — Arif wants the two surfaces mirrored: "Mirror how makcikgpt site being deploy. Zen both."
- **Caddy rule:** `/words/writing/*` is in `@static_dirs` (returns 404), never falls through to SPA. The SPA-rendered `/words/writing/:slug` route exists in App.tsx but is unreachable behind static_dirs — only the static HTML files are live. Rebuild via write_file + chown www-data:www-data + chmod 644.
- Pair-with logic:
  - **S4 triptych:** AGI Paradox ↔ Truth Is Not Cheap ↔ Third Axis of Failure (each links to the other two)
  - **S6 Eureka Trilogy:** each of EUREKA I/II/III links to the other two
  - **S8 Forge:** each of Agentic Intelligence Big Bang / The Tool Is the Thought / Survival of the Fittest Tools / Three Timelines One Boundary links to the other three
- Meta conventions: top bar includes HOME/EARTH/WORDS/WORLD/WORK nav (5-lane nav canon v7); meta line carries "S4 Governance Canon · Article #N" and "Epistemic tag: INT".
- Verify article pages with `scripts/verify-writing-article.py` (tag balance, cover-block, CSS link, refs, sections, link integrity) — ad-hoc check, not a canonical suite.

## `/words/` section pages — Doctrine, Constitution, Writing hub

**Live paths:**
- `/var/www/html/arif/words/index.html` — Words hub (compass hero, "What Lives Here" cards)
- `/var/www/html/arif/words/doctrine/index.html` — **Doctrine overview** (13 Floors, color-coded cards, human-readable)
- `/var/www/html/arif/words/constitution/index.html` — Full canon (detailed metrics, agent-facing)
- `/var/www/html/arif/words/writing/index.html` — Essay listing (SPA-rendered by EssayPage.tsx)

**Source paths:** `/root/arif-fazil.com/sites/arif-fazil.com/public/words/`

### Doctrine page design pattern (forged 2026-08-10)

The `/words/doctrine/` page is the **human-readable overview** of F1–F13. The `/words/constitution/` page is the **detailed agent-facing reference** with metrics. They serve different audiences.

**Design principles for doctrine/governance pages:**
1. **Section by type** — Hard (red) / Soft (amber) / Derived (green), with colored section headers + pill badges
2. **Card structure** — Each floor: number → name → type badge → essence (one-liner) → explanation (human sentence)
3. **F13 highlighted** — Gold border + elevated background. It is the capstone floor.
4. **Intro context** — "What this document is" paragraph + quote from an essay
5. **Legend** — Color legend at top for instant type recognition
6. **Footer** — Links to Full Canon, floors.json, GitHub, MCP, Essays
7. **Content-first** — Zero JavaScript. Works without CSS fallback.
8. **5-lane nav** — MUST use the current nav (Home, Earth, Words, World, Work), NOT the old 7-item nav

**CSS variables for floor types:**
```css
--hard: #D4536B;   /* red — VOID on violation */
--soft: #D49D53;   /* amber — CAUTION or HOLD */
--derived: #6BCF8B; /* green — score-based gate */
```

**Deploy recipe:**
```bash
# 1. Write to live
write_file /var/www/html/arif/words/doctrine/index.html
# 2. Fix permissions
chown www-data:www-data /var/www/html/arif/words/doctrine/index.html
chmod 644 /var/www/html/arif/words/doctrine/index.html
# 3. Sync to source repo
cp /var/www/html/arif/words/doctrine/index.html \
   /root/arif-fazil.com/sites/arif-fazil.com/public/words/doctrine/index.html
# 4. Verify live
curl -sIL "https://arif-fazil.com/words/doctrine/?cb=$(date +%s)" | head -5
# 5. Browser verify (MANDATORY — vision check for visual regressions)
browser_navigate → browser_vision
```

### Pitfall: Old nav on sub-pages

**Problem:** Sub-pages under `/words/` (especially `/words/doctrine/`) may carry an old 7-item nav (Home, Earth, Economics, World, Writing, Doctrine, Missions, ???, VITALS, llms.txt) instead of the current 5-lane nav (Home, Earth, Words, World, Work). This happens when a sub-page was created before the nav canon v7 reorg and wasn't updated.

**Detection:** `grep -c 'Economics\|Missions\|VITALS\|llms.txt' /var/www/html/arif/words/*/index.html` — any match = old nav.

**Fix:** Replace the `<nav>` block with the 5-lane pattern:
```html
<nav class="nav" aria-label="Primary">
  <a href="/">Home</a>
  <a href="/earth">Earth</a>
  <a href="/words" class="here">Words</a>
  <a href="/world">World</a>
  <a href="/work">Work</a>
</nav>
```

### Pitfall: Old CSS imports on sub-pages

**Problem:** Some `/words/` sub-pages import `/_shared/zen.css` and `/_shared/economics.css` instead of the design system (`tokens.css` + `hub-words.css`). The old CSS files may conflict with or not provide the design system variables.

**Detection:** `grep -l 'zen.css\|economics.css' /var/www/html/arif/words/*/index.html`

**Fix:** Replace with:
```html
<link rel="stylesheet" href="/_shared/design-system/tokens.css">
<link rel="stylesheet" href="/_shared/design-system/hub-words.css">
```

### Words section unified design (forged 2026-08-10)

All `/words/` sub-pages now share a unified design language: 5-lane nav, gold accent, design system CSS (tokens.css + hub-words.css), card-based layouts. The principle is **contrast yet federated** — same pattern, different voices.

| Page | Accent | Pattern | Voice |
|------|--------|---------|-------|
| `/words/` | Gold | Compass hero + 13 floors preview + featured essays | Navigational |
| `/words/doctrine/` | Gold (with red/amber/green floor cards) | Color-coded floor list | Constitutional |
| `/words/writing/` | Gold | Card-based essay listing with featured + series | Academic |

**Writing listing design pattern (forged 2026-08-10):**

The `/words/writing/index.html` listing uses card-based layout aligned with MakcikGPT's pattern:

1. **Hero** — Title + description + stats (15 essays · sealed 999 · updated DATE)
2. **Blockquote** — Featured quote from an essay
3. **Featured section** — 2×2 grid of 4 most important essays with "START HERE" badge
4. **Chronological groups** — Essays grouped by month with series labels (S4/S6/S8)
5. **Card structure** — Each card: gold accent line at top → title + date → excerpt → tags + "Read essay →" CTA
6. **Footer** — Links to Doctrine, Full Canon, Words Hub, /floors.json

**Card CSS pattern:**
```css
.w-card {
  background: #111318;
  border: 1px solid #1E232A;
  border-top: 3px solid var(--gold);  /* gold accent line */
  border-radius: 6px;
  padding: 1.15rem 1.35rem;
  margin: 0.65rem 0;
}
```

**Series tag colors:**
- S4 (Governance Canon): gold `#D4A853`
- S6 (Eureka Trilogy): cyan `#4FC3F7`
- S8 (Forge): ember `#E4572E`
- SITE: muted `#8A8578`

**Contrast with MakcikGPT:**
- MakcikGPT: red accent line, BM voice, domain-specific tags
- Writing: gold accent line, English academic, series tags
- Same card pattern, different accent color and voice

**Deploy recipe:** Same as doctrine page — write_file → chown → chmod → cp to source → verify with browser_vision.

### Pitfall: Duplicate content on listing pages

**Problem:** Listing pages (especially `/words/writing/index.html`) may contain duplicate content — e.g., a `<details>` toggle with essay list AND a hidden `<ul class="flat-list" aria-hidden="true">` with the same essays. This is redundancy that wastes bytes and confuses maintenance.

**Detection:** `grep -c 'class="flat-list"' /var/www/html/arif/words/writing/index.html` — if >0, duplicate exists.

**Fix:** Remove the hidden duplicate. Keep only the card-based listing.

### Pitfall: Zen-pulse bar on non-hub pages

**Problem:** The `zen-pulse` aside (WHERE AM I / WHY CARE / WHAT NEXT) was designed for hub pages but appeared on sub-pages like `/words/writing/`. It's confusing on sub-pages — the reader already knows where they are.

**Detection:** `grep -l 'zen-pulse' /var/www/html/arif/words/*/index.html` — any match on a sub-page = should be removed.

**Fix:** Remove the `<aside class="zen-pulse">` block from sub-pages. Keep it only on hub pages (`/words/`, `/world/`, etc.).

---

## MakcikGPT static article pages (`/makcikgpt-md/`) — mirrored surface

- **Live path is `/var/www/html/arif/makcikgpt-md/<slug>.html` — NOT under `world/`.** Caddy `@ai-bot-world` / `@makcikgpt_nojs` handlers strip the `/world/makcikgpt` prefix and serve `try_files {path} {path}.html {path}/index.html /index.html` from that dir. Browsers get the SPA shell (`handle /world/makcikgpt/*` → `/index.html`); only bots/no-JS clients see these statics. Full routing + layout: `references/makcikgpt-static-surface.md`.
- **Source of truth:** `/root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/<slug>.ts` — the `html:` template-literal field is the article body. Metadata (title, subtitle, date, domain, tags) lives in `makcikArticlesMeta` in `index.ts`.
- **Page pattern = writing-article pattern:** ARIF FAZIL top bar → `← MakcikGPT` breadcrumb → kicker `DOMAIN · SEALED 999` → h1 → subtitle → byline (`By Arif Fazil · Sealed 999 · date · N min read`) → tag pills → `<hr>` → article body → byline footer block + "Ditempa bukan diberi" + agent metadata + surface links. Brand = ARIF FAZIL. **Must match `/words/writing/` exactly** (Arif: "Mirror how makcikgpt site being deploy. Zen both.").
- **SPA parity required:** `src/pages/MakcikGptArticle.tsx` (browser route) must contain the same byline footer block. When patching, insert AFTER `</article>` and BEFORE the closing `</section></motion.div>` — use React `Link to=...` not `<a href>` for SPA-internal links. Patches to this file need to use `</Link>` not `</a>` (caught a typo on first attempt). TSX compiles via `npx tsc --noEmit` from `/root/arif-fazil.com/sites/arif-fazil.com`.
- **SPA slug registration is MANDATORY for browser visibility.** Writing a static file to `makcikgpt-md/<slug>.html` is NOT enough. Browsers hit `handle /world/makcikgpt/*` → SPA shell → React resolves the slug client-side. If the slug is not in the SPA bundle (`assets/index-*.js`), React renders **"ARTICLE NOT FOUND"** even though the static file exists and curl returns HTTP 200. See the verification recipe below.
- **Two-file drift:** `world/makcikgpt/<slug>/index.html` and `makcikgpt-md/<slug>.html` can diverge (different CSS, HTML entities, wording). Always write to ONE canonical source (the `makcikgpt-md/` path) and either `cp` to the other or delete the second copy. Never write both independently.
- **Generator (legacy):** `scripts/generate-makcik-articles.cjs` (site root) writes `public/makcikgpt-md/<slug>.html`. New approach: directly write_file to `/var/www/html/arif/makcikgpt-md/<slug>.html` + chmod. Don't use the generator — it strips headers we want kept.

### DUAL-WITNESS VERIFICATION (mandatory after any MakcikGPT publish)

**curl-only gates produce false positives.** A sibling agent reported "Gate 1–7 ALL PASSED, article live, HTTP 200" for `syaitan-ingat-dirinya-malaikat` (2026-08-09) — every gate used curl, which matches Caddy's `@ai-bot-world` UA matcher (`curl` is literally in the bot regex). The article was bot-visible only; real browsers rendered "ARTICLE NOT FOUND". Verified comparison:

| Article | In SPA bundle? | Real browser | curl/bot |
|---|---|---|---|
| cerita-makcik | ✅ | ✅ full article | ✅ |
| 70-sen-daripada-setiap-ringgit-untung-dah-keluar | ❌ | ❌ ARTICLE NOT FOUND | ✅ 200 |
| syaitan-ingat-dirinya-malaikat | ❌ | ❌ ARTICLE NOT FOUND | ✅ 200 |

Post-publish verification must pass ALL FOUR:

```bash
SLUG="<slug>"
# W1 — bot path (curl, -L required: trailing slash 301s to no-slash)
curl -sfL -o /dev/null -w "%{http_code} %{size_download}\n" \
  "https://arif-fazil.com/world/makcikgpt/$SLUG/"
# W2 — SPA bundle registration (browser visibility)
BUNDLE=$(grep -oE 'assets/index-[^"]+\.js' /var/www/html/arif/index.html | head -1)
grep -c "$SLUG" "/var/www/html/arif/$BUNDLE"   # 0 = browsers get ARTICLE NOT FOUND
# W3 — landing page lists the article
grep -c "$SLUG" /var/www/html/arif/makcikgpt-md/index.html
# W4 — REAL browser render (the decisive witness)
# browser_navigate → https://arif-fazil.com/world/makcikgpt/$SLUG/
# snapshot must show the <h1> article title, NOT "ARTICLE NOT FOUND"
```

If W1 passes but W2/W4 fail: the article is **bot-only**. Human sharing (WhatsApp/Telegram taps) dead-ends. Fix = register slug in SPA (`src/data/makcikgpt/<slug>.ts` + `index.ts` meta + rebuild) or land a Caddy route that serves the static file to browsers. Do NOT report "live" on W1 alone.

When the user/another agent insists "the article IS live, HTTP 200" after you report it browser-dead: they are quoting the bot witness. Do not concede — re-show the curl-vs-browser table with live probes. Arif rewards pushback backed by live evidence; "HTTP 200" from curl is not evidence of human accessibility on this surface.
- Writing index `/words/writing/index.html` S4 cards use kicker `WORDS · S4 · SEALED 999` — verify only, don't rewrite.

## Dual-register article workflow (English + Bahasa Makcik)

When Arif asks for two articles on the same topic — one English (Medium-level) at `/words/writing/` and one Bahasa Makcik at `/world/makcikgpt/` — the workflow is:

1. **Write both files in one pass.** Same body content, two registers. English academic = long sentences, sections, thesis→argument→proof→synthesis. Bahasa Makcik = conversational, "hang" address, "Makcik, hang tau tak", concrete examples from pasar malam.
2. **English article** → `/var/www/html/arif/words/writing/<slug>/index.html`. Use the existing writing pattern (ARIF FAZIL top bar, kicker, h1, hr, body, byline footer). Size: ~3000 words.
3. **Makcik article** → `/var/www/html/arif/makcikgpt-md/<slug>.html`. Use the existing MakcikGPT pattern (same top bar, kicker "BAHASA MAKCIK", h1, body, byline footer). Size: ~1500 words. **Deploy to `/var/www/html/arif/makcikgpt-md/` NOT `/var/www/html/arif/world/makcikgpt/`** (Caddy routing serves statics from `makcikgpt-md/` via `@ai-bot-world`).
4. **Register both in `/words/writing/index.html`** (essay list). Makcik article gets a link in the English essay's `Pairs with:` field.
5. **Add both to `/llms.txt`** in the key pages section.
6. **Compass page footer** — update with links to both essays if the topic is compass-related.

**Full architecture mapping:** see `references/makcikgpt-vs-writing-architecture-2026-08-10.md` (deployment, Caddy routing, design contrast, shared patterns, key architectural difference).

## Human-First Design Rules (apply to ALL public surfaces)

**The site is for humans first. Agents serve humans.** Every design decision must pass these filters before mutation:

| Filter | Rule | Failure mode |
|---|---|---|
| **Lead with human anchor** | First 100px above the fold must show WHO/WHERE/WHY in plain language. No status codes. No "888 JUDGE" jargon. No organ acronyms. | Visitor lands confused, bounces |
| **One question at a time** | Page answers WHERE AM I? / WHY CARE? / WHAT NEXT? within 3 seconds (Zen Pulse pattern). Don't dump stats before hero. | Cognitive overload → abandonment |
| **Lead with verb, not noun** | "Read the analysis" not "Analysis Page". "Latest words" not "Writing". Cards are actions, not items. | Page feels like a directory, not a destination |
| **No internal jargon leaking** | Public surfaces: NO F1-F13 codes in headlines, NO SEAL/HOLD/VOID stamps in `<title>`, NO organ acronyms, NO "888 JUDGE". Stamps OK in body/byline where source-attribution makes sense. | Visitor feels like they're reading audit logs |
| **Status rows go in footer, not header** | Header chrome: brand + nav + breadcrumb + kicker + h1 + subtitle. Footer: byline + date + tags + read time + provenance. The first thing eyes see is the WORK, not the META. | Author identity drowns out the actual content |
| **Color contrast = legibility** | Every accent color must pair with readable text. forge-red on dark bg = good. Tailwind blue-500 on dark bg = good. Bright yellow text on white bg = illegible. | Eye strain, low engagement |
| **No more than 3 accent colors per page** | More than 3 = circus. Red + gold + blue is enough. Add white/grey/dark for hierarchy. | Visual noise |
| **Mobile-first layout** | `<meta viewport>` set. Single-column below 768px. `flex-wrap` on pill rows. `gap-3` minimum between cards. | 60%+ mobile traffic gets broken layout |
| **Footer always carries "Ditempa bukan diberi"** | It is the sovereign mark. Removing it = F13 violation. | Identity loss |
| **No auto-playing audio/video on landing** | Static surface only. Animation OK if `prefers-reduced-motion` respected. | Accessibility violation, performance hit |

**The "human cognitive limit" rule:** No landing page should require more than 7 ± 2 navigation choices at once (Miller's Law). If you have >7 series cards, group them. If >10 articles visible, paginate. If >3 competing visual focal points, pick one.

## Pitfalls

- **DESIGN DRIFT INVESTIGATION — when user reports "design lari" / "previous design" / "I hate it" / "ugly for human" on ANY surface, follow the recipe BEFORE writing fixes (verified 2026-08-11).** Symptoms that trigger this recipe:
  - BM: `design lari` (design drifting), `aku benci site ni`, `design x boleh bagi sama ka?`, `current pon design lari`
  - EN: `previous design`, `I want the old version`, `the current site is ugly`
  - User shares a screenshot showing a different design than what's currently live
  - User compares two surfaces (article vs landing) and finds them inconsistent

  **Step 1 — Archive snapshots FIRST.** `/root/forge_work/deployments/arif-fazil.com/<timestamp>/previous/` has the exact pre-deploy state for every deploy. Each timestamp dir has `/previous/` with full file copies. `find /root/forge_work/deployments/arif-fazil.com/2026*/previous/ -name "index.html" -size +2k` → real content (105B = stub). This is the ground truth for "what was deployed before."

  **Step 2 — Git archaeology for deleted source.** When `.ts` source is missing from working tree but should exist: `git -C /root/arif-fazil.com log --all --oneline -- "**/*.ts"` to find the last commit that had it, then `git show <commit>:<path>` to extract the deleted source verbatim. Use the extracted source as design reference for the static HTML.

  **Step 3 — Run the 5-step recipe.** `references/makcikgpt-design-drift-recipe.md` has the full investigation: live-probe → source-of-truth (3 sources: static HTML / SPA component / TS source) → token diff → root cause classification (3 patterns: hand-written-no-TS / two-template-inconsistency / CSS-bundle-drift) → fix-path approval matrix.

  **Step 4 — Choose Path A or Path B per `references/makcikgpt-hand-written-drift-fix.md`.** Path A = upgrade static HTML in place (faster, static-only). Path B = add TS source for full SPA parity (multi-file, build pipeline). Pick based on whether the article needs future rebuilds to pick it up.

  **Do NOT start writing fixes before running the recipe.** Don't guess from screenshots — verify with `curl -s <url> -H "User-Agent: Mozilla/5.0 Chrome/119" -H "Accept: text/html" | grep -E "<known-element>"` what the live page actually serves. Single-curl probes miss UA-differential routing bugs.

- **SCREENSHOT PROOF PROTOCOL — user explicitly demands screenshots, deliver via `MEDIA:` prefix (verified 2026-08-11).** When user says `tunjuk screenshot`, `show screenshot`, `share link and screenshot`, `bagi link and screenshot for me to verify`:
  1. **Capture + IMMEDIATELY copy to /tmp** — screenshots in `cache/screenshots/*.png` get evicted between turns (cache size cap). The instant `browser_vision` returns the path, copy it: `cp <path> /tmp/<slug>-<purpose>.png`. The `/tmp/` copy is what survives until your reply ships. Verified 2026-08-11 on the `/world/makcikgpt/` design-regression session — without the /tmp copy, the screenshot URL was stale by the next turn.
  2. Include in reply: `MEDIA:/tmp/<slug>-<purpose>.png` (MUST be absolute path; the prefix triggers Telegram native file delivery)
  3. Also include the URL the screenshot is from — the link + screenshot pair is the verifiable witness
  4. **Common typo trap:** `IA:/path` (without the `MED`) silently fails — file is not delivered. Always use exactly `MEDIA:`.
  5. If vision tool returned blank or confused analysis, describe what curl/grep confirmed about the HTML — don't claim visual proof you don't have. The HTML/curl evidence IS the proof.
  6. Verify the file exists at the path before promising it: `ls -la /tmp/<slug>-<purpose>.png`.
  7. **Re-send fresh if user says "mana screenshot"** — they're saying the previous MEDIA didn't render or didn't arrive. Don't argue; retake + copy + resend with explicit "sini — 80KB, 1265×1021" size proof.

  **Vision tool unreliability on dark-mode designs:** `browser_vision` and `vision_analyze` frequently return "blank screenshot", hallucinated content ("MAKCIK INTELLIGENCE" from Medium), or confused analysis for dark-mode + tight-crop screenshots. When this happens, do NOT retry the vision tool — fall back to:
  - `curl -s <url> -H "User-Agent: Mozilla/5.0 Chrome/119.0.0.0"` with grep for known classes/text
  - Read the source HTML directly (`/var/www/html/arif/<path>/index.html`)
  - Describe the confirmed HTML structure in your reply alongside the screenshot

  For deeper vision needs when `vision_analyze` keeps failing, see `references/vision-bypass-gemini-api.md` for direct Gemini REST API recipe (works even when the model layer rejects `image_url` content parts).

- **AGENT-CHROME DEFENSE — DESIGN_INVARIANTS.md + design-lint.sh + idempotent mass style injector (forged 2026-08-11).** Three files lock the human-vs-agent surface boundary: (1) `DESIGN_INVARIANTS.md` declares the "5 Rein" forbidden patterns and per-surface visual contracts. (2) `scripts/design-lint.sh` scans every `public/`, `src/`, `*.tsx/ts/css` file for "Canonical landing:", "WHERE AM I?", "WHY CARE?", "Source of truth:", "Rendered by", "Generated by", file/script paths — exits 1 on match. (3) `scripts/inject-article-styles.sh` is the marker-aware idempotent bash+python pattern for retro-applying styles to N existing files (verified injecting Primer Dark CSS into 82 articles, <3 sec wall-clock, re-runnable). Wire to npm prebuild to make regression impossible. Full timeline + 4-layer resolution in `references/makcikgpt-design-regression-2026-08-11.md`.

- **BULLDOZE PATTERN — NEVER `write_file` an existing site's `index.html` or overwrite its root without first checking git (verified 2026-08-11).** Symptom: agent sees `/var/www/html/<site>/` showing only `.git` (or thin content) and assumes the site is empty, then writes a fresh blank-slate index.html that **wipes the canonical version** the user spent agents and hours building. User reaction: *"Weiii. Hang revert balik. Mana pi semua gold chart resit dashboard bagai. Suka2 bulldoze site yabg dah Ada. Penat agent Sebelum ni buat."*

  **Why this happens — the "verified empty" trap:** every site on disk has TWO sources of truth, and they may DIVERGE:
  1. The **git repo** (canonical — what the user's previous agents built)
  2. The **live webroot** on disk (may be a half-deployed, mid-edit, or rolled-back snapshot — what you see with `ls`)

  If they diverge, **git wins, NOT your `ls`.** The `ls` only shows whatever happened to be deployed when the last sibling agent finished. The actual canonical site lives in git history.

  **Mandatory sequence before ANY contribution to an existing LIVE site** (syedos.arif-fazil.com, arif-fazil.com, goldenratio.work, whatever has a `.git` in its webroot):
  ```bash
  cd /var/www/html/<site>/
  git log --oneline -10          # what's the canonical history?
  git status                     # any uncommitted diffs?
  git ls-tree -r HEAD --name-only # WHAT EXACTLY IS IN GIT?
  ls -la                         # what is deployed right now?
  ```
  If `git ls-tree` shows files that `ls -la` doesn't → the canonical content is in git; live is behind. **DO NOT OVERWRITE — INTEGRATE.**

  **Integration pattern (the right move):**
  1. `git checkout HEAD -- .` to restore all canonical files to disk
  2. `chown -R www-data:www-data /var/www/html/<site>/`
  3. `chmod 644` for files, `755` for dirs
  4. **Read the existing `index.html` first** to understand structure, cards, nav, anchor patterns
  5. **ADD a new card / new subroute** — do NOT overwrite the existing root
  6. If your new content logically belongs on the root, **patch the existing `index.html`** (use `patch` tool with multi-line unique anchor), don't write a blank replacement
  7. Verify all routes with `curl -s -o /dev/null -w "%{http_code} · %{size_download}B"` — every route that was 200 before must still be 200, with size ≥ pre-edit size

  **Recovery recipe** (when you already bulldozed, like 2026-08-11T15:30Z on SyedOS):
  ```bash
  cd /var/www/html/syedos/
  # 1. Backup any new content you wrote (don't lose it)
  cp -r meal-plan /tmp/syedos-meal-plan-backup  # example
  # 2. Restore canonical state from git
  git checkout HEAD -- .
  # 3. Fix perms
  chown -R www-data:www-data /var/www/html/syedos/
  chmod 644 /var/www/html/syedos/*.html /var/www/html/syedos/emas/index.html ...
  # 4. Re-add your new content carefully (as new route or new card in existing root)
  # 5. Probe ALL routes, not just the new one
  for path in / /dashboard/ /emas/ /heal/ /nasilemak/ /meal-plan/; do
    curl -s -o /dev/null -w "$path → %{http_code} · %{size_download}B\n" \
      "https://syedos.arif-fazil.com$path?cb=$(date +%s)"
  done
  ```

  **The deeper reason this matters (Arif's meta-rule):** the user invests in agent-built infrastructure. Each page is iteration. Bulldozing is not "fixing" — it's deleting. Every overwrite should answer: *"is the user's existing work wrong? Or am I just missing it?"* Default answer is the second one. Check first, write second.

- **STYLE-MATCH PROTOCOL — when adding new sub-pages to an existing site, match its style tokens EXACTLY (verified 2026-08-11).** Symptom: agent writes a new sub-page with its own color palette, fonts, card style, and rhythm — works fine standalone, but visibly doesn't belong on the site. User reaction: *"design x boleh bagi sama ka?"* — often softened, but the signal is clear: **match the host site's SOT, not invent your own.**

  **Why this happens:** every site on arif-fazil.com has a designer-curated palette and card style. The agent's defaults are usually off-palette (`#D4A853` gold when the site uses `#f0a500`, `border-radius: 4px` when the site uses `12px`, `font-size: 0.85rem` mono labels when the site uses `11px` uppercase). Even small drifts read as "different site."

  **Mandatory 4-step Style-Match Protocol — run BEFORE writing a new sub-page or content surface:**

  ```bash
  # 1. Extract the canonical palette + type scale from the host page
  head -90 /var/www/html/<site>/index.html
  # Look for: :root { --bg: ...; --card: ...; --gold: ...; --text: ...; --muted: ...; }
  # Look for: body { font-family: ...; padding: ...; }
  # Look for: .card, .pill, .timeline, .meal-card CSS rules
  # Note: border-radius (4 vs 6 vs 12), font sizes (px vs rem), grid (1fr 1fr vs auto-fit)
  
  # 2. Extract any shared CSS file the hub imports
  ls /var/www/html/<site>/_shared/ 2>/dev/null
  cat /var/www/html/<site>/_shared/*.css 2>/dev/null
  
  # 3. Cross-check with the design canon (if it exists)
  grep -i "<site-name>" /root/<source-repo>/canon/design-tokens.yaml 2>/dev/null
  ```

  **Apply EXACTLY these variables in your new sub-page's `:root`**:
  ```css
  :root {
    --bg: <exact hex from host>;
    --card: <exact hex>;
    --line: <exact hex>;
    --gold: <exact hex>;
    --gold2: <exact hex>;
    --text: <exact hex>;
    --muted: <exact hex>;
    --red: <exact hex>;
    --green: <exact hex>;
    --amber: <exact hex>;
  }
  ```

  **Reproduction: the 2026-08-11 meal-plan incident.** SyedOS hub uses `--bg: #0a0a0f`, `--card: #12121a`, `--line: #1e1e30`, `--gold: #f0a500`, `--text: #d1d5db`, `--muted: #6b7280`, mono-free sans-serif at 11–13px, `border-radius: 12px`, 2-column grid. My first meal-plan pass used `#0a0a0a`, `#141414`, `#1f1f1f`, `#D4A853` (slightly off), `#e8e8e8`, `#888`, mixed Courier mono, `border-radius: 4px`, single-column 1100px max-width. Visible mismatch on every line. User asked *"design x boleh bagi sama ka?"* — passed as soft correction, not loud. **Fix:** patch the CSS to match host `:root` variables exactly, then propagate the same `--bg/--card/--line/--gold/--text/--muted` everywhere; copy the host's `.card` style verbatim; keep mono only where the host uses mono.

  **Tier of severity:** if the user explicitly says "new design", "different look", "your style" — then your design stands, don't second-guess. If they say nothing about design, **default to match the host**. When in doubt: ask which way to lean, but offer "match host exactly" as the default option.

- **MAINTENANCE > FLASH — when choosing between rich archive palette vs canonical forge tokens, PICK FORGE TOKENS (verified 2026-08-11).** Symptom: user shows screenshot of beautiful older design (e.g. Primer Dark red/blue/yellow from `/root/backups/forge_work-archive-2026-07/.../20260731T124934083475118Z/previous/makcikgpt-md/index.html` — 19,638B), asks "deep archive extraction", and after seeing options asks "Mana yang lagi senang untuk future agents buat elok2 aku penat la web sites ni". User verdict: forge tokens win, NOT the flashier archive palette.

  **The trade-off matrix:**

  | Dimension | Custom archive palette (e.g. Primer Dark) | Forge tokens (canonical site palette) |
  |---|---|---|
  | Maintainability | Custom CSS variables (`--red:#e0301e`, `--blue:#1f3fd4`, `--yellow:#f2b705`) | Tailwind classes (`text-forge-red`, `text-forge-gold`, `border-forge-iron`) |
  | Cross-surface consistency | Per-page only | Same palette across `/words/`, `/doctrine/`, `/earth/`, `/world/`, `/000/`, `/999/` |
  | New page authoring | Recreate design from scratch (sibling agents will drift) | Copy pattern from existing page, swap content |
  | Custom JS required | Often (canvas particles, search bar, animated cards) | None — HTML + Tailwind classes |
  | Sibling agent drift risk | HIGH — every new page is bespoke | LOW — same pattern repeated |
  | User's mental model | "Why is every page different colors?" | "I know where the gold/red colors come from" |

  **Arif's actual ask (verbatim 2026-08-11):** "Mana yang lagi senang untuk future agents buat elok2 aku penat la web sites ni. Aku nak design tu cantik mata memandang. Manusia nak terus membaca." → "Which is easier for future agents to maintain well? I'm tired of this website. I want the design to be beautiful to look at. Humans want to keep reading." Decision: forge tokens. Rationale: Arif is tired of maintaining the site. Future agents will keep editing. Forge tokens give them a system to follow, not a one-off design to recreate.

  **Implementation recipe — tricolor contrast with forge tokens + minimal Tailwind:**
  ```html
  <!-- Header kicker — red / blue / gold contrast -->
  <div class="font-mono text-[0.65rem] uppercase tracking-widest flex gap-3">
    <span class="text-forge-red">CIVIC INTELLIGENCE</span>
    <span class="text-blue-500">Ξ WEALTH</span>
    <span class="text-forge-gold">SEALED 999</span>
  </div>

  <!-- Status pills — color-coded borders -->
  <span class="border border-forge-red text-forge-red">999 SEALED</span>
  <span class="border border-forge-gold text-forge-gold">26 ARTICLES</span>
  <span class="border border-blue-500 text-blue-400">5 SERIES</span>

  <!-- 5 series cards — each with different accent color -->
  <!-- M1 Energy     = red      -->
  <!-- M2 Governance = gold     -->
  <!-- M3 Tech       = blue     -->
  <!-- M4 Economy    = orange   -->
  <!-- M5 Politics   = white    -->
  ```

  **Forge palette tokens verified (from `/assets/index-Dte6gqTG.css`):**
  ```
  forge-red:    rgb(240, 80, 110)   /* pinkish-red */
  forge-gold:   rgb(201, 168, 76)   /* gold/amber */
  forge-green:  rgb(49, 196, 141)   /* mint green */
  forge-orange: rgb(176, 141, 87)   /* warm amber */
  forge-iron:   rgb(31, 39, 51)     /* dark grey */
  forge-dim:    rgb(139, 152, 168)  /* muted grey */
  forge-black:  rgb(10, 12, 16)
  forge-steel:  rgb(17, 21, 28)
  forge-white:  rgb(230, 237, 243)
  ```
  **No native forge blue.** For "blue" contrast use Tailwind utility classes: `text-blue-400`, `text-blue-500`, `border-blue-500` (RGB values are in the standard Tailwind palette baked into `index-Dte6gqTG.css`).

- **PERSONA-SURFACE PROMOTION — when an article body earns a MakcikGPT landing-page slot, the landing must match the article's voice and trim, NOT carry generic landing chrome (verified 2026-08-11).** Pattern from the `syaitan-ingat-dirinya-malaikat` flip: after patching the article to forge-red palette with section-label `Civilization Intelligence · Ξ WEALTH · MAKCIKGPT × PETRONAS × AMANAH`, the landing `makcikgpt-md/index.html` was also re-skinned with the same section-label, the same italic-uppercase h1 (`Makcik<br/>GPT` text-6xl md:text-8xl font-black), the same forge-red kicker, and tricolor pill status row. Result: clicking from landing → article no longer feels like two different sites.

  **Rule of thumb:** landing-page chrome and article-page chrome MUST share:
  - Section-label prefix (2 lines: domain · domain · cooperation)
  - h1 styling (font-display font-black uppercase tracking-tighter)
  - Kicker color (forge-red mono uppercase)
  - Subtitle palette (forge-orange for action, forge-white for emphasis)
  - Footer block (Ditempa bukan diberi + llms.txt/missions.json/surfaces.json)
  - Topbar nav (5-lane: Home/Earth/Words/World/Work, World active)

  **What NOT to copy across:**
  - Hero canvas / animated particles (landing-only decoration)
  - Search bar (landing-only, articles don't need it)
  - Custom JS render functions (articles are static HTML)

- **Content-Security-Policy blocks iframe embeds (YouTube, etc.).** The CSP header in `/etc/caddy/Caddyfile` (line ~45) does NOT include `frame-src` by default. Any page with `<iframe>` (YouTube embeds, external widgets) will render the iframe as EMPTY — no error, no console message, just blank space. Fix: add `frame-src https://www.youtube.com https://www.youtube-nocookie.com;` to the CSP directive BEFORE `frame-ancestors 'self'`. Then `sudo systemctl reload caddy`. Verified 2026-08-09: Taufiq Shadow page had 0 iframes rendering until CSP was patched. Symptom: `document.querySelectorAll('iframe').length === 0` despite HTML containing iframe tags.

- **JS injection order into existing `<script>` blocks is the #1 debugging trap.** When injecting JS into a page's existing `<script>` block, the new code MUST be placed AFTER all `const`/`function` declarations it depends on. Failure mode (2026-08-08): viz code using `$()` was injected before `const $=id=>document.getElementById(id)` — all viz functions failed silently, SVGs rendered empty, outputs showed `–`. The `node --check` validator passed syntax but not execution order. Diagnosis: `browser_console` → `engine is not a function` → trace revealed injection was before `$` definition. Fix: move injected block to after the last function call in the existing script (`engine();` at end = injection point). Validate with `node --check <script_content>` after extraction.

- **Subagents fabricate content and clobber your work in the background.** Concrete 2026-08-07 failures:
  1. A delegation wrote `<p>Hannah Arendt</p>` + `Eichmann in Jerusalem` references + book citations that Arif never wrote — he rejected them as "not even true or real". When a subagent says "I added more references and sections" without source backing, it's invention. **Rule: any essay body, references, sections, or quotes must come from the user's actual paste or the `.ts` source. Reject subagent additions unless they're sourced.**
  2. `scripts/render-words-essays.cjs` was created by a subagent and put in `npm run build` prebuild — it kept clobbering my work with its own (different) page format. **Fix on takeover**: `mv /root/arif-fazil.com/sites/arif-fazil.com/scripts/render-words-essays.cjs /root/scripts/render-words-essays.cjs.archived` AND remove ` && node scripts/render-words-essays.cjs` from the prebuild string in `package.json`. Verify with `grep -n render-words package.json` (should return nothing).
  3. After any subagent completion, **verify your work survived** by running `curl -s "https://arif-fazil.com/words/writing/<slug>/" | grep "<known-marker>"` against a marker YOU put in your HTML. If the marker is missing, the subagent overwrote your pages — diff with `git -C /var/www/html/arif diff` (won't work — these aren't git-tracked) or just rebuild from your source.
- **Sibling agents write to the same live paths.** Other arifOS agents build/rewrite these article pages concurrently and may (a) overwrite a spec-conforming page with a different pattern (inline `<style>`, no cover block, different refs) or (b) delete `_shared/` dirs site-wide. After any write, re-verify from disk; if verification suddenly fails, re-read the file — your content may have been replaced — and restore the spec-conforming version rather than "fixing" your own code. Check `stat` mtime + `wc -c` against what you wrote to detect replacement fast.
- **ARIF FAZIL brand string (Arif's explicit preference, 2026-08-07).** Use `ARIF FAZIL` (uppercase) as the top-bar brand — NOT "Arif Fazil". The byline inside article chrome uses `By Arif Fazil` (sentence case) — those are different. The user's site brand is the all-caps form.
- **`write_file` creates files owned by root:root mode 600 — unservable by Caddy.** After every `write_file` under `/var/www/html/`, immediately fix ownership and permissions:
  ```bash
  chown www-data:www-data /var/www/html/arif/<path>/index.html
  chmod 644 /var/www/html/arif/<path>/index.html
  # Repeat for _shared/writing.css if newly created:
  chown www-data:www-data /var/www/html/arif/words/writing/_shared/writing.css
  chmod 644 /var/www/html/arif/words/writing/_shared/writing.css
  ```
  Without this the page returns 403 or 404 to visitors. Existing files (644, www-data) are safe.

- **`write_file` creates files owned by root:root mode 600 — unservable by Caddy.** After every `write_file` under `/var/www/html/`, immediately fix ownership and permissions:
  ```bash
  chown www-data:www-data /var/www/html/arif/<path>/index.html
  chmod 644 /var/www/html/arif/<path>/index.html
  # Repeat for _shared/writing.css if newly created:
  chown www-data:www-data /var/www/html/arif/words/writing/_shared/writing.css
  chmod 644 /var/www/html/arif/words/writing/_shared/writing.css
  ```
  Without this the page returns 403 or 404 to visitors. Existing files (644, www-data) are safe.

- **Create `_shared/writing.css` BEFORE the article HTML.** The article links the shared CSS (`href="/words/writing/_shared/writing.css"`) and must not carry inline `<style>`. Write the CSS file first (or confirm it exists and has the right selectors), then write the HTML. A common failure mode: sibling agent deletes `_shared/` mid-session → article renders unstyled. Detect with `ls -la /var/www/html/arif/words/writing/_shared/writing.css` after every write.

- **Cover-block class names must match the CSS exactly.** The shared writing.css uses `.cover .cover-emoji`, `.cover .cover-kicker`, `.cover .cover-title`, `.cover .cover-subtitle`, `.cover .cover-byline` (all prefixed). HTML must use `class="cover-emoji"` (etc.), NOT `class="emoji"`, `class="title"`, `class="byline"`, or `class="date"`. The `verify-writing-article.py` script enforces this — run it before declaring done.
- **`patch` tool fails silently on large HTML pages** when `old_string` is short or `new_string`/`old_string` get truncated in the call body (the tool's wrapper sometimes reports "path required" even with `path` set). Failure mode: 3-4 identical `error: path required` responses in a row. Recovery: switch to Python via terminal:
  ```bash
  python3 << 'PYEOF'
  with open('/var/www/html/arif/<path>') as f:
      h = f.read()
  if old_string in h:
      h = h.replace(old_string, new_string)
      with open(...,'w') as f: f.write(h)
      print('OK')
  else:
      print('NOT FOUND')
  PYEOF
  ```
  This is a tool-layer glitch (appears when the tool message crosses some size threshold), NOT a code problem. Don't blame the file — fall back to Python and move on.
- **Always verify HTML structure after multi-section edits.** Single-region string-replace edits that delete a closing `</section>` or `</div>` look fine in the patch diff but render as a parse-error or silently swallow the next section. After any non-trivial edit, run:
  ```python
  print(h.count('<section '), h.count('</section>'), h.count('<div'), h.count('</div>'))
  ```
  Both tag pairs must balance. If they don't, the LAST patch you applied is suspect — re-grep for the closing tag it should have removed.
- **Browser cache busting after deploy: the `?cb=` trick only works for URL-shaped caches.** When browser-side cache is the suspect (page loads but JS errors or stale data), the navigation cache key includes the URL fragment (`#engine`) and query but the browser may serve from disk cache anyway. Force a fresh load by appending a unique value that breaks prior caches: `?cb=forcefresh<epoch>` or a different number of query params. Symptom: `curl` shows the latest file but `browser_console` reports old errors — the browser is replaying an old JS state, not loading the new script. Solution: also clear in-memory state via `browser_console` evaluation, or use `browser_navigate` to a path with no prior cache hits (e.g., `?cb=99999`).
- **Don't chase external dependencies when content is the right answer.** Arif's correction (2026-08-08): *"Hang nak kawal benda bukan hidup buat apa. Kawal diri sendiri sudah."* When asked to "redo the world site map atlas with map tools" because the schematic SVG was ugly, the right answer was NOT to wire Leaflet + Carto dark-matter tiles + Nominatim geocoding (a 2-hour detour that would have added external dependencies to a page already designed to be self-contained). The schematic polygon map was a deliberate Korzybski choice ("the map is the lens, not the territory") — ugliness is not a bug. **Rule:** if a page already ships and renders its own data, do not pull in external tools to "make it look better." Audit the user's complaint: is it about data fidelity, visual quality, or control over something external? If control over external = the answer, the right move is to ship more content (essays, compass data, articles), not import more infrastructure. If in doubt, ask whether the user wants the schema rebuilt or the schema explained.
- **Caddy static routes for SPA-prefixed content have hidden paths.** When a SPA lives at `/world/makcikgpt/` (with `handle /world/makcikgpt/*` rewriting to `index.html` for browser fallback), the **static files** that the AI-bot handler serves live at `/var/www/html/arif/makcikgpt-md/<slug>.html` — NOT under `/world/`. Path pattern:
  - **Bot user-agent** (`@ai-bot-world` matcher): `/world/makcikgpt/<slug>/` → strip prefix → `/<slug>.html` → serve from `makcikgpt-md/`. Bot gets the static article.
  - **No-JS client** (`@makcikgpt_nojs`, `Accept` ≠ text/html): same path, served via `try_files {path}.html {path}.md`. No-JS gets `.md` if `.html` missing.
  - **Browser** (Accept text/html, no bot UA): SPA fallback to `/world/makcikgpt/index.html`. React renders the article client-side.

  **Bug class to check for:** if a URL pattern the user expects (e.g., `/world/makcikgpt/articles/<slug>/` — with a stray `/articles/` segment) has no Caddy route, it falls through to the SPA fallback and serves the generic landing page instead of the article. Diagnosis: `curl -sL <url> | grep -oE "<title>..."`. Fix: add a `path_regexp` redirect to canonicalize the legacy path. Insert it BEFORE any `handle /world/makcikgpt/*` block (first-match-wins ordering). After `caddy validate --config /etc/caddy/Caddyfile` and `systemctl reload caddy`, verify with `curl -sIL <test-url>` to confirm the 301 chain lands on 200.
- **Cloudflare can serve stale HTML even on 200 OK.** First load after deploy may show the OLD page for ~30s. Bust with `?cb=$(date +%s)` and the `Last-Modified` header tells you what the edge cached. After any major deploy, also verify with `browser_navigate` to a unique-cb path, not the canonical URL — the canonical URL hits cache first.

- **`/words/*` and `/work/*` are served from `/var/www/html`, NOT `/var/www/html/arif/`** (verified 2026-08-11). The Caddy handlers `handle /words/* { root * /var/www/html }` and `handle /work/* { root * /var/www/html }` use a DIFFERENT root than `@static_dirs`. Deploying to `/var/www/html/arif/words/<subpath>/` is a silent no-op — Caddy reads from `/var/www/html/words/<subpath>/`. Hit this with the `/constitution/` META rewrite (2026-08-11): patched `arif/constitution/index.html` but Caddy was serving from `words/constitution/index.html` (after the 308 redirect `/constitution/` → `/words/constitution/`). **Detection:** `curl -sL -o /dev/null -w "%{url_effective}\n" https://arif-fazil.com/<path>/` — follow ALL 308 redirects to find the canonical URL. Then `grep -A5 "handle <canonical-prefix>" /etc/caddy/Caddyfile | grep "root \*"` to find the actual root. Full webroot map: `references/caddy-webroot-map-2026-08-11.md`.

  **Concrete instance (verified 2026-08-11):** `/constitution/` 308-redirects to `/words/constitution/`, which Caddy serves from `/var/www/html/words/constitution/index.html` (NOT `/var/www/html/arif/constitution/index.html`). Editing the dist/ or `arif/constitution/` copies is a silent no-op — the live page lives at `/var/www/html/words/constitution/`. Same pattern applies to any `/<old-slug>/` that 308-redirects to `/words/<old-slug>/`: the file lives at `/var/www/html/words/<old-slug>/index.html`, not `/var/www/html/arif/<old-slug>/`.
  ```html
  <link rel="preconnect" href="https://api.fontshare.com" crossorigin>
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&f[]=cabinet-grotesk@400,700,800&display=swap" rel="stylesheet">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  ```
  Verified 2026-08-10: landing page `/words/` rendered with system fonts until these were added. Doctrine and Writing pages already had them — the inconsistency was invisible until `browser_console` font check exposed it.

## Live-data wiring (do not trust inline prose)

Market pages have TWO content layers:
- **Hardcoded "plain-language digest" prose** near the top (BM/EN paragraphs) — frequently STALE (said $4035.23 while live was $4,246). It does NOT auto-update. Verify against the API; if stale, strip it — the live hero below is the real content.
- **Live hero + chart** driven by `/_shared/zen-market.js` (defer) reading inline `window.ZEN_MARKET = {asset, label, apiBase, ...}`. It fetches:
  - `/{asset}/api/snapshot` → `ticker: {price, changePct, rsi, signal, confidence, ema20/50/200, emaTrend, pivot}`, `levels: {support[], resistance[], support_daily[], resistance_daily[]}`, `macro: {dxy, us10y, vix, silver, usmyr, ...}}`
  - `/{asset}/api/history?interval=1d&period=3mo` → `{candles[], ema20[], ema50[], ema200[], rsi[]}`
  - `/{asset}/api/apex` → `{G, C_dark, dS, verdict, price, rsi_14, atr_14, ...}`
- `<script id="wealth-reality-packet" type="application/ld+json">` = last sealed snapshot; offline fallback only, not live truth.
- KLCI backend can return `500 {"error":"snapshot: ticker unavailable"}` (yfinance feed) — transient; page still renders "Reading the market…".

### WEALTH public API gotchas (verified 2026-08-08)

The public snapshot endpoint at `https://wealth.arif-fazil.com/api/snapshot` is **hardcoded to oil** — `?asset=klci`, `?asset=usdmyr`, `?asset=fx`, `?asset=gold` all return oil data regardless of the param. The per-asset routes (`/gold/api/ticker`, `/oil/api/history`, etc.) are the only reliable source for non-oil assets. Same for `api/history` — its response is whatever was last cached, NOT routed by query param.

| Asset | Live ticker | Live history | Comment |
|---|---|---|---|
| Oil (XBRENT) | `/oil/api/ticker` ✅ | `/oil/api/history` ✅ | Canonical |
| Gold (XAU/USD) | `/gold/api/ticker` ✅ | `/gold/api/history` ✅ | Canonical |
| Gas (XNATGAS) | `/gas/api/ticker` ✅ | `/gas/api/history` ✅ | Canonical |
| KLCI | ❌ no endpoint | ❌ no endpoint | Page falls back to hardcoded `1,748.17` — live chart impossible without new service |
| USD/MYR | ❌ no endpoint | ❌ no endpoint | Page falls back to `open.er-api.com/latest/USD` — no historical series |

**Implication for the vitals page:** hero charts can only be wired for oil/gold/gas. KLCI and USD/MYR sections must remain card-only (or get a new Node.js service in `/var/www/html/arif/world/economics/klci/api/` mirroring the oil/gold/gas pattern — out of scope until Arif commits to it).

### `/world/vitals/` chart layout — chart-as-hero, NEVER collapsed

Arif's standing preference (2026-08-08): **the tradingview-style chart IS the hero of every instrument section**. Charts must be **always-open** (no `<details>` toggle) and **anchor the section before the narrative cards**. Collapsed charts read as "incomplete" to him.

Required pattern for any new instrument section:

```html
<!-- HERO CHART — always visible, before narrative cards -->
<div class="chart-widget-hero" id="chart-<id>"
     data-symbol="..." data-api=".../api/history" data-ticker=".../api/ticker"
     data-prefix="<prefix>" data-color="#hex" data-decimals="N" data-unit="$" data-title="...">
  <div class="chart-body">
    <div class="price-strip">
      <span class="big" id="<prefix>-price">---</span>
      <span class="delta" id="<prefix>-delta">---</span>
      <span class="hero-tag">HERO · ALWAYS OPEN</span>
    </div>
    <div class="chart-toolbar">
      <div class="tf-pills">
        <button class="pill" data-tf="1h" data-chart="<id>">1H</button>
        <button class="pill active" data-tf="4h" data-chart="<id>">4H</button>
        <button class="pill" data-tf="1d" data-chart="<id>">1D</button>
        <button class="pill" data-tf="1w" data-chart="<id>">1W</button>
      </div>
      <div class="ema-toggles">
        <button class="pill active" data-e="20" data-chart="<id>">20</button>
        <button class="pill active" data-e="50" data-chart="<id>">50</button>
        <!-- 200 only for gold -->
      </div>
      <span class="live-dot" style="margin-left:auto"></span>
    </div>
    <div class="chart-canvas" id="chart-<id>-canvas" style="height:420px"></div>
  </div>
</div>

<!-- THEN the narrative cards -->
<div class="grid g3" style="margin-top:24px">...</div>
```

JS contract — eager init on page load, NOT lazy on `<details>` toggle:

```js
document.querySelectorAll('.chart-widget-hero, .chart-widget').forEach(w => {
  const id = w.id.replace('chart-','');
  if (w.classList.contains('chart-widget-hero')) {
    initChart(id);                                       // render immediately
    const tf = w.querySelector('.pill.active[data-tf]')?.dataset?.tf || '4h';
    loadChartData(id, tf);
    tickPrice(id);
  }
  w.addEventListener('toggle', function() { /* legacy <details> support */ });
  // ... pill handlers, EMA toggle handlers
});
setInterval(() => {
  ['oil','gas','gold'].forEach(id => {
    const el = document.getElementById('chart-'+id);
    if (!el) return;
    if (el.classList.contains('chart-widget-hero') || el.open) tickPrice(id);
  });
}, 30000);
```

CSS for `.chart-widget-hero` is in the page's `<style>` block (chart at 420px height, no summary toggle, border-radius 8px, 1px var(--line2) border). Copy from existing oil/gas/gold widgets — DO NOT rebuild from scratch, the contract is fixed.

Verification after any chart layout change:
```bash
grep -c "<section " index.html    # opens
grep -c "</section>" index.html   # closes — must equal opens
grep -c "<div\b" index.html
grep -c "</div>" index.html       # must equal opens
grep -c "<details" index.html     # must be 0 in markup (only allowed in comments)
```
Then `curl -sIL "https://arif-fazil.com/world/vitals/?cb=$(date +%s)"` and `browser_console` for live price cells.

### SyedOS `/emas/` (gold chart) — recovered from git 2026-08-11, fully live

The SyedOS `/emas/` dashboard exists at `/var/www/html/syedos/emas/index.html` (~20 KB) — built on `lightweight-charts@4.2.0`, live gold + silver via `api.gold-api.com`, EMA20/50/200 toggle, RSI, S/R levels, BULLISH/SABAR verdict, TradingView-style chart. Verified live 2026-08-11 after the bulldoze-recovery incident (restored from git commit `6465d50`). Recipe + color system + hub pattern in `references/syedos-personal-surface.md`.

When rebuilt:
- Chart: `lightweight-charts@4.2.0` standalone. Live price: `https://api.gold-api.com/price/XAU` and `/price/XAG` (both free, no key — silver was previously hardcoded $31.2 while live ~$62).
- History: WEALTH `https://arif-fazil.com/gold/api/history?...` first, fallback Binance `fapi.binance.com/fapi/v1/klines?symbol=XAUUSDT` → `api.binance.com/api/v3/klines?symbol=PAXGUSDT`.
- Compute REAL indicators in JS from candle closes (Wilder 14-RSI, EMA20/50, swing-high/low S/R) — never fake with `price × 0.99`-style math.
- Known past bugs: `tfMap['4h'] = '1h'` silently showed 1H data; double-init (`DOMContentLoaded` + `readyState!=='loading'`) fired tick twice; S/R were fake percentage offsets; RSI was a tick-diff heuristic. Expose closes to the tick loop (`window.__lastCloses`) and re-run `tick()` after chart data loads, or indicators stay empty on first paint.

## Atlas / `/world/` landing page (live signal surface, Palantir-style)

The `/world/` index page (2026-08-08) was redesigned from a static Korzybski wireframe into a **Palantir-grade live signal surface**:

- **SVG world map** (720×360) with 14 schematic continent polygons + 14 pulsing hub dots
- **Hub color semantics:** red=supply (OPEC, Moscow), green=oil/demand (Brent, Shanghai), gold=sovereign anchor (KL/PETRONAS), teal=LNG (JKM), blue=capital (DXY), orange=mixed (NY/Henry Hub)
- **Scroll ticker** with live prices — BRENT, HH-NAT, GOLD — 60s loop animation
- **Dynamics strip** with 3 big-number cards: BRENT/GOLD/JKM + RSI thermostat bars (redraw on every tick)
- **Sidebar:** Macro stack (DXY/US10Y/VIX/MYR/GSR/KLCI), Sovereign Thermostat (4 sealed dials: RM82.8B cash, 70.5% extract, 85.2B CFFO, $71.60 FCF-zero), Signal Threads (8 rotating alerts every 7s)
- **Trade flow lines** (6 dashed paths between hubs, animated), scanline (vertical traversal every 4s), compass reticle, corner brackets
- **Placecard** on hub hover — node-specific place card with city/asset/metric, positioned via stage-relative scaling

Full anatomy, hub coordinates, CSS tokens, JS wiring, deploy recipe, and pitfalls: `references/world-atlas-live-page-2026-08-08.md`.

**Hard constraints** (verifiable from the live source):
- Single-file HTML (`/var/www/html/arif/world/index.html` ~38 KB), inline CSS+JS, vanilla SVG only
- No CDN libraries — CSP blocks (`script-src 'self' 'unsafe-inline'`); no D3/Chart.js/anything
- Schematic continents, NOT real-geo Mercator — Korzybski lens, not territory
- Old/baseline versions are at `index.html.bak-*` (20260806/07) — backup before any further patch
- During the 2026-08-08 redesign, a `/tmp/index-v1.html` was kept as the v1 backup

**Intent signals:** Arif asks for "atlas", "live map", "palantir", "world dashboard", "signals", or a redesign request on `/world/`.

## Verification loop (browser)

- `browser_snapshot` text often omits JS-rendered values — `browser_console` with `document.getElementById('pulsePrice').textContent` is the truth.
- Cloudflare edge can serve stale HTML even with `cf-cache-status: DYNAMIC`; bust with unique query `?cb=<epoch>` / `?nocache=x`.
- Visual proof for Arif: `browser_vision` screenshot → send `MEDIA:<screenshot_path>`.

## Transmission Engine visualization (ExxonMobil IR style)

Arif directive (2026-08-08): *"For the transmission engine trail slider, where is graph visualization to model that slider. Use ExxonMobil modeling toolkit if needed. Use all data visualization intelligence skills u have."*

The Layer 5 Transmission Engine (`#engine` section) in `/world/vitals/` now has a **2×2 grid of pure SVG sensitivity visualizations** above the sliders, redrawn live on every slider move. Zero dependencies (no D3/Chart.js — CSP-safe, no CDN). See `references/vitals-transmission-engine-viz-2026-08-08.md` for the full pattern.

| Panel | What it shows | Key fact |
|---|---|---|
| TORNADO | Per-slider ±1σ PAT impact bars | BRENT ±10 → ±RM6.0B (green), JKM ±4 → ±RM2.4B (teal), FX/Gold = 0 |
| WATERFALL | PAT → CFFO → −CAPEX → FCF → −DIV → RETAIN | Dashed connectors between stages |
| SURFACE | PAT isolines on (Brent, JKM) plane | ✕ = current position, 6 isolines |
| SCENARIOS | Bull $110 / Base $85 / Bear $55 PAT paths | 4-quarter trajectories, 3 polylines |

**Full reference:** see `references/vitals-transmission-engine-viz-2026-08-08.md` for the complete pattern (panel-by-panel layout, drawGrid return-value contract, the rename-scope pitfall, validation checklist).

Model: `PAT = 45.4 + (Brent−85)×0.6 + (JKM−14)×0.6` · `CFFO = PAT×1.88` · capex RM46B · div capped 60% PAT floor RM20B.

### Caddyfile reversion hazard — sibling agent/process overwrites your patch (verified 2026-08-10)

**Symptom:** You patch a Caddyfile handler (e.g., `/999/vault` to serve local JSON instead of `reverse_proxy 127.0.0.1:8088`). `caddy validate` passes, `systemctl reload caddy` succeeds, your live probe confirms the fix works. Then minutes later the handler is BACK to the old config and serving 22-second 112KB payloads.

**Root cause:** A sibling agent or build process re-applies the Caddyfile from a different source. Your patch hit the file at `/etc/caddy/Caddyfile`, but the rebuild process regenerates from somewhere else.

**Mitigation steps:**

1. **Always snapshot before patch:** `cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak-$(date +%s)` BEFORE any edit.
2. **Probe AFTER every reload:** `curl -s -o /dev/null -w "%{http_code}|%{size_download}|%{time_total}" https://arif-fazil.com/<path>` — check size and time, not just status. A 22s response with 112KB payload is the smoking gun for a reverted proxy hitting a slow upstream.
3. **Re-verify after 5 minutes:** If you're done with the session, probe again before declaring done. Sibling reverts can happen mid-session.
4. **Check `git -C /root/arif-fazil.com log --oneline -5`:** if a sibling committed Caddyfile changes recently, that's the revert source.
5. **Fix the SOURCE if it's git-tracked:** Check `ls -la /etc/caddy/Caddyfile` and `readlink -f /etc/caddy/Caddyfile`. The real SOT might be in `/root/arif-fazil.com/infra/` or `/root/AAA/infra/`. Edit THAT instead.

**Specific incident (2026-08-10 T2):** `/999/vault` was patched to serve local `vault-data.json` via `file_server`. Worked at first probe (1791 bytes, 82ms). Then sibling re-applied Caddyfile with `rewrite * /api/observatory/v1/snapshot; reverse_proxy 127.0.0.1:8088` — proxied to observatory snapshot which returns 112KB payload and takes 22s. Fix: re-applied the patch, verified with size+time probe.

### /999/ live surfaces — the observability stack (forged 2026-08-10)

The `/999/` constellation is the live-proof surface of the federation. Static HTML shells fetch JSON from Caddy-routed endpoints every 30s:

| Surface | Data source | Caddy wiring |
|---|---|---|
| `/999/health` | arifOS kernel `:8088/health` | `reverse_proxy 127.0.0.1:8088` with `rewrite * /health` |
| `/999/flow` | arifFlow `:7073/health` | `reverse_proxy 127.0.0.1:7073` with `rewrite * /health` (root returns error JSON — MUST rewrite) |
| `/999/vault` | local `vault-data.json` (cron-refreshed) | `file_server` + `root * /var/www/html/arif/999` + `rewrite * /vault-data.json` |
| `/999/verify` | arifOS kernel attestation | `reverse_proxy 127.0.0.1:8088` with `rewrite * /999/verify` |

**F1 rule:** every `/999/*` handler carries `import cors_public` + `header Cache-Control "no-store"` + 405 on POST/PUT/DELETE (read-only by construction — the kernel and vault are never mutated through the public surface).

**Vault freshness cron:** `vault-data-refresh` (cron id `2123bfc0a3bc`) runs `/root/HERMES/scripts/refresh-vault-data.sh` every 5 min — tails `outcomes.jsonl`, extracts `ts/event/actor/tool/session`, writes `vault-data.json` as www-data:www-data 644.

**Progressive enhancement pattern:** the `/999/` index.html and `/words/doctrine/` live-enforcement section both use `fetch('/999/...')` inside `setInterval(..., 30000)`. If the fetch fails, the cell shows `OFFLINE`/`—` — the static content never breaks. This is the "static-first, enhancement-after" pattern that /999/ extends.

### META-rewrite proposal workflow (verified 2026-08-11)

When the user signals a tone/audience change for a canonical page (e.g., "/constitution/ META is cult dialect — rewrite for outsiders"), the workflow is:

1. **Locate the LIVE file first.** Three things matter:
   - The canonical source under git (`public/<route>/index.html` or `src/data/<topic>/<slug>.ts`)
   - The dist/ copy under `sites/<site>/dist/<route>/index.html` (DERIVED, hand_edit=false)
   - The LIVE webroot path — this is where the broken `/words/*` webroot trap catches you (see `/words/* and /work/* are served from /var/www/html` pitfall above)

2. **Patch the source**, not the live webroot. Source goes through git, gets committed, and survives sibling rebuilds.

3. **Copy to live webroot** — both the obvious path AND the redirected-from path. Example for `/constitution/`:
   - `/var/www/html/arif/constitution/index.html` (the old path)
   - `/var/www/html/words/constitution/index.html` (the actual live webroot after 308 redirect)
   - Fix perms: `chown www-data:www-data ... && chmod 644 ...`

4. **Copy to dist/** if you want the change to survive the next build: `cp <source> sites/<site>/dist/<route>/index.html`

5. **Verify live** with both `curl -sL "https://arif-fazil.com/<path>/" | grep <new-marker>` AND `curl -sL -o /dev/null -w "%{url_effective}\n" "https://arif-fazil.com/<path>/"` to follow ALL redirects.

6. **Commit source change** — `git -C /root/arif-fazil.com add ... && git commit -m "fix(<route>): <description>"`. The commit message is the receipt that the change was deliberate, not a sibling accident.

7. **Mention the proposal artifact location** if it was created in `forge_work/proposals/hermes/.../`. Future audits will look there for the rationale — not just "what changed" but "why this change over the alternatives considered."

**Specific incident (2026-08-11):** Constitution META rewrite — caught cult-dialect F1-F13 jargon in title/description/keywords. Proposal at `forge_work/proposals/hermes/constitution-meta-rewrite/v1/META_PROPOSAL.md` with before/after table. Source patch in `public/constitution/index.html`. Dist copy in `dist/constitution/index.html`. Deployed to BOTH `/var/www/html/arif/constitution/index.html` (the obvious path) AND `/var/www/html/words/constitution/index.html` (the actual live webroot). Committed as `d427ef2`. Verified live: `https://arif-fazil.com/constitution/` → 308 → `/words/constitution/` → 200 with new META.

**Common pitfall:** Patching only the source (`public/`) without copying to dist/ AND live webroot. The source change survives in git but the LIVE site still serves the old META until the next `make deploy` (which copies public → dist → live via rsync). For a fast META fix, copy directly to both dist/ and live to avoid waiting for the next build.

- **DEEP ARCHIVE EXTRACTION — when user says "deep archive" / "previous design" / "aku x mau ni" / "what was deployed before" / "restore the old one" / "I hate it / ugly for human", extract the archived design from git AND filesystem backups and serve it locally for visual comparison (verified 2026-08-11 on `/world/makcikgpt/`).** DESIGN DRIFT INVESTIGATION above lists the archives; this pitfall completes the workflow — once you find the old commit, you need to SEE the old design to decide what to restore.

  **Why this matters:** A git log line tells you a file existed in commit X. It does NOT tell you what that file looked like, whether it had a hero, whether the chrome matched. To make a restoration decision you need visual proof of the old design, side-by-side with the current one. The only way to get that is to extract the file and render it.

  **Step 1 — Search ALL archive paths, not just git.** The richest archived designs often live OUTSIDE git history. Search these paths in order, biggest first (size is a signal — 105B = stub, >10KB = real content):

  ```bash
  # Path 1: Recent deploy snapshots (last 7 days)
  find /root/forge_work/deployments/arif-fazil.com/2026*/previous/ \
    -name "index.html" -size +2k | xargs -I {} sh -c \
    'echo "{}: $(stat -c%s {})B"' | sort -t: -k2 -nr

  # Path 2: Older backup archives (FORGOT — found rich 19,638B Primer Dark here on 2026-08-11!)
  find /root/backups/forge_work-archive-2026-07/deployments/ -name "index.html" \
    -size +2k | xargs -I {} sh -c 'echo "{}: $(stat -c%s {})B"' | sort -t: -k2 -nr

  # Path 3: Site-archival backups (e.g. /root/_archive/2026-08-04/backups/)
  find /root/_archive/ -name "index.html" -size +2k -path "*makcikgpt*" | \
    xargs -I {} sh -c 'echo "{}: $(stat -c%s {})B"' | sort -t: -k2 -nr

  # Path 4: Quarantined versions
  find /var/arifos/quarantine/ -name "index.html" -size +2k | \
    xargs -I {} sh -c 'echo "{}: $(stat -c%s {})B"' | sort -t: -k2 -nr

  # Path 5: Git history (last resort — only if filesystem archives fail)
  cd /root/arif-fazil.com && \
    git log --all --oneline -- "**/<path-or-glob>" | head -20
  ```

  **Size tells the story:** 105B = stub (the placeholder HTML that Caddy falls back to). 14KB = flat agent-friendly listing. 19KB+ = rich human-designed chrome. The `+2k` filter excludes 105-byte stubs so you only see real designs.

  **Step 2 — Extract candidate files verbatim.**
  ```bash
  mkdir -p /tmp/<archive-name>
  for c in <commit1> <commit2> <commit3>; do
      git show "$c:public/makcikgpt-md/index.html"   > /tmp/<archive-name>/$c-md.html     2>/dev/null || true
      git show "$c:sites/arif-fazil.com/makcikgpt/index.html" > /tmp/<archive-name>/$c-old.html 2>/dev/null || true
      git show "$c:sites/arif-fazil.com/public/makcikgpt-md/index.html" > /tmp/<archive-name>/$c-public.html 2>/dev/null || true
  done
  ls -la /tmp/<archive-name>/      # confirm which paths existed per commit
  ```

  **Step 3 — Serve locally on a temp port.**
  ```bash
  cd /tmp/<archive-name> && python3 -m http.server 8765 &
  sleep 2
  curl -sf -o /dev/null -w "HTTP:%{http_code} SIZE:%{size_download}\n" http://127.0.0.1:8765/<file>.html
  ```

  **Step 4 — Screenshot each version with `browser_navigate` + `browser_vision`.** Save to `/tmp/<archive-name>/screenshot-<commit>.png` so they survive eviction (see SCREENSHOT PROOF PROTOCOL above).

  **Step 5 — Build the side-by-side comparison table for the user.** Format: commit · path · hero · chrome · stats · footer · vibe. Show the actual screenshots via `MEDIA:/tmp/<archive-name>/screenshot-<commit>.png`. Let the user pick which version to restore.

  **Step 6 — Don't auto-restore.** Show all candidates + current. Wait for the user's choice. Restoration is `cp <chosen> /var/www/html/arif/<live-path>/` + chown www-data + chmod 644 + curl verify + browser_navigate. The `git show` extraction is READ-ONLY until the user picks.

  **Real example (this session, `/world/makcikgpt/`):** Found 3-stage regression — `696f734` (chat-interface persona, warm gold/brown) → `767596c` (Primer Dark marketing hero, RED/BLUE/YELLOW, hero+stats+series cards) → HEAD (flat agentic list, "Source of truth: src/data/essays.json. Rendered by scripts/..."). Extracted all three via `git show`, served each from a temp HTTP server, screenshotted each, sent side-by-side. User picked the Primer Dark version (post-audit `767596c`) as the restoration target. Full timeline in `references/makcikgpt-design-regression-2026-08-11.md`.

  **Pattern class — "agentic web optimization" regression.** Each stage of this regression replaced human-friendly chrome (hero, persona, pull-quotes, colored cards) with agent-friendly metadata (canonical landing path, source-of-truth file paths, generator script names, "WHERE AM I? / WHY CARE? / WHAT NEXT?" info boxes). The user's pain is the institutional chrome leaking to human readers. If a regeneration step removes human voice, that is a regression regardless of "improvements" to AI discoverability.

### Caddy wildcard redirect pitfall — `@static_dirs` and `handle_path` shadow custom regex handlers (verified 2026-08-11)

**Symptom:** You add a custom `path_regexp` handler with a wildcard like `@em_redir path_regexp ^/economics/makcikgpt/(.+)$` and `handle @em_redir { redir /world/makcikgpt/{http.regexp.em_redir.1} 301 }`. `caddy validate` passes, `systemctl reload caddy` succeeds. But probes still return 404. You try:
- `path` matcher with `*` wildcard
- `handle_path` with `rewrite` + `redir`
- `handle` with `uri strip_prefix` + `{uri}` placeholder
- Named captures `{re.slug}`, `{http.regexp.*.1}`
- Header `Location` + `respond "" 301`

All return 404 or empty body. None fire.

**Root cause:** `handle` directives in Caddy are tried in **source order**, BUT once a `@static_dirs path /economics/*` handler exists later in the file, AND a `handle_path /economics/*` exists between your handle and the static_dirs handler, the request gets caught by `handle_path` first — which has `@not_makcikgpt not path /makcikgpt /makcikgpt/*` BUT `not` on a path matcher doesn't exclude sub-paths of `/makcikgpt/*` reliably in all Caddy versions. The result: your wildcard handler is shadowed.

**The actual fix (the one that works):** Put the wildcard logic INSIDE the existing `handle @static_dirs { ... }` block OR use a top-level `redir` directive with the `path` matcher that runs BEFORE all `handle` blocks. The Caddy processing order is:

```
1. `redir` directives at top level of the site block (run FIRST, before any handle)
2. `handle` directives in source order
3. `handle_path` directives
4. `handle @static_dirs` (or any other named matcher handler)
```

So `redir` at top level is the only thing that ALWAYS beats `handle @static_dirs`. For dynamic captures (article slug), you need:

```caddyfile
# 2026-08-11: Wildcard legacy MakcikGPT redirects — TOP-LEVEL bare redir.
# Bare redir runs BEFORE all handle blocks including @static_dirs.
# For simple fixed targets, this is the ONLY reliable pattern:
redir /economics/makcikgpt/* /world/makcikgpt{uri} 301
```

BUT `{uri}` includes the matched prefix, so for `/economics/makcikgpt/cerita-makcik` the redirect becomes `/world/makcikgpt/economics/makcikgpt/cerita-makcik` (wrong).

**The actual working pattern:** put the regex redirect INSIDE `handle @static_dirs { ... }` block:

```caddyfile
# Inside handle @static_dirs { try_files ... =404; file_server }
# Add at the TOP of the block, BEFORE try_files:
@legacy_makcikgpt path_regexp ^/(economics|wealth)/makcikgpt/(.+)$
rewrite @legacy_makcikgpt /world/makcikgpt/{http.regexp.*.2} 301
```

Or simpler: use Cloudflare page rules for legacy URL redirects if the Caddy regex handlers consistently misfire. Cloudflare rules run at the edge BEFORE Caddy, so they're immune to handler ordering issues.

**Lesson learned the hard way (2026-08-11):** spent 6 iterations on this. The pattern is: **when `path_regexp` handlers in a site block don't fire, it's because another handler (likely `handle_path` or `@static_dirs`) with a broader path matcher is catching the request first.** The reliable fix is one of:

1. Move the redirect logic INSIDE the catching handler (at the top, before try_files).
2. Use Cloudflare edge rules (immune to Caddy handler ordering).
3. Restructure the Caddyfile so the wildcard handler is in a separate vhost (rare, heavy).

NEVER assume a `handle` block will fire just because it's defined earlier in the Caddyfile. Always verify with a live probe and check the actual response body — `caddy validate` passing does NOT mean the handler fires.

### Bare landing path pitfall — `handle /path/*` does NOT match bare `/path/` (verified 2026-08-11)

**Symptom:** You land on `/world/makcikgpt/` (no slug, bare landing). The page renders but is essentially blank — a 1043-byte stub with `<h1>MakcikGPT Landing</h1>` and no CSS. The 24 articles on the corpus work fine; only the bare landing is broken. External probe finds it and reports "empty white".

**Root cause — five patterns that ALL require content after the prefix:**

```caddyfile
# 1. Bot handler — pattern requires at least one char after *
@ai-bot_world {
    path /world/makcikgpt/*  ← * requires content; bare path = NO MATCH
}
# 2. No-JS handler — regex requires at least 1 char
@makcikgpt_nojs path_regexp ^/world/makcikgpt/(.+)$  ← (.+) requires content
# 3. Trailing-slash handler — requires slug + trailing slash
@mk_trail path_regexp ^/world/makcikgpt/([^/]+)/$  ← [^/]+ requires content
# 4. Wildcard handle — * does not match empty path
handle /world/makcikgpt/* {  ← * requires content
# 5. Even the @static_dirs handler with /world/makcikgpt/* has the same constraint
```

For `/world/makcikgpt/` (bare, no slug after), all five handlers MISS. The request falls through to the SPA fallback stub.

**Fix — explicit bare-path handlers placed BEFORE the wildcard:**

```caddyfile
# Bare landing paths need their OWN handle block — * doesn't match empty.
# Place BEFORE handle /world/makcikgpt/* so first-match-wins applies.
handle /world/makcikgpt {
    uri strip_prefix /world/makcikgpt
    root * /var/www/html/arif/makcikgpt-md
    header Cache-Control "public, max-age=300"
    try_files /index.html =404
    file_server
}
handle /world/makcikgpt/ {
    uri strip_prefix /world/makcikgpt
    root * /var/www/html/arif/makcikgpt-md
    header Cache-Control "public, max-age=300"
    try_files /index.html =404
    file_server
}
# THEN the wildcard for slugs
handle /world/makcikgpt/* { ... }
```

**Detection recipe — sweep for the same pattern on other hubs:**

```bash
# For each hub landing, check if bare /world/<hub>/ returns real content or shell
for hub in vitals economics makcikgpt politics; do
  size=$(curl -s -o /dev/null -w "%{size_download}" "https://arif-fazil.com/world/$hub/")
  echo "/world/$hub/ → ${size}B $([ $size -lt 5000 ] && echo '⚠️ SUSPECT shell' || echo '✓ real content')"
done
# Repeat for /words/<hub>/, /propa/, /malaysia/, etc.
```

**Lesson:** When adding a new hub to the constellation, you need THREE handler blocks, not one:
1. `handle /hub` — bare landing
2. `handle /hub/` — bare landing with trailing slash
3. `handle /hub/*` — slugs (does NOT match the bare landing)

### Caddy insertion location trap — Python patch can target wrong handle block (verified 2026-08-11)

**Symptom:** Your `python3 << PY` script replaces a snippet in the Caddyfile correctly (e.g., `@api_organs_arifos` block). Then you do `c.replace(target, insert)` to add a new handle block right after the matched snippet. **But if your `target` anchor string is inside another `handle` block, your insertion goes INSIDE that block too** — and everything breaks (all routes start returning 404 or 500).

**Concrete incident (2026-08-11):** Replaced `import cors_public` (the @api_organs_arifos handler marker) with the @wm_legacy/@em_legacy handle blocks + `import cors_public`. But `import cors_public` appears 56 times in the Caddyfile — the FIRST occurrence was inside `@api_organs_arifos`, so my new handle blocks landed INSIDE that block. Result: `/api/organs/arifos/health` returned 404 AND `/wealth/makcikgpt/<slug>` returned 404 because the whole handler chain got poisoned.

**Mitigation:**

1. **Always use UNIQUE multi-line anchors.** Single-line targets like `import cors_public` will match the first occurrence — usually not where you want to insert.
2. **Verify the insertion point with `sed -n 'N,N+10p'` BEFORE the patch** — read the surrounding lines to confirm you're inside the right scope.
3. **Reload Caddy IMMEDIATELY after the patch and probe ALL known routes** — if any previously-working route breaks, the insertion went into the wrong block. Revert and re-target.
4. **Keep Caddy backups BEFORE every patch:** `cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak-$(date +%s)`.

**Recovery if it breaks:** `cp /etc/caddy/Caddyfile.bak-<timestamp> /etc/caddy/Caddyfile && caddy validate && systemctl reload caddy && verify with curl`.

### Dark subdomain + SPA catch-all pattern (verified 2026-08-11)

**Two related DRIFTs from external probe:**

**DRIFT #1 — Empty webroot + missing root handler:**
```caddyfile
wealth.arif-fazil.com {
    root * /var/www/html/wealth
    # ... other handlers for /mcp, /api, etc.
}
```
If `/var/www/html/wealth/` has no `index.html`, the subdomain returns 404 on `/` even though `/api/...` works. Fix: either add `index.html` (minimal landing), or `redir / https://arif-fazil.com/wealth/<reason> 308` to redirect to the canonical surface.

**DRIFT #4 — SPA catch-all serving shell on garbage routes:**
```caddyfile
geox.arif-fazil.com {
    root * /var/www/html/geox
    handle /mcp { reverse_proxy ... }
    # ... other handlers
    # NO final handle that fail-closes
}
```
Result: any path not caught by the named handlers falls through to `file_server` on the root dir, which serves `index.html` (the SPA shell) on every garbage route. External probe found `geox.arif-fazil.com/garbage-route-8f3k2` → HTTP 200 with shell content.

**Fix:** Add explicit fail-closed at the END of the vhost block:
```caddyfile
handle {
    respond "404 Not Found" 404
}
```

This catches all unhandled routes and returns honest 404 instead of serving the SPA shell. Same fix applies to any subdomain with mixed static + reverse_proxy routing.

### External witness probe pattern (verified 2026-08-11)

When auditing the live site, run an **external probe suite** with raw status codes + deviation math, NOT just "does curl return 200". The 10-probe matrix that caught the 4 DRIFTs:

| # | Probe | Pass criterion |
|---|---|---|
| 1 | All hub surfaces (`/`, `/words/`, `/earth/`, `/world/`, `/work/`, `/999/`, `/000/`) return 200 with sane sizes | HTTP 200 + 1KB < size < 100KB |
| 2 | `/000/` and `/999/` return real static docs (not SPA shells) | `size > 10KB` AND distinct `<title>` |
| 3 | `/oil/`, `/gas/`, `/gold/` JSON-LD prices within ±2% of live market | `\|sealed - live\| / live < 0.02` |
| 4 | Legacy redirects (`/economics/makcikgpt/*`, `/wealth/makcikgpt/*`) → 301 to canonical | `curl -sI <path> \| grep -i location` shows canonical URL |
| 5 | Unknown routes → real 404 (not SPA shell) | `curl -s <random-path> \| head` does NOT show SPA content |
| 6 | `feed.xml` article count matches sitemap | `grep -c '<item>' feed.xml == grep -c '<loc>' sitemap.xml` |
| 7 | `llms.txt` organs list matches `soul.json` | both enumerate same 5 organs |
| 8 | `/api/public-state` signed + fresh (timestamp < 5 min old) | `signature_state: SIGNED` AND `ts_utc` recent |
| 9 | MCP `POST /mcp initialize` returns valid JSON-RPC result | HTTP 200 + `result.protocolVersion` populated |
| 10 | Canonical redirects work (`/federation` → `/doctrine`) | 301 with correct Location header |

Verdict format per probe: `🟢 PASS` or `🔴 DRIFT` with specific failure detail. Aggregate verdict at the top: "6 PASS · 4 DRIFT — seal is NOT clean".

This pattern catches things internal agent audits miss because:
- It measures response **size** (112KB instead of expected 1.8KB = proxy regression)
- It measures response **time** (22s instead of 100ms = shadow handler firing)
- It probes from outside (catches Cloudflare edge cache, DNS routing)
- It includes deviation math for stale data (`/oil/` sealed 84.53 vs live 87.18 = 3.04%)

### UA-differential debugging — same path, different responses per UA (verified 2026-08-11)

**Symptom:** You curl `/world/makcikgpt/` → 200 / 15KB with the real landing page. Arif's browser hits the same URL → 404 (empty body). Both responses show `cf-cache-status: DYNAMIC` so Cloudflare isn't caching differently. Live page works for some clients, broken for others.

**This is the worst kind of bug** — your probes say "fine", user's reality says "broken", and there's no obvious explanation. Run the differential matrix BEFORE guessing.

**The 7-UA differential probe:**

```bash
URL="https://arif-fazil.com/<suspect-path>"
for ua_label in "CURL_DEFAULT" "MOZILLA_MAC" "MOZILLA_WIN" "MOZILLA_LINUX" "IPHONE_SAFARI" "EMPTY_UA" "PYTHON_URLLIB"; do
  case $ua_label in
    CURL_DEFAULT)     ua="curl/8.14.1" ;;
    MOZILLA_MAC)      ua="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" ;;
    MOZILLA_WIN)      ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" ;;
    MOZILLA_LINUX)    ua="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" ;;
    IPHONE_SAFARI)    ua="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" ;;
    EMPTY_UA)         ua="" ;;
    PYTHON_URLLIB)    ua="Python-urllib/3.10" ;;
  esac
  result=$(curl -sI "$URL" -H "User-Agent: $ua" -H "Accept: text/html" 2>/dev/null | grep -iE "^HTTP|content-length" | head -2 | tr '\n' ' ')
  printf "  %-15s %s\n" "$ua_label" "$result"
done
```

**Pattern recognition from this matrix:**

| UA pattern | Likely cause |
|---|---|
| All UAs → 200 | Genuine edge cache miss; user problem is browser-side |
| Only `curl/<ver>` → 200, all others → 404 | **Caddy handler order** — `@ai-bot-world` matcher shadows other handlers; handler chain terminates at the 404-producing block for non-bot UAs |
| Only `Mozilla/Chrome/Safari` → 200, `curl` → 404 | Cloudflare Super Bot Fight Mode blocking perceived bots |
| Only `Mozilla` with `Accept: text/html` → 404 | **`@makcikgpt_nojs` matcher** with `not header_regexp Accept text/html` — request WITHOUT that Accept is treated as a no-JS client and routed to a static path that doesn't exist for bare landings |
| All UAs → 404 | Genuine missing file or broken handler for everyone |

**The 2026-08-11 incident:** `curl/8.14.1` → 200 / 15KB; all other UAs → 404 / 0 bytes. `cf-cache-status: DYNAMIC` on both. Cause: a `handle /world/makcikgpt/` block at line 936 rewrote to `/spa-shell.html` (file doesn't exist on disk) → Caddy returns 404 for everyone. But curl UA matched `@ai-bot-world` (the matcher includes `curl` in its UA regex) AND fell through to a different handler that served real content. The two UAs took completely different paths through the handler chain.

**Diagnostic next steps after the matrix:**

1. **Identify which handler is producing the 404.** `caddy adapt --config /etc/caddy/Caddyfile --pretty > /tmp/caddy.json` then `grep -B2 -A20 '/suspect/path' /tmp/caddy.json` to see the actual handler chain. Walk the JSON to find which `try_files` or `file_server` is the terminal handler.
2. **Check Cloudflare trace** — `curl -s "https://arif-fazil.com/cdn-cgi/trace"` to see colo, IP, and confirm the request reaches origin. If `cf-cache-status: DYNAMIC` and `cf-ray` is present, Cloudflare passed through to origin — the divergence IS in Caddy.
3. **Check browser cache on the user's side** — if all probes return 200 from server but user sees 404, the user has stale browser cache. Tell them to hard-refresh (`Cmd+Shift+R` / `Ctrl+Shift+R`) and clear site data for the domain.
4. **Test direct-to-origin** — `curl -sk "https://127.0.0.1/<path>" -H "Host: arif-fazil.com" -H "User-Agent: Mozilla..."` to bypass Cloudflare entirely. If this returns 200, Cloudflare is the divergence source; if 404, Caddy is.
5. **Check sibling agent activity** — `git -C /root/arif-fazil.com log --oneline -10 -- sites/arif-fazil.com/public/` and `journalctl -u caddy --no-pager -n 30` for recent changes that might have reverted your work.

**Lesson:** Never declare "fixed" after a single curl probe. The matrix above is 30 seconds of work and catches UA-specific routing bugs that single-probe testing misses entirely. Add it to your standard post-deploy verification for any landing-page change.

### Critical JS scoping pitfall (verified 2026-08-08)

`drawGrid` returns its inner `<g>` SVG group. Callers store it as `const root = drawGrid(...)`. Then `root.appendChild(...)` adds chart elements. **BUT `drawGrid` also uses `g.appendChild(...)` internally to attach grid lines/text to the same group.**

The bug: a blanket `.replace('g.appendChild', 'root.appendChild')` across the entire viz block also rewrote `drawGrid`'s internal calls → `root is not defined` (root is only in the outer scope).

**Rule:** when renaming a variable across a JS block, scope the replacement to function boundaries:
```python
# WRONG — blanket replace breaks inner function
block = block.replace('g.appendChild(', 'root.appendChild(')

# RIGHT — scope to drawGrid only
start = html.find('function drawGrid(')
end = html.find('\nfunction drawTornado(', start)
drawGrid_func = html[start:end]
drawGrid_func = drawGrid_func.replace('root.appendChild(', 'g.appendChild(')
# outer scope stays root.appendChild
```

Then validate: `node --check <script_content>`.

## Trading-context answers (Arif)

Arif trades XAU/USD actively and watches silver/DXY/USD-MYR/KLCI. When he asks about entries ("bila boleh buy"), give **concrete trigger levels** (pullback to EMA20/50 zone with 4H close above, or breakout 4H close above R1 with stop beyond R2) — never indefinite "SABAR". Verdict vocabulary: SABAR / WATCH / HOLD / OVERBOUGHT. Always live-probe his dashboards' feeds before quoting numbers to him. See `references/gold-macro-context.md` for the current gold narrative.
## Recovery recipes (when design breaks — 2026-08-11 lessons)

These are step-by-step recovery recipes for the failure modes that recur. Run them BEFORE reinventing a fix.

### Recipe 1: "I just bulldozed a site" (recovery from empty/stub webroot)

```bash
cd /var/www/html/<site>/
# 1. NEVER trust the live webroot alone — check git SOT first
git log --oneline -10              # what's the canonical history?
git status                         # any uncommitted diffs?
git ls-tree -r HEAD --name-only    # WHAT EXACTLY IS IN GIT?
ls -la                            # what is deployed right now?

# 2. If git ls-tree shows files that ls -la doesn't → live is behind. Recover:
git checkout HEAD -- .             # restore canonical files
chown -R www-data:www-data /var/www/html/<site>/
chmod 644 /var/www/html/<site>/*.html /var/www/html/<site>/**/*.html
chmod 755 /var/www/html/<site>/*/

# 3. Verify all routes still serve:
for path in / /path1/ /path2/; do
  curl -s -o /dev/null -w "$path → %{http_code} · %{size_download}B\n" \
    "https://<domain>$path?cb=$(date +%s)"
done
```

### Recipe 2: "The design looks wrong / drifted from before"

```bash
# 1. Find what the canonical version is
TARGET="/var/www/html/arif/<surface>/index.html"
echo "=== Live size ==="
stat -c%s "$TARGET"

# 2. Find archived versions
find /root -name "index.html" -path "*<surface>*" 2>/dev/null \
  | xargs -I {} sh -c 'echo "$(stat -c%s {})B — {}"' | sort -nr | head -10

# 3. If an archive is LARGER and RICHER, ask Arif: "Found archived design from <date>, <size> bytes — restore this?"

# 4. Restore from the chosen archive (modify paths and counts as needed):
ARCHIVE="/root/.../previous/<surface>/index.html"
python3 -c "
import re
with open('$ARCHIVE') as f: html = f.read()
# Update slug paths, counts, dates — see specific surface for transforms
with open('$TARGET', 'w') as f: f.write(html)
"
chown www-data:www-data "$TARGET"
chmod 644 "$TARGET"
curl -sI "$TARGET" | grep -i last-modified
```

### Recipe 3: "I changed a design, sibling agent reverted it"

```bash
# 1. Check if sibling reverted via journalctl or git
journalctl -u caddy --no-pager -n 20  # recent Caddy reloads
git -C /root/arif-fazil.com log --oneline -5 -- <path>  # recent commits

# 2. If sibling reverted YOUR work, re-apply and lock with metadata comment
# (sibling agents don't intentionally revert — they overwrite via stale filesystem copy)

# 3. ALWAYS re-probe after 5 minutes:
sleep 300 && curl -s "<your-url>" -H "User-Agent: Mozilla/5.0" | grep <your-marker>
```

### Recipe 4: "Browser shows 404 but curl returns 200" (UA mismatch)

```bash
URL="https://arif-fazil.com/<suspect-path>"
for ua in "CURL" "MOZILLA_MAC" "IPHONE" "EMPTY" "PYTHON"; do
  case "$ua" in
    CURL) agent="curl/8.14.1";;
    MOZILLA_MAC) agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36";;
    IPHONE) agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1";;
    EMPTY) agent="";;
    PYTHON) agent="Python-urllib/3.10";;
  esac
  echo "=== $ua ==="
  curl -sI "$URL" -H "User-Agent: $agent" -H "Accept: text/html" 2>&1 | grep -iE "^HTTP|content-length" | head -2
done
# If curl gets 200 but others get 404, Caddy handler is bot-UA-matched
```

### Recipe 5: "Article returns ARTICLE NOT FOUND in browser" (SPA bundle miss)

```bash
SLUG="<article-slug>"
# 1. Check static file exists
ls -la /var/www/html/arif/makcikgpt-md/<slug>.html
# 2. Check SPA bundle registration (browser-rendered)
grep -c "$SLUG" /var/www/html/arif/index.html  # 0 = not registered
# 3. If SPA bundle misses the slug, Caddy static-first fix should serve the static HTML
#    Verify with REAL browser (not curl):
curl -sfL -A "Mozilla/5.0" "https://arif-fazil.com/world/makcikgpt/$SLUG/" -o /tmp/test.html
wc -c /tmp/test.html  # Should be >2000 bytes
grep "<h1" /tmp/test.html | head -1  # Should have article title, NOT "Article Not Found"
```

### Recipe 6: "Sovereign explicitly asked to redesign, but I don't know which design"

When Arif says "design is ugly, find the archive, restore" — this is a multi-archive archaeology task. Do NOT assume newest = best. Do NOT pick a design without showing him.

```
1. Run archive archaeology (Rule -2 above)
2. List 2-3 candidate designs with their distinguishing features:
   - File size + date
   - Color palette
   - Has canvas/JS animation? (fragile) or pure HTML? (stable)
   - Article count at time of archive
3. Show screenshots or curl evidence to Arif
4. Wait for his explicit "go" before restoring
```

**Meta-rule:** Arif is the F13 sovereign. When in doubt, SHOW options and ASK. Never auto-choose between design variants. The cost of asking is one message; the cost of wrong choice is rebuilding his trust.

---

## Memory anchors for future agents (post-2026-08-11)

When you load this skill, also load these memory facts:
- **MakcikGPT canonical landing design:** 19,638-byte archive from 2026-07-31 (rich red/blue/yellow palette with hero canvas). NOT the 14,074-byte degraded GitHub-dark version. Live path: `/var/www/html/arif/makcikgpt-md/index.html`.
- **Article pattern:** `/words/writing/` and `/world/makcikgpt/<slug>/` share the same chrome pattern (ARIF FAZIL top bar → breadcrumb → kicker section-label 2 baris → h1 italic uppercase → subtitle → byline pills → tag pills → body → footer).
- **arifOS federation ports live:** 8088 (kernel), 7071 (forge), 3001 (AAA), 8081 (GEOX), 18082 (WEALTH), 18083 (WELL), 7073 (arifFlow).
- **MakcikGPT article source-of-truth:** `/var/www/html/arif/makcikgpt-md/<slug>.html` (live) — there is NO .ts source in `src/data/makcikgpt/` for most articles. They are direct-written static HTML, not SPA-rendered.
- **Caddy static-first fix (2026-08-09):** All browsers get static HTML from `makcikgpt-md/`, NOT the SPA shell. SPA fallback only triggers if static file missing.
- **Ditempa bukan diberi** is non-removable from any arif-fazil.com surface.

DITEMPA BUKAN DIBERI — Forged, not given.
