---
name: geox-pressure-governance
id: geox-pressure-governance
version: 1.0.0
owner: AAA
risk_tier: high
floor_scope: [F2, F4, F7, F9, F12]
description: Governed pressure prediction pipeline for GEOX — enforces calibration gates, literature-grounded stratigraphy, and unknown-space mapping. Prevents hallucination of subsurface properties by distinguishing confidence from coverage. Forged from Bekok Deep-1 coverage failure and Bekantan-1 stratigraphy fabrication incident.
autonomy_tier: T2
triggers:
  - pore pressure analysis
  - pressure prediction
  - fracture gradient
  - calibration gate
  - coverage score
  - unknown space mapping
  - geomechanics
  - Eaton method
  - Bowers method
  - overpressure
  - mud weight window
  - subsurface pressure
---

# GEOX Pressure Governance

> DITEMPA BUKAN DIBERI — The pipe predicts pressure. The gate predicts confidence. The coverage knows where the map ends.

## Purpose

This skill governs how GEOX produces pressure predictions. It enforces three non-negotiable principles:

1. **No output without calibration manifest** — uncalibrated predictions must be labeled, gated, and carry explicit caveats
2. **No stratigraphy without literature grounding** — basin context must come from published references, not LLM priors
3. **No confidence without coverage** — the model must know WHERE it has never looked

## The Four Domains

| Domain | Question | Status |
|---|---|---|
| Physics | What IS the pressure? | Pp, FG, Sv, σ, thermal, compartment |
| Calibration | How close is model to observations? | Eaton/Bowers params, offset wells, RFT/MDT |
| Uncertainty | How wide is the range? | Bayesian envelope, ensemble range |
| **Coverage** | **Where does the map end?** | **#36 UNKNOWN_SPACE_MAPPING** |

## Component Registry

Full SOT: `/root/GEOX/resources/registry/pressure_components.yaml` (36 components, 4 domains + agent governance)

## Critical Rule — Coverage ≠ Uncertainty

> "Confidence calibrated to data is engineering. Confidence detached from calibration is narrative."

**Uncertainty** = how wide the range of possible values is.
**Coverage** = what part of reality have we actually observed.

A model can have confidence=0.81 in an interpolation while coverage_score=0.12 for that interval. That gap is where disasters live.

### Coverage Score Formula

```
coverage_score = count_of_observations_in_interval / total_interval_thickness_in_100m_bins
clamped to [0.0, 1.0]
```

### Coverage Levels

| Level | Score | Effect |
|---|---|---|
| SUFFICIENT | 0.7–1.0 | Interpolation supported |
| PARTIAL | 0.3–0.69 | Interpolation ok, extrapolation flagged |
| SPARSE | 0.1–0.29 | Label drops to HYPOTHESIS regardless of confidence |
| VOID | 0.0–0.09 | 888_HOLD. No observational basis for any claim. |

### Override Rules

```yaml
- rule: "coverage < 0.30"
  action: "epistemic_label = HYPOTHESIS"
  reason: "insufficient_observational_coverage"

- rule: "coverage < 0.10"
  action: "status = 888_HOLD"
  reason: "void_coverage_no_observational_basis"

- rule: "confidence > coverage + 0.30"
  action: "downgrade epistemic_label"
  reason: "confidence_outruns_evidence"
```

## Calibration Gate

`@requires_calibration` decorator enforces pre-flight on every geopressure entry point:

| Level | Requirements | Confidence Cap | Epistemic Label |
|---|---|---|---|
| CALIBRATED | sonic_log + rft_mdt + lot_xlot | 0.85 | CLAIM |
| PARTIAL | at least 1 offset well OR sonic_log | 0.72 | ESTIMATE |
| UNCALIBRATED | nothing | 0.45 | HYPOTHESIS |

Without calibration manifest → 888_HOLD with specific missing inputs listed.

## Stratigraphy Rule — No Fabrication

GEOX output MUST NOT fabricate stratigraphy. When asked for basin stratigraphy:
1. **Load from `resources/registry/stratigraphy/` YAML** (literature-grounded)
2. **Never synthesize group names/depths from LLM pretraining patterns**
3. **If registry doesn't exist → 888_HOLD, not "invent plausible groups"**

Every geological property output must carry:
- `basin_context_ref` — path to literature-grounded YAML
- `literature_citation` — primary source DOI or reference
- `coverage_score` — observational density in the interval

### Malay Basin Stratigraphy

Registry: `/root/GEOX/resources/registry/stratigraphy/malay_basin.yaml`

Key fact: The Malay Basin sequence skips B→D (Group C is absent — EPMI nomenclature). **Group G IS present** (confirmed Knova UM thesis 2020s, between F and H). **Group L IS present** (confirmed Madon 2010 GSM — best lacustrine source rock, HI 300-400, regional seal on basin flank). These were previously missed — the F13 sovereign caught the omission with: *"Malay basin got group G? Madon did some work here actually."*

Overpressure seal: **Group F** (regional transgressive shale) for basin centre. **Group L** for basin flank/margin.
Top of overpressure basin center: **1900–2000m** (Madon 2006, GSM Bull 49:135-144).
Top of overpressure basin margin: **2600–3000m** (sealed by Group L).

**Never declare a stratigraphic group absent without checking published literature.** The LLM's pretraining data is NOT a valid source for basin stratigraphy. Always load the registry or cite Madon/Tjia/USGS.

## Fabrication Failure Pattern (2026-08-13)

**What happened:**
1. Hermes was asked for Malay Basin pressure analysis (Bekantan-1, Group K TD)
2. Without literature registry, fabricated incorrect role for Group G (it exists but is NOT the seal — Group F is the seal), and skipped Groups G and L entirely in the stratigraphic column
3. Used generic "Group A through K" numbering with invented depths
4. Put overpressure onset at 2200m (actual: 1900-2000m)
5. User (the project geologist) caught it: *"Malay basin got group G? Madon did some work here actually."*

**Root cause:** LLM pretraining patterns substituted for published literature when no registry existed.

**Lesson:** The user knew one name — "Madon" — and that was enough to collapse the entire fabrication. Authority-by-reference is a valid linguistic signal for GEOX to recognize and act on.

## Canonical Coverage Failure — Bekok Deep-1

- Pre-drill model: confidence high for shallow section
- Observational coverage: ZERO for shallow gas hazard interval
- Drilled from platform → **no site survey data coverage** in that specific location
- Result: LOPC Tier 1 (4 Apr 2023), platform evacuation
- Official explanation: "well collide"
- Actual cause: shallow gas — a known hazard, but unsampled in that specific location

This is not an uncertainty failure. The model was not "wrong about the value." The model did not know where its own knowledge ended. Coverage was zero. Confidence was not.

**This is the founding scar for Component #36 UNKNOWN_SPACE_MAPPING.**

## Pressure Equations Reference

See `references/pressure-equations.md` for Eaton, Bowers, Phillips formulas with input parameters and typical Malay Basin values.

## Files

| File | Purpose |
|---|---|
| `/root/GEOX/resources/registry/pressure_components.yaml` | 36-component SOT |
| `/root/GEOX/resources/registry/stratigraphy/malay_basin.yaml` | Literature-grounded Malay Basin stratigraphy |
| `references/pressure-equations.md` | Eaton/Bowers/Phillips formulas + Malay Basin params |
| `references/coverage-score-formula.md` | UNKNOWN_SPACE_MAPPING operational details |
