# PDF & Image Toolchain

Depth companion to `human-facing-artifact-design` §8. Load when actually building the file.

## Choosing the build path

- Multi-slide visual packs and anything HTML-shaped → Chrome headless (see `FORGE-artifact-publisher` §6).
- Data-driven documents — resumes, dossiers assembled from Python structures, chart-and-table reports → **ReportLab** directly. Deterministic pagination, custom page furniture, no browser in the loop, repeatable builds.

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

## Matplotlib gotchas that cost time

- `plt.Rectangle` is **not exported** — `import matplotlib.patches as patches` and use `patches.Rectangle`.
- `Axes.text(x, y, ...)` raises `only 0-dimensional arrays can be converted to Python scalars` when `y` is a numpy slice. Collapse to a scalar first (`float(np.mean(y))`) before labelling a band or layer.
- A user style sheet can inject unsupported rcParams (e.g. `legend.bbox_to_anchor`) and emit a `Bad key` warning on every run. Cosmetic — the figure still writes.
- Both x and y for a band label must be scalars; compute midpoints from means, never from arrays.

### Geological cross-sections must read the right way up

- Iterate stratigraphic units strictly **top → bottom** (youngest first), accumulating thickness, and band each one with `fill_between`.
- Invert the depth axis explicitly: `ax.set_ylim(max_depth, -margin)` so depth increases downward. Forgetting this produces a section that reads upside down — the most common rejection.
- Draw the water layer from 0 to the water depth, and label a unit only when its mean thickness exceeds a floor (e.g. 0.15 km), otherwise labels collide.
- Wells: vertical line from 0 to TD, a marker at the wellhead, a tick at the target depth, and the name in a boxed annotation.

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
