---
name: reportlab-pdf-professional
description: Professional PDF generation with ReportLab for arifOS — colWidths, LEADING, SEAL block, cover page pattern
triggers:
  - generate pdf reportlab
  - wsj grade pdf
  - seal 999 pdf
  - professional report python pdf
tags:
  - devops
  - pdf
  - reportlab
created: 2026-05-07
---

# ReportLab Professional PDF Generation — arifOS Standard

## Context
Used to generate SEARAH-EXPOSE-v13-CLEAN.pdf — a 9-page WSJ-grade investigative document with SEAL 999 commitment block. Required 3 iterations to fix margin/overflow issues.

## Key Learnings (v14 — Multi-Template System)

### BaseDocTemplate + PageTemplate + Frame (NOT SimpleDocTemplate)
Use this for PDFs with distinct cover, content, and SEAL page layouts:
```python
from reportlab.platypus import (Paragraph, Spacer, Table, TableStyle,
                                 KeepTogether, PageBreak, HRFlowable,
                                 BaseDocTemplate, PageTemplate, Frame,
                                 NextPageTemplate)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

W, H = A4
ML, MR, MT, MB = 20*mm, 20*mm, 18*mm, 16*mm  # margins
CW = W - ML - MR  # content width

doc = BaseDocTemplate(OUTPUT, pagesize=A4,
    leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB)

# Cover frame (full page, no margins needed)
cover_frame = Frame(0, 0, W, H, id='cover', showBoundary=0)

# Body frame (with margins)
body_frame = Frame(ML, MB, CW, H-MT-MB, id='body', showBoundary=0)

# Cover page template
cover_tpl = PageTemplate(id='Cover', frames=[cover_frame],
    onPage=lambda c, d: None)  # cover has own draw() method

# Content page template (header + footer)
body_tpl = PageTemplate(id='Content', frames=[body_frame],
    onPage=on_page_body)  # draws gold header rule + page number

# SEAL page template (navy background, no header)
seal_tpl = PageTemplate(id='Seal', frames=[body_frame],
    onPage=on_page_seal)

doc.addPageTemplates([cover_tpl, body_tpl, seal_tpl])

# In story: switch templates
story.append(PageBreak())  # force new page
story.append(NextPageTemplate('Seal'))
story.append(Spacer(1, 20))
# ... SEAL content ...
```

### onPage Callback Signature — MUST be (canvas, doc)
```python
# WRONG (causes TypeError or silent blank pages):
def on_page_body(canvas):
    ...

# RIGHT:
def on_page_body(canvas, doc):
    canvas.saveState()
    ...
```

### Cover Frame with Zero Padding (Critical Fix)
When using BaseDocTemplate + PageTemplate for cover page, the cover Frame MUST use zero padding:
```python
# WRONG — causes LayoutError on page 2:
cover_frame = Frame(0, 0, W, H, id='cover', showBoundary=0)

# RIGHT — zero padding eliminates frame boundary overflow:
cover_frame = Frame(0, 0, W, H, id='cover', showBoundary=0,
    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
```
This prevents: `LayoutError: Flowable <CoverPage> too large on page 2 in frame 'cover'`
when the cover Frame dimensions don't match the body frame on subsequent pages.

### CoverPage as Flowable Subclass
```python
class CoverPage(Flowable):
    def __init__(self, w, h):
        super().__init__()
        self.width = w
        self.height = h

    def wrap(self, aw, ah):
        return (self.width, self.height)  # CLAIM this size, don't negotiate

    def draw(self):
        c = self.canv
        # Full cover design — navy bg, gold bars, title, author, SEAL footer
        c.setFillColor(HexColor('#0d1b2a'))
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        # ... all drawing here ...
```

### colWidths Must Sum to EXACT Content Width
```python
CW = W - ML - MR  # e.g., 595pt - 40pt = 555pt
# WRONG: sum(colWidths) < CW  → right column clips or collapses
# RIGHT: sum(colWidths) == CW  (every pt accounted for)
```

### LEADING > Font Size
```python
BODY = PS('Body', fontName='Helvetica', fontSize=10, leading=13, ...)
# leading=13 for fontSize=10 (ratio ~1.3)
# leading=11.5 for fontSize=8 (ratio ~1.4)
# If text clips vertically → increase leading, not fontSize
```

### Two-Pass Rendering for Full Documents
```python
# First pass: measure content height
from reportlab.platypus import BaseDocTemplate, Frame
doc = BaseDocTemplate(output_path, pagesize=A4)
# Use a single wide Frame to measure all content first
# Then assign heights

# Or: use SimpleDocTemplate and just set colWidths correctly
```

### SEAL Block (HMAC-SHA256 Commitment)
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm

SEAL = ParagraphStyle('SEAL', fontName='Courier', fontSize=7,
    leading=9, textColor=HexColor('#222'), backColor=HexColor('#f5f5f5'),
    leftIndent=6*mm, rightIndent=6*mm, spaceBefore=4*mm, spaceAfter=4*mm)
# Use 7pt Courier minimum (6.5pt clips at some PDF viewers)
```

### SEAL Block Design (v14 — No Word Wrap Issues)
```python
# SEAL block needs to handle long hex strings without breaking
# Use a Table with one column, fixed width = CW
seal_data = [
    [Paragraph(f"<b>SEAL 999 — HMAC-SHA256 COMMITMENT</b>", SEAL_HEAD)],
    [Paragraph(f"<b>Document:</b> SEARAH: The Deal That Could Reshape...", SEAL)],
    [Paragraph(f"<b>Commitment:</b>", SEAL)],
]
seal_table = Table(seal_data, colWidths=[CW])
# Hash rows in separate Table with small colWidths
hash_data = [[Paragraph(h, SEAL)] for h in hash_items]
hash_table = Table(hash_data, colWidths=[CW])
```

### Page Count Off / Blank Pages
```python
# If PDF renders with 0 pages or wrong count:
# 1. Check onPage callbacks have (canvas, doc) signature
# 2. Check PageTemplate has Frame assigned (BaseDocTemplate needs frames)
# 3. Check NextPageTemplate is imported and used correctly
# 4. Check story.append() vs story.extend() — mixed returns cause issues
```

### Flowable Subclassing Pattern (Cover Page)
```python
class CoverPage(Flowable):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
    def draw(self):
        c = self.canv
        # draw cover elements
    def wrap(self, aw, ah):
        return (self.width, self.height)
```

## Common Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| Right column text clips | sum(colWidths) < frame width | Add 1-2mm to last column or reduce padding |
| SEAL block text at x=-3.0 | 6.5pt Courier too small | Use 7pt Courier minimum |
| Flowable subclassing breaks | `super().__init__()` missing | Always call super() |
| story.append() fails with Flowable list | Return value not list | story.extend() for Flowable lists |
| Page count off by 1 | Last element didn't fit | Add Spacer(10*mm) at end of body |
| WeasyPrint flexbox broken | Flexbox/grid unsupported in WeasyPrint | Use ReportLab instead for complex layouts |

## Dependencies
```bash
pip install reportlab
# Optional: fitz (PyMuPDF) for PDF verification
```

## Alternative: Two-Pass PDF (Simpler, Recommended)
When you need a cover + multiple content pages and the BaseDocTemplate + Frame approach
is causing LayoutError or frame mismatch issues, use the two-pass approach instead:

```python
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, ...
from reportlab.lib.pagesizes import A4

W, H = A4

# PASS 1: Cover drawn directly on canvas
c = pdfcanvas.Canvas(OUTPUT, pagesize=A4)
# ... draw cover elements using c.setFillColor(), c.rect(), c.drawCentredString() ...
c.showPage()  # finish cover

# PASS 2: Rest of document via SimpleDocTemplate
doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm, topMargin=16, bottomMargin=18,
    author="Hermes ASI", title="...")
def on_later_pages(c_obj, doc_obj):
    c_obj.saveState()
    # draw header/footer
    c_obj.restoreState()
story = [Paragraph(...), ...]
doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
```
This completely avoids the Frame/LayoutError complexity for cover + content documents.
PyMuPDF can verify: `fitz.open("output.pdf").page_count` (should show 8+ pages).

## Canonical Files
- `/root/AAA/SEARAH/generate_pdf_v14b.py` — canonical working example (BaseDocTemplate + PageTemplate + Frame, 4 pages)
- `/root/AAA/SEARAH/SEARAH-EXPOSE-v14-FINAL.pdf` — output reference (4 pages: cover + 2 content + SEAL page)
- `/root/HERMES/hatyai_dinner/generate_hatyai_v2.py` — working two-pass example (canvas cover + SimpleDocTemplate body, 8 pages)
