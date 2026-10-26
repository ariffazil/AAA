---
name: business-letter-pdf
description: Rebuild formal letters as A4 PDF from a photo.
version: 1.0.0
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Business Letter PDF (rebuild from photo)

The user sends a photo of a signed letter and asks to re-date it, add a paragraph, or attach an appendix. You rebuild the document as a clean A4 PDF - you never edit the photo's pixels.

## Procedure

1. **Transcribe first, fully.** `vision_analyze` the image and ask for ALL text verbatim: letterhead, addressee block, date, salutation, subject line, every numbered paragraph and sub-item. Do both pages before writing any HTML.
2. **Reconstruct in HTML.** One file in `/tmp/`, A4 `@page` block, weasyprint render:
   ```bash
   weasyprint letter.html out.pdf
   ```
3. **Extract the signature** from the original photo (see below) and place it above the printed name.
4. **Verify** with `pdftoppm -r 90 out.pdf pg -png`, then `vision_analyze` each page. Confirm the changed date, the new paragraph, the signature, and that nothing is cut off.
5. Deliver with `MEDIA:/abs/path.pdf`.

## Page setup

```css
@page { size: A4; margin: 18mm 20mm 18mm 22mm;
  @bottom-center { content: counter(page) " / " counter(pages); font-size: 8pt; color: #999; } }
body { font-family: Arial, Helvetica, sans-serif; font-size: 10.5pt; line-height: 1.55; }
```

Malay formal-letter conventions that must be preserved:

- Letterhead left (company name / logo), contact block right, black rule underneath.
- Addressee block **uppercase**, bold, four lines: name, position, institution, ministry.
- Date on its own line, right-aligned, uppercase month (`20 OCT 2026`).
- Numbered paragraphs use a hanging indent so the text aligns after `1.`:
  `padding-left: 24px; text-indent: -24px;` with the marker in `<span class="marker">1.</span>` at `width: 24px`.
- Sub-items `a) b) c)` indent one level further under the parent paragraph, same hanging indent.
- Closing: `Sekian, terima kasih.` then `Yang benar,` then signature then bold name then position.

## Signature extraction (the part that usually looks wrong)

Crop the sign region from the original photo, then build an RGBA image where alpha is darkness - do NOT threshold to pure black and white, that leaves ragged edges:

```python
from PIL import Image
import numpy as np
a = np.array(Image.open(src).convert('L').crop((x1, y1, x2, y2)))
alpha = np.clip((235 - a.astype(np.int16)) * (255.0 / 235.0), 0, 255).astype(np.uint8)
rgba = np.dstack([np.zeros((*a.shape, 3), np.uint8), alpha])
Image.fromarray(rgba, 'RGBA').save('sig_trans.png')
```

Then embed at `width: 150-160px` with a small negative left margin so it sits where a pen would. Verify by compositing over white first - a transparent PNG viewed directly in an image tool looks like a black box and will mislead you.

Crop tightly enough to exclude `Yang benar,` above and the printed name below; the printed name stays as HTML text.

## Traps

- **Vision output redacts email addresses** as `[REDACTED:EMAIL]`. Never invent one on an official letter. Omit the email line and tell the user it is missing and why.
- **Do not retype what you cannot read.** If a line is illegible, say which line.
- If asked for an appendix, use a page break, a `LAMPIRAN n` title, the image at `max-height: 205mm; width: auto`, a thin border, and an italic caption. Verify the photo is not cropped and fits inside the margins.
- Re-render after every content change and re-check the changed paragraph by name; a paragraph inserted mid-list can shift pagination and orphan the signature block.
