# Engine Detail

## chrome — the default

```bash
google-chrome --headless --disable-gpu --no-sandbox \
  --no-pdf-header-footer \
  --run-all-compositor-stages-before-draw \
  --virtual-time-budget=15000 \
  --print-to-pdf=out.pdf "file://$PWD/doc.html"
```

- `--no-pdf-header-footer` is not optional. Without it the renderer stamps the `file:///` source
  path, a render date and `n/m` on every page. A deliverable carrying `/root/...` leaks the build machine.
- `--virtual-time-budget` gives JS and webfonts time to settle before the capture. Without it,
  a chart that renders client-side captures empty.
- `--headless=new` vs `--headless` changes layout behaviour on some Chrome versions; if a deck
  paginates oddly, try the other flag before suspecting the CSS.
- **Tagged PDF:** Chrome 85+ emits a tag tree on print-to-PDF. That is the accessibility baseline
  and it is free — but the tree's completeness is disputed (see the router's Contested note).
  `pdftotext` cannot see tags; use a tag-aware tool if the artifact must conform to PDF/UA-1
  (ISO 14289-1:2014, still the practical 2026 target).
- Operational caveat: Chrome is a browser, not a service. For untrusted HTML, high volume, or a
  long-lived daemon, prefer weasyprint or a managed renderer.

## weasyprint — CSS paged media done properly

```bash
weasyprint doc.html out.pdf
```

Its advantage over Chrome is real `@page` margin boxes:

```css
@page {
  size: A4; margin: 18mm 16mm 20mm 16mm;
  @bottom-left  { content: "EXECUTIVE BRIEFING · Edition " string(edition); font-size: 8pt; color: #5f5f5f; }
  @bottom-right { content: counter(page) " / " counter(pages); font-size: 8pt; color: #5f5f5f; }
}
@page :first { @bottom-left { content: none; } @bottom-right { content: none; } }
h1 { string-set: edition content(); }
```

Chrome ignores `@bottom-left` / `@bottom-right`. If you need running headers or footers, that is
weasyprint's strongest argument — or build the furniture into the body and accept manual pagination.

**No JavaScript.** Anything rendered client-side will be missing.

## reportlab — programmatic control

Use when the document is data-shaped rather than prose-shaped: figures placed by coordinate,
generated tables, embedded matplotlib output. It is a canvas, not a layout engine — you compute
positions. The expected-page count is the number of `showPage()` calls in your build script, and
reconciling that against `pdfinfo` is the gate (see `rendered-document-audit`).

## The page-break block worth memorising

```css
figure, table, .callout, .verdict, .keybox { page-break-inside: avoid; }
h2, h3, h4 { page-break-after: avoid; }
tr { page-break-inside: avoid; }
h2 { orphans: 3; widows: 3; }
p  { orphans: 2; widows: 2; }
```

And the one forced break a long document should have:

```css
.cover { page-break-after: always; }
```

## Traps that cost real time

- **Fixed-size slide divs + a non-zero `@page` margin = every slide splits into two pages.**
  Signature: total pages ≈ 2× slide count; odd pages carry a title only. Match the page box to the
  slide box, or set the margin to zero, or stop using fixed-size blocks.
- **`overflow: hidden` discards overflow with no error.** Content vanishes silently.
- **Sparse pixel sampling misreads a full-bleed page as empty.** Measure a bounding box or a row
  profile before declaring any page blank.
- **Inline `<svg><text>` contributes zero characters to the text layer.** A text-layer audit scores
  it as 100 % lost. Strip SVG before an atom diff and confirm those pages visually instead.
- **A `.pdf` extension is not a PDF.** Check the `%PDF-` magic bytes; a failed generator that
  writes an HTML error page still exits 0.

## Fonts

Check before use; a missing font falls back silently to an unreadable default.
Reliable: `/usr/share/fonts/truetype/dejavu/`, `.../liberation/`, `.../lato/`.
Embed the face explicitly in print CSS rather than relying on system resolution.
