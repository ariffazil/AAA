---
name: image-text-extraction
description: "Use when reading text off an image fails or is unreliable."
version: 1.0.0
tags: [ocr, vision, tesseract, documents, images, fallback]
---

# Image Text Extraction

Getting text and numbers out of a photograph of a document, receipt, form, label or screenshot —
especially when the vision lane is dark, rate-limited, or only a weak local fallback is available.
Also the class for any read where an invented value would be worse than no value (medical,
financial, safety).

## Procedure

1. **Printed text → OCR first, not vision.** `tesseract` is usually already present at `/usr/bin/tesseract`.
   Check once what it can read: `tesseract --list-langs`. Preprocessing is what makes phone photos
   readable — grayscale, LANCZOS upscale 2–4×, then autocontrast. Raw `tesseract IMAGE` on an
   unprocessed phone photo frequently returns nothing at all.

   ```bash
   python3 -c "
   from PIL import Image, ImageOps
   im = Image.open('PHOTO.jpg').convert('L')
   im = im.resize((im.width*3, im.height*3), Image.LANCZOS)
   ImageOps.autocontrast(im).save('/tmp/ocr.png')"
   tesseract /tmp/ocr.png - -l eng --psm 6
   ```

2. **Whole image once, then crop and re-read the tail.** On a long single-image report the first pass
   routinely loses the bottom sections (serology blocks, urine, ratios). Re-crop to the bottom ~45% at
   scale 4 and read again:

   ```bash
   python3 -c "
   from PIL import Image, ImageOps
   im = Image.open('PHOTO.jpg').convert('L'); W,H = im.size
   c = im.crop((0,int(H*0.55),W,H))
   c = c.resize((c.width*4, c.height*4), Image.LANCZOS)
   ImageOps.autocontrast(c).save('/tmp/ocr_bot.png')"
   tesseract /tmp/ocr_bot.png - -l eng --psm 6
   ```

3. **Grep for the sections that matter instead of re-reading by eye:**

   ```bash
   tesseract /tmp/ocr.png - -l eng --psm 6 | grep -i -E "hiv|hepat|vdrl|serolog|antibod|acr|hba1c"
   ```

4. **Take numbers only from a source that can actually read numbers.** If OCR produced the value it is
   OBSERVED. If only a weak fallback model produced it, it is UNKNOWN — say so.

5. **Handwritten documents → ask the sender to type the lines.** OCR returns empty or garbage on
   handwriting and no local model reads it. One line: "tulisan tangan, mesin tak boleh baca — type je".
   Never guess figures from a handwriting photo. Then, when they type it, produce the output they asked for
   rather than answering with another clarifying question.

## Pitfalls

- **A weak local fallback vision model fabricates readings.** Measured case: asked about a dashboard
  photo it invented a speed value *and* invented the shape and colour of each warning light. Never relay a
  fallback model's numbers, gauge values, or symbol identifications. Fabricating a clinical number or a
  warning light is worse than returning UNKNOWN.
- **PSM choice matters more than resolution for sparse text.** Scattered labels, a dashboard cluster, or
  one line in a large image read better with `--psm 11`; a document body reads better with `--psm 6`.
  When one returns noise, try the other before blaming the image.
- **A "cannot read it" verdict needs every rung tested.** An auth failure on the primary lane and a quota
  failure on the secondary are different problems with different remedies, and a local fallback is a third
  rung. Test them before telling the user a document is unreadable — and when the last rung is a weak
  model, prefer OCR over trusting it.
- **Do not let a failed read become a dead end.** Extract what is legible, state which fields are UNKNOWN,
  and ask only for the fields that actually change the answer.
- **Never narrate the plumbing to the user.** Name the field you could not read, not the lane, tool or
  provider that failed.

## Related

- `medical-document-interpretation` (external) — interpretation and Malaysian lab cutoffs, once the text is out.
- `ocr-and-documents` — PDF and scan parsing with Python libraries, when the input is a file rather than a photo.
