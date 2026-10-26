# Model Card — dalio_debt_cycle_v1

- **model_id:** dalio_debt_cycle_v1
- **epistemic_class:** INTERPRETATION
- **role:** causal_prior
- **decision_authority:** none
- **execution_authority:** none
- **max_ensemble_weight:** 0.25
- **calibration_status:** UNVALIDATED
- **required_countermodels:** sectoral_balances_v1, financial_cycle_v1, inflation_channels_v1, distribution_power_v1
- **provenance:** Ray Dalio, "How the Economic Machine Works" (video 2013; essay 2008, economicprinciples.org). Audit session 2026-10-09; transcript retrieval blocked (cloud-IP bot wall), content reconstructed from public template — DER/INTERPRETATION, not verbatim.

## Variables

Spending (money + credit), income, credit growth, debt-to-income, debt-service ratio, interest rate, asset prices/collateral, productivity growth.

## Claimed mechanisms

1. One party's spending = another party's income; credit pulls spending forward and creates matching balance-sheet entries.
2. **Short-term debt cycle (~5–8 yr):** cheap credit → spending up → inflation → central bank raises rates → recession → rates cut → repeat.
3. **Long-term debt cycle (~75–100 yr):** debt outgrows income until deleveraging. Four channels: (a) spending cuts (deflationary), (b) debt reduction/default, (c) wealth redistribution (political stress), (d) money creation ("beautiful deleveraging" when dosed so income growth > interest burden).
4. Productivity growth is the only non-cyclical long-run driver (rises steadily; "doesn't fluctuate much").

## Three rules of thumb

1. Don't let debt rise faster than income.
2. Don't let income rise faster than productivity.
3. Do all you can to raise productivity.

## Assumptions

- Economy describable as transactions between self-interested agents; credit is the dominant cyclical variable.
- Central bank rate policy is the primary lever on the short cycle.
- Cycle durations are approximate regularities, not constants.

## Exclusions

- No equations; dosages (e.g. money-creation amount) unparameterized.
- Representative-agent aggregation (sectoral heterogeneity suppressed).
- Simplified monetary transmission; "printing money" conflates reserves/deposits/transfers.
- Distribution treated late; open-economy constraints thin.

## Falsifiers

- BIS financial-cycle research: cycles often 10–20 yr, hard to identify in real time → fixed-clock reading fails (rule: never advance regime by elapsed time alone).
- Sectoral-balance counter-model: sectors moving in opposite directions breaks the aggregate narrative.
- Bank-of-England endogenous-money literature: reserve-multiplier story wrong in detail (lending creates deposits; BoE 2014).
- Any calibration window where regime probabilities from this lens underperform countermodels → weight reduced.

## Weight-increase gate

Weight > 0.25 requires: calibration score (Brier/log) vs counter-models over ≥1 full revision cycle, human-reviewed benchmark, and explicit sovereign sign-off.
