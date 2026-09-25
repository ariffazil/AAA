# Lightweight Charts Fan Overlay — Probabilistic Forecast on Web Chart

Recipe for rendering a probability fan chart (P10 / P25 / P50 / P75 / P90) extending past the
last historical candle on a lightweight-charts web widget. Used when the deliverable is a
forecast waveform drawn directly on the live price chart rather than a static matplotlib PNG.
Complements the existing `references/monte-carlo-fan-chart-pattern.md` which covers the
matplotlib variant for static PNG output.

## Why this pattern

A single-point price prediction ("gold will be $4,300 tomorrow") is fabrication. A probability
band over a horizon is empirical: it quantifies uncertainty instead of hiding it. When the
fan is drawn directly on the price chart extending past the last candle, the user sees
future probability as visual continuation of price action — not a separate numerical panel.

## Constraints (must satisfy)

- **No fabricated future candles.** Do not draw predicted OHLC bars at future timestamps; only
  draw quantile line/area series that exist in the backend response.
- **Clamped interpolation.** When connecting 3 daily endpoints to 72 hourly visual points,
  interpolate linearly between adjacent daily quantiles; never let interpolated points exceed
  the daily P10/P90 bounds.
- **Native library constraints.** lightweight-charts v4.x standalone build supports `addLineSeries`,
  `addAreaSeries`, `addCandlestickSeries`, `addHistogramSeries`, `setMarkers`, and
  `createPriceLine`. It does NOT support vertical time-line series. Workarounds below.

## Inputs (from WEALTH MCP, cross-origin from arif-fazil.com)

```js
const DATA_BASE = 'https://arif-fazil.com/gold/api';
// pre-2026-09-25: /forecast?horizon=3 returned 30-day cone truncated to 3 endpoints.
// post-2026-09-25: backend serves the same. Anchored at last fully closed 1H bar.
const fc = await fetch(`${DATA_BASE}/forecast?horizon=3&t=${Date.now()}`).then(r => r.json());
// fc.cone.t = 30 daily dates, fc.cone.p50[0..29], fc.cone.p25[0..29], fc.cone.p75[0..29],
// fc.cone.p10[0..29], fc.cone.p90[0..29], fc.basis.ema200, fc.basis.atr14
```

## Visual layer

```js
async function _renderForecastWaveform(chart, hist) {
  // Backend gives N daily points (3 for horizon=3, 30 for horizon=30). Anchor at the
  // last closed candle and linearly interpolate to hourly visual points. Clamped to
  // P10/P90 so interpolation cannot overshoot the supplied quantile envelope.
  const lastBar = hist.candles[hist.candles.length - 1];
  const lastTime = lastBar.time;
  const lastClose = lastBar.close;
  const days = fc.cone.t.length;
  const HOURLY_STEPS_PER_DAY = 24;
  const HORIZON_HOURS = days * HOURLY_STEPS_PER_DAY;
  const SECS_PER_HOUR = 3600;

  const tsList = [];
  for (let h = 1; h <= HORIZON_HOURS; h++) tsList.push(lastTime + h * SECS_PER_HOUR);

  const interpPath = (p50Arr, p10Arr, p90Arr) => {
    const points = [{ time: lastTime, value: lastClose }];
    for (let h = 1; h <= HORIZON_HOURS; h++) {
      const t = (h - 1) / HOURLY_STEPS_PER_DAY;
      const d = Math.floor(t);
      const f = t - d;
      const dd = d >= days ? days - 1 : d;
      const dn = d + 1 >= days ? days - 1 : d + 1;
      const p50 = p50Arr[dd] * (1 - f) + p50Arr[dn] * f;
      points.push({ time: tsList[h - 1], value: p50 });
    }
    return points;
  };
  const at = (h) => {
    const t = (h - 1) / HOURLY_STEPS_PER_DAY;
    const d = Math.floor(t);
    const f = t - d;
    const dd = d >= days ? days - 1 : d;
    const dn = d + 1 >= days ? days - 1 : d + 1;
    return (arr) => arr[dd] * (1 - f) + arr[dn] * f;
  };

  const interp = interpPath(fc.cone.p50, fc.cone.p10, fc.cone.p90);
  const p10Path = interp.p50.map((p, i) => ({ time: p.time, value: at(i + 1)(fc.cone.p90) }));
  const p90Path = interp.p50.map((p, i) => ({ time: p.time, value: at(i + 1)(fc.cone.p10) }));
  const p25Path = interp.p50.map((p, i) => ({ time: p.time, value: fc.cone.p75[Math.min(Math.floor(i / HOURLY_STEPS_PER_DAY), days - 1)] }));
  const p75Path = interp.p50.map((p, i) => ({ time: p.time, value: fc.cone.p25[Math.min(Math.floor(i / HOURLY_STEPS_PER_DAY), days - 1)] }));

  // Outer band: P10-P90. Two overlapping area series simulate a band; native band series
  // does not exist in v4.
  chart.addAreaSeries({ topColor: 'rgba(56,189,248,0.10)', bottomColor: 'rgba(56,189,248,0.10)',
    lineColor: 'rgba(56,189,248,0.30)', lineWidth: 1, title: 'P90', priceLineVisible: false })
    .setData(p10Path);
  chart.addAreaSeries({ topColor: 'rgba(56,189,248,0.10)', bottomColor: 'rgba(56,189,248,0.10)',
    lineColor: 'rgba(56,189,248,0.30)', lineWidth: 1, title: 'P10', priceLineVisible: false })
    .setData(p90Path);

  // Inner band: P25-P75 (denser).
  chart.addAreaSeries({ topColor: 'rgba(34,197,94,0.18)', bottomColor: 'rgba(34,197,94,0.18)',
    lineColor: 'rgba(34,197,94,0.40)', lineWidth: 1, title: 'P75', priceLineVisible: false })
    .setData(p25Path);
  chart.addAreaSeries({ topColor: 'rgba(34,197,94,0.18)', bottomColor: 'rgba(34,197,94,0.18)',
    lineColor: 'rgba(34,197,94,0.40)', lineWidth: 1, title: 'P25', priceLineVisible: false })
    .setData(p75Path);

  // P50 dashed median.
  const p50Series = chart.addLineSeries({
    color: '#32d7ff', lineWidth: 2,
    lineStyle: LightweightCharts.LineStyle.Dashed,
    priceLineVisible: false, title: 'P50',
  });
  p50Series.setData(interp.p50);

  // Endpoint markers via series.setMarkers (not the createSeriesMarkers plugin).
  const H24 = HOURLY_STEPS_PER_DAY;
  const H48 = 2 * HOURLY_STEPS_PER_DAY;
  const H72 = 3 * HOURLY_STEPS_PER_DAY;
  p50Series.setMarkers([
    { time: interp.p50[H24].time, position: 'aboveBar', color: '#fbbf24', shape: 'circle', text: '+24H' },
    { time: interp.p50[H48].time, position: 'aboveBar', color: '#fbbf24', shape: 'circle', text: '+48H' },
    { time: interp.p50[H72].time, position: 'aboveBar', color: '#fbbf24', shape: 'circle', text: '+72H' },
  ]);

  // FORECAST_START vertical divider. lightweight-charts v4 does NOT support vertical
  // time lines via API. createPriceLine is horizontal-only (price-level lines). Use an
  // HTML overlay positioned via timeToCoordinate and re-aligned on time-range changes.
  const overlay = document.createElement('div');
  overlay.style.cssText = `
    position: absolute; top: 0; bottom: 0; width: 2px;
    background: repeating-linear-gradient(to bottom, rgba(251,191,36,0.9) 0 4px, transparent 4px 8px);
    pointer-events: none; z-index: 5; left: 0;`;
  overlay.title = 'FORECAST START';
  document.getElementById('chart-container').appendChild(overlay);
  const updatePos = () => {
    const x = chart.timeScale().timeToCoordinate(lastTime);
    if (x != null) overlay.style.left = x + 'px';
  };
  updatePos();
  chart.timeScale().subscribeVisibleTimeRangeChange(updatePos);
  chart.subscribeCrosshairMove(updatePos);
  window.addEventListener('resize', updatePos);
}
```

Call this AFTER the candle series is set up and BEFORE `chart.timeScale().fitContent()` so the
fit includes the forecast projection.

## Honest limits (do not violate)

- **No predicted candles.** Never draw candlestick series at future timestamps. Quantile paths
  are the only honest future visualization.
- **Clamped interpolation.** Never allow interpolated points to exceed the supplied daily
  P10/P90 bounds. The helper above clamps via floor/ceil on the day index.
- **No monotonic cubic smoothing.** Linear interpolation between quantiles is the only safe
  smoothing. Cubic can overshoot P10/P90 and visually invent prices the model never predicted.
- **SHADOW watermark.** Until calibration moves the model from SHADOW to LIVE, the chart must
  show "SHADOW FORECAST" text on the chart canvas (HTML overlay, top-right). This prevents
  visual confusion with the observed historical candles.

## Verification checklist

After the chart renders, vision-read the PNG screenshot and ask:

1. Is there a DASHED CYAN LINE extending rightward from the last historical candle (the P50 median)?
2. Is there a fan-shaped band (green inner P25-P75, cyan outer P10-P90) extending past the candle?
3. Is there a vertical dotted yellow line at the boundary between historical candles and forecast?
4. Are there circular markers with labels +24H, +48H, +72H at the right edge of the projection?
5. Is "SHADOW FORECAST" watermark visible in the chart canvas (top-right)?
6. Are the EMA overlay lines (orange/cyan/purple) still visible UNDER the forecast bands?

A generic "describe this chart" prompt misses the boundary + marker specifics. Ask for each
visual element explicitly.

## Reference examples in the wild

- clivethompson.com/gold-predictor.html — projected gold path forward from today with blue
  probability fan overlay. Closest visual reference for the design language.
- sigmanomics.com/commodities-markets/xauusd — calibrated expected ranges over 7/14/28 days
  with model-agreement bands.
- goldpriceforecasted.com — historical data alongside blended ARIMA + technical predictions
  with 95% confidence intervals.

## Differences from the matplotlib variant

| Concern | matplotlib variant | lightweight-charts variant |
|---|---|---|
| Output format | Static PNG, A4 PDF | Live web widget |
| Interactivity | None | Hover, crosshair, zoom, pan |
| Time resolution | Whatever the figure specifies | Backend-bound; clamped to P10/P90 |
| Bands | `fill_between(x, p10, p90)` | Two overlapping `addAreaSeries` (no native band) |
| Median line | `ax.plot(x_pts, p50, ...)` | `addLineSeries` with dashed `lineStyle` |
| Markers | `ax.annotate` per endpoint | `series.setMarkers([{time, position, color, shape, text}])` |
| Vertical divider | `axvline` matplotlib call | HTML overlay + `timeToCoordinate` (no native support) |
| X-axis width | Fixed `set_xlim(0, 54)` | `fitContent()` after series set |