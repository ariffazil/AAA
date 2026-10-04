# Transmission Engine 4-panel Sensitivity Viz

**Live file:** `/var/www/html/arif/world/vitals/index.html` (Layer 5, `#engine` section)
**Forged:** 2026-08-08
**Model coefficients:** `PAT = 45.4 + (Brent−85)×0.6 + (JKM−14)×0.6` · `CFFO = PAT×1.88` · capex RM46B · dividend capped 60% PAT, floor RM20B.

## The four panels

A 2×2 grid of pure-SVG visualizations placed ABOVE the slider grid (chart-hero principle). Each redraws on every `input` event of any slider.

### 1. TORNADO (top-left)

Horizontal bars showing per-slider ±1σ PAT sensitivity. Each bar = the swing in RM B if the input moves ±1σ.

| Variable | σ | Impact (RM B) | Color |
|---|---|---|---|
| BRENT | $10 | ±6.0 | green `#57d98e` |
| JKM | $4/MMBtu | ±2.4 | teal `#4ecdc4` |
| USD/MYR | 0.3 | 0 | blue `#6aa8ff` |
| GOLD | $500/oz | 0 | gold `#e8b64c` |

USD/MYR and GOLD show as 0 because they don't enter the PAT equation (they only affect the Gold-RM/gram derived value). This is honest model construction — don't fabricate impact for inputs that don't matter.

### 2. WATERFALL (top-right)

PAT → CFFO → −CAPEX → FCF → −DIV → RETAIN cascade with dashed connectors between stages. Stages use `yTop/yBot` logic: positive stages draw from 0 upward; negative stages (CAPEX, DIV) draw from the running total downward; totals (FCF, RETAIN) span the full height.

```
PAT(45.4 base)  ┐
CFFO(PAT×1.88)   │  green
CAPEX(−46)       │  red dashed-connector to FCF
FCF              ┘  blue (total)
DIV(−60%PAT capped, RM20 floor)  ┐ amber dashed-connector
REMAINING                          ┘ green/red (total)
```

### 3. SURFACE (bottom-left)

PAT isolines on (Brent, JKM) plane, X-axis Brent $40–$120, Y-axis JKM $6–$25. Five iso-lines at PAT = 0, 20, 45.4 (base), 60, 80, 100. Current position as ✕ crosshair with `cPat` label.

Line equation: `B = (PAT - 45.4 - (J-14)*0.6) / 0.6 + 85`. Plot as a line from (B, j=6) to (B, j=25), clipped to chart bounds.

### 4. SCENARIOS (bottom-right)

3 trajectories: Bull $110 / Base $85 / Bear $55, interpolated linearly from current Brent to target across 5 points (Now, Q1, Q2, Q3, Q4). Each is a polyline with stroke matching sentiment color. Start marker at current position, end-label at Q4.

## Implementation sketch

```js
const VIZ = { W: 500, H: 220, m: { t: 25, r: 15, b: 35, l: 50 },
              get cw() { return this.W - this.m.l - this.m.r; },
              get ch() { return this.H - this.m.t - this.m.b; } };

function svgEl(tag, attrs) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  return el;
}

function drawGrid(svg, xTicks, yTicks, xLabel, yLabel) {
  svg.innerHTML = '';
  const g = svgEl('g', {});                    // ← LOCAL g, used for grid lines
  yTicks.forEach(({y, label, color}) => {
    g.appendChild(svgEl('line', { x1: VIZ.m.l, y1: y, ... }));
    const t = svgEl('text', ...);
    g.appendChild(t);                           // ← LOCAL g.appendChild (correct)
  });
  // ... axis lines, axis labels, return g
  return g;                                    // ← caller stores as `root`
}

function drawTornado(svg) {
  const root = drawGrid(svg, xTicks, yTicks);  // ← OUTER scope root
  ranges.forEach(r => {
    root.appendChild(svgEl('rect', ...));      // ← OUTER root.appendChild
  });
}
```

**Critical:** drawGrid's internal `g` and the caller-scope `root` reference the SAME DOM node (the `<g>` returned from drawGrid). Both `.appendChild` calls work — they target the same node. The trap is renaming one without the other.

## Validation checklist

1. `node --check /tmp/check.js` — extracts `<script>` blocks first via Python regex, then validates syntax
2. `browser_console` after load: `document.getElementById('viz-tornado').children[0].children.length` should be > 20
3. `outputs` should populate: `o-pat` etc. show numbers, not `–`
4. Trigger slider input event: `document.getElementById('s-brent').value = 110; .dispatchEvent(new Event('input'))` — outputs should redraw, viz child counts should hold steady

## Pitfalls hit while building this (all solved, now embedded in parent skill)

1. **JS injection order:** viz code injected before `const $=id=>...` definition → `engine is not a function`. Fixed by moving viz block to after the `engine();` call line.
2. **Variable shadowing:** `const g` reused in nested functions → node `--check` fails "Identifier 'g' has already been declared". Renamed outer scope to `root`.
3. **Blanket rename error:** `g.appendChild` → `root.appendChild` also rewrote drawGrid's internal `g.appendChild` → `root is not defined`. Fixed by scoping replacement to function body boundaries.
4. **Browser cache:** after patch, browser still shows old version. Fix: `?cb=forcefresh<epoch>` with a unique number.