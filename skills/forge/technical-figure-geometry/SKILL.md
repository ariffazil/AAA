---
name: technical-figure-geometry
description: "Use when a figure annotation's placement is disputed."
version: 1.0.0
owner: HERMES
risk_tier: low
tags: [figure, cross-section, annotation, svg, measurement, geology, chart]
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Technical Figure Geometry

For any figure that carries an axis and annotations on it — a geological cross-section, a chart, a
schematic, an engineering section — the question "is this label in the right place" is a
measurement, not an opinion. This skill is how to measure it, fix it, and prove the fix.

Triggers: "move that to the middle-right", "the arrow is at the wrong boundary", "this doesn't
match reality", "a geologist should be able to tell at a glance", or any request that a peer agent
reviewed and returned as unmeasurable.

## Core law

**A position described in words is not a specification.** "Middle-right", "around the boundary",
"obviously wrong at a glance" have no pass condition. Convert every complaint into a percentage of
the plotted axis before touching anything, and report the result the same way.

Corollary: a reviewer with no vision and no fetch capability cannot adjudicate placement. If the
page or file is reachable to you, measure it and answer with numbers — do not adopt their
estimate, and do not argue with it either.

## Step 1 — recover the axis mapping from the source

Never estimate the axis from a screenshot. Almost every programmatic figure defines the mapping in
one line; find it and reuse it verbatim:

```js
const W = 1480, L = 74, R = 26, KM = 833;
const X = km => L + km / KM * (W - L - R);      // axis -> pixel
```

Then define the percentage basis once and use it everywhere:

```python
pct = lambda v: (X(v) - L) / (W - L - R) * 100      # % of PLOT width, not page width
```

Two different denominators (page width vs plot width) will silently disagree by a few percent and
make a correct fix look wrong. Fix the basis in writing in the report.

## Step 2 — tabulate every annotation, before and after

Produce one table per revision, identical shape, so the diff is a number:

```
label                          km      % width   depth km
Moho 32 km (thickest)          545      65        40
mantle uplift (inferred)       660      79        34 -> 52
```

Pull the values from the rendered DOM, not from the source text — renderer defaults, label
anchors and auto-offsets move the ink:

```js
[...svg.querySelectorAll('text')].map(t => ({ t: t.textContent.trim(),
  x: +t.getAttribute('x'), y: +t.getAttribute('y'),
  w: t.getComputedTextLength() }))
```

## Step 3 — check for collisions and overflow, in the same pass

A correct position that overlaps another label is still a defect, and it is the one a text-only
review cannot see. Two annotations collide when their horizontal extents overlap **and** their
baselines are within roughly one line height:

```js
const hit = (a, b) =>
  !(a.x + a.w/2 < b.x - b.w/2 || b.x + b.w/2 < a.x - a.w/2) && Math.abs(a.y - b.y) < 14;
```

Report collisions as a list of pairs, `none` when empty. Also assert the figure does not overflow
horizontally at the narrowest delivery width:

```js
document.documentElement.scrollWidth <= window.innerWidth + 1
```

Measure at desktop **and** a mobile viewport (`Emulation.setDeviceMetricsOverride`); a figure that
places correctly at 1440 px and collides at 390 px is not fixed.

## Step 4 — cache-bust before believing any measurement

A re-measure after a fix routinely reports the *previous* geometry: the browser served a cached
document, or the served file is not the file you edited. Both produce a confident, wrong reading —
in either direction.

```python
goto_url(f"{path_or_url}?cb={int(time.time())}")
wait_for_load(); js("location.reload(true)")
```

Then reconcile the three states explicitly, because they drift:

| State | How to check |
|---|---|
| working file | the path you edited |
| served file | `curl` the live URL, `grep` for a string you just introduced |
| rendered DOM | the measurements above |

A webroot copy that is byte-different from the source tree is the normal cause of "my fix did not
take". Diff the two, copy, and re-probe — do not reload a proxy or purge a cache for this; the
static file is simply a second copy.

## Step 5 — the semantic gate: annotation vs geometry

Placement being measurable does not make it *true*. Before accepting any annotation, read the drawn
value underneath it:

- **An annotating glyph must not assert a process over geometry that contradicts it.** A
  "crustal thinning" arrow drawn across the thickest section, or an "uplift" arrow over a deepening
  basin, is a label-vs-geometry contradiction — and it survives review because the label and the
  shape are each checked separately. Query the geometry under the arrow before shipping it.
- **A label naming two mechanisms makes the reader draw them in one place.** If the name bundles
  processes that the figure separates by depth or domain (a tectonic style plus a mechanism), split
  the naming in the caption even when the model name is a published attribution you must not change.
- **Absent datum → label the gap, never invent the shape.** When the constraint is missing from the
  data (a boundary that is not imaged over 300 km, a value with no source), draw the gap and label
  it — `not constrained 230–540 km` — rather than interpolating a plausible curve. An invented
  reference datum is worse than a visible blank, because the next reader cannot tell which is which.
- **State the time basis.** A cross-section or chart mixes present-day geometry with historical
  events on an adjacent axis; say which is which in the caption. A glyph that implies an active
  process on a present-day slice is a new claim, not a cosmetic correction.
- **An inferred mechanism belongs in the caption, not as a drawn arrow**, unless the figure has a
  visual convention for inferred vs observed. Prefer "inferred" in the annotation text over a
  second colour the legend does not explain.

## Step 6 — re-measure and report numbers

Close with: the new table, `collisions: none|list`, the overflow check at both widths, and the
live-URL confirmation that the retired string is gone and the new one is present:

```bash
curl -s "$URL?cb=$(date +%s)" | for s in 'new label' 'old label'; do printf '%-24s %s\n' "$s" "$(grep -c "$s")"; done
# new=1, old=0
```

"Should be fixed now" is not a receipt. Percentages and grep counts are.

## Pitfalls

- **Measuring from a screenshot or from the source text.** The screenshot is downscaled and cropped;
  the source does not contain renderer offsets. Read the DOM.
- **Using page width as the percentage basis.** A figure with a 60 px left gutter makes "40 % of page"
  mean "34 % of plot", and the fix lands outside the intended domain.
- **Trusting one viewport.** Desktop-only verification misses the collision class entirely.
- **Re-measuring without a cache-bust.** Reports the old geometry with full confidence.
- **Editing the source tree and declaring the live page fixed.** Check the served copy; on static
  hosts there is often a second copy under the webroot.
- **Moving a glyph to satisfy a reviewer without checking the data underneath it.** The complaint can
  be right about the position and wrong about the mechanism; the fix is only correct if both hold.
- **Filling a gap in the geometry to make the figure look complete.** Label the gap.
- **Deleting an annotation that named an unsupported claim without leaving a trace of why.** If the
  model legitimately keeps the claim, move the claim to the caption where it can carry "inferred";
  deleting it silently loses the argument the figure was making.

DITEMPA BUKAN DIBERI
