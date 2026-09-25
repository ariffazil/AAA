---
name: market-prediction-falsification
description: Use when asked to predict a market. Falsify, then size.
category: wealth
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Market Prediction Falsification

> The absence of the claim is the finding.

Load when a human asks "what will X do", when a chart pattern or indicator is offered as a predictor of a
move or a collapse, or when a forecasting system is about to be quoted as a reason to act.

The instinct to answer a prediction question with a prediction is the failure this skill exists to stop. A
forecast you cannot falsify is a story, and a story about prices is worse than silence because the human will
trade on it.

## The rule

**Never assert a predictive claim you have not tried to falsify, and never present a forecast without
showing the baseline it must beat.**

If the test fails, report the failure as the answer. A null result tells the human something true and
useful — that the tool they were about to trust carries no edge — and it is worth more than a confident
direction would have been.

## Procedure

### 1. Decide what is being claimed

- **A rule** — "this pattern precedes a collapse", "this filter catches the bad ones". Testable
  cross-sectionally, over many observations. Use the **base-rate test** (step 2).
- **A predictor** — "I/we/the model can call this". Testable only by commitment. Use the **blind commitment
  test** (step 3).

Both may be needed. A rule can pass the base-rate test and still not make anyone able to predict.

### 2. Base-rate test (a rule)

For every observation of the signal state, record whether the outcome followed inside the horizon.

```
base rate   = P(outcome)
conditional = P(outcome | signal)
sensitivity = P(signal | outcome)      <- the number that kills most indicators
specificity = P(-signal | -outcome)
lift        = conditional / base rate
```

**Specificity is the mirage.** "Always say no" scores high specificity, and so does a signal that almost
never fires. Only `sensitivity` says whether the signal actually catches the events it claims to detect.

**The kill criterion:** if `sensitivity` is low while `lift` is only modestly above 1, the signal cannot be a
diagnosis — it can only be a trigger. Say so in those words.

Worked example, EMA50 < EMA200 ("death cross", monthly) as a predictor of ≥50% drawdown within 24 months, 30
large caps over all available history: **7,858 stock-months; base rate 4.1%; conditional 7.5%; sensitivity
7.8%; specificity 95.9%; lift 1.84×.** It misses more than nine in ten of the events it is claimed to detect.

### 3. Blind commitment test (a predictor)

1. Pick N cases. **N ≥ 4 for a binary call** — with 3 cases a coin scores 33% and the test proves nothing.
2. Build each chart: normalise to 100 at the cut; strip names, tickers, dates and prices.
3. Assign labels by **seeded shuffle**, so label order carries no information about which case is which.
4. Write the truth map to a **separate file** and do not read it.
5. Get the answer committed — with **confidence** — before the reveal.
6. Score against the trivial baseline: all-"no", or always-up.

**Discipline that makes it a test rather than a demonstration:**

- **Compute the truth without reading it.** Write it to a separate artefact in the same run that builds the
  charts; do not print it into your own context.
- **State the commitment in the message BEFORE the reveal.** If the reveal and the commitment arrive together,
  the reader cannot tell which came first and the whole thing degrades into hindsight.
- **Score yourself honestly and say the verdict plainly** — including "this beat the baseline by nothing".
  Measured: an agent scored 6/8 on eight anonymised charts, identical to answering "no" eight times without
  looking once.

### 4. Answer the question that was actually askable

When the honest answer is "the direction is unknowable", do not stop there — the human asked because they have
a position. Redirect to the arithmetic that *is* knowable:

> `p` (how often you win) × `RR` (how big the win) × `f` (how much you stake)

`p` is unknowable and must never be manufactured. `RR` follows from the entry and the stop. **`f` is the only
variable entirely inside the human's control, and it is the one nobody asks about.**

Then answer the real question — for this volatility and this horizon, will the stop be hit by ordinary noise
before the thesis can ever pay? Full arithmetic, the ruin table, the forward cone, the barrier Monte Carlo and
the Kelly curve: `references/position-sizing-and-edge-mathematics.md`.

## Domain epistemics — what a chart is worth (never collapse these)

This is where most "the chart predicts the company" claims must be rejected.

**"Gold has no fundamentals" is WRONG.** USD is the other leg of the pair, and USD has a president, an FOMC,
an NFP and a CPI. The real distinction is **symmetry of information**:

| | Gold (XAUUSD) | A listed company | PETRONAS |
|---|---|---|---|
| Fundamentals exist? | Yes — via USD | Yes | Yes |
| How they arrive | **Public, scheduled, simultaneous** — dates published a year ahead, everyone reads 8:30pm together, nobody front-runs CPI | **Hidden, controlled, staggered** — insiders know before the market does | Not observable from outside |
| Symmetry | Symmetric | Asymmetric | — |
| What the chart is | Technical analysis *is* the reality | The chart is the *belief* of others, and belief can be faked | No chart exists |

- **Gold** — no counterparty, no CEO, no auditor, no hidden books. Work can earn an edge; let the chart stand.
- **A company** — the chart is a *trace* of what others know, never a measurement of the business. It is blind
  to the **cause** and only reflects the **effect** once insiders are already selling. "It has never been sick
  before" is not a test: the companies that died looked healthiest immediately before dying.
- **PETRONAS** — no ticker, no public float, no insider-sell mechanism, no early warning. The chart that killed
  Enron cannot exist for it. The only honest remaining measure is money out to government versus capex in. Say
  that plainly rather than charting a proxy and calling it the company.

Two people can both be right here — one trades a commodity, one holds a business — because they are answering
different questions. Do not referee it as a dispute.

**Never present a post-hoc chart as a prediction.** A chart drawn after a collapse always shows a clean top.
If the series was reconstructed or the window chosen after the fact, stamp that on its face.

## Price-time physics — the actual invariant (state machine, not indicator pile)

> Added 2026-09-25 after Arif rejected the indicator-pile framing in a deep-research session.
> The corrections below replace any "this indicator says X" verdict that survives in this skill.

The marginal executable demand curve meets insufficient immediately available liquidity at the current price.
Every executed trade has a seller; what changes is the **marginal price to clear the next unit**. If offers
deplete or cancel, buy orders walk the book upward. Same physics on the downside.

```
ΔP_{t,h} ≈ (Q_net_aggressive + Q_forced_hedge + Q_forced_liquidation
            − Q_passive_absorption) / Λ_{t,h} + ε
```

where Λ is depth / liquidity elasticity. **Price impact ∝ signed urgency ÷ resilient liquidity** — NOT volume,
NOT DOM imbalance. The actionable variable is how depth behaves under stress, not displayed depth alone.

### Liquidity is not conserved

Executable liquidity is **state-dependent willingness to quote**, not conserved material. Orders can cancel,
hide, replenish, internalize, or shift across venues between snapshots. A static DOM image is weak evidence.
The dynamic behaviour of depth under stress is the evidence.

### The five-question loop (every bar close)

```
Q1  MACRO IMPULSE       — DXY, real yields, ETF/CB demand, geopolitical, risk repricing
Q2  POSITIONING/FLOW    — COT percentile, options OI map, CTA trend proxy, dealer-gamma scenario
Q3  LIQUIDITY RESILIENCE — spread percentile, replenishment, impact/volume ratio
Q4  AUCTION ACCEPTANCE   — value-area location, anchored VWAP acceptance, retest behavior
Q5  CALIBRATION HEALTH  — rolling Brier vs regime-conditional baseline
```

No signal may be emitted as a bare boolean. Every output carries `{state, regime, confidence, half_life,
disambiguators}`.

### Signal hierarchy (causal proximity × data integrity × regime fit × freshness)

| Rank | Signal family | Allowed verdict |
|------|---------------|-----------------|
| 1 | Auction acceptance / market structure | Primary direction verdict |
| 2 | Liquidity resilience | Continuation vs fragile-move classifier |
| 3 | Macro impulse | Regime + directional bias |
| 4 | Positioning / hedging flow | Amplification factor |
| 5 | Volatility state | Strategy choice + stop geometry |
| 6 | Bar / volume shape | Confirmation only, never primary |
| 7 | Oscillator divergence | Low-weight early warning only |

A slow indicator may NEVER veto a fast causal state transition without independent evidence.

### State machine (mutually exclusive tags)

| State | Operating mode |
|-------|----------------|
| `MARKET_INTEGRITY_FAIL` | `OBSERVE_ONLY` (feed dispersion / stale tick / abnormal cancel) |
| `COMPRESSION` | `BRACKET_AND_WAIT` |
| `COMPRESSION_TO_EXPANSION` | `PREP_TRIGGER` (requires six conditions, see below) |
| `ESTABLISHED_TREND` | `TRAIL_AND_HOLD` |
| `RANGE` | `ROTATION_ONLY` |
| `EXHAUSTION` | `REDUCE_OR_REVERSE` |

### Compression-to-expansion gate (six conditions, ALL required)

A break bar is NOT a regime transition. A close outside the BB is NOT a transition. Required:

1. Range escape (close outside structural edge).
2. Acceptance (≥ 2 consecutive bar closes outside).
3. Sustained signed flow in the breakout direction.
4. Realized volatility expansion from compressed baseline.
5. Macro / cross-asset does NOT contradict.
6. Retest behavior (broken edge holds, or price re-enters and fails to reclaim).

If any one fails → remain in `COMPRESSION`, do not chase the wick.

### What dynamics mean (do not infer intent from flow)

| Observed | Possibly means | NOT necessarily |
|----------|---------------|-----------------|
| Large buy volume, little upward move | Passive absorption OR two-sided auction | "Smart money accumulating" |
| Modest buy volume, big upward move | Offer withdrawal (fragile) | "Strong demand" |
| Visible bid imbalance, then cancellation | Spoofing / fragile display | Real institutional bid |
| Spread widens, depth shrinks | Liquidity stress | Normal volatility expansion |
| Price rises while signed flow weakens | Offer withdrawal | Healthy uptrend |

**Rule:** order flow ≠ price impact. Two markets can produce identical volume signatures with opposite
interpretation depending on liquidity resilience.

### Smart-money framing is narrative-dangerous

A large call-OI increase may mean customer upside bet, producer hedge, fund spread, dealer structured-product
hedge, institution rolling position, market-maker block facilitation, or delta-neutral vol trade. Observed
options flow ≠ directional institutional conviction until independently corroborated by trade initiation,
subsequent OI, IV/skew movement, spot/futures response, expiry, strike location, and post-trade hedge
behaviour. Same rule for dark-pool prints and COT positioning: commercials are hedging business risk, not
necessarily "right." COT positions are measured Tuesday, released Friday — never a timing trigger.

### Time-zone rule

LBMA fix windows are 10:30 and 15:00 **London** time. London and New York shift relative to Malaysia
during DST transitions. Agents MUST convert dynamically, not hard-code "16:00 MYT" or "21:00 MYT" session
labels. Use exchange/calendar timestamps.

### Calibration discipline (Brier is not portable)

A model can be calibrated yet economically useless (e.g. 52% across the board after cost returns negative
expectancy). Track four independent layers:

- **Discrimination** — rank IC, AUC, top-decile lift
- **Calibration** — reliability curve, Brier, log loss, ECE
- **Economic edge** — net expectancy after pessimistic cost, profit factor, turnover-adjusted Sharpe
- **Stability** — rolling metrics, regime-conditioned, live shadow monitoring

Block execution when rolling out-of-sample **Brier Skill Score** is non-positive over a precommitted window.
"Brier < 0.25" is NOT a universal threshold — depends on event base rate. A constant-base-rate forecast for a
35%-prevalence event has Brier 0.2275 without doing any work.

### Indicator-pile framing is rejected

Do not output "RSI bearish", "BB squeeze bullish", "volume climax reversal", "Wyckoff spring", or
"dealer-gamma gravity at strike X" as standalone verdicts. Same RSI reading in `COMPRESSION` vs
`ESTABLISHED_TREND_DOWN` means opposite things. **Context > signal.** Pattern without state tag is noise.
BB inside Keltner is a low-volatility envelope, NOT a Wyckoff spring. "3× volume = reversal" is FALSE as a
universal rule — high volume can mark reversal, continuation, absorption, news repricing, or liquidation.
The information is in the price response AFTER the volume, not the volume itself.

Candle anatomy (body-to-wick, close position, body vs ATR) is CONFIRMATION, not cause. These are outcome
summaries of the auction. Require auction acceptance and flow context before treating candle shape as a
verdict.

## Quoting a forecasting system

Before repeating any model's or oracle's accuracy, **read its own calibration and report it.** A system's
counters are the cheapest falsification available and they are usually unflattering.

- Report `active / ever-verified / ever-accurate` and the scoring rule, not a headline claim. A store with many
  live predictions and **zero** verified ones has demonstrated nothing; say "never been right yet" in those
  words rather than implying a track record.
- **An uncalibrated forecaster may not be laundered into a recommendation.** If the calibration is absent or
  empty, the system can be read for state but not cited for direction.
- **"No signal" is a valid, reportable output.** When a signal tool returns a flat verdict on the grounds of
  poor reward:risk or low confluence, report the tool's own reason verbatim. Manufacturing a direction to
  satisfy the question is the failure.
- Quote the live price leg from its own tool rather than from memory, and state the timestamp.

## Presentation

When the payload is numeric, **draw the contrast; do not tabulate it.** Arif has said plainly that figures are
the barrier: a table of seven risk levels produced "I don't understand", one labelled figure produced
comprehension and the next question. One panel per idea, three panels maximum, every panel labelled in words,
the **baseline shown beside the result**. Keep prose to one sentence per conclusion, and do not restate the
figure as prose — that trains the reader to skip the image. Full rule and build pitfalls:
`human-facing-artifact-design` §1 (fourth case) and `visual-artifact-delivery`.

## Pitfalls

- **Do not answer a prediction question with a prediction.** The most common failure is reading the question as
  a request for a forecast. It is a request for a basis to act; supply the basis or the honest absence.
- **Do not invent `p`.** A win rate estimated from a backtest that ignores slippage, spread and regime change is
  not a probability. If `p` is unknown, say unknown and size for ruin instead.
- **Reward:risk alone is a marketing number.** Two positions can quote `1:1.5` with win rates of 45% and 40%;
  the second has zero expectancy. Never let RR stand without the win rate beside it.
- **A single indicator is not a diagnosis.** Require the base-rate test before a pattern is allowed to carry an
  argument, and prefer two independent classes of evidence over two settings of the same class.
- **Do not reveal a sealed answer early.** Computing the truth and revealing it in the same turn destroys the
  test. Commit in one message, reveal in the next.
- **An unknown threshold is not a passed threshold.** If the baseline cannot be computed, the test has not been
  run — do not present a score as if it were measured against something.
- **Never let "the market is volatile" be the whole answer.** Volatility is the input to a range, and the range
  is actionable: it tells the human their stop sits inside the noise.

- **Indicator-pile framing is rejected (F13 2026-09-25).** Do not output "RSI bearish", "BB squeeze bullish",
  "volume climax reversal", "Wyckoff spring", or "dealer-gamma gravity at strike X" as standalone verdicts.
  Same indicator reading means opposite things in `COMPRESSION` vs `ESTABLISHED_TREND_DOWN`. Context > signal.
  Every signal must carry `{state, regime, confidence, half_life, disambiguators}`.

- **Brier < 0.25 is NOT a universal usability threshold (F13 2026-09-25).** A constant-base-rate forecast for a
  35%-prevalence event has Brier 0.2275 without doing any work. Gate execution on **Brier Skill Score > 0**
  over a precommitted rolling window, against a regime-conditional baseline. A calibrated model can still be
  economically useless — track net expectancy after pessimistic cost independently.

- **"Smart money" / institutional accumulation = narrative-dangerous (F13 2026-09-25).** A call-OI surge may
  be producer hedge, dealer structured product, customer spread, or roll — not directional conviction. Same
  for dark-pool prints and COT positioning. Never infer intent from a single trace.

- **DOM imbalance alone is weak evidence (F13 2026-09-25).** Top-of-book imbalance is easily stale, cancelled,
  or withdrawn. Require persistence across multiple bars, cancellation-adjusted depth, AND trade-execution
  confirmation (impact/volume ratio). Spoofing is normal.

- **Liquidity is state-dependent, not conserved (F13 2026-09-25).** A book showing 5,000 contracts at one
  instant can have 4,500 cancelled before the next trade. The actionable variable is how depth behaves under
  stress, not displayed depth.

- **Price impact ∝ signed urgency ÷ resilient liquidity, NOT volume (F13 2026-09-25).** A market can rally on
  modest volume if offers vanish (fragile upside), or stall despite massive buy volume if passive sellers
  absorb. Order flow and price impact are separate physics.

- **Fixed MYT session times are WRONG (F13 2026-09-25).** London (10:30 / 15:00) and NY open shift relative
  to Malaysia across DST transitions. Convert dynamically from exchange/calendar timestamps. Never hard-code
  "16:00 MYT" or "21:00 MYT".

- **COT "commercials are right" is FALSE (F13 2026-09-25).** COT classifies by self-reported business purpose
  (hedging vs speculative), not by who is directionally correct. Producer shorts may be prudent hedges while
  believing spot rises. Use as weekly positioning regime, not timing trigger.

- **Compression-to-expansion requires six conditions, all six (F13 2026-09-25).** A break bar is NOT a regime
  transition. A close outside the BB is NOT a transition. Range escape + acceptance + sustained flow + RV
  expansion + macro non-contradiction + retest behavior — drop any one and stay in `COMPRESSION`.

## Support files

- `references/position-sizing-and-edge-mathematics.md` — ruin table, forward cone from realised volatility,
  barrier/first-passage Monte Carlo, the Kelly curve, both falsification tests, and build notes.
