# Multi-Page Geological PDF — Layout Forensics

Proven 2026-09-15 auditing the Kinabalu Basin visual pack. That pack's *content* was sound —
verified citation, consistent domain colour logic, proper four-thermochronometer T–t plot —
and it still failed as a deliverable. These are the checks that isolated why.

## Audit sequence

```bash
cp <delivered>.pdf /tmp/qa/pack.pdf && cd /tmp/qa
pdfinfo pack.pdf | head -14                 # pages, page size, producer, creator
pdfimages -list pack.pdf                    # native raster dims + PPI per page
pdftotext -layout pack.pdf txt.txt          # text layer, in layout order
pdftoppm -png -r 110 pack.pdf page          # rasterise for vision QA
```

`pdfinfo`'s **Producer/Creator** names the real engine. `Skia/PDF` + `HeadlessChrome` means an
HTML deck through the browser print path — expect page-geometry and browser-furniture
failures. `WeasyPrint` means a styled HTML document — expect content spilling onto orphan
pages instead, not slide splitting.

Document-cache PDFs may be mode-restricted (`/root/.hermes/cache/documents/*`); `cp` them to
a writable workdir before running `qpdf`/`pdftoppm` or you will chase a phantom permission
error that has nothing to do with the PDF.

## Detector 1 — page count vs designed count

A count mismatch *is* the diagnosis. `Pages` at double the number of designed blocks means the
print box is smaller than the block and every block split. The near-empty companion pages
confirm it. Fix the CSS, re-render, re-count.

## Detector 2 — ink coverage

```bash
python3 - <<'EOF'
import glob
from PIL import Image
for f in sorted(glob.glob('/tmp/qa/page-*.png')):
    im = Image.open(f).convert('L'); w,h = im.size; px = im.load()
    dark = tot = 0
    for y in range(0,h,3):
        for x in range(0,w,3):
            tot += 1
            if px[x,y] < 235: dark += 1
    print(f, f"{100*dark/tot:5.2f}%")
EOF
```

Broken pack (24 pp): populated pages 0.3–3.5 %, four pages under 0.7 %. Same deck after the
CSS fix (12 pp): 5.5–24 %. Healthy WeasyPrint dossier the same day (29 pp): 1.75–30 %, with
one outlier at 1.75 % where a summary item spilled alone. A single low outlier is normal in
WeasyPrint output; a *cluster* of near-empty pages is not.

## Detector 3 — raster aspect ratio vs container

The most expensive defect, because it survives the page-geometry fix and looks fine on a page
thumbnail. `pdfimages -list` gives native dimensions:

| Page | Native raster | Ratio | Verdict |
|---|---|---|---|
| 8 | 5578 × 2778 | 2:1 | plot frame is 2:1 — the geology inside sits in a ~110 px band |
| 10 | 2083 × 1155 | 1.8:1 | acceptable in its column |
| 18 | 3000 × 2200 | 1.36:1 | acceptable |

A 2:1 raster in a wide short card is the signature: the source figure's y-axis was scaled to
the full crustal column (Moho included), so everything interpretable compressed to a ribbon
while the plot's top margin stayed empty. **Fix the figure, not the page** — crop the depth
axis to the interval that carries data, put the deep reference horizon in an inset.

## Detector 4 — orientation / datum consistency

One cross-section slide carried four conflicting direction statements:

- slide title: `NW–SE Cross-Section`
- in-figure title: `Semporna to Dangerous Ground (NE–SW)`
- footer: `SE–NW Cross-Section through Sabah`
- x-axis: `Distance from Semporna (km)`, 0 → 400, reading guide placing SE on the left

Build the check into the generator: keep direction tokens in one variable and interpolate, so
an edit cannot desynchronise them. A specialist reading three conflicting orientations stops
trusting every other number in the pack.

## Detector 5 — annotation size and contrast

In-figure annotation rendered at ~7–8 px cap height (≈0.55 % of slide width) against a ~1.5 %
projection threshold — legible zoomed on a monitor, dead on a projector or print reduction.
Measure the rendered page, not the source SVG. Contrast is the companion failure: red text on
a maroon fill was the lowest-contrast label in the pack. Any label on a dark or saturated fill
needs a backing plate.

## What was already right (say so)

An audit that only lists defects is not a verdict. The same pack had a verified citation (DOI
resolved to Cottam et al. 2013, *JGS London* — journal, year, authors all correct), consistent
three-domain colour logic, honest epistemic tags (`OBS`/`INT`/`SPEC`) on every claim, and a
proper four-thermochronometer cooling plot. State what holds — that is what tells the reader
how much of the rest to keep.

## Reporting shape

Lead with cause, not symptom. "The PDF is broken because the print box is smaller than the
slide" is actionable; "the figures are missing" sends the reader hunting for a render bug that
does not exist. Then separate defects sharing one root cause from defects needing independent
work, and say which is which. Deliver the fixed artifact with the audit — a corrected re-render
(`--no-pdf-header-footer`, `margin: 0`) is cheap and proves the diagnosis.
