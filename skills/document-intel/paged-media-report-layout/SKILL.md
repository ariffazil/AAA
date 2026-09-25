---
name: paged-media-report-layout
description: Use when building long multi-page HTML→PDF reports.
version: 1.0.0
tags: [pdf, layout, paged-media, weasyprint, qa, long-form-report]
capability_tier: fed-long-context
ecology_state: WARM
---

# Paged Media Report Layout

**Trigger:** any document longer than ~4 pages rendered from HTML through a print engine — weasyprint, headless Chrome `--print-to-pdf`, or any CSS-paged-media renderer. Intelligence dossiers, analyst briefs, research reports, decks exported to PDF.

**Scope:** layout and pagination only. Pipeline order, delivery mechanics, and the "a `.pdf` extension is not a PDF" rule belong to the delivery skill; this one governs how the pages break.

## The governing idea

A print engine already paginates. Every forced break you add is a guess about where the content ends, and in a long document the guess is wrong repeatedly — the wrongness shows up as blank space, not as an error.

## Always-on rules

1. **Let the engine paginate.** Reserve one forced break: the cover (`page-break-after: always` on the cover wrapper). Nothing else gets one.
2. **Never force a break per section header.** `h2 { page-break-before: always }`, or a `.pagebreak` class sprayed across wrappers, is the single most common cause of a report full of near-empty pages.
3. **Pin what must not split**, so the engine's own pagination is safe: figures, tables, callouts and rows get `page-break-inside: avoid`; headings get `page-break-after: avoid`.
4. **Keep a figure with its context.** A chart stranded on a page away from its heading, its caption, or its source line reads as an orphan even when the page is full.
5. **Style running furniture in `@page`, not in the body.** Footer via `@page { @bottom-left/@bottom-right { content: ... } }` with `counter(page)` / `counter(pages)`; suppress it on the cover with `@page :first`.
6. **Verify by measurement, never by eye** — especially with no vision lane. Page count, then ink coverage, then the text layer. See the gates below.
7. **Resolve the renderer and interpreter rather than hardcoding paths.** `which weasyprint` and `python3 -c "import matplotlib, reportlab"` before committing to a pipeline; bindings differ per host and image, and a stale hardcoded path fails silently inside a script.

## CSS skeleton

Full recipe — `@page` geometry, cover block, footer, break rules, typography scale: `references/html-paged-media-css.md`.

The break block worth memorising:

```css
figure, table, .callout, .verdict, .danger, .keybox { page-break-inside: avoid; }
h2, h3, h4 { page-break-after: avoid; }
tr { page-break-inside: avoid; }
h2 { orphans: 3; widows: 3; }
p  { orphans: 2; widows: 2; }
```

## QA gates — run in this order, every time

1. **It is a real PDF.** `file out.pdf` → `PDF document, version 1.7`. Anything else means a text file with the wrong extension.
2. **Page count and geometry.** `pdfinfo out.pdf | grep -E 'Pages|Page size'`. Sanity-check the count against the designed structure.
3. **Ink coverage — the blank-page detector.** Run `scripts/ink_coverage_sweep.py out.pdf`. Counting pages is not enough; a page can be counted and still be empty.
4. **Text layer per section.** `pdftotext -f N -l N out.pdf - | head` for the pages you care about, to confirm sections landed in order with nothing truncated, and that no heading sits alone at a page bottom.
5. **Assets all present.** `pdfimages -list out.pdf` — the row count should match the number of embedded figures plus any repeated header art. A missing figure is invisible in every other check.
6. **Reconcile every stated total against its own rows.** Any table with a summary row, any "N items"
   in a heading, any running count must be recomputed from the rows actually rendered — never carried
   from the draft. A hand-assembled total drifts as rows are edited, and it drifts **silently**: a
   breakdown shipped summing to 245 beneath a stated total of 257 renders perfectly, passes every other
   gate, and discredits the whole document the moment a reader adds the column up. Assert it in code
   (`assert sum(rows) == stated`) before the render, and again after any row edit.

7. **Sample pages through the vision lane when one is available.** `pdftoppm -png -r 85 -f N -l N out.pdf` for
   three or four representative pages — the cover, one table-heavy page, one carrying a callout or a diagram
   block — then inspect them with the vision lane. It is the only gate that sees a wrong weekday stamped on the
   cover, a table row orphaned onto the next page leaving a blank cell behind it, or a callout whose text has run
   past its own border. Treat every report as a **candidate**: confirm it against the authored HTML before
   editing, then re-render and re-run gates 2–4.

Pass condition: every page above ~3 % ink coverage, no wide spread, no page whose text layer is a
heading only, every stated total equal to the sum of its own rows, and — where a vision lane ran — every
defect it raised either fixed against the source or dismissed with a reason.

## Pitfalls

- **A forced break on every section header ships a document full of blank space.** Each section starts fresh, whatever room was left on the previous page goes empty, and the ink sweep reports 1–3 % pages sitting beside 13 % pages. In one 20-page A4 brief written this way, three pages came in at 1.1 %, 2.7 % and 2.7 % coverage. Removing the forced breaks and adding the `page-break-inside: avoid` block above took the same document from 21 pages with three near-blank to 20 pages with a clean 3.7 % minimum. The blank pages were never a content problem — they were a CSS problem.
- **Matching page count is not evidence of good layout.** A document can hit its designed page count and still be half empty, because the forced breaks ate the slack. Only the ink sweep sees this.
- **A wide coverage spread is the signature of a layout break, not of intentional design.** Under ~2 % is a split or empty page. Over ~60 % is a full-bleed cover — acceptable on screen, but it eats toner and gradients band on paper, so flag it if the deliverable is meant to be printed.
- **Don't judge layout from screenshots when the active model has no vision lane.** The text layer plus the ink sweep is the reliable gate, and it is also cheaper than rendering and inspecting images.
- **A vision read is authoritative on space and unreliable on characters.** It reliably catches an orphaned row, overflow past a box, and an element present in the HTML but absent from the page; it will also report a typo the source does not contain, because small low-contrast letterspaced type is easy to misread. Confirm every reported defect against the source before patching — otherwise you edit a correct word and leave the real defect standing.
- **Fixed-size page/slide divs under a non-zero `@page` margin split into two pages each** on the browser-print path. If the deck is built from fixed-height blocks rather than flowing content, check that the block fits the printable box before blaming the engine.
- **Re-render and re-run the gates after every layout edit.** A change to one section's length moves every break below it; a gate run before the last edit certifies a document that no longer exists.
- **Match the document to the reader's appetite, not to the content's length.** A user who responds "panjang aku pon x mau baca" to a 7-page brief wants the executive read, not the full argument. Ship the 1-page TLDR first, the long form behind a clear "full version" link. Two outputs from one source — same data, different densities. The dense version reads in 90 seconds; the long form lives behind a filename the reader opens only when they choose to.

## Proven

Long-form sovereign intelligence brief, A4, 20 pages, 16 embedded matplotlib figures, ~59 KB authored HTML → 1.6 MB PDF through weasyprint, with the ink sweep and text-layer gates as the only layout checks and no vision lane in the loop.
