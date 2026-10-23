---
name: social-promotional-poster
description: 'Build fixed-size promotional raster graphics (Instagram post 1080x1350, Story 1080x1920, FB cover, X header 1500x500, Telegram channel banner) end-to-end - HTML authoring to headless Chrome screenshot to vision-loop'
version: 1.0.0
metadata:
  hermes:
    tags: [poster, design, html, headless-chrome, social-media, malaysian-brand, image-pipeline, viral, instagram, telegram]
    related_skills: [claude-design, sketch, excalidraw, popular-web-designs]
---

# Social Promotional Poster - HTML to PNG pipeline

Build downloadable, fixed-size raster graphics designed for sharing on Instagram, Telegram, X, Facebook, etc. The user expects a PNG file at known pixel dimensions, not an open-in-browser page.

Use this skill when the deliverable is a single image meant to post on social platforms. For interactive web surfaces (landing pages, dashboards, decks), use `claude-design` instead. For throwaway variant exploration, use `sketch`.

## When NOT to use this

- User wants a real interactive web page -> `claude-design`
- User wants 2-3 variants to compare -> `sketch`
- User wants a diagram, flowchart, or schematic -> `excalidraw`, `architecture-diagram`
- User wants a slide deck (multi-page interactive) -> `claude-design` deck mode

## Core recipe

### 1. Pick the canvas dimensions up-front

| Platform | Size | Aspect |
|---|---|---|
| Instagram post (feed) | 1080 x 1350 | 4:5 portrait |
| Instagram Story / Reel | 1080 x 1920 | 9:16 portrait |
| Instagram square | 1080 x 1080 | 1:1 |
| Facebook cover | 851 x 315 | ~2.7:1 landscape |
| X / Twitter header | 1500 x 500 | 3:1 landscape |
| X / Twitter post (single) | 1200 x 675 | 16:9 |
| Telegram channel banner | 1280 x 720 | 16:9 |
| LinkedIn cover | 1584 x 396 | 4:1 landscape |

If the user does not specify, default to **1080 x 1350** (IG post) - most universal Malaysian social-marketing format. Ask before generating at non-standard sizes.

### 2. HTML canvas setup

```html
<!DOCTYPE html>
<html lang="ms">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;600;700;800;900&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1080px; height: 1350px;
  background: #0a0a0a;
  font-family: 'Inter', sans-serif;
  overflow: hidden;
  position: relative;
}
/* ... your design ... */
</style>
</head>
<body>
<!-- Hero image, badge, title, features, CTA, footer -->
</body>
</html>
```

**Critical:** fixed `width/height` on `<body>`. Never `vw/vh` - Chrome `--window-size` matches the body box.

### 3. Headless Chrome render - the right invocation

```bash
google-chrome --headless --disable-gpu --no-sandbox \
  --user-data-dir=/tmp/chrome-data-fresh-$(date +%s) \
  --virtual-time-budget=8000 \
  --hide-scrollbars \
  --screenshot=/path/to/out.png \
  --window-size=1080,1350 \
  "file:///path/to/poster.html"
```

**Mandatory flags (verified failures without them):**

| Flag | Why |
|---|---|
| `--user-data-dir=/tmp/...-$(date +%s)` | Without a fresh profile dir, Chrome reuses cached state and renders can return identical MD5 even after CSS changes (proven - 3 successive renders with different CSS values produced same hash until `--user-data-dir` was set) |
| `--virtual-time-budget=8000` | Google Fonts load asynchronously. <3000ms budget -> fonts miss -> wrong metrics -> wrong layout |
| `--hide-scrollbars` | Cleaner PNG without scroll-bar artifacts |
| `--window-size=W,H` | Must match `<body>` dimensions. Mismatch -> silent upscale |

Verify with `identify /path/to/out.png` (from ImageMagick `imagemagick` package) and check MD5 hash before/after CSS patches. **Identical MD5 after a patch means the patch did not render. Investigate, do not trust the output.**

### 4. Vision-loop self-critique

After every render, run this exact prompt against the PNG:

```
Review this promotional poster. Be brutally honest:
1. Hero image - present and clean, or YouTube UI / watermarks / product mismatch leaking through?
2. Typography hierarchy - which element wins the eye first? What is competing?
3. CTA clarity - is there ONE clear next action with one clear next channel?
4. Overall viral coefficient 0-10. What is broken, what is working, what is the ONE thing that would push this +2 points?
```

Iterate at least 3 times. The first render is a draft, the third render is a candidate, final render only after the user picks a direction. Never ship the first render.

### 5. Save final + deliver

Final files in a dedicated poster folder with clean naming:

```
sado/poster/
├── SADO-POSTER-FINAL.png      <- user-facing
├── sado-v5.html                <- source HTML
├── syed-hero-v5.jpg            <- cropped hero
├── hero.jpg                    <- food/product hero
└── variants/sado-v3.png        <- earlier versions for reference
```

Tell the user: file path, dimensions, what is in the design, what caveats remain.

---

## Hero image sourcing

### Stock: Unsplash direct CDN extraction

Public Unsplash photo pages embed the direct CDN URL in their HTML. Pattern:

```bash
curl -sL "https://unsplash.com/photos/<id>" \
  | grep -oE 'https://images\.unsplash\.com/photo-[a-zA-Z0-9_?&=/%+-]+' \
  | head -1
```

Then pre-download locally (Chrome headless cannot reliably fetch external images):

```bash
curl -sL "<cdn-url>?w=1200&q=85&auto=format&fit=crop" -o /path/to/hero.jpg
```

Always verify the image content matches expectation via `vision_analyze` before compositing - wrong photo category (e.g. dim sum instead of nasi lemak) is the #1 unsplash mistake.

### Real-person photo from Telegram/WhatsApp/screenshot

When the user supplies a screenshot (paused video, paused phone, screen recording):

1. **First try: ask for the original frame file.** Screen recordings, original photo, or unpaused capture - anything without UI overlays baked in.
2. **Second try: inpainting.** OpenCV `cv2.inpaint` (TELEA or NS algorithm) with `inpaintRadius=15-25`. Verify via `vision_analyze` whether the cleanup is acceptable. Realistically it produces visible smudges, not clean reconstruction.
3. **Third try (and the honest answer):** when inpainting cannot deliver, **embrace the artifact as a design motif**. The "Playing on 32 inch Smart Monitor M7" caption in the Syed screenshot became a punchline (e.g. "Bukan airbus - rasa power."). Honest viral energy beats half-cleaned smudges.
4. **Diffusion inpainting (LaMa/SDXL) is not installed by default** on this box. `torch` + `transformers` are available, `diffusers` is not. `pip install diffusers` before promising production-clean inpainting - adds ~10-15min install time + ~4GB model download.

### Real-people-in-promos hard rule

**AI-generated stand-ins must NEVER replace a named real person in external promotional posts.** The federation has AI bodybuilder images stored at `/root/forge_work/abang_sado_*.png`, `/root/.openclaw/media/*sado*.jpg`, `/root/abang_sado_chest.png` - these are pipeline diagnostic artifacts, not real subjects. They are OK for:

- Rough layout mockups
- Internal brand exploration
- Testing typography / color treatments

They are NOT OK for:

- External social posts where the named human is referenced
- Brand collab materials with another person is real identity
- Any deliverable going to a third party (clients, vendors, public followers)

Before any poster featuring a named human:

1. `find /root -maxdepth 5 -type f \( -iname "*<name>*" -o -iname "*<handle>*" \) \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.webp" \)` for existing real photos.
2. If none, ask the user to supply a fresh photo (single message: "Real photo needed - Syed shot from chest-up clean frame works"). Do not proceed with AI stand-ins and pretend.
3. Arif is words (verbatim, 2026-08-06 session): "Syed adalah manusia Sado sebenar. Hang jangan nak buat dia jadi AI Agent plak." - the brand is the person, the person is real, fake stand-ins destroy trust.
4. **Image-edit models ALSO fail identity preservation** (verified 2026-08-12). Do NOT use Gemini/Qwen image-to-image edit to "place this person in a new scene" — the model regenerates the face. Use the **composite fallback** (rembg cutout + empty background + PIL paste) documented in `gemini-media-gen` → `/root/AAA/skills/gemini-media-gen/references/identity-preservation-composite-fallback.md`. Arif's binding rule: "Hang jangan ubah muka manusia."

---

## Malaysian brand voice (BM / Manglish)

When the poster is for a Malaysian audience or Malay-speaking subject (Abang Sado style, local F&B, Malaysian trader, local event):

- **Tone:** Direct, masculine, no-nonsense. Numbers over adjectives ("3 level" not "multiple options").
- **Bahasa:** Mix BM casual + Manglish ("Macam mana?", "Hang pilih", "Jalan terus", "Pre-order malam sebelum"). Do not use formal BM like "Anda boleh" - too stiff for viral reach.
- **Tagline construction:** Pair the literal product with attitude. "Otak sado, sambal sado, nasi lemak power punya." - three-beat joke, quotable, screenshot-able.
- **Urgency:** Malaysian social buyers respond to scarcity + pre-order loops: "Weekend confirm sold out. DM sekarang untuk slot." Slot mechanics > discount mechanics for local food drops.
- **CTA channel:** ONE channel only. Pick Instagram DM (`@handle`) OR WhatsApp OR Telegram - not three competing options. Decision fatigue kills conversion.
- **Emoji:** Sparingly. Spice, fire, muscle, alarm, bell for urgency - but never as section dividers (looks generic SaaS).
- **The bridge line:** If two personas are involved (subject of photo != seller), add a one-line bridge credit so viewers know who is who. *"Muscle by Syed. Sambal by Abang Sado."* - disambiguates collab.

---

## Visual decision frameworks

### Layout archetypes

| Archetype | When | Pattern |
|---|---|---|
| Hero-overlap | Single big subject (one person, one product) | Full-width hero top + 3-pillar features bottom |
| Hero-side-by-side | Person + product collab | Hero left 50%, content right 50% - gold panel right with copy |
| Contrast-flow | Two opposing subjects (muscle + food, boss + team) | Top zone = subject A, bottom zone = subject B, gold accent on bridge |
| Diagonal-energy | High-motion products (food drop, sneaker drop) | Diagonal split with action bleeding across |
| Quote-centric | Founder story, mission statement | Big quote fills hero zone, supporting proof below |

For viral Malaysian food/local drops, **contrast-flow** (Syed shirtless to nasi lemak) and **hero-overlap** both work. Avoid **quote-centric** unless there is a real founder story - otherwise it reads as templated.

### Color palettes

| Brand vibe | Base | Accent | Notes |
|---|---|---|---|
| Premium Malaysian F&B | #0a0a0a | #d4af37 (gold) | Black + gold = "classy sado" |
| Street / hipster | #fff8e7 (warm cream) | #e63946 (sambal red) | Warm light, food-forward |
| Tech / SaaS | #0a0a0a | #0066ff (electric blue) | Default tech - avoid unless brand warrants |
| Outdoor / fitness | #1a3a2a (forest green) | #f5d76e (sunlit gold) | Earthy, contrasts well with skin |
| Bold / Gen Z | one bold color | white text | Hot pink, electric green, neon yellow |

For Syed/sado-style personal brand, **black + gold** is the proven winner (tested 2026-08-06 nasi lemak poster - 8/10 viral coefficient from vision loop review).

### Typography

| Role | Family | Weight |
|---|---|---|
| Display title (brand name) | Playfair Display, Bodoni, Didot | 900 |
| Section headers | Inter, Sora, Space Grotesk | 800 |
| Body | Inter | 400-600 |
| Quote / accent | Playfair Display italic | 700 |

Avoid: Inter-only stacks (looks default SaaS), Bebas Neue for body (illegible below 18px), system fonts (signals "no design effort").

---

## Pitfalls (learned from production)

1. **Chrome cache returns identical MD5 across CSS changes.** Verify with `md5sum` after every patch - never trust a render until hash differs.
2. **Google Fonts do not load in <3000ms headless budget.** Set `--virtual-time-budget=8000` minimum.
3. **Unsplash direct URL guessing returns 404.** Always extract from the photo page HTML.
4. **Unsplash `?w=900&q=85` URLs that "work" can serve wrong content** - random food photo returned dim sum when "nasi lemak" was requested. Always `vision_analyze` to verify before compositing.
5. **OpenCV inpainting only blurs, does not regenerate skin.** Promising cleanups that cannot be delivered destroys trust. Either install `diffusers` or embrace the limitation as design motif.
6. **Real people's faces from `/root/forge_work/` or `/root/.openclaw/media/` are AI-generated stand-ins** - for mockups only, never for external posts with named humans.
7. **Mixing 4 fonts creates slop.** Two max for body, one for display. Inter + Playfair Display is the safe default.
8. **Hero image filters change brand mood.** `brightness(0.55)` = moody/cinematic, `brightness(0.85)` = warm/applealing, `brightness(1.0)` = flat. Match filter to food (warm/bright) vs person (moody/contrast).
9. **AI slop archetype #1: "centered hero + three equal-weight feature cards."** Already trained as anti-pattern in `claude-design`. Reuse that framework, do not reinvent.
10. **Promotion channel confusion.** If poster says "DM @handle" AND "WhatsApp" AND "Telegram" - viewer picks none. One channel only.

If poster says "DM @handle" AND "WhatsApp" AND "Telegram" - viewer picks none. One channel only.

### Matplotlib fallback (when no Chromium / no Unsplash hero)

For layout-only editorial pieces (event calendars, intelligence briefs, weekly radar posters, dark editorial infographics) where the lane capability map lists `matplotlib` instead of HTML/Chrome — use this pattern, NOT the HTML/Chrome pipeline. Verified 2026-08-11 on the SADO PHYSIQUE RADAR weekly scan (1080x1080 dark editorial, 4 event cards, A4 landscape PDF sibling).

**When to use this vs. the HTML pipeline:**
- No hero image required (geometric grid, list-based, dark editorial)
- Chromium not available / heavy-handed for the task
- Need precise pixel control over a fixed canvas at known dimensions
- The deliverable is a *third* alongside PDF + HTML (e.g. poster + PDF + HTML = 3 artifacts from one dataset)

**Canvas recipe:**
```python
fig = plt.figure(figsize=(10.8, 10.8), dpi=100, facecolor="#0a0a0c")
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_facecolor("#0a0a0c"); ax.axis("off")
```

**The 5 matplotlib layout pitfalls that bite every time** (verified by re-rendering the SADO POSter 3x):

1. **Title overflow into right meta column.** Default matplotlib font metrics are wider than HTML. If you have a header with title-on-left and meta-on-right, compute title width FIRST (`len(text) * fontsize * 0.55` ≈ pixel width for DejaVu Sans bold) and pad the right column by that much. Or render title at `fontsize=38` (not 44+) for full-page-width text.
2. **Card text bleeds past card width.** `textwrap.wrap(string, width=N)` BEFORE drawing — never let `ax.text()` flow. Measure N from card width: `width_chars = (card_px * 0.85) / (fontsize * 0.55)`.
3. **Adjacent cards overlap when content is wider than expected.** Top-row card-2 title can visually intrude into bottom-row card-1 if titles are 2-line. Always lay name-block at fixed `y + h - 56` with `va="top"`, advance by line_height around 24 per wrapped line, and leave at least 30px before the meta block.
4. **Right-edge text gets clipped silently.** `ax.text(..., ha="right")` with `x = W - 50` works for short labels. For long right-aligned meta strings, render with `ha="left"` and `x = W - estimated_width - 50`. Matplotlib does NOT auto-clip warnings.
5. **Legend dots overlap legend text.** Place each dot+label with `x = base + cumulative_offset`, not `x = base + i * 80`. Compute the offset from the previous label's actual rendered width.

**Mandatory verify loop after EVERY render** (structural + visual):
```python
from pathlib import Path
import struct
p = Path(out)
assert p.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", "not PNG"
with p.open("rb") as f:
    f.seek(16); w, h = struct.unpack(">II", f.read(8))
assert w == 1080 and h == 1080, f"wrong dim {w}x{h}"
```
Then `vision_analyze` the saved PNG with a targeted question: "Any text overlap, cutoff, or alignment issues?" The vision loop is the cheapest way to catch the 5 pitfalls above; pure structural checks miss them.

**For multi-iteration editorial pieces (poster + PDF + HTML together):**
- Build all 3 in one session, then verify each
- First render is a draft — expect to fix overlap on iterations 2–3
- The vision_analyze loop IS the test for visual editorial work

### Creative UI / visual work — testing discipline

For purely visual / editorial deliverables (posters, dashboards, slide decks, infographics, calendar renders):
**hold off on tests/linters until the user says they like the result OR you are about to commit.**
Lint passes do not catch text overlap. Vision review does. Per system guidance (2026-08-11):
> "if this is creative UI/visual work, hold off on tests and linters until the user says they like the result or you're about to commit."

The right discipline is: build → vision_analyze → patch → vision_analyze → final. The `vision_analyze` loop IS the test. Structural verification (PNG signature, PDF header, HTML content presence) is the right complement, not a substitute for the vision loop.

## Templates and references

- `templates/social-poster-1080x1350.html` - generic IG post scaffolding with hero slot, badge, title, three-pillar features, gold CTA, footer
- `references/poster-iteration-checklist.md` - copy-paste vision-loop review prompt + dimension verification checklist
- `references/malaysian-brand-voice.md` - BM/Manglish tagline patterns, urgency phrases, CTA channel conventions
- `references/matplotlib-editorial-poster-skeleton.py` - 1080x1080 dark editorial skeleton (proven SADO PHYSIQUE RADAR 2026-08-11): canvas + grid texture + 4-card event layout + legend + footer + built-in PNG signature+dim verification

## Routing notes (moved from description 2026-10-23)

self-critique to multi-iteration. Covers hero image sourcing (Unsplash CDN extraction, real-photo inpainting limits), typography hierarchy, BM/Manglish copywriting for Malaysian brand voice, and the brand-fidelity rule that AI stand-ins must NEVER replace a named real person. Triggers include poster, banner, cover, social card, IG post, promote X, viral, Jordon Yeoh style, poster untuk abang, or any request for a downloadable PNG/JPG designed for sharing.
