---
name: reportlab-page-template-architecture
category: pdf-generation
description: "Fix ReportLab PDFs where one PageTemplate bleeds into other pages — running headers, backgrounds, or drawing functions appearing on wrong pages. Root cause: shared Frame dimensions across PageTemplates."
---

# ReportLab PageTemplate Architecture Fix

## Context
When using ReportLab's PageMaker + Frame + PageTemplate system for multi-section PDFs (e.g., cover page, content pages, seal page), drawing functions from one template can inadvertently affect other pages if Frame dimensions are not properly isolated.

**Symptoms**
- Full-page background color (navy) appearing on ALL pages, not just the intended section
- Large section titles repeating across multiple pages
- Running headers visible on the cover page (or vice versa)
- Content appearing below the intended area on a specific page

**Root cause** — Multiple PageTemplate objects sharing a Frame with identical dimensions. When `draw_cover` (or any draw function) is called on a Frame, it paints over whatever is already on the canvas. If the cover Frame has the same dimensions as the content Frame, the cover's painter runs on every page that uses that Frame geometry.

## The Fix

### Wrong Pattern (causes bleed)
```python
# Cover and content use SAME frame geometry — draw_cover paints ALL pages
frame = Frame(ML, MB, CW, H, id='cover')  # same as content
cover_tmpl = PageTemplate(id='Cover', frames=[frame], onPage=draw_cover)
content_tmpl = PageTemplate(id='Regular', frames=[frame], onPage=draw_regular)
```

### Correct Pattern
```python
from reportlab.platypus import Frame, PageTemplate, NextPageTemplate

W, H = letter  # actual page dimensions

# Cover frame = FULL page (paints entire canvas)
cover_frame = Frame(0, 0, W, H, id='cover')

# Content frame = starts BELOW running header area (~16mm tall)
content_frame = Frame(ML, MB + 16*mm, CW, H - MB - 16*mm, id='regular')

# Each PageTemplate has its OWN frame covering only its target pages
cover_tmpl = PageTemplate(id='Cover', frames=[cover_frame])
regular_tmpl = PageTemplate(id='Regular', frames=[content_frame], onPage=draw_regular)
seal_tmpl = PageTemplate(id='Seal', frames=[Frame(0, 0, W, H, id='seal')])

doc.addPageTemplates([cover_tmpl, regular_tmpl, seal_tmpl])
```

### Switching Templates mid-story
```python
story = [
    SomeFlowable(),       # uses Cover template
    NextPageTemplate('Regular'),  # ← switch BEFORE next page
    MoreFlowables(),       # uses Regular template
    NextPageTemplate('Seal'),
    SealFlowable(),        # uses Seal template
]
```

## Running Header Pattern (only on non-cover pages)
```python
from reportlab.platypus import Frame
from reportlab.lib.units import mm

def draw_regular(canvas, doc):
    """Running header: thin gold top rule + SEARAH | MAY 2026 + page number"""
    canvas.saveState()
    canvas.setStrokeColor(gold)
    canvas.setLineWidth(0.5)
    canvas.line(ML, H - 10*mm, W - MR, H - 10*mm)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(navy)
    canvas.drawString(ML, H - 16*mm, "SEARAH  |  MAY 2026")
    canvas.drawRightString(W - MR, H - 16*mm, str(doc.page))
    canvas.restoreState()
```

## Key Insight
ReportLab's PageTemplate system uses frames as paint targets, not as passive clips. When a PageTemplate's `onPage` function runs, it paints directly on the canvas at whatever position the Frame occupies. If two templates share the same Frame geometry, visual elements bleed across pages.

**Rule** — Every distinct visual section (cover, content, seal) must have its own Frame covering exactly the area it should paint. Use `NextPageTemplate()` to switch between them.

## Verification
```python
import fitz
doc = fitz.open('output.pdf')
for i, page in enumerate(doc):
    print(f"Page {i+1}: {page.rect.width:.1f} x {page.rect.height:.1f} pt")
    paths = page.get_drawings()
    for p in paths:
        color = p.get('color')
        if color and color != (0,0,0):
            print(f"  Non-black fill: {color}")
```

## Related
- SEARAH PDF v15: `/root/AAA/SEARAH/generate_pdf_v15.py`
- SEARAH PDF v16 (FORGED_V5 journalism style): `/root/AAA/SEARAH/generate_pdf_v16.py`

---

# ReportLab Font Registration + FORGED_V5 Journalism Style

## Font Registration — Critical Gotchas

ReportLab's `pdfmetrics.registerFont(TTFont(...))` lets you register custom fonts, but the registered name must match EXACTLY what you pass to `setFont()` and `ParagraphStyle`. Common mistakes:

### Gotcha 1: `-Oblique` vs `-Italic` suffix
**Wrong:** `'LiberationSans-Oblique'` — ReportLab can't resolve this
**Right:** `'LiberationSans-Italic'`

When registering italic/bold variants, use the exact suffix ReportLab expects:
```python
font_paths = {
    'LiberationSans':             '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    'LiberationSans-Bold':        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    'LiberationSans-Italic':      '/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf',
    'LiberationSans-BoldItalic':  '/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf',
    'LiberationSerif':            '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
    'LiberationSerif-Bold':       '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf',
    'LiberationSerif-Italic':     '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf',
}
# Verify files exist before registering
import os
for name, path in font_paths.items():
    if not os.path.exists(path):
        print(f"MISSING: {name} at {path}")
```

To find available fonts on VPS:
```bash
fc-list | grep -i liberation | grep -i sans
# Output: /usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf: Liberation Sans:style=Regular
```

### Gotcha 2: Hyphenated font names in ParagraphStyle — ReportLab's parser chokes
If a `ParagraphStyle` has `fontName='SomeFont-Italic'` and the Paragraph contains markup text with inline tags, ReportLab's HTML parser tries to resolve `SomeFont-Italic` and may fail.

**Safe pattern:** Register the font with the exact name, then use it consistently. Don't mix `SomeFont-Italic` in a style AND pass inline `<i>` tags in the same Paragraph.

### Gotcha 3: Typo in setFont() — `'LiberurierSerif'`
This typo is easy to make (finger memory for 'LiberationSerif' slips). Use:
```python
c.setFont('LiberationSerif', 11)   # correct
# c.setFont('LiberurierSerif', 11)  # WRONG — silent KeyError at render time
```

## FORGED_V5 Professional Journalism Style — Complete Palette

When replicating FORGED_V5 investigative report aesthetic:

```python
from reportlab.lib.colors import HexColor, white, black

# FORGED_V5 exact palette
C_BLACK  = HexColor('#000000')   # primary text
C_111    = HexColor('#111111')   # dark headings, dark rule lines
C_1A1A   = HexColor('#1A1A1A')   # body text
C_222    = HexColor('#222222')   # secondary dividers
C_333    = HexColor('#333333')   # secondary body
C_555    = HexColor('#555555')   # subtitle gray
C_888    = HexColor('#888888')   # labels / metadata
C_999    = HexColor('#999999')   # footer / page numbers
C_CCC    = HexColor('#CCCCCC')   # light borders
C_DDD    = HexColor('#DDDDDD')   # table/border lines
C_F0F0   = HexColor('#F0F0F0')   # alternating table row
C_F8F8   = HexColor('#F8F8F8')   # table alt row 2
C_FAFA   = HexColor('#FAFAFA')   # timeline background
C_WHITE  = white                 # page background
C_RED    = HexColor('#CC0000')   # FORGED_V5 red accent — sparingly used
```

## FORGED_V5 Layout Geometry

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

W, H = A4   # 595 × 842 pts

# Margins (~90pts = ~3.2cm) matching FORGED_V5
ML = 90; MR = 90   # left/right
MB = 82             # bottom
MT = 60             # top
CW = W - ML - MR   # 415 pts content width

# Running header zone: ~43pts below top of page
# (gray line at y = H - 43, text at y = H - 36)
```

## FORGED_V5 Typography Scale

```python
BODY        = S('Body',   fontName='LiberationSerif', fontSize=11,  leading=15.5,
                alignment=TA_JUSTIFY, spaceAfter=6, textColor=C_1A1A)
COVER_TITLE = S('CT',     fontName='LiberationSerif-Bold', fontSize=32, leading=38,
                textColor=C_111)
COVER_SUB   = S('CSub',   fontName='LiberationSerif-Italic', fontSize=9.5, leading=13,
                textColor=C_555)
PART_LBL    = S('PLbl',   fontName='LiberationSans-Bold', fontSize=8, leading=10,
                textColor=C_RED)
SEC_LBL     = S('SLbl',   fontName='LiberationSans-Bold', fontSize=7.5, leading=10,
                textColor=C_888)
PULLQ       = S('PQ',     fontName='LiberationSerif-Italic', fontSize=12, leading=17,
                alignment=TA_CENTER, textColor=C_111, spaceBefore=10, spaceAfter=4)
PULLQA      = S('PQA',    fontName='LiberationSans', fontSize=8.5, leading=12,
                alignment=TA_CENTER, textColor=C_555)
HL_KEY      = S('HLK',    fontName='LiberationSans-Bold', fontSize=7.5, leading=10,
                textColor=C_888)
HL_VAL      = S('HLV',    fontName='DejaVuSans', fontSize=7.5, leading=10,
                textColor=C_111)
WIT_TXT     = S('Wit',    fontName='LiberationSans-Italic', fontSize=7, leading=10,
                textColor=C_888, alignment=TA_CENTER)
CORR_TXT    = S('Corr',   fontName='LiberationSans', fontSize=7.5, leading=11,
                textColor=C_RED)
```

## FORGED_V5 Key Flowable Patterns

### Drop cap on cover (canvas drawing)
```python
def draw_cover(canvas, doc):
    canvas.saveState()
    c = canvas
    # Drop cap "O" — 60pt bold
    c.setFont('LiberationSerif-Bold', 60)
    c.setFillColor(C_111)
    c.drawString(ML, H - 370, 'O')
    # Rest of first word inline
    c.setFont('LiberationSerif', 11)
    c.setFillColor(C_1A1A)
    c.drawString(ML + 37, H - 370, 'n the morning of November 3, 2025...')
    canvas.restoreState()
```

### Dark key fact box (#111 background, white text)
```python
def key_fact(label, value):
    data = [[
        Paragraph(label, S('KFL', fontName='LiberationSans-Bold', fontSize=7.5,
                            textColor=C_RED, leading=10)),
        Paragraph(value,  S('KFV', fontName='LiberationSans', fontSize=8.5,
                            textColor=C_WHITE, leading=12)),
    ]]
    t = Table(data, colWidths=[52*mm, CW - 52*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), C_111),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(0,-1),  6),
        ('RIGHTPADDING',  (0,0),(-1,-1), 6),
    ]))
    return t
```

### Timeline with alternating rows
```python
tl_data = [[Paragraph(date, S('TD', fontName='LiberationSans-Bold', fontSize=8,
                               textColor=C_RED, leading=11)),
            Paragraph(text, S('TT', fontName='LiberationSerif', fontSize=8.5,
                               textColor=C_333, leading=12))]
           for date, text in entries]
tl_table = Table(tl_data, colWidths=[28*mm, CW - 28*mm])
tl_table.setStyle(TableStyle([
    ('ROWBACKGROUNDS',  (0,0),(-1,-1), [C_WHITE, C_F0F0]),
    ('BACKGROUND',      (0,0),(-1,-1), C_FAFA),  # outer bg
    ('VALIGN',          (0,0),(-1,-1), 'TOP'),
    ('TOPPADDING',      (0,0),(-1,-1), 3),
    ('BOTTOMPADDING',   (0,0),(-1,-1), 3),
    ('LEFTPADDING',     (0,0),(-1,-1), 5),
    ('RIGHTPADDING',    (0,0),(-1,-1), 5),
    ('LINEBELOW',       (0,0),(-1,-2), 0.3, C_DDD),
]))
```

### Part title page with red left bar (canvas drawing)
```python
def draw_part(canvas, doc):
    canvas.saveState()
    # Red vertical bar — 3pt wide, full height, left edge
    canvas.setFillColor(C_RED)
    canvas.rect(0, 0, 3, H, fill=1, stroke=0)
    # Top thin gray line
    canvas.setStrokeColor(C_CCC)
    canvas.setLineWidth(0.75)
    canvas.line(0, H - 43, W, H - 43)
    # Header (date left, title right)
    canvas.setFont('DejaVuSans', 8)
    canvas.setFillColor(C_999)
    canvas.drawString(ML, H - 36, '5/6/26, 8:52 AM')
    canvas.drawRightString(ML + CW, H - 36, "Document Title Here")
    # Footer
    canvas.setStrokeColor(C_CCC)
    canvas.setLineWidth(0.5)
    canvas.line(ML, 28, ML + CW, 28)
    canvas.setFont('LiberationSans', 7.5)
    canvas.setFillColor(C_999)
    canvas.drawCentredString(W / 2, 17, f'{doc.page}  |  For Public Review  |  May 2026')
    canvas.restoreState()
```

### Questions table (red number | body)
```python
def question_row(num, text):
    data = [[
        Paragraph(num, S('QN', fontName='LiberationSans-Bold', fontSize=11,
                          textColor=C_RED, leading=14)),
        Paragraph(text, S('QB', fontName='LiberationSerif', fontSize=11,
                          textColor=C_1A1A, leading=15.5)),
    ]]
    t = Table(data, colWidths=[12*mm, CW - 12*mm])
    t.setStyle(TableStyle([
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),(-1,-1), 2),
        ('BOTTOMPADDING', (0,0),(-1,-1), 2),
        ('LEFTPADDING',   (0,0),(0,-1),  0),
        ('RIGHTPADDING',  (0,0),(-1,-1), 0),
    ]))
    return t
```

## Workflow for Matching a Reference PDF Style

1. **Analyze reference** — Use subagent with terminal + fitz to extract all pages as PNG, then `mmx vision describe` each page for full text/structure analysis
2. **Catalog style** — Extract: palette (hex codes), fonts (names + sizes), margins, header/footer format, section structure, unique visual elements
3. **Register fonts** — Verify actual font files exist with `fc-list`, register with `TTFont`, use exact registered names
4. **Build generator** — Start with cover page drawing function, then regular pages, then special sections (part titles, quotes, seal)
5. **Test and iterate** — Generate → render with fitz → `mmx vision describe` → fix → repeat
6. **Verify** — Check all pages for: correct fonts, colors matching palette, no bleed from other templates, correct content per page

## Common Font Name Typos to Avoid

| Wrong | Right |
|-------|-------|
| `LiberurierSerif` | `LiberationSerif` |
| `LiberationSans-Oblique` | `LiberationSans-Italic` |
| `Helvetica-Oblique` | Use DejaVuSans or register Helvetica Italic |
