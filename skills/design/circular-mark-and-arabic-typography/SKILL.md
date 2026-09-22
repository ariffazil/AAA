---
name: circular-mark-and-arabic-typography
description: "Design circular logos/avatars; verify by pixel sampling."
version: 1.0.0
owner: Hermes
risk_tier: low
tags: [logo, avatar, arabic, typography, svg, telegram, verification]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Circular Mark & Arabic Typography

For any request to design a logo, avatar, seal, badge, or circular group mark. Covers the two things
that silently break: **SVG that does not render**, and **verifying Arabic with a vision model**.

## 1. Render type in a browser — never in PIL or matplotlib

Browsers do full Arabic shaping (contextual joining, lam-alef ligature, hamza placement). PIL and
matplotlib do not — they need `arabic_reshaper` + `python-bidi` and even then produce weaker output.
So build the mark as **HTML with inline CSS/SVG**, load the fonts with `@font-face` pointing at
`file://` TTF paths, and screenshot through Chrome/CDP at `deviceScaleFactor=2`, then downscale with
LANCZOS to the delivery size. The 2x render plus LANCZOS downscale is what makes small sizes crisp.

Download display faces from the Google Fonts GitHub mirror:
`https://github.com/google/fonts/raw/main/ofl/<family>/<File>.ttf` (URL-encode the filename if it
contains `[]` or `,`, e.g. `ReemKufi%5Bwght%5D.ttf`).

Arabic display faces that render correctly and are safe for religious or community names:
**Amiri** (naskh — most orthographically explicit; make this the default), **Scheherazade New**,
**Aref Ruqaa** (calligraphic ruqaa), **Reem Kufi** (geometric kufi).

## 2. Bare SVG elements in HTML render as nothing

A `<circle>` or `<rect>` written directly into HTML — with no `<svg>` wrapper — is an unknown element.
The browser drops it. **No error, no console warning, no visual clue in the code review.** The design
just loses its rings and frame, and the page still looks plausible because the background and text
rendered fine.

Always wrap geometry:

```html
<!-- WRONG: silently invisible -->
<div class="sq" style="background:...">
  <circle cx="512" cy="512" r="462" fill="none" stroke="#C9A227" stroke-width="11"/>
</div>

<!-- RIGHT -->
<div class="sq" style="background:...">
  <svg class="decor" viewBox="0 0 1024 1024"
       style="position:absolute;top:0;left:0;width:1024px;height:1024px">
    <circle cx="512" cy="512" r="462" fill="none" stroke="#C9A227" stroke-width="11"/>
  </svg>
</div>
```

**Detect it by sampling pixels, never by reading the markup.** Load the rendered PNG and count pixels
matching the accent colour in the annulus where the ring should be. If the count is zero, the ring is
not there:

```python
from PIL import Image
import numpy as np
a = np.asarray(Image.open(png).convert("RGB")).astype(int)
m = np.abs(a - np.array(acc_rgb)).sum(axis=2) < 90
y, x = np.nonzero(m)
r = np.sqrt((x - 512)**2 + (y - 512)**2)
print("ring pixels:", int(((r > 455) & (r < 470)).sum()))   # zero => not rendered
```

Same method proves the mark is centred: take the **centre of mass** of the ink colour, not the
bounding-box centre. A calligraphic bbox is pulled upward by ascenders and dots; the mass centre is
the honest optical centre. Nudge the CSS `top` until mass centre lands on the canvas centre.

## 3. Do not verify Arabic with a vision model

A VLM asked to read the same Arabic word from the same image returned, across three calls, three
different readings — one correct, one a different word, one the correct word with a fabricated
orthographic error. It also reported a missing frame that *was* genuinely missing in one render and
*present* in another, with no reliable signal about which. **The model's Arabic reading is not
evidence.**

What is evidence:

- **The DOM string is the truth.** A browser text engine renders exactly the codepoints it is given.
  There is no failure mode where it substitutes different characters. Assert the string:
  `assert "\u0627\u0644\u0623\u0645\u064a\u0646" == AR`.
- **Differential render to prove a diacritic is drawn and where.** Render the word once with the
  diacritic and once without (e.g. with-hamza vs plain-alef), diff the two rasterisations, and check the
  difference sits at the expected position:

```python
arr = np.asarray(ImageChops.difference(img_with, img_without))
y, x = np.nonzero(arr > 60)
word_left, word_right = 321, 701          # from the ink bbox
frac = (x.mean() - word_left) / (word_right - word_left)
# RTL: the first letter is at the RIGHT. A hamza on the 3rd letter lands mid-word, near the top.
assert 0.5 < frac < 0.75 and y.mean() < 120
```

Report verification by the method used — "the string is exact and the hamza measures present at 63%
along the word" — not "the model says it looks right".

Vision remains useful for **composition** judgements it is good at: is the mark off-centre, is anything
clipped by the circle, does the colour read at small size. Take its *geometric* observations as leads to
check numerically, and take its *text* observations as noise.

## 4. The small-size gate is the real design review

An avatar must survive **40 px**, and ideally 28 px. Render the set at 200 / 112 / 64 / 40 / 28 px,
circle-cropped, into one contact sheet, and look at it. What fails there:

- **A Latin subtitle under the Arabic kills small sizes.** It steals vertical space, forcing the Arabic
  smaller. Ship the mark **pure** (calligraphy only) as the avatar, and hold the Latin lockup as a
  separate file for headers, banners and posters.
- **Thin calligraphic strokes disappear.** Fatten the glyphs deliberately with
  `-webkit-text-stroke: 5px <same colour as fill>` — invisible at 1024, decisive at 40.
- **Light grounds and dark grounds both need testing.** High contrast wins; the specific hue matters
  less than the contrast ratio. A cream ground with dark green type and a dark ground with pale gold
  type were the two survivors in practice.

Size the word by measurement, not by eye: render it at a reference size in the browser, read
`getBoundingClientRect().width`, and solve for the font-size that gives the target width (about 78% of
the canvas). A word with a ~2x width-to-font-size ratio needs roughly `font-size = target_width / 2`.

## 5. Deliverable set

Produce, at 1024 and 512 px, square with the circle inscribed so the platform's circular crop lands on
the ring:

1. **Primary avatar** — pure mark, best contrast, no Latin. Name it as the recommendation.
2. **One alternate ground** — light and dark so the user can match their platform theme.
3. **Lockup with the Latin name** — for headers and documents only, labelled as such.
4. **Contact sheet** — every variant at 200/112/64/40/28 px, so the choice is made on the small-size
   evidence rather than on the pleasing large render.

Deliver the contact sheet plus the recommendation. Do not send six near-identical files and ask which
one — name the pick and explain the evidence.

## Pitfalls

- Writing SVG without an `<svg>` wrapper. Silent total loss of the frame. Sample pixels.
- Trusting a vision model's reading of Arabic. It invents words and diacritic errors.
- Centring on the bounding box. Use the ink centre of mass.
- Only reviewing at large size. The 40 px render is the design review.
- Putting the Latin name under the Arabic on the avatar. It crowds the mark out at small sizes.
- Delivery files at 2048 px only. Telegram and most platforms want 512–1024; downscale with LANCZOS.
