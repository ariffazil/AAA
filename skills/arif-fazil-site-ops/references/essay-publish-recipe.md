# Essay Publish Recipe — Aug 2026 session log

Full reproduction recipe for publishing a new direct-publication essay under
`/words/writing/` (or `/world/makcikgpt/` for BM articles). Mirror of the
MakcikGPT dark GitHub theme — `scripts/generate-makcik-index.cjs` is the
canonical design reference.

## When you need this recipe

- User says "publish this on my site" with prose content
- User says "new essay under /words/" or `/words/writing/`
- Sibling agent asks how to add an essay to the constitutional surface

## The 6-step canonical flow

```bash
# 1. Probe live state — is this slot occupied?
curl -sIL "https://arif-fazil.com/words/writing/<candidate-slug>/" | head -2
ls /var/www/html/arif/words/writing/ | grep <candidate-slug>

# 2. Probe siblings — has anyone deployed a parallel?
grep -rl "<candidate-slug>" /root/arif-fazil.com/sites/arif-fazil.com/public/ 2>/dev/null
find /root/arif-fazil.com -maxdepth 6 -iname "*<slug>*" -not -path "*/node_modules/*"
```

If a sibling already deployed, **adopt and reconcile** — don't re-inject.

## The 5 registers to wire

Every new essay touches FIVE files. Skip any and it won't render or list.

### Register 1 — `src/data/essays/<NN>-<slug>.ts`
Typed `EssayContent` interface. Filename is `<NN>-<slug>.ts` where `NN` is the next available
essay number prefix (read existing files to find the gap). Use backtick template literals
for multi-line html body. `mediumUrl: ''` for direct-publication-only essays.

### Register 2 — `src/data/essays/articles.json`
Insert at TOP (newest first). Schema:
```json
{
  "slug": "<slug>",
  "title": "<title>",
  "date": "YYYY-MM-DD",
  "categories": ["AI-Governance", "AGI", ...],
  "mediumUrl": "https://arif-fazil.com/words/writing/<slug>/",
  "hasContent": true,
  "isDirectPublication": true
}
```

### Register 3 — `src/data/essays/index.ts`
FOUR edits in one file. Get the slot right or build fails with `Cannot find module`:

```ts
// (a) Add to imports (numbered essays grouped together, e0X series)
import e24 from "./24-the-agi-paradox-why-bigger-models-wont-save-us";

// (b) Push to essayModules array (preserves existing order)
export const essayModules = [e01, ..., e23, e24, g0, ...];

// (c) Append to allEssays array (with full EssayMeta)
{
  title: `...`,
  date: "2026-08-07",
  slug: "...",
  excerpt: `...`,
  tags: [...],
  mediumUrl: "https://arif-fazil.com/words/writing/<slug>/",
  isDirectPublication: true,
},

// (d) Add to CURATED_SLUGS under the right domain (e.g. "AI Governance")
"<slug>": "AI Governance",
```

### Register 4 — `public/words/writing/index.json`
Top-level listing (machine-readable). Insert at TOP, schema:
```json
{
  "title": "...",
  "slug": "<slug>",
  "href": "/words/writing/<slug>",
  "date": "YYYY-MM-DD",
  "territory": "writing",
  "language": "en",
  "tags": ["essay", "AI-Governance", ...],
  "risk_level": "INT",
  "epoch": "YYYY-MM-DD"
}
```

### Register 5 — `src/App.tsx`
Already has `<Route path="/writing/:slug">` from legacy. Add the canon v7 route:
```tsx
<Route path="/words/writing/:slug" element={<EssayPage />} />
```
Keep both routes — legacy `/writing/<slug>` URL must still resolve.

### Register 6 — Caddyfile routing
If `/words*` not already in `@spa_routes` matcher:
```caddyfile
@spa_routes path / ... /words* /work* ...
handle @spa_routes {
    root * /var/www/html/arif
    try_files {path} {path}/index.html =404   # may need: {path} {path}/index.html {path}/
    ...
}
```
Then `sudo caddy validate && sudo systemctl reload caddy`.

## The build + deploy + verify sequence

```bash
# Build (prebuild runs render-words-essays.cjs after makcik-index)
cd /root/arif-fazil.com/sites/arif-fazil.com && npm run build

# Deploy
cd /root/arif-fazil.com && bash scripts/deploy-site.sh arif-fazil.com --apply

# Gate
bash scripts/verify-pages.sh   # MUST show "VERDICT: PASS" — otherwise HOLD

# Live probe
curl -sI "https://arif-fazil.com/words/writing/<slug>/" | head -2   # HTTP/2 200

# Browser verify (the SPA shell 200 is not enough — essay body must render)
# Open in browser_navigate, check title + first H2 section, then close.
```

## Source-of-truth rules (revised 2026-08-07)

| Field | Source of truth |
|---|---|
| Title, date, slug, html body | `src/data/essays/<NN>-<slug>.ts` |
| Tags, categories, mediumUrl, hasContent | `src/data/essays/articles.json` |
| `allEssays` array order, CURATED_SLUGS | `src/data/essays/index.ts` |
| Static index.json listing | `public/words/writing/index.json` |
| Rendered static HTML pages | `public/words/writing/<slug>/index.html` |

**Critical:** the prerender script `scripts/render-words-essays.cjs` reads from `.ts` files
(content source of truth), not from `articles.json`. Filtering by `articles.json.isDirectPublication`
silently skips essays where the field wasn't set but the `.ts` has real content.

## Pitfalls encountered (each = real time lost)

| Symptom | Cause | Fix |
|---|---|---|
| Essay shows 14 entries with duplicates | Two `.ts` files share slug (legacy + new) | Dedupe by slug; first match by filename length wins |
| Essay slug mismatch → 404 | `EssayContent.slug` field doesn't match `articles.json.slug` | All registries must use same slug |
| `tsc -b` fails: `Cannot find module './26-...'` | `.ts` file deleted but import line remains in `index.ts` | Always remove import + essayModules + allEssays + CURATED_SLUGS together |
| Build pulls in old essay with wrong slug | My prebuild renamed slug mid-deploy, leaving two dirs | Confirm slug in `.ts` matches articles.json before deploy |
| Live shows "Constitutional Essays" not "Long-form Essays" | Sibling agent overwrote index.html | md5sum check post-deploy; reconcile |
| Static `index.html.bak-makcik-style` appears | Sibling backed up my version | Expected; let sibling's version stand |

## Why the trilogy works

The AGI Paradox trilogy (Aug 2026 — The AGI Paradox, Truth Is Not Cheap, The Third Axis
of Failure) demonstrates the complete recipe end-to-end:

- All 5 registers wired correctly → all 3 essays show 200 + correct content
- Sibling agent enriched the index with series chips (S4/S6/S8) — adopted their version
- Keystone line surfaced as gold-emphasized epigraph in two places: index + closing
  blockquote of the third essay
- 14 essays × 2 surfaces (index.html + .md mirror) + 1 index.html + 1 index.json
  = 30+ files generated in one `npm run build`

## Reference scripts

| File | Purpose |
|---|---|
| `scripts/render-words-essays.cjs` | Static prerender for `/words/writing/` (parallel of `generate-makcik-index.cjs`) |
| `scripts/generate-makcik-index.cjs` | The design language source — read first |
| `scripts/lib/makcik-source.cjs` | SOT helper for MakcikGPT (different schema — essay registry uses simpler loadEssays) |
| `scripts/copy-static-html.js` | Postbuild mirror `public/*/index.html → dist/*/index.html` |
| `scripts/verify-pages.sh` | Mandatory gate before SEAL |

## Design language (SPA, not static HTML)

**CRITICAL (2026-08-07, Arif rejected flat static essays):** Essay pages are served by
the React SPA's `EssayPage.tsx`, NOT by static HTML files. Per-essay static
`<slug>/index.html` files shadow the SPA — users get the plain version instead of the
rich design. **NEVER generate per-essay static HTML for `/words/writing/<slug>/`.**

The design contract lives in `EssayPage.tsx` (forge-black hero, tag pills, prose
typography, Continue Reading nav) and `references/makcikgpt-design-audit-2026-08-07.md`.

The index page (`/words/writing/index.html`) is hand-curated by sibling agents or
by `scripts/render-words-essays.cjs` (prebuild). It should NEVER be regenerated to
overthrow the sibling's enriched version. Always `md5sum` to check before writing.

### Caddyfile requirement (SPA fallback for /words/writing/<slug>/)

`@agent_shells` MUST contain `/words` so requests to `/words/writing/<slug>/` hit the
SPA fallback (which rewrites to /index.html for client-side routing). Without this
entry, paths 404 at the static_dirs layer. See "Adding a nav-canon path to the SPA"
in the main SKILL.md for the full recipe.