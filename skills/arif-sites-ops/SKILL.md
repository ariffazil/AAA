---
name: arif-sites-ops
description: Operate arif-fazil.com — add/route pages, deploy through the arif-sites pipeline (build → verify-pages gate → deploy-site.sh), diagnose dead URLs (Caddy matchers vs missing files).
---

# arif-sites-ops

Operating the arif-fazil.com Ψ human surface: how pages are served, how to add one, the deploy gate, and 404 diagnosis.

## Current rule (2026-10-13, wins over later copy-paste)

Later `caddy reload`, `systemctl reload caddy`, `make deploy`, `deploy-site.sh --apply`, and `rsync -a dist/ /var/www/html/arif/` are historical scars. Live vhost file is `/etc/caddy/vhosts/arif-fazil.com.conf`. `/etc/caddy/Caddyfile` only imports vhosts. Ship with `arifos-site-patch-without-caddy-reload`: additive per-route, `rsync -av --update` of new assets, no `--delete`, no reload. A full-tree rsync without `--delete` still overwrites live-only HTML. Count live HTML that names a hashed file the new dist lacks. `--delete` only after that count is zero. On 2026-10-13 that count was 74. Re-count. August 5-lane nav, `/propa/` paired with `/malaysia/`, sitemap loc counts, and "a deploy will fix it" are REPORTED August. October front door is nine rooms. `/propa/` 301s to `/vitals/`. `/malaysia/` 308s to `/wealth/malaysia/`. Do not reverse those redirects. Do not edit Caddy. Queue is `/root/work/tasks.json`.

## Human-First Doctrine (LEAD — applies to ALL arif-fazil.com surfaces, 2026-08-11)

**Arif, verbatim:** *"The sites must be bijaksana dan genius and more clarity, serve human first for human cognitive limit and then we do all agentic backend as needed for future agentic web."*

The correct priority order when designing or auditing any landing page, hub, or major surface:

1. **Human first.** Cognitive fit trumps machine extractability. A page that machines love but humans can't navigate is failure.
2. **Agentic backend second.** Machines serve humans — they don't replace them. LLMs/agents crawl to UNDERSTAND content so they can serve users who land later.
3. **Both layers fail-closed.** If a tired human at 2am can't navigate the page, it's broken regardless of how structured its JSON-LD is. If a search crawler can't extract the headline, it's invisible regardless of how pretty it looks.

### The "served" test — apply before deploying any landing page or hub

1. **Human at 2am test:** Can a tired human, looking at this on a phone in the dark, find what they came for in 10 seconds?
2. **Agent at scale test:** Can a search crawler or LLM scraper extract the headline, the 5 most important facts, and the navigation in one pass?
3. **Sovereign at noon test:** Can Arif (the human sovereign) open this URL, glance at it for 30 seconds, and say "yes, this is what I wanted"?

If any answer is "no" — the surface is broken. Patch before deploy.

### Cognitive-fit rules (apply BEFORE the existing deploy-gate discipline)

| Filter | Rule | Failure mode |
|---|---|---|
| **≤7±2 navigation choices** | Miller's Law. More than 9 competing choices at once = paralysis. Group, paginate, or hide. | Visitor bounces |
| **≤3 accent colors per page** | Red + gold + blue max. More = circus. White/grey/dark for hierarchy. | Visual noise |
| **First 100px = human anchor** | Above the fold: brand + nav + breadcrumb + kicker + h1 + lede. NO status codes, F-codes, organ acronyms, "888 JUDGE", "intelligence kernel", SEAL/HOLD/VOID stamps. | Visitor feels like they're reading audit logs |
| **Status metadata in FOOTER, not header** | Byline + date + tags + read-time + provenance go BELOW body. Header is the attention anchor — first thing human eyes + LLM extractors see. | Identity drowns content |
| **Lead with verb, not noun** | "Read the analysis" not "Analysis Page". "Latest words" not "Writing". Cards are actions, not items. | Page feels like a directory |
| **One question at a time** | Page answers WHERE AM I? / WHY CARE? / WHAT NEXT? within 3 seconds. Don't dump 8 stats before the hero. | Cognitive overload |
| **No jargon leaking to public** | F-codes, organ acronyms, "intelligence kernel" — INTERNAL only. Public surfaces: plain language. | Visitor feels locked out |
| **Footer always carries "Ditempa bukan diberi"** | Sovereign identity mark. Removing it = F13 violation. | Identity loss |
| **No auto-playing media** | Animation OK if `prefers-reduced-motion` respected. Audio/video autoplay = accessibility violation. | Accessibility failure |

### When human-first conflicts with machine-extractable

| Conflict | Resolution |
|---|---|
| `<title>` must be plain-language (human) but extractors want metadata | Use `<meta name="description">` for machine, `<title>` for human. Both serve same content via different surfaces. |
| Status badges belong in footer by human-first rule, but extractors scan header | Put badges in BOTH header chrome (small, mono) AND footer (full). Human glances; machine reads top-down. |
| Plain language conflict with formal taxonomy | Public surface: plain. Discovery surfaces (`/llms.txt`, JSON-LD): formal. Two-tier discipline. |

## Architecture map (probe live before trusting prose)

| Layer | Path | Role |
|---|---|---|
| SPA source | `/root/arif-fazil.com/sites/arif-fazil.com/src/` | React Router app: routes in `App.tsx`, pages in `src/pages/` |
| Static shells | `.../public/<route>/index.html` | content-first no-JS pages; `public/_redirects` = clean-URL rewrites |
| Build | `npm run build` = prebuild generators → `tsc -b` → `vite build` → postbuild `scripts/copy-static-html.js` (mirrors `public/*` → `dist/*`) | `dist/` is DERIVED, never hand-edit |
| Registry | `infra/runtime-overlays.json` | site defs, webroot names, preserve-live overlays (`static/wealth.html`, `data/wealth`) |
| Deploy | `scripts/deploy-site.sh <site> --dry-run \| --validate-build \| --apply \| --restore <tag>` | atomic swap + rollback + JSON receipt |
| Live webroot | `/var/www/html/arif/` (site `arif-fazil.com`, webroot `arif`) | what Caddy actually serves |
| Caddy | `/etc/caddy/Caddyfile` | matcher order: `@static_dirs` → `handle /words/*` / `handle /work/*` → `@agent_shells` → `@spa_routes` → SPA fallback. **Key exceptions:** `/words/*` and `/work/*` use `root * /var/www/html` (NOT `/arif/`); `/999/verify`, `/999/health`, `/999/flow` are reverse-proxied; `/` is static-first (zero React bundle). Full map: `arif-fazil-web-ops/references/caddy-webroot-map-2026-08-11.md`. |
| Gate | `scripts/verify-pages.sh` (a.k.a. `make verify-pages`) | probes every `dist/*/index.html` against live site; any gap → **HOLD** |

## Diagnosing a dead URL (case: /pm-bayang/)

A path can be registered in Caddy yet still 404 when the **file was never built** (intent/execution gap). Trace in this order and report which layer is missing:

1. `curl -sL -o /dev/null -w "%{http_code}" https://arif-fazil.com/<path>/`
2. `grep -n "<path>" /etc/caddy/Caddyfile` → which matcher catches it, what `try_files` it runs
3. `ls /var/www/html/arif/<path>/` → live webroot
4. `ls sites/arif-fazil.com/dist/<path>/` → build output
5. `ls sites/arif-fazil.com/public/<path>/` → static shell source
6. `grep -n "<path>" sites/arif-fazil.com/src/App.tsx` → SPA route

Fix options: build the static shell (`public/<path>/index.html` → rebuild → deploy), 301 redirect (`public/_redirects`), or remove the Caddy matcher.

## Adding a page (the sanctioned path)

1. Build in proposal zone first: `forge_work/proposals/<agent-id>/<mission>/` (file-authority.yaml is FAIL-CLOSED; `public/**/*.html` = DERIVED, `src/**` = CANON).
2. For a static shell: put `index.html` (+ assets) in `public/<route>/`, `npm run build` → mirror lands in `dist/<route>/`.
3. For a Vite sub-app: set `base: '/<route>/'`, build, copy `dist/*` (index.html + assets/) into `public/<route>/`.
4. Gate: `bash scripts/verify-pages.sh` — must pass. Pre-existing gaps: declare them, don't silently bypass.
5. `scripts/deploy-site.sh arif-fazil.com --dry-run` only. `--apply` is T3. Ship the one route with additive rsync, no `--delete`. Verify live. Receipt in `receipts/<agent-id>/`.
6. Backup before replacing a live page: keep `index.html.bak-*` in place.

## User doctrine (Arif)

- **"Dont simply replace. I Want upgraded"** — upgrading a page preserves its existing content (e.g. MakcikGPT sections on /world). Never wholesale-replace a page with content.
- **Alignment before deploy** — "Hang Check dulu segala benda allligned": verify the change fits the existing pipeline (SPA routes, mirrors, Caddy, overlays) before applying.
- Deploy signals: "X deploy lagi" = HOLD; "Nak deploy Roger" / "deploy ja la bila Ready" = green light.
- Voice-to-text typos are constant — interpret semantically, search the repo for the artifact FIRST, ask once max.
- **Top-bar brand = "ARIF FAZIL" exactly**, no suffix. Stated: "I prefer. ARIF FAZIL". `font-display` serif italic, white, links to `/`.
- **Every article gets the byline footer** (user-mandated, fixed format — full template in `references/essay-makcikgpt-mirror.md`):
  ```
  Muhammad Arif bin Fazil
  Geoscientist · Architect, arifOS · Petronas Carigali · UW–Madison '13
  Penang, Malaysia
  Published: <date> · Direct Publication · /words/ context
  Epistemic Tag: INT — <one-line description of epistemic scope>
  Pairs with: <correct cross-link to other articles in the same series>
  ```
  Plus the DITEMPA BUKAN DIBERI footer block ("Forged, not given") with /words/, MakcikGPT, Doctrine, /feed.xml, llms.txt, missions.json, surfaces.json, agent notice.
- **Cover block IS the attention anchor.** "The first section is very important, that's where human attention is the highest. Same with ai llm." Kicker → h1 → lede → byline row → tags must all be above the fold; never bury metadata below. For LLM extraction, the first 150 chars of `<meta description>` and the visible H1 are what gets surfaced.
- **Minimal header chrome (HARD RULE, Arif's explicit instruction 2026-08-07).** Article page header = top bar (ARIF FAZIL brand) + breadcrumb + kicker + h1 title + lede excerpt + hr. NOTHING ELSE. The "By Arif Fazil" pill, "Sealed 999" pill, date pill, read-time pill, and tag pills all live in the FOOTER byline block — not the header. (Arif: "Remove this at header of the articles and make it as footer.") Rationale: header is the attention anchor for humans AND LLMs — both extract metadata from the first section above the body. Cluttering the header with chrome steals attention from the actual article content. The footer (where attention lingers before scroll-out) is the right place for identity metadata. Build/regenerate order: write the body, then header chrome (top bar + breadcrumb + kicker + h1 + lede + hr), then FOOTER byline block (pills row + identity block + site footer). Never reverse — putting chrome in the footer first leads to re-pasting it at the top.
- **Header-chrome audit recipe (verified 2026-08-07).** When the user says "remove X from header / put it in footer", the safe way to confirm clean separation is a script audit, not visual inspection:
  ```bash
  # Header section = between <header class="flex" and <article
  for slug in $(ls /var/www/html/arif/words/writing/ | grep -v _shared); do
    h=$(awk '/<header class="flex/,/<article /' "/var/www/html/arif/words/writing/$slug/index.html" | grep -cE "By Arif Fazil|Sealed 999|<date>|min read")
    printf "%-50s header_chrome=%d (want 0)\n" "$slug" "$h"
  done
  ```
  Plus the dual check: `f=$(grep -c "Muhammad Arif bin Fazil" <page>)` should be ≥ 1 (footer has the byline). The audit pattern catches both directions of the contract: header is empty, footer carries the identity.
- **Parallel rebuild pipeline for essay surface (verified 2026-08-07).** If the writing surface needs a rebuild, sequence it: (1) extract `.ts` source body, (2) build the HTML head + cover chrome, (3) build the article body with series-aware `<h2>` styling, (4) build the byline footer block with the cross-link map, (5) write the live + source-mirror in one pass. Do NOT run subagents on `public/words/` in parallel — see "Parallel subagents collide" pitfall below.
- **Pairs-with is content-derived, not arbitrary.** For each series: every article links to the OTHER articles in the same series, not to itself, not to unrelated content. Triptych: 3 articles, each pairs with the other 2. S6 Eureka Trilogy: each pairs with the other 2 EUREKA papers. S8 Forge: 4 articles, each pairs with the other 3. Wrong pair-with is worse than no pair-with — it breaks the cross-link graph that holds the canon together.
- **Never paraphrase his vocabulary.** "BANGANG and stupid is different meaning" — his exact words are the only acceptable words; register changes meaning. When he flags a term, propagate the correction to every page + essays.json + llms.txt + .ts source. Title correction propagation chain: `.ts` `title:` field → `<h1>` → `<title>` meta → meta description → essays.json → index cards → llms.txt.
- **Vocabulary integrity is a hard veto on "improvement".** Arif's words carry BM register, Malaysian English, and philosophical precision that generic English flattens. "BANGANG" carries the makcik register and a specific failure-state meaning — flattening it to "stupid" loses both. When the user pastes a term, use that term verbatim in the title, in `<h1>`, in cross-links, in pull-quotes. If a later task tempts you to "improve" or "normalize" any word in his essay, leave it. The only legitimate edit is when Arif explicitly asks for a substitution — and even then, propagate to every surface (`.ts` source, essays.json, llms.txt, index cards, footer blocks, articles-annotated.json) in one pass.
- **Content must be his words, verbatim.** He rejected pages twice in one session because subagents added invented quotes (Hannah Arendt's "banality of evil"), fabricated references, and rewrote sections. **Zero tolerance:** no invented citations, no embellishment, no added analysis attributed to him. The full guard below — read before any essay-publish.

## Pitfalls

### Archive archaeology (BEFORE any landing-page or major-surface mutation, verified 2026-08-11)

**The single biggest cause of design drift on arif-fazil.com is agents writing to live without first checking archive.** Multiple design versions of the same surface exist across:

- `/root/forge_work/deployments/arif-fazil.com/<TS>/previous/<path>` — per-deploy snapshots, file sizes tell design age
- `/root/backups/forge_work-archive-2026-07/deployments/arif-fazil.com/<TS>/previous/<path>` — older monthly archives
- `/root/_archive/2026-08-04/backups/...` — pre-reconciliation snapshots
- `/var/www/html/makcikgpt-md.removed-20260811/` — quarantine directory
- git history (`git log --all --oneline -- <path>`)

**Mandatory pre-flight sequence:**

```bash
TARGET="/var/www/html/arif/makcikgpt-md/index.html"
echo "=== Live ==="
ls -la "$TARGET"

echo "=== Archived copies (sorted by file size = design age) ==="
find /root /var/www -name "index.html" -path "*makcikgpt*" 2>/dev/null \
  | xargs -I {} sh -c 'echo "$(stat -c%s {})B — {}"' \
  | sort -t: -k1 -nr | head -10

# If multiple versions exist, compare file sizes:
#   LARGEST = most design investment (richer CSS, more JS, animation)
#   SMALLEST = stub or degraded
# Pick the design Arif wants — ASK if ambiguous (do NOT assume "newer = better")
```

**Verified incident 2026-08-11:** `/world/makcikgpt/` was live-served at 14,074 bytes (degraded GitHub-dark palette), while archives held 19,638 bytes (rich red/blue/yellow palette with hero canvas). After "deep archive extraction" Arif chose the 19,638-byte design as canonical.

**Use the canonical script:** `scripts/detect-design-drift.sh` runs the archaeology and lists candidates with sizes/dates/colors.

### Pitfalls

- `/_shared/design-system/tokens.css` is runtime-resolved — build warning "doesn't exist at build time" is expected and harmless.
- Don't hand-edit `dist/` or `public/**/*.html` (DERIVED) — patch the source SPA or proposal zone, rebuild.
- Overlays `static/wealth.html` + `data/wealth` are cron-owned preserve-live — a deploy must never clobber them (deploy-site.sh handles via registry).
- The SPA routes in `App.tsx` only execute when Caddy falls through to the SPA; static shells in `public/` win for matching paths.
- `/world/` served a static landing while the SPA `WorldArrow.tsx` route is dead weight — check which layer is actually winning before editing.

### CSP iframe trap (verified 2026-08-09)

Pages with YouTube/Vimeo/iframes render blank because the Caddy Content-Security-Policy
blocks external frames. Symptom: HTML serves fine (HTTP 200), page renders, but iframe
is missing from DOM entirely (0 iframes found via JS inspection). Root cause: CSP header
has `frame-ancestors 'self'` but no `frame-src` directive.

**Fix:** Add `frame-src` to the CSP in `/etc/caddy/Caddyfile`:
```
Content-Security-Policy "...; frame-src https://www.youtube.com https://www.youtube-nocookie.com; frame-ancestors 'self'; ..."
```
Caddy reload is T3. Do not run `sudo systemctl reload caddy`. Verify: browser inspect shows iframe with
`src="https://www.youtube.com/embed/..."` and Play button visible.

**Pattern:** When adding ANY external embed (YouTube, Vimeo, Spotify, Twitter/X),
always add the corresponding `frame-src` domain to CSP BEFORE deploying.

### Path-root trap (verified 2026-08-06)

Siblings pastes of "this directory is missing" are often **wrong-path** claims. arif-fazil.com has two slightly different roots and it bites:

```text
/root/arif-fazil.com/                       ← repo root (contains sites/, dist/, public/ etc.)
/root/arif-fazil.com/sites/arif-fazil.com/  ← site root (the one you want)
.../sites/arif-fazil.com/src/               ← SPA React source
.../sites/arif-fazil.com/public/<route>/    ← static shells (source-of-truth)
.../sites/arif-fazil.com/dist/<route>/      ← build output (mirrors public/* via copy-static-html.js)
/var/www/html/arif/                         ← LIVE webroot (what Caddy serves)
```

When asked "where is /000 source?" the **correct** probe is:

```bash
ls /root/arif-fazil.com/sites/arif-fazil.com/public/000/   # ← NOT /root/arif-fazil.com/000/
```

If the source is at `public/000/`, it WILL exist. The sibling that said "source directory missing, only dist/000/ is present" had looked at `sites/arif-fazil.com/000/` (without `public/`) and was wrong. Always state the full 4-segment probe path when reporting "missing source."

### Constitution-root surfaces: /000 + /999

Two pages have non-standard properties — they ARE constitutional artifacts, not ordinary site pages.

| Page | Role | Special wiring |
|---|---|---|
| `/000/` | Genesis · Sovereign Anchor | Caddy `handle /000 { try_files /000/index.html }` + assets |
| `/999/` | Proof · Sealed Vault | Caddy `handle /999 { try_files }` + **`/999/verify` is REVERSE-PROXIED to 127.0.0.1:8088** (live arifOS kernel JSON, not a static file under `/var/www/html/arif/999/verify*`) |
| `/genesis/` | Alias | `redir /genesis/* /000/ 301` |
| `/verify` (root) | Kernel attestation | `handle /verify { rewrite * /verify/index.json file_server }` (separate from /999/verify) |

Edits to /000+ files should never be appended live without a signature re-issuance — `genesis-statement.sig` is currently a literal `PLACEHOLDER_SIGNATURE_BASE58` placeholder (F2 TRUTH violation, real defect, adversary-discoverable via `curl`). Edits to /999/*.json should advance `generated_at` if the underlying data has moved; `/999/verify` is the only /999 artifact driven by kernel state and is always fresh.

See `references/constitution-surfaces-000-999.md` for full file inventory, the placeholder-sig trap, three encoding paths to fix it, the /999/verify reverse-proxy mechanism, and the patch discipline (one problem, one patch per session).

### Deploy pipeline — three paths, two gates (verified 2026-08-07)

`make deploy` is **not** the same gate as `make verify-pages`. The full chain:

```text
make deploy
  → verify       (verify-surfaces.cjs → verify-pages.sh → verify-content.sh → caddy validate → dist dev-only scan)
  → sync-aaa     (rsync /root/AAA/dist/ → sites/arif-fazil.com/dist/aaa/)
  → build        (8 prebuild generators + tsc + vite + render-propa + inject-panel + generate-discovery)
  → verify-pages (content gate, runs again)
  → reload       (HISTORICAL. caddy validate + systemctl reload caddy is T3. Do not run.)
```

`verify-surfaces.cjs` is the **strictest** gate — it reads `surfaces.json` and
probes every entry. It fails on legacy paths that 308 after the 5-lane reorg,
even when the heroes are already live from manual rsync. As of 2026-08-07, 13
surfaces fail: `/economics/`, `/writing/`, `/doctrine/`, `/999/`, `/oil/`,
`/gas/`, `/gold/`, `/propa/`, `/malaysia/`, `/politics/shadow/{,board/,derita/}`,
`/pulse/`.

Decision: if your day's work is small content edits and `make verify-pages`
PASSES but `make deploy` fails at `verify`, it is almost certainly **catalog
drift, not your problem**. Use the manual rsync path and report the catalog
drift as a separate day's work. Do NOT patch `verify-surfaces.cjs`.

See `references/deploy-pipeline-vs-verify-pages.md` for the full decision tree,
probe recipes, and the 2026-08-07 reproduction.

### Surfaces.json trust gap — verify-pages is content-thin (verified 2026-08-07)

`make verify-pages` asserts HTTP 200 only. **It will pass for stale content**
if the file exists at the expected path. Hit twice on 2026-08-07:

1. `/world/` had live `3809 B` content (old 10-item nav, no hero). After patch
   + rsync, live went to `9026 B`. But between rsyncs the src had been silently
   reverted by a `git checkout` event (git-tracked file). When `curl`'d live
   after deploy, the gate had reported PASS on what was stale content.
2. `/words/` and `/work/` showed new hero on one probe, stale hero-core glyph
   on a later probe — same gate PASSED both times.

**Mitigation:** after every content deploy, manually grep the live page for a
unique marker:

```bash
for r in /words/ /world/ /work/; do
  printf "%-12s marker=" "$r"
  curl -s "https://arif-fazil.com$r" | grep -oE "your-marker"
done
```

If the marker is missing, the patch didn't reach the live webroot — diff is
between `sites/arif-fazil.com/dist/<route>/` and `/var/www/html/arif/<route>/`.

### surfaces.json doctrine-introspection drift (verified 2026-08-06)

`surfaces.json` has a `doctrine` field that describes itself. The doctrine claims
**"64 surfaces"** but the file has **70**. The doctrine was not bumped when surfaces
were added. This is the §16 trap from `verify-nested-sibling-reports` — the
canonical file contradicts itself.

**Also:** the doctrine promises routes `/human/map/` and `/machine/map/` as generated
views. Live probe: `/human/map/` returns 200 ✓, `/machine/map/` returns **404**.
The same doctrine promises `fail_closed: "Any status:live surface returning non-200
fails the build."` But the build is green — because `/machine/map/` is not in
`dist/*/index.html`, it's a doctrine-promised route that was never wired.

**Also:** `sitemap.xml` serves only **42 `<loc>` entries** vs 70 in `surfaces.json`.
Either 28 surfaces are sitemap-excluded or the sitemap is stale.

**Probe recipe before citing surfaces.json in any audit:**

```bash
# 1. Count doctrine claim vs actual data
python3 -c "
import json
d = json.load(open('/root/arif-fazil.com/surfaces.json'))
print('doctrine title:', d['doctrine']['title'][:80])
print('surfaces list:', len(d['surfaces']))
"

# 2. Probe doctrine-promised routes
for r in human/map machine/map; do
  echo -n "/$r/: "; curl -s -o /dev/null -w "%{http_code}\n" https://arif-fazil.com/$r/
done

# 3. Cross-check sitemap coverage
echo "sitemap locs: $(curl -s https://arif-fazil.com/sitemap.xml | grep -c '<loc>')"
echo "surfaces.json: $(python3 -c 'import json; print(len(json.load(open("/root/arif-fazil.com/surfaces.json"))["surfaces"]))')"
```

**Two clean fixes (T1, reversible):**
1. Bump doctrine title from "64 surfaces" → "70 surfaces".
2. Either wire `/machine/map/` to serve `/root/arif-fazil.com/public/machine/map.json` (file already exists) via Caddy rewrite, or remove from doctrine.

See `references/world-atlas-data-sources.md` for the SOT Atlas data recipes (GDELT, World Bank, countries dataset, map geometry) and SOT math.

## Anatomy of a failed gate pass (session 2026-08-06)

3 broken pages surfaced by verify-pages: `/oil/world/`, `/gas/world/`, `/world/sot/`. All pre-existing routing gaps — files exist in `dist/` but Caddy hasn't served them because the live webroot was out of sync. The gate probes live state, so it fails before deploy. This is a chicken-and-egg: the gate blocks deploy because the live site is old; deploy would fix the gaps. **Respect the gate — fix the gap sources, don't patch the gate script.**

The real question is always: **is the URL registered in Caddy, and does the file exist?** If yes to both and it's still 404, the live webroot is stale — a deploy will fix it. If no file source exists, that's an intent/execution gap (the `/pm-bayang/` pattern: Caddy route registered in Caddyfile, `public/` directory never created).

**Pre-existing Caddy orphan patterns (verified 2026-08-06):** `/oil/world/` and `/gas/world/` return 404 indefinitely because no Caddy route catches them but `public/oil/world/index.html` (etc.) exists from an earlier agent build. These are NOT routing bugs to fix during routine deploys — they are pre-existing surface surfaces. `verify-pages.sh`'s `INTENTIONAL_EXCLUSIONS` list is for surfaces you don't intend to serve; these two are *unintentional* orphans. The verbiage in `verify-pages.sh` reports them as `✗ 404` but does NOT block deploy when other paths you built pass. **Trust the gate's status summary, not individual page checks.** The final `VERDICT: HOLD` line is what blocks deploy, not the individual ✗ lines.

## When the sibling already built the artifact

Before scaffolding a duplicate, always grep the repo for the existing build. The "WB Tire" / "Staford" / "NYBSite" mentions can refer to a sibling CodeX/333-AGI build that already lives in `public/<route>/`. Pattern: `find /root/arif-fazil.com/sites/arif-fazil.com/public -type d -name '<keyword>*'` first. Two parallel builds → wasted entropy, broken gate.

## Editing an existing static shell — git-tracked vs untracked (verified 2026-08-07)

`public/<route>/index.html` is served **directly by Caddy** from `/var/www/html/arif/<route>/index.html`.

**For untracked shells** (e.g. `public/words/`, `public/work/` — committed dirs
don't yet exist in git): normal flow — edit src, `npm run build`, `rsync
dist/<route>/ /var/www/html/arif/<route>/`, verify.

**For git-tracked shells** (e.g. `public/world/index.html`, committed in a9404d5):
the postbuild mirror step + `git checkout` events can both revert your
`write_file` mid-session. Verified 2026-08-07 on `/world/` — the src had reverted
between the `write_file` and the rsync. Workaround that works:

```bash
# 1. Write directly to the live webroot FIRST
cat > /var/www/html/arif/<route>/index.html << 'EOF'
... new content ...
EOF

# 2. Mirror src/dist to keep them aligned (do this BEFORE next `npm run build`)
cp /var/www/html/arif/<route>/index.html \
   /root/arif-fazil.com/sites/arif-fazil.com/public/<route>/index.html

# 3. Verify live has the patch — curl + grep for unique marker
curl -s https://arif-fazil.com/<route>/ | grep -oE "your-marker"
```

Check track-status with `git -C /root/arif-fazil.com ls-files sites/arif-fazil.com/public/<route>/index.html`.

### Verify the live engine, not just the HTML

After deploying a static shell with an inline `<script>` engine, **`curl` is not enough**. The HTML is server-rendered but the engine runs client-side. To prove the engine actually works on the live page:

1. `browser_navigate` to the URL.
2. `browser_console` → assert no JS errors.
3. `browser_console` → assert the engine elements exist and have the expected default values:
   ```js
   JSON.stringify({
     canvas: !!document.getElementById('pv-canvas'),
     defaultBrent: document.getElementById('pv-brent')?.value,
     defaultVerdict: document.getElementById('pv-verdict')?.textContent,
   });
   ```
4. Programmatically dispatch a slider event and assert the readout updates:
   ```js
   document.getElementById('pv-brent').value = 85;
   document.getElementById('pv-brent').dispatchEvent(new Event('input'));
   // assert verdict changed
   ```
5. `browser_vision` → screenshot for layout / overlap / readable verdict colour.

Without step 4 you don't actually know the engine works — only that the HTML parses without throwing.

## Cross-organ coupling (the multi-page live edit)

When two sovereign organs need to refer to each other (e.g. `/propa/` = PETRONAS institutional pulse, `/malaysia/` = federal sovereign pulse), they are **structurally coupled** — high oil on one side becomes subsidy-driven stress on the other. To make this coupling legible without building a SPA-level integration:

1. **Pick the shared subsystem** (e.g. subsidy paradox) and give it one canonical anchor name: `<section id="subsidy-paradox">` on **both** pages.
2. **Bidirectional anchor cross-links** in plain `<a href="/<other-route>/#subsidy-paradox">See the <other-side> paradox on /<other-route>/ →</a>` — both directions, with the same anchor label so the cross-link is scannable.
3. **Nav canon update** — add the cross-route link to the `<div class="zp-nav">` block on each page if it isn't already there. The /malaysia/ page gained `<a href="/propa/">PETRONAS</a>` as a nav link so the coupling is reachable from the global header, not only in-body.
4. **Distinct accent colours per page** — `/propa/` uses navy+gold (corporate identity); `/malaysia/` uses red (sovereign identity). The cross-link callout on each page uses **the destination page's accent colour** so the reader visually knows which page they're being sent to. /propa/'s "see /malaysia/" callout uses `var(--accent)` which on /propa/ is gold; on /malaysia/'s "see /propa/" callout uses `var(--accent)` which on /malaysia/ is red.
5. **Charts in `_charts/` subfolder per route** — keeps them co-located with the page they serve. Caddy serves them with the rest. Each page's charts are PNG via matplotlib, named `S01_<topic>.png` etc., distinct from PDF-report charts to avoid namespace collisions.
6. **Single shared data point, two framings** — the corporate page shows the corporate binding constraint (60% cap × RM20B floor × subsidy bill); the sovereign page shows the sovereign binding constraint (debt/GDP, deficit/GDP, subsidy bill). The shared data is the subsidy bill; each page derives its own consequence.

Proven 2026-08-06: `/propa/` and `/malaysia/` coupled via subsidy paradox + 3 charts each + 1 cross-link each + 1 nav link. All HTTP 200. `verify-pages` passed 117/117.

## MakcikGPT architecture — three-layer routing (updated 2026-08-09)

MakcikGPT articles are **NOT** on the SPA essay pipeline. They live in a flat
corpus: `/var/www/html/arif/makcikgpt-md/<slug>.html` (+ optional `<slug>.md`).
Caddy routes three paths:

| Path | Handler (live) | What it serves |
|---|---|---|
| `@ai-bot-world` (bot UA) | `root makcikgpt-md/` → `try_files {path}.html {path}.md =404` | Static article `.html` directly |
| `@makcikgpt_nojs` (no text/html Accept) | Same root, `.md` fallback | Markdown mirror |
| `/world/makcikgpt/` (landing) | `try_files /makcikgpt-md/index.html /index.html` | Landing page index |
| `/world/makcikgpt/*` (article via browser) | `try_files /makcikgpt-md{path}.html /makcikgpt-md{path}/index.html /index.html` | Static article FIRST, SPA shell FALLBACK |

**Critical: the landing page handler was changed from `rewrite * /index.html` to `try_files /makcikgpt-md/index.html /index.html`** (line ~836). Before this change, the landing always served the SPA React shell instead of the static index — a fresh deploy broke the landing page navigation entirely. The article handler uses `try_files` to prefer `.html` over `/index.html` so direct-write articles work in browsers without SPA registration.

Before 2026-08-09 fix: browsers got "ARTICLE NOT FOUND" because Caddy routed ALL browser traffic to the SPA shell, and the SPA didn't know the slug. Bots worked fine via `@ai-bot-world`. After fix: `try_files` checks for the static `.html` first, falls back to SPA only if no static file exists. Zero SPA registrations needed anymore.

The landing page is a hand-authored static HTML file at `/var/www/html/arif/makcikgpt-md/index.html`. It has two lists: a visible grouped-by-series section (collapsible `<details>`) and a hidden `ul.flat-list` for RSS readers. Both must be updated when adding a new article. Use dates `YYYY-MM-DD` format, ascending within each series. Cross-list articles in every applicable series.

**Publish steps:**
1. Write `<slug>.html` (self-contained inline CSS — copy the style block of an existing article).
2. `chmod 644` — root-owned 600 files won't serve.
3. Verify (7-gate): HTTP 200 · `<title>` present · unique body markers grep ≥1 · zero author-name leakage · landing page still 200 · sibling articles still 200 · served size sane.
4. Canonical URL = **no trailing slash** (`/<slug>/` 301s to `/<slug>` — harmless; probe without).

**⚠️ ROLE SEPARATION — do not become the deploy debugger (user-mandated, 2026-08-09).**
Arif, verbatim: *"Hang x boleh pakai untuk fix website"* and *"Website tu aku suruh
agent lain fix la."* When asked for a MakcikGPT article: **write it → verify ONCE
(single curl round) → hand over canonical URL + file path.** Do NOT spend the session
rewriting Caddy handlers, rebuilding the landing index, or chasing permissions on this
corpus — a site-ops agent owns it and concurrent rebuilds WILL wipe your work. Listing
the article on the landing page is also the site-ops agent's job; hand over slug +
one-line description and stop.

**Concurrent-rebuild hazard (verified 2026-08-09):** another agent rebuilt
`makcikgpt-md/` mid-session — a live article vanished with no error anywhere. When the
user reports "article not found", FIRST probe is `ls -la /var/www/html/arif/makcikgpt-md/<slug>.html`.
Gone → re-write once, verify once, move on. Do not deep-dive Caddy routing.

**Protected surfaces (locked 2026-08-09):** Landing page and critical index files
are protected with `chattr +i` (Linux immutable flag). Any agent attempting to
overwrite them gets `Operation not permitted`. Deploy guard pattern:

```bash
# DEPLOY PATTERN — unlock → deploy → verify → lock
chattr -i /var/www/html/arif/makcikgpt-md/index.html   # unlock
# ... deploy new content ...
# ... verify live ...
chattr +i /var/www/html/arif/makcikgpt-md/index.html   # lock
```

Known-good backups exist as `<filename>.known-good` alongside the locked file.
To restore: `cp index.html.known-good index.html && chattr +i index.html`.

**This protection exists because:** an agent replaced the landing page with a
generated version without asking. The user's feedback: "No maaf. Improve the
system. Maaf saja x Dak guna." — meaning: don't apologize, build safeguards.
The system should prevent the mistake, not rely on the agent choosing correctly.

**MakcikGPT persona guard (F2 + virality):** articles are authored by the "MakcikGPT"
voice — never attribute to Arif by name (he said explicitly: "jangan letak nama aku,
letak persona makcikgpt" — his name doesn't travel, the persona does). Voice rules:
opens "Makcik nak tanya/cerita…", everyday analogies (kedai runcit, kebun getah),
`.makcik-fact` red/teal number boxes, closing *"Enjin melapor. Manusia yang putuskan."*
Never soften his register words ("BANGANG" stays). See `templates/essay-makcikgpt-mirror.html`.
**CRITICAL voice correction (Arif 2026-08-09):** "Ni bahasa accounting la weiii. Cakap macam makcik kampung."
MakcikGPT articles MUST NOT use accounting/financial jargon. Translate all financial concepts through
village-auntie analogies: kedai runcit (small shop), beli stok/jual barang (buy stock/sell goods),
basuh berak pakai air bukan tisu (wash with water not tissue = circular economy), kebun getah (rubber estate).
For landing page structure: see `references/makcikgpt-landing-page-template.md`.

## Tripwire proposal pattern (proposing a new tripwire on a sealed page)

When the analysis reveals a NEW tripwire the existing sealed anchors didn't cover (e.g. the v2 subsidy paradox demanded a 10th tripwire):

1. **Don't mutate the sealed composite pulse.** Sealed = sealed. The new tripwire is *additive* and *proposed*.
2. **Add a `[NEW TRIPWIRE PROPOSAL · F13 sign-off pending]` section** on the page, not inside the tripwire grid. The sealed grid stays intact; the proposal sits as a new section with full parameter table (id, metric, threshold, safe anchor, engagement action, FY25/FY26 values, status = PROPOSAL).
3. **Spell out F13 sovereignty** — "awaiting F13 sovereign veto per F13 sign-off protocol". This makes it explicit that only the human can promote it to sealed.
4. **State the contrast** — "would not have engaged at FY25 anchors but would engage at FY26 anchors" so the reader sees why the new tripwire matters now and didn't before.
5. **Reference it in the live proxy / methodology section** as "10th tripwire, PROPOSAL" so the fact that it's pending shows up in machine-readable metadata too.

This keeps the seal honest (nothing was unsealed retroactively) while letting the analysis surface what the seal missed.

## Live interactive model on a static shell (the v2→v3 upgrade pattern)

When the user pushes back on static charts ("why u do so many static graph? Baked that into the model slider"), the right move is to bake the analysis dimensions into the existing slider engine rather than add more images. The pipeline:

1. **Python source-of-truth + JS port.** Build a pure-function library (no side effects, no I/O) at `forge_work/<project>/<lib>/model.py`. Every function: deterministic, units in the docstring, defaults match the sealed page anchors. JS port at `<lib>.js` mirrors the Python exactly — both expose the same API surface.
2. **Cross-validate in Node.** After writing both, run a small Node script that loads the JS and asserts each output matches the Python output for a fixed parameter set. This catches JS translation errors that look like "model is wrong" in production but are actually "I mistyped the piecewise slope in JS":
   ```js
   const fs = require('fs');
   global.window = {};
   eval(fs.readFileSync('v3-engine.js', 'utf8'));
   const V3 = global.window.PetronasV3;
   // assert V3.sub(p) === expected for each case
   ```
3. **Bake into the slider HTML.** Replace the static-chart section with `<input type="range">` sliders (5–10 of them), a `<canvas>` chart, and a readout panel that updates on every `oninput`. Math runs in JS; chart re-draws; verdict text + colour updates; tripwire badge flips STANDBY→ENGAGED on threshold cross.
4. **Default-state neutrality rule.** The page's initial slider values must NOT open in the worst-case verdict (red PARADOX badge on first paint). Anchor defaults at a *comfortable* state (e.g. Brent $65, Iran war 0%, reform delay 0mo) so the user *discovers* the paradox by dragging the Brent slider up. The BULL/BASE/BEAR preset buttons can still load extreme states — that's user-initiated, not the default.
5. **Verify in a real browser.** After deploy, run `browser_navigate → browser_console` and assert:
   - `document.getElementById('pv-canvas')` exists with non-zero width
   - Default slider values render a non-PARADOX verdict
   - Programmatically dispatching `new Event('input')` on a slider updates the readout text within the same frame
   - No JS errors in console
6. **Remove the static charts.** Once the live model is wired, delete the old `<img src="/propa/_charts/S0X_*.png">` tags. Verify with `grep -c '_charts/S0' <served-html>` — should be zero. The model is the chart now.

Pitfall: the new sliders will collide with existing slider IDs from the page's old fan engine (e.g. `brent` vs `pv-brent`). Namespace everything in the new engine — pick a 2-letter prefix (`pv-`, `mv-`) and use it for all IDs in the live model section.

## When the user asks "did the collapse date move?" — verify against the published model table

Sharper diagnosis ≠ faster timeline. The published Bear crossover is 2027; the published Base case has no crossover through 2031. If the new analysis added a paradox framing but didn't change the cash-flow model, the dates haven't moved. Always verify against the published assumption table before answering.

Probe recipe:

```bash
# 1. Pull the actual scenario rows from the live HTML
grep -B1 -A3 "Net-debt crossover year\|net-debt crossover" \
     /root/arif-fazil.com/sites/arif-fazil.com/public/propa/index.html

# 2. Check for any new model code paths since last seal
grep -E "firstCross|crossover" <page> | head

# 3. If only narrative changed (v2 added subsidy paradox as new section),
#    the corporate net-debt timeline is unchanged
# 4. If the model itself changed (new cost terms, new break-even),
#    re-run the cash-flow model and update the table
```

The hidden-tell: if the user remembers "2026 for Base" but the published Base row says "none <2031", they're conflating a *decision* date (cap-floor collision = a board must decide) with a *collapse* date (net-debt crossover). The cap-floor collision is a real time pressure — it doesn't trigger Bear crossover math. Different events on the timeline.

## Do NOT remove old engine state when layering a new engine on the same page

When v2 added the subsidy paradox to `/propa/`, the existing 6-slider fan engine (year-by-year net-cash path with net-debt crossover) was still the live net-cash projection. The v3 upgrade added a NEW slider engine *for the paradox dimensions* — but kept the fan engine untouched.

On `/malaysia/` the v3 upgrade put the new slider engine *first* (live paradox is the main feature) and folded the old 2-slider fan inside a `<details class="zen-reveal">` collapse ("Old: sovereign PULSE fan · Brent + MYR only") so it's still reachable but doesn't dominate the page.

Pattern: **add the new engine prominently, demote the old engine to collapsed/labelled "legacy" state, don't delete**. Deleting the old engine breaks any URL fragments or live-readout IDs the sovereign or other agents may reference.

## Nav canon v7.0 — organ→site mirror (locked 2026-08-06)

The 5-item top-nav is the **human mirror** of organ outputs:
HOME(AAA) · EARTH(GEOX) · WORDS(arifOS) · WORLD(WEALTH) · WORK(WELL).
Organs are agent-owned — they live in `machine_links`, not the human nav.
See `/root/AAA/skills/arif-fazil-site-ops/references/nav-canon-v7-organ-mirror.md` for the full architecture.

## Hub hero pattern (locked 2026-08-07)

Every hub now carries its own hero — the human-attention grabber modelled on `/earth/`
(the gold standard, per sovereign: "hero is central theme to get human attention").
Earth has a live-data hero; the other hubs are static (content-first, no-JS).

| Hub | Hero title | Visual | Pull-quote |
|---|---|---|---|
| `/earth/` | "The Dynamic Earth." | live Macrostrat globe (WebGL) | Sagan, *Pale Blue Dot* |
| `/words/` | "The Compass." | SVG compass rose, 60s CSS rotation | T. S. Eliot, *Little Gidding* |
| `/world/` | "The Live Map." | wireframe globe SVG + equator pulse | Korzybski, *Science and Sanity* |
| `/work/` | "The Drill." | CSS drill-string stroke animation | Will Durant / Aristotle |

Static hero anatomy (shared by words/world/work): `.kicker` (mono, gold `#c9a227`,
uppercase, wide letter-spacing) → `h1.hero-title` (display serif, `clamp(2rem,5vw,3.25rem)`)
→ `.hero-prose` → `blockquote.hero-quote` (gold left border, italic, mono `cite`)
→ `.hint` (mono, dim, starts `▸`). Visual + text in a 2-col grid
(`minmax(220px,1fr) minmax(0,1.4fr)`), collapses to 1 col ≤720px with centered text.
Palette: bg `#0A0B0D`, gold `#c9a227`, ink `#e8e6e1`; fonts from design-system tokens.
No JS — pure CSS keyframes (`compass-spin 60s`, `eq-pulse 6s`, `drill-stroke 4.5s`);
every animation guarded by `@media (prefers-reduced-motion:reduce){animation:none}`.

### Pitfalls — hub hero deploy (verified 2026-08-07)

- **Git-tracked static shells get reverted by the build cycle.** `public/world/index.html`
  is git-tracked (committed in a9404d5); `public/words/` and `public/work/` are untracked
  dirs. After `write_file` + `npm run build`, `public/world/index.html` was back at HEAD
  content (old nav, no hero) — the write did not survive. Fix that worked: write the new
  HTML **directly to `/var/www/html/arif/<route>/index.html`** (what Caddy actually serves),
  verify live, then commit the src change separately. Untracked shells patch normally
  (src → build → rsync dist → live).
- **verify-pages passing ≠ content updated.** The gate asserts HTTP 200 only. 2026-08-07:
  `/words/` and `/work/` showed the new hero but `/world/` silently stayed stale while the
  gate PASSED. After any deploy, content-verify per page:
  `curl -s https://arif-fazil.com/<route>/ | grep -oE "hero-title|kicker"`.
- **Sibling ad-hoc deploy.sh is a webroot-nuking hazard.** A pasted deploy helper ran
  `rsync -a --delete public/ /var/www/html/arif/` (would delete live surfaces not in
  `public/` — `/999/verify`, `/work/proof`, `/earth/` shells), copied a non-existent
  `world-index.html`, and rsynced `public/` instead of `dist/`. Never run a sibling's
  deploy script. Use additive per-route rsync (no `--delete`). `deploy-site.sh --apply` is T3.

## Orphaned CSS classes — markup has classes, stylesheet is gone (verified 2026-08-07)

Symptom: a page renders as bare text where it should be styled — kicker/h2/lede
visible but no card borders, no grid, no padding. Cause: the HTML still uses
`.acts` / `.act` / `.no` / `.basin-callout` / `.facts` etc., but the CSS rules
for those classes were deleted (or never migrated when the stylesheet was
consolidated). Hit on `/earth/` 2026-08-07: `#dynamic` (3 readings) and `#malay`
(case-study facts table) rendered as flat prose.

**Detect before claiming a section is "weak content" instead of "missing CSS":**

```bash
# 1. List the unique class names used in the section's HTML
sed -n '/<section id="<id>"/,/<\/section>/p' public/<route>/index.html \
  | grep -oE 'class="[^"]+"' | sort -u

# 2. Probe each against the page's CSS sources
for css in public/<route>/_shared/*.css public/_shared/design-system/*.css; do
  echo "== $css =="
  grep -E "\.act|\.no|\.basin-callout|\.facts" "$css" || echo "  (no match)"
done

# 3. If no match anywhere — orphan. The CSS exists ONLY in some legacy mirror
#    (e.g. /earth/_legacy-globe/index.html) but isn't loaded by the current page.
```

**Fix:** add the missing rules to the page's existing inline `<style>` block
(every page on earth has one — keep the pattern). Use the page's own CSS
variables (`var(--earth-gold)`, `var(--font-display)`, `var(--font-mono)`)
defined in `tokens.css` / `components.css` / the page's shared stylesheet,
not hardcoded hex. New pattern classes should match the design-system tokens
so they look continuous with the rest of the page, not a designer-stamp.

Recipe for the canonical `card grid + facts table` pair added 2026-08-07 to
`/earth/`: see `references/hub-hero-pattern.md` (sections "Acts card grid" and
"Two-column prose + data table").

## Nav canon drift on hub pages (verified 2026-08-07)

The 5-lane nav canon (HOME EARTH WORDS WORLD WORK) is exact. Active page
gets `class="here"`. `llms.txt` and `missions.json` are machine-readable
hints — they belong in `<link rel="alternate">` head tags, never as visible
nav links. 2026-08-07: `/world/` had `<a href="/llms.txt">llms.txt</a>` in its
nav while `/words/` and `/work/` did not. Single-line drift, but breaks
visual alignment across the hub row. Before declaring two hubs "aligned,"
`diff` their `<nav class="nav">...</nav>` blocks — anything beyond `class="here"`
on the active page is a hidden drift.

## /earth/ is a specialty page, not a hub template (verified 2026-08-07)

`/earth/` has its own design system that diverges from the three hub pages:

| Element | `/words/` `/world/` `/work/` | `/earth/` |
|---|---|---|
| Nav class | `class="nav"` | `class="earth-site-nav"` |
| Nav children | `Home Earth Words World Work` + active `here` | brand + Earth/Economics/World/Writing/Doctrine/Missions/999/Machines |
| Stylesheets | `tokens.css` only | `tokens.css` + `components.css` + `earth/_shared/earth-shell.css` + inline `<style>` |
| Page-level tokens | none | `--earth-gold: #C9A227`, `--earth-paper: #0A0B0D`, `--earth-ember: #E4572E` |
| Container | `<div class="frame">` | own layout, no `frame` |
| Card style | shared `.card` | `.dossier-card`, `.stat`, `.intent-card` |
| Hero treatment | static SVG/CSS | live WebGL globe (`globeViz`) + waypoint deck |

**Don't try to align `/earth/` to the hub frame.** Earth is the house specialty
page — the hub pages point TO it (their `here` reason is "this is what Earth
does for you"). When the user says "earth is the gold standard for the hero"
they mean the hero *pattern* (kicker + h1 + visual + prose + pull-quote +
hint), not the page chrome. The hub frame template is `/work/` (cleanest
hero hierarchy, uses only `tokens.css`, ships the 5-lane nav).

`scripts/render-propa.cjs` looks for `<!--B11-B:FAN-SVG-MARKER:BEGIN/END-->` in
`public/propa/index.html`. Deleting them when replacing the fan-sec section
breaks `npm run build`. Preserve as empty stubs OR update the script to skip missing markers.

## Publishing a MakcikGPT article on /world/makcikgpt/ (verified 2026-08-09)

Full recipe: `references/makcikgpt-publish-recipe.md`. The load-bearing facts:

- **Write to `/var/www/html/arif/makcikgpt-md/<slug>.html`** — that is the serve
  root for `/world/makcikgpt/*` (Caddy strips the prefix). Writing to
  `/var/www/html/arif/world/makcikgpt/` serves nothing.
- **`chmod 644` immediately** — a root-owned `0600` file is invisible to Caddy.
- **Update `makcikgpt-md/index.html` in BOTH lists** (grouped `<details>` per
  series AND the hidden `ul.flat-list`), bump the "NN articles" counter, and
  grep-count after inserting — sed duplicated entries across the two sections.
- **No author attribution in the article** — MakcikGPT persona only. Arif:
  "Jangan letak nama aku, letak persona makcikgpt. Aku share artikel x dak sapa
  baca." The persona is the distribution strategy.
- **Never announce "published" before the live probe passes** (article 200 +
  correct title + index links it + other articles unbroken). Arif hit "Article
  not found. Pembohong hang." twice from premature announcements. Publish =
  findable from `/world/makcikgpt/`, not just 200 on a direct URL.

## Publishing a new long-form essay on /words/writing/ (verified 2026-08-07)

Full recipe: `references/essay-publish-workflow.md` · design tokens: `references/writing-design-system.md` · session postmortem + fabrication incident: `references/essay-pipeline-2026-08-07.md` · standalone page shell: `templates/essay-makcikgpt-mirror.html`.

### Arif's design ruling — makcikgpt language wins for essays

Arif (2026-08-07): **"Design wise makcikgpt site is much better."** When building essay/article surfaces, default to the MakcikGPT design language, NOT the hub-page hero language:

- Palette: GitHub-dark — bg `#0d1117`, body `#c9d1d9`, headings/links `#58a6ff` (blue), accent `#ffd700` (gold), meta `#6e7681`/`#8b949e` (note: differs from hub gold `#c9a227`)
- Cover block: `.cover` with emoji, kicker (uppercase mono), title, subtitle, byline incl. `999 Meterai · seal` line
- Zen pulse: 3-column aside answering WHERE AM I? / WHY CARE? / WHAT NEXT? in 3 seconds
- Breadcrumb nav: `← arif-fazil.com /words/ Writing` at top
- Collapsible `<details class="zen-reveal">` series sections with emoji + mono label + count
- 999 seal + DITEMPA BUKAN DIBERI footer; superscript `[n]` refs with anchors; epistemic tag badge (INT/OBS/SPEC)
- Cross-link the essay triptych: each article's footer links its paired articles ("Pairs with:")

**Reality check 2026-08-07 end-state:** the generator (`render-words-essays.cjs`) emits pages with **inline `<style>`** blocks (self-contained). The `_shared/writing.css` file was created and then removed from live because nothing linked it. Verify what the generator emits before assuming a shared CSS is in play — if the generated pages carry inline styles, keep them; don't force a `<link>` the generator will strip on rebuild.

When the user pastes a new essay and says "publish on my site under /words/", this is a **constitutional publication**, not a content edit. Source-of-truth chain:

```text
src/data/essays/<N>-<slug>.ts     CANON essay module (EssayContent type)
  ↓
src/data/essays/index.ts          register import + add to essayModules[]
  ↓
src/data/essays.json              SPA catalog entry (series S4=Governance, S6=Eureka, S8=Forge)
  ↓
npm run build                     prebuild runs scripts/render-words-essays.cjs
  ↓
public/words/writing/<slug>/index.html + <slug>.md + index   (generated)
dist/words/writing/<slug>/...                                 (mirrored)
  ↓
rsync dist → /var/www/html/arif/words/writing/   Caddy @static_dirs serves it
```

`scripts/render-words-essays.cjs` is the **sanctioned generator** (created 2026-08-07, same pattern as `generate-makcik-index.cjs`). Do NOT hand-write `public/words/writing/<slug>/index.html` — the build will overwrite it with whatever the .ts contains. Hand-writing is wasted entropy.

Steps:

1. **Essay module** — `src/data/essays/<N>-<slug>.ts` exporting `EssayContent` (`{title, date, slug, tags, excerpt, mediumUrl, html}`).
2. **Register** — import the module in `src/data/essays/index.ts` and append to `essayModules[]`.
3. **Catalog** — add an entry to `src/data/essays.json` (SPA registry). Series assignment: S4 = governance canon (new constitutional writing), S6 = Eureka Trilogy, S8 = The Forge field notes.
4. **Build** — `npm run build` triggers the prebuild generator. Generated `public/words/writing/<slug>/index.html` + `public/words/writing/<slug>.md` + `public/words/writing/index.html` appear automatically.
5. **Deploy** — `rsync` from `dist/words/writing/` (the copy-static-html.js mirror step) to `/var/www/html/arif/words/writing/`, or use the standard `scripts/deploy-site.sh`.

User doctrine: **direct publication, no Medium repost** for constitutional writing. Mark `mediumUrl: ''`, `isDirectPublication: true`.

References block convention: arXiv/linked citations as superscript markers `<sup class="ref"><a href="#ref-N">[N]</a></sup>` with an `<ol class="ref-list">` at the bottom — not bare inline URLs. Matches the published canon elsewhere on the site. F2 TRUTH: every external citation gets the discipline; if the URL is a real reference but the source's view isn't endorsed, add "Cited works are external references; their views are not necessarily endorsed by the author" near the refs list.

- **Title fidelity is semantic, not cosmetic — translate, don't paraphrase.** (verified 2026-08-07.) The canonical title lives in the essay's `.ts` file `title:` field, NOT in any hand-built page. When hand-authoring, the rendered title must match the `.ts` value character-for-character. Arif rejected a verbose paraphrase ("What Acemoglu Missed, Why Institutions Become Stupid, and How Humans, AI, and Organizations Turn Evil") and corrected it: *"BANGANG and stupid is different meaning."* The canonical title was the short "Simulative Institutions: The Third Axis of Failure". Always:
  1. Read the `.ts` file's `title:` field first — it's CANON.
  2. Align `<h1>`, `<title>`, meta description, `essays.json`, the index cards, and `llms.txt` to that exact value.
  3. Cross-check `articles-annotated.json` — it has the authoritative registry.

### Pitfalls (hit 2026-08-07)

- **Parallel subagents collide on the same file set (hit 2026-08-07).** Dispatching 3 parallel subagents to write `.ts` modules, static HTML, and the index in the same directory (`/words/writing/`) caused fights: one deleted `_shared/writing.css`, another restored it, another wrote a duplicate `.ts` with a different slug → two index rows with the same title. **Fix:** serialize site-file writes (one subagent per concern) OR give each disjoint paths and reconcile slugs yourself before running the renderer. Never let parallel subagents overlap on the same `public/words/` subtree.
- **F2 TRUTH fabrication guard — subagents MUST NOT author the essay body (verified 2026-08-07, escalated 2026-08-07 same session).** A 3-way parallel delegation on this session "enriched" Arif's Third Axis of Failure essay with **Hannah Arendt's *Eichmann in Jerusalem***, invented book citations, and editorial commentary he never wrote. His feedback verbatim: **"Some of the article is not even true or real!!"** After stripping the fabrication, he added: **"I reflect that."** The body came back with quotes about the "banality of evil" and references that don't appear anywhere in his paste.

  **Rule:** the user's paste IS the source of truth. Subagents may build page shells, CSS, design, verification, deploy glue, and the byline footer — **never the essay body itself**. Extract the body programmatically from the user's text:
  ```bash
  # From .ts file
  python3 -c "import re;t=open('path.ts').read();m=re.search(r'html:\s*\`(.*?)\`,\s*\n\};',t,re.DOTALL);print(m.group(1) if m else 'NOT FOUND')"
  ```
  Preserve only the user's own reference URLs, and never invent a quote or citation. If the user says "include references [1][2][3]" but does not paste the URLs, **ASK before fabricating URLs**.

  **Strip check before delivery:**
  ```bash
  # For each cited author name, verify it appears in the user's paste
  # Strip any scholarly citation, historical anecdote, or quote that:
  #   - Is not in the source paste
  #   - Adds framing language ("Makcik analisa", "Makcik tanya")
  #   - Quotes scholars (Hannah Arendt, Einstein, etc.) without source text
  #   - Extends sections beyond what user pasted (subagents love adding "Examples" sections)
  ```

  **What survived the strip:** Arif's body text + his own [1][2][3] superscripts that he explicitly pasted with the URLs (Nobel Prize, UBS Nobel Perspectives, archive.org Why Nations Fail). His closing line — *"Humans, institutions, and AI do not become evil because they are malicious. They become evil when they get better at protecting narratives than correcting themselves with reality."* — preserved exactly as he wrote it.

  **Heuristic:** if a subagent's output contains text that has a polished citation format, scholarly tone, or a "Makcik" voice that wasn't in the original paste, it is almost certainly fabricated. Trust the user's draft; never trust the subagent's embellishment.
- **Slug mismatch `.ts` slug ↔ `essays.json` `dest.path` → SPA catalog 404s while static page works.** The renderer's URL comes from the `.ts` slug. If `essays.json` `dest.path` uses a different slug, the SPA catalog links to a 404 but the static page renders fine. Fix essays.json, never rename the .ts. Always: `python3 -c "import json;d=json.load(open('src/data/essays.json'));[print(e.get('dest',{}).get('path','')) for e in d if 'title-key' in e.get('title','')]"` then diff against the live `/words/writing/<slug>/` URL.
- **Duplicate-row trap: two `.ts` files, same content, different slugs → two rows in the index.** `render-words-essays.cjs` dedupes by slug (first occurrence by filename length wins), not by title. A leftover `26-the-third-axis-of-failure.ts` + new `26-the-third-axis-of-failure-what-acemoglu-missed.ts` will both ship to the index. Delete the stray file before rebuild.
- **SPA-only slug = invisible to text-only crawlers (verified 2026-08-07).** EssayPage renders per-essay content client-side. A slug with NO static `public/words/writing/<slug>/index.html` returns the React shell to any JS-less fetcher (EMD crawler, Copilot, research agents, curl) → content UNKNOWN even though the URL is 200 and humans see it fine. This is a *publishing architecture problem*, not a retrieval problem. **Rule: every essay publish MUST ship a static shell + markdown mirror.** After adding a `.ts` module + `essays.json` entry + rebuild + rsync, verify the text-only path:
  ```bash
  # 1. Static shell exists (server-rendered content)
  curl -sf "https://arif-fazil.com/words/writing/<slug>/" | grep -c "unique-body-phrase"
  # 2. Markdown mirror exists
  curl -sf -o /dev/null -w "%{http_code}" "https://arif-fazil.com/words/writing/<slug>/index.md"
  # 3. Discoverable via llms.txt (auto-regenerated by renderer)
  curl -s "https://arif-fazil.com/words/writing/llms.txt" | grep -c "<slug>"
  ```
  Template: `templates/essay-standalone.html` or the hand-authored static shell pattern (inline `<style>`, forge palette, minimal hero = breadcrumb + kicker + h1 + lede, chrome pills in footer). The static shell must mirror the SPA footer (ARIF FAZIL identity block, publication, epistemic stance, pills, manifesto line) so both render paths carry the same F2/999 markers. Tri-witness retrieval = browser presentation + static document + agent discovery index (llms.txt); failure of any one witness no longer destroys recoverability.

- **`render-words-essays.cjs` runs in prebuild AND gets resurrected by subagents (verified 2026-08-07).** When the session started, the script existed in `scripts/` and was wired into `package.json` `prebuild` (` && node scripts/render-words-essays.cjs`). I disabled it by renaming `.disabled` and rm'd it. A subagent then **recreated the script from scratch and rewired `prebuild`** within the same session — running `npm run build` clobbered the hand-written index page. The fix that stuck was three actions together: (1) `rm -f scripts/render-words-essays.cjs` so it's gone, (2) `mv scripts/render-words-essays.cjs.disabled /root/scripts/render-words-essays.cjs.archived` so the disabled copy is OUT of the scripts dir (subagents search `scripts/`), (3) edit `package.json` `prebuild` to remove the script reference. Verify with `grep render-words package.json` → must return nothing. Subagents will treat a `scripts/<name>.cjs` file as canonical and re-wire it on every site-edit task. Anything you want disabled permanently must leave the scripts/ dir entirely.

- **Article slug format — never include the file prefix.** Filename: `24-the-agi-paradox-why-bigger-models-wont-save-us.ts` → slug field: `the-agi-paradox-why-bigger-models-wont-save-us` (no `24-` prefix). Same convention applies to all 17 essay .ts files.
- **`articles.json` registry is mandatory (added 2026-08-07, refined 2026-08-07).** The `.ts` file → `index.ts essayModules` → `essays.json` chain is INCOMPLETE. Per-essay SPA bundle inclusion requires a matching entry in `src/data/essays/articles.json` (slug + title + date + categories + hasContent + isDirectPublication). Without it, Vite tree-shakes the essay out of the production bundle → `getEssay(slug)` returns undefined → SPA renders "Essay Not Found" even though shell HTML loads fine and `essays.json` has the slug. Verified live 2026-08-07 publishing "I'm Not a Programmer": the 404 looked exactly like a build/cache issue but the real fix was adding an entry to `articles.json`. Diagnose with: `grep "<your-slug>" dist/assets/index-*.js` — empty means articles.json is missing the slug.

- **Essay publish chain — 4-file discipline (refined 2026-08-07).** The publish workflow touches **4 registries**, not 2. Missing any one of the four produces a different failure mode and each fails silently:

  | # | File | Field | If missing → |
  |---|---|---|---|
  | 1 | `src/data/essays/<N>-<slug>.ts` | `slug:` in EssayContent | Build fails (no slug to render URL) |
  | 2 | `src/data/essays/index.ts` | import + `essayModules[]` entry | Vite tree-shakes the essay out of bundle → SPA returns undefined for slug |
  | 3 | `src/data/essays.json` | `dest.path` matching slug | `/words/writing/` index omits the essay (renderer can't link it) |
  | 4 | `src/data/essays/articles.json` | slug + title + date + categories + hasContent + isDirectPublication | Same as #2 (articles.json is the SPA bundle inclusion registry; essays.json is the listing-page registry) |

  The cleanest publish workflow: edit `.ts` → edit `index.ts` → edit `essays.json` → edit `articles.json` → `npm run build` → copy the shells that name the NEW hash, plus `rsync -av --update` of the new assets (not a full-tree `rsync -a dist/`). Do not add `--delete`. Count live HTML that names a hash the new dist lacks. `--delete` only after that count is zero. On 2026-10-13 that count was 74. Re-count. Then verify with the 5-gate check. The "5th file" of the chain is the static shell `public/words/writing/<slug>/index.html` + `index.md` — see SPA-only pitfall below for why this is mandatory.

- **`sitemap.xml` stale drift (verified 2026-08-07).** Live sitemap has 46 `<loc>` entries; site has 140+ pages including 15 essays in `/words/writing/`. Zero essay URLs in sitemap — the static essay shells and markdown mirrors are crawler-invisible via sitemap even though they're discoverable via llms.txt + landing pages. `make deploy` runs the `verify-surfaces.cjs` probe that catches SOME drift but NOT sitemap-vs-essays mismatch. Diagnose: `curl -s https://arif-fazil.com/sitemap.xml | grep -c "<loc>"` (count) vs `curl -s https://arif-fazil.com/words/writing/llms.txt | grep -c "^- \["` (essay count). If sitemap count << llms.txt essay count, sitemap is stale. Fix: add a generator to prebuild that scans `public/words/writing/<slug>/index.html` and emits `<loc>` entries (deferred — separate day's work). Until fixed, agents using sitemap as a discovery path will MISS the essays entirely.

- **FRAME recovery from quarantine (verified 2026-08-07).** During the repo audit session, `/root/FRAME/` source was deleted (still alive in `/opt/frame/app/` runtime). Recovery: check `/root/_quarantine_FRAME_<date>/` first, `mv` back to `/root/FRAME/`, content parity verified by `diff <(ls src/frame_organ/) <(ls /opt/frame/app/frame_organ/)`. Then `git push` to `ariffazil/FRAME` (private, gh repo create + push). Never assume a deleted source is unrecoverable — the quarantine dir holds 7-day grace copies per F1 doctrine. Lesson: when executing F1-authorized deletions, always check quarantine FIRST; the recovery path may be one `mv` away.
- **SPA bundle rsync — full-site, not just `/words/writing/` (added 2026-08-07).** The per-slug SPA shell at `/words/writing/<slug>/` references a hashed bundle (`assets/index-XXXXXXX.js`). If you only rsync `dist/words/writing/` to live, the new shell ships but still points at the OLD bundle hash from the previous build. That old bundle doesn't have the new slug → 404. Fix: copy the shells that name the NEW hash, plus `rsync -av --update` of the new assets. Do not full-tree rsync. Do not add `--delete`. Count live HTML that names a hash the new dist lacks. `--delete` only after that count is zero. On 2026-10-13 that count was 74. Re-count. Then verify: `curl -s <slug-url> | grep index-` should match `ls dist/assets/index-*.js`. Both shell and bundle land in one pass. Full detail in `references/essay-publish-workflow.md`.

- **Three-layer build-then-hand-write pipeline traps (verified 2026-08-07).** When the writing surface has both (a) a build-time generator, (b) a live `/var/www/html/arif/` webroot mirror, AND (c) a source `/root/arif-fazil.com/sites/arif-fazil.com/public/words/writing/` mirror, edits to layer (c) won't reach layer (b) unless (b) is also patched. Build pipeline regenerates (c) from `.ts` files, then `copy-static-html.js` mirrors (c) to `dist/`, then `rsync` mirrors `dist/` to (b). Three sequential steps, each can independently fail. Best practice for this surface: write directly to (b) for verification, then mirror back to (c) and trust the next `npm run build` to keep them in sync if you haven't changed the .ts source.
- **Two .ts files with the same `slug:` field → renderer uses the first by filename length, ignores the second.** Always check that a unique slug is used; if the user gives a long slug, search the dir for any other essay claiming it.
- **Build orphans can sneak in.** When the article slug differs from the `.ts` filename (e.g. file is `25-truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens.ts` with slug `truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens`), the live URL is the slug. If you keep an older stale directory on disk (e.g. `truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens-more-compute-and-more-patience/`), Caddy serves a 404 because that path has no file. Clean stale dirs after slug changes.
- **Hand-written page emitted with malformed h2 tags.** When the generator strips `class="paper-section-title"` from `<h2>` but leaves a trailing space, output becomes `<h2 >Section 1 — ...</h2>` or `<h2>>Section 1 — ...</h2>` — browsers render but the markup is wrong and search-engine parsers may split. Always post-process the rendered output: `re.sub(r'<h2\s*>>?', '<h2>', h)`. Validate with `grep -E '<h2>>|<h2 >' /var/www/html/arif/words/writing/<slug>/index.html` → must return 0 lines.

### Shared CSS — `/words/writing/_shared/writing.css` (added 2026-08-07, status: inactive)

A canonical shared stylesheet WAS created at `/var/www/html/arif/words/writing/_shared/writing.css` (510 lines, 13.5 KB, all 30 design-system classes covered). But after the session settled, the generator (`render-words-essays.cjs`) emits pages with **inline `<style>` blocks** instead of `<link>` to the shared CSS. The shared file ended up orphaned (rmdir'd from live webroot) because nothing linked it.

**Practical guidance:**

- **New essays:** start from `templates/essay-standalone.html` (a static HTML skeleton with the shared CSS `<link>`). The generator will overwrite it on next `npm run build` — either commit to the generator's inline-style output OR patch the generator to emit `<link>` to the shared CSS instead.
- **Existing essays:** all shipped with inline styles that duplicate the shared CSS. Migrating them is low-priority cleanup. Both approaches work in the browser.
- **Generator patch (one-time, T1):** in `scripts/render-words-essays.cjs`, replace the emitted `<style>...</style>` block with `<link rel="stylesheet" href="/words/writing/_shared/writing.css">`. Then the shared file earns its keep.

Full class inventory, token table, breakpoint map, and migration notes:
`references/writing-design-system.md`.

**Migration note:** existing essays (AGI Paradox, Truth Is Not Cheap, The Third Axis of Failure)
ship inline `<style>` blocks that duplicate the shared CSS. They look right; they pass verify-pages;
nothing links `_shared/writing.css`. Don't treat the orphan shared file as a defect — it documents the
intended design system even if the generator currently emits inline styles.

### [object Object] pitfall — SPA render failure on static shells

Symptom: `public/<route>/index.html` exists but every link renders as
`[object Object]` literally in the served HTML.

Cause: the static shell was hand-authored assuming the SPA would re-render
it at build time, but no generator ever overwrites the file. React JSX
inside a `template` tag or a `<div dangerouslySetInnerHTML>` with an object
gets stringified to "[object Object]" when no React runtime hydrates.

Fix: **rewrite the static shell by hand**. Group entries by series (S1–S9),
use real `<a href="...">` for every link (no template objects, no `{e.title}`
JSX leaking). For the writing index the pattern is:

```html
<p class="series-label">S4 · Governance Canon</p>
<ul>
  <li><a href="/words/writing/<slug>/">Title</a> <span class="meta">· YYYY-MM-DD</span></li>
</ul>
```

For Medium cross-links (separate language/territory) keep them grouped
under "Medium Pieces (cross-linked)" with `target="_blank" rel="noreferrer"`.

### Caddy `/writing/*` double-prefix bug (verified 2026-08-07)

`/etc/caddy/Caddyfile` has:

```caddy
redir /writing/* /words/writing{uri} 308
redir /essays/* /words/writing{uri} 308
```

`{uri}` includes the matched prefix, so `/writing/foo` → `/words/writing/writing/foo`
(double `/writing/`). Same for `/essays/foo` → `/words/writing/essays/foo`.
Both 404. **Affects every essay, not just new ones** — pre-existing.

Canonical URLs (`/words/writing/<slug>/`) work fine. The legacy redirects
are decorative for SEO/backlinks; if any inbound links exist they currently
break.

Fix recipe (T1, reversible):

```caddy
redir /writing/* /words{uri} 308
redir /essays/* /words{uri} 308
```

Strip the `/writing` or `/essays` prefix by replacing the destination
template, then verify:

```bash
curl -sIL "https://arif-fazil.com/writing/<any-slug>/" | grep -i location
# expect: location: /words/writing/<any-slug>/
```

Until this Caddy rule is patched, tell the user the canonical URL and note
the redirect chain is broken for inbound `/writing/` and `/essays/` traffic.
Do NOT silently patch Caddy during a routine essay-publish — that's a
separate day's work.

### Essay module slug convention — avoid prefix collisions (verified 2026-08-07)

The essay filename in `src/data/essays/` uses an ordinal prefix
(`01-...`, `02-...`, ..., `24-...`) but the **slug in the EssayContent**
must NOT include that prefix. Slug is the URL path component — `/words/writing/<slug>/`.

```ts
// filename: src/data/essays/24-the-agi-paradox-why-bigger-models-wont-save-us.ts
const content: EssayContent = {
  slug: 'the-agi-paradox-why-bigger-models-wont-save-us',  // ← no `24-` prefix
  // ...
};
```

If the filename prefix leaks into the slug, the canonical URL becomes
`/words/writing/24-the-agi-paradox-...` instead of the human-friendly form,
and `articles-annotated.json` entries won't match.
