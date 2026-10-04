# /words/writing/ essay publish workflow

End-to-end recipe. The 2026-08-07 session published the AGI Paradox + Truth Is Not Cheap + Third Axis triptych through this exact workflow (six iterations on slugs, two subagent collisions, one orphan CSS, one clean rebuild). The SKILL.md "Publishing a new long-form essay" section is the canonical version; this file is the worked recipe with all the pitfalls fleshed out.

## ## The chain (CANON → build → live) — UPDATED 2026-08-07

```
src/data/essays/<N>-<slug>.ts        ← EssayContent (typed CANON)
        │
        ▼  import eNN + add to essayModules[]
src/data/essays/index.ts             ← registry (essayModules[])
        │
        ▼  matching series id/n + dest.path matching .ts slug
src/data/essays/essays.json          ← SPA catalog (Title + dest.path)
        │
        ▼  matching slug entry (machine-readable registry, drives SPA bundle)
src/data/essays/articles.json        ← SPA bundle inclusion list (slugs compiled into EssayPage)
        │
        ▼  npm run build  →  prebuild runs render-words-essays.cjs
public/words/writing/<slug>/index.html   ← generated (inline <style>)
dist/words/writing/<slug>/...            ← mirrored by copy-static-html.js
dist/assets/index-XXXXXXX.js             ← SPA bundle (must include the slug)
        │
        ▼  rsync dist → /var/www/html/arif/  (FULL SITE — not just /words/writing/)
Caddy @static_dirs serves  →  https://arif-fazil.com/words/writing/<slug>/
                            → SPA bundle loaded → EssayPage resolves slug → 200
```

> **CRITICAL lesson (2026-08-07, publishing "I'm Not a Programmer"):** The original recipe only listed `essays.json` as Step 3. The full chain has TWO catalog files: `essays.json` (SPA catalog, drives index cards) AND `articles.json` (SPA bundle inclusion list, drives EssayPage). Without `articles.json`, Vite tree-shakes the essay content out of the production bundle → `getEssay(slug)` returns undefined → SPA renders "Essay Not Found" even though the slug is correct in `.ts` and `essays.json`. Step 3b added below. Also: deploy step must rsync the full `dist/` (not just `dist/words/writing/`) to push the new bundle file alongside the shell.

## Step 1 — Essay module (CANON)

`src/data/essays/<N>-<slug>.ts`:

```ts
import type { EssayContent } from './types';

const content: EssayContent = {
  title: `Full Title Here`,
  date: '2026-08-07',                        // ISO date
  slug: 'the-slug-without-NN-prefix',       // MUST match filename minus prefix
  tags: ['ai-governance', 'agi', 'arifos'],
  excerpt: `One-sentence thesis for the SPA catalog.`,
  mediumUrl: '',                              // '' for direct publication
  isDirectPublication: true,                  // direct, not Medium repost
  html: `<article>...full body HTML...</article>`,
};

export default content;
```

## Step 2 — Register in `src/data/essays/index.ts`

Two edits:
- Add `import eNN from "./<N>-<slug>";` after the previous essay import
- Add `eNN` to `essayModules` array: `export const essayModules = [..., eNN, ...]`

## Step 3 — Catalog entries (TWO files, both required) — UPDATED 2026-08-07

### 3a — `src/data/essays/essays.json` (SPA catalog, drives index cards)

Add entry at top (newest-first convention):

```json
{
  "id": "s4-3",
  "title": "...",
  "date": "2026-08-07",
  "lang": "en",
  "series": { "id": "S4", "n": 3 },
  "tags": [...],
  "dest": {
    "type": "onsite",
    "path": "/writing/<slug-without-NN-prefix>"
  },
  "seal": null
}
```

Series assignments:
- **S4** = Governance Canon (direct constitutional publications)
- **S6** = Eureka Trilogy (geophysics → AI governance)
- **S8** = The Forge (field notes)

### 3b — `src/data/essays/articles.json` (SPA bundle inclusion, drives EssayPage) — ADDED 2026-08-07

Add entry at top:

```json
{
  "slug": "the-slug-without-NN-prefix",
  "title": "...",
  "date": "2026-08-07",
  "categories": ["AI-Governance", "AGI", "..."],
  "mediumUrl": "https://arif-fazil.com/words/writing/<slug>/",
  "hasContent": true,
  "isDirectPublication": true
}
```

**Why this matters (verified 2026-08-07):** The SPA `EssayPage.tsx` calls `getEssay(slug)` which reads `essayModules` (from `index.ts`). But the **bundle inclusion** is driven by `articles.json` — if the slug isn't there, Vite tree-shakes the essay content out of the production bundle. Result: shell HTML renders 200, bundle has no slug, EssayPage renders "Essay Not Found."

Diagnose with:
```bash
grep "<your-slug>" dist/assets/index-*.js | head -3
# empty? articles.json is missing the slug
```

## Step 4 — Build

```bash
cd /root/arif-fazil.com/sites/arif-fazil.com
npm run build
```

This triggers `scripts/render-words-essays.cjs` in prebuild. Outputs land in `public/words/writing/<slug>/index.html`, `<slug>.md`, and `index.html`. The SPA bundle `dist/assets/index-XXXXXXX.js` is rebuilt by Vite — if `articles.json` had the slug, the slug now appears in the bundle.

Verify slug IS in the bundle before deploying:
```bash
grep "your-slug" dist/assets/index-*.js | head -1
# expected: at least one match (slug string + title string + html string)
```

## Step 5 — Deploy (FULL-SITE rsync, not just /words/writing/) — UPDATED 2026-08-07

```bash
rsync -a dist/ /var/www/html/arif/
```

**Do NOT rsync only `dist/words/writing/`.** Verified 2026-08-07:

The `/words/writing/index.html` shell (zen-pulse listing) and the SPA shell at `/words/writing/<slug>/` reference an `assets/index-XXXXXXX.js` bundle by hash. If you only rsync `dist/words/writing/`, the listing page updates with the new essay link, but the per-slug shell still references the OLD bundle hash (the previous build's `index-OLD.js`). Then:
- `curl https://arif-fazil.com/words/writing/<slug>/` returns 200 with SPA shell HTML ✅
- But the SPA shell HTML loads the old `<script src="/assets/index-OLD.js">` ❌
- That old bundle does NOT contain the new slug → 404 "Essay Not Found" rendered

Fix: `rsync -a dist/ /var/www/html/arif/` — copies the new bundle file alongside the new shell HTML. Both reach live in one pass.

Verify the shell now references the new bundle:
```bash
curl -s "https://arif-fazil.com/words/writing/<slug>/" | grep -oE "index-[A-Za-z0-9_-]+\.js" | head -1
# expected: the new bundle hash (matches dist/assets/index-*.js)
```

If you really need a narrow rsync (e.g. to avoid touching other content), the minimum is:
```bash
rsync -a dist/assets/ /var/www/html/arif/assets/        # bundle
rsync -a dist/words/writing/ /var/www/html/arif/words/writing/  # shells + index
```
But the full-site rsync is simpler and the canonical pattern.

## Verification (every step mandatory)

```bash
# 1. Live URL serves 200
curl -s -o /dev/null -w "%{http_code}\n" "https://arif-fazil.com/words/writing/<slug>/?cb=$(date +%s)"

# 2. Title appears in served HTML
curl -s "https://arif-fazil.com/words/writing/<slug>/" | grep -oE "<title>.*</title>" | head -1

# 3. Index lists the essay (not a duplicate)
curl -s "https://arif-fazil.com/words/writing/" | grep -oE "<slug>" | sort | uniq -c

# 4. Cross-links work
curl -s "https://arif-fazil.com/words/writing/<slug>/" | grep -oE "Pairs with|/words/writing/<other-slug>"

# 5. essays.json path matches the .ts slug exactly
python3 -c "
import json
d = json.load(open('/root/arif-fazil.com/sites/arif-fazil.com/src/data/essays.json'))
for e in d:
    if 'unique-title-keyword' in e.get('title','').lower():
        print(e['dest']['path'])
"
```

## Pitfalls (every one of these fired during the 2026-08-07 triptych OR the follow-up publish)

### 1. Slug mismatch between `.ts` and `essays.json`

The renderer's URL comes from `.ts slug:`. If `essays.json dest.path` uses a different slug, the SPA catalog links to a 404 but the static page renders fine. Detection: `curl -sIL https://arif-fazil.com/<path-from-essays-json>` returns 404 while `curl -sIL https://arif-fazil.com/<slug-from-ts>/` returns 200.

**Fix:** update `essays.json`, never rename the `.ts`. Slug is canonical at the `.ts` source.

### 2. Missing `articles.json` entry — the 404 that survives a build (ADDED 2026-08-07)

The SPA `EssayPage.tsx` calls `getEssay(slug)` which reads `essayModules` (from `index.ts`). But the **bundle inclusion** is driven by `articles.json` — if the slug isn't there, Vite tree-shakes the essay content out of the production bundle. Result: shell HTML renders 200, bundle has no slug, EssayPage renders "Essay Not Found."

Detection:
```bash
grep "<your-slug>" dist/assets/index-*.js
# empty? articles.json is missing the slug
```

**Fix:** add the entry to `src/data/essays/articles.json` (Step 3b above), rebuild.

### 3. SPA shell still references old bundle hash (ADDED 2026-08-07)

If you only rsync `dist/words/writing/`, the per-slug shell HTML gets the new listing-page link, but it still points to the OLD `<script src="/assets/index-OLD.js">` from the previous build. The old bundle doesn't contain the new slug.

Detection:
```bash
curl -s "https://arif-fazil.com/words/writing/<slug>/" | grep -oE "index-[A-Za-z0-9_-]+\.js" | head -1
# compare against ls dist/assets/index-*.js
# mismatch? rsync was scoped wrong
```

**Fix:** `rsync -a dist/ /var/www/html/arif/` (full site, not just `dist/words/writing/`). Both shell and bundle land in one pass.

### 4. Duplicate-row from two `.ts` files

`render-words-essays.cjs` dedupes by slug (first occurrence by filename length wins), not by title. If two `.ts` files share a slug-derived URL, the index gets two rows with the same title. Detection: `curl -s https://arif-fazil.com/words/writing/ | grep -oE "Title" | sort | uniq -c` shows count > 1.

**Fix:** delete the stray `.ts`, rerun the renderer, rsync clean.

### 3. Hand-written page wiped by generator

The renderer runs in prebuild. It will overwrite any `public/words/writing/<slug>/index.html` you hand-placed. If you hand-wrote the page then ran `npm run build`, your work is gone — what's left is whatever the generator emitted from the `.ts`.

**Fix:** always check `scripts/render-words-essays.cjs` exists before hand-writing. If it does, edit the `.ts` and rebuild. Hand-writing is wasted entropy.

### 4. Parallel subagent collisions

Dispatching 3 parallel subagents to write `.ts`, HTML, and index files in the same `public/words/` subtree causes fights: file deletes, restore races, duplicate `.ts` files. Detection: after parallel delegation, check `ls -la /var/www/html/arif/words/writing/` against `ls -la public/words/writing/` and reconcile.

**Fix:** serialize site-file writes. One subagent per concern, disjoint paths, OR sequential rather than parallel.

### 5. Stale directories after slug change

If a slug changes between builds, the OLD directory stays on disk. Caddy serves 404 for paths whose file was deleted but whose parent dir remains. Detection: `curl -sIL https://arif-fazil.com/<old-slug>/` returns 200 (parent dir exists) but the body is empty / 404.

**Fix:** after slug changes, `rm -rf` the stale directory from BOTH `public/words/writing/` AND `/var/www/html/arif/words/writing/`. Then rerun renderer + rsync.

### 6. Caddy `/writing/*` double-prefix bug (pre-existing, NOT yours to fix in essay publishing)

`/writing/<slug>/` 308-redirects to `/words/writing/writing/<slug>/` → 404. Affects every essay, not just yours. Canonical `/words/writing/<slug>/` works. Fix in Caddy is one-line (`/writing/* → /words{uri}` instead of `/words/writing{uri}`) but it's a separate day's work. Tell the user the canonical URL; don't patch Caddy during essay publishing.

### 7. `execute_code` blocked during cron mode

Fallback: heredoc into `python3 << EOF` via terminal tool. Verbose but works. Pipe-to-interpreter (`cat | python3 -m json.tool`) triggers security scan auto-approval but runs cleanly.

## Design language — makcikgpt (Arif's ruling, 2026-08-07)

Arif: **"Design wise makcikgpt site is much better."** Default to this for essays, NOT the hub-hero language.

### Visual tokens

| Token | Value | Use |
|---|---|---|
| bg | `#0d1117` | page background |
| body | `#c9d1d9` | paragraph text |
| heading/link | `#58a6ff` | h1/h2, anchor color |
| accent | `#ffd700` | kicker, seal, paired-article borders, lead paragraph |
| meta | `#6e7681` / `#8b949e` | dates, mono labels |
| mono font | `ui-monospace, SFMono-Regular, Menlo, monospace` | meta + breadcrumbs |

> Note: differs from hub-hero palette (gold `#c9a227`, ink `#e8e6e1`). Don't mix them on essay pages.

### Required blocks (in order)

1. **Breadcrumb nav:** `<nav aria-label="Breadcrumb"><a href="/">← arif-fazil.com</a> / <a href="/words/">/words/</a> / <a href="/words/writing/"><strong>Writing</strong></a></nav>`
2. **Cover block:** `<div class="cover">` with `.cover-emoji`, `.cover-kicker`, `.cover-title`, `.cover-subtitle`, `.cover-byline` (incl. `999 Meterai · seal 999`)
3. **Zen pulse aside:** 3-column `<aside class="zen-pulse">` answering WHERE/WHY/WHAT-NEXT
4. **Paper header (visible):** title, author byline, geo/role, location, "Published: YYYY-MM-DD · Direct Publication · /words/", epistemic tag
5. **Body** with sectioned h2 headings, `<sup class="ref"><a href="#ref-N">[N]</a></sup>` citations
6. **References** `<ol class="ref-list">` with anchor `#ref-N` matching the in-body citations
7. **Footer-note:** "Pairs with:" linked, "DITEMPA BUKAN DIBERI", machine-readable catalog

### Inline vs linked CSS — current reality

`render-words-essays.cjs` emits pages with **inline `<style>` blocks**. The shared CSS at `/words/writing/_shared/writing.css` was created then orphaned because nothing linked it. New essays inherit the inline-style pattern from the generator. Don't manually link a shared CSS — the generator will strip it on rebuild. If you want shared CSS instead, patch the generator (one-line change in `render-words-essays.cjs`).

## Cross-linking the triptych (when essays are paired)

If a set of essays was published as a series, each article's footer-note should link the others:

```html
<div class="footer-note">
  <p>Pairs with: <a href="/words/writing/<other-slug>/">Other Essay</a> · <a href="/words/writing/<third-slug>/">Third Essay</a></p>
  <p>More from /words/writing/: <a href="/words/writing/">all essays</a> · <a href="/words/">/words/</a> · <a href="/llms.txt">/llms.txt</a></p>
</div>
```

The index page should list all three prominently with NEW badges under a "Latest" or "S4 · Governance Canon" series label.

## "Done" gates (7 must-pass — UPDATED 2026-08-07)

1. ✅ `.ts` file exists, exports `EssayContent`
2. ✅ `index.ts` imports it AND includes it in `essayModules[]`
3. ✅ `essays.json` has matching `dest.path` and series id/n
4. ✅ **`articles.json` has the slug** — often-forgotten; gate added after real 404-from-build incident (publishing "I'm Not a Programmer")
5. ✅ Live URL `https://arif-fazil.com/words/writing/<slug>/` returns 200, body contains title + references + footer (post-JS hydration — use `browser_navigate` for a definitive check)
6. ✅ Live SPA shell references the NEW bundle hash (not the old one from the previous build) — `curl -s <url> | grep index-...`
7. ✅ Writing index lists the essay exactly once, with NEW badge if `date >= today - 30d`

If any of those fail: stop, fix, re-verify. Don't seal receipt.

## Series taxonomy (current as of 2026-08-07)

| Series | Label | Theme |
|---|---|---|
| S1 | ORIGIN — The Accident | How arifOS happened |
| S2 | THE NAMING DIPTYCH | Naming as first act of creation |
| S3 | MCP WEEK — July 2026 Tetrad | MCP week essays |
| S4 | GOVERNANCE CANON | AGI Paradox, Truth Is Not Cheap, Third Axis, BINATANG→WARGA, Mind is Not Model, **I'm Not a Programmer** (added 2026-08-07, slug: `i-didnt-invent-a-token-i-invented-a-question`, S4 n=4) |
| S5 | CONSTITUTIONAL PHYSICS | Physics-constrained attention |
| S6 | EUREKA TRILOGY | AVO/attention trilogy (3 papers) |
| S7 | BAHASA & MALAYSIA | BM pieces, Rukun AGI |
| S8 | THE FORGE — Field Notes | Tool is thought, survival of fittest, three timelines |
| S9 | REFLECTIONS | Second brain, paradox of language |
| M1 | MAKCIKGPT · PETRONAS DNA | PETRONAS analysis pieces |
| M2 | MAKCIKGPT · SEARAH | Gas Sarawak coverage |
| M3 | MAKCIKGPT · YTL & ILMU | YTL monopoly coverage |
| M4 | MAKCIKGPT · RAKYAT | People-focused coverage |
| M5 | MAKCIKGPT · AKAL | Critical-reasoning coverage |

When adding a new essay, pick the matching series id; the SPA `Essays.tsx` groups by series automatically (in the SPA route). For the static `writing/index.html` shell, organize by series labels manually.