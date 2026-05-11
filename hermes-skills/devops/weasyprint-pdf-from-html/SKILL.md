---
name: weasyprint-pdf-from-html
description: Generate polished PDFs from HTML using WeasyPrint — certificates, reports, documents. Covers CSS gotchas, font loading, A4 layout, and the full HTML→PDF pipeline for arifOS artifact generation.
triggers: ["generate pdf", "weasyprint", "certificate pdf", "html to pdf", "create pdf artifact"]
tags: [pdf, weasyprint, html, css, document-generation, artifact]
---

# WeasyPrint PDF Generation Skill

Generate beautiful PDFs from HTML using WeasyPrint. Used for arifOS certificates, reports, and document artifacts.

## Prerequisites

WeasyPrint must be installed:
```bash
which weasyprint  # confirm available
```

If missing: `pip install weasyprint` or `uv pip install weasyprint`

## Basic Pipeline

1. Write HTML with inline CSS (or `<style>` block)
2. Save as `.html` file
3. Run: `weasyprint input.html output.pdf`
4. Verify: `ls -lh output.pdf`

## Critical CSS Gotchas

### `inset` is NOT supported
WeasyPrint does NOT support the CSS `inset` shorthand property. Always expand to individual sides:

```css
/* WRONG — will be silently ignored */
position: absolute;
inset: 12mm;

/* CORRECT */
position: absolute;
top: 12mm; right: 12mm; bottom: 12mm; left: 12mm;
```

This applies to ALL `inset` values throughout the CSS (e.g., `inset: 4px`, `inset: 3px`).

### `@import must be first`
Google Fonts `@import` must appear before ALL other CSS rules, including `* { box-sizing: border-box; margin: 0; padding: 0; }`.

```css
/* ✅ CORRECT ORDER */
@import url('https://fonts.googleapis.com/css2?family=...');

* { box-sizing: border-box; margin: 0; padding: 0; }
:root { ... }

/* ❌ WRONG — @import after reset rules is ignored */
* { box-sizing: border-box; margin: 0; padding: 0; }
@import url('https://fonts.googleapis.com/css2?family=...');
:root { ... }
```

Workaround if you must: put fonts in `<link>` tags in the HTML `<head>` instead of `@import` in CSS.

## A4 Certificate Layout (reference)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Font1&family=Font2&display=swap');

  :root {
    --gold: #c9a84c;
    --deep: #111827;
    --cream: #f5f0e8;
  }

  @page {
    size: A4;
    margin: 0;
  }

  body {
    font-family: 'DM Sans', sans-serif;
    width: 210mm;
    min-height: 297mm;
    background: #faf8f5;
    position: relative;
  }

  /* Border — use top/right/bottom/left, NOT inset */
  .border {
    position: absolute;
    top: 12mm; right: 12mm; bottom: 12mm; left: 12mm;
    border: 1.5px solid var(--gold);
  }

  /* Inner double border */
  .border::before {
    content: '';
    position: absolute;
    top: 4px; right: 4px; bottom: 4px; left: 4px;
    border: 0.5px solid rgba(201,168,76,0.4);
  }
</style>
</head>
<body>
<!-- content -->
</body>
</html>
```

## When WeasyPrint Fails for Complex Layouts

WeasyPrint crashes or renders incorrectly for complex CSS. Known failures:

### `display: grid` → AssertionError `float_layout`
```
File "weasyprint/layout/float.py", line 79, in float_layout
    assert isinstance(box, boxes.BlockReplacedBox)
AssertionError
```
Fix: Use `display: block` instead of `display: grid`.

### `display: flex` with `justify-content` → crashes
Fix: Avoid flexbox for multi-column layouts in WeasyPrint. Use ReportLab instead.

### `@page :first` → crashes
Fix: Remove `:first` pseudo-class. Use plain `@page { margin: 0; }` for cover pages.

**When to skip WeasyPrint entirely and use ReportLab instead:**
- Document has complex multi-column layouts
- Pixel-perfect text positioning required
- Document is legally sensitive (text layer must be clean, not overlaid)
- WeasyPrint crashes on your CSS despite being spec-compliant

## ReportLab Alternative (for legally-sensitive documents)

When WeasyPrint can't handle the layout, use ReportLab directly:

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
import hashlib, hmac

W, H = A4  # 595.28pt × 841.89pt

# Page template with header/footer
def on_page(canvas_obj, doc):
    if doc.page == 1:  # skip cover
        return
    canvas_obj.setFont('Helvetica', 6)
    canvas_obj.setFillColor(HexColor('#888888'))
    canvas_obj.drawString(18*mm, 8*mm, 'Document Title')
    canvas_obj.drawRightString(W - 18*mm, 8*mm, str(doc.page))

# Styles
def S(name, **kw):
    return ParagraphStyle(name, **kw)

BODY = S('Body', fontName='Helvetica', fontSize=9.5,
          leading=15, alignment=TA_JUSTIFY)

# Build
story = []
story.append(MyCoverPage())  # custom Flowable
story.append(PageBreak())
story.append(Paragraph("Text content here...", BODY))

doc = SimpleDocTemplate('output.pdf', pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm,
    topMargin=16*mm, bottomMargin=16*mm)
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
```

Note: ReportLab Canvas does NOT have `setCharSpace()`. Use plain `drawString()` with manual letter spacing via font metrics if needed.

## Common Properties Supported

| Property | Support | Notes |
|----------|---------|-------|
| `position: absolute/relative` | ✅ Full | |
| `top/right/bottom/left` | ✅ Full | NOT `inset` |
| `border-radius` | ✅ Full | |
| `box-shadow` | ✅ Full | |
| `linear-gradient` | ✅ Full | |
| `CSS Grid / Flexbox` | ✅ Full | |
| `@import url()` | ✅ | Must be first rule |
| Google Fonts `<link>` | ✅ | In `<head>`, more reliable |
| CSS Variables | ✅ Full | |
| `mm/cm/px` units | ✅ Full | |
| `border-image` | ❌ Ignored | |
| `backdrop-filter` | ❌ Ignored | |
| `float` | ⚠️ Limited | Prefer flexbox |
| `column-count` | ❌ May fail | |

## Workflow for arifOS Artifact Certificates

1. Design HTML with inline CSS (no external stylesheet needed)
2. Use gold/navy/cream palette for formal certificates
3. Test with: `weasyprint input.html output.pdf`
4. Check stderr for CSS warnings (ignored properties)
5. Verify: `ls -lh output.pdf` (should be 20-100KB)
6. Deliver via Telegram with MEDIA: path

## Critical: Patching Existing PDFs vs Regenerating

If you need to CORRECT facts in an existing PDF (e.g., fixing a legal document with wrong claims):

**Image overlay approach (PIL/fitz rendering):** Visually replaces text but the PDF TEXT LAYER still contains the old wrong text. Anyone running `pdftotext` or `pdfgrep` will find the original incorrect claim. **Not safe for legal/judicial documents.**

**Correct approach:** Regenerate the entire PDF from source content. Treat the source Markdown/HTML as the canonical document, not the PDF.

This matters when:
- Document will be reviewed by lawyers (they will grep/text-search)
- Claims need to be retracted and corrected publicly
- Document has a cryptographic seal/commitment (text layer must match visual layer)

## Troubleshooting

### "Font not loading"
- Use `<link>` in `<head>` instead of `@import` in CSS
- WeasyPrint fetches fonts over network — ensure internet access in container
- Fallback: use system fonts (Arial, Georgia) if network unavailable

### "Colors look wrong"
- WeasyPrint uses RGB, not CMYK. Print shops need CMYK conversion.
- Use hex or rgb() values, not named colors for best accuracy.

### "Page breaks look wrong"
- Use CSS `break-before: page;` or `break-after: page;` for multi-page docs
- Single-page certs don't need this

### "weasyprint command not found"
```bash
pip install weasyprint --break-system-packages
# or
uv pip install weasyprint
```
