---
name: market-claim-assessment
description: "Use when grading a P&L, trade record, or leverage claim."
version: 1.0.0
author: Hermes Agent
tags: [trading, pnl, leverage, grading, risk, chart, forensic, wealth]
organ: WEALTH (:18082)
triggers:
  - "grade the trading"
  - "bape % ni"
  - "bape percent"
  - "trade record"
  - "P&L screenshot"
  - "margin level"
  - "leverage"
  - "bankrupt company chart"
  - "chart company yang dah bankrap"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Market Claim Assessment

For when a market artifact arrives and someone asks you to **read it, grade it, or
validate it** — a broker screenshot, a trade record, a chart of a company that later
died, or a stated position size. Companion to `agentic-trading-companion` (risk rules,
MT5 bridge) and `trading-signal-chart` (signal charts); both are user-owned, so this
skill carries the assessment discipline rather than extending them.

**One rule over everything:** recompute before you interpret. An artifact that does
not reconcile with itself cannot be graded at any level.

---

## 1. Recompute the book first

Identity checks, in order. If any fails, say so and stop.

| Check | Identity |
|---|---|
| equity | `balance + floating P&L` (± rounding) |
| margin level | `equity ÷ margin × 100` |
| free margin | `equity − margin` |
| position P&L | `(entry − now) × lots × 100 oz × USD/MYR`, sign flipped for long |

`scripts/pnl_screenshot_probe.py` does all of it — fill the INPUTS block from the
image and run it. Deriving the implied FX rate from the positions is also the cleanest
cross-check: if the implied rate disagrees with the stated one, the screenshot is not
internally consistent.

---

## 2. Name the denominator — every time

The same result is four different, equally true percentages:

| Denominator | What it actually means |
|---|---|
| balance | return on capital |
| equity | share of the account still **unrealised** |
| margin | return on posted collateral |
| notional (lots × 100 × price) | the market's own move, amplified |

Quote all four, or name the one used. A headline percentage with no denominator is how
a trading result gets inflated without anyone lying. When the user asks *"bape % ni"*,
the honest answer is the set, not the biggest one.

---

## 3. Split floating from realised before anything else

`equity − balance` is unrealised P&L. A small balance with a huge equity is an **open
position, not a result** — nothing is banked and it can be zero before the next
screenshot. Say this first; it changes the meaning of every other number.

A large balance with small floating is a trader with a history. The reverse is a
trader with a position.

---

## 4. Compute the distance to zero, not just the profit

```
move_to_call = (equity − margin × 1.00) ÷ USD_per_account ÷ total_oz
move_to_stop = (equity − margin × 0.50) ÷ USD_per_account ÷ total_oz
```

Report in units of the underlying **and** as a percentage of price. Under ~1% is a
position one loud tick from gone, however far up it is.

---

## 5. Separate leverage from skill

```
multiplier = account_move_% ÷ market_move_%
exposure   = lots × 100 × price          (state as a multiple of equity)
```

A several-hundred-percent account move off a sub-1% market move is **exposure, not
reading**. The same multiplier runs in both directions, so the edge was never the
input that produced the outcome. Say this plainly — it is the single most useful thing
you can tell someone holding a large winner.

---

## 6. Grade on four axes, never one letter

| Axis | Question |
|---|---|
| Direction | with the trend, or against it? |
| Sizing | exposure vs equity — 1×? 10×? 800×? |
| Discipline | stop? target? scale-out? |
| Sample | independent **decisions**, not positions |

A record can be right on direction and reckless on sizing — say both. One letter
hides the axis that failed, and the failed axis is the only actionable part. Two
positions in the same direction at two prices is **one decision executed twice**.

---

## 7. Refuse to grade the human from one outcome

N=1 gives a likelihood ratio of 1 between skill and luck — zero bits. *"Not yet
proven"* is the correct verdict, and it is different from both praise and insult;
praising before the test and condemning from one point are the same error with the
sign flipped.

Two corollaries to state when asked for comparisons:

- **Ensemble ≠ time average.** The average across many traders is not the trajectory
  of any one trader. With any non-zero chance of ruin per trade, sufficient repetition
  reaches zero even at positive expectancy. Never quote an aggregate return as if a
  single account can be expected to realise it.
- **Famous investors are defined by decades of survival, not by a return.** The axis
  is years; a one-month record cannot be placed on it at all.

---

## 8. Never prescribe "add more indicators"

When asked how to improve a trading system, do not answer with more layers, filters or
indicators. Adding filters does not add information — it reduces trade count and
disguises the absence of information as discipline. The three things that genuinely
raise quality all live outside the chart:

1. Knowing something the market has not priced.
2. Knowing where other participants' stops sit.
3. Risk process tight enough for a small edge to survive.

---

## 9. Domain rule — does the instrument have hidden books?

Ask this before applying chart-only analysis to anything.

| Instrument | Hidden state | What the chart actually is |
|---|---|---|
| Commodity (gold, oil, gas) | none — no earnings, no counterparty, no auditor | the object itself; technical-only analysis is **complete** there, not lazy |
| Listed company | balance sheet, auditor, insiders | belief — records what people paid, can be wrong for years |
| Unlisted state company | no ticker at all | **no chart exists**; closest series is capital out vs capital reinvested |

A commodity has no books, so there is nothing hidden for the chart to miss — telling a
commodity trader that technicals are "blind" is wrong. A company always has books, so
chart-only analysis of a company is incomplete at every timeframe no matter how clean
the chart. Never use one domain's answer in the other.

---

## References

- `references/collapsed-company-charts.md` — charting a failed/delisted company:
  reconstruction method, mandatory provenance disclosure, the pre-collapse signature,
  and the stacked-comparison recipe.
- `scripts/pnl_screenshot_probe.py` — recompute a broker screenshot; prints the book
  checks, the four denominators, distance-to-zero and the leverage split.
