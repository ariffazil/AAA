# O&G Sector Analysis Chart Pack

Proven 2026-08-09 on UOBKH O&G intelligence report. 8-chart template for any oil & gas / energy sector analysis PDF.

## Chart Inventory

| # | Chart | Type | Data Source | Purpose |
|---|-------|------|-------------|---------|
| 01 | Brent Trajectory | Line + fill | yfinance or web scrape | Price context, floor/ceiling markers |
| 02 | Stock Scorecard | Horizontal bar | Analyst calls | Upside to TP for all covered names |
| 03 | NG Sensitivity | Bar (diverging) | Analyst notes | Commodity price → earnings sensitivity |
| 04 | Extraction Rate | Vertical bar | Audited financials | Sovereign fiscal extraction visualization |
| 05 | House Stance | Horizontal bar | Multiple houses | Comparative sector ratings |
| 06 | Timeline | Dot timeline | Research dates | Events + catalysts chronology |
| 07 | Risk Heatmap | Scatter (bubble) | Risk assessment | Likelihood × Impact matrix |
| 08 | Valuation Waterfall | Stacked bar | Valuation model | Build-up to target price |

## Matplotlib Recipes

### Chart 01: Commodity Price Trajectory
```python
# Key: fill_between for area, axhline for forecast anchors
ax.fill_between(range(len(months)), prices, alpha=0.15, color=RED)
ax.plot(range(len(months)), prices, color=RED, linewidth=2.5, marker='o')
ax.axhline(y=forecast_avg, color=GOLD, linestyle='--')  # house forecast
ax.axhline(y=next_year_target, color=BLUE, linestyle=':')  # next year
# Annotate spike events with bbox callout
```

### Chart 02: Stock Scorecard (Upside to TP)
```python
# Key: horizontal bars, color by call (GREEN=BUY, ORANGE=HOLD, RED=SELL)
upside = [(tp - last) / last * 100 for tp, last in zip(targets, last_prices)]
bars = ax.barh(stocks, upside, color=colors, height=0.55)
# Label each bar with "+X% TP RMX.XX"
```

### Chart 03: Commodity Sensitivity
```python
# Key: diverging bars around zero, vertical lines for current vs forecast
np_change = [(p - base) / base * sensitivity_pct * 100 for p in price_range]
colors = [GREEN if n > 0 else RED for n in np_change]
ax.axvline(x=current_price, color=GREY, linestyle='--')
ax.axvline(x=forecast_price, color=ORANGE, linestyle='--')
```

### Chart 04: Extraction / Cash Flow Waterfall
```python
# Key: positive bars = inflows (BLUE), negative = outflows (RED), retained = GREEN
values = [cffo, -capex, -dividend, -tax, retained]
colors = [BLUE, RED, RED, RED, GREEN]
# Annotation: extraction_rate = (dividend + tax) / cffo * 100
```

### Chart 05: House Stance Comparison
```python
# Key: mapped scale (0=UW, 0.5=MW, 1=OW), color by conviction
stance_map = {"Underweight": 0, "Neutral": 0.3, "Market Weight": 0.5,
              "Slight OW": 0.6, "Overweight": 0.8, "Overweight": 1.0}
```

### Chart 06: Event Timeline
```python
# Key: scatter dots on horizontal line, alternating up/down annotations
ax.scatter(range(N), [0]*N, s=140, color=colors, edgecolors='white', linewidths=2)
# Alternate xytext=(0, 30) and (0, -50) for readability
ax.plot(range(N), [0]*N, color=NAVY, linewidth=2, alpha=0.3)
```

### Chart 07: Risk Heatmap
```python
# Key: bubble size = likelihood × impact, color by severity
sizes = [l*imp*900 for l,imp in zip(likelihoods, impacts)]
colors = [RED if l*imp > 0.4 else ORANGE if l*imp > 0.2 else GREEN]
ax.scatter(likelihoods, impacts, s=sizes, c=colors, alpha=0.7, edgecolors=NAVY)
# Label bubbles with risk names (white text on dark bubbles)
```

### Chart 08: Valuation Waterfall
```python
# Key: stacked bars showing value build-up from book to target
bottoms = [0, book_value, book_value+premium1, book_value+p1+p2, 0, 0]
heights = [book_value, premium1, premium2, premium3, current_price, target_price]
colors = [BLUE, GREEN, GREEN, ORANGE, GREY, GOLD]
```

## Colour Palette (O&G sector)

| Role | Hex | Usage |
|------|-----|-------|
| NAVY | #0e1a2b | Text, axes, borders |
| GOLD | #c9a227 | Forecasts, targets, accents |
| RED | #c0392b | Risk, outflows, price spikes |
| GREEN | #27ae60 | BUY calls, inflows, upside |
| BLUE | #2c7be5 | Book value, neutral data |
| ORANGE | #e67e22 | HOLD calls, warnings, INT tags |
| GREY | #95a5a6 | Current price, stale data |
| TEAL | #1abc9c | Consensus (not primary house) |

## Adaptation for Other Sectors

Replace commodity-specific charts with sector equivalents:
- **Banking:** NIM trajectory, NPL ratio, loan growth
- **Plantation:** CPO price trajectory, yield per hectare, cost production
- **Property:** Launch vs take-up, inventory overhang, developer margins
- **Tech:** Revenue by segment, capacity utilization, order book

The 8-chart structure (trajectory → scorecard → sensitivity → extraction → stance → timeline → risk → valuation) is sector-agnostic. Only the data changes.
