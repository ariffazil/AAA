# Publication Pipeline — Getting an Article Actually Reachable, and Rendering an Artifact

Two distinct delivery problems. Both have been got wrong. Both are cheap to test.

## Part 1 — An article must be registered in three places + git-tracked + built

The site is a Vite/React SPA with a client-side route `/world/makcikgpt/:slug`. Adding the content file is not enough; the route resolves against a metadata list that is maintained separately from the content files.

An article is reachable only when **all five** of these are true:

| # | Surface | What it needs |
|---|---|---|
| 1 | `src/data/makcikgpt/<slug>.ts` | The content module, default-exporting an object with a `slug` and an `html` string |
| 2 | `src/data/makcikgpt/index.ts` | An import, an entry in the **modules** array, AND an entry in the **meta** array — two separate lists in the same file |
| 3 | `src/data/essays.json` | An entry whose `dest.path` is `/world/makcikgpt/<slug>` |
| 4 | `git add + git commit` | Files must be tracked; untracked files do not appear in `make build` output |
| 5 | `npm run build` in `sites/arif-fazil.com/` | NOT `astro build` — the project uses Vite/React, not Astro |

### Step 4 detail — git tracking is the silent killer

An article can exist as a `.ts` file, be registered in `index.ts`, and still not deploy because it was never `git add`+`git commit`. The `rsync --delete` from `dist/` to webroot only ships what the build produced, and the build only sees tracked files. Symptom: `curl` returns the old markdown mirror (20-byte content-length) instead of the SPA shell.

Fix: `git status` the `makcikgpt/` directory before building. `??` beside your article slug = untracked = will not deploy.

### Step 5 detail — build command

`cd sites/arif-fazil.com && npm run build` — this runs Vite, copies static HTML, generates SPA shells for all article slugs (currently 78+), and produces `dist/`. The Makefile target is `make build` which also runs `build-ledger.py` and `copy-static-html.js` as pre/post steps.

Do NOT run `astro build` — the project migrated from Astro to Vite/React but some config files still reference Astro.

Surface 2 and surface 3 are the ones that get missed. A file present in the modules array but absent from `essays.json` compiles, builds, deploys, and does not render.

### The generator for surface 3 does not run automatically

`scripts/generate-essays-json.cjs` is the intended producer for `essays.json`, and it is not wired into the build's `prebuild` chain. It also reads the TypeScript canon with `require()`, which Node cannot resolve for a `.ts` file — so when it is invoked directly it fails on module resolution before writing anything.

Consequence: `essays.json` is a **manually maintained file that looks generated**. Check its modification date against the article files. If it is older than the newest article, that article is not registered.

**Fix direction, not yet applied:** register the new entry in `essays.json` directly (matching the shape of a neighbouring makcikgpt entry — `id`, `title`, `date`, `lang`, `series`, `tags`, `dest`, `seal`, `provenance_status`), and treat repairing the generator as a separate piece of work. Do not renumber or regenerate the whole file to add one entry.

### How to detect it — assert on content, never on status

The repo's page gate (`scripts/verify-pages.sh`, run as `make verify-pages`) probes every `dist/**/index.html` against the live URL and asserts HTTP 200. It will report **PASS, all pages reachable** while an article is serving the section hub instead. The SPA catch-all returns 200 for an unknown slug.

So the gate is blind to this entire failure class. Test by content:

1. Count article content files against `essays.json` entries. A gap is the finding.
2. Load a suspect slug **and a known-good slug from the same section, in the same run** — one broken page proves nothing on its own; it only becomes a finding when a working sibling exists.
3. Assert on the rendered text: the article renders when page text length is well above the hub's and contains the article title. The hub fallback renders the section landing copy (an "N articles · updated" line) and is short.
4. Check the served asset hash against the built one (`md5sum`) if you suspect a stale deploy.

Fetch with a real user agent and a cache-busting query parameter; the front is behind a CDN.

### Caddy auto-routes new slugs — no manual config needed

The Caddyfile has a catch-all pattern for `/world/makcikgpt/*` that serves `{path}/index.html` via `try_files`. New slugs are handled automatically as long as the SPA shell exists in `dist/world/makcikgpt/<slug>/index.html`. Do NOT add manual route entries to the Caddyfile for new MakcikGPT articles.

Exception: if the new article needs a legacy redirect from an old slug, add that redirect to `/etc/caddy/vhosts/arif-fazil.com.conf`.

### The published page is served from the repo's `dist/` mirrored to a webroot

`/root/arif-fazil.com` holds the Makefile and deploy scripts; the app itself is in `sites/arif-fazil.com`. The webroot is **not** the repo's `dist/`. Confirm the live path before concluding a deploy has landed by comparing the served bundle hash to the built bundle hash.

### Partial deploy (build only, skip Caddy reload) — manual rsync required

When invoking `npm run build` directly inside `sites/arif-fazil.com/` rather than running the full `make deploy`, the build produces the SPA shell and markdown mirror under `dist/` but neither file is mirrored to the live webroot. The Caddy catch-all will still serve any published slug, but only because the source files happen to already exist there from an earlier full deploy.

For a new article, sync explicitly after build:

```
rsync -av sites/arif-fazil.com/dist/world/makcikgpt/<slug>/ /var/www/html/arif/world/makcikgpt/<slug>/
rsync -av sites/arif-fazil.com/dist/makcikgpt-md/<slug>.md /var/www/html/arif/makcikgpt-md/
```

Then `curl -sI https://arif-fazil.com/world/makcikgpt/<slug>` should return `HTTP/2 200` with HTML content. If `curl` returns the markdown mirror (small content-length, `text/markdown`) instead of the SPA shell, the rsync step was skipped.

The full `make deploy` target runs `sync-aaa`, `build`, `verify-pages`, `reload` (Caddy reload), and `split-roots` in order and handles the rsync implicitly — but `make deploy` is a T3 HOLD per the site AGENTS.md unless explicitly named. Sub-deploys stay inside `sites/arif-fazil.com/` and require explicit rsync.

---

## Part 2 — Rendering a house-style PDF artifact

For dossiers and reports the user asks to be delivered as PDF.

### Render path

Write the document as a single self-contained HTML file with an inline `<style>` block, then convert. `weasyprint` works and handles the `@page` rules needed for print:

```python
from weasyprint import HTML
HTML(filename=src).write_pdf(out)
```

A headless browser renderer also produces a valid PDF but extracts oddly — display type with letter-spacing comes out as one character per line in `pdftotext`. If you use one, verify visually rather than trusting the text layer.

### Verify, always — four checks

1. `pdfinfo out.pdf` — page count and page size (A4).
2. `pdftotext -layout -f 1 -l 1 out.pdf -` — confirms cover text is present and in order.
3. `pdftotext out.pdf - | tail` — confirms the closing section and the footer are on the last page, i.e. nothing was clipped.
4. **Look at page 1 and one interior page.** Render them at ~90 dpi and check them as images. Vision catches what text extraction cannot: a palette that renders as an invisible grey, a table that overflows the margin, a section header orphaned from its body. Text-only verification of a designed document is not verification.

### House design language

Standing palette for the user's artifacts — forged steel. Dark first page, warm paper interior:

| Token | Hex | Use |
|---|---|---|
| ink | `#1a1612` | cover background, table headers, pull-quote blocks |
| blood | `#8b1a1a` | section rules, kickers, emphasis |
| brass | `#a08040` | accents, numerals, the closing mark |
| bone | `#d8d0c0` | body text on dark |
| steel | `#5a5650` | small metadata |
| paper | `#efeae0` | body background |

Typography: monospace for labels, headers, tables and numerals; serif for prose. `//` as a section separator prefix. A ruled `@page` footer with the page number. Structure the document with numbered sections; put the plain-language version last, addressed to the reader rather than the specialist.

Do not introduce pastel or decorative palettes, spiritual iconography, or rounded/soft component styling into these artifacts.
