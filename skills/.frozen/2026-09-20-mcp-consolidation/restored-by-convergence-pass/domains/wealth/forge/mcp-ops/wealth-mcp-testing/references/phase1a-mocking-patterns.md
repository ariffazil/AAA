# Phase 1a Mocking Patterns — Detailed Reference

> Session-specific details for WEALTH MCP tool testing after the Phase 1a refactor.

## Phase 1a Refactoring Summary

The monolithic `wealth_mcp/tools/canonical.py` (3400+ lines, 11 tools) was split into individual files:

| File | Tool | Register Function |
|------|------|-------------------|
| `indicator.py` | capital_indicator | `register_indicator(mcp)` |
| `backtest.py` | capital_backtest | `register_backtest(mcp)` |
| `entry_plan.py` | capital_entry_plan | `register_entry_plan(mcp)` |
| `primitive.py` | capital_primitive | `register_primitive(mcp)` |
| `health.py` | capital_health | `register_health(mcp)` |
| `diagnose.py` | capital_diagnose | `register_diagnose(mcp)` |
| `market.py` | capital_market | `register_market(mcp)` |
| `ledger.py` | capital_ledger | `register_ledger(mcp)` |
| `registry.py` | capital_registry | `register_registry(mcp)` |
| `entropy.py` | capital_entropy | `register_entropy(mcp)` |
| `judge_handoff.py` | wealth_judge_handoff | `register_judge_handoff(mcp)` |

The orchestrator `canonical.py` now just imports and calls all `register_*` functions.

## Why register_canonical_tools Hangs

`register_canonical_tools` imports `wealth_core.optimizers.kelly` which imports `scipy.optimize.minimize_scalar`. On this system, `scipy.optimize` takes 30+ seconds to import, causing pytest collection to time out.

**Fix**: Import only the per-tool module you need:
```python
from wealth_mcp.tools.indicator import register_indicator
```

## yfinance Mocking Deep Dive

### The Problem

Tools import yfinance inside the function body:
```python
async def capital_indicator(symbol="GC=F", ...):
    import yfinance as yf  # LOCAL import, not module-level
    ticker = yf.Ticker(sym)
    hist = ticker.history(...)
```

Since `yf` is a local variable, `patch("wealth_mcp.tools.indicator.yf")` has no effect — the patch targets a non-existent module attribute.

### The Solution

Patch `yfinance.Ticker` at the module level:
```python
with patch("yfinance.Ticker") as MockTicker:
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = df
    MockTicker.return_value = mock_ticker
    result = await capital_indicator(symbol="GC=F", indicator="rsi")
```

When the function body executes `yf.Ticker(sym)`, Python looks up `yf` (which is the `yfinance` module), then calls `yf.Ticker(...)`. Since we patched `yfinance.Ticker`, our mock is returned.

### Pattern for Each Tool

```python
# indicator.py, backtest.py, entry_plan.py — all use yfinance the same way
with patch("yfinance.Ticker") as MockTicker:
    MockTicker.return_value = _mock_yfinance(df)
    result = _run(capital_X(...))
```

## Mock OHLCV for Backtest Engine

The backtest engine (`backtest/engine_v2.py`) creates OHLCV objects from `signals.scanner.OHLCV` and accesses them via attribute access:

```python
# In backtest code:
candles[0].timestamp  # attribute access, not dict
candles[0].open
candles[0].high
```

The mock must support this:
```python
mock_ohlcv = type("OHLCV", (), {
    "__init__": lambda self, **kw: setattr(self, "_attrs", kw) or None,
    "__getattr__": lambda self, name: self._attrs.get(name),
})

# Usage:
candle = mock_ohlcv(timestamp=idx, open=100.0, high=105.0, low=95.0, close=102.0, volume=10000)
assert candle.timestamp == idx  # Works via __getattr__
assert candle.open == 100.0
```

## Epistemic Tag Values

The `wrap_result` function in `wealth_contracts/envelope.py` determines the epistemic tag. For tool results:
- Tools that compute from user inputs → `"DERIVED"`
- Tools that fetch external data → `"OBSERVED"`

Most WEALTH tools return `"DERIVED"` even when they fetch data internally (yfinance). Don't hardcode `"OBSERVED"` in assertions:

```python
# CORRECT
assert result["epistemic_tag"] in ("OBSERVED", "DERIVED")

# WRONG — will fail for most tools
assert result["epistemic_tag"] == "OBSERVED"
```

## Synthetic OHLCV Generation

### Random Walk (default)

```python
def _make_ohlcv_df(n=100, base_price=2300.0, volatility=0.02):
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="1h")
    close = [base_price]
    for _ in range(n - 1):
        change = close[-1] * volatility * np.random.randn()
        close.append(close[-1] + change)
    close = np.array(close)
    high = close * (1 + np.abs(np.random.randn(n)) * 0.005)
    low = close * (1 - np.abs(np.random.randn(n)) * 0.005)
    open_ = close * (1 + np.random.randn(n) * 0.003)
    volume = np.random.randint(1000, 50000, size=n).astype(float)
    return pd.DataFrame({
        "Open": open_, "High": high, "Low": low,
        "Close": close, "Volume": volume,
    }, index=dates)
```

### Trending (for entry_plan tests)

```python
def _make_ohlcv_df(n=200, base_price=2300.0, trend="up", volatility=0.01):
    drift = volatility * 0.3 if trend == "up" else (-volatility * 0.3 if trend == "down" else 0)
    # ... same as above but with drift added to each step
```

### Monotonic (for RSI overbought/oversold)

```python
close = np.linspace(2000, 2500, 100)  # Rising → RSI > 70
close = np.linspace(2500, 2000, 100)  # Falling → RSI < 30
```

## Standalone vs pytest

The existing test (`test_step9_canonical_e2e.py`) runs as a standalone script, not through pytest. This avoids pytest's asyncio strict mode and collection overhead.

For new tests, include BOTH:
1. pytest-compatible test classes (for `pytest tests/test_X.py -v`)
2. `__main__` block (for `python tests/test_X.py`)

The `__main__` block is the fallback when pytest collection hangs due to heavy imports.
