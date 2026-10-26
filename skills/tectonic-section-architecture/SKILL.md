---
name: tectonic-section-architecture
description: "Build tectonic cross-sections that survive review."
version: 1.0.0
owner: HERMES
author: hermes
license: proprietary
risk_tier: low
floor_scope: [F2]
autonomy_tier: T1
tags: [geology, cross-section, tectonics, provenance, sabah]
metadata:
  hermes:
    tags: [geology, cross-section, tectonics, provenance]
    related_skills: [generated-scientific-artifact-audit, geological-artifact-rigor]
---

# Tectonic Section Architecture

> A structural cross-section of an active margin answers "what sits under the unconformity and why".
> A generator that only stacks strata will answer a different question, confidently, and wrong.

## When to Use

Producing or repairing a structural cross-section, basin panel, or multi-model crustal figure for a
collisional or active margin. Companion to `generated-scientific-artifact-audit` (how to audit one) and
`geological-artifact-rigor` (field-wide standards).

## What a stacked-strata renderer can and cannot draw

Generic generators, including `geox_model(mode="geological_generate")`, take
`{formation, lithology, thickness_m}` plus a grid and draw horizontal layers over a basement, with one
fault as a vertical line carrying a throw label. Valid for passive-margin stratigraphy. It cannot express:

- underthrust crust (one plate passing beneath another)
- a mobile-shale wedge with a basal detachment
- an accretionary prism as a distinct body
- a Moho of varying depth
- differential subsidence or inverted structures
- a fault that actually offsets the layers it crosses

Audit tell of the renderer rather than the basin: horizontal boundaries everywhere, one vertical fault,
uniform basement, throw label that does not match the apparent offset at each contact.

If the framework contains crustal architecture, that architecture IS the figure. Draw it from geometry you
control (matplotlib / SVG), or scope the artifact to "stratigraphic column only" and say so in the caption.

## Framework outranks the formation column

- The basin profile says **how the basin works**: phases, collision timing, mobile shale, inversion.
- The stratigraphic file says **what the parts are called and how thick**: formation names, ranges.

Architecture comes from the framework. The strat column supplies labels and envelope only. When they
disagree about architecture the framework wins; when they disagree about a name, cite both.

Failure shape: the profile is quoted correctly in the caption while the drawing was built from the strat
column, so caption and polygons describe different tectonic models. That is how a superseded model gets
re-shipped while looking sourced.

## Chainage discipline

Compute along-route distance from the station coordinates with a WGS84 geodesic, then place every body by
chainage. Say both halves: "chainage computed from published coordinates; the coordinates themselves are
schematic" — arithmetic precision does not create positional accuracy.

A feature outside the transect is either given a longer transect or labelled projected and kept out of the
polygon set. Drawing it inside a province it does not occupy is an error any regional geologist spots at a
glance. Recomputing chainage from coordinates does upgrade the axis from schematic to derived; say which.

## Surfaces are families, not numbers

Regional unconformities carry different ages because they are picked on different markers in different
domains, and merge landward with other surfaces. Published spread for one named surface can exceed 3 Myr.

- print the marker or domain with the age ("DRU, shelf picks, 13.5–12.5 Ma")
- or print the range, and call it a range
- never print one age as the surface's age when picks disagree
- never average competing ages into a new number — that value belongs to no source
- a label like "top NN9 = 8.5 Ma" is internally inconsistent when the published biohorizon is ~9.5 Ma;
  check the marker against the calibration before accepting the label

## Well outcomes

Only from a named operator or regulator release, tier recorded. A placeholder well has no outcome and is
omitted. Giving one an outcome — especially one borrowing a real play name to sound credible — is the most
damaging fabrication class in a technical figure, because it is indistinguishable from data at a glance.

## Designing the model set

- Six scenarios is not six models if two pairs share geometry: hash `bodies` and compare titles.
- Each model: claim, evidence for, evidence against, and one discriminating test naming the measurement,
  the expected signal and the deciding value.
- Models at different depths (crustal architecture vs mantle process) are complementary, not competing.
  Ranking them against each other is a category error.
- Keep a rejected model only when the rejection is auditable and labelled — it records a decision.
- "Not all possible models" belongs in the caption; a closed set presented as complete is itself a claim.

## NW Sabah anchors

- Dangerous Grounds is thinned **continental** crust underthrusting southeast beneath Sabah. The Sabah
  Trough is a foredeep, not a suture with relict oceanic crust.
- The margin was built by PSCS subduction followed by Dangerous Grounds / Reed Bank arrival — not a
  Eurasia vs Philippine Sea plate collision. A basin profile carrying the latter framing is wrong at source.
- North Sabah–Palawan Wedge: overpressured mobile shale ~2–4 km sub-sea, basal detachment in the 5–8.7 km
  range, mud canopy, mini-basins loaded by kilometres of clastics. Shortening is part crustal, part
  gravity-driven, varying along strike — a slider, not a binary.
- Crocker Range is an uplifted accretionary prism (Crocker / Rajang turbidites); crust thickens to about
  60 km beneath it against roughly 24 km in central Sabah.
- Telupid ophiolite sits near 117.1 °E, east of the Crocker axis, with contested age (Mesozoic mapping vs
  later Miocene zircons). It cannot stand in for Crocker Range basement.
- Mt Kinabalu: sheeted granite, U–Pb zircon 7.85–7.22 Ma, emplaced under extension, ~4,095 m present
  elevation. It is not evidence for a regional magmatic ridge.

## Reference files

`references/` — extend here with per-basin architecture notes as they are verified, one file per basin.
