# WEALTH MCP Tool Schemas — Verified 2026-09-25

Concrete reference for calling the federation WEALTH MCP tools without triggering
argument-validation errors. Two distinct tools, distinct schemas, distinct output
shapes. Verified by live calls.

## `mcp__wealth__capital_market` — market snapshot

**Required:** `mode` (one of: `fundamentals`, `fx`, `commodity`, `indicator`, `stock`,
`gold`, `oil`, `gas`).

**REJECTS these keys:** `interval`, `symbol`, `commodity` (when mode requires a
commodity, the mode itself determines the asset). The tool schema is strict — extra
keys trigger `additionalProperties: false` rejection.

### Mode `commodity` — anchor for fan charts

```python
mcp__wealth__capital_market(
    mode="commodity",
    commodity="gold"   # or "brent_crude", "wti_crude", etc.
)
```

**Returns:** ticker snapshot with `price`, `change`, `changePct`, `rsi`, `rsiState`,
`ema20/50/200`, `emaTrend`, `support[]`, `resistance[]`, `pivot`. PLUS macro block:
`{dxy, vix, us10y, silver, usmyr, gold_silver_ratio}`.

**PLUS** signal block: `{direction, strength, confidence, entry_price, stop_loss,
take_profit_1, take_profit_2, rr_ratio, confluence_score, suggested_lot, verdict,
judge_reason}`. Verdict is one of `SABAR`, `HOLD`, `PROCEED`. `judge_reason` gives
the textual reasoning (e.g. "RR ratio 0.0 < 1.5 — insufficient reward").

### Mode `fundamentals` — equity/stock fundamentals

```python
mcp__wealth__capital_market(
    mode="fundamentals",
    ticker="GC=F"   # BurSa code or yfinance ticker
)
```

For commodities like `GC=F`, fundamentals returns `NEEDS_DATA` (no F1–F9 invariants
for gold spot — those are equity-specific). For equities: returns invariant F1–F9
verdicts with F8_BUSINESS_QUALITY often `FLAG` for cyclical commodities.

## `mcp__wealth__capital_indicator` — single technical indicator

**Required:** `indicator`, `period`, `interval`, `symbol`.

**REJECTS these keys:** `mode`, `commodity`, `base`, `targets`, `country`,
`asset_class`, `indicator` is a free string but valid options include `rsi`, `macd`,
`atr`, `bb`, `ema`.

**`symbol` defaults to `"GC=F"` (gold spot).** Period in candles (e.g. `14` for
RSI-14, `20` for BB-20). Interval: `"1d"`, `"1h"`, `"15m"`, etc.

### RSI example

```python
mcp__wealth__capital_indicator(
    symbol="GC=F",
    indicator="rsi",
    period=14,
    interval="1h"
)
```

Returns: `{current, overbought, oversold, series_last_5, data_points}`.

### MACD example

```python
mcp__wealth__capital_indicator(
    symbol="GC=F",
    indicator="macd",
    period=14,
    interval="1h"
)
```

Returns: `{macd_line, signal_line, histogram, bullish, data_points}`.

### ATR example

```python
mcp__wealth__capital_indicator(
    symbol="GC=F",
    indicator="atr",
    period=14,
    interval="1h"
)
```

Returns: `{current, current_price, atr_pct, data_points}`. `atr_pct` is the ATR as a
percentage of current price — the most useful single number for sizing Monte Carlo
fan-chart volatility.

### Bollinger Bands

```python
mcp__wealth__capital_indicator(
    symbol="GC=F",
    indicator="bb",
    period=20,
    interval="1h"
)
```

Returns: `{sma, upper, lower, current_price, bandwidth_pct, price_position_pct}`.
`bandwidth_pct` = `(upper - lower) / sma × 100`. `price_position_pct` = where current
price sits between lower and upper (0–100).

### EMA

```python
mcp__wealth__capital_indicator(
    symbol="GC=F",
    indicator="ema",
    period=20,
    interval="1h"
)
```

Returns: `{current, current_price, series_last_5}`.

## Pattern — use these two tools together for fan-chart inputs

```python
# Snapshot + 5 indicators in 6 calls
snapshot = capital_market(mode="commodity", commodity="gold")
rsi = capital_indicator(indicator="rsi", period=14, interval="1h")
macd = capital_indicator(indicator="macd", period=14, interval="1h")
atr = capital_indicator(indicator="atr", period=14, interval="1h")
bb = capital_indicator(indicator="bb", period=20, interval="1h")
ema20 = capital_indicator(indicator="ema", period=20, interval="1h")

# Anchor price + ATR → run Monte Carlo GBM
price = snapshot["snapshot"]["ticker"]["price"]
sigma_per_candle = atr["current"]
# n_paths × n_candles simulation, percentile bands for P10/P25/P50/P75/P90
```

## Common errors and fixes

- **`'mode' was unexpected`** → you passed `mode="commodity"` to `capital_indicator`.
  `capital_indicator` doesn't accept `mode`. Use only `indicator`, `period`,
  `interval`, `symbol`.
- **`'commodity', 'mode' were unexpected`** on `capital_indicator` → same root cause.
- **`Unknown mode 'pulse'`** → valid modes are listed above; `pulse` is not one of
  them. Use `mode="commodity"` or `mode="indicator"`.
- **`SESSION_MISSING: Mcp-Session-Id header required`** when calling via curl →
  don't call MCP tools via raw HTTP; use the `tool_call` MCP wrapper or the
  `mcp__wealth__*` tool names directly.

## Pacing (live, verified)

Single `capital_market` call: ~0.05–0.5 seconds.
Single `capital_indicator` call: ~0.4–0.6 seconds.
Parallel: all 6 calls in one `tool_call` block complete in ~0.5 seconds total.
