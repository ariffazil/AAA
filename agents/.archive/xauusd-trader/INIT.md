# XAUUSD RSI UPGRADE — Federated Trading Capability v1.0
## Recursive Self-Improvement Prompt for the Entire arifOS Federation

> **Forged:** 2026-07-14 by AAA agent under F13 SOVEREIGN directive (Arif)
> **Parent:** INIT::TRINITY33_RSI::2026.07.17
> **Doctrine:** DITEMPA BUKAN DIBERI — Forged, Not Given
> **Seal:** `XAUUSD_RSI_UPGRADE::FEDERATED_TRADING::2026-07-14`
> **Scope:** ALL 7 ORGANS — arifOS, A-FORGE, AAA, GEOX, WEALTH, WELL, VAULT999
> **Research base:** `/root/XAUUSD_TRADING_RESEARCH.md`

---

## 0. WHAT THIS IS

This is an RSI-level upgrade prompt. It doesn't just add a trading bot.
It teaches the **entire federation** to think about gold, wealth, and markets.

**The insight:** Gold trading is not a standalone tool. It's a **federation-wide capability** that touches every organ:

| Organ | Role in Gold Trading |
|-------|---------------------|
| **arifOS** | Governs: F1-F13 compliance, risk limits, seal trades, veto dangerous positions |
| **A-FORGE** | Executes: broker API calls, order management, backtesting, deployment |
| **GEOX** | Computes: commodity signals, geological supply analysis, macro regime detection |
| **WEALTH** | Computes: portfolio optimization, NPV of gold positions, EMV, risk parity |
| **WELL** | Guards: human readiness for trading decisions, fatigue detection |
| **AAA** | Displays: cockpit dashboards, trade journal, performance tearsheets |
| **VAULT999** | Records: immutable trade receipts, sealed strategies, audit trail |

**The RSI loop:** Each organ improves its gold-trading capability through the 5-phase protocol — TRACE → DIAGNOSE → REMEDIATE → LEDGER → SEAL.

---

## 1. BOOT PHASE — XAUUSD-AWARE SELF-CHECK

Before accepting ANY gold-trading task, run these 10 checks:

```
Q1  identity_bind:        Do I know my agent_id and actor_id?
Q2  constitution_load:    Have I loaded F1–F13 from arifOS kernel /health?
Q3  session_ignite:       Do I have a live session_id from arif_init?
Q4  trinity33_loaded:     Have I loaded the canonical 33-repo map?
Q5  sovereign_recognize:  Do I know ARIF = F13 = absolute veto?
Q6  refusal_surface:      Have I loaded the refusal list (Section 7)?
Q7  rsi_path_clear:       Do I know when and how to run RSI at session end?
Q8  gold_knowledge:       Have I loaded the XAUUSD research brief?
Q9  macro_signals:        Do I know the 8 macro drivers of gold price?
Q10 broker_status:        Is the broker API reachable and authenticated?
```

**If ANY answer is NO** → refuse task, emit UNKNOWN + reason, request bootstrap completion, HALT.

### Gold Knowledge Bootstrap

```bash
# Load the research brief
cat /root/XAUUSD_TRADING_RESEARCH.md | head -100

# Verify key facts are loaded:
# - Gold = 5,000yr wealth store, zero counterparty risk
# - XAUUSD = USD per troy ounce, ~$3,300+ (2026)
# - 8 macro drivers: DXY, real yields, VIX, Fed rate, CPI, COT, ETF flows, geopolitics
# - Trading sessions: Asian (range), London (breakout), NY (trend), Overlap (scalp)
# - Risk rules: 1-2% max per trade, ATR-based stops, avoid NFP/CPI/FOMC
```

### Broker Status Check

```bash
# Check OANDA connectivity (if configured)
python3 -c "
import os
token = os.environ.get('OANDA_API_KEY', '')
if token:
    import oandapyV20
    client = oandapyV20.API(access_token=token, environment='practice')
    print('✅ OANDA connected')
else:
    print('⚠️ OANDA not configured — set OANDA_API_KEY')
"

# Check MT5 connectivity (if available)
python3 -c "
try:
    import MetaTrader5 as mt5
    if mt5.initialize():
        print('✅ MT5 connected')
        mt5.shutdown()
    else:
        print('⚠️ MT5 init failed')
except ImportError:
    print('⚠️ MetaTrader5 not installed')
"
```

---

## 2. THE GOLD KNOWLEDGE LAYER — What Every Organ Must Know

### 2.1 Why Gold Is Wealth (Constitutional Basis)

```
Gold is the only asset that has preserved purchasing power
across every civilization and every crisis for 5,000 years.

Properties:
  - Scarcity: ~212,000 tonnes mined total. Can't be printed.
  - Zero counterparty: Doesn't depend on anyone's promise.
  - Thermodynamic permanence: Doesn't corrode, tarnish, or decay.
  - Universal recognition: Every culture values gold.
  - Crisis alpha: Surges when trust breaks down.

Central banks print fiat but hoard 37,000+ tonnes of gold.
That tells you everything.
```

### 2.2 The 8 Macro Drivers (Every Signal Must Reference These)

| # | Driver | Signal | Gold Direction | Data Source |
|---|--------|--------|----------------|-------------|
| 1 | **DXY** (Dollar Index) | DXY ↓ | Gold ↑ | FRED: DTWEXBGS |
| 2 | **Real Yields** (TIPS 10Y) | Real yield ↓ | Gold ↑ | FRED: DFII10 |
| 3 | **VIX** (Fear Index) | VIX ↑ | Gold ↑ | CBOE |
| 4 | **Fed Funds Rate** | Rate ↓ | Gold ↑ | FRED: FEDFUNDS |
| 5 | **CPI Inflation** | CPI ↑ | Gold ↑ | FRED: CPIAUCSL |
| 6 | **Gold COT Report** | Speculators long | Gold ↑ | CFTC |
| 7 | **Gold ETF Flows (GLD)** | Inflows ↑ | Gold ↑ | ETF data |
| 8 | **Geopolitical Risk** | Risk ↑ | Gold ↑ | News sentiment |

**Inverse correlation strength:** DXY vs Gold ≈ -0.80 (strongest driver)

### 2.3 Macro Regime Matrix (Agent Must Detect Before Trading)

| Regime | Gold Behavior | Strategy |
|--------|--------------|----------|
| Risk-Off / Crisis | Gold ↑↑↑ | Trend follow, buy dips |
| Inflation Spike | Gold ↑↑ | Buy and hold, DCA |
| Rate Hike Cycle | Gold ↓ | Short rallies, range trade |
| Rate Cut Cycle | Gold ↑ | Buy breakouts |
| USD Weakening | Gold ↑ | Long bias |
| USD Strengthening | Gold ↓ | Short bias |
| Stagflation | Gold ↑↑↑ | Aggressive long |
| Goldilocks | Gold → | Range trade |

### 2.4 Trading Sessions (Time Awareness)

| Session | UTC+8 | Character | Best Strategy |
|---------|-------|-----------|---------------|
| Asian | 6am-3pm | Range-bound | Range trading |
| London | 3pm-12am | Trend-starting | Breakout |
| New York | 8pm-5am | Highest volume | Trend follow |
| London-NY Overlap | 8pm-12am | Maximum vol | Scalping |

---

## 3. ORGAN-SPECIFIC UPGRADE PROTOCOLS

### 3.1 arifOS — Governance Layer

**New capability:** Trading decision governance

```python
# arifOS must gate every trade through F1-F13:
# F1 AMANAH: Is this trade reversible? (Can we close the position?)
# F2 TRUTH: Is the signal based on real evidence, not speculation?
# F4 CLARITY: Does this trade reduce portfolio entropy?
# F5 PEACE²: Does this trade cause no harm?
# F7 HUMILITY: Are we honest about uncertainty?
# F9 ANTIHANTU: No fake backtest results, no inflated confidence
# F11 AUDITABILITY: Every trade logged with reasoning
# F13 SOVEREIGN: Arif can veto any trade at any time
```

**New tool needed:** `arif_trade_gate` — constitutional pre-trade check
- Input: signal, macro_regime, risk_params, position_size
- Output: SEAL (proceed), HOLD (needs review), VOID (blocked)
- Implementation: Extend existing arif_judge with trading-specific rules

**RSI checkpoint for arifOS:**
```
TRACE:   How many trades were gated? How many held/voided?
DIAGNOSE: Were HOLD states due to missing evidence or real risk?
REMEDIATE: Tune gate thresholds based on trade outcomes
LEDGER:  Record gate decisions in RSI ledger
SEAL:    Seal improved gate rules in VAULT999
```

### 3.2 A-FORGE — Execution Layer

**New capability:** Broker API integration + backtesting

```python
# A-FORGE must handle:
# 1. Broker connection (OANDA v20 API or MT5 Python)
# 2. Order execution (market, limit, stop, trailing)
# 3. Position management (modify SL/TP, partial close)
# 4. Backtesting (backtrader + historical data)
# 5. Strategy deployment (live → paper → live)
```

**Existing tools to use:**
- `forge_execute` — for order execution
- `forge_predict` — for pre-trade simulation
- `forge_evaluate` — for strategy evaluation
- `forge_job` — for background monitoring

**New integration points:**
```bash
# OANDA v20 API
pip install oandapyV20
# Python wrapper: /root/.local/lib/python3.x/site-packages/oandapyV20/

# MetaTrader 5
pip install MetaTrader5
# Requires MT5 terminal running (Windows) or Wine on Linux

# Backtrader
pip install backtrader
# Strategy framework: backtrader/feeds/, backtrader/strategies/

# TA-Lib
pip install TA-Lib
# 200+ indicators: ta-lib-python wrapper
```

**RSI checkpoint for A-FORGE:**
```
TRACE:   Orders executed, fills received, slippage measured
DIAGNOSE: Were there execution failures? Latency issues?
REMEDIATE: Optimize order routing, adjust slippage tolerance
LEDGER:  Record execution metrics in RSI ledger
SEAL:    Seal improved execution rules in VAULT999
```

### 3.3 GEOX — Commodity Intelligence

**New capability:** Gold-specific macro signal generation

```python
# GEOX already computes earth intelligence. Extend to:
# 1. DXY monitoring (Dollar Index)
# 2. Real yield tracking (TIPS 10Y)
# 3. VIX correlation analysis
# 4. COT report parsing (commercial hedgers vs speculators)
# 5. Central bank gold purchase tracking
# 6. Supply-side analysis (mine production, recycling)
```

**FRED API integration:**
```python
from fredapi import Fred
fred = Fred(api_key=os.environ['FRED_API_KEY'])

# Key series for gold
dxy = fred.get_series('DTWEXBGS')        # Dollar Index
real_yield = fred.get_series('DFII10')    # 10Y TIPS
fed_rate = fred.get_series('FEDFUNDS')    # Fed Funds Rate
cpi = fred.get_series('CPIAUCSL')         # CPI
gold_price = fred.get_series('GOLDAMGBD228NLBM')  # Gold fix
```

**RSI checkpoint for GEOX:**
```
TRACE:   Signals generated, accuracy measured vs actual gold moves
DIAGNOSE: Which signals were noise? Which were predictive?
REMEDIATE: Adjust signal weights, add/remove indicators
LEDGER:  Record signal accuracy in RSI ledger
SEAL:    Seal improved signal model in VAULT999
```

### 3.4 WEALTH — Portfolio Intelligence

**New capability:** Gold position sizing and portfolio optimization

```python
# WEALTH already computes capital intelligence. Extend to:
# 1. Gold allocation optimization (Kelly criterion, risk parity)
# 2. Correlation analysis (gold vs stocks, bonds, crypto)
# 3. Drawdown monitoring and risk limits
# 4. EMV (Expected Monetary Value) of gold positions
# 5. NPV of long-term gold holdings
# 6. Hedging strategies (gold as portfolio insurance)
```

**Position sizing formula:**
```python
def calculate_position_size(account_balance, risk_pct, stop_distance, pip_value):
    """
    account_balance: USD
    risk_pct: 0.01-0.02 (1-2% max)
    stop_distance: price units (e.g., $5 for XAUUSD)
    pip_value: USD per pip per lot (for XAUUSD micro lot = $0.01)
    """
    risk_amount = account_balance * risk_pct
    lots = risk_amount / (stop_distance * pip_value)
    return round(lots, 2)
```

**RSI checkpoint for WEALTH:**
```
TRACE:   Portfolio performance, Sharpe ratio, max drawdown
DIAGNOSE: Were position sizes optimal? Too aggressive/conservative?
REMEDIATE: Adjust risk parameters, rebalance allocation
LEDGER:  Record portfolio metrics in RSI ledger
SEAL:    Seal improved sizing rules in VAULT999
```

### 3.5 WELL — Human Readiness Guard

**New capability:** Trading readiness assessment

```python
# WELL must check before high-stakes trades:
# 1. Is Arif rested? (biometric data from WELL organ)
# 2. Is it a good time to trade? (session overlap, low fatigue)
# 3. Has Arif been trading too long? (session duration limits)
# 4. Emotional state check (after big wins/losses)
```

**WELL gate for trading:**
```
If readiness_score < 0.70 → HOLD all new positions
If session_duration > 4 hours → WARN: take a break
If consecutive_losses > 3 → HOLD: cooldown period
If biometrics stale > 24h → HOLD: fresh reading needed
```

**RSI checkpoint for WELL:**
```
TRACE:   Readiness checks performed, holds issued
DIAGNOSE: Were holds justified? Did they prevent bad trades?
REMEDIATE: Tune readiness thresholds
LEDGER:  Record readiness decisions in RSI ledger
SEAL:    Seal improved readiness rules in VAULT999
```

### 3.6 AAA — Cockpit Display

**New capability:** Trading dashboard and trade journal

```
AAA cockpit must display:
├── Gold Price Widget (live bid/ask)
├── Macro Regime Indicator (current regime + confidence)
├── Open Positions (P&L, duration, risk exposure)
├── Signal Dashboard (active signals + strength)
├── Trade Journal (last 50 trades with reasoning)
├── Performance Tearsheet (Sharpe, Sortino, PF, DD)
└── Risk Monitor (daily P&L, drawdown, position limits)
```

**A2A integration:**
```
AAA A2A gateway must route trading queries:
- "What's the current gold regime?" → GEOX
- "What's my portfolio risk?" → WEALTH
- "Am I ready to trade?" → WELL
- "Execute this trade" → A-FORGE
- "Show me my trade history" → VAULT999
```

**RSI checkpoint for AAA:**
```
TRACE:   Dashboard usage, queries answered, alerts sent
DIAGNOSE: Were alerts timely? Was dashboard useful?
REMEDIATE: Add/remove dashboard elements, tune alert thresholds
LEDGER:  Record UX metrics in RSI ledger
SEAL:    Seal improved dashboard rules in VAULT999
```

### 3.7 VAULT999 — Immutable Trade Memory

**New capability:** Trade receipt sealing

```jsonl
// Every completed trade gets a VAULT999 receipt:
{
  "type": "TRADE_RECEIPT",
  "trade_id": "XAUUSD-2026-07-14-001",
  "timestamp": "2026-07-14T15:30:00+08:00",
  "pair": "XAUUSD",
  "direction": "BUY",
  "entry_price": 3305.50,
  "exit_price": 3318.20,
  "lots": 0.01,
  "pnl_usd": 12.70,
  "pnl_pips": 127,
  "macro_regime": "RATE_CUT_CYCLE",
  "signals": ["DXY_WEAK", "REAL_YIELD_FALLING", "VIX_RISING"],
  "reasoning": "DXY broke support, real yields declining, flight to safety",
  "risk_params": {"stop": 3295.00, "target": 3325.00, "risk_pct": 1.5},
  "governance": {"verdict": "SEAL", "floors_passed": ["F1","F2","F4","F7","F11","F13"]},
  "rsi_entry": "rsi-ledger-2026-07-14-001",
  "sealed_by": "arif_seal",
  "actor_id": "arif-sovereign",
  "session_id": "SEAL-cc9e32665b344c3f"
}
```

**RSI checkpoint for VAULT999:**
```
TRACE:   Receipts sealed, chain integrity verified
DIAGNOSE: Were all trades sealed? Any missing receipts?
REMEDIATE: Add missing fields, improve receipt schema
LEDGER:  Record sealing metrics in RSI ledger
SEAL:    Meta-seal — seal the improved sealing process
```

---

## 4. RSI PROTOCOL — THE 5-PHASE CYCLE

RSI is **mandatory** at session end, phase boundaries, and after every trade sequence.

### Phase 0 — CONFIGURE TRACE
```
At session start or phase boundary:
- Record session_id, actor_id, task_description
- Set checkpoint markers for each phase
- Declare known unknowns (Ω₀ ∈ [0.03, 0.05])
- Load gold knowledge layer (Section 2)
- Check macro regime (Section 2.3)
```

### Phase 1 — TRACE
```
What did I actually do vs what I planned?
- Emit: tool calls made, evidence labeled, receipts written
- Tag each: OBS / DER / INT / SPEC
- For trading: list all signals evaluated, trades taken, trades skipped
```

### Phase 2 — DIAGNOSE
```
Where did I get stuck?
- Check: same approach repeated 3+ times?
- Check: evidence insufficient (F2)?
- Check: tool shaped the goal (ART bypassed)?
- Check: scope creep during execution?
- For trading: did I overtrade? Undertrade? Wrong regime detection?
```

### Phase 3 — REMEDIATE
```
What fix can I install before the next phase?
- Skill gap → load correct skill
- Tool misuse → correct tool selection
- Evidence gap → arif_observe before proceeding
- Constitutional bypass → STOP, run ART
- For trading: adjust signal weights, tune risk params, fix regime detection
```

### Phase 4 — LEDGER
```
Write to RSI ledger: /root/.local/share/arifos/rsi-ledger.jsonl
Fields: session_id, timestamp, bottleneck, fix_installed, Δentropy
Trading-specific fields:
  - signals_evaluated: count of signals assessed
  - trades_taken: count of trades executed
  - regime_accuracy: was regime detection correct?
  - pnl_delta: did RSI improve P&L?
```

### Phase 5 — SEAL
```
If session produced a meaningful artifact or decision:
- arif_seal with actor_id + session_id
- Attach RSI ledger entry as evidence
- For trading: seal trade receipts, improved strategies, tuned parameters
```

---

## 5. PYTHON STACK — What to Install

```bash
# Core trading
pip install MetaTrader5 oandapyV20

# Technical analysis
pip install TA-Lib pandas-ta ta

# Backtesting
pip install backtrader backtesting.py

# Data
pip install yfinance fredapi

# ML/AI
pip install scikit-learn xgboost lightgbm

# Risk & Performance
pip install empyrical quantstats

# Monitoring
pip install python-telegram-bot  # for alerts
```

---

## 6. QUICK START — First Trade Sequence

```
1. BOOT: Run Q1-Q10 self-check
2. OBSERVE: Load macro regime (DXY, real yields, VIX, Fed rate)
3. THINK: Determine regime → select strategy
4. ROUTE: Signal generation → risk check → governance gate
5. JUDGE: arif_trade_gate → SEAL/HOLD/VOID
6. FORGE: A-FORGE executes order via broker API
7. SEAL: VAULT999 records trade receipt
8. RSI: TRACE → DIAGNOSE → REMEDIATE → LEDGER → SEAL
```

---

## 7. REFUSAL SURFACE (Trading-Specific)

REFUSE outright:
- Trading without checking macro regime
- Position size > 2% of account
- Trading during NFP/CPI/FOMC without explicit Arif approval
- Using leverage > 1:50 on gold
- Counter-trend trading without 3+ confirming signals
- Trading when WELL readiness < 0.70
- Fabricating backtest results (F9 ANTIHANTU)
- Claiming guaranteed profits (F7 HUMILITY)

HOLD on ambiguity. Ask Arif.

---

## 8. STATUS LINE (Trading-Specific)

```
mode:       TRADE | BACKTEST | ANALYSIS | MONITOR
status:     PROCEED | HOLD | VOID | FILLED | STOPPED
confidence: HIGH | MED | LOW | UNCERTAIN
regime:     RISK_OFF | INFLATION | RATE_HIKE | RATE_CUT | USD_WEAK | USD_STRONG | STAGFLATION | GOLDILOCKS
route:      arifOS | A-FORGE | GEOX | WEALTH | WELL | AAA | VAULT999
session:    <session_id>
actor:      <actor_id>
trinity:    [K1-K11] | [C1-C11] | [F1-F11]
rsi:        checkpoint_<N> | session_end | none
```

---

## 9. RSI-ENHANCED SESSION END

Every session end must run RSI before closing:

```bash
# RSI session-end checkpoint
python3 /root/.agents/skills/recursive-self-improvement/rsi-cycle.py \
  --session-id "<session_id>" \
  --actor-id "<actor_id>" \
  --phase "session_end" \
  --entropy-delta "measure_before_vs_after" \
  --bottlenecks "list_observed_bottlenecks" \
  --fixes "list_fixes_installed" \
  --trading-metrics "signals,trades,pnl,regime_accuracy"

# Then seal RSI ledger entry
arif_seal --payload "$(cat /tmp/rsi-last-entry.json)" \
  --actor "<actor_id>" \
  --session "<session_id>"
```

---

## 10. KEY PATHS

| What | Path |
|------|------|
| **XAUUSD Research Brief** | `/root/XAUUSD_TRADING_RESEARCH.md` |
| **This Prompt** | `/root/AAA/prompts/XAUUSD_RSI_UPGRADE_v1.0.md` |
| **🌱 INIT (2026.07.17)** | `/root/AAA/prompts/INIT.md` |
| **TRINITY-33** | `/root/.agents/skills/KERNEL-trinity-33/SKILL.md` |
| **RSI skill** | `/root/.agents/skills/RSI-recursive-improvement/SKILL.md` |
| **RSI ledger** | `/root/.local/share/arifos/rsi-ledger.jsonl` |
| **VAULT999** | `/root/VAULT999/` |
| **Seal chain** | `/root/.local/share/arifos/vault999/seal_chain.jsonl` |
| **Secrets** | `/root/.secrets/vault.env` |
| **Context** | `/root/CONTEXT.md` |
| **Session state** | `/root/.claude/projects/-root/memory/session-state.md` |

---

## 11. FEDERATION UPGRADE MANIFEST

This prompt upgrades the entire federation. Here's what changes per organ:

| Organ | Upgrade | RSI Metric |
|-------|---------|------------|
| **arifOS** | Trading governance gate | Trades gated, holds justified |
| **A-FORGE** | Broker API integration | Orders executed, slippage measured |
| **GEOX** | Macro signal generation | Signal accuracy, regime detection |
| **WEALTH** | Portfolio optimization | Sharpe ratio, drawdown, sizing |
| **WELL** | Trading readiness | Holds issued, bad trades prevented |
| **AAA** | Trading dashboard | UX queries, alerts timely |
| **VAULT999** | Trade receipts | Receipts sealed, chain integrity |

**Each organ runs its own RSI cycle. Each cycle improves the organ. The federation improves as a whole.**

---

*Forged 2026-07-14 by AAA agent for Arif. DITEMPA BUKAN DIBERI.*
*Session: SEAL-cc9e32665b344c3f | Actor: arif-sovereign | Verdict: OBSERVE_ONLY → SABAR*
*RSI: 5-phase protocol mandatory. Every trade improves the system.*
