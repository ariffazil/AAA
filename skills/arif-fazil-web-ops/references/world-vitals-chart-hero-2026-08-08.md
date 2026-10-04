# /world/vitals/ chart-hero pattern (Forged 2026-08-08, shipped 2026-08-08)

> **Status: this is now the production default for /world/vitals/.** The vitals page currently has hero charts for oil, gas, gold, and USD/MYR. KLCI and the 6-card Malaysia section still use the legacy card-only layout. See `references/vitals-transmission-engine-viz.md` for the engine section's sensitivity visualization (Layer 5).

## The directive

Arif: *"[D]on't collapse it. Make chart as the contrast."*

Translation: charts are not summaries — they're the visual anchor of each section. Cards underneath read in light of the chart, not the other way around.

## What was changed

The pre-2026-08-08 vitals page (`/var/www/html/arif/world/vitals/index.html`) wrapped every chart in `<details class="chart-widget">` — collapsed by default, only render on user click. Plus three other problems:

1. **Collapsed by default** — only saw the chart if you expanded the widget. Bad first impression.
2. **Section order** — chart sat BELOW the narrative cards. Reading the prose before the visual.
3. **Chart height 340px** — small, lost in a sea of cards.
4. **Lazy init on `<details>` toggle** — first paint had no charts; SEO/bots saw nothing.

## What it is now

Pattern: `<div class="chart-widget-hero">` (no `<details>`, no toggle) at the top of each instrument section, then the narrative cards below. Charts init eagerly on page load.

| Before | After |
|---|---|
| `<details class="chart-widget">` | `<div class="chart-widget-hero">` |
| Collapsed by default | Always visible |
| `height: 340px` | `height: 420px` |
| Chart sits after cards | Chart sits before cards (hero) |
| Lazy load on `toggle` event | Eager load on page init |
| `if (chart.open) tickPrice(id)` | `if (chart.hero \|\| chart.open) tickPrice(id)` |

## CSS pattern (must match exactly)

```css
.chart-widget-hero{
  margin-top:12px;border:1px solid var(--line2);border-radius:8px;
  overflow:hidden;background:var(--panel)
}
.chart-widget-hero .chart-body{padding:0}
.chart-widget-hero .chart-toolbar{display:flex;align-items:center;gap:10px;
  padding:10px 14px;border-bottom:1px solid var(--line);flex-wrap:wrap}
.chart-widget-hero .chart-toolbar .tf-pills,
.chart-widget-hero .chart-toolbar .ema-toggles{display:flex;gap:3px}
.chart-widget-hero .chart-toolbar .pill{
  font-family:'IBM Plex Mono',monospace;font-size:9px;padding:3px 8px;
  border-radius:12px;border:1px solid var(--line2);background:transparent;
  color:var(--dim);cursor:pointer;transition:all .15s}
.chart-widget-hero .chart-toolbar .pill.active{
  border-color:var(--gold);color:var(--gold);background:rgba(232,182,76,.1)}
.chart-widget-hero .chart-toolbar .pill:hover:not(.active){
  border-color:#444;color:#ccc}
.chart-widget-hero .chart-canvas{height:420px}
.chart-widget-hero .price-strip{display:flex;align-items:baseline;gap:12px;
  padding:10px 14px;font-family:'IBM Plex Mono',monospace}
.chart-widget-hero .price-strip .big{font-size:26px;font-weight:700;color:#fff}
.chart-widget-hero .price-strip .delta{font-size:14px;font-weight:600}
.chart-widget-hero .price-strip .hero-tag{
  margin-left:auto;font-size:9px;letter-spacing:.12em;color:var(--faint);
  border:1px solid var(--line2);padding:3px 8px;border-radius:3px}
.chart-widget-hero .live-dot{width:7px;height:7px;border-radius:50%;
  background:var(--green);animation:pulse 2s infinite}
```

## JS init pattern (works for both new `.chart-widget-hero` and any legacy `<details class="chart-widget">`)

```js
document.querySelectorAll('.chart-widget-hero, .chart-widget').forEach(w => {
  const id = w.id.replace('chart-','');
  if (w.classList.contains('chart-widget-hero')) {
    initChart(id);                                  // eager
    const tf = w.querySelector('.pill.active[data-tf]')?.dataset?.tf || '4h';
    loadChartData(id, tf);
    tickPrice(id);
  }
  w.addEventListener('toggle', function() {          // legacy support
    if (!this.open) return;
    initChart(id);
    loadChartData(id, this.querySelector('.pill.active[data-tf]')?.dataset?.tf || '4h');
    tickPrice(id);
  });
  w.querySelectorAll('.pill[data-tf]').forEach(b => b.addEventListener('click', function(e) {
    e.preventDefault(); e.stopPropagation();
    const cid = this.dataset.chart;
    const w2 = document.getElementById('chart-'+cid);
    w2.querySelectorAll('.pill[data-tf]').forEach(p=>p.classList.remove('active'));
    this.classList.add('active');
    initChart(cid);
    loadChartData(cid, this.dataset.tf);
  }));
  w.querySelectorAll('.pill[data-e]').forEach(b => b.addEventListener('click', function(e) {
    e.preventDefault(); e.stopPropagation();
    this.classList.toggle('active');
    const cid = this.dataset.chart, ema = this.dataset.e;
    if (charts[cid]) {
      const s = charts[cid].ema[ema] || (ema==='200'?charts[cid].ema200:null);
      if (s) s.applyOptions({visible:this.classList.contains('active')});
    }
  }));
});

setInterval(() => {
  ['oil','gas','gold'].forEach(id => {
    const el = document.getElementById('chart-'+id);
    if (!el) return;
    if (el.classList.contains('chart-widget-hero') || el.open) tickPrice(id);
  });
}, 30000);

['oil','gas','gold'].forEach(id => tickPrice(id));
```

## HTML template for one instrument (oil)

```html
<!-- LIVE CHART: Brent Crude — HERO (always open) -->
<div class="chart-widget-hero" id="chart-oil"
     data-symbol="XBRENT" data-api="/oil/api/history" data-ticker="/oil/api/ticker"
     data-prefix="co" data-color="#57d98e" data-decimals="1" data-unit="$"
     data-title="Brent Crude · XBRENT">
  <div class="chart-body">
    <div class="price-strip">
      <span class="big" id="co-price">---</span>
      <span class="delta" id="co-delta">---</span>
      <span class="hero-tag">HERO · ALWAYS OPEN</span>
    </div>
    <div class="chart-toolbar">
      <span style="font-size:10px;color:var(--dim);font-family:'IBM Plex Mono',monospace">TF:</span>
      <div class="tf-pills">
        <button class="pill" data-tf="1h" data-chart="oil">1H</button>
        <button class="pill active" data-tf="4h" data-chart="oil">4H</button>
        <button class="pill" data-tf="1d" data-chart="oil">1D</button>
        <button class="pill" data-tf="1w" data-chart="oil">1W</button>
      </div>
      <span style="font-size:10px;color:var(--dim);font-family:'IBM Plex Mono',monospace;margin-left:8px">EMA:</span>
      <div class="ema-toggles">
        <button class="pill active" data-e="20" data-chart="oil">20</button>
        <button class="pill active" data-e="50" data-chart="oil">50</button>
      </div>
      <span class="live-dot" style="margin-left:auto"></span>
    </div>
    <div class="chart-canvas" id="chart-oil-canvas" style="height:420px"></div>
  </div>
</div>

<!-- THEN narrative cards -->
<div class="grid g3" style="margin-top:24px">...</div>
```

For **gold**, add a third EMA pill: `<button class="pill active" data-e="200" data-chart="gold">200</button>`. For **gas**, height stays 420px, color `#4ecdc4`, two-decimal display.

## Pitfalls hit during this forge (verified 2026-08-08)

1. **`patch` tool returned `error: path required` 4× in a row** when patching the trailing JS block. The block was a multi-line string with lots of escape sequences. Recovery: switched to Python `replace()` via terminal — completed in one shot. The tool seems to have a size threshold past which the call body truncates and `path` gets dropped. **Default to Python for multi-region edits on files > 600 lines.**

2. **Duplicate `</div></section>` survived one patch pass.** The first attempt to delete the gold `<details>` block left a stray closing pair. Structure check after deploy would have caught it before browser render. **Always balance-tag count after any multi-section HTML edit:**
   ```python
   print(h.count('<section '), h.count('</section>'),
         h.count('<div'), h.count('</div>'))
   ```

3. **Stale `live_prices.json` confusion.** `/var/www/html/arif/vitals/live_prices.json` is from a different surface (older `/vitals` page that 308s to `/propa/`). Don't read it for `/world/vitals/` state. Use the live `/oil/api/ticker`, `/gold/api/ticker`, `/gas/api/ticker` only.

## Verification script (browser)

After deploy, always:
```js
JSON.stringify({
  oil: {price: document.getElementById('co-price')?.textContent,
        delta: document.getElementById('co-delta')?.textContent},
  gas: {price: document.getElementById('cg-price')?.textContent,
        delta: document.getElementById('cg-delta')?.textContent},
  gold:{price: document.getElementById('cau-price')?.textContent,
        delta: document.getElementById('cau-delta')?.textContent},
  heroElements: document.querySelectorAll('.chart-widget-hero').length,    // expect 3+
  legacyCollapsed: document.querySelectorAll('details.chart-widget').length // expect 0
}, null, 2)
```

All three price cells must show `---` until tick fires (~1s after load), then live `$XX.X (-X.X%)` with a green/red delta.

## What this skill does NOT cover

- KLCI/USD/MYR charts: blocked by missing API endpoints (see SKILL.md Live-data wiring section). Don't promise them without first building the `/klci/api/` and `/usdmyr/api/` Node.js services.
- TradingView-style advanced indicators (RSI subchart, MACD, volume profile): only candlesticks + EMA overlays are wired. Adding RSI subchart needs a second canvas + a different lightweight-charts addon.
