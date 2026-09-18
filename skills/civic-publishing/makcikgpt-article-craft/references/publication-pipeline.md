# Publication Pipeline — Getting an Article Actually Reachable, and Rendering an Artifact

Two distinct delivery problems. Both have been got wrong. Both are cheap to test.

## Part 1 — An article must be registered in three places

The site is a Vite/React SPA with a client-side route `/world/makcikgpt/:slug`. Adding the content file is not enough; the route resolves against a metadata list that is maintained separately from the content files.

An article is reachable only when **all three** of these are true:

| # | Surface | What it needs |
|---|---|---|
| 1 | `src/data/makcikgpt/<slug>.ts` | The content module, default-exporting an object with a `slug` and an `html` string |
| 2 | `src/data/makcikgpt/index.ts` | An import, an entry in the **modules** array, AND an entry in the **meta** array — two separate lists in the same file |
| 3 | `src/data/essays.json` | An entry whose `dest.path` is `/world/makcikgpt/<slug>` |

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

### The published page is served from the repo's `dist/` mirrored to a webroot

`/root/arif-fazil.com` holds the Makefile and deploy scripts; the app itself is in `sites/arif-fazil.com`. The webroot is **not** the repo's `dist/`. Confirm the live path before concluding a deploy has landed by comparing the served bundle hash to the built bundle hash.

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
