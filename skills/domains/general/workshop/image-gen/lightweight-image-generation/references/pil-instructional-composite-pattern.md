# PIL Instructional Composite Pattern

**Captured:** 2026-08-26 (SADO competition-tan how-to session)

When a user asks for a "step-by-step infographic" or "how-to guide with images,"
don't try to make one engine render text + 5 steps + decorative borders — no
free model handles that. Instead, compose: multi-AI-gen grid + PIL text overlay.

## Pattern

```
1. Generate 3-5 candidate images via parallel engines
   (focused prompts, each one = one step or aspect)
2. vision_analyze each — pick the best partial that hints at the step
3. PIL-composite: grid of images + header bar + caption boxes + pro-tips text
5. Single MEDIA: delivery of the composite PNG
```

## Why this works

- Free engines (SANA, free GET) reliably render bodies, gym scenes, buttfleshand
  poses — they just can't hold a full multi-step infographic concept
- PIL is local, always available, deterministic, zero cost
- User gets ONE deliverable that combines best partial images with real readable text
- Text in PIL renders cleanly; text in SANA/multi-element renders never do

## Working recipe (from competition-tan session)

```python
from PIL import Image, ImageDraw, ImageFont

# Load images (each = one step)
img1 = Image.open('/tmp/step1.jpg').resize((540, 540))
img2 = Image.open('/tmp/step2.jpg').resize((540, 540))
img3 = Image.open('/tmp/step3.jpg').resize((540, 540))

W, H = 1620, 1240
canvas = Image.new('RGB', (W, H), '#0a0a0a')
draw = ImageDraw.Draw(canvas)

# Fonts — fall back to default if DejaVu unavailable
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
cap_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

# Header bar
draw.rectangle([(0, 0), (W, 80)], fill='#FF6B35')
draw.text((W//2, 25), "TITLE", fill='white', font=font, anchor='mm')
draw.text((W//2, 60), "subtitle", fill='#330000', font=sub_font, anchor='mm')

# Image grid + captions
captions = [
    ("1. STEP TITLE", "description line 1"),
    ("2. STEP TITLE", "description line 2"),
    ("3. STEP TITLE", "description line 3"),
]
x_positions = [0, 540, 1080]
for x, img, (title, desc) in zip(x_positions, [img1, img2, img3], captions):
    canvas.paste(img, (x, 100))
    draw.rectangle([(x, 100), (x+540, 640)], outline='#FF6B35', width=3)
    draw.rectangle([(x, 640), (x+540, 740)], fill='#1a1a1a')
    draw.text((x+270, 670), title, fill='#FF6B35', font=cap_font, anchor='mm')
    draw.text((x+270, 700), desc, fill='#aaa', font=sub_font, anchor='mm')

# Pro tips section (below grid)
draw.rectangle([(0, 760), (W, H)], fill='#1a1a1a')
draw.rectangle([(0, 760), (W, 770)], fill='#FFD700')  # gold divider
draw.text((W//2, 790), "PRO TIPS - Category", fill='#FFD700', font=font, anchor='mm')

y = 830
for tip in tips_list:
    draw.text((60, y), ">", fill='#FF6B35', font=tip_font)
    draw.text((85, y), tip, fill='#ddd', font=tip_font)
    y += 55

canvas.save('/tmp/output.png', quality=95)
```

## Critical PIL pitfalls

| Pitfall | Fix |
|---------|-----|
| `text("multi\nline", anchor='mm')` → `ValueError: anchor not supported for multiline text` | Either split into per-line `text()` calls, OR use single-line captions. Both work. |
| DejaVu font not found on minimal systems | Wrap `truetype()` in `try/except`, fall back to `ImageFont.load_default()`. |
| Caption text overlaps image border | Add filled rectangle below image (e.g. y=640 to y=740), THEN draw text on top. |
| Text vertical alignment looks off | Use `anchor='mm'` (middle-middle) for centered labels in boxes. |
| Tips text spills past canvas | Track `y` cursor, increment per line (~55px for 17-pt font + line break). |

## When to use this vs. single AI-gen

| Use case | Route |
|----------|-------|
| User wants "show me how X is done, step by step" | **PIL composite** (this pattern) |
| User wants ONE illustration, single scene | Single AI-gen, vision_analyze, ship |
| User wants character portrait or headshot | MiniMax image-01 (realism wins) |
| User wants brand poster with text overlay on photo | PIL composite (1 hero image + text) |
| User wants conceptual composite scene (3+ elements) | MiniMax/Wan paid lane OR honest degraded SANA |

## Companion pattern

For countdown / T-minus hype posters (single hero + side panel + bottom quote,
NOT a grid), see `brand-motivational-poster-pattern.md`.

## Honest delivery rule

If PIL composite ships with AI-gen partials that don't perfectly match every
caption, say so in the chat reply: "Yang ketiga tu — apply evenly dengan coach..."
Be transparent which step's photo is partial/full. Arif (and most users) values
honesty over pretending each photo = exact step depicted.