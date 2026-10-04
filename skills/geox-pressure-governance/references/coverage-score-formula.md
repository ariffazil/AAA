# Unknown-Space Mapping — Coverage Score Operational Details
# DITEMPA BUKAN DIBERI — Forged from Bekok Deep-1, 2026-08-13

## What Coverage Score Measures

Coverage score answers: **"What fraction of the depth interval has actual observational data?"**

It does NOT answer:
- "How uncertain am I?" (that's Bayesian uncertainty)
- "How many wells are nearby?" (that's offset well density)
- "How confident is the model?" (that's confidence — which must be checked against coverage)

## Formula

```
coverage_score = N_observations_in_interval / N_100m_bins_in_interval
```

Where:
- `N_observations_in_interval` = count of RFT, MDT, FIT, DST, LOT/XLOT data points falling within the interval of interest
- `N_100m_bins_in_interval` = total thickness of interval divided by 100m (rounded up)

Clamped to [0.0, 1.0].

## Example — Bekok Deep-1 (Coverage Failure)

```
Interval: Shallow gas hazard zone (0-1000m below mudline)
N_observations: 0 (drilled from platform, no site survey coverage)
N_100m_bins: 10
coverage_score = 0 / 10 = 0.0
```

Model confidence for this interval: ~0.85 (based on regional seismic interpretation)
Confidence minus coverage: 0.85 - 0.0 = 0.85 > 0.30

**Result:** `HYPOTHESIS` label, `888_HOLD` for drill planning use.
**What actually happened:** No gate existed. Confidence was used as-is. LOPC Tier 1.

## Example — Bekantan-1 at 750m TVDSS

```
Interval: Group E (550-900m, 350m thick = 4 bins)
N_observations: 2 (RFT from adjacent wells in PM304)
N_100m_bins: 4
coverage_score = 2 / 4 = 0.50
```

Model confidence: 0.78 (Eaton with regional parameters)
Confidence minus coverage: 0.78 - 0.50 = 0.28 < 0.30

**Result:** `ESTIMATE` label (coverage PARTIAL, confidence within bounds).

## Example — Malay Basin Group K (3000-5500m)

```
Interval: Group K (2500m thick = 25 bins)
N_observations: 0 in Bekantan-1 (well not drilled that deep)
N_100m_bins: 25
coverage_score = 0 / 25 = 0.0
```

Model confidence from Eaton: 0.72 (regional NCT)
Confidence minus coverage: 0.72 - 0.0 = 0.72 > 0.30

**Result:** `888_HOLD — void_coverage_no_observational_basis`
**Action required:** Obtain offset well data or RFT in Group K before any drill planning.

## Override Logic (Pseudocode)

```python
def check_coverage_and_confidence(coverage_score, confidence, current_label):
    """Enforce coverage bounds on confidence."""

    if coverage_score < 0.10:
        return {
            "status": "888_HOLD",
            "label": "VOID",
            "reason": "void_coverage_no_observational_basis"
        }

    if coverage_score < 0.30:
        return {
            "label": "HYPOTHESIS",
            "reason": "insufficient_observational_coverage"
        }

    if confidence > coverage_score + 0.30:
        return {
            "label": downgrade(current_label),
            "reason": "confidence_outruns_evidence"
        }

    return {"label": current_label}
```

## Key Insight

> Coverage is not uncertainty. Coverage is WHERE the map ends.

A model can be confident about places it has never looked. That is not uncertainty — that is hallucination with a number attached.
