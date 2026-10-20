---
name: geoscience-model-figure
version: 1.0.0
description: Use when forging a multi-model geological section.
---

# Geoscience model figures — falsifiable by construction

Arif is an exec geoscientist (12 yr, zero dry wells). He reads a section faster than you can describe it,
and he rejects a figure that looks authoritative but cannot lose. A picture that cannot be wrong is
decoration. Build so each model carries one measurable prediction.

## Rule 0 — do not hand him a to-do list

When he asks you to falsify or validate, **do the falsification**. Run the arithmetic, state verdicts
(LULUS / GAGAL) per item, show the numbers. Do not tell him which tests he should run, which papers to
read, or how to work. "Don't tell me what to do!! I'm a geologist!!"
Output is a result he can fight, not a curriculum.

## Build procedure

1. **Anchor the transect on real coordinates before drawing anything.** Take published lat/lon control
   points and recompute chainage with WGS84 geodesics. Stations are L0; anything drawn between them is
   L2. A section that ends at the Crocker front must mark a unit east of it as off-section, not place it
   inside the range.
2. **Read the framework that supersedes the formation table.** A named-formation stratigraphy list is
   not a tectonic framework. If the current framework is a wedge / underthrust model, a layer-cake stack
   with regional ophiolite basement is wrong even when every formation name in it is correct. This is
   the single most repeatable failure mode.
3. **Hash every model's geometry at runtime and publish the hashes.** Two models that share a Moho
   surface are not two models. Either they differ in the added body (declare the alias: "shares crust
   with A, differs only in the ophiolite sheet") or the figure fails. Fail the page on identical
   full-geometry hashes. Never let a compare control sit between two identical shapes.
4. **Give each model an observable, a pass window, and a killer.** Tag every window: COMPUTED
   (derivation on the page) / PUBLISHED (cited) / UNKNOWN (no constraint — draw no window). An UNKNOWN
   row is part of the deliverable, not a gap to hide.
5. **Downgrade the status vocabulary.** "Best supported" reads as a ranking. Use MOST CONSTRAINED ·
   NOT VALIDATED / PARTIALLY CONSTRAINED / TESTABLE · UNRESOLVED / FALSIFIED. Never "closest to
   reality", "validated", or "best model" — those need evidence objects and a scoring rule that do not
   exist yet.
6. **Make missing data a visible UI element.** The unresolved list (no per-station receiver-function
   pick, no SEG-Y, no pressure history, no dated slip) belongs on the page, not in prose beneath it.

## Physics checks — run before publishing

**Airy isostasy.** `e = ((rho_m - rho_c)/rho_m) * (t - t0)`. With 2800/3300 the bracket is 0.1515:
24 km -> -0.91 km, 40 -> 1.52, 50 -> 3.03, 57 -> 4.09, 60 -> 4.55. A 4.095 km summit needs **57 km**
of crust (51-68 km across densities).

**T0 is a parameter but not a free one.** Publish the sensitivity (T0 25/30/35 -> 52.0/57.0/62.0 km) and
say T0 is bound to the density pair. T0 = 6 km with rho_c = 2800 puts a 6 km granitic column at sea
level — wrong by 3.6 km. Oceanic crust (rho_c ~ 2900) is the case that genuinely needs ~39 km. Mixing
the two systems manufactures a false "no paradox" result.

**Exhumation is not summit height / age.** Emplaced at 7-12 km, now at surface, over 7.85 Myr is
0.9-1.5 mm/yr average; the same 7 km over a ~1 Myr pulse is ~7 mm/yr peak. Always label average vs peak.

**Overpressure has two numbers.** At 3 km (Sv 67.7, Ph 30.3, leak-off 0.8*Sv = 54.2 MPa): Sv - Ph =
37.4 MPa is the excess to reach lithostatic (a ceiling); leak-off - Ph = 23.9 MPa is the excess to
exceed the least principal stress — the injection threshold shale actually needs. Say which one.

**Diapirs rise without magma.** Mobile shale 2200-2300 kg/m3 under overburden 2350-2450 gives 50-250
kg/m3 buoyancy. Compaction alone cannot make the overpressure; gas generation plus rapid loading can.

## Pitfalls

- **A hypothesis with no kill criterion is a preference.** Name the measurement that would end each
  model. If you cannot, mark it REGISTERED and draw no geometry for it — inventing a section for a
  model with no published geometry is the same defect as inventing a well outcome.
- **Never invent a well outcome.** Placeholder wells carry no result; omit them rather than assigning
  one. A real well's status comes from the operator release, with its evidence tier attached.
- **Gradient is not magmatism.** Advection along faults and pipes raises gradient with normal surface
  heat flow. Magmatism needs a magnetic body and a broad anomaly.
- **Non-unique is not wrong.** Potential-field and gravity inversions admit multiple bodies. Calling a
  published interpretation wrong because another also fits is a category error; say what would
  discriminate them.
- **Conflicting ages are three questions, not one error.** A biostratigraphic age, a geodynamic timing
  and an event-spine pick are separate objects. Keep them side by side with their marker basis; never
  average and never relabel one as another.
