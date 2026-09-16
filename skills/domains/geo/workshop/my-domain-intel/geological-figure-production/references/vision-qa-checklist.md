# Vision-Driven QA Checklist — Geological Figures

Use this checklist when running `vision_analyze` on each figure PNG. After each call, mark items as PASS / FAIL and route to fix-and-re-render.

## Universal checks (every figure)

- [ ] **Title visible** at top, in expected color (gold `#f0a500` for GEOX), no clipping
- [ ] **Axes labeled** with units (km, m, Ma, %, Ro %) — never bare numbers
- [ ] **Legend readable** if present — no text inside colored squares
- [ ] **Caption / epistemic tag** present at bottom or in figure description
- [ ] **All plotted elements visible** — no NaN-driven gaps, no missed layers
- [ ] **Color contrast** adequate on dark background — light text on dark fills

## Per-figure specific

### Strat Column (Fig.1 in Senegal set)

- [ ] Each row readable — period | age | formation | lith swatch | thickness | role | notes
- [ ] No row overlap (rebuilt with evenly-spaced Y if any two units share age_top)
- [ ] Lithology swatch labels visible as readable words (SAND, SS, MARL, LS, SH, EVAP, BAS) — not raw hex codes
- [ ] Period grouping visible on left
- [ ] Title and attribution outside the table

### Cross-Section (Fig.3)

- [ ] Seabed profile visible — not flat, not broken (NaN-safe curve)
- [ ] All 6-8 stratigraphic layers visible and stacked in correct order
- [ ] Salt diapir present (where applicable) — translucent polygon, labelled
- [ ] Growth faults solid orange/red lines with labels
- [ ] Discovery star markers visible — Sangomar, Tortue, etc.
- [ ] Source kitchen indicator visible with label
- [ ] Migration arrows visible (dashed or curved lines)
- [ ] Domain labels at top (Coast, Shelf, Slope, Deepwater)
- [ ] Scale bar at lower-right
- [ ] Vertical exaggeration called out in caption

### Burial History + Ro (Fig.2)

- [ ] Both panels present with twin-axis layout
- [ ] Burial curve monotonic-increase from basement at depth to seafloor at top
- [ ] All horizon points marked with colored scatter dots and labels
- [ ] Phase bands (RIFT / THERMAL SUBSIDENCE / CENOZOIC DRIFT) distinguishable
- [ ] Ro curve monotonic-increase with depth
- [ ] Oil window (Ro 0.6-1.2) shaded in orange/amber
- [ ] Gas window (Ro >1.2) shaded in deeper amber
- [ ] Immature zone (Ro < 0.6) shaded green
- [ ] Reference horizon Ro values labelled (e.g., "Top Jurassic ~Ro 1.15")

### Block Map (Fig.4)

- [ ] Basin orientation correct (Senegal = WNW-ESE, not vertical strip)
- [ ] Coastline visible and curves naturally
- [ ] Water depth contours parallel to coast (not crossing it)
- [ ] PSC block polygons distinguishable from each other (different colors)
- [ ] Block labels centered in polygons, not overflowing
- [ ] Wells plotted as triangles with year labels (e.g., SNE-1 2014)
- [ ] Country labels positioned south of coast
- [ ] North arrow + scale bar in margins
- [ ] Atlantic Ocean / sea label present if offshore block map

### Risk Heatmap (Fig.5)

- [ ] Quadrant shading visible (red = critical, orange = warn, green = low)
- [ ] X-axis = Probability, Y-axis = Severity
- [ ] Axis tick labels meaningful (Very Low / Low / Medium / High / Very High; Negligible / Minor / Moderate / Major / Severe)
- [ ] All 7 risk bubbles visible, no exact-overlap
- [ ] Labels readable — use leader lines to margin if central region congested
- [ ] Risk register table at bottom lists all 7 risks with ranks

### Events Chart (Fig.6)

- [ ] Time axis runs from past (left) to present (right) — or inverted if conventional
- [ ] All 8-10 PSM element bars visible
- [ ] Trap-formation-predates-migration line annotated
- [ ] Exploration milestones at top with gold/orange scatter markers
- [ ] Era labels (RIFT / DRIFT / PASSIVE MARGIN) readable at bottom

### Discovery Timeline (Fig.7)

- [ ] Year axis spans 2014-2026 with ticks
- [ ] Bubble size matches resource estimate
- [ ] Color-coded by hydrocarbon type (oil/gas/mixed)
- [ ] Three era bands shaded (EXPLORATION / APPRAISAL / DEVELOPMENT)
- [ ] First Oil and First Gas lines clearly marked
- [ ] Major wells (SNE-1, Tortue-1, Yakaar-1, FID) labeled with resource annotations

## After QA

For each FAIL item: route to fix-script, re-render only that figure, re-run QA on that figure only (not all 7).

Do NOT re-render whole deliverable for one figure — incremental saves time and tokens.
