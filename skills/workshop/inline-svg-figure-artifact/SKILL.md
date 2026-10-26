---
name: inline-svg-figure-artifact
description: "Use when a technical figure ships as inline SVG."
version: 1.0.0
author: HERMES
license: proprietary
tags: [figure, svg, artifact, verification, honesty]
risk_tier: low
autonomy_tier: T1
metadata:
  hermes:
    tags: [figure, svg, artifact, verification, honesty]
    related_skills: [self-contained-html-tool, geological-artifact-rigor, visual-artifact-delivery]
---

# Inline SVG Figure Artifact

A technical figure emitted as **SVG markup inside the deliverable HTML** — no matplotlib, no PNG,
no chart library. Crisp at any zoom, printable, and interactive (hover or tap a region, a fixed
detail card updates). This is the right shape when the reader will *interrogate* the figure rather
than just look at it, and when the page must survive being forwarded and opened offline.

Route elsewhere when the shape differs: matplotlib for dense scientific plots and multi-panel
figures (`geological-artifact-rigor` → `references/cross-section-generation.md`); SVG-rendered-to-PNG
via Playwright when the figure must travel as an image attachment
(`references/svg-cross-section-generator.md`); a filterable data table is `self-contained-html-tool`,
not this skill.

## 1. Fix the measured set before drawing anything

Write down the numbers the source actually publishes. That list is the figure's entire factual
spine, and it is usually short — for a field cross-section it might be water depth, field length
and width, maximum fault throw, zone count, and which block each platform develops.

Everything the drawing needs beyond that list is **framework**: fault positions, dip sense,
closure shape, contacts, and every depth below a datum. Framework is legitimate. Framework drawn
as if measured is the defect this skill exists to prevent.

## 2. State the measured set inside the figure, not only in the caption

The caption is read second, if at all. Put the honesty furniture in the plot area at figure scale:

- A stamp: `SCHEMATIC — NOT SURVEYED / NOT MEASURED` (name what it is *not*).
- Orientation: end labels (`W`/`E`) plus one line naming the section and what it is perpendicular to.
- A true-unit scale bar for the horizontal axis, and the exaggeration factor printed.
- Every schematic quantity labelled as such where it is drawn — `contacts schematic` on the contact
  itself, not in a footnote.
- No axis value where the source publishes none.

The caption then itemises the two lists: measured (with numbers) and schematic (named one by one).

## 3. Two scales, one computed exaggeration

Set horizontal and vertical metres-per-pixel independently, then compute the factor explicitly:

```python
M_PER_PX_X = W_M / (X1 - X0)
M_PER_PX_Z = 1 / PX_PER_M_Z
VE = M_PER_PX_X / M_PER_PX_Z     # horizontal m/px DIVIDED BY vertical m/px
```

Inverting that division silently reports an exaggeration below 1, which is not a section — it is a
flattened caricature, and the practitioner in the audience notices before they read a word. Print
`VE` in the figure and sanity-check that it is plausible for the subject (a few units, not 0.7).

## 4. Boundaries that are not ruled, and not random

A smooth analytic shape plus a small **deterministic** wobble reads as geology; straight lines read
as a diagram, and per-render randomness means two builds of the same figure cannot be compared.

```python
def crest(x, crest_x, half):
    u = abs((x - crest_x) / half)
    return 0.0 if u >= 1 else 0.5 * (1 + math.cos(math.pi * u))

def wobble(x, seed):                 # +-6 m, reproducible for a given seed
    return 6.0 * math.sin(x / 300.0 + seed * 1.7) + 3.0 * math.sin(x / 91.0 + seed)
```

Decay amplitude with depth so deeper horizons flatten relative to shallower ones — correct for
compaction-driven and late-fold settings, and it stops the figure reading as concentric copies of
one curve.

## 5. Displacement means separate polygons

To show a fault, **split the x range into blocks, leave a gap either side of the fault, and emit
each unit once per block with a per-block vertical offset.** A single polygon with a line drawn on
top of it reads as a line *on* the geology, not as displacement — the commonest tell that a section
was drawn rather than thought about. Use the published throw as the offset magnitude and state the
sense where it is schematic.

## 6. Labels that survive any fill

Halo every label instead of computing a per-region background colour:

```html
<text paint-order="stroke" stroke="#0f1a23" stroke-width="3.2" fill="#dce7ef">Group F · seal</text>
```

That one attribute pair replaces stratum-aware bbox logic and works over flat fills, hatching and
gradients alike.

- **Thin bands never carry their own label.** Put group names in a left label column outside the
  plot area, `text-anchor="end"`, with a thin leader tick into the band.
- **Stagger callout leaders.** Three callouts at one x always collide; give each a different
  horizontal offset and label length, and re-check after any coordinate change.
- **A short tick plus a haloed label** beats a leader dragged across the whole figure.

## 7. Interactivity that earns its place

Put the region key on the geometry (`data-k` on each path) and have one handler write into a fixed
detail card elsewhere on the page. The figure then answers "what is that band" without the reader
scrolling to a legend — and it degrades to a readable static figure if JS never runs.

## 8. Visual QC — element-clipped screenshots, then eyes

Do not screenshot the whole page and squint. Clip to the figure element, at device scale, using
**absolute page coordinates** (add `window.scrollY`), and pass `scale` explicitly — the CDP call
rejects a clip missing it:

```python
info = json.loads(js("""(() => { window.scrollTo(0,0);
  const r = document.querySelector('#fig').getBoundingClientRect();
  return JSON.stringify({x:r.x, y:r.y+window.scrollY, width:r.width, height:r.height, scale:2}); })()"""))
res = cdp('Page.captureScreenshot', format='png', clip=info, captureBeyondViewport=True)
open(path,'wb').write(base64.b64decode(res['data']))
```

Then ask the vision pass a **defect question**, not a description question — "any overlapping
labels, clipped annotations, illegible text on dark fills, collisions between markers and lines" —
and require a concrete list. A description question returns a confident summary of intent and
misses exactly the collisions you are hunting. Two to four patch-and-recapture rounds is normal;
never ship the first render.

Cheap independent checks worth running too: every path's `getBBox()` inside the `viewBox` (catches
geometry drawn off-canvas), the interaction handler writing real text into the detail card on click,
and `document.documentElement.scrollWidth == clientWidth` at 390 px wide.

## 9. Pre-delivery checklist

1. Measured set listed in the caption, with numbers.
2. Stamp inside the figure naming what it is not.
3. Exaggeration computed the right way round and printed.
4. No value on an axis the source does not publish.
5. Faults drawn as block gaps with offsets, not as lines over a continuous surface.
6. Every label haloed; no label inside a thin band; no two callouts sharing an x.
7. Scale bar in true units, orientation stated.
8. Visual QC passed at element clip; nothing clipped at the panel edge.
9. Mobile width gate passed; the generator script kept beside the artifact so the next revision is a
   re-run rather than a hand-edit.

## Reference

- `references/geological-section-and-plan.md` — worked generator for a structural cross-section plus
  plan map inside one HTML file: coordinate model, per-block horizon paths, halo labels, honesty
  furniture, and the QC questions that found real defects.
