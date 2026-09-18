# PIL text posters — build recipe

When: one-page, text-dominant flat graphic — architecture diagram, role/hierarchy
poster, cheat sheet, decision table rendered as an image. For paged documents use
`reportlab`; for photographic scenes use an image model.

PIL is a drawing library, not a layout engine. Everything HTML gives you free —
wrapping, right alignment, letter-spacing, collision detection — must be computed
explicitly. The recipe below is those computations.

## 1. Geometry first, content second

Fix canvas, gutter, type scale and row pitch as constants. Derive every y from a row
origin plus `i * ROW_H` so the grid is stable when you add or drop a row.

```python
W, H = 1600, 2300
L, R = 90, 1510          # left / right content edge
USABLE = R - L
ROWS_Y0, ROW_H = 578, 116

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FL = "/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)
```

Confirm the font paths exist before the first build — a missing font falls back
silently to an unreadable default and the render still exits 0.

## 2. The overflow check — the reason this file exists

PIL neither wraps nor raises. An overlong string silently runs off the canvas edge,
and you discover it only by looking. Measure instead, at build time:

```python
def check(label, text, font, maxw):
    w = d.textlength(text, font=font)
    if w > maxw:
        print("  !! OVERFLOW [%s] %.0f > %d :: %s" % (label, w, maxw, text[:60]))
    return w
```

Call it for **every** string with its true column width, not the full canvas:

```python
title  = "OpenClaw + HERMES for the arifOS Federation"
check("subtitle", title, f_sub, USABLE)
check("mand%d" % i, mandate, f_mand, R - (L + 92))   # indented column
```

A clean build prints `saved <path> (W, H)` and **zero** `!! OVERFLOW` lines. Treat a
printed overflow as a build failure: shrink the font, shorten the copy, or widen the
column, then rebuild. The vision pass is then a confirmation, not the detector.

## 3. Tracked and right-aligned text

PIL has no letter-spacing and no right-align. Both are five lines:

```python
def tracked_w(text, font, tr):
    return sum(d.textlength(c, font=font) for c in text) + tr * (len(text) - 1)

def draw_tracked(xy, text, font, fill, tr=0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tr
    return x

def right_tracked(x_right, y, text, font, fill, tr=0):
    draw_tracked((x_right - tracked_w(text, font, tr), y), text, font, fill, tr)
```

Use `draw_tracked` with a small tracking (`5–7` at display sizes) for eyebrow lines and
right-edge category tags; plain `d.text` for body copy. Right-aligned tags computed this
way never drift into the role names on their left.

## 4. Grid furniture

- Draw a separator between rows with `if i < len(rows) - 1:` — an unconditional rule
  leaves a dangling line under the last row.
- Draw the container rail (timeline spine, left accent bar) once, from the first row's
  centre to the last row's centre, not per row.
- Highlight one row by filling a rectangle *behind* it and painting the left accent bar
  after the fill; draw the text last so nothing overlays it.
- Hairline rule plus a small centred diamond as a section break:
  `d.line([(L, y), (R, y)], fill=GOLD, width=2)` then a four-point `d.polygon` centred at
  `((L + R) // 2, y)`.

## 5. Order of operations

1. Write the build script to a stable path in the work dir, never to the delivery name.
2. Run it. Read stdout: `saved … (W, H)` present **and** no `!! OVERFLOW`.
3. `file <out>.png` plus byte size — confirms it is a real raster and not a truncated write.
4. `vision_analyze` on the **shipped path**, asking it to (a) read every line back
   verbatim, (b) name any clipped, overlapping or colliding text, (c) confirm no line
   passes the right margin. The read-back is what catches semantic spill the measurement
   cannot — e.g. a section heading landing on the wrong block.
5. Fix, rebuild, re-verify. Ship only the passing build.

## 6. Content that trips screening gates

A build script whose *payload* touches screened variable classes can be refused at write
time, and the refusal message may not name the exact trigger. Do not burn turns hunting
it and do not re-shard the same payload to slip past. Separate concerns instead: keep the
renderer generic and put the copy in a data structure, so the drawing code carries no
prose at all. If it is still refused, re-ground the content or escalate — a gate on the
payload is a statement about the payload, not about the filename.
