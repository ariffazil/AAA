# Image Overlay Annotation Pattern

Recipe for overlaying interpretation markers on a user-supplied photo (seismic
sections, financial charts, x-rays, screenshots). The user is the domain expert —
your job is to lay down GENERIC interpretation markers visually without
claiming professional interpretive authority.

Use when: a domain expert shares a screenshot of their work (geologist shares a
seismic section, trader shares a chart, doctor shares an x-ray, designer shares
a mockup) and asks for "annotations" or "interpretation" drawn on top.

## The fundamental split

You draw visual markers that communicate "this is what someone might look at
in this region." You do NOT draw a real professional interpretation.

The artifact is for visual reference (conversation prompt, slide placeholder,
template starter). It is NOT a deliverable for submission to a client, regulator,
or peer review. State this in a visible disclaimer on the artifact.

## Color and symbol convention (generic, domain-agnostic)

Use a small, consistent palette. Each color represents a CATEGORY, not a specific
feature — the user overlays domain labels themselves.

```python
# Generic interpretation palette (works for seismic, financial chart, x-ray)
PRIMARY_RESERVOIR_TOP   = '#ff9500'   # orange — main target / primary level
SECONDARY_HORIZON      = '#ff3b3b'   # red — other levels
DEEP_LEVEL              = '#7a7aff'   # blue dashed — secondary / background
FAULT_LINE              = '#ff00ff'   # magenta — discontinuity, with tick-marks
STRUCTURAL_FEATURE      = '#00ff00'   # green dashed — possible closure / anticline
GOLD_ACCENT             = '#a8884a'   # title / legend / disclaimer border
TEXT                    = '#f5f0e1'   # light cream (on dark backgrounds)
DIM                     = '#cccccc'   # secondary text
```

Choose these because they survive vision OCR — orange and red stay
distinguishable after PNG compression; magenta is unmistakable against
grayscale backgrounds.

## The Y-flip trap (matplotlib vs image coordinates)

**Vision reads PNGs in image-native coordinates (origin top-left, Y increases
downward). Matplotlib's default `ax` has Y increasing upward. When you display
an image via `ax.imshow()` AND overlay text via `ax.text()`, the two coordinate
systems disagree silently.**

Three viable fixes; pick one and be consistent:

**Fix A — flip the axis once after plotting everything:**
```python
ax.set_ylim(ax.get_ylim()[::-1])  # flip matplotlib Y to match image
```

**Fix B — flip only the text positions when you plot them:**
```python
# If image height is H, place text at y_pixel directly (not flipped)
ax.text(x, y_pixel, label, ...)  # where y_pixel is 0..H measured top-down
```

**Fix C — use `origin='lower'` on imshow:**
```python
ax.imshow(img, origin='lower')   # image Y grows up, matches matplotlib
# BUT: image content appears flipped vertically. Don't use this unless
# the image itself doesn't matter orientationally.
```

**Pitfall:** Setting `ax.set_ylim(H, 0)` (the inverse form) is tempting because
it feels like "flipping", but it only flips the DATA view, not the text
rendering coordinate system. Vision will see the image right-side-up but your
"top" title text will appear at the BOTTOM in vision's read because vision
reports positions in image-native coordinates. Three re-renders converged on
this exact defect in the seismic annotation pass — fix it ONCE and verify
with the vision checklist below.

## Annotating over a user-supplied chart

When the user provides a chart screenshot, **do not invent coordinates**. The
image has its own axes, scale bars, label positions. Anchor markers to
visible features:

1. **Read the visible scale first** (depth labels on a seismic section,
   price labels on a financial chart, etc.).
2. **Convert visible-position → image-pixel coordinates** by visual
   inspection of the image (since you cannot read the underlying data).
3. **Annotate in image-pixel space**, not data space. The artifact is
   visual; precision comes from the user's later professional overlay, not
   from your marker placement.

If the user provides the image WITH overlaid labels (well markers, etc.),
read THOSE labels with vision first. They are ground truth. Don't second-
guess them.

## Past candles / past events in the image

If the image has historical reference (left half of a chart, earlier scan in
a medical sequence, prior page in a doc), draw **only on the user's present
view**, not on the historical reference. The historical reference is fixed;
your annotations should be additive on top of the current view.

```python
# Annotation zone vs reference zone
annotation_zone = (0.55, 1.00)  # x-range for your markers (right half)
# Don't draw horizon/fault/annotation lines through the past/reference zone
# unless the user explicitly asks for overlay across both.
```

## Tick-marks on discontinuity lines

When annotating a fault line or break, add small horizontal tick-marks at
intervals along the line. This is a universal geological convention that
also reads as "discontinuity" in chart annotations.

```python
for ty in [y_top + 0.05*H, (y_top+y_bot)/2, y_bot - 0.05*H]:
    ax.plot([x - 5, x + 5], [ty, ty], color=color, lw=2, zorder=5)
```

Three tick-marks per line is the standard convention. Two looks
accidental; four looks decorative.

## Structural closure (anticline, channel, basin) ellipse

When annotating a possible structural feature (anticline in geology, channel
in finance, lesion in medical imaging), use a dashed ellipse outline. The
dashed style communicates "interpretation, not data". A solid ellipse claims
the feature is real; a dashed ellipse says "this is what someone would
highlight as worth investigating."

```python
from matplotlib.patches import Ellipse
ell = Ellipse(xy=(cx, cy), width=W, height=H,
              fill=False, edgecolor=STRUCTURAL_FEATURE,
              linewidth=2.5, linestyle='--', alpha=0.8)
ax.add_patch(ell)
```

Place the label ABOVE the ellipse with a small vertical offset, not inside
the ellipse. Inside-label clutters the shape and reads as redundant.

## Disclaimer is mandatory

Every interpretation overlay artifact MUST carry a visible disclaimer. Suggested
template (modify for domain):

> "Generic visual overlay · For [user] visual reference only · Real
> interpretation by [user title] ([user expertise])"

Place the disclaimer in a non-overlapping corner with a thin gold border.
The disclaimer is non-negotiable because it shifts interpretive authority
back to the user, where it belongs.

## Vision-verify checklist (specific to overlay-on-photo)

```python
# Generic checklist — append domain-specific questions
[
    "1. Is the original image visible as background (not over-saturated or covered)?",
    "2. Are the annotation colors distinguishable from each other AND from the image background?",
    "3. Are the annotation lines CONFINED to the user's region of interest (not extending across the whole image)?",
    "4. Is the title visible at the TOP of the artifact (not bottom)?",
    "5. Is the legend visible AND not overlapping the image?",
    "6. Is the disclaimer visible AND readable?",
    "7. Is there any text the model hallucinated that wasn't in your script (extra words, garbled characters)?",
]
```

Question 7 is the catch-all. AI image generators will sometimes hallucinate
text, but matplotlib text won't — so if vision reports "label X exists" and
you didn't write it, that's a real bug to investigate (often a coordinate
collision producing glyph overlap).

## What this pattern is NOT

- **Not** a substitute for the user's professional work. A seismic overlay
  does not let you publish geological findings. The disclaimer exists because
  the artifact is a CONVERSATION PROMPT, not a deliverable.
- **Not** a single-pass generator. Two to three vision-verify iterations are
  normal. The pattern that converges fastest is: write → vision-check → fix
  → repeat, with each vision prompt asking 3-5 specific layout questions,
  not a generic "describe the chart".
- **Not** universal across all domains. Geological horizons → financial
  support/resistance → medical anatomy → UI mockup annotation. The
  convention stays (color-coded markers, dashed = interpretation, solid =
  measurement, disclaimer mandatory), the SPECIFIC colors and shapes
  change. When in doubt, ask the user what categories to mark.

## Verified failure modes (as of 2026-09-25)

- 3 re-render cycles needed to converge on a seismic annotation due to the
  matplotlib Y-flip issue (vision read image in image-native coordinates,
  report said "title at bottom" when it was at top in matplotlib's frame
  but bottom in image coordinates). Fix once with `set_ylim(yl, yh)` where
  `yl > yh` for top-down image space — but verify with vision-verify on
  each render.
- Vision reading "PRADDICEOL" or similar gibberish indicates two header
  strings placed at the same x-coordinate. Fix by separating column
  positions by at least 11 units when in a 0-54 x-space.
- Annotations extending past x_right=0.95 of image width create the
  illusion that the line "goes forever". Constrain annotation x-range to
  `0.05*W to 0.95*W` to leave margin.


## Seismic-specific horizon geometry

When the user-supplied photo is a **seismic section** (interpreted by a
geoscientist), the pattern above applies AND an additional geometry rule
binds:

**Railroad-track horizons = wrong.** A V1 overlay that draws H1, H2, H3,
H4 as equispaced flat horizontal lines across the section will be
rejected as bangang (stupid) by any geologist. Real reflectors:

- Have **variable vertical spacing** — inter-horizon gaps expand or
  compress along the section, not constant.
- Have **wavy geometry** — they follow structural dip, anticline crests,
  syncline troughs, fault offsets. A flat line implies a non-deformed
  layer, which contradicts the rest of the section if any structure is
  visible.
- Have **variable amplitude** — bright/dim bands. Horizon lines drawn
  on top should at minimum respect the visible curvature; better, they
  should sit on top of actual peak/trough picks.

Build horizon y-positions from a sampled list, not from a formula:

```python
# BAD — railroad tracks
horizons = {
    'H1': 0.30 * H,
    'H2': 0.45 * H,
    'H3': 0.60 * H,
    'H4': 0.75 * H,
}

# GOOD — variable spacing + structural curvature
horizon_H2 = [
    (x0, 0.52*H), (x0 + 0.2*W, 0.45*H), (x_mid, 0.40*H),  # crest at center
    (x_mid + 0.2*W, 0.45*H), (x1, 0.55*H),                # flank dips
]
horizon_H3 = [
    (x0, 0.65*H), (x0 + 0.2*W, 0.58*H), (x_mid, 0.55*H),
    (x_mid + 0.2*W, 0.58*H), (x1, 0.68*H),
]
# H3-H2 spacing TIGHT at crest, WIDER at flanks — geological realism
```

For plots that require actual structural picks, prefer the GEOX organ
(`mcp__geox__geox_seismic_interpret` mode `classical_section` or
`interpret_section`) — it returns a candidate ensemble with P10/P50/P90
depth bands. The matplotlib overlay then visualizes GEOX's
QUALIFIED_CANDIDATE output, NOT a hand-drawn graphic. Per the GEOX
zen: image-only input caps `seal_eligibility = false`; the overlay
artifact is conversation prompt only, not a SEAL-able structural
framework.

Vision-verify question for seismic overlays: *"Do the horizon lines
look like railroad tracks (equally spaced parallel lines), or do they
have variable spacing and follow the section's structural curvature?"*
If railroad tracks, the overlay is not domain-acceptable. Re-sample
horizons from the visible reflectors and re-render.
