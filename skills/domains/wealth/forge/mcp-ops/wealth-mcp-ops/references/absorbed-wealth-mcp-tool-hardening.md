---
id: wealth-mcp-tool-hardening
name: wealth-mcp-tool-hardening
version: 1.0.0
description: "Harden or extend WEALTH MCP tools. Checklist and patterns."
owner: A-FORGE
risk_tier: medium
floor_scope: [F1, F2, F11]
autonomy_tier: T1
ecology_state: WARM
triggers:
  - "WEALTH MCP"
  - "wealth tools"
  - "capital_primitive"
  - "capital_indicator"
  - "capital_backtest"
  - "capital_entry_plan"
  - "wealth_mcp"
  - "canonical.py"
  - "harden WEALTH"
related_skills:
  - XAUUSD-trading-stack
  - FORGE-repo-intelligence
---

# WEALTH MCP Tool Hardening and Extension

> The WEALTH organ computes. arifOS judges. Arif decides.

## Repository Layout

```
/root/WEALTH/
├── wealth_mcp/                    # MCP server + tool registrations
│   ├── server.py                  # FastMCP server, receipt wiring, session binding (2800 lines)
│   ├── __init__.py                # CAPITAL_TOOL_NAMES, PUBLIC_TOOL_NAMES, version
│   ├── tools/
│   │   ├── canonical.py           # ALL 11 tool implementations (3461 lines MONOLITH)
│   │   ├── bid_surface.py         # Bid scoring engine (214 lines)
│   │   └── optimize_mwc.py        # MWC optimizer
│   ├── middleware/                 # Evidence middleware
│   └── prompts/                   # 7 prompt templates
├── wealth_core/                   # Core computation engines
│   ├── math/                      # IRR, NPV
│   ├── risk/                      # EMV, Monte Carlo, EVOI, asymmetry, breakeven
│   ├── capital/                   # Conservation, flow, runway
│   ├── optimizers/                # Kelly, Markowitz, robust, chance-constrained, two_stage
│   ├── institutional/             # Stress index, cascade, governance, exploitation
│   ├── power/                     # Incentive map, capture, coercion, rent, rule asymmetry
│   ├── commodity_engines.py       # Gold/Oil/Gas API wrappers
│   ├── market_data_fallback.py    # yfinance + fallback chain
│   └── ingest/crypto/             # Binance, CoinGecko, DeFiLlama router
├── wealth_contracts/              # Envelope, epistemic tags, authority
├── entropy-integrity/             # Optional entropy analysis (separate package)
├── engines/                       # Raw API fetchers (commodity, crypto)
├── trading/                       # Backtest engines, signals, risk management
├── internal/                      # Legacy monolith, stock analysis, power modules
├── tests/                         # Test suite
├── pyproject.toml                 # Dependencies (Python 3.12+, fastmcp, yfinance, etc.)
└── docs/mcp-tool-families-spec.md # Tool surface spec
```

## Current MCP Tool Surface (11 tools)

### Canonical 8 (declared in __init__.py)

| Tool | Modes | Test Coverage |
|---|---|---|
| capital_primitive | npv, irr, emv, evoi, mc, kelly, markowitz, robust, chance_constrained, two_stage, reward_design | tests/core/test_math.py, test_optimizers.py |
| capital_health | conservation, flow, runway, survival (3 submodes), indicators, cross_validate | tests/core/test_capital.py, test_risk.py |
| capital_diagnose | stress_index, cascade_model, governance_capacity, exploitation_detect, bid_surface, power_*, opacity, collapse_signature | tests/core/test_power.py |
| capital_market | fx, commodity, indicator, stock, gold, oil, gas, crypto | tests/test_market_data.py, test_commodity_engines.py |
| capital_ledger | query, write | tests/test_vault_supabase_sync.py |
| capital_registry | status, schema | tests/mcp/test_registry_truth.py |
| capital_entropy | observe, route | tests/test_capital_entropy_bugfixes.py |
| wealth_judge_handoff | build, validate | tests/mcp/test_direct_session_gate.py |

### Added 3 (post-zen, zero test coverage)

| Tool | Modes | Test Coverage |
|---|---|---|
| capital_indicator | compute | **NONE** |
| capital_backtest | run | **NONE** |
| capital_entry_plan | compute | **NONE** |

**These 3 are the #1 hardening priority.**

## Architecture Patterns

### Mode-dispatched tools

Each canonical tool is a single @mcp.tool() with a mode parameter. Chain of if-blocks. Follow this for new modes — do not create separate tools per sub-capability.

### WealthEnvelope wrapping

ALL returns go through wrap_result() from wealth_contracts.envelope. Adds epistemic_tag, evidence_quality, source_attribution, session/actor/trace IDs, errors, warnings. **Never return raw dicts.**

### Session binding

OBSERVE tools (market, registry, primitive, entropy, indicator, backtest, entry_plan) = OBSERVE_UNBOUND (no session needed). MUTATE tools (ledger write, handoff) = require valid session via HTTP bridge.

### MCP transport coercion

All params arrive as strings. Use CoercedList, CoercedDict, CoercedDictList types.

### Receipt persistence

Middleware writes receipts to /root/VAULT999/wealth/receipts.jsonl. Tools do not call _emit_receipt() directly.

## Hardening Checklist (Phase 1)

### 1. Split canonical.py (3461 lines)

One file per tool under wealth_mcp/tools/. Each file has one register_X_tools(mcp) function. __init__.py calls all.

### 2. Add tests for indicator/backtest/entry_plan

Three production tools have zero test coverage. Test: RSI range, MACD signal+histogram, Ichimoku 5 lines, backtest SMA crossover, backtest empty data, entry_plan S/R levels, entry_plan missing data error.

### 3. Replace legacy routing in capital_market stock mode

capital_market(mode="stock") calls _call_legacy_tool("wealth_stock_analysis"). Replace with direct import from wealth_core/stock/.

### 4. Add retry/timeout to external API calls

In commodity_engines.py and crypto/router.py: httpx AsyncClient, 3-retry exponential backoff, 10s timeout.

### 5. Standardize error envelope

All modes return structured errors (status ERROR, error_code, message). Never raise ValueError. Some modes currently raise.

## New Tool Development (Phase 2)

### Adding a new mode

1. Add to if-m chain in canonical.py
2. Add to valid_modes in error fallback
3. Import from wealth_core/
4. wrap_result()
5. Add test
6. Update docs/mcp-tool-families-spec.md

### Adding a new tool

1. Create wealth_mcp/tools/<name>.py
2. register_<name>_tools(mcp)
3. @mcp.tool() with output_schema=WEALTH_OUTPUT_SCHEMA
4. Add to CAPITAL_TOOL_NAMES in __init__.py
5. Register in server.py create_mcp_server()
6. Add test
7. Update docs/mcp-tool-families-spec.md

### Priority new tools

**XAUUSD:** capital_signal (indicator+regime+volume -> signal), capital_chart (mplfinance PNG)
**Power:** capital_power (expose wealth_core/power/ already built but not exposed)
**Institutional:** verify capital_diagnose covers all wealth_core/institutional/ modes

## Pitfalls

- canonical.py is SOT — docs are documentation, not truth
- Never import arifosmcp into WEALTH (Zen 2026-07-11 FNF-0)
- capital_entropy optional — return UNAVAILABLE when dependency absent
- Receipt failure is not tool failure
- _call_legacy_tool() is compat shim — new code imports from wealth_core/ directly
- 3 tools have zero tests — treat outputs as provisional
- Canonical 8 registered via register_canonical_tools(), added tools registered separately in server.py
