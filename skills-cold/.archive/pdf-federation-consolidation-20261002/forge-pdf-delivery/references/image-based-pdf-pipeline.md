# Image-Based PDF Generation — Page-by-Page Pipeline

When the deliverable needs visual layout control per page — diagrams, charts, custom typography, multi-language code-switching — generate each page as a high-resolution PNG with matplotlib, then compile into a PDF with WeasyPrint.

This is **not** the markdown → HTML → PDF path. Use this when:
- Each page is a custom layout (not flowing prose)
- You need precise control over header, footer, color blocks, callout boxes
- Content includes inline equations, scientific notation, or complex visualizations
- Pages have specific background colors (dark themes, gradient banners, etc.)

## When to use this vs the markdown path

| Use markdown path when | Use image-based path when |
|---|---|
| Long flowing text | Per-page custom layout |
| Standard academic report | Magazine-style with banners/footers |
| Tables and lists are sufficient | Need diagrams, colored boxes, math symbols |
| One consistent font/style | Multiple text styles per page |
| Source of truth is .md file | Source of truth is Python script |

## Pipeline (use this exact order)

### Step 1 — Set up the canvas constants ONCE

```python
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle

# A5 portrait is the sweet spot for readable magazine-style content
PAGE_W, PAGE_H = 5.83, 8.27  # inches
ASSETS = "/path/to/assets/"
os.makedirs(ASSETS, exist_ok=True)
```

### Step 2 — Define a `make_page()` helper

Every page should share header and footer. Define once:

```python
def make_page(page_no, total, title=None):
    fig = Figure(figsize=(PAGE_W, PAGE_H), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    # Top accent line (gold 5pt-thick band)
    ax.add_patch(Rectangle((0.05, 0.96), 0.9, 0.005, facecolor=GOLD))
    # Header label
    ax.text(0.05, 0.945, f"GUIDE · {page_no:02d}", fontsize=7, color=GREY, family='serif')
    ax.text(0.95, 0.945, f"{page_no:02d} / {total:02d}",
            fontsize=7, color=GREY, ha='right', family='serif')
    # Optional page title
    if title:
        ax.text(0.5, 0.91, title, fontsize=10, color=INK, family='serif',
                fontweight='bold', ha='center', style='italic')
    return fig, ax
```

`axis('off')` is mandatory — never let matplotlib draw axes ticks on the PDF.

### Step 3 — Each page: build, save, never batch in same call

Save each page as a separate PNG. Batching causes memory issues at 14+ pages.

```python
canvas = FigureCanvasAgg(fig)
canvas.print_png(f"{ASSETS}/p03_content.png")
plt.close(fig)
```

Use sequential numbering (`p02`, `p03`...) so the order is preserved even if generation fails midway.

### Step 4 — Compile to PDF using base64-embedded images

WeasyPrint's `<img>` tag must point to a real file OR a data URL. Data URLs survive file moves and PDF relocation:

```python
import os, base64
from weasyprint import HTML

def img_to_data_url(p):
    with open(p, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{b64}"

order = ["cover.png", "p02_toc.png", "p03_content.png", ...]  # sorted
html = ['<!DOCTYPE html><html><head><meta charset="utf-8">',
        '<style>@page { size: 148mm 210mm; margin: 0; }',
        'body { margin:0; padding:0; }',
        '.page { page-break-after: always; width:148mm; height:210mm; overflow:hidden; }',
        '.page img { width: 100%; height: 100%; display: block; object-fit: contain; }',
        '.last { page-break-after: auto; }</style></head><body>']
for i, f in enumerate(order):
    cls = "page last" if i == len(order)-1 else "page"
    html.append(f'<div class="{cls}"><img src="{img_to_data_url(ASSETS+chr(47)+f)}" /></div>')
html.append('</body></html>')
HTML(string=''.join(html)).write_pdf(OUT_PDF)
```

Set `@page { size: 148mm 210mm }` to match the Figure figsize exactly. Any mismatch causes silent cropping.

## Pitfalls (these WILL cost you a re-render)

### Pitfall 1 — Vision cannot OCR image-based PDFs

After WeasyPrint compilation, `pdftotext` returns empty because the PDF is essentially scanned images. **You cannot verify content textually** — you must use vision_analyze on each rendered page.

**Workflow fix:** After each page generation, run vision_analyze on the PNG before adding to the PDF order. Catch typos/truncations page-by-page, not all-at-once at the end (where the cost is rebuilding the whole PDF).

### Pitfall 2 — Text truncation at right edge

Matplotlib does NOT auto-wrap text. If a sentence is too long for the column width, characters get cut off mid-word. Vision will read "alpha mde" when source was "alpha male".

**Defensive rules:**
- Keep body text to 70 characters max per line for narrow columns
- For short content lines (under 50 chars), use larger font (8pt) — feels readable
- For longer content lines (50-90 chars), use smaller font (6.5pt) and shorter text
- Test with the longest possible content first

**Symptom:** Vision reports "Text appears truncated/clipped at the right edge" or shows incomplete words like "mde" or "Sesual" instead of intended words. Always read back your code source vs rendered output.

### Pitfall 3 — Banner overlap with title

When you stack a main title + subtitle + content, matplotlib positions them at fixed y-coordinates. If the subtitle text is long, it overlaps with the next content block.

**Fix:** Keep subtitle text under 30 characters. For longer subtitles, push the next content block down by 0.02-0.03 units.

### Pitfall 4 — Cover image AI-generated text artifacts

When you use an AI image generator (qwen-image-plus, wan, etc.) for the cover photo, the model often adds fake text/logo overlays ("MASTORY", "ALPHA", etc.) that look unprofessional.

**Fix:**
1. Inspect the AI output via vision BEFORE adding banner overlay
2. Make the opaque banner tall enough (≥ 200pt) to fully cover the AI text
3. Use 100% opaque background (alpha=1.0), not semi-transparent — semi-transparent leaks the underlying AI text

### Pitfall 5 — Unicode glyph missing

DejaVu Serif (default matplotlib font) lacks many symbols:
- ⚠ (warning sign) — fails
- ✅ ❌ (check/cross) — fails
- letterspacing (text property) — fails
- some emoji — fails

**Fix:** Replace with text equivalents:
- ⚠ → "Peringatan:" or just bold heading
- ✅ → "OK" or "BETUL"
- ❌ → "X" or "TIDAK"
- letterspacing → use space between chars manually, or use Title Case

### Pitfall 6 — Vision re-rendering takes 10-20 seconds per page

For 14-page PDFs, full vision verification = 3-5 minutes. Don't re-run vision on every page after every typo fix. Verify on:
- Cover (always — AI artifact risk)
- One early content page (template renders correctly?)
- One middle content page (consistency)
- One late content page (text overflow risk at bottom)
- Cover page last (after banner fix)

If those 5 pass, the middle usually passes too.

### Pitfall 7 — Background colors

Use a consistent palette. Random colors per page = visual noise. Define once:

```python
BG = "#f5f1e8"      # warm cream paper
INK = "#1c1c1c"     # near-black text
GOLD = "#a8884a"    # warm gold accent
GOLD_LITE = "#c9a961"
GREY = "#7a7a7a"
RED = "#a3180f"
GREEN = "#2f6b3a"
BLUE = "#2a4d7d"
LIGHT = "#f5f0e1"
DARK = "#0e0e0e"
```

## Final verification checklist

Before declaring done:

1. **File verify:** `import pypdf; print(len(pypdf.PdfReader(OUT_PDF).pages))` — page count must equal designed page count
2. **Size check:** PDF file size > 500 KB suggests images embedded correctly. < 100 KB = problem (WeasyPrint may have skipped images)
3. **Vision check 5 sample pages:** cover, page 2, middle, last, and one with tables/diagrams
4. **Text accuracy:** Read back source code vs rendered text for typos, especially long words
5. **Deliver via MEDIA:** Include absolute path with `MEDIA:/full/path/to.pdf`

## Compile-and-save pattern that works

```python
import os, base64
from weasyprint import HTML

ASSETS = "/path/to/assets/"
OUT_PDF = "/path/to/output.pdf"

order = sorted([f for f in os.listdir(ASSETS) if f.endswith('.png')])

def img_to_data_url(p):
    with open(p,'rb') as f: b=base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{b}"

html=['<!DOCTYPE html><html><head><meta charset="utf-8">',
      '<style>@page { size: 148mm 210mm; margin: 0; }',
      'body { margin:0; padding:0; }',
      '.page { page-break-after: always; width:148mm; height:210mm; overflow:hidden; }',
      '.page img { width: 100%; height: 100%; display: block; object-fit: contain; }',
      '.last { page-break-after: auto; }</style></head><body>']
for i,f in enumerate(order):
    cls = "page last" if i == len(order)-1 else "page"
    html.append(f'<div class="{cls}"><img src="{img_to_data_url(ASSETS+chr(47)+f)}" /></div>')
html.append('</body></html>')
HTML(string=''.join(html)).write_pdf(OUT_PDF)
print(f"PDF: {OUT_PDF}, {os.path.getsize(OUT_PDF)/1024:.0f} KB")
```

## When NOT to use this

- Single page with just paragraphs → use markdown → WeasyPrint directly
- 50+ pages → consider HTML/CSS print engine instead, image-based doesn't scale
- Confidential content where you need searchable text layer → use markdown path, this path is image-based so text is not searchable

## Real cost observed in one session

14-page PDF, A5 portrait, full visual layout per page:
- Page generation: 30-60 seconds per page
- Compilation: 5-10 seconds
- Vision verification (5 pages): 60-100 seconds
- Defect fixing (vision caught typos): 2-3 cycles × 30 seconds
- **Total: ~15 minutes for a 14-page magazine-style PDF**

Acceptable when the user expects a polished deliverable. Not acceptable for "quick summary" requests — use markdown path instead.
