---
name: formal-document-rebuild
description: Rebuild a formal A4 document from a photo or prior PDF.
version: 1.0.0
author: hermes
---

# Formal Document Rebuild (A4, client-facing)

Use when an existing business document must be reissued: a letter photographed on paper, a company
profile PDF that needs translating, an invoice re-skinned for a new client, or any request of the
shape "change the date / add a clause / add an appendix / translate this / use this picture
instead". The deliverable is a clean A4 PDF that regenerates from source, never a patched image.

Source of truth is a directory of artifacts; the render is disposable. Keep the HTML beside the PDF
so the next edit is a one-line change and a re-render, not a fresh transcription.

## Procedure

1. **Extract the source text before touching layout.** `pdftotext -layout in.pdf -` for a PDF; for a
   photo, read it with the vision tool and transcribe structure (headings, numbered paragraphs,
   sub-items a) b) c), signature block) — not just words. Note the letterhead fields: company name,
   registration number, phone, address.
2. **Pull embedded images from the source PDF** with `pdfimages -png in.pdf outdir/img`. This is what
   gives you the logo and any appendix photos at full native resolution instead of a screenshot.
3. **Rebuild in HTML + CSS, render with weasyprint.** `weasyprint doc.html out.pdf`. A4 via
   `@page { size: A4; margin: ~18-20mm }`. Body font Arial/Helvetica 10.5pt, `line-height: 1.48`.
   Chrome headless is for screen mockups; weasyprint is for paginated A4 documents.
4. **Re-read the render, per page.** `pdfinfo out.pdf | grep Pages`, then
   `pdftotext -f N -l N -layout out.pdf -` for each page, then one vision read on every page you
   touched. A page-count change means content reflowed; find what moved before delivering.
5. **Deliver** with `MEDIA:/abs/path`, and state in one line what changed vs the previous version.

## Numbered paragraphs need hanging indents

`<ol>` with the default markers, or markers typed inside the text, produce collisions: `1.Saya
Izzuddin…` runs the numeral into the first word. Correct form — remove the list marker and give the
marker its own fixed-width span:

```css
ol.paras > li { padding-left: 24px; text-indent: -24px; text-align: justify; }
ol.paras > li .marker { display: inline-block; width: 24px; text-indent: 0; }
ol.subs { padding-left: 34px; }   /* one level deeper than the parent */
```

```html
<li><span class="marker">1.</span>Saya Izzuddin Tajuddin daripada …</li>
<li><span class="marker">e.</span>Produk makanan dan minuman …</li>
```

Malay letters keep the numeral with a full stop (`1.`, not `1)`); sub-items take a closing bracket
(`a)`). The user's existing document is the authority on this — copy its convention exactly.

## Signatures: extract from the source, never redraw

A reissued letter keeps the real signature. Extract it as a transparent PNG from the source scan:

```python
from PIL import Image
import numpy as np
im = Image.open(src).convert('L')          # crop tightly around the ink first
crop = im.crop((x0, y0, x1, y1))
a = np.array(crop)
alpha = np.clip((235 - a.astype(np.int16)) * (255.0 / 235.0), 0, 255).astype(np.uint8)
rgb = np.zeros((*a.shape, 3), dtype=np.uint8)
Image.fromarray(np.dstack([rgb, alpha]), 'RGBA').save('sig.png')
```

Verify before embedding: composite the RGBA over white (`Image.alpha_composite`) and look at the
result — a hard luminance threshold (`np.where(a < 150, 0, 255)`) leaves a ragged black outline and
greys the paper edge, while the alpha ramp keeps strokes sharp on any background. The crop must
contain ink only; if printed text bleeds into the frame, move the top edge down and re-crop. Embed at
~150-160px (`~40mm`) between the closing line (`Yang benar,`) and the printed name, with a small
negative left margin so it aligns with the name block.

## Appendices

Page-break before the appendix, then a `LAMPIRAN N` heading, a one-line subtitle, the figure, and an
italic 9pt caption. Size the figure by **height in mm**, not `width: 100%` — a full-width portrait
photo overflows the page box and pushes the caption to the next page:

```css
.appendix-figure img { height: 190mm; width: auto; max-width: 100%; border: 1px solid #ddd; }
```

When the caption is edited, re-check the page count: a longer caption that no longer fits is the most
common cause of an unplanned extra page.

## Translating a document, not a paragraph

Translate the content and keep the layout: section numbering, sub-item letters, table columns, and
page order survive translation unchanged. Company names, registration numbers, addresses, phone
numbers, and personal names stay verbatim — never translated, never reformatted. Technical terms take
the industry-standard local form rather than a literal gloss (vending machine → *mesin vending*,
cashless → *tanpa tunai*, eWallet → *e-dompet*, tempered glass → *kaca tempered*, stock
replenishment → *penambahan semula stok*). After rendering, grep the PDF for English leakage
(`pdftotext … | grep -iE '\b(the|and|with|for)\b'`) instead of assuming the translation was
complete.

## Page layout QA (any rendered page)

- **Detect text collisions deterministically:** `pdftotext -layout` concatenates overlapping strings
  onto one line (`Total471`, `Transactions RM2228.00`). Sub-second probe; page count and file size
  cannot see this.
- **A clean text extract is not proof the page is clean** — boxes can overlap while text extracts
  perfectly. Pair the text probe with one vision read asking a *layout* question about the elements
  you changed ("does the footer overlap the last row of cells? are all group labels visible?").
- **When the human says a page is wrong without naming the fault, render it and probe it yourself.**
  Never ask them to describe the defect, and never ship another render before inspecting the previous
  one.
- **A grouped grid belongs in one coordinate system.** Cards drawn as separate axes/panels collide by
  construction, nothing in the code reports it, and each "fix" adds another layer (label band, group
  border, tile border) that becomes a new defect. After the *second* patch to the same layout fault,
  rewrite the page as a flat cell grid: `row_h = 1/n_rows`, `col_w = 1/n_cols`, every cell an explicit
  rectangle at `(col*col_w, y)`. Reserve the outer band — start content below `y=0.90`, end above
  `y=0.08` on a `suptitle(y=0.97)` page, or the title and footer both collide.

## Honesty rules

- **A pipeline that redacts emails/phones from images cannot be worked around by guessing.** If the
  address is unreadable, leave the field out, tell the user which field is missing, and offer to
  re-render the moment they supply it. Never fabricate a company email on a document that will be
  signed and sent.
- **Never carry an old date silently.** When the request is "change the date", change it and say so
  explicitly; a stale date on a reissued letter is a legal problem, not a cosmetic one.
- **Report what changed, one line per change,** with the numbers that moved (page count, total, GP).
  Do not describe the document back to the person who wrote it.

## Related

`wop-invoice-generator` covers the invoice variant of this workflow (single-page A4, `YYYYMMDD-NNN`
invoice numbers, payment schedule table). Reuse its layout when the deliverable is an invoice; this
skill's signature, appendix, and translation sections are the ones that apply to letters and profiles.
