# PDF & Image Toolchain

Depth companion to `human-facing-artifact-design` §8. Load when actually building the file.

## Choosing the build path

- Multi-slide visual packs and anything HTML-shaped → Chrome headless (see `FORGE-artifact-publisher` §6).
- Data-driven documents — dossiers assembled from Python structures, chart-and-table reports → **ReportLab** directly. Deterministic pagination, custom page furniture, no browser in the loop, repeatable builds.
- HTML that already declares its own page geometry with `@page { size: A4; margin: ... }` → **print it with the browser**, no shell call and no PDF library (next section). When the layout work is already done in CSS, re-implementing it in ReportLab is duplicated effort and a second place for the two to drift.

## HTML → PDF through the browser's own print pipeline

An artifact that sets its own `@page` rule can be printed by the browser it is already being viewed in. This is the shortest path for a styled one-to-two page document (résumé, one-pager, brief):

```python
import base64
new_tab("file:///abs/path/artifact.html")
wait_for_load()
res = cdp("Page.printToPDF",
          printBackground=True,        # default False silently drops every CSS background
          preferCSSPageSize=True,      # defer to the artifact's @page rule
          paperWidth=8.27, paperHeight=11.69,   # fallback when no @page is declared
          marginTop=0.51, marginBottom=0.47, marginLeft=0.55, marginRight=0.55)
with open(out_pdf, "wb") as f:
    f.write(base64.b64decode(res["data"]))
```

- `printBackground=True` is mandatory for any themed document. Without it the browser omits background colour and a light card on a coloured page arrives as an unstyled white sheet — the artifact looks broken rather than unthemed.
- Then extract text from the built PDF in the same session before delivering. A render that dropped a stylesheet, or a section that failed to lay out, is invisible in the HTML source and obvious in the extracted text.
- **Assert every embedded image decoded before printing.** For a document carrying base64 figures, check `[...document.images].every(i => i.complete && i.naturalWidth > 0)` in the loaded page. A base64 image that fails to decode prints as a silent gap while the page still measures as non-blank — so page count, character count and ink coverage all pass a document with a missing figure.
- Deliver with `MEDIA:/abs/path.pdf`.

## ReportLab recipes

### Paged footer ("Page N of M" on every page)

Subclass the canvas and buffer pages so the total is known before any footer is drawn:

```python
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

class PagedCanvas(canvas.Canvas):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._pages = []
    def showPage(self):
        self._pages.append(dict(self.__dict__))
        canvas.Canvas.showPage(self)
    def save(self):
        total = len(self._pages)
        for i, page in enumerate(self._pages):
            self.__dict__.update(page)
            self._footer(total, i + 1)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    def _footer(self, total, pg):
        self.saveState()
        self.setFont("Helvetica", 6)
        self.drawString(16*mm, 8*mm, "LABEL | ORGAN | CONFIDENTIAL")
        self.drawRightString(194*mm, 8*mm, f"{pg}/{total}")
        self.restoreState()

doc.build(elements, canvasmaker=PagedCanvas)
```

Buffering `self.__dict__` per page is what makes "of M" possible — a footer drawn inside `showPage` never knows the total.

### Dark full-bleed page theme (personal / reflective documents)

For a document with a coloured page background (dark theme, warm gold text), do **not** subclass
the canvas — pass page callbacks to `SimpleDocTemplate`. They run before the flowables draw, so a
filled rect becomes the backdrop, and the same callback is the simplest place for a centred page
number:

```python
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4

BG, GOLD, DIM = HexColor("#1a1a2e"), HexColor("#d4a574"), HexColor("#8a7060")

def draw_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFont(body_font, 8)
    canvas.setFillColor(DIM)
    canvas.drawCentredString(A4[0]/2, 15*mm, f"— {doc.page} —")
    canvas.restoreState()

doc.build(story, onFirstPage=draw_bg, onLaterPages=draw_bg)
```

Setting `bg=None` on `SimpleDocTemplate` does not affect the page background — the callback is the
only mechanism.

**Register the font family explicitly — base and bold are separate faces.** One TTF registration
gives you exactly one face and there is no implicit bold. Discover the files instead of hardcoding
paths:

```python
import glob
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

for fp in glob.glob("/usr/share/fonts/truetype/**/*.ttf", recursive=True):
    if "dejavuserif" in fp.lower() and fp.endswith(".ttf"):
        name = "DejaVuSerif-Bold" if "bold" in fp.lower() else "DejaVuSerif"
        pdfmetrics.registerFont(TTFont(name, fp))
```

Referencing `"DejaVuSerif-Bold"` without registering it falls back silently to a default font — on
a dark page that is a visible style break, not a subtle one.

**Every style needs its own colour; there is no global text colour.** A `canvas.setFillColor`
inside the page callback does not reach flowable text. Each `ParagraphStyle` carries its own
`textColor`, so on a dark background a style you forgot to colour renders **invisible**, not merely
inconsistent. Set it on title, subtitle, heading, body, quote, footer and intro styles explicitly,
and pass an explicit light `color=` to every `HRFlowable` — the default rule colour is near-black
and vanishes against the theme.

Dark-theme checklist: every style has an explicit light `textColor`; every divider has an explicit
light `color`; the callback fills the rect before drawing the page number; and the normal §3
density check still applies unchanged (`page.get_text()` is unaffected by background colour).

**A style `parent` must be a style object, not a style name.** If a string reaches the paragraph
parser where a style is expected, ReportLab fails with `'str' object has no attribute 'fontName'`
(and a follow-on `'str' object has no attribute 'name'`) from `paraparser._initial_frag` — an error
that names neither your variable nor your paragraph, so it reads as a ReportLab bug rather than a
bad argument. Build styles through a small factory that always receives `parent=<style object>`, and
keep one helper per document so every style is constructed the same way:

```python
def mk(name, **kw):
    base = dict(fontName=body_font, fontSize=9, textColor=GOLD, leading=14, spaceAfter=3*mm)
    base.update(kw)
    return ParagraphStyle(name, **base)   # name is a label, never a parent
```

When a build fails with an attribute error inside `paraparser`, check the style arguments before
touching the content.

### Section header band

Wrap each title in a one-cell Table with a background colour. Gives a coloured band without drawing primitives or measuring text:

```python
t = Table([[Paragraph(title, h1_style)]], colWidths=[178*mm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), TEAL),
    ("LEFTPADDING", (0, 0), (-1, -1), 3*mm),
    ("TOPPADDING", (0, 0), (-1, -1), 2*mm),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2*mm),
]))
```

### Info-box grids (spec sheets, key-fact panels)

A single-row `Table` with `colWidths=[43.5*mm] * 4` plus `INNERGRID` and `BOX` in the accent colour produces the four-cell fact panel and paginates cleanly. Set `VALIGN TOP` and use a 7pt `ParagraphStyle` for the cell body.

### Density control

Values that hold up at document density: body 8–9pt with 10.5–12pt leading; section headers 8.5–11pt bold; info-box text 7–7.5pt with 9.5–10pt leading. Tighten `topMargin`/`bottomMargin` to ~10–14mm for dense two-page documents; below ~8mm the body collides with the footer band.

### Verify the build — this is the §3 density check

Assert page count and per-page character count from the built PDF instead of trusting the layout:

```python
import pymupdf
doc = pymupdf.open(path)
for i, page in enumerate(doc):
    print(i + 1, len(page.get_text()))
```

Two dense A4 pages land around 3.5k–4.5k characters each. A page under ~2k is under-filled — fix the layout, do not ship it. A page returning a few hundred characters usually means content overflowed to nowhere or a table failed to render.

### Ink coverage — the complementary check (§3)

Character count catches emptiness; it does not catch a page that has a few lines of text but reads visually empty. Rasterise the pages, then compute dark-pixel share for each:

```python
# first: pdftoppm -png -r 100 out.pdf /tmp/qa/page
from PIL import Image
import glob

for f in sorted(glob.glob("/tmp/qa/page-*.png")):
    im = Image.open(f).convert("L")
    w, h = im.size
    px = im.load()
    dark = tot = 0
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            tot += 1
            if px[x, y] < 235:
                dark += 1
    print(f, f"{100 * dark / tot:5.2f}%")
```

Healthy text-and-figure pages sit roughly 4–25%. **A single page an order of magnitude below its
neighbours is the signature of a stranded fragment**, not of intentional design — typically a
closing epigraph, signature block or footer that overflowed onto a page of its own. Fix it by
tightening that block's top margin and leading so it joins the preceding page, and by shortening
its line lengths if that is what makes it fit. Do not delete the block and do not pad it with
filler.

**Exclude pages designed to be figure-only before thresholding.** A one-figure-per-page layout
legitimately reads 3–15 % ink, because the figure's own white margins dominate the raster — so a flat
"under 2 % is a defect" rule reports every correct figure page as broken. Rank the pages and inspect
the outlier instead of thresholding each one, and pair ink with the per-page embedded-image count
(`len(page.get_images(full=True))`) so a figure page and a blank page are told apart before you "fix"
a layout that was already right.

Skip this sweep when the active model has no vision lane; the numbers are the whole check, and a
page-count match alone will not report a stranded page (the fragment still counts as a page).

**Rasterise in memory instead of shelling out to `pdftoppm`.** `pymupdf` renders each page without a
PNG round-trip, and sampling the **modal** pixel value first (rather than thresholding against
white) makes the same snippet correct on a dark page as well as a light one:

```python
import pymupdf, collections

doc = pymupdf.open(path)
for i, page in enumerate(doc):
    pm = page.get_pixmap(dpi=72)
    vals = pm.samples[::3][:60000]
    modal = collections.Counter(vals).most_common(1)[0][0]   # the page background
    ink = sum(1 for v in vals if abs(v - modal) > 24) / len(vals)
    print(i + 1, len(page.get_text()), "%.2f%%" % (ink * 100))
```

Dense A4 text pages land near 9–13% by this measure. Read the numbers **relative to each other**
within one document — the absolute value shifts with page size, margin and type size, so a
cross-document threshold is not meaningful; a page far below its siblings is the finding.

## Matplotlib gotchas that cost time

- **`print_png()` and `Figure.savefig()` reject `dpi` as a keyword argument** when called on a `FigureCanvasAgg` instance — pass `dpi` to `Figure(figsize=...)` constructor instead, then `print_png()` without arguments. A `TypeError: FigureCanvasAgg.print_png() got an unexpected keyword argument 'dpi'` mid-script costs a turn to diagnose.
- **A malformed `mplstyle` in the user config dir (e.g. `~/.config/matplotlib/stylelib/`) can throw on every save.** Symptoms: `Bad key 'legend.bbox_to_anchor' in file ...` followed by `Style Error:`. The figure still renders — but every call prints a stack trace that looks fatal. Delete the offending `.mplstyle` file and the warning disappears. Check `~/.config/matplotlib/stylelib/` before debugging the agent code.
- **`Axes.text(...)` does NOT accept `letterspacing=` as a kwarg.** It throws `AttributeError: 'Text' object has no property 'letterspacing'`. Spread-letter is achieved via `fontproperties` (using a `FontProperties` with `style='normal'`) or by inserting space characters manually between letters. Using `letterspacing` looks like a typo and wastes a turn.
- **Matplotlib auto-DPI on this host can produce bizarre oversized images** (e.g. a 1024×1365 figure written as 285,643×622 px). When `figsize` is set in inches and the output PNG is implausibly wide, the `matplotlibrc` is being overridden somewhere — typically a stale `~/.config/matplotlib/matplotlibrc` or a rogue `mplstyle`. **Fix by constructing the figure explicitly**: `fig = Figure(figsize=(W/100, H/100))` + `canvas = FigureCanvasAgg(fig)` + `canvas.print_png(path)` (no dpi kwarg). This bypasses pyplot's rcParams lookup and gives a predictable size.
- `plt.Rectangle` is **not exported** — `import matplotlib.patches as patches` and use `patches.Rectangle`.
- `Axes.text(x, y, ...)` raises `only 0-dimensional arrays can be converted to Python scalars` whenever `y` is an array rather than a scalar — a slice, or equally a **one-element array** returned by a helper you expected to give two floats (`xa, ya = curve(t)` yields length-1 arrays when `t` is a list rather than a linspace). Collapse explicitly: `float(np.mean(y))` for a band or layer, `float(xa[0])` for a single sample. The error names neither the variable nor the call, so grep for `ax.text(` and your curve helpers first when it appears after a refactor.
- A user style sheet can inject unsupported rcParams (e.g. `legend.bbox_to_anchor`) and emit a `Bad key` warning on every run. Cosmetic — the figure still writes.
- **Reserve head-room before a title band collides with the axes.** A `fig.suptitle` plus a `fig.text` subtitle drawn near the top edge gets overprinted the moment `tight_layout()` runs — and the line it eats is usually the figure's own provenance note, i.e. the disclaimer that makes the schematic admissible. Draw the header at about `y≈1.005` / `y≈0.963` and pass the reserve explicitly (`fig.tight_layout(rect=(0, 0.05, 1, 0.945))` when a legend also sits below the axes), then confirm both lines survived on the rendered PNG — the collision is invisible to every count-based check.
- Both x and y for a band label must be scalars; compute midpoints from means, never from arrays.

### Geological cross-sections must read the right way up

- Iterate stratigraphic units strictly **top → bottom** (youngest first), accumulating thickness, and band each one with `fill_between`.
- Invert the depth axis explicitly: `ax.set_ylim(max_depth, -margin)` so depth increases downward. Forgetting this produces a section that reads upside down — the most common rejection.
- Draw the water layer from 0 to the water depth, and label a unit only when its mean thickness exceeds a floor (e.g. 0.15 km), otherwise labels collide.
- Wells: vertical line from 0 to TD, a marker at the wellhead, a tick at the target depth, and the name in a boxed annotation.
- **The axis label and the tick signs must agree.** Ticks running `0 → −26` under a label reading "Depth below sea level (km)" is a contradiction a specialist spots in the first second. Either label the axis "Elevation relative to sea level (km)" for negative values, or carry positive depth and invert with `set_ylim(max_depth, -margin)` — and use the same convention in the caption.
- **No placeholder or unresolved token in rendered text** — no `?`, `(7.85–? Ma)`, `~7x`, `TBC`. Resolve it or drop the clause; one unresolved token makes the whole figure read as unchecked and discredits the resolved numbers beside it.
- **Every figure carries a legend**, and every schematic element says so (`schematic` / `indicative` / `not to scale`) in both the subtitle and the caption. Colour fills without a key read as unfinished; an unlabelled schematic passes interpretation off as measurement.
- **Structural geometry must be kinematically coherent** — a wedge has a décollement, a taper and a hinterland-verging thrust set, and every fault has a named sense. A pile of coloured polygons with two unlabelled red lines is a collage, and a specialist rejects the whole pack on it. The same test applies to bodies: a pluton is a tapered intrusion with a narrow stem rather than a rectangle, a carbonate platform has a build-up profile rather than constant thickness, and a seal follows the top of the unit beneath it. **A geological name obliges a geological shape** — geometry that contradicts its own label costs more trust than a missing element does.
- **A value the caption claims and the panel contradicts is worse than no value.** If the caption says a horizon lies at 45–60 km and the panel stops at 26 km, drop the claim or extend the panel.
- **Say where a schematic came from.** `built from published cross-sections and figures (<author year, journal vol:pages>); not re-picked from seismic` in the subtitle is the sentence that makes the figure admissible in a technical deliverable.

### Regional basemaps without a cartopy data download

Natural Earth vectors are served as GeoJSON from the Natural Earth repo — download and parse directly: no cartopy data-fetch step, and no projection library in the loop.

```python
BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
for f in ["ne_10m_land.geojson", "ne_10m_coastline.geojson",
          "ne_10m_admin_0_boundary_lines_land.geojson"]:
    urllib.request.urlretrieve(BASE + f, os.path.join(GEO, f))
```

- Use **10m** for a regional map. The 110m land file carries one polygon per continent with its vertices at extreme latitudes, so a regional bbox test over it finds nothing usable.
- **Clip by vertex count inside a padded bbox, never by a whole-feature bbox.** A continent feature's bbox spans the globe, so any regional test matches it and you end up drawing the world. Keep rings with at least a few vertices inside the window, padded by ~2° so the coastline closes at the frame edge.
- Draw land as filled patches first, then coastline rings as lines, then boundaries dashed.
- `ax.set_aspect(1.0 / np.cos(np.radians(mid_lat)))` renders the degrees at their true local shape; `aspect=1` visibly stretches a regional map away from the equator.
- **Furniture a specialist checks for, each a few lines:**
  - *North arrow* — `ax.annotate("", xy=(x, y_hi), xytext=(x, y_lo), arrowprops=dict(arrowstyle="-|>"))` plus a bold `N`. Never omit it on a frame that is cropped or rotated; a map without one reads as a plot.
  - *Scale bar with a representative fraction* — `dlon = km / (111.32 * np.cos(np.radians(mid_lat)))`, then label the bar `"100 km  (~1:2,200,000 at 5°N)"`. A bar with a length but no RF is not a scale, and a length in degrees with no stated latitude is worse.
  - *Block and well outlines in the water, clear of the coastline* — a licence rectangle crossing land is the fastest way to lose a specialist reader, and it is the one map defect that reads as carelessness rather than as a deliberate schematic.
  - *Graticule labels as degrees* — `f"{v}°E"`. Bare numbers read as a plot axis, not a map.
  - *Legend below the frame* — `ax.legend(..., loc="upper center", bbox_to_anchor=(0.5, -0.055), ncol=N, frameon=False)` with `tight_layout(rect=...)` reserving the space. A legend placed inside a regional map covers a landmass or a country label every time; vision QA catches it as "legend covering data".
- **Say which half of the map is real.** Caption the basemap as real geography (source and datum) and the block outlines, contours and well symbols as `indicative`, with a plain `not a licence map` where that is true. Naming the sourced half is what buys the reader's trust in the approximated half — and never draw a guessed coordinate pair as if it were the licence shape.
- Distinguish evidence classes by line style — solid for sourced or measured, dashed for indicated or schematic — so the reader does not need the caption to tell them apart.
- **`Line2D` has no `where` kwarg.** `ax.plot(x, y, where=cond)` raises `AttributeError: Line2D.set() got an unexpected keyword argument 'where'`. Mask instead: `ax.plot(x, np.ma.masked_where(~cond, y))`. `where=` is valid on `ax.step()` and `ax.fill_between()`, not on `ax.plot()` — grep every `where=` in a figure script before trusting the run.
- The full geo stack (`geopandas`, `shapely`, `pyproj`, `cartopy`, `rasterio`) is installed in the organ virtualenvs rather than the system interpreter or the agent venv — on this host `/root/GEOX/.venv/bin/python` carries all of them, so run figure scripts with that binary: `/root/GEOX/.venv/bin/python make_figs.py`. Probe the candidates with `importlib.util.find_spec` before installing anything — installing is the slow path, and a missing import in one interpreter is not evidence the stack is absent from the host:
  ```bash
  for v in /opt/arifos/venv /root/GEOX/.venv; do echo "== $v"; "$v/bin/python" -c "import geopandas, cartopy; print('geo stack OK')" 2>&1 | tail -1; done
  ```
  The Hermes sandbox carries `matplotlib` and `numpy` but not the geospatial stack — fine for a quick geometry check, wrong for a real basemap.

## Image generation (Gemini API)

Text-only Gemini models answer an image prompt with prose or inline SVG. To get real pixels:

- Use an image-capable model: `gemini-2.5-flash-image` (also `gemini-3-pro-image`, `nano-banana-pro-preview` on the same key).
- Set `generationConfig.responseModalities = ["IMAGE", "TEXT"]`.
- Read pixels from `candidates[0].content.parts[*].inlineData.data` (base64) — **not** from `text`. A response carrying only a `text` part means the model was not image-capable; switch the model rather than re-prompting.
- When a model name is rejected, enumerate what the key can reach:
  `GET https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY`
- API keys live in `/root/.secrets/kunci-root.env` and `/root/.secrets/kunci-mas.env`; load both before selecting a provider, and never echo the key.

### Prompt construction for logos and marks

State explicitly: the shape, the exact hex palette, the top/bottom composition, the style rejection (`no photographic elements, clean vector-style`), and the **destination** (`circular profile picture — keep elements centred, nothing critical near the edge`).

Iterate by adding the constraint that was violated — do not rewrite the whole prompt. When the user asks for a specific brand's inverse, shadow or anti-matter version, name the reference brand and the transformation (inverted, dissolving, palette shift) rather than describing an abstract mood.

For a circular platform avatar, request a 1:1 image with all critical elements centred; the platform crops to a circle and edge content is lost.
