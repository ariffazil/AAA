# WEALTH MCP Abstraction Enhancement — Status: PENDING

## What Was Proposed

OpenClaw reviewed Hermes's WEALTH abstraction proposal and found 3 bugs, then produced corrected patches for two existing tools:

### `energy_crisis_assess` — +5 optional params

**Params added:**
- `brent_price_usd: Optional[float]` — current oil price context
- `domestic_production_pct: Optional[float]` — self-sufficiency (0.0–1.0)
- `rm_usd_rate: Optional[float]` — USD/MYR exchange rate
- `refinery_margin_usd: Optional[float]` — downstream crack spread

**Computed values:**
- `price_dignity` — citizen affordability under oil price stress
- `energy_sovereignty` — domestic production buffer against global spikes
- `grid_integrity` — refinery margin stress indicator
- `maruah_score` — citizen dignity under energy stress
- `hold_triggered` — `price_dignity < 0.5 AND not Malaysia`

**Bug fixes from original proposal:**
1. `hedge_drag = abs(brent - rm_usd_rate*100)` → WRONG. Correct: `abs(brent - hedge_lock) / brent`
2. `refinery_stress` → NameError when `refinery_margin_usd=None`. Fix: default to `0.0`
3. `revenue_rm_impact` → dead code, removed

### `wealth_evaluate_prospect` — +5 optional params

**Params added:**
- `hedge_lock_usd: Optional[float]` — locked oil price vs spot exposure
- `rm_usd_rate: Optional[float]` — FX conversion rate
- `downstream_margin_usd: Optional[float]` — refinery margin squeeze
- `production_decline_rate: Optional[float]` — annual decline (e.g. 0.05 = 5%/yr)
- `lng_contract_price: Optional[float]` — JKM/HH gas price reference

**Key formula (corrected by OpenClaw):**
```python
effective_price = hedge_lock_usd if hedge_lock_usd else oil_price
hedge_drag = abs(oil_price - effective_price) / oil_price if oil_price != effective_price else 0.0
recovery_factor = 0.35 * max(0.5, 1.0 - (production_decline_rate * 4.5)) if production_decline_rate else 0.35
```

**Computed values:**
- `effective_price` — hedge-adjusted oil price
- `hedge_drag` — uncertainty band (F02 Truth)
- `net_cash_flow` — includes LNG delta + downstream cost
- `paradox_score` — danger signal (≥ 0.5 triggers HOLD)
- `hold_triggered` — `paradox >= 0.5 OR hedge_drag > 15% OR decline > 8%/yr`

---

## Status: PENDING APPLICATION

| Item | Status |
|------|--------|
| OpenClaw corrected patch | ✅ Delivered |
| `publish-image.yml` fix (GHCR_TOKEN removed) | ✅ Applied + pushed (`99e00ab`) |
| `energy_crisis_assess` code patch | ❌ NOT applied |
| `wealth_evaluate_prospect` code patch | ❌ NOT applied |
| GitHub Actions push for abstraction code | ❌ Blocked (403 GHCR) |

**Next:** When GitHub Actions GHCR push is fixed, these changes need to be committed to the code AND pushed. The workflow will rebuild + push the new image.

---

## Decision Point

Arif said "No new tools. Make it abstraction." — done via parameter enhancement, no new tool surface. This follows the rule: existing tools get optional params for backward compatibility.

**Requires:** Code patch to `/root/WEALTH/mcp/server.py` (energy_crisis_assess + wealth_evaluate_prospect functions) + commit + push → workflow → new image deployed.

**888_HOLD needed?** The code changes are on existing tools (backward compatible), not new surfaces. But container restart + image deploy is operational change → likely 888_HOLD for deploy, but the patch itself can be prepared autonomously and queued.