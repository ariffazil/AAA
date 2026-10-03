# Browser-Print Layout Gate (headless Chrome → PDF)

Proven 2026-09-15: a 12-slide deck was delivered as a 24-page PDF carrying browser furniture
on every page, with two figures squashed below legibility. The content was correct. The
geometry was not. These checks catch that entire class.

## Why HTML decks break silently

Headless Chrome paginates; it does not respect intent. It emits one page per viewport-plus
overflow, inserts its own header/footer, and renders a figure at whatever share of its
container the flex layout grants it — all without a warning or a non-zero exit code.

## Check 1 — page count must equal designed page count

```bash
pdfinfo out.pdf | grep -E '^Pages'
```

12 slides → 24 pages is arithmetic, not mystery (`@page` box smaller than the `.slide` div).
Every surplus page is an overflow, and blank tails pair with the split.

```css
/* BROKEN: printable box is (297-2) x (210-2) mm — smaller than the slide */
@page { size: A4 landscape; margin: 1cm; }
.slide { width: 297mm; height: 210mm; }

/* FIXED: slide owns its padding, page supplies no margin */
@page { size: A4 landscape; margin: 0; }
.slide { width: 297mm; height: 210mm; padding: 18mm 22mm; }
```

Changing only that one line took the same deck from 24 pages / 0.3–3.5 % ink to 12 pages /
5.5–24 % ink. No content changed.

## Check 2 — strip browser furniture

```bash
google-chrome --headless --disable-gpu --no-sandbox \
  --no-pdf-header-footer \
  --print-to-pdf=out.pdf file:///abs/path/deck.html
```

Without `--no-pdf-header-footer`, every page carries the render timestamp, the document
title, and the raw `file:///` source path. That path is an internal filesystem leak on a
document sent to a third party. Verify after the fact:

```bash
pdftotext out.pdf - | grep -c 'file://'   # must be 0
```

## Check 3 — inspect the raster at native size, not the page

A figure can be present, correctly framed, and still useless. `pdfimages -list` gives the
native pixel dimensions and PPI of every embedded raster:

```bash
pdfimages -list out.pdf
```

A 5578×2778 raster (2:1) placed in a wide short card renders as a thin strip — this is a
**source-figure** defect, not a page-geometry one, and fixing `@page` will not touch it.
Fix at the source: crop the axis to the interval carrying data, move the deep reference
horizon to an inset. Below ~200 PPI, printed annotation will not hold; regenerate at higher
DPI rather than upscaling.

## Check 4 — cross-reference consistency

Any figure carrying a direction, age, datum or scale in more than one place must agree with
itself. In the 2026-09-15 pack, one cross-section was labelled three ways on a single slide:
slide title `NW–SE`, in-figure title `NE–SW`, footer `SE–NW`, while the x-axis read
`Distance from Semporna (km)` left-to-right. A specialist reader loses trust instantly.

Grep the source for the tokens (`NW`, `SE`, `Ma`, `km`) and confirm every occurrence agrees
before delivery. Same discipline for stated vertical exaggeration: if the subtitle claims
`~32×`, the figure needs a VE note or a scale bar, or the claim is decoration.

## Delivery checklist

1. Page count == designed count.
2. `pdftotext` shows zero `file://` and zero render timestamps.
3. No page under 2 % ink.
4. Every embedded raster checked at native aspect ratio against its container.
5. Directions, ages and scales agree everywhere they appear.
