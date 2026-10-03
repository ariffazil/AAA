---
name: wealth-mcp-testing
id: wealth-mcp-testing
version: 1.0.0
owner: AAA
description: Use when writing pytest tests for WEALTH MCP tools.
risk_tier: low
floor_scope: [F1, F2, F4, F11]
autonomy_tier: T1
tags: [wealth, testing, pytest, yfinance, mocking, mcp-tools]
capability_tier: fed-agent-subagent
ecology_state: WARM
triggers:
  - "WEALTH test"
  - "WEALTH pytest"
  - "capital_indicator test"
  - "capital_backtest test"
  - "capital_entry_plan test"
  - "WEALTH tool test"
  - "WEALTH mock yfinance"
  - "WEALTH Phase 1a test"
---

# WEALTH MCP Testing Patterns

> Use when writing or running pytest tests for WEALTH MCP tools. Covers the Phase 1a per-tool import pattern, yfinance mocking, and the StubMCP registration approach.

## Overview

WEALTH MCP has 11 canonical tools. After the Phase 1a refactor (2026-08-28), tools are split from monolithic canonical.py into per-tool files under wealth_mcp/tools/. This changes how tests import and mock tools.

## The Three Patterns

### 1. Import from per-tool modules (NOT canonical.py)

Phase 1a split canonical.py (3400+ lines) into individual files:
- wealth_mcp/tools/indicator.py -> register_indicator(mcp)
- wealth_mcp/tools/backtest.py -> register_backtest(mcp)
- wealth_mcp/tools/entry_plan.py -> register_entry_plan(mcp)
- (and 8 more for other tools)

DO NOT import from canonical.py - it imports ALL tools including heavy scipy optimizers that hang on import.

```python
# CORRECT - imports only the tool you need
from wealth_mcp.tools.indicator import register_indicator

# WRONG - triggers heavy optimizer imports that hang
from wealth_mcp.tools.canonical import register_canonical_tools
```

### 2. Mock yfinance.Ticker (NOT module attribute)

Tools import yfinance inside the function body (import yfinance as yf), not at module level. So patch("wealth_mcp.tools.indicator.yf") does NOT work - yf is a local variable, not a module attribute.

```python
# CORRECT - patches the yfinance module Ticker class
with patch("yfinance.Ticker") as MockTicker:
    MockTicker.return_value = mock_ticker
    result = _run(capital_indicator(symbol="GC=F", indicator="rsi"))

# WRONG - yf is a local variable, not a module attribute
with patch("wealth_mcp.tools.indicator.yf") as mock_yf:
    mock_yf.Ticker.return_value = mock_ticker  # Never reaches the function
```

### 3. StubMCP pattern for tool registration

Each per-tool module has a register_* function that takes an MCP instance and registers the tool via @mcp.tool() decorator. Use a StubMCP to capture the decorated function:

```python
class _StubMCP:
    def __init__(self):
        self.tools = {}
    def tool(self, name=None, **_kwargs):
        def decorator(func):
            self.tools[name or func.__name__] = func
            return func
        return decorator
    def __getattr__(self, name):
        return lambda **kwargs: (lambda f: f)

_stub = _StubMCP()
register_indicator(_stub)
capital_indicator = _stub.tools["capital_indicator"]
```

## Test File Structure

Every WEALTH test file should follow this structure:

```python
"""Tests for capital_X - description."""
from __future__ import annotations
import asyncio, sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import numpy as np, pandas as pd, pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import from per-tool module
from wealth_mcp.tools.X import register_X

# StubMCP + registration (see pattern above)
# Mock helpers (_make_ohlcv_df, _mock_yfinance, _run)
# Test classes
# if __name__ == "__main__": standalone runner
```

## Standalone Runner

Include a __main__ block for running outside pytest:

```python
if __name__ == "__main__":
    passed = failed = 0
    tests = [TestClass1(), TestClass2()]
    for test_obj in tests:
        for method_name in dir(test_obj):
            if method_name.startswith("test_"):
                method = getattr(test_obj, method_name)
                try:
                    method()
                    passed += 1
                    print(f"  PASS: {test_obj.__class__.__name__}.{method_name}")
                except Exception as e:
                    failed += 1
                    print(f"  FAIL: {test_obj.__class__.__name__}.{method_name}: {e}")
    print(f"\nResults: {passed} pass, {failed} fail of {passed + failed}")
    sys.exit(0 if failed == 0 else 1)
```

## Mock Helpers

### Synthetic OHLCV DataFrame

```python
def _make_ohlcv_df(n=100, base_price=2300.0, volatility=0.02):
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="1h")
    close = [base_price]
    for _ in range(n - 1):
        change = close[-1] * volatility * np.random.randn()
        close.append(close[-1] + change)
    close = np.array(close)
    return pd.DataFrame({
        "Open": close * (1 + np.random.randn(n) * 0.003),
        "High": close * (1 + np.abs(np.random.randn(n)) * 0.005),
        "Low": close * (1 - np.abs(np.random.randn(n)) * 0.005),
        "Close": close,
        "Volume": np.random.randint(1000, 50000, size=n).astype(float),
    }, index=dates)
```

### Mock OHLCV for backtest engine

The backtest engine expects objects with attribute access (.timestamp, .open, etc.):

```python
mock_ohlcv = type("OHLCV", (), {
    "__init__": lambda self, **kw: setattr(self, "_attrs", kw) or None,
    "__getattr__": lambda self, name: self._attrs.get(name),
})
```

### Run async tools synchronously

```python
def _run(coro):
    return asyncio.run(coro)
```

## Common Pitfalls

1. register_canonical_tools hangs - it imports ALL tools including scipy optimizers. Always import per-tool register_* functions instead.
2. patch("wealth_mcp.tools.X.yf") does not work - yfinance is imported locally inside tool functions. Use patch("yfinance.Ticker").
3. Mock OHLCV needs attributes - backtest engine accesses .timestamp, .open etc. via attribute access, not dict keys.
4. epistemic_tag values - tools return DERIVED, not OBSERVED. Test assertions should accept both.
5. Run standalone - pytest collection may hang due to heavy imports. Always include __main__ runner.

## Reference Files

- references/phase1a-mocking-patterns.md - Detailed mock setup for each tool type
