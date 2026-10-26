# Pitfall index — arif-sites-ops (merged from four skills)

> Merged 2026-10-23 from `arif-sites-ops`, `arif-fazil-site-ops`, `arif-fazil-web-ops`
> and `arif-sites-content-ops` (F13 consolidation order). Bodies are verbatim — this is a
> merge, not a rewrite. Blocks whose normalised body already appeared earlier in the merge
> were dropped; when that happened the drop is recorded under "dropped as exact duplicates".

## source: arif-sites-ops

- Archive archaeology (BEFORE any landing-page or major-surface mutation, verified 2026-08-11)
- Pitfalls
- CSP iframe trap (verified 2026-08-09)
- Path-root trap (verified 2026-08-06)
- Constitution-root surfaces: /000 + /999
- Deploy pipeline — three paths, two gates (verified 2026-08-07)
- Surfaces.json trust gap — verify-pages is content-thin (verified 2026-08-07)
- surfaces.json doctrine-introspection drift (verified 2026-08-06)

## source: arif-fazil-web-ops

- arif-fazil-web-ops — pitfall list

## source: arif-fazil-site-ops

- arif-fazil-site-ops — intro
- `/words/writing/` essay publishing — SPA renders, not static (2026-08-07)
- Dead nav stubs in `@agent_shells` (2026-08-06, /pm-bayang/)
- `patch` tool refuses system config paths
- `_redirects` is Cloudflare Pages syntax — Caddy doesn't read it
- Probe before act
- Live-engine debugging — silent IIFE death + Node validation (2026-08-06)
- Arif's brand preference: "ARIF FAZIL" (Arif correction 2026-08-07)
- Arif's language preference: "bangang" vs "stupid" (Arif correction 2026-08-07)
- Arif's editorial bar: multimodal audit before designing (2026-08-07)
- Upgrade, not replace (Arif, verbatim)
- Check alignment before deploy (Arif)
- verify-pages reports LIVE state
- verify-pages garbled HTTP code (2026-08-07, "HTTP 200000")
- Caddyfile root path ≠ /var/www/html/<slug>/ — THREE webroots exist (2026-08-06, updated 2026-08-12)
- Cloudflare CDN serves stale despite `Cache-Control: no-cache` (2026-08-06)
- `/_shared/` assets must be synced to `/var/www/html/_shared/` (2026-08-12, 90 min wasted)
- Caddy routing order
- Caddy `{uri}` is FULL URI — use `{0}` for wildcard capture (2026-08-07, 15 min)
- Adding a nav-canon path to the SPA (2026-08-07)
- Live webroot drifts from dist/
- Editing dist/ is futile — public/ is the source-of-truth for static HTML (2026-08-11)
- .bak naming convention for T1 reversible edits (2026-08-11)
- Renaming an agent_shells path (e.g. `/vitals/` → `/propa/`) — full recipe (2026-08-06)
- MakcikGPT article publishing — FOUR registers + generator (2026-08-09)
- MakcikGPT pre-publish audit — 5-gate verification protocol (2026-08-09)
- MakcikGPT authoring voice — Bahasa Kampung, NOT Accounting (2026-08-09)
- Content fact-verification against primary sources (2026-08-09)
- Number-timeline accuracy — critical for leadership pieces
- MakcikGPT article publishing — FOUR registers + generator (2026-08-09)
- Essay publish wiring — FIVE registers + Caddy routing (verified 2026-08-07)
- Agent-chrome creep — every "small addition" turns a journalism brand into a GitHub repo (2026-08-11)
- Article HTML has NO inline CSS by default — articles render as white background (2026-08-11)
- Renaming an essay title after publish (5 registries, 2026-08-07)
- Per-essay static HTML generation was REMOVED (2026-08-07, Arif rejected)
- `@static_dirs` needs SPA fallback for nav-canon paths (2026-08-07)
- GDELT from this host

## source: arif-sites-content-ops

- arif-sites-content-ops — pitfall list

---

# ── source: arif-sites-ops ──

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

# ── source: arif-fazil-web-ops ──

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
  1. `# HISTORICAL SCAR. Do not run: git checkout HEAD -- .` to restore all canonical files to disk
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
  # HISTORICAL SCAR. Do not run: git checkout HEAD -- .
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

# ── source: arif-fazil-site-ops ──

## Pitfalls (each cost real time)

### `/words/writing/` essay publishing — SPA renders, not static (2026-08-07)

**Critical (after Arif rejected flat static essays):** Essay pages under
`/words/writing/<slug>/` are rendered by the React SPA's `EssayPage.tsx`,
NOT by static HTML files. Per-essay static `<slug>/index.html` files SHADOW
the SPA — users get the plain static version instead of the rich SPA design
(MakcikGPT-style: forge-black hero, tag pills, prose typography, "Continue
Reading" nav, JSON-LD). **NEVER generate per-essay static HTML for essay
slugs under `/words/writing/`.**

The prebuild script `scripts/render-words-essays.cjs` (in prebuild chain
after `generate-makcik-index.cjs`) generates ONLY:
- `public/words/writing/index.html` — the listing surface
- `public/words/writing/index.json` — machine-readable list
- `public/words/writing/llms.txt` — LLM discoverability surface

When sibling agents enrich the index with series chips, stat pills, reading
time badges, or RSS link — do NOT re-inject. md5sum reconcile, adopt theirs.

**Source-of-truth rule (revised 2026-08-07):** `.ts` file with
`isDirectPublication: true` AND real HTML body (≥200 chars) determines what
gets listed. `articles.json` is metadata hints only — filtering by
`articles.json.isDirectPublication` silently skips essays where the field
wasn't set but `.ts` has real content.

Caddy requirement: `@agent_shells` MUST contain `/words` so
`/words/writing/<slug>/` hits `@writing_spa` fallback (which rewrites to
`/index.html`). Without this entry, paths 404 at the static_dirs layer.

### Dead nav stubs in `@agent_shells` (2026-08-06, /pm-bayang/)
A path can be listed in `/etc/caddy/Caddyfile` `@agent_shells` matcher but have **no source file** — Caddy `try_files` returns 404. Symptom: HTTP 404 for a path that "should" exist per the nav canon.

**Detection probe:**
```bash
curl -sI https://arif-fazil.com/<path>/ | head -1   # 404?
find /root/arif-fazil.com -maxdepth 6 -iname "*<slug>*" -not -path "*/node_modules/*"
```
**Fix:** see `references/dead-stub-redirect-recipe.md` — 3 patterns (alias redirect, static shell, parent redirect) + the sudo+python Caddyfile edit. `scripts/detect-dead-stubs.sh` probes every registered path and reports 404s in one shot.

### `patch` tool refuses system config paths
The `patch` tool refuses `/etc/caddy/Caddyfile` with `"Refusing to write to sensitive system path: use the terminal tool with sudo"`. **Use `sudo python3`** to edit Caddyfile (the script does find-and-replace in-place — never `write_file` or `cat > Caddyfile` since indentation is tab-sensitive):
```bash
sudo python3 << 'PYEOF'
path = '/etc/caddy/Caddyfile'
with open(path) as f: c = f.read()
old = '<exact unique block>'
new = '<block with redir added>'
assert old in c, "pattern not found — print c to see what shifted"
open(path, 'w').write(c.replace(old, new, 1))
PYEOF
sudo caddy validate --config /etc/caddy/Caddyfile   # Always validate after edit
# HISTORICAL SCAR. Do not run: sudo systemctl reload caddy
```
**Always back up Caddyfile first** to `/root/backups/Caddyfile-<timestamp>-pre-<reason>.bak`. Single `cp` reverts.

### `_redirects` is Cloudflare Pages syntax — Caddy doesn't read it
`public/_redirects` works for Cloudflare Pages routes but **NOT for the Caddy-served site**. For Caddy redirects, edit `Caddyfile` directly (see above). Keep both files in sync as convention.

### Probe before act
Built a whole parallel SOT Atlas at `/world/` when `/world/sot/` already existed from a prior agent. Always curl + ls the target path first.

**Specifically: when user asks for a new atlas/dashboard/section, do a 5-step probe FIRST:**
```bash
# 1. Does a similar path already exist?
curl -sI https://arif-fazil.com/<path> | head -1
# 2. Is there content on disk?
find /root/arif-fazil.com -maxdepth 6 -iname "*<keyword>*" -not -path "*/node_modules/*"
# 3. Is it listed anywhere?
grep -r "<path>" /root/arif-fazil.com/sites/arif-fazil.com/src/data/
# 4. What does the existing instance look like?
ls /var/www/html/arif/<existing-path>/
# 5. Can it be extended, or do you need to build a parallel?
```

**Step 6 (added 2026-08-06 — sibling-already-deployed):** grep the live HTML for the
section id you were about to inject. If `grep -c 'paradox-sec\|pv-brent' public/<path>/index.html`
returns >0, **a sibling already deployed it.** Don't re-inject — verify the live engine
works (`curl -s <url> | grep -c 'pv-brent'`, browser readout probe), then treat your
proposal zone as a witness doc. On 2026-08-06 the v3 paradox engine (8 sliders /propa/,
4 sliders /malaysia/, both cross-linked at `#subsidy-paradox`) was already live before my
inject landed. Three build versions (v1 static → v2 calibrated → v3 signal-dense) were
all superseded. The correct move: **reconcile, don't re-inject.**

Probe first → reuse if possible → build parallel only if reuse fails.

### Live-engine debugging — silent IIFE death + Node validation (2026-08-06)

Two traps that cost real time on the paradox engine build:

**IIFE scope trap kills the engine silently.** `for(let lo=40,hi=125,i=0;i<30;i++){...} return Math.round(lo);` — `lo` is block-scoped to the for loop; returning it outside throws ReferenceError which kills the whole IIFE with **no visible page error**. Symptom: static HTML values render but JS-updated readouts stay `–`. Declare `let lo=40,hi=125` BEFORE the loop. Diagnose by probing one readout in browser console; if static but not dynamic, the engine IIFE died at parse/run.

**Validate injected JS with Node, not Python.** Python `compile()` rejects Unicode box-drawing chars (═ ─) in JS comments → false syntax errors on every script containing decorative comment rules. Use Node, skipping `application/ld+json` blocks (JSON data, not executable JS):
```bash
node -e '
const fs=require("fs"); const html=fs.readFileSync("file","utf8");
const re=/<script(?![^>]*type="application\/ld\+json")[^>]*>([\s\S]*?)<\/script>/g;
let m; while((m=re.exec(html))){ const b=m[1]; if(b.trim().length<200) continue; new Function(b); }
console.log("OK");'
```

### Arif's brand preference: "ARIF FAZIL" (Arif correction 2026-08-07)

Arif explicitly said: *"I prefer. ARIF FAZIL"* — the brand on all pages is **ARIF FAZIL** (uppercase, masthead wordmark, nav logo, footer anchor). The full legal name "Muhammad Arif bin Fazil" appears ONLY inside the identity footer block (the 3-column "Forged by" section at the bottom of each essay page). Never in body headers, nav links, or the hero. This applies to both `/words/writing/` essays and MakcikGPT articles.

### Arif's language preference: "bangang" vs "stupid" (Arif correction 2026-08-07)

Arif corrected: *"I mean change on the site. BANGANG and stupid is different meaning"*

- **English prose essays** (`/words/writing/`): use **"stupid"** (standard English). "Bangang" is Bahasa Malay slang and does not belong in English body text. Sibling agents have silently substituted "bangang" into English prose ("Why Institutions Become Bangang") — always check and restore "stupid" if this drift appears.
- **Bahasa Makcik essays** (`/world/makcikgpt/`): **"bangang" is correct** — it is the author's intentional BM civic-journalism voice. Do NOT replace with "stupid" in MakcikGPT body text or tag names. Some MakcikGPT slug names legitimately contain "bangang" (e.g. `chennah-bangang`, `dap-8-tahun-bangang`) — those are author-named and stay.

### Arif's editorial bar: multimodal audit before designing (2026-08-07)

Arif rejected the first attempt at `/words/writing/` because the static
prebuild pages were plain HTML — they looked worse than `/world/makcikgpt/suara-terlalu-siap`.
His exact phrasing: *"Can u please audit live and do multimodal audit. I mean
this page is nicer then whatever u do just now https://arif-fazil.com/world/makcikgpt/suara-terlalu-siap"*

**Embedded preference (Arif, first-class signal):**
- When upgrading a surface, ALWAYS run `browser_vision` against both the
  target AND a peer reference before designing. Do not ship a design until
  it passes the peer-parity check — Arif will reject it and force a re-do.
- When the user references a URL, the visual standard is implicit: the
  referenced page IS the design contract. Open it, screenshot it, study the
  components (hero, tag pills, claim register, Continue Reading), and clone
  the design language into the new surface.
- "Audit live and do multimodal audit" is a recurring pattern — pair
  `browser_navigate` (for content/structure) with `browser_vision` (for
  visual/typography/palette) before declaring any surface ready. Visual
  regressions are silent if you only check HTTP 200.
- Reference surface for /words/* design language: `/world/makcikgpt/<slug>`
  (sibling corpus with full hero + claim-register + Continue-Reading
  components — see `references/makcikgpt-design-audit-2026-08-07.md`).
- Reference surface for `/propa/*` + `/malaysia/*` interactive engines:
  the live v3 paradox engine — see "Live interactive engine replaces static
  charts" pitfall below.

### Upgrade, not replace (Arif, verbatim)
Pages carry soul content (MakcikGPT masthead, columns, VITALS doors). Never wholesale-replace a page's identity — preserve existing content below the fold or keep its links. A revamp that deletes the soul is a failed revamp.

### Check alignment before deploy (Arif)
Run the gate + dry-run BEFORE `--apply`. Arif expects the agent to self-verify; a deploy that skips the gate is a violation.

### verify-pages reports LIVE state
Pre-existing orphan pages (`/oil/world/`, `/gas/world/`, `/world/sot/` were 404s in Aug 2026) block the gate independent of your change. Do NOT edit `verify-pages.sh` INTENTIONAL_EXCLUSIONS to make the gate pass — fix routing (`_redirects` / Caddy) or document the orphan.

### verify-pages garbled HTTP code (2026-08-07, "HTTP 200000")

The gate sometimes prints an HTTP code like `200000` — that's not a real response code, it's `200` (real) concatenated with `000` (curl failure fallback from `|| echo "000"`). Happens when curl's writeout format produces 200 for the actual response but the script's error-capture also writes 000. Confusing to read — looks like a real failure when it's actually a 200 plus a transient timeout.

**Detection:** any HTTP code ≥ 4 digits (200000, 500000, 301000) in gate output is a script artifact, not a real failure. Re-probe the path directly:
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://arif-fazil.com/<path>/
curl -sIL https://arif-fazil.com/<path>/ | head -3
```
If both report a real 3-digit code, the path is fine. The gate printed garbage.

**Don't fix the gate without checking live first.** Reading "FAIL · /geox/workspaces/ · HTTP 200000" while `curl -sI` returns clean 200 is a false-positive bug in the gate's HTTP code construction (likely the `|| echo "000"` fallback appending after a successful exit). Leave the gate alone unless you can reproduce the failure live — false-positives get quietly ignored and the gate stays trustworthy. False-negatives (gate says PASS but live returns 404) are the dangerous class.

### Caddyfile root path ≠ /var/www/html/<slug>/ — THREE webroots exist (2026-08-06, updated 2026-08-12)
The `arif-fazil.com` Caddyfile is complex — different routes point to different roots.
**Some routes serve from `/var/www/html/<slug>/` (old paths), some from `/var/www/html/arif/<slug>/` (new paths), and some from `/var/www/html/world/<slug>/` (legacy world root).** If you edit the wrong one, nothing changes live even after Caddy reload.

**REPORTED 2026-08-12. Stale as of 2026-10-13.** Re-probe before acting. Do not reload Caddy. Do not copy `/world/economics/` over the live oil or gas page. The table below is the August scar:

| Route | Actual root on disk | Notes |
|---|---|---|
| `/world/economics/{gold,oil,gas,klci,usdmyr}/` | `/var/www/html/world/economics/{slug}/` | **THE CANONICAL LIVE ROOT** (Aug 2026 update) |
| `/gold/`, `/oil/`, `/gas/`, `/klci/`, `/usdmyr/` | 308 redirect → `/world/economics/{slug}/` | So editing `/var/www/html/arif/{slug}/` has NO effect on the live page |
| `/propa/*` | `/var/www/html/arif/propa/` (or `/var/www/html/world/propa/`) | Check both |
| `/syedos/*`, `/emas/*` | `/var/www/html/syedos/{emas,heal}/` |
| `/aaa/*` | `/var/www/html/aaa/` |
| `/_shared/*` | `/var/www/html/_shared/` | Used by unified-header-loader.js, zen.css, etc. |

**TRIPLE-WEBROOT TRAP (2026-08-12):** `/oil/` → 308 → `/world/economics/oil/`. The file at
`/var/www/html/arif/oil/index.html` is NOT served live — it's shadowed by the redirect. The
ACTUAL served file is at `/var/www/html/world/economics/oil/index.html`. If you edit only
`/var/www/html/arif/oil/`, verify with `curl -s https://arif-fazil.com/world/economics/oil/`
NOT `curl -s https://arif-fazil.com/oil/` (the latter follows the redirect and shows the
world/economics copy). **Always grep the LIVE HTML after editing to confirm the change landed.**

**Detection:** `grep -E 'root \*' /etc/caddy/Caddyfile | head -20` — shows which route maps to which root.
**Fix:** always `grep` the Caddyfile for the exact path BEFORE editing any HTML. Edit the path Caddy ACTUALLY serves.

### Cloudflare CDN serves stale despite `Cache-Control: no-cache` (2026-08-06)
Even when the Caddyfile has `header Cache-Control "no-cache, no-store, must-revalidate"`, Cloudflare edge may hold the old HTML if you edited the wrong disk path (see above). Once the correct path is updated, Cloudflare fetches fresh on the next request (no purge needed — `cf-cache-status: DYNAMIC`).

### `/_shared/` assets must be synced to `/var/www/html/_shared/` (2026-08-12, 90 min wasted)
**Pages link `/_shared/zen.css`, `/_shared/economics.css`, etc. Caddy resolves `/_shared/*`
from `/var/www/html/_shared/`.** But the repo source lives at
`/root/arif-fazil.com/sites/shared/`. The `deploy-site.sh` script does NOT sync `sites/shared/`
→ `/var/www/html/_shared/`. So new/updated CSS files sit in the repo but never go live.

**Symptom:** commodity pages render as completely unstyled raw text. Header has no dark
background, cards have no borders, buttons have no styling. The CSS link returns HTTP 404.

**Detection:** `curl -sI https://arif-fazil.com/_shared/<file>.css` → 404 + `content-length: 0`
means the file is missing from `/var/www/html/_shared/`. If the file IS there but still 404,
it's a **stale Cloudflare edge cache** of the previous 404 — append `?cb=$(date +%s)` to bust
the cache.

**Fix:**
```bash
# Sync ALL shared assets from repo to live webroot
cp /root/arif-fazil.com/sites/shared/*.css /var/www/html/_shared/
cp /root/arif-fazil.com/sites/shared/*.js /var/www/html/_shared/
chown -R www-data:www-data /var/www/html/_shared/
# Verify
curl -sI "https://arif-fazil.com/_shared/zen.css?cb=$(date +%s)" | head -3
```

**Cloudflare stale-404:** CF caches 404s. Adding `?v=<timestamp>` to the CSS link in the HTML
forces CF to re-fetch. Update `<link href="/_shared/zen.css?v=20260812T152400Z">` in the
commodity pages. CF will eventually expire the stale 404 naturally, but cache-busting is the
immediate fix.
All 5 market pages load `/_shared/zen-market.js` (858 lines) which fetches from the WEALTH snapshot APIs, populates pulsePrice/pulseDelta/biasPill/maVerdict/pulseLevels/macroTicker, and renders the full chart. **If the hero shows `—` or stale numbers, the issue is NOT dead JS — it's stale prose residue above the hero or CDN cache.** The fix is to strip hardcoded digest/paragraph blocks from the page shell, not to rewire the JS engine.

**WEALTH snapshot endpoints (all live, 2026-08-06):**
- `/gold/api/snapshot` — XAUUSD price, RSI, EMA20/50/200, signal, confidence, S/R
- `/gold/api/history?interval=<tf>&period=<p>` — candles + EMA series + RSI series
- `/gold/api/apex` — G score, C_dark, dS, regime, verdict
- `/oil/api/snapshot` — Brent
- `/gas/api/snapshot` — NatGas
- `/klci/api/snapshot` — FBMKLCI (includes EWM, OPR)
- `/usdmyr/api/snapshot` — Ringgit FX (includes stress_band, mean_90d, SGD-MYR, rate differential)

**Nav canon trap:** links point to `/usdmyr/`, not `/usmyr/`. There is no `/usmyr/` directory. 404 if you guess.

### Caddy routing order
`@static_dirs` (explicit path list) matches BEFORE `@spa_routes`. `@static_dirs` does `try_files {path} {path}/ =404` — no `index.html` fallback. A new subpage needs BOTH the file in webroot AND a route/redirect.

### Caddy `{uri}` is FULL URI — use `{0}` for wildcard capture (2026-08-07, 15 min)
In Caddy `redir` directives, `{uri}` expands to the **entire** request URI (e.g. `/writing/the-agi-paradox`). `{0}` expands to the first `*` wildcard segment (e.g. `the-agi-paradox`). Using `{uri}` in a wildcard redirect like `redir /writing/* /words/writing/{uri} 308` produces `/words/writing//writing/the-agi-paradox` — the `/writing/` prefix is doubled.

**Correct pattern:**
```caddyfile
redir /writing/* /words/writing/{0} 308   # ✓ {0} = wildcard capture
redir /writing/* /words/writing{uri} 308   # ✗ {uri} = full URI, produces double path
```

**Detection:** `curl -sIL https://arif-fazil.com/<legacy>/<slug> | grep location` — if you see `location: /words/writing/writing/` (doubled path) or empty slug, you have this bug.

**However:** even `{0}` may silently produce an empty value depending on Caddy version. The safest approach for legacy path redirects is to **only redirect the top-level path** (`redir /writing /words/writing/ 308`) and let the SPA handle slugs via the existing `/writing/:slug` route in React Router — don't try to transform the slug in Caddy at all.

### Adding a nav-canon path to the SPA (2026-08-07)
To publish under a new nav-canon URL like `/words/*` (vs legacy `/writing/*`):

1. **App.tsx** — add a route: `<Route path="/words/writing/:slug" element={<EssayPage />} />` (keep legacy `/writing/:slug` for backward compat).
2. **Caddyfile `@spa_routes` matcher** — add `/words*` (and `/work*` etc.) to the matcher list. Without this, requests for `/words/writing/<slug>/` land in `@static_dirs` (which has no SPA fallback → 404) instead of falling through to `@spa_routes` (which serves `index.html` for SPA rendering).
3. **Reorder rule:** `@spa_routes` must list the new path BEFORE more specific static-shell paths, or the static shell wins. Caddy matchers are first-match-wins by ordered appearance.
4. **Reload:** `sudo caddy validate --config /etc/caddy/Caddyfile` then `sudo systemctl reload caddy` (reload preserves peers; never restart).

### Live webroot drifts from dist/
If `dist/` has files the live site 404s on, the deploy hasn't synced yet — deploy, then re-run the gate.

### Editing dist/ is futile — public/ is the source-of-truth for static HTML (2026-08-11)
**`copy-static-html.js` mirrors `public/` → `dist/` during `npm run build`.** Any hand-edit to `dist/<path>/index.html` gets clobbered on the next build. Always edit `public/<path>/index.html` instead. **Proved on `/constitution/`**: edited dist/, the file survived briefly (sha256 confirmed), then copy-static-html overwrote it with a regenerated version from public/ — the dist/ hash changed from `175b1e85...` to `b20359e1...` and the meta text became a different (third-party) variant.

**Detection:** if your sha256 changes after any build on a file you edited in dist/, this pitfall hit you. Symptom check: `grep copy-static-html package.json` — if present in postbuild, dist/ is derived, public/ is source. Also `cat scripts/copy-static-html.js | head -30` to see what it mirrors.

**Fix path:** edit `public/<path>/index.html` (the canonical source), then `npm run build` regenerates dist/ correctly. The T1 `.bak` you made of the old dist/ is still useful as a witness, just don't expect it to drive live behavior.

### .bak naming convention for T1 reversible edits (2026-08-11)
When backing up a file before mutation, use UTC timestamps:
```
index.html.bak-20260811T060135Z
```
Two formats seen on disk and both work:
- New (preferred): `<name>.bak-YYYYMMDDTHHMSSZ` — sortable, parseable, no prefix needed
- Legacy: `<name>.bak-pre-<change-tag>-YYYYMMDDTHHMSS` (e.g. `index.html.bak-pre-hero-20260807T033116`)

Single `cp` reverts:
```bash
cp file.html.bak-20260811T060135Z file.html
```
The UTC timestamp is the key element (timestamp sorting + timezone clarity). Capture state BEFORE any mutation — never after.

### Renaming an agent_shells path (e.g. `/vitals/` → `/propa/`) — full recipe (2026-08-06)
To move an agent_shells path to a new canonical URL while preserving backward compat:

1. **Caddyfile** — add new path to `@agent_shells`, add 308 redirect from old to new:
   ```caddyfile
   redir /vitals /propa/ 308
   redir /vitals/ /propa/ 308
   ```
   The new path goes in `@agent_shells` AFTER existing paths (Caddy matchers are first-match-wins by ordered appearance).

2. **Source HTML** (`public/<old>/index.html`) — replace old references with new (canonical link in JSON-LD, `href` attrs). Re-run `render-vitals.cjs` to regenerate `dist/<old>/index.html` AND copy to `dist/<new>/index.html`.

3. **Nav canon** (`src/data/navCanon.ts`, `src/data/missions.ts`) — swap the `href` from `/<old>/` to `/<new>/` so the navbar reflects the new canonical.

4. **`public/_redirects`** — keep both files in sync with the Caddyfile dir as the convention:
   ```
   /propa        /propa/index.html         200
   /propa/       /propa/index.html         200
   /propa/*      /propa/:splat             200
   /vitals       /propa/                   308
   /vitals/      /propa/                   308
   ```

5. **Live sync** — `rsync -av dist/<new>/ /var/www/html/arif/<new>/` (no `--delete`) then `cp dist/<old>/index.html /var/www/html/arif/<old>/index.html` (keep old serving same content during transition window).

6. **Reload Caddy** is T3. Do not run `sudo systemctl reload caddy`. The `/vitals/` → `/propa/` direction in this recipe is the August scar. October is the reverse. Do not reverse the live redirects.

### MakcikGPT article publishing — FOUR registers + generator (2026-08-09)

Publishing a MakcikGPT article under `/world/makcikgpt/<slug>/` touches **four** places. Skip any and the article is invisible to browsers or bots. Full recipe: `references/makcikgpt-article-registration-2026-08-09.md`.

1. **`src/data/makcikgpt/<slug>.ts`** — ArticleContent interface (`slug` + `html` template literal). The `html` field contains ONLY the article body (no cover/header — the SPA renders those from meta). Must escape backticks and `${` for JS template literal.
2. **`src/data/makcikgpt/index.ts`** — THREE edits: (a) `import <name> from './<slug>'`, (b) add to `makcikArticleModules` array, (c) add full `MakcikArticleMeta` object to `makcikArticlesMeta` array (slug, title, subtitle, date, domain, language, excerpt, tags, seal).
3. **`src/data/essays.json`** — add entry with `id`, `title`, `date`, `lang: "bm"`, `series`, `tags`, `dest: { type: "onsite", path: "/world/makcikgpt/<slug>" }`, `seal: "999"`. This is the generator source-of-truth for feed.xml, sitemap, llms.txt, and `generate-makcik-articles.cjs`.
4. **`public/makcikgpt-md/<slug>.html`** — bot-serving static HTML. Generated by `node scripts/generate-makcik-articles.cjs` (reads essays.json + .ts files). Do NOT hand-write — run the generator.

**Skip `essays.json` → generator won't create bot HTML, feed/sitemap won't list it. Skip `index.ts` → SPA renders "Article Not Found". Skip `.ts` file → SPA has no body content.**

**Static-page CSS classes don't exist in SPA.** When extracting HTML from a static makcikgpt page for SPA registration, transform: `.question` divs → `<blockquote>`, `.makcik-fact` grid divs → inline-styled flex rows (SPA has no global `.makcik-fact` CSS), `.makcik-closing` → inline `border-top` div. The SPA's `essay-content prose-invert` handles `p`, `h2`, `strong`, `em`, `blockquote`, `ul`, `li` natively.

**Nested-div regex trap.** When extracting `.makcik-fact` blocks, a naive `<div class="makcik-fact">(.*?)</div>` regex stops at the first nested `</div>` (the `.angka` closer), producing broken content. Use nesting-aware regex: `<div class="makcik-fact (void|sabar)">\\s*<div class="angka">(.*?)</div>\\s*<div class="fakta">(.*?)</div>\\s*</div>`.

**Deploy uses `--delete`.** `deploy-site.sh` rsyncs with `--delete`. Files in `/var/www/html/arif/makcikgpt-md/` not in `dist/makcikgpt-md/` are wiped on next deploy. Always run `npm run build` (which mirrors `public/makcikgpt-md/` → `dist/makcikgpt-md/` via `copy-static-html.js`) BEFORE deploying.

**Verification (three surfaces):**
```bash
# 1. SPA browser — should render full article (not "Article Not Found")
# Use browser_navigate + snapshot
# 2. Bot branch — GPTBot UA should get static HTML
curl -sI -H "User-Agent: GPTBot" "https://arif-fazil.com/world/makcikgpt/<slug>" | head -3
# 3. Landing page — article should appear in card grid
curl -s "https://arif-fazil.com/world/makcikgpt/" | grep -c "<slug>"
```

### MakcikGPT pre-publish audit — 5-gate verification protocol (2026-08-09)

When Arif says artikel dah live and you need to verify: **always check all five gates**. Never trust a single HTTP 200 from curl alone — that only proves the bot branch works.

| Gate | What | How | What fails if skipped |
|------|------|-----|----------------------|
| **G1 — HTTP 200** | Server returns status code | `curl -sfL https://arif-fazil.com/<path>/ -o /dev/null -w "%{http_code}"` | Nothing (but trivially fast) |
| **G2 — Title fidelity** | `<title>` matches expected | `grep -oE '<title>[^<]+</title>' response.html` | Wrong page indexed by search |
| **G3 — Browser rendering** | Real Chrome sees content | `browser_navigate` + snapshot — look for "ARTICLE NOT FOUND" | **MOST CRITICAL** — SPA-only articles pass curl but show DEAD END to humans |
| **G4 — Landing page index** | Slug listed on `/world/makcikgpt/` | `grep -c "<slug>" /var/www/html/arif/makcikgpt-md/index.html` | Article is live but undiscoverable from navigation |
| **G5 — Content sanity** | Numbers match source docs | Cross-reference key figures against FRA/IR PDF excerpts | Credibility loss when readers catch fabricated/inaccurate numbers |

**G3 is the killer gate.** Many articles pass G1-G2 (HTTP 200, correct title) but fail G3 because the slug isn't registered in the SPA bundle. Symptom: curl returns article content, browser shows "ARTICLE NOT FOUND". Anyone sharing the link on WhatsApp/Telegram gets a dead end.

**Root cause of G3 failure:** Publishing creates the `.ts` file and static HTML but forgets to register the slug in `src/data/makcikgpt/index.ts` (the import + array insertion). The SPA doesn't know the slug exists → renders default "Not Found" component.

**If G3 fails after publish, fix by editing `src/data/makcikgpt/index.ts`:**
```typescript
// ADD import at top:
import <name> from './<slug>';

// ADD to makcikArticleModules array:
// [..., <name>, ...]

// ADD to makcikArticlesMeta array:
// { slug: '<slug>', title: '...', subtitle: '...', date: 'YYYY-MM-DD', domain: 'politics', language: 'bm', excerpt: '...', tags: [], seal: '999' },

// Save → npm run build → deploy-site.sh --apply → re-probe G3
```

### MakcikGPT authoring voice — Bahasa Kampung, NOT Accounting (2026-08-09)

Arif explicitly rejected accounting-language MakcikGPT prose: *"Ni bahasa accounting la weiii. Cakap macam makcik kampung."*

**Voice rules:**
- **Every financial figure MUST come with a kampung/stall analogy.** Revenue down? → compare to kedai runcit makin kurus. Dividend drain? → compare to taking full salary while the shop shrinks. Bond issuance? → borrowing to pay yourself.
- **Short sentences.** Max 1-2 clauses. Questions as paragraph starters. Rhetorical questions as section openers.
- **"Makcik" voice = curious elder auntie at pasar malam**, not corporate analyst. Uses "kau" (informal you). Direct address throughout. Not deferential.
- **No jargon.** If you use "capex" explain it in the next sentence. If you say "payout ratio," immediately translate to English/Malay equivalent ("berapa banyak untung yang keluar sebagai dividen").
- **Punch endings.** Each numbered point ends with a rhetorical question or sharp statement, not a summary.
- **Avoid corporate framing words:** "optimized," "portfolio rebalancing," "value preservation," "disciplined capital allocation" — these ARE the lie Makcik is exposing. Translate them: "cleaning balance sheet" → "jual aset untuk bayar diri sendiri."

**Example — BAD (accounting-speak):**
> "CAPEX declined 23% year-over-year indicating reduced investment capacity."

**Example — GOOD (kampung voice):**
> "Kalau kau ada kedai, dan setiap bulan kau beli barang makin kurang — tapi kau tetap ambil gaji penuh — satu hari kedai tutup. Macam tu PETRONAS sekarang."

**Pre-publish checklist for voice:**
1. Read the draft aloud. Does it sound like someone talking TO you over kopi, or reading FROM a boardroom slide deck?
2. Every number ≥ RM1 billion MUST have an accompanying analogy in the next 1-2 sentences.
3. No bullet-point lists longer than 3 items — break them into narrative paragraphs.

### Content fact-verification against primary sources (2026-08-09)

**NEVER write numbers into a draft from memory or estimation.** Every financial figure must be verified against the PRIMARY SOURCE DOCUMENT before inclusion in any article.

**Verification protocol:**
1. **Identify the primary source** for the article's topic:
   - PETRONAS financials → `PETRONAS Integrated Report FY20XX` or `PETRONAS Group FRA FY20XX` PDF (hosted at petronas.com)
   - Government data → Bank Negara Malaysia reports, Ministry of Finance statements
   - Market data → Bloomberg, Reuters, The Edge Malaysia, Free Malaysia Today
2. **Download/open the source PDF** using `web_extract(urls=[source_pdf_url])` or `browser_navigate` for interactive pages.
3. **Search for each specific figure** mentioned in the draft. Record exact values from the source.
4. **Compare draft numbers against source.** Even small discrepancies (e.g., RM52B vs RM54.2B for capex) discredit the entire article when caught.
5. **Flag unverifiable claims.** If a figure can't be found in any public document, mark it as `[SPEC]` (speculation) or remove it.

**Known primary sources for PETRONAS articles:**
- Financial Performance PDF: `https://www.petronas.com/integrated-report-2025/assets/pdf/by-section/8_PETRONAS_IR25_FinancialPerformance.pdf`
- FRA PDF: `https://www.petronas.com/sites/default/files/uploads/content/2026/PETRONAS%20Group%20FRA%20FY2025%20-%20Financial%20Operational%20Report.pdf`
- Press release: `https://www.petronas.com/media/media-releases/petronas-posts-lower-profit-amid-market-headwinds-strengthens-resilience`
- News coverage: The Edge Malaysia (`theedgemalaysia.com`), Free Malaysia Today (`freemalaysiatoday.com`)

### Number-timeline accuracy — critical for leadership pieces

When writing about executive tenures, contract extensions, or succession:
- **Verify the EXACT contract number** (kali pertama/kedua/ketiga) by checking news sources. Drafts containing "kali kedua" when it's actually "kali ketiga" lose credibility instantly.
- **Check source dates carefully.** Contract expiry months, announcement months, and extension start dates must align. A common error: confusing the announcement month with the effective start month.
- **For appointment chains, map the sequence:** predecessor name → transition date → successor appointment date → first extension → second extension → third extension. Verify each against at least two independent sources.

**Quick verification command for PETRONAS CEO tenure:**
```bash
# Search recent news for Tengku Taufik contract details
curl -s "https://news.google.com/search?q=Tengku+Taufik+PETRONAS+contract+extension&hl=en-MY&gl=MY&ceid=MY:en" | \
    grep -oiE '[0-9]+ extension|kali [ke-]?[0-9]+' | sort -u
```

### MakcikGPT article publishing — FOUR registers + generator (2026-08-09)

Publishing a MakcikGPT article under `/world/makcikgpt/<slug>/` touches **four** places. Skip any and the article is invisible to browsers or bots. Full recipe: `references/makcikgpt-article-registration-2026-08-09.md`.

1. **`src/data/makcikgpt/<slug>.ts`** — ArticleContent interface (`slug` + `html` template literal). The `html` field contains ONLY the article body (no cover/header — the SPA renders those from meta). Must escape backticks and `${` for JS template literal.
2. **`src/data/makcikgpt/index.ts`** — THREE edits: (a) `import <name> from './<slug>'`, (b) add to `makcikArticleModules` array, (c) add full `MakcikArticleMeta` object to `makcikArticlesMeta` array (slug, title, subtitle, date, domain, language, excerpt, tags, seal).
3. **`src/data/essays.json`** — add entry with `id`, `title`, `date`, `lang: "bm"`, `series`, `tags`, `dest: { type: "onsite", path: "/world/makcikgpt/<slug>" }`, `seal: "999"`. This is the generator source-of-truth for feed.xml, sitemap, llms.txt, and `generate-makcik-articles.cjs`.
4. **`public/makcikgpt-md/<slug>.html`** — bot-serving static HTML. Generated by `node scripts/generate-makcik-articles.cjs` (reads essays.json + .ts files). Do NOT hand-write — run the generator.

**Skip `essays.json` → generator won't create bot HTML, feed/sitemap won't list it. Skip `index.ts` → SPA renders "Article Not Found". Skip `.ts` file → SPA has no body content.**

**Static-page CSS classes don't exist in SPA.** When extracting HTML from a static makcikgpt page for SPA registration, transform: `.question` divs → `<blockquote>`, `.makcik-fact` grid divs → inline-styled flex rows (SPA has no global `.makcik-fact` CSS), `.makcik-closing` → inline `border-top` div. The SPA's `essay-content prose-invert` handles `p`, `h2`, `strong`, `em`, `blockquote`, `ul`, `li` natively.

**Nested-div regex trap.** When extracting `.makcik-fact` blocks, a naive `<div class="makcik-fact">(.*?)</div>` regex stops at the first nested `</div>` (the `.angka` closer), producing broken content. Use nesting-aware regex: `<div class="makcik-fact (void|sabar)">\s*<div class="angka">(.*?)</div>\s*<div class="fakta">(.*?)</div>\s*</div>`.

**Deploy uses `--delete`.** `deploy-site.sh` rsyncs with `--delete`. Files in `/var/www/html/arif/makcikgpt-md/` not in `dist/makcikgpt-md/` are wiped on next deploy. Always run `npm run build` (which mirrors `public/makcikgpt-md/` → `dist/makcikgpt-md/` via `copy-static-html.js`) BEFORE deploying.

**Verification (three surfaces):**
```bash
# 1. SPA browser — should render full article (not "Article Not Found")
# Use browser_navigate + snapshot
# 2. Bot branch — GPTBot UA should get static HTML
curl -sI -H "User-Agent: GPTBot" "https://arif-fazil.com/world/makcikgpt/<slug>" | head -3
# 3. Landing page — article should appear in card grid
curl -s "https://arif-fazil.com/world/makcikgpt/" | grep -c "<slug>"
```

### Essay publish wiring — FIVE registers + Caddy routing (verified 2026-08-07)
Publishing a direct-publication essay touches **five** places, plus a Caddyfile routing requirement. Skip any and the essay won't render or list:

1. **`src/data/essays/<NN>-<slug>.ts`** — hand-authored content file (`EssayContent` interface: title, date, slug, tags, excerpt, mediumUrl, html). Filename carries the essay number prefix (e.g. `24-the-agi-paradox-...ts` → imported as `e24`). Direct publications get `isDirectPublication: true` + `mediumUrl` pointing at the site URL. Entries with `hasContent: false` in articles.json are Medium-linked stubs served by auto-generated `g*` modules — don't hand-author those. **The `.ts` file is the source of truth for actual HTML content.**
2. **`src/data/essays/articles.json`** — slug list; insert at TOP (newest first) with `"hasContent": true, "isDirectPublication": true`. **NOT a reliable filter for what to render** — many direct-publication `.ts` files don't have `isDirectPublication: true` in `articles.json` (the field was added later). The prebuild script must read content from `.ts` files, not filter by `articles.json`.
3. **`src/data/essays/index.ts`** — FOUR edits in one file: (a) `import e24 from "./24-..."`, (b) add `e24` to `essayModules` array, (c) add full meta object to `allEssays` array, (d) add slug to `CURATED_SLUGS` under the right domain (e.g. "AI Governance") so it appears in curated domain views.
4. **`public/words/writing/index.json`** — the static-shell listing. After the Aug 2026 nav reorg this lives at `public/words/writing/`; there is NO `public/writing/` directory. Add item at top with `"risk_level": "INT"`, `"epoch"` etc.
5. **`src/App.tsx`** — SPA route. Canon v7 URL is `/words/writing/:slug`; legacy route `/writing/:slug` must stay for backward compat. Add BOTH: the `/words/writing/:slug` line as a second `<EssayPage />` route. App.tsx alone is NOT enough — see Caddy routing item below.
6. **`/etc/caddy/Caddyfile`** — the `@spa_routes` matcher MUST include `/words*` (and `/work*`) so the SPA shell (`index.html`) is served for paths under `/words/*`. Without this, paths like `/words/writing/<slug>/` land in `@static_dirs` which has no SPA fallback → 404. See "Caddy routing order" pitfall.

**Skip `articles.json` → bundled but SPA listing won't link it. Skip `words/writing/index.json` → static-shell index won't list it. Skip `CURATED_SLUGS` → missing from curated domain views. Skip App.tsx `/words/writing/:slug` route → SPA shell loads but router can't match slug.

**Source-of-truth rule (revised 2026-08-07):** the `.ts` file with `isDirectPublication: true` AND a real HTML body (≥200 chars after extraction) is what the prebuild script renders. `articles.json` is metadata hints only. Filtering by `articles.json.isDirectPublication` will silently skip essays that have real content but are missing the field — script must dedupe by slug AND require non-empty html body.

**Verifying a live essay URL:** curl shows 308 (trailing-slash) → 200 with SPA shell; essay body is client-rendered so `grep` for the title in curl output fails even when live. Don't declare 404 from curl on a router-handled path — verify with `browser_navigate` + snapshot (title + section headings) before concluding the page is down.

**Dedupe multiple `.ts` files per slug:** legacy + new essay files may share a slug (e.g. `26-the-third-axis-of-failure.ts` + `26-the-third-axis-of-failure-what-acemoglu-missed.ts`). The prebuild script must dedupe by slug — first occurrence by filename length wins (canonical shorter filename preferred over renames). If a `.ts` file is deleted but `index.ts` still imports it, `tsc -b` fails the build with `Cannot find module`. Always remove the import line from `index.ts` when deleting the source file.

### Agent-chrome creep — every "small addition" turns a journalism brand into a GitHub repo (2026-08-11)

The most pernicious failure mode on arif-fazil.com is not a single big mistake — it's
the slow accumulation of small "helpful" additions that serve agents, not humans.

**Symptoms** (any one = this pitfall hit the page):
- Page header has a line like "Canonical landing: <path>"
- A 3-column info card: "WHERE AM I? | WHY CARE? | WHAT NEXT?"
- Footer with: "Source of truth: src/data/essays.json. Rendered by scripts/<x>.cjs."
- Multiple `[OBS] [DER] [INT] [SPEC]` tags visible to humans (these belong in agent metadata only)
- Every list item carries "· seal 999" suffix
- Footer has: "llms.txt · missions.json · surfaces.json" — bot metadata leaking into visual surface

**The drift trail (proven on `/world/makcikgpt/` between 2026-07-31 and 2026-08-11):**

| State | Date | Commit | Header chrome |
|---|---|---|---|
| **Primer Dark** | 2026-07-31 | `767596c` | Hero + stats + quote + 5 series cards (clean) |
| **HUMAN_FIRST chrome** | 2026-08-04 | `34fed66` | + epistemic tags, pairings, "read next" navigation |
| **Zen Pulse agent-nav** | 2026-08-08 | `3fe612d` | + "WHERE AM I? WHY CARE? WHAT NEXT?" zen-pulse card |
| **Source-of-truth footer** | 2026-08-10 | `051d799` | + "Source of truth: src/data/essays.json" |

Each change was "small." Combined: a journalism brand became a GitHub repo.

**Arif's rejection (verbatim, 2026-08-11):** *"Buruk. Aku x mau ni. deep archive extraction."*

**The fix is three layers deep:**

1. **Canonical SOT** — `/root/arif-fazil.com/sites/arif-fazil.com/DESIGN_INVARIANTS.md` declares what is and isn't allowed in visual surfaces. Read this BEFORE touching any visual HTML.
2. **Auto-block lint** — `/root/arif-fazil.com/sites/arif-fazil.com/scripts/design-lint.sh` scans every `public/**/*.html` + `src/**/*.{tsx,ts,css}` for the 5 Rein (forbidden chrome strings: `Canonical landing:`, `WHERE AM I?`, `WHY CARE?`, `Source of truth:`, `Rendered by`). Exit 1 on any hit. Wire to `npm run build` prebuild.
3. **Visual recovery** — git archive at `767596c` has the Primer Dark landing template. Use `git show 767596c:sites/arif-fazil.com/makcikgpt/index.html` to extract.

**The 3-second human test:** within 3 seconds of landing, a human reader knows what this page is, why they should care, and what to do next — without reading any tag labels, source paths, or federation jargon. If the page fails this, redesign it.

**Visual chrome that IS allowed:**
- Hero text with persona voice
- Persona signature footer ("MAKCIKGPT · DITEMPA BUKAN DIBERI")
- Series badges with semantic meaning
- Date stamps in human-readable form
- 999 SEAL stamp in hero or footer
- Site links in footer (max 4: HOME / WORLD / LLMS.TXT / DOCTRINE)

**Metadata for agents must use:**
- `<link rel="alternate" type="application/json" href="...">` (head, invisible)
- `<meta name="..." content="...">` (head, invisible)
- `data-*` attributes (machine-only, never displayed)
- Separate `/llms.txt`, `/.well-known/*.json`, `sitemap.xml` (their own surfaces)

**When restoring archived designs:**
- Primer Dark landing: `git show 767596c:sites/arif-fazil.com/makcikgpt/index.html`
- Original chat interface: `git show 696f734:sites/arif-fazil.com/makcikgpt/index.html`
- Minimal essay page: `git show 75dcd84:sites/arif-fazil.com/src/pages/EssayPage.tsx`
- Archived articles: `git show 767596c:sites/arif-fazil.com/public/makcikgpt-md/<slug>.html`

**Companion skill:** `makcikgpt-archived-designs` — full archive extraction recipe + the Primer Dark token palette + the inject-article-styles.sh pattern.

### Article HTML has NO inline CSS by default — articles render as white background (2026-08-11)

`prerender-articles.cjs` uses puppeteer to render SPA pages into static HTML in
`/root/arif-fazil.com/sites/arif-fazil.com/dist/makcikgpt-md/<slug>.html`. The script
writes the article HTML body + meta tags + JSON-LD, but **does NOT inject a `<style>`
block**. The HTML has cover chrome (`<div class="cover">`, `cover-emoji`, `cover-kicker`,
`cover-title`, `cover-subtitle`, `cover-byline` with 999 Meterai stamp) but no CSS to
style it.

**Symptom:** articles load as white background with default browser Times New Roman —
visually correct but visually ugly. The user sees the content but in newspaper-style
plain HTML, not the Primer Dark aesthetic they expect.

**Fix:** `scripts/inject-article-styles.sh` (in site repo) injects a `<style>` block
+ Google Fonts link (`Newsreader` serif + `IBM Plex Mono`) into every article's
`<head>`. Idempotent — checks for the sentinel string `MAKCIKGPT ARTICLE — Primer Dark
reader` before injecting. Safe to re-run after regenerations.

```bash
bash /root/arif-fazil.com/sites/arif-fazil.com/scripts/inject-article-styles.sh
# ✓ injected: petronas-dna.html
# ✓ injected: chennah-bangang.html
# ...
# inject-article-styles.sh · injected=82 · skipped=1 · errors=0
```

The `index.html` (landing) is skipped — it has its own styling from
`generate-makcik-index.cjs`.

**When the daemon overwrites your injection:** see "Federation sync daemons overwrite
your static-HTML output" pitfall — re-run after daemon ticks. The injection script is
fast (< 1s for 82 files).

### Renaming an essay title after publish (5 registries, 2026-08-07)

Arif asked to shorten `The Third Axis of Failure: What Acemoglu Missed, Why Institutions Become Stupid, and How Humans, AI, and Organizations Turn Evil` → `Simulative Institutions: The Third Axis of Failure`. The title appears in **five** distinct places that all have to agree or the SPA essay card, the listing card, and the article header show different titles (the worst failure mode — three titles for one essay):

1. **`src/data/essays/<NN>-<slug>.ts`** — the `title:` field (frontmatter of `EssayContent`)
2. **`src/data/essays/articles.json`** — top-level entry's `title` field (machine index, llms.txt consumers)
3. **`src/data/essays/index.ts`** — `allEssays` array (React SPA EssayPage gets title from here at runtime)
4. **`public/words/writing/index.json`** — top-level entry's `title` (machine-readable listing)
5. **`public/words/writing/index.html`** — the `<h2>` inside the article card AND any "Read article →" anchor text

After patching all five: `sed -i 's/OLD TITLE/NEW TITLE/g' public/words/writing/index.html` is the safe one-liner for the HTML — all matches are intentional. Then `npm run build` (vite rebuilds the React SPA bundle with the new `allEssays` data) → `deploy-site.sh --apply` → `rsync -av public/words/writing/index.html /var/www/html/arif/words/writing/` → `md5sum` reconcile → `verify-pages.sh`.

**Limitation:** I cannot edit the essay on Medium itself — `medium.com/@arifbfazil/<slug>-<id>` is bot-gated (403 from sandbox) and requires Arif's authenticated session. Document the title change locally and ask Arif to mirror it on Medium manually, OR set up a Medium-XML-RPC credential bridge first.

**Domain-B leak risk:** if the slug field is changed without updating all five places, the SPA will 404 the essay (slug mismatch between `essayModules` slug and the URL). Always confirm the slug stays the same when editing title — title edits are slug-safe, body edits are NOT.

### Per-essay static HTML generation was REMOVED (2026-08-07, Arif rejected)
Earlier revisions of `scripts/render-words-essays.cjs` generated
`<slug>/index.html` and `<slug>.md` for each essay. **This was rejected** —
per-essay static HTML shadows the SPA `EssayPage` and users see the plain
version instead of the rich SPA design (forge-black hero, tag pills, prose
typography, Continue Reading nav, JSON-LD). The script now generates ONLY:
- `index.html` — listing surface
- `index.json` — machine-readable list
- `llms.txt` — LLM discoverability

If a sibling deploys a richer index with reading-time pills, tag chips,
stat pills, RSS, or author byline — do NOT re-inject. `md5sum` reconcile,
adopt theirs (copy live webroot `index.html` to `public/words/writing/`).
The sibling-built index is canon.

### `@static_dirs` needs SPA fallback for nav-canon paths (2026-08-07)
`@static_dirs` matcher's `try_files {path} {path}/ =404` has NO `{path}/index.html` fallback — a request for `/words/writing/<slug>/` with no exact physical match returns 404 even when `dist/words/writing/<slug>/index.html` exists (the postbuild mirror lands it but `try_files` doesn't fall through to `index.html`). For nav-canon paths that mix static files with subpath routes, change to:

```caddyfile
try_files {path} {path}/index.html {path}/ =404
file_server { index index.html }
```

This serves the physical `index.html` when a subpath matches a directory, before falling through to 404. Without it, the static prerender pages under `/words/writing/<slug>/` 404 even though the file exists at `/var/www/html/arif/words/writing/<slug>/index.html`.

### GDELT from this host
Often times out/429s; from a real user browser it works. Don't conclude the app is broken from sandbox probes — see references.

# ── source: arif-sites-content-ops ──

## Pitfalls — ARCHIVE

The pitfall history for this skill (`## Pitfalls` and `## Additional Pitfalls`, ~31 KB)
now lives in `references/pitfalls-archive.md`, extracted 2026-09-15 because this
SKILL.md had crossed the 100,000-char tool limit and could no longer be patched.

Load the archive when the inline notes here do not cover your situation — in particular
for the 2026-08-01 deploy/cron/Caddy trap set. Find your case with:

```
grep -n -i "<keyword>" <skill_dir>/references/pitfalls-archive.md
# useful keywords: cron, caddy, deploy, nav, redirect, cache, race, build, dirty
```

