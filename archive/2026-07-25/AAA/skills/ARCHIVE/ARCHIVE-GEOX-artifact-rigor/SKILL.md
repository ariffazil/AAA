---
name: GEOX-artifact-rigor
description: "Standing instruction for all geoscience artifacts — panels, dossiers, maps, cross-sections"
version: 1.0.0
author: arif-sovereign
tags: [geology, GEOX, rigor, standing-instruction, F2-truth]
related: [hermes-prime-identity, explorer-dispatch-protocol, measure-before-acting]
---

# Geological & Technical Artifact Rigor

> **Origin:** A working PETRONAS exploration geologist reviewed a tectono-stratigraphic panel and said "tak cukup geology" — not enough geology. The artifact had epistemic-confidence tagging and stylized cartoon cross-sections but lacked actual technical substance. This skill prevents that failure mode.

## Trigger

Any time you produce or revise a geoscience, reservoir, or subsurface artifact: panels, dossiers, maps, cross-sections, stratigraphic columns, well correlations, seismic interpretations, prospect assessments.

## Hard Rules

### 1. Epistemic Tags Are Not a Substitute for Content
Confidence labeling (CLAIM/HYPOTHESIS/etc.) is a wrapper around a claim, not the claim itself. Every tagged item must carry the actual data point, number, reference, or mechanism — not just a label and a schematic shape.

### 2. No Cartoon Geometry for Technical Audiences
Do not render generic sine-wave "basin" shapes, blob "anticlines," or arrow-only "overpressure" icons as interpretation. If real seismic character, well logs, structure/isopach maps, or published figures exist, reference or reproduce their actual geometry and cite the figure. If no real data exists, say so explicitly — do not fill the gap with a schematic that looks authoritative.

### 3. Quantitative Claims Need the Supporting Curve
Any timing claim (e.g. "oil expelled early, gas expelled late") must be backed by the actual maturity indicator (Ro, Tmax, burial history) or flagged as UNSUPPORTED ASSUMPTION. Any reservoir/seal/trap claim needs closure area, net-to-gross, or volumetric range — not just a geometric cartoon of "reservoir here."

### 4. Terminology Precision Check
Cross-check every named geological entity, terrane, or structural term against its established usage in the cited literature. Flag any term used in a way that could conflate two distinct concepts (e.g. a named crustal block vs. the process acting on it). State the check was done.

### 5. State What Data Would Upgrade Each Hypothesis
For every item tagged HYPOTHESIS or PLAUSIBLE, name the specific dataset, well, or measurement that would move it to CLAIM. A reader should know exactly what's missing, not just that something is missing.

### 6. Age/Stage Precision Must Match Actual Resolution
Do not present a stage duration more narrowly than the underlying dataset resolves. If the number is an onset age bounding a longer process, say so — don't let stage boxes imply false precision.

### 7. Self-Check Before Delivery
Before presenting any geoscience artifact, run this test:
> "Would a subsurface geologist with access to real well/seismic data accept this as technical content, or would they say this is dressing without depth?"
If the honest answer is the latter, add real data, cite the actual figure/table, or explicitly scope the artifact as conceptual framing only — labeled as such up front.

### 8. Distinguish Framework from Finding
Epistemic tagging (CLAIM/PLAUSIBLE/HYPOTHESIS/ESTIMATE/SCHEMATIC) is a valuable governance layer for tracking confidence over time — keep it. But it governs geological content; it does not generate geological content. Never let the elegance of the tagging system create the impression of rigor that the underlying geology doesn't have.

## Coordinate Verification (supplementary)

- Every coordinate must have a verified source (GPS, published map, GeoNames)
- "From memory" = SPECULATED, never OBSERVED
- Plotting wrong coordinates in geoscience = wrong well = dry hole
- Lipad/Tabin: actual 5.188°N, 118.502°E (GPS verified)
- Maliau Basin: actual 4.830°N, 116.900°E (Wikipedia)

## Block vs Structure Names (supplementary)

- PSC block names (Block G, H, K, N, X, R) = operator/PETRONAS designations
- Structural trend names (L-B-P, M-La-S, Pg-Lt-U) = geological labels
- Field names (Limbayong, Bestari, Kikeh, Rotan) = discovery names
- These are NOT interchangeable. Verify before using.

## Output Requirement

Any geoscience artifact must be reviewable by a working geologist without them needing to ask "where's the geology?" — the tagging system sits on top of real technical substance, not replaces it.
