# v3 Engine — Source Code Reference

The deployed model on /propa/ + /malaysia/ lives in two sibling files:

- **Python (canonical):** `/testbed/petronas_malaysia_v3/model.py`
- **JavaScript (browser):** `/testbed/petronas_malaysia_v3/v3-engine.js`

## Why two files

The Python file is the source of truth — unit tests run against it. The JS file is a hand-translated mirror for the browser canvas. They MUST stay in sync. The cross-validation script (`/testbed/tests/cross-validate-js.js`) loads the JS file and asserts 6 sentinel scenarios match Python to ±0.05. Both must pass before any deploy.

## Cross-validation sentinel (test before every deploy)

```
(50, 0, 0)    → sub=8.0,  t10=False, htr=0.40
(65, 0, 0)    → sub=15.0, t10=False, htr=0.75
(85, 0, 0)    → sub=45.0, t10=True,  htr=1.65
(85, 50, 8)   → sub=57.4, t10=True,  htr=2.11
(100, 100, 24)→ sub=75.0, t10=True,  htr=2.07 (capped)
(125, 100, 24)→ sub=75.0, t10=True,  htr=1.46 (capped)
```

If any sentinel shifts more than 0.05, the JS-Python pair has drifted.

## Subsidy curve anchor points (do NOT change without recalibrating against MoF)

| Brent | Subsidy (RM B, no modifiers) |
|---|---|
| $40 | 3.0 |
| $50 | 8.0 |
| $65 | 15.0 |
| $90 | 52.5 |
| $125 | 72.5 (capped) |

## Page-specific default state

Both pages open at: Brent $65, Iran war 0%, reform delay 0 → verdict TIGHT (yellow), hidden tax 0.75×, tripwire STANDBY. A user must drag Brent UP to discover the paradox.

## Deploy pattern

The JS engine is inlined into the HTML (not a separate script src). Each page sets Cache-Control: no-cache on the section, so the engine refreshes with the page load.