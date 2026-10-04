# v3 Live Model Pattern — Python source + JS port + cross-validation

The proven recipe for building an interactive live model on a static-shell page. First run: 2026-08-06, `/propa/` and `/malaysia/` subsidy paradox.

## Architecture

```
forge_work/<project>/model.py          ← Python source-of-truth (53 tests, unit-testable)
forge_work/<project>/v3-engine.js      ← JS port (loaded by browser, mirrors Python exactly)
forge_work/<project>/tests/cross-validate-js.js   ← Node harness: asserts JS matches Python
sites/arif-fazil.com/public/<route>/index.html     ← static shell with <script> inline
sites/arif-fazil.com/public/<route>/_charts/*.png  ← optional static charts (removed once model live)
```

## Python model structure (model.py)

Pure functions, no side effects, no I/O. Every function: docstring, units, defaults from sealed anchors.

```python
# Constants — from audited IFR, never change mid-session
BASE = {"pat": 45.4, "cffo": 85.2, "capex": 41.6, "net_cash_start": 82.8, ...}
DIVIDEND_CAP_PCT = 0.60
MOF_FLOOR = 20.0

# Piecewise-linear function anchored at specific Brent levels
def subsidy_bill_for(params):
    brent = params.get("brent", 85)
    if brent <= 50:   base = 3.0 + (brent - 40) * 0.5
    elif brent <= 65: base = 8.0 + (brent - 50) * 0.467
    elif brent <= 90: base = 15.0 + (brent - 65) * 1.0
    else:             base = 30.0 + (brent - 90) * 0.571
    # Modifiers — multiplier on the base
    iran_uplift = 1.0 + 0.10 * (iran_war / 50.0)
    reform_uplift = 1.0 + 0.02 * delay
    return round(min(base * iran_uplift * reform_uplift, CEILING) * 10) / 10
```

**Critical: piecewise continuity.** Compute slopes so f(x) matches at every breakpoint. If slopes don't align, the function is non-monotonic and produces visually jarring jumps when the user crosses a boundary. Use: `slope = (y2 - y1) / (x2 - x1)` at each segment, and verify `f(breakpoint)` from both sides.

## JS port (v3-engine.js)

Same API, same constants, no React dependency. Wrap in IIFE and export to `window.PetronasV3`:

```js
const V3 = {
  pat(p, idx) { ... },
  sub(p) { ... },
  htr(p) { ... },
  t10(p) { ... },
};
if (typeof window !== 'undefined') window.PetronasV3 = V3;
```

## Cross-validation (tests/cross-validate-js.js)

```js
const V3 = global.window.PetronasV3;
const cases = [
  { brent: 50, iran_war: 0, reform_delay_months: 0 },
  { brent: 85, iran_war: 0, reform_delay_months: 0 },
  ...
];
// Python expected values hardcoded or read from a JSON fixture
assert(Math.abs(V3.sub(p) - expected.sub) < 0.05);
assert(V3.t10(p) === expected.t10);
```

Run: `node tests/cross-validate-js.js`. Both Python and JS must agree.

## Embedding in static shell

Inline `<script>` in the `index.html`. Namespace all IDs with a 2-letter prefix (`pv-` for propa, `mv-` for malaysia). The script computes and draws on every slider `oninput`:

```js
function live() {
  const p = params(); // read all slider values
  const pat = V3.pat(p, 0);
  const sub = V3.sub(p);
  const htr = V3.htr(p);
  // update DOM readouts
  r_pat.textContent = 'RM' + pat.toFixed(1) + 'B';
  r_sub.textContent = 'RM' + sub.toFixed(1) + 'B';
  // update verdict colour + badge
  // draw chart via canvas
  drawChart(p);
}
ids.forEach(id => sels[id].addEventListener('input', live));
live(); // initial render
```

## Default-state neutrality rule

Page opens at the "comfortable" state, not the worst-case state. Proven on propa/malaysia:

- Default Brent: **$65** (not $85)
- Default Iran war: **0%** (not 50%)
- Default reform delay: **0 months** (not 8)

BULL/BASE/BEAR buttons load scenario presets — user-initiated, not default. A page that opens on red PARADOX is a UX failure because the visitor has no context for what they're looking at.

## Deployment

Same as any static shell edit: rsync to `/var/www/html/arif/<route>/` then verify:
1. `curl -sf https://arif-fazil.com/<route>/ | grep -c 'slider-IDs'` — engine elements present
2. `browser_navigate` → `browser_console` → assert default readout values match expectations
3. `browser_console` dispatching `new Event('input')` on a slider → assert verdict updates

## Pitfall: sibling's scen-btn collision

The old fan engine uses `<button class="scen-btn" data-scen="BASE">`. If the new engine also adds `<button class="scen-btn" data-scen="BASE">`, both respond to the same click. The old `querySelectorAll('.scen-btn')` event delegation picks up all buttons. Fix: namespace the new buttons with a data attribute and event delegation scoped to the new engine's container, or give them a distinct class (`pv-scen-btn`).
