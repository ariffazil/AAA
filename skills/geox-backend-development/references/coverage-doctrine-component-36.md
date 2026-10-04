# Coverage Doctrine — Component #36: UNKNOWN_SPACE_MAPPING

> **Forged:** 2026-08-13 by Arif Fazil (F13 SOVEREIGN) + Hermes
> **Canonical scar:** Bekok Deep-1 (SCAR-6), PM9, 4 Apr 2023

## Axioms

1. "Confidence calibrated to data is engineering. Confidence detached from calibration is narrative."
2. "Disasters begin when confidence outruns evidence."
3. "Where does the map end?"

## 4-Layer Coverage Check

Coverage ≠ uncertainty. Coverage is WHERE THE MAP ENDS.

| Layer | Question | Bekok Deep-1 | Status |
|---|---|---|---|
| Sensing | Did sensors touch reality? | 3D seismic bright spot + historical well + mud logging | PASS |
| Recognition | Was the signal seen? | Bright spot = DHI, not hazard | FAIL |
| Interpretation | Was it correctly interpreted? | Pressure increase = "formation" | FAIL |
| Institutional memory | Was interpretation preserved or compressed? | Report compressed to "formation issue" | FAIL |

## Bright Spot Recontextualization

Same seismic data → DHC indicator (reservoir) OR shallow gas hazard. Data doesn't change. Interpretation changes. Coverage includes: was the right interpretation applied?

## Operational Rules

1. `coverage_score = count_observations / interval_thickness_100m_bins`, clamped [0, 1]
2. `coverage < 0.30` → epistemic_label = HYPOTHESIS (regardless of confidence)
3. `coverage < 0.10` → 888_HOLD (void)
4. `confidence > coverage + 0.30` → downgrade
5. Sensing PASS but others FAIL → HOLD

## Malay Basin Literature

- Madon 2006 (GSM Bull 49:135-144) — overpressure, Group F seal, 1900-2000m
- Madon 1997 (GSM Bull 41:95-108) — heat flow, beta stretching
- USGS OF-99-50T — Malay Basin Province 3703
- Tjia 1994 — inversion tectonics

## Implementation

- **code:** `/root/GEOX/src/geox_core/gates/coverage_gate.py`
- **tests:** `/root/GEOX/tests/test_coverage_gate.py` (10 tests)
- **SOT:** `/root/GEOX/resources/registry/pressure_components.yaml` (36 components)
- **basin registry:** `/root/GEOX/resources/registry/stratigraphy/malay_basin.yaml`
