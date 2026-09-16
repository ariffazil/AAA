# XAUUSD Strategy Inventory & Gap Analysis
**Date:** 2026-08-26
**Canonical code:** `/root/WEALTH/trading/` (post 2026-07-19 migration from `/root/trading/`)

---

## 1. Existing Strategy Stack

### `/root/WEALTH/trading/apex/`
| File | What it does |
|------|-------------|
| `scanner.py` | EMA, SMA, RSI, MACD, ATR, Bollinger Bands, Parabolic SAR, S/R pivots, candlestick patterns (doji, hammer, engulfing, pin bar), trend detection. Pure-Python. |
| `regime.py` | Regime classification: UPTREND / DOWNTREND / SIDEWAYS from EMA20/50/200 alignment. Swing point detection. Zone clustering (0.5% threshold). |
| `apex_predictor.py` | APEX theory: G = A·P·E·X·Φ scalars, C_dark shadow, multi-TF witness (1H/4H/1D), volume confirmation, volatility regime (low/normal/high/extreme from ATR ratio). |

### `/root/WEALTH/trading/backtest/`
| File | What it does |
|------|-------------|
| `engine_v2.py` | Swing-zone strategy: regime-gated (skip SIDEWAYS), ATR-based SL (2× ATR), partial TP + trailing (1.5 ATR after 1R), RSI confirmation, max 2 positions, lot sizing. **Zero slippage/commission/spread.** |
| `engine.py` | Older v1 engine, superseded. |
| `metrics_enhanced.py` | Performance metrics (Sharpe, drawdown, etc.). |

### `/root/WEALTH/trading/risk/`
| File | What it does |
|------|-------------|
| `manager.py` | Drawdown tracking, daily loss cap. |
| `position_sizer.py` | Kelly criterion. **No vol-targeting.** |

### `/root/WEALTH/trading/governance/`
| File | What it does |
|------|-------------|
| `gate.py` | F1-F13 constitutional floor checks, verdict gate. |

### `/root/WEALTH/trading/config/`
| File | What it does |
|------|-------------|
| `trading_spec.json` | H1 primary, H4/D1 context, EMA20/50, RSI14, min RR 1:2, ideal 1:3, max 2 trades/day, sessions London/NY only, event filter (CPI/NFP/FOMC ±30/+60 min). |

### `/root/WEALTH/trading/reference/`
| File | What it does |
|------|-------------|
| `red-news-impact.md` | CPI/NFP/FOMC impact table + the 15-min rule (close T-15, watch T+15, re-enter T+30). Reference-only, not wired to code. |

### `/root/WEALTH/wealth_core/` (capital primitives — NOT wired to live XAUUSD signal)
| File | What it does |
|------|-------------|
| `alpha158.py` | 158-feature systematic engine (TradeMaster distillation). Price ratios, volume-price divergence, multi-period ATR ratios, momentum, mean reversion, microstructure proxies. **Exists but never wired to live signal.** |
| `regime_map.py` | Distribution-aware regime (BULL/BEAR/SIDEWAYS/VOLATILE/CRISIS), rolling std/skew/kurtosis, distribution-shift detection. **Not live-wired.** |
| `ensemble.py` | Voting layer, not a learner. |
| `stress_test.py`, `macro_diagnosis.py`, `commodity_engines.py`, `compass.py` | Capital intelligence primitives. |

---

## 2. Installed Packages (verified 2026-08-26)

| Package | Installed? | Notes |
|---------|:----------:|-------|
| backtrader 1.9.78 | ✅ | |
| TA-Lib 0.7.0 | ✅ | |
| yfinance 1.4.1 | ✅ | |
| oandapyV20 0.7.2 | ✅ | |
| textblob 0.20.1 | ✅ | Installed but **never imported** in trading code |
| transformers 5.12.1 | ✅ | Installed but **never imported** in trading code |
| sentence-transformers 5.6.0 | ✅ | Installed but **never imported** in trading code |
| nltk 3.10.2 | ✅ | Installed but **never imported** in trading code |
| ccxt | ❌ | Listed in SKILL.md but NOT installed |
| fredapi | ❌ | Listed in SKILL.md but NOT installed |
| pandas-ta | ❌ | Listed in SKILL.md but NOT installed |

---

## 3. Gap Analysis vs Reddit ML Scalper

| Pillar | Reddit scalper | WEALTH today | Gap |
|---|---|---|---|
| **Price/volume features** | 100+ OHLCV-derived | Alpha158 has 158 features, unused in live signals | Latent — exists, not wired |
| **Volatility features** | Garman-Klass, Parkinson, Yang-Zhang, vol-of-vol, ATR ratios, IV surface | One ATR ratio in scanner.py. alpha158.py has multi-period ATR ratios but no GK/PK/YZ. No realized-vol time series, no vol-of-vol. | **CRITICAL** — highest-ROI gap |
| **Sentiment features** | News NLP (FinBERT/VADER), Reddit/WSB chatter, Fear&Greed, COT, DXY-yield spreads | red-news-impact.md is reference-only markdown. No sentiment pipeline, no NLP module, no feed ingestion. textblob/transformers installed but unused. | **CRITICAL** — second pillar |
| **ML model layer** | GBM / LSTM on engineered features | No supervised model. ensemble.py is voting, not learning. | Medium — depends on features |
| **Backtest realism** | Tick-level fills, slippage, fees, spread-blowout on events | engine_v2 has zero slippage, zero commission, zero spread model. | Medium — easy to fix |
| **Position sizing** | Kelly + vol-targeting | Kelly + drawdown cap. No vol-targeting. | Low |
| **Regime gate** | HMM / CUSUM / change-point detection | EMA-based regime + APEX state. regime_map.py exists but not wired live. | Low |
| **Execution latency** | Sub-second | Hourly cron. Not a scalper stack. | Architectural mismatch |

---

## 4. Recommended Build Order

1. **Volatility feature engineering** (2 days) — Garman-Klass, Parkinson, Yang-Zhang, vol-of-vol, range compression. Pure-numpy, no new deps. Extends alpha158.py harness. Unlocks vol-targeting position sizing.
2. **Backtest realism** (1 day) — Slippage, commission, spread model, event-window spread blowout. Required to falsify any new feature's claimed edge.
3. **Sentiment pipeline** (5-7 days) — NewsAPI/FinBERT feed, DXY/US10Y cross-asset sentiment, Fear&Greed daily. Highest expected edge but highest engineering cost.
4. **ML model layer** (3-5 days) — GBM/LSTM on the feature set from steps 1+3. After both feature pillars are wired.
