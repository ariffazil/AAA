# PDF Book Pipeline — reportlab parameters and SVG cover recipe

Concrete reference for rendering a Walter Isaacson-style biography PDF with proper book layout using reportlab.

## Margins (hardcover-style paperback)

```python
LEFT_MARGIN = 2.8*cm    # binding edge
RIGHT_MARGIN = 2.2*cm
TOP_MARGIN = 3*cm
BOTTOM_MARGIN = 2.8*cm
```

Asymmetry between left and right is intentional: the binding edge needs more room. Do not set equal margins — it looks like a report, not a book.

## Body type

| Element | Font | Size | Leading | Color | Alignment | First-line indent |
|---------|------|------|---------|-------|-----------|-------------------|
| Body prose | Times-Roman | 11 | 17 | #222222 | justify | 18 |
| Chapter title | Times-Roman | 20 | 26 | #1a1a1a | left | 0 |
| Chapter subtitle (date stamp) | Times-Italic | 11 | 14 | #666666 | left | 0 |
| Source citation | Times-Itic | 9 | 12 | #888888 | left | 0 |
| Epilogue prose | Times-Italic | 11 | 16 | #333333 | justify | 14 |
| Author note (— aku —) | Times-Italic | 11 | 16 | #666666 | left | 0 |

Use `keepWithNext=1` on chapter title and source citation so they stay with the first body paragraph. Otherwise the chapter title floats to the bottom of one page and the body opens at the top of the next.

## Page numbering

```python
def on_page(canvas_obj, doc_obj):
    canvas_obj.saveState()
    canvas_obj.setFont("Times-Italic", 9)
    canvas_obj.setFillColor(colors.HexColor("#888888"))
    canvas_obj.drawCentredString(width/2.0, 1.5*cm, f"—  {doc_obj.page}  —")
    canvas_obj.restoreState()

doc.build(flow, onFirstPage=on_page, onLaterPages=on_page)
```

The cover page is page 1 but should have no visible page number. `onFirstPage=on_page` will paint the footer on page 1 too — that is fine if the cover is a full-bleed image (the footer gets painted underneath). If the cover is text-only (no image), use `onFirstPage=lambda c, d: None` to suppress the footer on the cover only.

## Cover image insertion

```python
from reportlab.platypus import Image as RLImage

img = RLImage("/tmp/cover.png", width=15*cm, height=20*cm)
img.hAlign = 'CENTER'
flow.append(Spacer(1, 1*cm))
flow.append(img)
```

Image must be PNG or JPEG. SVG must be converted first (see SVG recipe below).

## Title page typography

The title page goes after the cover (separated by PageBreak). Center vertically with generous space at the top:

```python
flow.append(Spacer(1, 4*cm))
flow.append(Paragraph("ALPHA &amp; ZEN", title_main_style))
flow.append(Spacer(1, 0.3*cm))
flow.append(Paragraph("&amp;", ampersand_style))
flow.append(Spacer(1, 0.3*cm))
flow.append(Paragraph("ZEN", title_main_style))
flow.append(Spacer(1, 1*cm))
flow.append(Paragraph("A Biography of Two Men", subtitle_style))
flow.append(Paragraph("and the Federation of Agents", subtitle_style))
flow.append(Spacer(1, 4*cm))
# Dedication, author, location — centered, italic
```

## SVG cover recipe (programmatic line art, two silhouettes)

The default cover for biographies of living subjects. No faces, KL skyline silhouette, two figures (one slimmer in front, one broader behind).

```python
svg_cover = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 800" width="600" height="800">
  <defs>
    <linearGradient id="sky" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0a3d4d"/>
      <stop offset="60%" stop-color="#1a5b6e"/>
      <stop offset="100%" stop-color="#c08b3c"/>
    </linearGradient>
  </defs>
  <rect width="600" height="600" fill="url(#sky)"/>
  <rect y="600" width="600" height="200" fill="url(#ground)"/>
  <!-- KL skyline silhouettes, sun glow, two figures, title typography -->
</svg>'''
```

Convert to PNG via rsvg-convert:

```bash
rsvg-convert -w 1500 -h 2000 /tmp/cover.svg -o /tmp/cover.png
```

Use 1500x2000 minimum — that's enough for ~5 inch cover at 300 DPI. Below 1200x1600 the cover will be visibly soft on print.

## Naming convention

```
/root/.hermes/cache/documents/doc_biography_<TITLE>.pdf
```

`<TITLE>` is the book's title (one or two words), not the subject's name. Examples:
- `doc_biography_ALPHA_ZEN.pdf`
- `doc_biography_STEVE.pdf`

Not:
- `doc_biography_arif_syed.pdf` (leaks subject names into filename)
- `doc_biography_FINAL_v3_REVISED.pdf` (version-named, breaks the one-PDF contract)

## Iteration rule (single PDF in documents/)

When the principal asks for an iteration:

```bash
ls /root/.hermes/cache/documents/doc_biography_*.pdf
# If a previous version exists, rm it before writing the new one
```

The intermediate `.md` files in `/tmp/` accumulate (they are not surfaced). The PDF does not. One PDF per biography, named by content.

## Verification before delivery

```bash
file /root/.hermes/cache/documents/doc_biography_<TITLE>.pdf
```

Must report `PDF document, version 1.7+`. A text file with `.pdf` extension is the most common defect and the most embarrassing — verify before announcing the deliverable.

## Common mistakes

- **Bullets in body.** Walter Isaacson biography is prose paragraphs. Bullets go in TOC, chapter lists, or metadata — never in body.
- **Equal margins (2.5cm all sides).** Looks like a report. Use 2.8/2.2/3/2.8.
- **Page number on cover.** Use `onFirstPage=lambda c, d: None` to suppress.
- **Forgetting `keepWithNext` on chapter title.** Causes title to float to bottom of one page while body opens at top of next.
- **Not converting SVG to PNG.** reportlab does not read SVG; must convert via rsvg-convert or cairosvg.
- **Saving intermediate PDFs as `FINAL_v2` etc.** The principal does not want a graveyard of versions. One PDF, named by content.
- **HTML instead of reportlab.** reportlab is the right tool for prose — weasyprint is for documents with charts and complex layout. For a prose biography, reportlab's `Paragraph` flowables give cleaner justification and better hyphenation.