# HTML → Paged-Media CSS Recipe

Skeleton that produced a clean 20-page A4 report with 16 embedded figures. Copy and adjust the geometry; keep the break discipline intact.

## Page geometry and running furniture

```css
@page {
  size: A4;
  margin: 16mm 14mm;
  @bottom-left  { content: "DOCUMENT TITLE · SECTION · DATE"; font-size: 6.8pt; color: #8a94a0; }
  @bottom-right { content: "PAGE " counter(page) " / " counter(pages); font-size: 6.8pt; color: #8a94a0; }
}
/* Suppress running furniture on the cover */
@page :first {
  @bottom-left  { content: ""; }
  @bottom-right { content: ""; }
}
```

`counter(pages)` needs a paged-media engine that resolves total page count; if the footer renders the literal string, the engine does not support it and the count must be dropped or injected upstream.

## Base styles

```css
* { box-sizing: border-box; }
body {
  font-family: "DejaVu Sans", sans-serif;
  font-size: 9.4pt; line-height: 1.52; color: #1d2733; margin: 0;
}
h1 { font-size: 24pt; line-height: 1.14; margin: 0 0 6px 0; letter-spacing: -0.4px; }
h2 { font-size: 13.4pt; margin: 22px 0 7px 0; padding-bottom: 4px; border-bottom: 2px solid #0d2b45; }
h3 { font-size: 10.8pt; margin: 15px 0 5px 0; }
h4 { font-size: 9.8pt; margin: 12px 0 4px 0; }
p  { margin: 0 0 8px 0; }
```

Body text at ~9.4 pt with 1.5 line-height is the density that keeps a data-heavy A4 page readable in a Telegram-attached PDF; below ~9 pt it stops being legible on a phone.

## The break block — the part that matters

```css
figure, table, .callout, .verdict, .danger, .keybox, .stat-strip { page-break-inside: avoid; }
h2, h3, h4 { page-break-after: avoid; }
tr { page-break-inside: avoid; }
figure img { width: 100%; border: 1px solid #dfe4e9; }
h2 { orphans: 3; widows: 3; }
p  { orphans: 2; widows: 2; }
```

Do **not** add a `.pagebreak { page-break-before: always; }` utility and apply it to sections. If the class must exist for a rare deliberate case, apply it to at most one element in the whole document.

## Cover block

```css
.cover { height: 252mm; page-break-after: always; }
.cover-rule { height: 5px; background: linear-gradient(90deg, #0d2b45 0%, #1b7f79 55%, #d98324 100%); margin-bottom: 22px; }
.kicker   { font-size: 8.2pt; letter-spacing: 2.6px; text-transform: uppercase; font-weight: 700; }
.stat-strip { display: flex; gap: 9px; }
.stat { flex: 1; border-top: 3px solid #1b7f79; padding: 8px 9px; }
.stat .n { font-size: 15pt; font-weight: 700; line-height: 1.1; }
.stat .l { font-size: 7.5pt; line-height: 1.3; }
```

A cover sized at ~252 mm plus `page-break-after: always` lands as exactly one page on A4 with 16 mm margins. Size it larger and it silently becomes two.

## Report structure that paginates well

The order below keeps long tables and multi-line findings away from page bottoms, because each section opens with a heading plus one or two prose paragraphs before any table:

1. Cover — title, one-paragraph summary box, a 4-cell stat strip, provenance/metadata block
2. Executive read — numbered findings, one paragraph each, tagged
3. Scope, method, disclosures — two-column layout
4. Layer 1 — what is verifiably true (tables, first figure)
5. Layer 2 — what it implies
6. Layer 3 — scenario space (probability bars, entanglement table, collapse triggers in two columns)
7. Layer 4 — absence analysis (category table, predictive-void note)
8. Market/regulatory frame
9. Falsification — what would have to be true, plus a monitoring list
10. Counter-narrative
11. Conclusions — numbered
12. Gaps and what the document does not know
13. Appendices — source ledger, provenance, constitutional frame

Two-column blocks (`display: flex; gap: 14px;` with `flex: 1` children) pack method-note and disclosure sections densely and break cleanly, provided the block itself is in the `page-break-inside: avoid` list.

## Render and verify

```bash
which weasyprint
weasyprint brief.html "Report-Name-YYYY-MM-DD.pdf"
file *.pdf && pdfinfo *.pdf | grep -E 'Pages|Page size|File size'
python3 scripts/ink_coverage_sweep.py "Report-Name-YYYY-MM-DD.pdf"
pdfimages -list "Report-Name-YYYY-MM-DD.pdf" | tail -n +3 | wc -l
```

Keep the deliverable between ~1–3 MB; heavier PDFs are slow to attach and slow to open on a phone.
