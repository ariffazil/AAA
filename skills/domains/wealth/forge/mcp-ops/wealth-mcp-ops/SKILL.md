---
name: wealth-mcp-ops
description: "Use when changing or testing WEALTH MCP tools — add a mode, harden, or write pytest. One owner for the WEALTH MCP toolchain."
id: wealth-mcp-ops
version: 1.0.0
owner: A-FORGE
risk_tier: medium
floor_scope: [F1, F2, F4, F11]
autonomy_tier: T1
ecology_state: WARM
tags: [wealth, mcp, capital-tools, pytest, mocking, hardening, canonical.py, envelope, registry]
supersedes:
  - wealth-mcp-testing
  - wealth-mcp-tool-hardening
triggers:
  - "WEALTH MCP"
  - "wealth tools"
  - "capital_primitive"
  - "capital_indicator"
  - "capital_backtest"
  - "capital_entry_plan"
  - "capital_health"
  - "capital_diagnose"
  - "wealth_mcp"
  - "canonical.py"
  - "harden WEALTH"
  - "WEALTH test"
  - "WEALTH pytest"
  - "WEALTH mock yfinance"
  - "register_canonical_tools hangs"
  - "StubMCP"
related_skills:
  - mcp-ops
  - XAUUSD-trading-stack
  - FORGE-repo-intelligence
capability_tier: fed-agent-subagent
---

# WEALTH MCP Operations — the organ-bounded MCP owner

> The WEALTH organ computes. arifOS judges. Arif decides.
> For the *general* MCP lifecycle (discover / probe / wire / test / govern / retire) use `mcp-ops`.
> This skill owns only what is **WEALTH-specific**: this repo's layout, its 11 tools, its envelope and
> session rules, and the two ways we change them — **harden** and **test**.

## The flow

```
LOCATE (repo + tool surface) → CHANGE (add mode / add tool / harden) → TEST (three patterns) → GOVERN (envelope + session + receipts) → VERIFY
```

## 1 — LOCATE

```
/root/WEALTH/
├── wealth_mcp/
│   ├── server.py                  # FastMCP server, receipt wiring, session binding
│   ├── __init__.py                # CAPITAL_TOOL_NAMES, PUBLIC_TOOL_NAMES, version
│   ├── tools/
│   │   ├── canonical.py           # legacy monolith (3461 lines) — SOT for the canonical 8
│   │   ├── indicator.py           # Phase 1a per-tool modules ↓
│   │   ├── backtest.py
│   │   ├── entry_plan.py
│   │   ├── bid_surface.py         # bid scoring engine
│   │   └── optimize_mwc.py
│   ├── middleware/                # evidence middleware (writes receipts)
│   └── prompts/                   # prompt templates
├── wealth_core/                   # computation engines: math, risk, capital, optimizers,
│                                  #   institutional, power, commodity_engines, market_data_fallback
├── wealth_contracts/              # envelope, epistemic tags, authority
├── engines/ trading/ internal/    # raw API fetchers, backtest engines, legacy monolith
├── tests/
└── docs/mcp-tool-families-spec.md # tool surface spec
```

**Current surface — 11 tools.**

| Tool | Modes | Coverage |
|---|---|---|
| capital_primitive | npv, irr, emv, evoi, mc, kelly, markowitz, robust, chance_constrained, two_stage, reward_design | covered |
| capital_health | conservation, flow, runway, survival (3 submodes), indicators, cross_validate | covered |
| capital_diagnose | stress_index, cascade_model, governance_capacity, exploitation_detect, bid_surface, power_*, opacity, collapse_signature | covered |
| capital_market | fx, commodity, indicator, stock, gold, oil, gas, crypto | covered |
| capital_ledger | query, write | covered |
| capital_registry | status, schema | covered |
| capital_entropy | observe, route | covered |
| wealth_judge_handoff | build, validate | covered |
| capital_indicator | compute | **NONE ← #1 hardening priority** |
| capital_backtest | run | **NONE ← #1 hardening priority** |
| capital_entry_plan | compute | **NONE ← #1 hardening priority** |

## 2 — CHANGE

### Adding a mode (preferred — do not create a tool per sub-capability)

Each canonical tool is a single `@mcp.tool()` with a `mode` parameter and an if-chain.

1. Add to the if-chain in the tool's module (or `canonical.py` for the canonical 8).
2. Add the mode to `valid_modes` in the error fallback.
3. Import from `wealth_core/`.
4. Return through `wrap_result()`.
5. Add a test.
6. Update `docs/mcp-tool-families-spec.md`.

### Adding a tool

1. Create `wealth_mcp/tools/<name>.py`.
2. Write `register_<name>_tools(mcp)`.
3. `@mcp.tool()` with `output_schema=WEALTH_OUTPUT_SCHEMA`.
4. Add to `CAPITAL_TOOL_NAMES` in `__init__.py`.
5. Register in `server.py::create_mcp_server()`.
6. Add a test.
7. Update `docs/mcp-tool-families-spec.md`.

### Hardening checklist (Phase 1)

1. **Split `canonical.py`** (3461 lines) — one file per tool, each exporting `register_X_tools(mcp)`; `__init__.py` calls all. *(Partially done: indicator/backtest/entry_plan already split — that is why the tests below import per-tool.)*
2. **Add tests for indicator / backtest / entry_plan** — RSI range, MACD signal+histogram, Ichimoku 5 lines, SMA-crossover backtest, empty-data backtest, entry_plan S/R levels, entry_plan missing-data error.
3. **Replace legacy routing** in `capital_market(mode="stock")` — drop `_call_legacy_tool("wealth_stock_analysis")` for a direct `wealth_core/stock/` import.
4. **Add retry/timeout to external API calls** — `commodity_engines.py`, `crypto/router.py`: httpx AsyncClient, 3-retry exponential backoff, 10s timeout.
5. **Standardise the error envelope** — every mode returns a structured error (status ERROR, error_code, message). Never raise `ValueError` out of a tool.

**Priority new tools.** XAUUSD: `capital_signal` (indicator + regime + volume → signal), `capital_chart` (mplfinance PNG). Power: `capital_power` (already built in `wealth_core/power/`, not exposed). Institutional: verify `capital_diagnose` covers all `wealth_core/institutional/` modes.

## 3 — TEST (the three patterns)

> After the Phase 1a split, tools live in per-tool modules. This changes both how tests import and how they mock.

**Pattern 1 — import from the per-tool module, never `canonical.py`.**

```python
# CORRECT — imports only the tool you need
from wealth_mcp.tools.indicator import register_indicator

# WRONG — imports ALL tools, including heavy scipy optimizers that hang on import
from wealth_mcp.tools.canonical import register_canonical_tools
```

**Pattern 2 — mock `yfinance.Ticker`, not a module attribute.** Tools do `import yfinance as yf`
*inside* the function body, so `yf` is a local, not a module attribute.

```python
# CORRECT
with patch("yfinance.Ticker") as MockTicker:
    MockTicker.return_value = mock_ticker
    result = _run(capital_indicator(symbol="GC=F", indicator="rsi"))

# WRONG — never reaches the function
with patch("wealth_mcp.tools.indicator.yf") as mock_yf:
    mock_yf.Ticker.return_value = mock_ticker
```

**Pattern 3 — `StubMCP` to capture the decorated tool.**

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

**Every test file:** module docstring → `sys.path` bootstrap → per-tool import → StubMCP registration →
mock helpers (`_make_ohlcv_df`, `_mock_yfinance`, `_run`) → test classes → a `__main__` standalone
runner (pytest collection can hang on the heavy imports, so the standalone runner is not optional).

Pitfalls: `register_canonical_tools` hangs; `patch("…X.yf")` is a no-op; mock OHLCV needs **attribute**
access (`.timestamp`, `.open`), not dict keys; `epistemic_tag` is `DERIVED`, so assertions should
accept DERIVED *and* OBSERVED.

## 4 — GOVERN

- **`WealthEnvelope` on every return** — `wrap_result()` from `wealth_contracts.envelope` adds epistemic_tag, evidence_quality, source_attribution, session/actor/trace IDs, errors, warnings. **Never return a raw dict.**
- **Session binding** — OBSERVE tools (market, registry, primitive, entropy, indicator, backtest, entry_plan) are OBSERVE_UNBOUND; MUTATE tools (ledger write, handoff) require a valid session via the HTTP bridge.
- **Transport coercion** — all params arrive as strings; use `CoercedList`, `CoercedDict`, `CoercedDictList`.
- **Receipts** — middleware writes to `/root/VAULT999/wealth/receipts.jsonl`; tools never call `_emit_receipt()` directly. A receipt failure is not a tool failure.
- **Boundary** — never import `arifosmcp` into WEALTH (Zen 2026-07-11 FNF-0). `capital_entropy` is optional; return UNAVAILABLE when its dependency is absent.

## 5 — VERIFY

- `canonical.py` is the SOT — docs are documentation, not truth. Check the code, then the spec.
- `capital_registry(status|schema)` is the registry-truth surface; a tool absent from `CAPITAL_TOOL_NAMES` is not registered however well it is written.
- The 3 zero-coverage tools return **provisional** output — say so when relaying their numbers.

## Absorbed references (verbatim)

| File | Was |
|---|---|
| `references/absorbed-wealth-mcp-testing.md` | `wealth-mcp-testing` — full pytest patterns |
| `references/absorbed-wealth-mcp-testing/references/phase1a-mocking-patterns.md` | its per-tool mock detail |
| `references/absorbed-wealth-mcp-tool-hardening.md` | `wealth-mcp-tool-hardening` — full hardening/extension detail |

*Merged 2026-09-20 from `wealth-mcp-testing` + `wealth-mcp-tool-hardening`; both names still resolve.*
*DITEMPA BUKAN DIBERI ⚒️*
