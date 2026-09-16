# Brand Motivational Poster Pattern

**Captured:** 2026-08-29 (Mr. Enrich 1-hr-before poster for Amir, Syed's gym)

When the user asks for a **countdown hype poster / motivational board / fight-night
graphic** — single dramatic hero background, big bold typography, side info
panel with checklist, bottom quote band. NOT a multi-image grid (that's the
separate `pil-instructional-composite-pattern.md`). This is the **single-hero
brand poster** pattern.

## Pattern

```
1. Generate ONE strong background via SANA/FLUX
   (silhouette bodybuilder, dramatic gym lighting, dark + red/orange accent,
    subject readable through vignette but not too detailed under the text)
2. PIL: vignette darkening (Gaussian-blurred ellipse mask) to focus center
3. PIL: top header bar (red 170,0,0 ~240 alpha) with bold title + subtitle
4. PIL: center hero text (huge ~120pt, yellow accent 255,230,100)
5. PIL: subtitle below (mid-sized white)
6. PIL: right-side info panel — black 210-alpha rectangle + yellow 3px border,
   numbered checklist items at ~80px row pitch
7. PIL: bottom quote band — dark fill, motivational quote + sign-off line
8. Save as PNG, deliver via MEDIA:
```

## Why this works

- One hero image is all the bodybuilder silhouette needs; users judge vibe, not
  detail at this scale
- PIL is local, always available, deterministic, zero cost — text renders
  cleanly, layout is exact
- Single composite delivers instantly as PNG to Telegram
- Personalization (event name, athlete name, date) lands in the header strip
  + bottom sign-off — makes it feel custom, not generic

## Working recipe (Mr. Enrich 1-hr-before poster, 2026-08-29)

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Hero background from SANA (768x768 free tier, resize up)
src = Image.open('/tmp/hero.jpg').convert('RGB').resize((1080, 1080), Image.LANCZOS)

# Vignette to focus center
vignette = Image.new('L', src.size, 0)
vd = ImageDraw.Draw(vignette)
cx, cy = 540, 540
for r in range(800, 0, -20):
    alpha = max(0, min(180, (800 - r) // 4))
    vd.ellipse([cx-r, cy-r, cx+r, cy+r], fill=alpha)
vignette = vignette.filter(ImageFilter.GaussianBlur(80))
canvas = Image.composite(src.convert('RGBA'),
                        Image.new('RGBA', src.size, (0,0,0,255)),
                        vignette)
canvas = Image.alpha_composite(canvas, Image.new('RGBA', src.size, (0,0,0,120)))

# Header bar
hdr = Image.new('RGBA', canvas.size, (0,0,0,0))
hd = ImageDraw.Draw(hdr)
hd.rectangle([0, 0, 1080, 100], fill=(170, 0, 0, 240))
hd.text((40, 22), "T-MINUS 1 HOUR", font=F(54), fill=(255, 230, 100))
hd.text((40, 70), "MR. ENRICH ON THE GO 2026 - MENS FITNESS FINAL",
        font=F(24, 1), fill=(255, 255, 255))
canvas = Image.alpha_composite(canvas, hdr)

draw = ImageDraw.Draw(canvas)

# Hero text — center via textbbox
hero_f = F(120)
bbox = draw.textbbox((0,0), "OWN IT.", font=hero_f)
draw.text(((1080 - (bbox[2]-bbox[0])) // 2, 140),
          "OWN IT.", font=hero_f, fill=(255, 230, 100))

# Side panel — keep clearance so border doesn't clip header text
panel = Image.new('RGBA', canvas.size, (0,0,0,0))
pd2 = ImageDraw.Draw(panel)
pd2.rectangle([650, 360, 1050, 970],   # 400px wide
              fill=(0, 0, 0, 210), outline=(255, 200, 60), width=3)
canvas = Image.alpha_composite(canvas, panel)
draw = ImageDraw.Draw(canvas)

# Panel header — inset 20px from panel left edge
draw.text((670, 372), "FINAL HOUR CHECKLIST", font=F(26),
          fill=(255, 230, 100))
draw.line([670, 405, 1030, 405], fill=(255, 200, 60), width=2)

# Items at 80px row pitch
items = [("01", "FINAL PUMP", "Light curls + band work"), ...]
iy = 430
for num, title, desc in items:
    draw.text((670, iy), num, font=F(34), fill=(255, 200, 60))
    draw.text((720, iy + 4), title, font=F(22), fill=(255, 255, 255))
    draw.text((720, iy + 34), desc, font=F(18, 1), fill=(200, 200, 200))
    iy += 80

# Bottom quote band — reserve 100px height
bot = Image.new('RGBA', canvas.size, (0,0,0,0))
bd = ImageDraw.Draw(bot)
bd.rectangle([0, 980, 1080, 1080], fill=(15, 15, 15, 235))
canvas = Image.alpha_composite(canvas, bot)
draw = ImageDraw.Draw(canvas)

qb = draw.textbbox((0,0), quote, font=F(32))
draw.text(((1080 - (qb[2]-qb[0])) // 2, 1000), quote, font=F(32),
          fill=(255, 230, 100))

# Signoff line smaller
gb = draw.textbbox((0,0), signoff, font=F(20, 1))
draw.text(((1080 - (gb[2]-gb[0])) // 2, 1042), signoff, font=F(20, 1),
          fill=(200, 200, 200))

canvas.convert('RGB').save(out, 'PNG', optimize=True)
```

## Critical pitfalls (encountered in the field)

| Pitfall | Fix |
|---------|-----|
| Panel border clips header text on right edge | Make panel 400px wide (NOT 380); inset header 20px from panel left; **measure textbbox first** |
| Editing via partial clear leaves ghost border | Don't edit-on-top — regenerate whole poster from scratch, faster than chasing artifacts |
| `fill=(r,g,b)` silently drops alpha on RGBA canvas | Use `(r,g,b,255)` tuples, or PIL flattens to opaque and panel looks wrong |
| Vignette too dark → text unreadable on top | Apply vignette THEN add a 100-120 alpha black overlay before drawing text — gives consistent darkening everywhere |
| Hero text off-center | Manual centering via `((canvas_w - textbbox_width) // 2, y)` — don't trust font metrics alone |
| Bottom quote band cuts off signature line | Reserve 100px height (y=980 to y=1080); quote at y=1000, signoff at y=1042 with smaller font (20pt) |
| `text()` with multiline string + `anchor='mm'` | Same as grid pattern — use single-line captions or split |
| DejaVu font not found on minimal systems | Wrap `truetype()` in `try/except`, fall back to `ImageFont.load_default()` |

## Personalization levers

A motivational poster only feels custom when these land:
- **Event name + date** in the header strip
- **Athlete name + gym** in the bottom sign-off line
- **Quote source** if attribution matters (otherwise generic works)
- **Color palette** — for bodybuilding use red+gold+yellow on black; for other
  sports swap accent colors but keep contrast high

If the user wants variants (different quote, different checklist), do them as
separate PIL passes — don't try to template-generate. Single-pass PIL is
faster and more reliable than a templating layer.

## When to use which poster pattern

| Use case | Pattern |
|----------|---------|
| Step-by-step how-to infographic | Grid pattern (`pil-instructional-composite-pattern.md`) |
| Countdown / T-minus hype / fight-night | **This pattern** (single hero + panel) |
| Athlete headshot poster | MiniMax image-01 alone — no PIL |
| Brand announcement with multiple photos | Grid pattern with hero band on top |
| Promotional graphic with date/venue/call-to-action | **This pattern**, drop the checklist, swap to event info |

## Honest delivery rule

The SANA/FLUX background is silhouette + vibe, not a photoreal athlete. Tell
the user upfront: "Background ni AI-generated silhouette untuk vibe, bukan
athlete specific." Athlete will recognize it as hype graphic, not a fake photo
of them. Don't oversell the realism — the typography + layout is what makes
it feel pro, the photo just sets mood.