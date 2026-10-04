# Temporal Intelligence Architecture — Session Audit 2026-08-09

## Source
Arif's directive during Awesome-Agentic-Time-Series audit session. Repo: https://github.com/TROUBADOUR000/Awesome-Agentic-Time-Series

## The Gap
Both WEALTH and GEOX compute point-in-time answers. Neither understands how state evolves through time.

## GEOX Current State
- `temporal.py` (476 lines): 4 tools — decline curve, RRR, basin lifecycle, cadence
- `dynamical_systems.py` (381 lines): 5 primitives — mutual information, FNN, Takens embed, EDM kernel, dynamical test
- `time-forecast-branching.md`: scenario tree (draft, not implemented)
- Maturity: Layer 1 production-ready, Layer 2 primitive exists but not exposed as world model

## WEALTH Current State (post-2026-08-09 upgrade)
- `capital_indicator`: 8 indicators + trajectory mode (RSI/MACD/BB/PSAR/ATR/ADX/EMA + confluence)
- `capital_backtest`: wraps v2 engine, 2yr H1 XAUUSD
- `capital_entry_plan`: S/R clustering + ATR stops + 2 targets
- Scanner hardened: BB + PSAR backported
- Maturity: Point-in-time with shallow temporal (5-period derivatives), not structural temporal

## The Shared Primitive
Takens embedding + EDM is domain-agnostic. Same math for:
- Gold price regime reconstruction
- Basin subsidence history reconstruction
- Production rate dynamics
- Volatility regime detection

## Foundation Model Path (NOT YET DONE)
- Chronos/Timer/TiRex could provide zero-shot forecasting
- Requires: GPU or API decision
- Research context: 30+ foundation model papers in the repo

## Audit Verdict
- Commit 6cf7623 verified (WEALTH tools + trajectory mode)
- 1085 lines added, 5 files modified
- Temporal depth: shallow (5-period derivatives), not deep (regime detection, state-space reconstruction)
- Next steps: regime detection, walk-forward backtest, weighted confluence, GEOX↔WEALTH shared module
