---
name: subsurface-dossier-from-public-domain
id: subsurface-dossier-from-public-domain
version: 1.0.0-2026.09.22
owner: GEOX (arifOS)
risk_tier: medium
floor_scope: [F1, F2, F4, F7, F9]
description: "Build subsurface deliverables from public-domain sources."
autonomy_tier: T1
ecology_state: WARM
capability_tier: fed-agent-subagent
---

# Subsurface Dossier from Public Domain

The deliverable class this skill governs: anything an operator geologist asks for that would, in production, consume measured subsurface data (LAS curves, formation tops, TWT/MD). Built strictly from public-domain sources, with declared-gap accounting so the user can populate proprietary data on top.

## 1. Two Deliverable Modes Only

Pick exactly one; never the middle ground.

**Basemap mode.** Wells placed by Lat/Lon (block-centre approximation, never survey-tracked unless disclosed). Operator, block, role, source. No formation tops, no correlation tie lines. A numbered gap list declaring what is needed to upgrade to a cross-section.

**Framework mode.** Stratigraphic framework (e.g. Groups A–M, formations, depositional settings) drawn for each well column *without* correlation tie lines. The reader sees a column with the well's role and the basin position, but no depth values imply a measured tie.

> **Refuse mode.** When neither mode is appropriate, say so. State what is missing, name the source that resolves it, stop. Never ship the third option — extrapolated depths plotted as if measured.

## 2. Three Tests Before Drawing

1. **Per-well measured inputs.** Do you have, for every well, a logged formation-top table, an LAS file, or a survey-corrected wellhead Lat/Lon? If not for every well, the cross-section is partial. Stop and ask.
2. **Inter-basin fact.** Are all wells in the same basin / structural province as the stratigraphic source? A PM304 well (Central Malay Basin western flank) and an MTJDA well (North Malay Basin, MTJA-administered) cannot share a tie line. Their Group ages, source-rock kitchens, depositional settings and reservoir geometries diverge. The merge looks coherent; the science is wrong.
3. **Operator provenance.** Is each well tied to a public-record operator disclosure (PETRONAS release, WoodMac report, MTJA 40 YEARS, peer-reviewed biostratigraphy paper, regulator filing)? A well invented to fill basin coverage is a fabrication even when surrounding blocks are real.

## 3. The Math That Is Not Measurement

Three formulas the skill explicitly bans for any depth output:

- *nadir + tilt* — Group-F top = base ± smooth-sag envelope along the section axis.
- *distance-based interpolation* — between any two wells, depth is a linear-in-distance function of two endpoints.
- *Gaussian sag or normal envelope* — central deepening fit to a published "basin-centre deepest" sentence.

Each of these is the smoking gun in a measurement-vs-extrapolation review. Any depth produced by such a function is **DECLARED GAP**, not data.

## 4. Required Sections in the Deliverable

- A figure (basemap or framework) with source caption naming every public-domain data source.
- A **DECLARED GAPS** list (or equivalent). Numbered, source-disclaimered.
- A **Sources** block listing every URL/DOI; primary vs secondary classification.
- A **NOT a substitute** caption visible above or below the figure, naming the operator.
- A **Next steps** block enumerating data the operator must supply for a measured cross-section (datum shift, TWT→MD calibration, fluid contacts, sand-by-sand correlation).

## 5. Metric of a Basemap-Only Deliverable

A basemap-only deliverable is successful when:

- Every well marker has a public-record source URL.
- Block boundaries and operator mix are correct.
- No depth value appears in the figure for any well.
- Structural comments are stratigraphic-age or framework-depositional (literature-supplied), not depth-of-marker.
- The next-steps block is enough for a working geologist to know exactly what to send back to upgrade the deliverable.

## 6. Routine Pitfalls

- **Lumping PSAs** — different operators under one label. Each PSC operator must be named with a source.
- **Block-centre coordinates passed as survey coordinates** — Lat/Lon for the figure are block-group centroids; survey-corrected is a separate release.
- **A well named in conversation is not a well in a basemap.** If the operator cannot cite a public release, do not place the well in the figure.
- **Reported reserves written without year and as-at date** — every reserve number carries a vintage; cite both.
- **Re-using a figure caption that names a "Subcommittee" or "Working Group" without sourcing its membership.**
- **"Bid Round X" claims that aren't in the actual bid-round release.** PSAs from analysts are secondary; the operator release is primary.

## 7. Refusal Patterns

Refuse the deliverable when:

- The user asks for a tie line through two wells from different basins or PSC regimes without a measured source.
- The user asks for a single "representative" well column to be presented as actual well data.
- The user asks for stage pressures, fluid contacts, OWC/GOC, GDT or any quantitative reservoir number without a dated source.
- The user asks for a shale break thickness without logging evidence.

Refusals must be short, naming the missing data and the source that would resolve it.
