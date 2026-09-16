# Poster Text Overlay — PIL Pipeline (proven 2026-08-28)

For motivation posters, generate the base image first (no text in prompt), then layer BM/EN quote overlay via PIL. The model almost always renders cleaner without in-prompt text overlay requests.

## When to use

- Quote-driven motivation poster (BM + EN subtitle)
- Brand watermark + attribution required
- Need pixel-perfect text placement (model text is unreliable)

## Standard pattern

```python
from PIL import Image, ImageDraw, ImageFont

base = Image.open('image.jpg').convert('RGB')
w, h = base.size

# 1. Top vignette for text contrast (covers top 35-42%)
overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
for y in range(int(h * 0.42)):
    alpha = int(210 * (1 - y / (h * 0.42)))
    draw.rectangle([(0, y), (w, y+1)], fill=(0, 0, 0, alpha))
base = base.convert('RGBA')
base = Image.alpha_composite(base, overlay)

# 2. Load font (DejaVu/Liberation/Noto — DejaVu Sans Bold safe default)
font_main = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', int(w * 0.043))
font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', int(w * 0.022))

# 3. Centered text with shadow for readability
draw2 = ImageDraw.Draw(base)
def draw_centered(text, font, y, fill=(255, 255, 255, 255), shadow=(0, 0, 0, 255)):
    bbox = draw2.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (w - tw) // 2
    draw2.text((x+2, y+2), text, font=font, fill=shadow)
    draw2.text((x, y), text, font=font, fill=fill)

# 4. Layout: 2-3 main lines + 1-2 EN subtitle + watermark + attribution
draw_centered("LINE 1", font_main, int(h * 0.04), fill=(255, 245, 230, 255))
draw_centered("LINE 2", font_main, int(h * 0.04) + int(w * 0.060), fill=(255, 220, 160, 255))
draw_centered("LINE 3", font_main, int(h * 0.04) + int(w * 0.120), fill=(255, 220, 160, 255))

# EN subtitle — 2-line wrap, lower contrast
draw_centered('"English line 1"', font_small, int(h * 0.04) + int(w * 0.190), fill=(170, 170, 170, 220))
draw_centered('English line 2."', font_small, int(h * 0.04) + int(w * 0.220), fill=(170, 170, 170, 220))

# Watermark bottom-right (gold)
wm = "DITEMPA BUKAN DIBERI ⚒"
bbox = draw2.textbbox((0, 0), wm, font=font_small)
ww = bbox[2] - bbox[0]
draw2.text((w - ww - int(w*0.04) + 1, h - int(h*0.04) + 1), wm, font=font_small, fill=(0, 0, 0, 200))
draw2.text((w - ww - int(w*0.04), h - int(h*0.04)), wm, font=font_small, fill=(255, 200, 100, 220))

# Attribution bottom-left (gray)
attr = "i-ARIF · 2026"
draw2.text((int(w*0.04) + 1, h - int(h*0.04) + 1), attr, font=font_small, fill=(0, 0, 0, 200))
draw2.text((int(w*0.04), h - int(h*0.04)), attr, font=font_small, fill=(140, 140, 140, 220))

# 5. Save final
final = base.convert('RGB')
final.save('output.jpg', quality=92)
```

## Text sizing rules (learned 2026-08-28)

| Element | Size formula (w = image width) | Notes |
|---|---|---|
| BM main quote | `w * 0.043` | `w * 0.055` OVERFLOWS on long words ("BERJAYA", "SANGGUP") |
| EN subtitle | `w * 0.022` | Lower contrast, italic-feel |
| Watermark | `w * 0.022` | Gold (255, 200, 100), bottom-right |
| Attribution | `w * 0.022` | Gray (140, 140, 140), bottom-left |
| Line height (main) | `w * 0.060` | Vertical spacing between BM lines |

## Color palette (verified 2026-08-28)

- **Main line 1 (warm white):** `fill=(255, 245, 230, 255)` — pure white too clinical
- **Main line 2-3 (warm gold):** `fill=(255, 220, 160, 255)` — accent
- **EN subtitle (gray):** `fill=(170, 170, 170, 220)` — secondary
- **Watermark (gold):** `fill=(255, 200, 100, 220)` — arifOS constitutional
- **Attribution (gray):** `fill=(140, 140, 140, 220)` — provenance

## Mandatory post-generation check

After saving, **always** call `vision_analyze` on the output:

1. Read all visible text verbatim — verify no truncation
2. Check for text overflow at edges — reduce font 15-20% if overflow
3. Verify watermark + attribution visible and not overlapping subject

If overflow detected → re-render with smaller fonts. Don't ship overflowing posters.

## Composition rules (for the prompt that generates the base image)

To get good poster composition, instruct the model:
- "leaves clean dark space at the top third of the frame for text overlay"
- "subject in lower 60% of frame, centered or rule-of-thirds"
- Background should be defocused so vignette + text doesn't fight scene detail

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Text overflows right edge | `font_size = w * 0.055` too large for long BM words | Reduce to `w * 0.043`, re-wrap lines manually |
| Text invisible against bright background | Top vignette too weak | Increase alpha from 210 to 240, OR extend vignette to 50% |
| Watermark overlaps subject face | Bottom-right placement collision | Move watermark to bottom-left, attribution to bottom-right |
| EN subtitle cut off ("do..." overflow) | Single-line wrap assumed | Always wrap EN subtitle into 2 lines manually |
| Quote feels disconnected from image | No color harmony | Use warm whites/golds (`255, 245, 230`) over noir images, not pure white |

## Proven BM + EN pairings (use as default quote library)

| BM main | EN subtitle |
|---|---|
| "Orang berjaya sanggup bayar harga yang orang biasa tak sanggup." | "The price of greatness is doing what average people are unwilling to do." |
| "Kebanyakan orang mahukan hasil luar biasa, tetapi tidak sanggup membayar harga yang luar biasa." | (same EN as above) |
| "Orang panggil dia gila, sampai jadi. Lepas tu orang panggil genius." | "People call it crazy until it works. Then they call it genius." |
| "DITEMPA BUKAN DIBERI." | "Forged, not given." (arifOS constitutional motto) |
| "Harga kejayaan ialah buat benda yang orang biasa tak sanggup buat." | "Successful people are willing to do what unsuccessful people are not willing to do." |

**Avoid** for this lane (too soft / generic — Arif's stated preference):
- "Believe in yourself" / "Dream big" / "Be the change" / "Every cloud has a silver lining"

## Default-archetype safety (F9 anti-hantu, 2026-08-28)

**Rule:** When user requests a portrait of a named real person but no reference photo is uploaded in the same turn, **default to a generic archetype**. Never hallucinate a face from memory + imagination.

The output label convention (always include in delivery message):

> "Subject: generic [ethnicity] sado archetype — bukan [named person's] face. Aku generate dari prompt tanpa reference photo. Kalau nak jadi portrait [named person], supply reference + authorization untuk face-preserve flow."

Scar (2026-08-27): confidently listed "Siti Nurhaliza/Yuna/Aina" for a Jiwa Merdeka poster without calling vision_analyze — actually guessed from typical Malaysia Merdeka lineup. Arif scolded. A poster of a named real person generated from prompt-only is the same pattern. Default to archetype, label clearly, never declare unverified identity.

## Verification before delivery

Always run `vision_analyze` on the final poster before sending to user:
- "Read all visible text in this poster verbatim. Does any text overflow or get cut off at the edges?"
- Fix overflow if detected, re-render, vision-QC again.
- Never deliver a poster that hasn't been vision-QC'd.
