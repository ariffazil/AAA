---
name: geoscience-figure-audit
description: Use when auditing a geological cross-section figure.
---

# Geological figure and model-space audit

A section drawing is an argument, and every element of it can be checked. The failure mode is not ugliness — it is a figure whose labels claim more than its geometry, or whose model space contains duplicates presented as alternatives.

## Procedure

1. **Hash the model geometries before trusting a comparison control.**
   Build a crust signature (`topography + basement + Moho + detachment`) and a full signature (crust + every added body flag). Two models with the same crust hash differ only in the added body; that is allowed but must be **declared as an alias in the UI**. Two models with the same *full* hash are a defect — the compare button is comparing a drawing with itself.
   Surface the verdict on the page (PASS / PASS with declared aliases / FAIL), computed at runtime, not asserted in prose.

2. **Check every numeric label against the source the figure itself cites.**
   A label like "thickest crust here" must match the cited paper's numbers. If the citation says the maximum is elsewhere, the label is false no matter how the line was drawn. This is the highest-yield check in the whole audit: the figure usually cites the paper that contradicts it.

3. **Do not let a hand-plotted line borrow the authority of a measurement.**
   Separate three things in the labelling: schematic geometry, published constraint, and fitted pick. A published deep constraint that was **not** fitted to the drawn line goes in as an unattached dashed annotation with the words "published, not fitted". Attaching it invents a pick that nobody made.

4. **Draw absence as absence.**
   If there is no constraint over a stretch of section, break the line and label the gap. Interpolating a smooth surface across an unconstrained interval manufactures agreement that the data does not contain.

5. **Place mechanism glyphs inside the domain that owns them.**
   An extension/thinning/rift glyph sitting on a seam between two crustal blocks reads as a boundary process, not as a process inside either block. Check the x-position against the body polygon that ends there. Label inherited structures as inherited ("rift faults — inherited, not the young event") — the lines may be correct while the absence of a label makes them read as active.

6. **Each model needs one killable number.**
   A model entry requires: predicted observable, pass window, what kills it, and a basis tag — `COMPUTED` (derived on the page from a shown equation), `PUBLISHED` (cited), `UNKNOWN` (no constraint exists, so no window is drawn). A model with no falsifiable number is REGISTERED, not TESTED. Say so in the status vocabulary: "MOST CONSTRAINED · NOT VALIDATED" rather than "BEST SUPPORTED".

7. **Never rank models without a scoring rule and evidence objects.**
   "Closest to reality" is only meaningful once a test exists that the other models fail. Absent that, the honest output is the model family plus the next discriminating measurement — not a winner.

## Numeric discipline (these get argued about)

- **Airy isostasy:** `e = ((ρm − ρc)/ρm)·(t − t0)`. T0 is **not a free parameter** — it is fixed by the density pair. Using ρc ≈ 2800 with t0 = 6 km claims a 6 km granitic column sits at sea level, which is wrong by ~3.6 km; oceanic crust (ρc ≈ 2900) needs t0 ≈ 39 km for the same reason. Quote the required thickness as a **range across plausible t0** (25/30/35 km), not one number, and say what each t0 represents.
- **Shale mobilisation:** the excess pressure required is **leak-off minus hydrostatic** (≈ 0.8·Sv − Ph, order 20–30 MPa at 3–4 km), not lithostatic minus hydrostatic. Sv − Ph is the ceiling to reach lithostatic, not the requirement. A critic computing Sv − Ph and calling your number wrong has computed a different quantity — distinguish the two explicitly rather than conceding.
- **Exhumation rate:** peak and average are different numbers over different intervals. 7 km exhumed over ~1 Myr is ~7 mm/yr peak; the same 7 km over the full pluton age is <1 mm/yr average. Summit-height ÷ age is neither — it is a third quantity. Always name the interval.
- **Grading a correction:** before accepting "your number is wrong", check **which quantity** the other party computed. Of four corrections in one review, two were arithmetic errors by the reviewer and one was a labelling ambiguity on our side. Fix the ambiguous label; do not delete a correct number.

## Evidence discipline for well and outcome data

- Placeholder wells carry **no outcome**. Omit them from the figure rather than attaching a plausible result.
- Public well status comes from the operator's release or a peer-reviewed source, tagged by tier; a model must not author an outcome.
- A composite/stacked hypothesis is a **new identifier** (e.g. "ophiolite over continent"), not a redefinition of an existing one. Never mutate an existing hypothesis ID — mint a new one, or every later test scored against the old ID is ambiguous.

## NW Sabah anchor values (verify before citing)

Use these to recognise a contradiction quickly; every one needs a provenance check before it goes public.

- Crustal maximum ~60 km beneath the Crocker Range, minimum ~24 km in central Sabah (receiver functions); gravity-inversion Moho 32.8–52.5 km.
- Dangerous Grounds crust 25–30 km, thinning to 20–25 km under the trough with **no crustal suture and no relict oceanic crust** beneath it (Vijayan et al. 2013); the trough is a foredeep, not a trench.
- Collision framing is PSCS subduction then Dangerous Grounds / Reed Bank collision — not Eurasia vs Philippine Sea.
- Surfaces as ranges: BMU ~23–24 Ma; DRU 13.5–12.5 (some picks 14.2–14.9); UIU ~10.5; SRU ~8.5–9.5. Top NN9 ≈ 9.53 Ma, so "Top NN9 at 8.5 Ma" is internally inconsistent.
- Kinabalu granite 7.85–7.22 Ma (U-Pb zircon), emplacement ~7–12 km depth, intruded under extension.
- Telupid ophiolite sits at ~117.15 °E, east of the Crocker axis; age contested Mesozoic vs Miocene. Ranau peridotites are a separate body.
- Basal detachment in the NW Borneo belt ~5–8.7 km below seabed, dipping landward ~1.9°.

## Thermal discrimination

High geothermal gradient alone does not imply magmatism — advective flow along faults and pipes raises local gradient without raising surface heat flux or leaving a magnetic body. Discriminate on **geometry**, not on "hot": heat confined to fault/pipe traces with normal flux means advection; heat broad across blocks with high flux **and** a magnetic body means an internal source. Carry conductive, advective, transient burial/uplift and magmatic explanations as competitors until data excludes one.

## Reporting

Report claim-by-claim: what the figure says, what the source says, what the geometry actually draws. Separate "wrong" from "underspecified" from "schematic and labelled as such" — only the first two need a fix.
