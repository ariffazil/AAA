# SVG Letterform Primitives

Reusable SVG fragments for rendering the letters A, I, R, F, N as geometry (not text).
Use when a monogram must contain specific letters at small accent sizes (12–24 px tall).

Coordinate system: each letter is centred at (0, 0) inside a `<g transform="translate(x,y)">`.
Stroke widths assume 1024 px canvas; scale proportionally for other sizes.

---

## I — vertical bar with top and bottom serifs

```svg
<rect x="-12" y="-130" width="24" height="220" fill="<colour>"/>
<rect x="-44" y="-138" width="88" height="14" fill="<colour>"/>
<rect x="-44" y="74" width="88" height="14" fill="<colour>"/>
```

- Total height: ~280 units (top serif to bottom serif)
- Stem width: 24 units
- Serif overhang: 32 units each side
- Render with `fill`, not `stroke`, so corners stay sharp at small sizes

---

## A — two slanted legs meeting at apex + horizontal crossbar

```svg
<line x1="-40" y1="0" x2="0" y2="-50" stroke="<colour>" stroke-width="14" stroke-linecap="round"/>
<line x1="40" y1="0" x2="0" y2="-50" stroke="<colour>" stroke-width="14" stroke-linecap="round"/>
<line x1="-26" y1="-22" x2="26" y2="-22" stroke="<colour>" stroke-width="10" stroke-linecap="round"/>
```

- Apex at (0, -50), legs spread to (-40, 0) and (40, 0)
- Crossbar at y=-22, ~52 units wide
- `stroke-linecap="round"` softens the apex tip

---

## R — vertical stem + top loop

```svg
<line x1="0" y1="0" x2="0" y2="48" stroke="<colour>" stroke-width="8" stroke-linecap="round"/>
<path d="M 0 0 L 18 0 C 30 0, 32 16, 18 22 L 0 22"
      fill="none" stroke="<colour>" stroke-width="8" stroke-linecap="round"/>
```

- Vertical stem 48 tall
- Top loop opens from (0, 0) → (18, 0) → curve out to (32, 16) → back to (18, 22) → (0, 22)
- The cubic Bezier `C 30 0, 32 16, 18 22` gives the rounded bowl

---

## F — vertical stem + top arm + middle bar (no bottom)

```svg
<line x1="0" y1="0" x2="0" y2="48" stroke="<colour>" stroke-width="8" stroke-linecap="round"/>
<line x1="0" y1="0" x2="22" y2="0" stroke="<colour>" stroke-width="8" stroke-linecap="round"/>
<line x1="0" y1="22" x2="16" y2="22" stroke="<colour>" stroke-width="8" stroke-linecap="round"/>
```

- Same stem height as R for visual alignment when side-by-side
- Top arm 22 wide, middle bar 16 wide (slightly shorter for proportion)

---

## N — left stem + diagonal + right stem

```svg
<line x1="0" y1="0" x2="0" y2="-30" stroke="<colour>" stroke-width="8" stroke-linecap="round"/>
<line x1="0" y1="0" x2="20" y2="-30" stroke="<colour>" stroke-width="8" stroke-linecap="round"/>
<line x1="20" y1="-30" x2="20" y2="0" stroke="<colour>" stroke-width="8" stroke-linecap="round"/>
```

- Two vertical stems 30 tall, connected by a diagonal
- This primitive draws an N oriented with the apex pointing up; rotate the
  enclosing `<g>` if you need a different orientation

---

## Combining into a monogram

Anchor each letter group with its own `<g transform="translate(x,y)">` so the positions are
independent. Example layout (I at centre, A on top, R/F/N on right):

```svg
<g transform="translate(256, 270)">              <!-- I at centre -->
  <rect x="-12" y="-130" width="24" height="220" fill="#fafaf5"/>
  <rect x="-44" y="-138" width="88" height="14" fill="#fafaf5"/>
  <rect x="-44" y="74" width="88" height="14" fill="#fafaf5"/>

  <g transform="translate(0, -100)">              <!-- A on top of I -->
    <line x1="-40" y1="0" x2="0" y2="-50" stroke="#ff7849" stroke-width="14" stroke-linecap="round"/>
    <line x1="40" y1="0" x2="0" y2="-50" stroke="#ff7849" stroke-width="14" stroke-linecap="round"/>
    <line x1="-26" y1="-22" x2="26" y2="-22" stroke="#ff7849" stroke-width="10" stroke-linecap="round"/>
  </g>

  <g transform="translate(56, -60)">              <!-- R upper-right -->
    <line x1="0" y1="0" x2="0" y2="48" stroke="#ff7849" stroke-width="8" stroke-linecap="round"/>
    <path d="M 0 0 L 18 0 C 30 0, 32 16, 18 22 L 0 22" fill="none" stroke="#ff7849" stroke-width="8" stroke-linecap="round"/>
  </g>

  <g transform="translate(56, 14)">               <!-- F lower-right -->
    <line x1="0" y1="0" x2="0" y2="48" stroke="#fafaf5" stroke-width="8" stroke-linecap="round"/>
    <line x1="0" y1="0" x2="22" y2="0" stroke="#fafaf5" stroke-width="8" stroke-linecap="round"/>
    <line x1="0" y1="22" x2="16" y2="22" stroke="#fafaf5" stroke-width="8" stroke-linecap="round"/>
  </g>

  <g transform="translate(60, 86)">               <!-- N tail -->
    <line x1="0" y1="0" x2="0" y2="-30" stroke="#4a5568" stroke-width="8" stroke-linecap="round"/>
    <line x1="0" y1="0" x2="20" y2="-30" stroke="#4a5568" stroke-width="8" stroke-linecap="round"/>
    <line x1="20" y1="-30" x2="20" y2="0" stroke="#4a5568" stroke-width="8" stroke-linecap="round"/>
  </g>
</g>
```

For letters other than A/I/R/F/N, prefer `<text font-family="...">` rendered at the target size
rather than hand-crafting geometry. The five letters above are the ones that come up often enough
to warrant primitives.

---

## Verifying

`vision_analyze` will report the closest plausible Latin glyphs from SVG primitives — not the
intended letters. To verify the SVG is correct, read the source directly. To verify the rendered
PNG matches the SVG, compute a hash of the rasterised pixels and compare to a previous render; the
SVG → rsvg pipeline is deterministic.
