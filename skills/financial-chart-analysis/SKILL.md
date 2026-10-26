---
name: financial-chart-analysis
description: Generate financial charts with technical indicators (PSAR, RSI, MACD, etc.) using Python, and produce future analysis with epistemic-labeled verdicts. Covers live data via yfinance, custom indicator calculations, dark-themed matplotlib rendering, TradingView browser automation pitfalls, and the analysis output format (tables + signal summary). Use when the user asks for "stock chart", "live chart", "add [indicator]", "technical analysis", "buy or do nothing", or any request to visualize market data with overlays.
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Financial Chart Analysis

Generate financial charts with technical indicators and produce actionable analysis for Arif. This skill covers the full pipeline: data acquisition → indicator calculation → chart rendering → vision verification → analysis delivery.

## Triggers
- "stock chart", "live chart", "gold chart", "oil chart"
- "letak [indicator]" / "add [indicator]" on a chart
- "buy or do nothing", "future analysis", "forecast"
- Any request to visualize price data with technical overlays

## Pipeline

### 1. Data Acquisition
```python
import yfinance as yf
# Gold futures: GC=F
# Oil futures: CL=F
# Forex: XAUUSD=X
data = yf.download("GC=F", start=start, end=end, progress=False)
```
- yfinance works from VPS without API key
- Futures symbols (`GC=F`, `CL=F`) are more accurate than spot for analysis
- Flatten MultiIndex columns: `data.columns = data.columns.get_level_values(0)`

### 2. Indicator Calculation
- **Parabolic SAR:** Custom implementation in `scripts/psar_chart.py`
- **RSI, MACD, Bollinger:** Use `ta` library or custom calculation
- Always calculate on raw DataFrame before chart rendering

### 3. Chart Rendering
- **Theme:** Dark (`#131722` background, white text, `#363a45` grid)
- **Library:** matplotlib (mplfinance for quick candles, but custom for PSAR overlays)
- **Candle colors:** `#26a69a` (bull/green), `#ef5350` (bear/red)
- **PSAR dots:** `^` teal for buy, `v` orange for sell
- **Volume panel:** color-matched to candles
- **Trend strip:** bottom panel showing indicator trend state
- Save to `/tmp/<asset>_psar.png` (or relevant indicator name)

### 4. Vision Verification
```python
vision_analyze(image_url="/tmp/chart.png", question="Describe the PSAR signals...")
```
Always verify the chart renders correctly before sending to user.

### 5. Analysis Output Format
Use structured tables + epistemic labels:
- `[OBS]` = live data observed
- `[DER]` = derived from models/calculations
- `[INT]` = interpretation
- `[SPEC]` = speculation

**Required sections:**
1. Chart image (MEDIA:/path/to/chart.png)
2. Signal table (Current Price | Indicator Level | Signal | Gap/Cushion)
3. Flip/Signal history table (recent signal changes)
4. Analysis paragraph with epistemic labels
5. VERDICT table (Asset | Signal | Stop Level | Action)

## Pitfalls

### TradingView UI Cannot Be Automated for Indicators
TradingView's indicators dialog uses custom canvas/shadow-DOM rendering — no standard `<input>` elements exist in the DOM. `browser_click` on the Indicators button opens the dialog, but `browser_type` cannot find or interact with the search field. Pressing keyboard keys may open the Symbol Search dialog instead. **Do not waste turns trying to automate TradingView indicator addition.** Go straight to Python chart generation.

### yfinance Column Structure
yfinance now returns MultiIndex columns even for single-ticker downloads. Always flatten:
```python
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)
```

### PSAR Calculation Edge Cases
- PSAR must not exceed prior 2 period lows (in uptrend) or highs (in downtrend)
- Trend flip requires price to cross PSAR level, not just touch it
- AF (acceleration factor) resets to 0.02 on each flip
- Default: AF_start=0.02, AF_increment=0.02, AF_max=0.2

### Weekend/Holiday Data
Markets closed = last available price. Note this in analysis — don't present stale data as "live".

## Worked Example (2026-08-09 Session)
- User asked for gold + oil charts with Parabolic SAR
- TradingView automation failed after 3 attempts
- Pivoted to Python: yfinance (125 rows, 6 months) → custom PSAR → matplotlib dark theme
- Generated 2 charts (gold + oil) with 3-panel layout (price+PSAR, volume, trend strip)
- Gold: BUY signal (PSAR $3,982, price $4,341, +$359 cushion)
- Oil: SELL signal (PSAR $87.14, price $78.18, -$8.96 gap)
- Vision-analyzed both charts for verification before delivery
