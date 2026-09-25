# Monte Carlo Fan Chart — Quantitative Prediction Bands

Recipe for rendering a probability fan chart over a candlestick chart: synthesised
past candles on the left, Monte Carlo forecast paths on the right with percentile
bands (P10/P25/P50/P75/P90), and a multi-column intelligence panel below. Use
when the deliverable is a "WEALTH CHRON intelligence"-style probability reading
for gold / FX / equity over a 24H horizon.

## Why this pattern (not single-point prediction)

A single-point price prediction ("gold will be $4,300 tomorrow") is fabrication.
A probability band over a horizon is empirical: derived from the asset's recent
volatility (ATR), it quantifies uncertainty instead of hiding it. The band is
what a real trader or risk manager acts on, not the midpoint.

## Inputs (from WEALTH MCP)

```python
snapshot = mcp__wealth__capital_market(mode="commodity", commodity="gold")
# → snapshot.ticker.price (entry anchor), snapshot.ticker.ema20/50/200

rsi   = mcp__wealth__capital_indicator(indicator="rsi", period=14, interval="1h")
macd  = mcp__wealth__capital_indicator(indicator="macd", period=14, interval="1h")
atr   = mcp__wealth__capital_indicator(indicator="atr", period=14, interval="1h")
# → atr.current (absolute $ per candle — the volatility unit)
bb    = mcp__wealth__capital_indicator(indicator="bb", period=20, interval="1h")
ema20 = mcp__wealth__capital_indicator(indicator="ema", period=20, interval="1h")
```

The macro block inside `snapshot` (`dxy`, `vix`, `us10y`, `silver`, `usmyr`,
`gold_silver_ratio`) feeds the QUALITATIVE column of the intelligence panel,
not the math. Keep math and narrative in separate columns.

## Monte Carlo engine

```
sigma_per_candle  = atr.current                      # from capital_indicator(atr)
sigma_24h         = sigma_per_candle * sqrt(24)     # daily sigma (1H candles)
expected_move_95  = 1.96 * sigma_24h                 # symmetric 95% CI width
n_paths           = 2000                              # convergence at ~1000+
n_candles         = 24                                # forecast horizon
drift_per_candle  = (target_close - last_price) / n_candles   # EMA20 gravity
last_price        = snapshot.ticker.price

# Each path: GBM with drift
p = [last_price]
for _ in range(n_candles):
    p.append(p[-1] + drift_per_candle + normal(0, sigma_per_candle * 0.55))
```

Drift convention: pull toward EMA20 if price is on the wrong side, else zero
drift. The 0.55 multiplier tightens the per-candle sigma so the visible band
matches typical intraday ranges — without it the Monte Carlo fans are
visually too wide to read.

```python
# Percentile bands (vectorised)
arr = np.array(all_paths)  # shape (n_paths, n_candles+1)
p10, p25, p50, p75, p90 = np.percentile(arr, [10, 25, 50, 75, 90], axis=0)
```

Critical: `arr.shape[1] == n_candles + 1` because each path includes the
starting price as `out[0]`. When constructing the x-axis, use
`np.linspace(start_x, end_x, n_candles + 1)` to match. Mixing T and T+1 in
`fill_between` raises `ValueError: 'x' has size 24, but 'y1' has an unequal size
of 25`.

## Visual layer (matplotlib, dark theme)

```python
fig = Figure(figsize=(24, 15), facecolor=BG, dpi=180)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 54)
ax.set_ylim(4150, 4400)        # keep ylim low enough for the bottom panel
ax.set_facecolor(BG); ax.axis('off')

# 1. Past candles (synthesised walk anchored to live snapshot)
for i, c in enumerate(past_ohlc):
    color = GREEN if c.c >= c.o else RED
    ax.plot([x, x], [c.l, c.h], color=color, lw=0.7)
    body_h = max(abs(c.c - c.o), 0.4)
    ax.add_patch(Rectangle((x - 0.35, min(c.o, c.c)), 0.7, body_h,
                            facecolor=color, edgecolor=color))

# 2. Forecast x-axis (must match n_candles+1 from Monte Carlo paths)
x_pts = np.linspace(30.5, 52.5, 25)

# 3. Fan bands — make the inner band visibly denser than the outer
ax.fill_between(x_pts, p10, p90, color=GOLD, alpha=0.08)
ax.fill_between(x_pts, p25, p75, color=GOLD, alpha=0.45)
ax.plot(x_pts, p75, color=GOLD, lw=1.5, alpha=0.85)
ax.plot(x_pts, p25, color=GOLD, lw=1.5, alpha=0.85)
ax.plot(x_pts, p90, color=GOLD, lw=0.6, alpha=0.5, linestyle=':')
ax.plot(x_pts, p10, color=GOLD, lw=0.6, alpha=0.5, linestyle=':')
ax.plot(x_pts, p50, color='#ffd700', lw=3.0, alpha=1.0)   # bright yellow median

# 4. Sample paths (sparse, low alpha, behind the bands)
for s in range(0, n_paths, 67):
    ax.plot(x_pts, arr[s], color='#a8884a', lw=0.4, alpha=0.15)
```

The 0.45 alpha on the inner P25-P75 band + the 1.5-width outlines are what
make the fan readable. Without them the two bands blend into one gold blob.

## Right-edge labels (without clipping)

Right-edge text placed at `x = xlim_max - epsilon` still overflows the spine.
Two fixes that survive (use both for full safety):

```python
# (a) bbox-mask the labels so any overflow has a dark background
ax.text(51.0, y, label, ha='right', va='center',
        bbox=dict(facecolor='#1a1a1a', edgecolor='none', pad=1.5, alpha=0.9))

# (b) place inside the plot, not at the spine
# x = 51.0 with xlim=(0, 54) gives ~3 units of right-side margin
```

## Five-column bottom intelligence panel

Distinct column x-positions with non-overlapping text bands. For a 0–54
x-space, use:

```python
col_x = [5, 16, 27, 38, 49]
col_labels = ["QUALITATIVE", "QUANTITATIVE", "QUANTUM / REGIME", "CHRON", "PROTOCOL"]
for cx, label in zip(col_x, col_labels):
    ax.text(cx, 4210, label, fontsize=9, weight='bold', ha='center')

# Column body content keeps its own left-aligned x:
ax.text(2, 4200, "Regime", ...)        # col 1 body
ax.text(13, 4200, "RSI 14", ...)        # col 2 body
ax.text(24, 4200, "VOL REGIME", ...)    # col 3 body
ax.text(35, 4200, "TODAY", ...)         # col 4 body
ax.text(46, 4200, "WAIT trigger zone", ...) # col 5 body
```

Header-body x-offset of 3 units prevents the right edge of col-N's body text
from colliding with the left edge of col-N+1's header. If you put headers
and body on the same x, you get garbled letter-collision (\"PRADDICEOL\"-
style artefacts).

## Box placement

The QUANT FORECAST box and the bottom panel must NOT collide with the
fan chart. Two rules:

- QUANT FORECAST box: y between 4250–4340 (above the 4250 mid-chart line)
- Bottom panel: y0=4190, height=28, content y from 4170 to 4220
- Set `ax.set_ylim(4150, 4400)` so the y=4150 floor is below the panel

If you set ylim to 4230–4320 (just for the chart), the bottom panel's
bottom row clips silently — vision will see the panel border but report
\"TRIGGERS / STOPS / RR rows missing\".

## Verdict wording

Keep the verdict a single word in big bold: `SABAR`, `HOLD`, or `PROCEED`. The
engine's `judge_reason` field explains why in one line — surface it below
the verdict label so a reader doesn't have to cross-reference two locations.

## What this recipe is NOT

- **Not** a replacement for the wealth MCP verdict. Run the engine first,
  read `judge_reason`, then build the visual to match.
- **Not** a substitute for a real TradingView / MT5 chart. The past candles
  are synthesised (walk anchored to the live snapshot price); the right-edge
  fan is statistical, not historical. State this in the footer.
- **Not** a single-point price target. Anyone asking \"what will the price
  be tomorrow\" gets the band, not a fake specific number.

## Vision-verify checklist (specific to this pattern)

```
"1. Is the inner P25-P75 band visually distinguishable from the outer P10-P90 band?"
"2. Are all 5 percentile labels (P10/P25/P50/P75/P90) fully visible on the right edge?"
"3. Are the 5 column headers (QUALITATIVE / QUANTITATIVE / QUANTUM / CHRON / PROTOCOL) distinct with no overlapping text?"
"4. Is the bottom panel's bottom row visible (not clipped at y=0)?"
"5. Is the median line drawn in a brighter color than the percentile curves so it reads as the central tendency?"
"6. Is the snapshot price ($X,XXX.XX) marked at the live/forecast boundary?"
```

Each question targets a specific failure mode that has happened in this
domain. A generic \"describe this chart\" prompt misses them.
