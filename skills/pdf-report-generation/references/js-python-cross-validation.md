# JS ↔ Python cross-validation for live interactive models

Proven 2026-08-06 on the `petronas_malaysia_v3` model (8-slider ExxonMobil IR
engine + subsidy paradox). Use whenever a JS engine on a live site page must
mirror Python math exactly.

## Why this matters

A live site page embeds a `<script>` block that recomputes the same numbers
as a Python model. Two implementations of the same math drift if anyone
touches one without the other. Unit-test the Python. Cross-validate the
JS against the Python. Deploy both together.

## The pattern

### 1. Pure-Python model with unit tests

```python
# petronas_malaysia_v3/model.py
def subsidy_bill_for(params):
    brent = params["brent"]
    if brent <= 50:
        return 3.0 + (brent - 40) * 0.5
    ...

def tripwire_10_engaged(params):
    return div_for(pat_compute(params, 0)) > 0 and \
           subsidy_bill_for(params) / div_for(pat_compute(params, 0)) > 1.0
```

```python
# tests/test_model_v3.py — 53 tests covering edge cases
def test_subsidy_monotonic_in_brent():
    subs = [subsidy_bill_for({"brent": b, "iran_war": 0, "reform_delay_months": 0})
            for b in range(40, 126, 2)]
    for i in range(1, len(subs)):
        assert subs[i] >= subs[i-1]   # NO discontinuities

def test_tripwire_engaged_at_high_oil():
    assert tripwire_10_engaged({"brent": 110, "iran_war": 0, "reform_delay_months": 0}) is True
```

### 2. JS port as IIFE module — same constants, same math

```js
// petronas_malaysia_v3/v3-engine.js
const V3 = {
  SUBSIDY_HARD_CEILING: 75.0,
  sub(p) {
    const brent = p.brent || 85, iran = p.iran_war || 0, delay = p.reform_delay_months || 0;
    let base;
    if (brent <= 50) base = 3.0 + (brent - 40) * 0.5;
    // ... identical to Python
    return Math.round(Math.min(base * iu * ru, this.SUBSIDY_HARD_CEILING) * 10) / 10;
  },
  t10(p) {
    const d = this.div(this.pat(p, 0));
    const s = this.sub(p);
    return d > 0 && (s/d) > 1.0;
  }
};

if (typeof window !== 'undefined') {
  window.PetronasV3 = { ... };   // for browser embed
}
```

### 3. Node cross-validation script

```js
// tests/cross-validate-js.js
const fs = require('fs');
const engineSource = fs.readFileSync(
  path.join(__dirname, '..', 'petronas_malaysia_v3', 'v3-engine.js'),
  'utf8'
);
global.window = {};
eval(engineSource);   // IIFE runs, populates window.PetronasV3
const V3 = global.window.PetronasV3;

// Sample parameter sets — same sets the Python tests assert
const cases = [
  { brent: 50,  iran_war: 0,   reform_delay_months: 0 },
  { brent: 85,  iran_war: 50,  reform_delay_months: 8 },
  { brent: 100, iran_war: 100, reform_delay_months: 24 },
];

const expected = { /* from Python tests */ };
let fail = 0;
for (const p of cases) {
  const sub = V3.subsidy_bill_for(p);
  const t10 = V3.tripwire_10_engaged(p);
  if (Math.abs(sub - expected.sub) > 0.05) fail++;
  if (t10 !== expected.t10) fail++;
}
process.exit(fail > 0 ? 1 : 0);
```

Run: `node tests/cross-validate-js.js` → exits 0 if JS == Python, exits 1 if
drifted. Add to CI / pre-deploy hook.

### 4. Inline embed in the live page

```html
<!-- public/propa/index.html -->
<section id="subsidy-paradox" data-version="propa-v3-live-model">
  <!-- sliders, readouts, chart canvas ... -->
</section>

<script>
(function(){
  const V3 = { /* inline copy of v3-engine.js */ };
  // ... sliders + chart rendering + tripwire badge
})();
</script>
```

DO NOT load `v3-engine.js` as a separate file — the inline `<script>` avoids
CORS/cache issues on the static page and ensures the model is shipped with
the page.

## Test counts that prove the pattern (2026-08-06)

- `tests/test_model_v3.py` — 53 unit tests pass (subsidy bill math, tripwire
  engagement, PAT elasticity, cap-floor collision, edge cases)
- `tests/cross-validate-js.js` — 6 cross-validation tests pass (Python ==
  JS within 0.05 tolerance)
- Deploy gate `bash scripts/verify-pages.sh https://arif-fazil.com
  /root/arif-fazil.com/sites/arif-fazil.com/dist` — 117/117 pages pass

If either test count drops, a future agent broke the parity — re-derive
JS from Python before shipping.

## What this catches

| Drift case | Caught by |
|---|---|
| Wrong slope coefficient in JS piecewise-linear | `test_subsidy_monotonic_in_brent` + cross-validate |
| Math operator difference (Python `//` vs JS `Math.trunc`) | Unit test on boundary values |
| Cap applied too early in JS | Cross-validate at extreme param values |
| Slider default value drift (85 vs 80) | UI smoke + human readout assertion |
| Tripwire engagement threshold change | `test_tripwire_engaged_*` |
| Iran war modifier direction reversed | Cross-validate at 0 vs 100% |

## Files

- `petronas_malaysia_v3/model.py` — canonical Python model (53 unit tests)
- `petronas_malaysia_v3/v3-engine.js` — JS port (6 cross-validate tests)
- `tests/test_model_v3.py` — pytest suite
- `tests/cross-validate-js.js` — Node cross-validate runner