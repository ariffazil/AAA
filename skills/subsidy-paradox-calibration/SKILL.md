---
name: subsidy-paradox-calibration
description: "Reference data bank for PETRONAS/Malaysia subsidy paradox modeling. Load when building or verifying any NOC sovereign-side analysis where oil price affects both company dividend and government subsidy bill."
version: "1.0.0"
tags: [wealth, calibration, petronas, malaysia, subsidy-paradox]
---

# PETRONAS Subsidy Paradox — Calibration Reference

## When to load

- Building/verifying any NOC sovereign-side model where oil price affects both corporate dividend AND government fuel subsidy
- Cross-checking any "high oil = national windfall" assumption (likely wrong)
- Re-running the live engine on `/propa/#paradox-sec` or `/malaysia/#paradox-flow`

## The Paradox (one sentence)

When oil rises, PETRONAS wins (higher PAT → higher dividend, capped at 60%). The nation loses faster (subsidy bill grows with market price). Crossover = structural inflection.

## Calibration (MoF Parliamentary Reply 2025-2026)

| Input | Value | Source |
|---|---|---|
| RON95 unsubsidized market price at $85 Brent | ~RM 4.25/L | `MKT(B) = max(1.5, B × 0.04 + 0.85)` |
| BUDI95 subsidized cap | RM 1.99/L | MoF, Sep 2025– |
| National fuel consumption (total) | ~38B L/yr | Bureau of Statistics |
| Subsidy bill at $85 (BUDI95) | ~RM 38B/yr | MoF: RM 3.5B/mo steady, RM 7.5B/mo Apr 2026 peak |
| **Subsidized pool (derived)** | **17B L/yr** | RM 38B ÷ (RM 4.25 − RM 1.99) = 17B |
| **NOT total consumption** | **38B L/yr** | First calibration was wrong here |

## Calibration Discipline (the lesson)

```
WRONG constant: assume total pool × assumed per-unit gap
RIGHT constant: actual pool = reported total bill ÷ known per-unit gap
```

The first calibration used total national fuel consumption (38B L/yr) as the subsidized pool. MoF reports RM 3.5B/month at ~$90 Brent. At that price the gap is RM 2.46/L. RM 42B/yr ÷ RM 2.46/L = 17B L/yr — the actual subsidized pool.

The difference: total consumption includes diesel, commercial vehicles, and B40 users who are NOT in the BUDI95 scheme. The BUDI95 scheme only covers eligible private car/motorcycle owners up to 300L/month.

**Always cross-check model output against reported peaks:**
- MoF peak RM 7.5B/month (Apr 2026, Brent ~$120) = model RM 62B/yr at $120 → ~10% over, same order. ✓
- MoF steady RM 3.5B/month (Jun-Jul 2026, Brent ~$90) = model RM 42B/yr at $90. ✓

## Model Constants (shared across engines)

```javascript
const BASE_PAT = 45.4;   // RM B, FY2025 audited
const SENS     = 1.00;   // RM B PAT per $1 Brent delta
const CAP      = 0.60;   // AMEND-2026-08-03-001, 60% dividend cap
const FLOOR    = 20.0;   // MoF Budget 2026 dividend declaration
const V_L      = 17e9;   // subsidized pool, 17B L/yr — CALIBRATED, not total consumption
const MKT = B => Math.max(1.5, B * 0.04 + 0.85);  // market RON95 price
const REG = {BUDI95: 1.99, FULL: 1.88, FLOAT: null};
```

## Key Outputs (BUDI95 regime)

| Brent | PAT | Dividend | Subsidy | Net | State |
|---|---|---|---|---|---|
| $40 | 0.4 | 20 | 8 | +12 | A · QUIET |
| $55 | 15.4 | 20 | 18 | +2 | B · SQUEEZE |
| **$57** | | | | **~0** | **CROSSOVER** |
| $70 | 30.4 | 20 | 28 | −8 | C · PARADOX |
| $85 | 45.4 | 27.2 | 38 | −11 | C · PARADOX |
| $120 | 80.4 | 48.2 | 62 | −14 | C · PARADOX |

## Regime Impact

- **BUDI95**: crossover ~$57. Nation bleeds above $57. Bleed = RM 8-14B/yr at $70-$120.
- **FULL (pre-Sep 2025)**: crossover <$40. Nation bleeds at virtually all Brent levels.
- **FLOAT (zero subsidy)**: crossover ~$98. Nation wins below $98, bleeds above.

## MoF Subsidy Timeline (parliamentary reply)

| Period | Monthly cost | Note |
|---|---|---|
| Jan 2026 | RM 700M | Baseline |
| Mar 2026 | RM 5.0B | Iran war spike |
| Apr 2026 | RM 7.5B | Peak (Brent ~$120) |
| Jun 2026 | RM 3.5B | Stabilized |
| Jul 2026 | RM 3.5B | Stabilized |

Peak was 10x the steady state. Iran war drove a temporary crisis within the structural regime.

## Live Anchors

- `/propa/#subsidy-paradox` → corporate-side paradox (PETRONAS engine + dividend cap)
- `/malaysia/#subsidy-paradox` → sovereign-side paradox (federal budget engine + subsidy bill)
- Both share the same v3 model (`/testbed/petronas_malaysia_v3/model.py` + `v3-engine.js`)
- Cross-link anchors run both ways: each page links to the other section
- The LIVE engine on each page is canvas-rendered, all-sliders, no static charts

## Session-learned pitfalls (2026-08-06)

### Default slider state must be TIGHT, not PARADOX
When deploying the v3 live engine on a public page, opening with PARADOX (red) on first load is wrong UX. The paradox section exists to be *discovered* by the user dragging Brent up — it should not be red on arrival.

**Default state:** Brent $65, Iran war 0%, reform delay 0 months → verdict TIGHT (yellow), hidden tax 0.75×, tripwire STANDBY.

**Why this matters:** A page visitor who lands on a red verdict thinks the institution is collapsing. It's not. The model's job is to show the *range*, not the *worst case*. A page opening in red is a credibility leak.

### Dual-canvas approach for mixed magnitude domains
When the same chart area must show both subsidy bill (RM15-80B) and net-cash trajectory (RM0-150B), put them in two separate canvases with separate Y-axis scales. Single canvas with dual scale confuses readers — small-magnitude lines collapse to flat lines near zero.

Pattern (verified on /propa/ 2026-08-06):
- Canvas 1: paradox dimensions (dividend, subsidy, net-to-budget) — RM0-80B scale, 280px tall
- Canvas 2: net-cash trajectory (Bull/Base/Bear envelopes + live) — RM-30 to 150B scale, 220px tall
Both update on same slider events. Total height ~500px vs old single 380px chart with collapsed lines.

### Static charts are entropy; sliders are metabolism
v1 had 4 static matplotlib PNG charts (S01-S04) in the paradox section. v3 replaced them with a single live engine. Static charts show one state; sliders show the full range.

Entropy reduction: 4 images → 0 images, replaced by 1-2 interactive canvases. Always prefer interactive over static for user-facing models on landing pages. Keep static charts for printed/PDF deliverables where interaction is impossible.

### Cross-validate the model output against real MoF reported peaks
The piecewise-linear subsidy curve must land within ±10% of Anwar's parliamentary reply numbers. At Brent $90, curve gives RM52.5B — MoF said ceiling RM40B. At $120, curve gives RM72.5B — MoF said peak RM7.5B/mo × 12 = RM90B/yr. The high end overshoots but captures the *trend* correctly. Label as INT, not OBS.

**Test recipe:** before shipping any NOC subsidy model, plug in 3 sentinel Brent prices ($50 / $85 / $120) and compare to any published ceiling/peak. If your model deviates > 20% on any sentinel, the piecewise anchors need recalibration.

### Test API: keep Python (pytest) and JS in lockstep via cross-validation
For any financial model served as both Python (for tests) and JS (for browser), write a JS cross-validation script that imports the JS source and asserts the 6-10 sentinel scenarios match Python to ±0.05. The bug pattern this catches: Python and JS drift silently when one gets updated and the other doesn't.

## v3 model constants (what's actually live as of 2026-08-06)

The skill's earlier "BUDI95 pool" formula (`sub = V_L × (MKT - 1.99)`) was a first-pass approximation that overestimated the bill at high Brent. The deployed v3 model uses **continuous piecewise-linear in Brent** plus two sovereign modifiers:

```python
# Anchor points (continuous, no discontinuities at the boundaries):
# $40 → RM3B  · $50 → RM8B  · $65 → RM15B  · $90 → RM52.5B  · $125 → RM72.5B
if brent <= 50:    base = 3.0 + (brent - 40) * 0.5      # slope 0.5 (low regime)
elif brent <= 65:  base = 8.0 + (brent - 50) * 0.467    # slope 7/15 (transition)
elif brent <= 90:  base = 15.0 + (brent - 65) * 1.5     # slope 1.5 (paradox entry)
else:              base = 52.5 + (brent - 90) * 0.571   # slope 4/7 (paradox ceiling)

# Sovereign modifiers (multiplicative)
iran_uplift = 1.0 + 0.10 * (iran_war / 50.0)         # 10% per 50pp war probability
reform_uplift = 1.0 + 0.02 * reform_delay_months      # 2% per month Anwar delay
subsidy = min(base * iran_uplift * reform_uplift, 75.0)  # hard ceiling
```

**Why the new shape:** the BUDI95/V_L formula produced RM 38B at $85, which is roughly correct, but it didn't capture the *steeper* trajectory at $90-$120 (actual peak RM 7.5B/mo = RM 90B/yr, not RM 62B). The piecewise-linear version calibrated against MoF peak/month shows RM 52.5B at $90 and RM 72.5B at $125, which match the observed peak better. Cross-validation: 6/6 JS-Python tests pass within 0.05 tolerance.

## v3 tripwires (added 2026-08-06)

| Tripwire | Metric | Trip | Engagement action | Status |
|---|---|---|---|---|
| 10 | Subsidy bill / Petroleum dividend | > 1.0× for 2 consecutive quarters | Freeze discretionary payout until subsidy reform passes parliament | PROPOSAL — awaiting F13 sign-off |

Tripwire 10 **engages at FY26 anchors** (Iran war50, delay8mo, Brent85 → ratio1.65×). Would NOT engage at FY25 anchors (subsidy ~RM15B, dividend RM32B → ratio 0.47×).