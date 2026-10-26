---
name: business-document-production
description: Use when producing a letter, profile or document PDF.
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Business Document Production

Produce print-quality business documents — official letters, company profiles, appendices, screen mockups — from a photo/PDF of an existing document, from dictated content, or from scratch, in BM or English.

## When to load

- User sends a photo/PDF of a letter and asks to amend it (new date, extra clause, extra page)
- User asks to translate a company profile or corporate document
- User asks for an appendix, a cover page, or a "proper" version of a document
- User asks for a mobile-app / UI mockup image

## Golden rule: rebuild, never retouch

You cannot edit pixels. Never claim to "add a line" to an image. Extract the text and assets, rebuild the page as HTML at true A4, re-render. The only thing carried over as an image is artwork you cannot retype: logos, signatures, product photos.

This produces a clean vector PDF instead of a patched photo, and lets every later amendment be a one-line edit.

## Procedure

1. **Extract the source.** `pdftotext -layout file.pdf out.txt` for text-PDFs. For photos, `vision_analyze` the image and transcribe verbatim — numbers, addresses, registration numbers, and sub-item letters included.
2. **Harvest the artwork.** `pdfimages -png file.pdf ./img/img` pulls the embedded logo, cover render, and photos as lossless PNGs. For a photo-only source, crop from the image.
3. **Extract the signature** (see below) if the document is signed.
4. **Build the HTML** — A4 page CSS, real margins, `page-break-before: always` for deliberate page starts. Do not rely on natural flow to land page breaks where the original had them; the page count should match the original unless the user asked for more.
5. **Render** with `weasyprint in.html out.pdf`.
6. **Verify every page**, then deliver.

## Signature extraction

Handwritten signature on white paper → transparent PNG with an **alpha ramp**, not a hard threshold:

```python
from PIL import Image
import numpy as np
a = np.array(Image.open(src).convert('L').crop((x1, y1, x2, y2)))
alpha = np.clip((235 - a.astype(np.int16)) * (255.0 / 235.0), 0, 255).astype(np.uint8)
rgb = np.zeros((*a.shape, 3), dtype=np.uint8)
Image.fromarray(np.dstack([rgb, alpha]), 'RGBA').save('sig.png')
```

Hard `a < 150` thresholding produces ragged edges and a visible box on the rendered page. The ramp keeps anti-aliased strokes. Crop **above** the typed name line so no printed text lands inside the crop, then place it in the sign block with a small negative left margin so it sits over the closing line.

## Amendments the user actually asks for

- **Add a sub-item to a numbered list.** Insert at the correct letter position and keep the rest untouched. Do not renumber paragraphs.
- **Change the date.** Change only the date block. Do not silently change other dates in the body.
- **Append an appendix.** New page, `LAMPIRAN 1`-style heading, subtitle, image, italic caption. Size the image with a fixed `height:` and `width: auto` so it is never squashed.
- **Extend a caption.** Append to the existing sentence; do not rewrite the caption's existing clauses.
- **Translate.** Translate prose, keep proper nouns, company names, registration numbers, phone numbers, product names, and legal references in their original form.

## Verification loop (do not skip)

`weasyprint` failing silently is invisible in the text layer. Render and look:

```bash
weasyprint in.html out.pdf && pdfinfo out.pdf | grep Pages
pdftoppm -r 90 out.pdf pg -png          # then vision_analyze each pg-N.png
```

Check per page: title not colliding with the first content row, nothing running off the bottom edge, tables not split mid-row, images undistorted.

**Images are the usual cause of a wrong page count.** An oversized inline image pushes a section onto a new page and the document grows. If the page count exceeds the original, constrain the image `height:` in mm and re-render before touching anything else. Because weasyprint reflows, a section landing at the top of a page looks correct in text extraction while looking broken on the page — always check the raster.

## Redacted content

Cached images and some PDFs come back with emails replaced by `[REDACTED:EMAIL]`. **Never invent the address to fill the gap.** Either ask for it, or omit the line and tell the user it is missing. A fabricated email on an official letter is worse than a missing one.

Tesseract (`tesseract img.png stdout`) reads letterheads and short contact blocks more reliably than a vision model, because it does not paraphrase. Use it for the letterhead before transcribing body text with vision.

## Voice and language

- Match the document's existing language. A BM letter stays BM; do not switch register mid-document.
- Formal BM business register: `Dengan segala hormatnya`, `Sehubungan itu`, `Sekian, terima kasih`, `Yang benar`. Keep it — do not modernise.
- Translate terms by industry convention, not literally. See `references/bm-corporate-glossary.md`.
- Keep the sender's structure: numbered paragraphs, alpha sub-items `a) b) c)`, addressee block in capitals, date right-aligned.

## Screen mockups

Same pipeline, different frame: author an HTML phone frame (~390px wide, rounded corners, status bar with time and battery), then

```bash
google-chrome --headless=new --disable-gpu --no-sandbox --screenshot=out.png \
  --window-size=430,900 --hide-scrollbars file:///abs/path.html
```

Use a **snapshot** for a live-status screen (one date, one time, one reading) and a **range plus min/max/average** for a history/report screen. Never mix them: one reading presented beside a "period" implies the value held for the whole period.

Do not present a "safe operating range" band next to a single reading — a healthy asset holds its **set point**, flat. A band implies drift. If the user asks for a flat line at a set point, draw a horizontal line with the set point as the label and drop any "no fluctuation" reassurance sentence; the flat line already says it.

## Delivery

- One PDF (or PNG) via `MEDIA:/absolute/path`, not a menu of files
- State what changed in 2–4 lines; list outstanding gaps (missing email, unverified figure) explicitly
- Do not paste the document body back into chat
