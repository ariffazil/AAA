# /world/vitals/ Transmission Engine — 4-panel sensitivity viz (Forged 2026-08-08)

## The directive

Arif: *"For the transmission engine trail slider, where is graph visualization to model that slider. Use ExxonMobil modeling toolkit if needed. Use all data visualization intelligence skills u have."*

Translation: the slider section must show the model, not just numbers. ExxonMobil's IR cash-flow sensitivity deck was the visual reference (tornado + waterfall + surface + scenarios).

## What was added

A 2×2 grid of pure SVG visualizations above the existing 4 sliders, live-updating on every slider `input` event:

```
┌────────────────────┬────────────────────┐
│ TORNADO            │ WATERFALL          │
│ ±1σ PAT impact     │ PAT → CFFO → ...   │
├────────────────────┼────────────────────┤
│ SURFACE            │ SCENARIOS          │
│ PAT(Brent, JKM)    │ Bull/Base/Bear     │
└────────────────────┴────────────────────┘
       4 sliders below (Brent, JKM, FX, Gold)
       6 output cells below (PAT, CFFO, FCF, Div, Gold RM/g, FCF-zero)
```

**No external dependencies.** Pure SVG via `document.createElementNS('http://www.w3.org/2000/svg', tag)`. CSP-friendly (no `cdn.jsdelivr.net`, no D3).

## Model equations (SPEC, non-scoring — sourced from the sealed transmission audit)

```js
const pat = 45.4 + (b - 85) * 0.6 + (j - 14) * 0.6;        // RM B
const cffo = pat * 1.88;                                   // FY25 ratio
const capex = 46;                                          // RM B guidance
const fcf = cffo - capex - div;
const div = Math.max(Math.min(0.6 * pat, pat), Math.min(20, 0.6 * pat));
// div = 60% PAT cap, with RM20B MoF floor where affordable
```

## HTML scaffolding (the 4 panels)

Insert ABOVE the existing `<div class="sliders">` block, INSIDE the existing `<div class="engine">` wrapper. Replace the engine block's `style` attribute to remove default padding (the panels need to span full width):

```html
<div class="engine" style="padding:0;overflow:hidden">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line)">
    <div style="background:var(--panel);padding:20px">
      <div class="mono" style="font-size:10px;letter-spacing:.18em;color:var(--gold);margin-bottom:10px">▎ TORNADO · PAT SENSITIVITY (RM B / ±1σ)</div>
      <svg id="viz-tornado" viewBox="0 0 500 220" style="width:100%;height:220px;display:block"></svg>
      <div class="mono" style="font-size:10px;color:var(--faint);margin-top:6px">Each bar = ±1σ swing of slider → PAT impact. ExxonMobil IR convention.</div>
    </div>
    <div style="background:var(--panel);padding:20px">
      <div class="mono" style="font-size:10px;letter-spacing:.18em;color:var(--gold);margin-bottom:10px">▎ CASH-FLOW WATERFALL · RM B</div>
      <svg id="viz-waterfall" viewBox="0 0 500 220" style="width:100%;height:220px;display:block"></svg>
      <div class="mono" style="font-size:10px;color:var(--faint);margin-top:6px">Live: every slider movement redraws PETRONAS cash bridge.</div>
    </div>
    <div style="background:var(--panel);padding:20px">
      <div class="mono" style="font-size:10px;letter-spacing:.18em;color:var(--gold);margin-bottom:10px">▎ SURFACE · PAT = f(BRENT, JKM) RM B</div>
      <svg id="viz-surface" viewBox="0 0 500 220" style="width:100%;height:220px;display:block"></svg>
      <div class="mono" style="font-size:10px;color:var(--faint);margin-top:6px">Two-variable sensitivity. ✕ = current (Brent, JKM). Filled bands = PAT isolines.</div>
    </div>
    <div style="background:var(--panel);padding:20px">
      <div class="mono" style="font-size:10px;letter-spacing:.18em;color:var(--gold);margin-bottom:10px">▎ SCENARIO PATHS · 12-MONTH RM B</div>
      <svg id="viz-scenarios" viewBox="0 0 500 220" style="width:100%;height:220px;display:block"></svg>
      <div class="mono" style="font-size:10px;color:var(--faint);margin-top:6px">Base $85 brent / Bull $110 / Bear $55. PAT walk per quarter.</div>
    </div>
  </div>

  <!-- existing sliders block follows here, with padding:24px -->
  <div class="sliders" style="padding:24px">
    <div class="sl">...</div>  <!-- 4 sliders as before -->
  </div>
  <div class="outputs" style="border-top:1px solid var(--line)">
    <!-- 6 output cells as before -->
  </div>
</div>
```

## JS contract — pure SVG, zero dependencies

Insert the viz code in the `<script>` block **AFTER** the existing `engine()` function and the `engine();` init call. Why: the viz code reads `$('s-brent').value` etc. via the `$ = id => document.getElementById(id)` helper. If you insert before that, `ReferenceError: $ is not defined` and the whole script dies silently.

```js
// ═══ EXXONMOBIL IR-STYLE SENSITIVITY VISUALIZATION ═══
// Insert AFTER engine(); init call. Pure SVG, no D3 dependency.

const VIZ = {
  W: 500, H: 220,
  m: { t: 25, r: 15, b: 35, l: 50 },
  get cw() { return this.W - this.m.l - this.m.r; },
  get ch() { return this.H - this.m.t - this.m.b; },
};

function svgEl(tag, attrs) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  return el;
}

// drawGrid returns the group it built. Callers MUST store it as `root` (see pitfall #1).
function drawGrid(svg, xTicks, yTicks, xLabel, yLabel) {
  svg.innerHTML = '';
  const g = svgEl('g', {});                              // inner `g` — used inside this function only
  yTicks.forEach(({y, label, color}) => {
    g.appendChild(svgEl('line', { x1: VIZ.m.l, y1: y, x2: VIZ.W - VIZ.m.r, y2: y, stroke: color || '#1c2634', 'stroke-width': 0.5 }));
    const t = svgEl('text', { x: VIZ.m.l - 6, y: y + 4, fill: '#7c8b9e', 'font-size': 9, 'text-anchor': 'end', 'font-family': 'IBM Plex Mono, monospace' });
    t.textContent = label;
    g.appendChild(t);                                     // inner scope: g.appendChild
  });
  xTicks.forEach(({x, label}) => {
    const t = svgEl('text', { x, y: VIZ.H - VIZ.m.b + 18, fill: '#7c8b9e', 'font-size': 9, 'text-anchor': 'middle', 'font-family': 'IBM Plex Mono, monospace' });
    t.textContent = label;
    g.appendChild(t);                                     // inner scope: g.appendChild
  });
  g.appendChild(svgEl('line', { x1: VIZ.m.l, y1: VIZ.m.t, x2: VIZ.m.l, y2: VIZ.H - VIZ.m.b, stroke: '#263244', 'stroke-width': 1 }));
  g.appendChild(svgEl('line', { x1: VIZ.m.l, y1: VIZ.H - VIZ.m.b, x2: VIZ.W - VIZ.m.r, y2: VIZ.H - VIZ.m.b, stroke: '#263244', 'stroke-width': 1 }));
  if (xLabel) {
    const t = svgEl('text', { x: VIZ.W / 2, y: VIZ.H - 2, fill: '#4a586a', 'font-size': 8, 'text-anchor': 'middle', 'font-family': 'IBM Plex Mono, monospace' });
    t.textContent = xLabel;
    g.appendChild(t);
  }
  if (yLabel) {
    const t = svgEl('text', { x: 8, y: VIZ.H / 2, fill: '#4a586a', 'font-size': 8, 'text-anchor': 'middle', 'font-family': 'IBM Plex Mono, monospace', transform: `rotate(-90, 8, ${VIZ/2})` });
    t.textContent = yLabel;
    g.appendChild(t);
  }
  svg.appendChild(g);
  return g;                                                // callers assign: const root = drawGrid(...)
}

function yMap(v, min, max) { return VIZ.H - VIZ.m.b - ((v - min) / (max - min)) * VIZ.ch; }

// ─── 1. TORNADO ───
function drawTornado(svg) {
  const b = parseFloat($('s-brent').value), j = parseFloat($('s-jkm').value);
  const ranges = [
    { name: 'BRENT', sigma: 10, impact: 0.6 * 10, color: '#57d98e' },
    { name: 'JKM',   sigma: 4,  impact: 0.6 * 4,  color: '#4ecdc4' },
    { name: 'USD/MYR', sigma: 0.3, impact: 0, color: '#6aa8ff' },
    { name: 'GOLD',  sigma: 500, impact: 0, color: '#e8b64c' },
  ];
  const maxY = Math.max(...ranges.map(r => r.impact)) * 1.4 || 10;
  const yTicks = [0, Math.round(maxY/2), Math.round(maxY)].map(v => ({ y: yMap(v, 0, maxY), label: v > 0 ? '+'+v : '0' }));
  const xTicks = ranges.map((r, i) => ({ x: VIZ.m.l + (i + 0.5) * (VIZ.cw / 4), label: r.name }));
  const root = drawGrid(svg, xTicks, yTicks, '', 'RM B');
  ranges.forEach((r, i) => {
    const cx = VIZ.m.l + (i + 0.5) * (VIZ.cw / 4);
    const bw = VIZ.cw / 5;
    const barH = Math.min(VIZ.ch, (r.impact / maxY) * VIZ.ch);
    root.appendChild(svgEl('rect', { x: cx - bw/2, y: yMap(r.impact, 0, maxY), width: bw, height: barH, fill: r.color, opacity: 0.8, rx: 3 }));
    const val = svgEl('text', { x: cx, y: yMap(r.impact, 0, maxY) - 6, fill: r.color, 'font-size': 10, 'text-anchor': 'middle', 'font-family': 'IBM Plex Mono, monospace', 'font-weight': 'bold' });
    val.textContent = r.impact > 0 ? '+' + r.impact.toFixed(1) : '0';
    root.appendChild(val);
  });
}

// ─── 2. WATERFALL ───
function drawWaterfall(svg) {
  const b = parseFloat($('s-brent').value), j = parseFloat($('s-jkm').value);
  const pat = 45.4 + (b - 85) * 0.6 + (j - 14) * 0.6;
  const cffo = pat * 1.88, capex = 46;
  const fcf = cffo - capex;
  const div = Math.max(Math.min(0.6 * pat, pat), Math.min(20, 0.6 * pat));
  const stages = [
    { name: 'PAT',   value: pat,   running: pat,    color: '#e8b64c', type: 'pos' },
    { name: 'CFFO',  value: cffo,  running: cffo,   color: '#4ecdc4', type: 'pos' },
    { name: 'CAPEX', value: -capex, running: fcf,  color: '#ff5d5d', type: 'neg' },
    { name: 'FCF',   value: fcf,   running: fcf,    color: '#6aa8ff', type: 'total' },
    { name: 'DIV',   value: -div,  running: fcf-div,color: '#ffb84d', type: 'neg' },
    { name: 'RETAIN',value: fcf-div,running: fcf-div,color: fcf-div>=0?'#57d98e':'#ff5d5d', type: 'total' },
  ];
  const maxV = Math.max(...stages.map(s => Math.abs(s.running)), Math.abs(pat), cffo, capex, div) * 1.2 || 100;
  const yTicks = [0, Math.round(maxV/2), Math.round(maxV)].map(v => ({ y: yMap(v, 0, maxV), label: v.toFixed(0) }));
  const xTicks = stages.map((s, i) => ({ x: VIZ.m.l + (i + 0.5) * (VIZ.cw / stages.length), label: s.name }));
  const root = drawGrid(svg, xTicks, yTicks, '', 'RM B');
  stages.forEach((s, i) => {
    const cx = VIZ.m.l + (i + 0.5) * (VIZ.cw / stages.length);
    const bw = VIZ.cw / stages.length * 0.6;
    let yTop, yBot;
    if (s.type === 'pos') {
      yTop = yMap(Math.abs(s.value), 0, maxV); yBot = yMap(0, 0, maxV);
    } else if (s.type === 'neg') {
      yTop = yMap(s.running + Math.abs(s.value), 0, maxV); yBot = yMap(s.running, 0, maxV);
    } else {
      yTop = yMap(s.running, 0, maxV); yBot = yMap(0, 0, maxV);
    }
    const barH = Math.max(1, Math.abs(yBot - yTop));
    root.appendChild(svgEl('rect', { x: cx - bw/2, y: Math.min(yTop, yBot), width: bw, height: barH, fill: s.color, opacity: 0.85, rx: 3 }));
    if (i < stages.length - 1 && s.type !== 'total') {
      const nextX = VIZ.m.l + (i + 1.5) * (VIZ.cw / stages.length);
      root.appendChild(svgEl('line', { x1: cx + bw/2, y1: yMap(s.running, 0, maxV), x2: nextX - bw/2, y2: yMap(s.running, 0, maxV), stroke: '#4a586a', 'stroke-width': 0.8, 'stroke-dasharray': '4,2' }));
    }
    const val = svgEl('text', { x: cx, y: Math.max(12, yTop - 6), fill: s.color, 'font-size': 10, 'text-anchor': 'middle', 'font-family': 'IBM Plex Mono, monospace', 'font-weight': 'bold' });
    val.textContent = s.value.toFixed(1);
    root.appendChild(val);
  });
}

// ─── 3. SURFACE: PAT as f(BRENT, JKM) ───
function drawSurface(svg) {
  const bNow = parseFloat($('s-brent').value), jNow = parseFloat($('s-jkm').value);
  const bMin = 40, bMax = 120, jMin = 6, jMax = 25;
  const patAt = (b, j) => 45.4 + (b - 85) * 0.6 + (j - 14) * 0.6;
  const isolines = [
    { pat: 0, color: '#ff5d5d' },
    { pat: 20, color: '#ffb84d' },
    { pat: 45.4, color: '#e8b64c', dash: '' },
    { pat: 60, color: '#4ecdc4' },
    { pat: 80, color: '#6aa8ff' },
    { pat: 100, color: '#57d98e' },
  ];
  const yMin = -30, yMax = 120;
  const yTicks = [yMin, 0, Math.round(yMax/2), yMax].map(v => ({ y: yMap(v, yMin, yMax), label: v }));
  const xTicks = [
    { x: VIZ.m.l, label: bMin },
    { x: (VIZ.m.l+VIZ.W-VIZ.m.r)/2, label: ((bMin+bMax)/2).toFixed(0) },
    { x: VIZ.W - VIZ.m.r, label: bMax },
  ];
  const root = drawGrid(svg, xTicks, yTicks, 'BRENT USD/bbl', 'PAT RM B');
  const jToY = j => VIZ.m.t + (1 - (j - jMin) / (jMax - jMin)) * VIZ.ch;
  isolines.forEach(iso => {
    const j1 = jMin, j2 = jMax;
    const b1 = (iso.pat - 45.4 - (j1 - 14) * 0.6) / 0.6 + 85;
    const b2 = (iso.pat - 45.4 - (j2 - 14) * 0.6) / 0.6 + 85;
    const bToX = b => VIZ.m.l + ((b - bMin) / (bMax - bMin)) * VIZ.cw;
    if (b1 >= bMin && b1 <= bMax || b2 >= bMin && b2 <= bMax) {
      const x1 = Math.max(VIZ.m.l, Math.min(VIZ.W - VIZ.m.r, bToX(b1)));
      const x2 = Math.max(VIZ.m.l, Math.min(VIZ.W - VIZ.m.r, bToX(b2)));
      root.appendChild(svgEl('line', { x1, y1: jToY(j1), x2, y2: jToY(j2), stroke: iso.color, 'stroke-width': 1.2, opacity: 0.7, 'stroke-dasharray': iso.dash || '6,3' }));
      const lbl = svgEl('text', { x: (x1+x2)/2 + 5, y: (jToY(j1)+jToY(j2))/2 + 3, fill: iso.color, 'font-size': 8, 'font-family': 'IBM Plex Mono, monospace' });
      lbl.textContent = iso.pat;
      root.appendChild(lbl);
    }
  });
  // Current position cross
  const cx = VIZ.m.l + ((bNow - bMin) / (bMax - bMin)) * VIZ.cw;
  const cy = jToY(jNow);
  root.appendChild(svgEl('circle', { cx, cy, r: 6, fill: 'none', stroke: '#e8b64c', 'stroke-width': 2 }));
  root.appendChild(svgEl('circle', { cx, cy, r: 2, fill: '#e8b64c' }));
  const cPat = patAt(bNow, jNow);
  const lbl = svgEl('text', { x: cx + 10, y: cy - 8, fill: '#e8b64c', 'font-size': 10, 'font-family': 'IBM Plex Mono, monospace', 'font-weight': 'bold' });
  lbl.textContent = cPat.toFixed(1);
  root.appendChild(lbl);
}

// ─── 4. SCENARIO PATHS ───
function drawScenarios(svg) {
  const bNow = parseFloat($('s-brent').value);
  const scenarios = [
    { name: 'Bull $110', bStart: bNow, bEnd: 110, color: '#57d98e', dash: '' },
    { name: 'Base $85',  bStart: bNow, bEnd: 85,  color: '#e8b64c', dash: '' },
    { name: 'Bear $55',  bStart: bNow, bEnd: 55,  color: '#ff5d5d', dash: '' },
  ];
  const quarters = ['Now', 'Q1', 'Q2', 'Q3', 'Q4'];
  const patAt = (b, j) => 45.4 + (b - 85) * 0.6 + (j - 14) * 0.6;
  const j = parseFloat($('s-jkm').value);
  const allPts = scenarios.flatMap(s => quarters.map((_, i) => patAt(s.bStart + (s.bEnd - s.bStart) * (i / 4), j)));
  const yMin = Math.min(...allPts) - 10;
  const yMax = Math.max(...allPts) + 10;
  const yTicks = [Math.round(yMin), Math.round((yMin+yMax)/2), Math.round(yMax)].map(v => ({ y: yMap(v, yMin, yMax), label: v }));
  const xTicks = quarters.map((q, i) => ({ x: VIZ.m.l + (i / 4) * VIZ.cw, label: q }));
  const root = drawGrid(svg, xTicks, yTicks, '', 'PAT RM B');
  if (yMin < 0 && yMax > 0) {
    root.appendChild(svgEl('line', { x1: VIZ.m.l, y1: yMap(0, yMin, yMax), x2: VIZ.W - VIZ.m.r, y2: yMap(0, yMin, yMax), stroke: '#ff5d5d', 'stroke-width': 0.8, 'stroke-dasharray': '4,2' }));
  }
  scenarios.forEach(sc => {
    const pts = quarters.map((_, i) => {
      const bInterp = sc.bStart + (sc.bEnd - sc.bStart) * (i / 4);
      const pat = patAt(bInterp, j);
      return `${VIZ.m.l + (i / 4) * VIZ.cw},${yMap(pat, yMin, yMax)}`;
    }).join(' ');
    root.appendChild(svgEl('polyline', { points: pts, fill: 'none', stroke: sc.color, 'stroke-width': 2, 'stroke-dasharray': sc.dash || '' }));
    const last = pts.split(' ').pop().split(',');
    const lbl = svgEl('text', { x: +last[0] + 4, y: +last[1] - 6, fill: sc.color, 'font-size': 9, 'text-anchor': 'start', 'font-family': 'IBM Plex Mono, monospace', 'font-weight': 'bold' });
    lbl.textContent = sc.name;
    root.appendChild(lbl);
    root.appendChild(svgEl('circle', { cx: +pts.split(' ')[0].split(',')[0], cy: +pts.split(' ')[0].split(',')[1], r: 3, fill: sc.color }));
  });
}

// ─── Unified redraw + hook into slider events ───
function drawAllViz() {
  drawTornado(document.getElementById('viz-tornado'));
  drawWaterfall(document.getElementById('viz-waterfall'));
  drawSurface(document.getElementById('viz-surface'));
  drawScenarios(document.getElementById('viz-scenarios'));
}

['s-brent','s-jkm','s-fx','s-gold'].forEach(i => {
  $(i).addEventListener('input', () => { setTimeout(drawAllViz, 0); });
});

drawAllViz();  // initial render — also a smoke test for syntax
```

## Pitfalls hit during this forge (verified 2026-08-08)

### 1. Blanket `.replace()` broke inner function scope

`drawGrid` returns the inner `<g>` group. The outer scope names it `const root = drawGrid(...)`. Inside `drawGrid`, `g` is the local group. After my first `drawTornado` etc., I named the outer variable `g` too (collision-free at the call site because of function scoping), then did a blanket `g.appendChild` → `root.appendChild` rewrite for clarity. **Wrong.** The rewrite also touched `drawGrid`'s internal `g.appendChild(...)` calls, which then became `root.appendChild(...)` — but `root` doesn't exist in `drawGrid`'s scope → `ReferenceError: root is not defined` at runtime.

Symptom: `browser_console` shows `console_messages: []` with empty `js_errors` array (browser swallows the page-level exception and continues). But `document.getElementById('viz-tornado')?.children.length === 0` and the 6 output cells stay `–` (engine() never ran either because the script died before its `engine();` call).

Fix: scope the replacement to the outer functions only, not into `drawGrid`:

```python
start = html.find('function drawGrid(')
end = html.find('\nfunction drawTornado(', start)
drawGrid_func = html[start:end]
drawGrid_func = drawGrid_func.replace('root.appendChild(', 'g.appendChild(')  # undo in drawGrid
html = html[:start] + drawGrid_func + html[end:]
```

### 2. JS injection order: insert viz AFTER `engine();` init call

The viz code references `$('s-brent').value` etc. via the `$ = id => document.getElementById(id)` helper. If the viz code is inserted in the script block BEFORE the `const $ = ...` declaration or BEFORE the `engine();` init call, those identifiers are `undefined` and the entire script throws. The browser then renders the page with `–` placeholders and no chart work.

**Rule:** insert the viz block immediately AFTER `engine();` line in the existing `<script>` block. Validate with `node --check` before deploy.

### 3. Validate inline JS before deploy

Extract the largest `<script>...</script>` block (use Python regex `re.finditer(r'<script>([\s\S]*?)</script>', html)`, pick the biggest match), write to `/tmp/check.js`, run `node --check /tmp/check.js`. Catches `const g` redeclaration, stray braces, syntax errors before the browser does.

### 4. Browser cache shows stale JS after deploy

`browser_console` can run old code even after the server serves the fix — Cloudflare's HTML edge cache holds ~30s, and a stale in-memory `window.charts`/`engine` may persist across `browser_navigate` if the URL is too similar. Verify with `curl -s URL | grep <new-marker>` (server side, bypasses browser cache), AND navigate with a fresh unique query param like `?cb=forcefresh2026`. The `n=88888` style also works.

### 5. Validate via console probe

```js
(() => {
  try { drawTornado(document.getElementById('viz-tornado')); return 'ok'; }
  catch(e) { return e.message + ' | ' + (e.stack||'').split('\n').slice(0,2).join(' | '); }
})()
```

If you see `ReferenceError: $ is not defined`, you injected before the `$` helper. If you see `root is not defined`, see pitfall #1.

## Verification script (browser)

```js
JSON.stringify({
  outputs: {
    pat:  document.getElementById('o-pat')?.textContent,
    cffo: document.getElementById('o-cffo')?.textContent,
    fcf:  document.getElementById('o-fcf')?.textContent,
  },
  viz: {
    tornado:    document.getElementById('viz-tornado')?.children[0]?.children.length,
    waterfall:  document.getElementById('viz-waterfall')?.children[0]?.children.length,
    surface:    document.getElementById('viz-surface')?.children[0]?.children.length,
    scenarios:  document.getElementById('viz-scenarios')?.children[0]?.children.length,
  }
}, null, 2)
```

Expected on first load: outputs have numbers (PAT/CFFO/FCF all `XX.X`), viz panels have ~20-30 inner children each (grid lines + ticks + bars + labels + isolines + scenarios + markers). On slider drag, both numbers AND children count update live.

## Slider reactivity check

```js
(() => {
  const b = document.getElementById('s-brent');
  b.value = 110;
  b.dispatchEvent(new Event('input'));
  return 'dispatched — check outputs in next tick';
})()
```

After this fires, expected: `o-pat` jumps from ~46 → ~60 (Brent $87 → $110 = +$23 swing × 0.6 ≈ +RM13.8B), `o-cffo` from ~88 → ~113, `o-fcf` from ~14 → ~31. Tornado BRENT bar grows visibly.

## What this skill does NOT cover

- Adding the FCF-zero (red line at PAT that drops FCF to 0) as an interactive scenario — currently static text.
- Per-quarter dividend scenario with 70.5% extraction tripwire overlay (the Pacemaker panel below the engine has it; could mirror here).
- WebGL / ShaderToy rendering — pure SVG is fine for the slider count and gives crisp print-quality exports.