---
name: figure-annotation-verification
version: 1.0.0
description: "Use when a figure's glyphs may contradict its data."
owner: HERMES
risk_tier: low
floor_scope: [F1, F2, F4]
autonomy_tier: T1
tags: [figure, svg, annotation, chart, cross-section, verification, dom, geology]
---

# Figure Annotation Verification

An annotation on a figure is a claim. "Extension here", "thickest crust", "peak value",
"boundary" — each asserts something about the data underneath. Most figure defects are not
style defects: they are annotations the drawn geometry contradicts, placed by eye rather than
measured.

Applies to SVG cross-sections, charts, infographics, posters, and any HTML/PDF surface where an
author drew a glyph on top of data.

## Rule 0 — moving a glyph is not a fix until the coordinate system is known

Before relocating anything, establish three facts **from the source**, never by eye:

1. What the x-axis encodes (distance, index, latitude, or decoration) and its units.
2. Where the axis starts and ends, and the plot bounds used to map data to screen.
3. Where every relevant annotation currently sits, as a fraction of plot width.

"Move it to the middle-right" is not a specification: it changes meaning with window width.
Convert any request in those words to a percentage range before editing, and state the percent
in the report — otherwise the before/after comparison is opinion.

## Step 1 — read the coordinate transform out of the source

Most figure pages carry an explicit mapping. Find it before measuring anything:

```bash
grep -nE 'const (X|Y|W|L|R|KM|scale)|function (X|Y)\b|viewBox' page.html | head
```

A typical shape is `X = km => L + km / KM * (W - L - R)`, which yields both the data→pixel map
and the plot width `W - L - R`. With that, every annotation converts to a percentage. Record the
constants — they are what makes the finding checkable by someone who never opens the file.

## Step 2 — measure the rendered result, not the source numbers

The source says what was intended. The DOM says what shipped — after variant switching, dynamic
redraws, and de-collision code. Measure the DOM:

```python
js("""(() => {
  const svg = document.querySelector('#xs');
  const T = [...svg.querySelectorAll('text')].map(t => ({
    t: t.textContent.trim(),
    x: +t.getAttribute('x'), y: +t.getAttribute('y'),
    w: t.getComputedTextLength ? t.getComputedTextLength() : 0
  }));
  return JSON.stringify(T);
})()""")
```

Convert `x` to percent using the bounds from Step 1 and print a sorted table:

```
28%  Moho
45%  Moho not constrained 230-540 km
65%  Moho 32 km (thickest)
79%  mantle uplift (inferred)
```

**Re-measure after every model/tab switch.** A page with four selectable variants renders four
different annotation sets from one script; one measurement describes one of them. Loop the
variants and record each.

## Step 3 — collision check, not eyeballing

```python
hit = lambda a, b: not (a['x']+a['w']/2 < b['x']-b['w']/2
                        or b['x']+b['w']/2 < a['x']-a['w']/2) \
                    and abs(a['y']-b['y']) < 14
```

Report `collisions: none` explicitly, or list the pairs. A label placement that reads fine at
desktop width collides after a mobile override — measure both (`Emulation.setDeviceMetricsOverride`)
before declaring the figure clean. Also assert
`document.documentElement.scrollWidth <= window.innerWidth + 1`, which catches the horizontal
scroll a moved glyph introduces.

## Step 4 — semantic consistency: the glyph against the geometry under it

This is the defect class that survives every style review. Check each annotation against the
data it sits on:

- An arrow asserting **thinning** drawn where the section shows its **thickest** layer.
- A **peak** or **maximum** label over a trough on the same axis.
- A **boundary** label at a position the data shows no boundary.
- A **direction** arrow pointing opposite to the numbers in the table beside it.

Extract the geometry arrays (polyline points, series values) alongside the annotation list, then
compare the annotation's stated property against the local value at its x. When they disagree,
the fix is usually to **delete** the glyph, not move it — a semantic contradiction does not
become true by relocating.

**Never invent missing data to satisfy a label.** If the source has no constraint over a span
(a gap between measured segments), the honest annotation is `not constrained <range>`. Drawing
an interpolated curve to justify a glyph converts a known unknown into a fabricated fact.

## Step 5 — state the time slice before changing process symbols

Arrow glyphs that encode *process* (extension, uplift, flow, erosion) also encode *when*. A
section drawn as present-day geometry with a process arrow on it asserts the process is active
now — a new claim, not a visual correction. Establish and record:

- Present-day slice, or a named interval?
- Are the ages on the figure history (an event bar) or a live state?

Unknown means write UNKNOWN and stop. Moving a symbol that should not exist is the same error at
a different coordinate.

## Step 6 — verify the deployed surface, and prove the old string is gone

Editing the repo does not change what a browser receives. After deploy, fetch the live URL with
a cache-buster and assert both directions:

```bash
curl -s "https://<host>/<path>?cb=$(date +%s)" | grep -c '<new string>'   # expect >=1
curl -s "https://<host>/<path>?cb=$(date +%s)" | grep -c '<old string>'   # expect 0
```

Then re-run Steps 2 and 3 against the **live** page at two widths. "Fixed in the source" is not
a delivered fix.

## Pitfalls

- **Judging placement from an image you cannot measure.** With no vision lane, say so and stop —
do not narrate positions you did not read.
- **Treating the caption as the fix.** Prose saying "extension is drawn in the centre" does not
correct a misplaced glyph; it documents the disagreement. Change the glyph or delete it.
- **Asssuming an existing annotation is correct because it shipped.** The prior edit may have
been a guess. Measure before preserving.
- **Trusting a backup over the live page.** Web root, build directory, and repo checkout can all
disagree. Confirm the served bytes.
- **Publishing a before/after without the numbers.** "Now it is in the right place" with no
percent-of-width pair is unfalsifiable and gets re-litigated next session.
- **Deleting a glyph and saying nothing.** A removed process symbol changes the figure's claim;
name what was removed and why, in the same breath as what was added.
