# Auditing a Delivered PDF — Artifact-Level Defects

For the case where the figures are fine and the **deliverable** is broken. Run this whenever a PDF arrives for review — produced here or by another agent — and always before endorsing a deck built from an HTML slide source.

Report shape: **cause → evidence → fix**. "The figure is missing" is the wrong diagnosis when the figure is present and rendered at one-sixth scale.

## 1. Page count is the first tell

```bash
pdfinfo <pdf> | grep -E '^Pages'
```

An HTML slide source of N slides that produces ~2N pages means the **slide box is larger than the printable box** and the renderer is fragmenting every slide into a title page plus a figure page.

Canonical mismatch: `.slide { width: 297mm; height: 210mm }` against `@page { size: A4 landscape; margin: 1cm }` — the printable area is 277×190 mm, so every 297×210 mm slide overflows by 20 mm in both axes.

Fix: set `@page { margin: 0 }` (or size the slide to the real printable area). Confirm by re-rendering and checking the count **halves**. Do not try to fix this with `page-break-*` rules — the box geometry is the cause.

## 2. Kill the browser chrome

Headless Chromium's `--print-to-pdf` stamps a timestamp, the document title, the **source `file:///…` path**, and `n/m` onto every page unless told otherwise:

```bash
google-chrome --headless --disable-gpu --no-sandbox \
  --no-pdf-header-footer --print-to-pdf=out.pdf file:///abs/path/to/source.html
```

A local file path printed onto a client-facing or archival deliverable is an information leak, and the header/footer consumes height that worsens §1. Verify: `pdftotext out.pdf - | grep -c 'file://'` → expect 0.

## 3. Ink-coverage triage — find the blank pages without opening them all

```bash
pdftoppm -png -r 110 deck.pdf page
# then per PNG: share of pixels darker than ~235/255
```

- Pages under ~3 % are fragments, section dividers, or failed renders. A *run* of them pinpoints where the page break falls and how many slides got split.
- A cover/back-cover near 80 % is full-bleed dark. Flag it if the deck may be printed: toner cost is an order of magnitude higher and CSS gradients band on paper.
- Comparing ink coverage before and after a fix is the cheapest proof the fix worked — a correct render jumps from ~1–3 % to ~5–25 % per content page.

## 4. Raster-versus-vector census

```bash
pdfimages -list deck.pdf     # which pages carry rasters, at what pixel size
```

Most of an SVG-built deck is vector; only embedded basemaps/photos appear here. Two things to read from it:

- A raster with a healthy pixel count that still looks tiny on the page is being **shrunk by its container**, not by its source. A `max-width:100%; max-height:100%` image dropped into a flex column renders at whatever the column gives it — often a fraction of the card it sits in, with ~40 % of the card left empty underneath.
- Judge the **content band**, not the frame. A cross-section whose geology occupies a 120 px ribbon inside a 380 px image is squashed even though nothing is cropped and every axis label is present. If the caption advertises a vertical exaggeration, ask whether the strata are thick enough on screen for that exaggeration to mean anything — a section flattened to a ribbon defeats its own scale statement.

Fix direction for a squashed section: crop the source to the plot frame, drop any duplicated internal title, and either upscale to fill the card or split into a regional panel plus an inset zoom. Raise annotation/legend type so the figure does not depend on surrounding prose to be readable.

## 5. Consistency checks that decide whether an expert trusts the figure

Run these on the rendered page, not the source:

- **Orientation agreement.** Slide title, the figure's own internal title, the running footer, and the x-axis direction must all state the same transect orientation. Disagreement (NW–SE vs NE–SW vs SE–NW) means one of them is wrong and the reader cannot tell which — fix before delivery, do not annotate around it.
- **Scale, vertical exaggeration, colour key.** A caption claiming a vertical exaggeration with no VE note, no scale bar, and no legend on the figure is an *illustration*, not a *figure*. Add all three or drop the claim.
- **Monotonic axes.** Check that tick labels step evenly. A skipped interval (8.0, 7.5, 7.0, 6.0, 5.0) reads as a data gap even when the data is complete — add the missing tick or annotate why.
- **Label contrast at print scale.** Annotation type below roughly 1.5 % of figure width will not survive projection or print reduction; low-luminance pairs (dark red on maroon) fail even on screen. Flag both even when the page passes ink-coverage triage.
- **Claim/artifact ratio.** A cover line claiming an artifact count the deck does not carry is a credibility defect, not a rounding error — and the fix is to count, not to soften the wording.

## 6. Verify citations before endorsing them

Resolve every DOI in the deck. A reference whose DOI resolves to a different paper, or to none, invalidates the claims resting on it — and a *near-future* author year is the usual signature of a fabricated or mis-transcribed citation.

```bash
curl -sL https://doi.org/<doi>    # pass condition: Crossref record matches title/year/authors
```

State plainly which citations verified. In a technical deliverable an independently confirmed citation is worth calling out: it is the part a reviewer checks first, and reporting the passes proves the audit was not a hunt for faults.

## 7. Never audit only the generator

A clean build script proves nothing about the rendered artifact. Re-render the source HTML yourself into a scratch dir, compare page count and ink coverage against the delivered file, and only then attribute the defect. This separates "the renderer was mis-invoked" from "the source geometry is wrong" — different owners, different fixes.
