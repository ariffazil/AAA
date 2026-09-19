# Measurement Recipes

Runnable snippets for verifying a rendered artifact. All assume Pillow + numpy for images and
`pymupdf` (imported as `pymupdf`; the `fitz` alias is deprecated) for PDFs.

---

## 1. Element presence — count pixels in the region where it should be

```python
from PIL import Image
import numpy as np

def element_pixels(png, rgb, tol=90, annulus=None):
    """Count pixels matching an accent colour. annulus=(r_in, r_out) restricts to a
    ring around the centre, for checking a border/ring was actually drawn."""
    a = np.asarray(Image.open(png).convert("RGB")).astype(int)
    m = np.abs(a - np.array(rgb)).sum(axis=2) < tol
    if annulus is not None:
        y, x = np.nonzero(m)
        r = np.sqrt((x - a.shape[1] / 2) ** 2 + (y - a.shape[0] / 2) ** 2)
        return int(((r > annulus[0]) & (r < annulus[1])).sum())
    return int(m.sum())
```

Zero in the annulus means the ring is not in the file, whatever the markup says.

---

## 2. Optical centre — ink centre of mass, not the bounding box

```python
from PIL import Image
import numpy as np

def ink_centre(png, rgb, tol=70, band=None):
    """band=(y0,y1) crops to just the element, so surrounding chrome cannot pull the mean."""
    a = np.asarray(Image.open(png).convert("RGB")).astype(int)
    if band:
        a = a[band[0]:band[1]]
    m = np.abs(a - np.array(rgb)).sum(axis=2) < tol
    y, x = np.nonzero(m)
    cy = y.mean() + (band[0] if band else 0)
    return float(x.mean()), float(cy)

# Compare against the canvas centre and require the residual to be small.
w = h = 1024
cx, cy = ink_centre("mark.png", (11, 61, 42), band=(250, 700))
assert abs(cx - w/2) <= 8 and abs(cy - h/2) <= 8, (cx, cy)
```

Arabic and other calligraphic display faces carry their ink mass right-of and above the advance-box
centre. Measure the offset once at the working size, apply it as a CSS `transform: translate(dx, dy)` on
the text element, then re-measure. The offset scales roughly with font size, so re-derive it after a
large size change.

---

## 3. Small-size legibility — percentile contrast inside the glyph zone

```python
from PIL import Image
import numpy as np

def legibility(png, size=40, disc_frac=0.34):
    im = Image.open(png).convert("L").resize((size, size), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    yy, xx = np.mgrid[0:size, 0:size]
    disc = ((xx - size/2)**2 + (yy - size/2)**2) < (size * disc_frac)**2
    v = a[disc]
    lo, hi = np.percentile(v, 5), np.percentile(v, 95)
    return {"contrast_ratio": round(float((hi + 1) / (lo + 1)), 2),
            "spread": round(float(v.std()), 1)}
```

The disc restriction is the point: measured over the whole canvas, bright chrome inflates the score and
the ranking between variants becomes meaningless. Report the numbers alongside the recommendation.

---

## 4. Per-page ink coverage — find stranded and blank pages

```python
import pymupdf, collections

def page_ink(pdf):
    d = pymupdf.open(pdf)
    out = []
    for i, pg in enumerate(d):
        pm = pg.get_pixmap(dpi=72)
        vals = pm.samples[::3][:60000]
        modal = collections.Counter(vals).most_common(1)[0][0]   # modal, NOT white
        ink = sum(1 for v in vals if abs(v - modal) > 24) / len(vals)
        out.append((i + 1, len(pg.get_text().strip()), round(ink * 100, 2),
                    len(pg.get_images(full=True))))
    return out
```

Reading the **modal** value rather than assuming white is what makes this work on dark-background
documents. Flag any page under ~2 % as a split or failed render, and any page with few characters but
an image as a figure page (expected).

---

## 5. Text content — assert against the source, never against a model

**HTML/SVG-rendered text:** the DOM string is the truth. Assert the codepoints you passed in:

```python
AR = "\u0627\u0644\u0623\u0645\u064a\u0646"   # الأمين
assert len(AR) == 6 and AR[2] == "\u0623"     # hamza must sit on the third alef
```

**Text inside a PDF:** extract the layer and assert on it.

```python
import pymupdf
d = pymupdf.open(pdf)
full = "".join(pg.get_text() for pg in d)
for token in ("SEAL-25d58123ed5543fa", "Bortfeld", "0.0 m"):
    assert token in full, token
```

This catches the case where a figure or caption silently failed to make it into the build.

---

## 6. Conditional-render diff — prove a detail is drawn, and where

Render the artwork twice: once with the detail, once without. Diff and check the difference lands where
it should.

```python
from PIL import Image, ImageChops
import numpy as np

arr = np.asarray(ImageChops.difference(Image.open(a_png).convert("L"),
                                       Image.open(b_png).convert("L")))
y, x = np.nonzero(arr > 60)
assert x.size > 40, "detail not drawn at all"

word_left, word_right = 321, 701                       # from the ink bbox
frac = (x.mean() - word_left) / (word_right - word_left)
# RTL text: the first letter is at the RIGHT. A detail on the 3rd of 5 letters sits mid-word.
assert 0.5 < frac < 0.75 and y.mean() < 120
```

Use for a diacritic, a hyphen, a unit suffix, a conditional annotation — anything where "is it there and
is it in the right place" is the question. Canvas `getImageData` on cross-origin images raises a
SecurityError, so do the diff with Pillow on saved PNGs rather than in-page.

---

## 7. Pass / fail gate before delivery

```
[ ] Every element believed drawn is confirmed by pixel count in its own region
[ ] Primary element centre of mass lands within ~8 px of canvas centre
[ ] Every content claim checked against source (DOM string / PDF text layer), not a model
[ ] Small-size gate run at the real consumption sizes, choice made on that sheet
[ ] Per-page ink coverage checked; no page an order of magnitude below its neighbours
[ ] Rendered pages actually LOOKED AT for composition, not only measured
[ ] Every fix re-measured and the new numbers quoted
[ ] Gaps named explicitly rather than filled with an unmeasurable number
```
