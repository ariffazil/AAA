---
name: market-prediction-falsification
description: Use when asked to predict a market. Falsify, then size.
category: wealth
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
  is actionable: it is what tells the human their stop sits inside the noise.

## Support files

- `references/position-sizing-and-edge-mathematics.md` — ruin table, forward cone from realised volatility,
  barrier/first-passage Monte Carlo, the Kelly curve, both falsification tests, and build notes.
