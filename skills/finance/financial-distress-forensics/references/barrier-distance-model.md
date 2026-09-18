# Barrier-distance model — derivation, failure modes, calibration

The underlying object is a first-passage problem: a firm fails the first time its value
touches a barrier. Distance to that barrier is not a matter of opinion, and neither is
the rate at which the barrier is closing.

## Core quantity

```
distance   D = ln(assets / liabilities)        # log gap to the debt barrier
gap-closing rate  λ = -(ΔD) / Δt               # per year, over a multi-year window

time to barrier   T = D / λ                    # years;  unbounded when λ <= 0
```

`λ ≤ 0` means the gap is **widening** — the firm is pulling away from the barrier and the
honest answer is "not on this trajectory", not a large finite number.

### Amplifiers

- **Negative operating cash flow** accelerates the close: divide T by `(1 + |OCF|/assets)`,
  capped so a single bad year cannot drive the estimate to zero.
- **A maturity wall** is a *deterministic* λ spike. This is the mechanism behind failures that
  look sudden in a headline — a refinancing that does not roll is a scheduled event, not an
  accident. Where a debt-maturity ladder is available, prefer it to a measured λ.

## Two failure modes — two detector families

| Mode | Mechanism | Detector |
|---|---|---|
| **Erosion** | distance closes steadily over years | `T = D / λ` |
| **Fabrication** | distance looks healthy; cash never arrives | `OCF ÷ net income`, `cash ÷ total borrowings`, accrual-gap measures |

**Neither detector alone is sufficient.** A company can walk toward its barrier while reporting
profit every year, and the reported-profit line is the one being watched.

### Why the barrier term is blind to fabrication

`D = ln(assets / liabilities)`. When the fabricated item is **assets**, inflating them
*increases* D. The metric reports improving health precisely as the lie gets larger. Publish the
cash pair beside it, every time.

### Reading the cash pair

- **`OCF ÷ net income`** — how much cash each unit of reported profit actually produced. A
  genuine operation converts at or above ~1. Sustained readings well below 1 mean the profit
  exists only on paper.
- **`cash ÷ total borrowings`** — the ability to service debt from hand. Watch the *shape*: a
  monotone decline across every year is stronger evidence than any single low reading, because
  it needs no restatement, no audit finding, and no announcement.

## Calibration observed in a single validation pass

Treat as order-of-magnitude expectations, not constants — they come from one sample.

**Against companies that actually failed** (13 firms, filed balance sheets, measured in the
years before the event): median T ≈ **1.2 years**, against ≈ **10.9 years** for firms still
trading. At a threshold of T < 1 year, ~45% of failing-company observations sat below it versus
~7% of surviving-company observations (≈ 7× separation). This is a *triage* instrument, not a
verdict: a majority of observations below the threshold did **not** fail.

**The fabrication indicators on a documented case:** a company later found to have unverifiable
contracts reported profit while converting roughly 0.2–0.4 of cash per unit of profit, with
cash-to-borrowings falling every year (roughly 0.45 → 0.39 → 0.13 → 0.02 → 0.01) before
restatement. The barrier metric went to *unbounded* at the exact point the audit challenge
landed.

**Where the model missed:** two of the validated failures were shock deaths, not erosions —
leverage *improving* right up to the event. Both were reported as misses in the write-up rather
than dropped.

## Known limits — state these in any write-up

- **Measures erosion, not shock.** A balanced firm hit by an exogenous price collapse will not
  be flagged; its leverage may be *improving* as it approaches failure.
- **Book values, not market values.** Overstated assets widen the computed distance falsely.
- **Survivorship in a price-based panel.** Delisted names have no price history, so any
  price-only backtest is a survivors-only population. Correct it by going to the filings.
- **Reported figures only.** Liabilities can be concealed as readily as earnings.
- **A high score is not safety.** Distance can close for years while the cash signal stays
  healthy; erosion alone only matters once the cash stops arriving.
