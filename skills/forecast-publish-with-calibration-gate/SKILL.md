---
name: forecast-publish-with-calibration-gate
description: Publish commodity forecast with calibration gate enforced.
---

# Forecast Publish — Calibration Gate Discipline

The arifOS doctrine says: **promote a forecast only when walk-forward validation proves it beats a frozen baseline**. Aspirational "LIVE" labels without calibration evidence are a defect, not a feature. This is the workflow that gates every commodity surface (gold, oil, gas, klci, usdmyr) before promotion.

## The six-authority separation

Forecast output is a single artifact but six actors must not collapse into one. Each is a separate function with a separate input/output contract; combining them is the canonical recipe for over-trust.

| Actor | Job | Input | Output | Veto |
|---|---|---|---|---|
| **000 Integrity** | Feed health gate | ticker+apex timestamps, spread, missing bars, feed disagreement | `PASS / DEGRADED / FAIL` | FAIL = NO_FORECAST |
| **111 Regime** | Multi-TF regime posterior | 1H/4H/1D features | `regime_state ∈ {COMPRESSION, EXPANSION, TRENDING_UP, TRENDING_DOWN, RANGE, TRANSITION, EXHAUSTION}` with probability + uncertainty | unclear regime raises uncertainty, never blocks outright |
| **333 Forecast** | Quantile ensemble | regime + features + horizon | `quantile_path[]` (P10/P25/P50/P75/P90) for each horizon. NO fake OHLC | outputs distribution only, no actions |
| **555 Calibration** | Walk-forward validator | matured forecast-outcome pairs | pinball loss, coverage, Brier skill score, PBO, regime-conditional coverage | can demote SHADOW to QUARANTINE |
| **777 Translator** | Stance derivation | quantile distribution + regime + user inputs | per-audience stances (Trade / Simpan / Saver) | cannot override calibration state |
| **888 Judge** | Decision gate | all of above + risk envelope | `ACT / WAIT / HOLD / BLOCKED` (default HOLD) | holds BLOCKED even if 555 says LIVE |
| **999 Witness** | Receipt mint | input snapshot hash + config hash + code hash + output | immutable receipt to `/root/AAA/VAULT999/receipts/` | no decision power |

**Promotion rule** (binding):
```
LIVE iff (walk_forward_passed == true
         AND tuning_better_than_baseline == true
         AND hardening_passed == true
         AND at_least_30_days_data == true
         AND 888 has not BLOCKED)
else SHADOW.
```

A single failed adversarial test in the hardening layer (missing-data degradation, regime-shift skill drop, PSI drift) promotes to QUARANTINE — never quietly substitutes missing evidence with confidence.

## Two-audience rails (no translation)

A forecast server emits a single distribution. The frontend translates to different vocabularies per audience. **There is no auto-translation between rails** — LONG BIAS in the trade rail does NOT cause TAMBAH BERPERINGKAT in the saver rail. Saver stance is derived ONLY from saver-side inputs (XAU/MYR, dispersion, median return, plan horizon).

### Trade rail (margin technical)
- `LONG BIAS / SHORT BIAS / NO TRADE / EVENT RISK`
- Inputs: APEX verdict + confluence + regime
- Default: NO TRADE

### Saver rail (physical saver)
- `SABAR / TUNGGU / JAGA / TAMBAH BERPERINGKAT`
- Inputs: dispersion (P75-P25)/close > 6% → JAGA, |median return| > 3% → TUNGGU, default SABAR
- Default: SABAR
- NEVER manufacture TAMBAH BERPERINGKAT from technical signals

### Honest labels

Quantile displacement is NOT a probability. `((p50 - close) / close) * 100` is a **median return projection**, not "directional probability". Display it as `+0.45% median`, not `45% chance up`. When you don't have actual P(up) from a calibrated model, don't invent one.

Timeframes matter. RSI 37.8 (1D) and RSI 56.2 (1H) are different distributions. Always tag the timeframe on every metric you display.

## Schema contract (binding for every commodity)

The forecast endpoint exposes `wealth.gold.forecast.v1`-style schema with three horizons (+24h, +48h, +72h), quantile bands per horizon (P10/P25/P50/P75/P90), `p_up_after_cost`, regime state, validation block (baseline, pinball skill, coverage, Brier skill, calibration state), outputs block split by rail (trade_72h, physical_saving), and governance block (human_confirmation_required=true, execution_enabled=false, receipt_uri).

If the server cannot honor a horizon parameter, return 400. Never silently substitute (e.g. don't return 30-day cone when 72h was requested).

## Cadence (do not pollute receipts)

| Event | Update | Receipt |
|---|---|---|
| 30-60s | Display price only | No |
| Each closed 1H bar | Features + regime log | Light |
| **Daily (fixed time)** | **Official +24/+48/+72h forecast** | **Yes** |
| Major event (CPI/FOMC) | `EVENT_RESET` forecast, new ID | Yes |
| Outcome matures (24/48/72h later) | Score previous forecast | Yes |
| Weekly | Calibration/drift review | Yes |
| Deployment | Build hash + diff + tests + post-deploy probe | Yes |

**One receipt per forecast issuance, not per frontend fetch.** Polling UI must not create receipts — that's the difference between a ledger and a log.

## Procedure for a new commodity

When extending from one commodity (e.g. gold) to another (oil, gas, klci, usdmyr):

1. **Identify the data source class**: which WEALTH endpoint exposes the live ticker/forecast for this asset?
2. **Confirm endpoint exists and returns expected schema** (HTTP 200, JSON body, fields present)
3. **Copy the gold source tree** (`cp -r src/syedos-emas src/syedos-<asset>`), rename everything.
4. **Update gold.json** → `<asset>.json`: data endpoints, stance vocab, calibration thresholds.
5. **Update template.html** to match the new asset's tone (BM Penang for brotherhood, formal English for institutional, etc.).
6. **Cross-origin check**: vhost may not have `/api/*` route → use absolute URL to main domain.
7. **Build, atomic write, probe, receipt** — same as a single-asset patch.
8. **Don't promote until walk-forward passes** — gold was the first surface, set the SHADOW default.

## Common pitfalls

- **Median ≠ probability**. Computing `((p50 - close) / close) * 100` and calling it "directional probability" is a labelling defect. Display it as a median return projection.
- **Two-rail coupling**. `deriveSimpanStance` calling `apex.verdict` is indirect translation from technical state to saver recommendation. Decouple.
- **Schema discipline on horizon parameters**. If the server ignores the parameter and returns 30-day cone, either fix the server or relabel the frontend to be truthful about what the user is seeing.
- **Quiet forecaster promotion**. Don't switch to `LIVE` because the engine says so. The engine says LIVE; 555 must prove it; 888 must not BLOCK. All three required.
- **Receipt spam**. Don't mint receipts for every frontend fetch. One per forecast issuance. Polling UI ≠ ledger.
- **TIMEFRAME TAGGING**. Always tag the timeframe (1H, 4H, 1D) on every metric. RSI 37.8 ≠ RSI 56.2 if they're on different clocks.
- **lightweight-charts IS TradingView**. The npm package `lightweight-charts@4.x` is the open-source JavaScript library published by TradingView (BSD-3-Clause). Same chart engine as the embedded advanced-chart widget. Document the choice if asked.