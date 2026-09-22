---
name: multi-period-cashflow-analysis
description: "Use when cash flows span periods or parties."
version: 1.0.0
author: hermes
metadata:
  hermes:
    tags: [finance, cashflow, npv, time-value, forensic, dispute]
    related_skills: [financial-report-forensic, petronas-petros-shell-dispute]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Multi-Period Cash Flow Analysis

For any question of the form "how much did X lose", "what does Y earn", "what is this
worth", where the flows span more than one period or more than one party. These are the
errors that survive a correct-looking spreadsheet, so they run BEFORE the arithmetic, not
after it.

## Order of operations

1. **Name the seat.** Whose economics is the question asking about? Write it down.
2. **Lay out the flows with dates.** Not just amounts — every flow gets a date.
3. **Reconcile the rate.** Back out the implied rate from each independent source and compare.
4. **Identify the dominant variable** (input cost share, or the largest flow).
5. **Only then compute.** Separate scenarios; state assumptions on the face of the output.

## Rule 1 — Never sum nominal flows across time

Payments at different dates are not additive. A "total" spanning 25 months is a nominal
sum wearing the costume of a figure.

- Report as a **dated range**, or **discount it**. Never as a single bare number.
- Applies to every "total paid / total lost / total claimed / cumulative" over a multi-period
  dispute.
- Test to apply: *over what dates, and at what rate?* If you cannot answer both, you have a
  nominal sum, not a valuation.

**Rate selection IS the answer.** RM100 due in 9 years, valued today:

| Discount rate | Present value |
|---|---|
| 3% | RM76.6 |
| 5% | RM64.5 |
| 8% | RM50.0 |
| 12% | RM36.1 |
| 15% | RM28.4 |
| 20% | RM19.4 |

A 4x spread on the same cash flow. So when presenting any discounted figure, **name the rate
and say why** — and when reviewing someone else's NPV, the first question is *what rate did
you use*. A rate chosen to make a project clear a hurdle is a conclusion in disguise.

Do not use one rate for flows of different riskiness. A near-certain salary stream and a
one-off lump sum are not the same asset; discounting them at the same rate is not a
comparison, it is a conflation.

## Rule 2 — Lost revenue is not the cost of carrying a receivable

A supplier who delivers and is paid late has not lost the revenue. It has incurred the
**cost of funds on the delayed amount**.

```
carrying cost = amount × cost of funds × (average months held / 12)
```

Check whether the order or contract carries late-payment interest — if it does, compute both
the gross headline and the net position.

How big the gap gets: a claimed "RM80m per month for 14 months" (RM1.12bn headline) against
an RM1bn receivable held ~7 months at ~3.5% = **~RM20m carrying cost**. The headline overstated
the economic loss by ~56x. Same flows, same period — one is a cash-phasing number, the other
is a P&L number, and they answer different questions.

## Rule 3 — Reconcile the rate before you multiply by it

When two independent sources report different rates for the same flow, one of them is a
different metric or is simply wrong. Back both out and compare.

Worked shape: arrears reported as RM523m at month 12 imply RM43.6m/month; the same matter
reported as ~RM1bn at month 14 implies RM71.4m/month. Same flow, 64% apart. Possible causes:
revenue or margin rather than invoice value; gross vs net of something; interest included in
one figure; or a wrong number. **Until it reconciles, the base is unverified and every
downstream multiplication inherits the error.** Say so out loud rather than picking one.

## Rule 4 — Analyse from the seat the question names

Being asked "what does the counterparty earn?" and answering "what the other side loses" is
answering a different question. The rate, the elasticity that matters, and the conclusion all
change with the seat.

Before computing, write down: *which party's economics am I being asked about, and which line
items are theirs?* If you catch yourself computing the inverse, stop and invert the frame.
A question about the gainer is usually the more informative one — the loser's position is
often already known and is usually just the mirror.

## Rule 5 — For an input-dominated business, find the dominant input first

Back out the input cost share (input cost ÷ implied revenue) before sensitivity-testing
anything else. If one input exceeds ~50% of revenue, the elasticity of earnings to **that
input's price** is the entire story and every other variable is noise.

State the elasticity explicitly — *"1% on gas = 1.8% on EBITDA"* — so the leverage is visible.
Then the scenario table writes itself:

| Scenario | Input cost | EBITDA | Margin | vs base |
|---|---|---|---|---|
| Pay full (base) | 220 | 125 | 30% | 1.00x |
| Input 25% cheaper | 165 | 180 | 43% | 1.44x |
| Input 50% cheaper | 110 | 235 | 55% | 1.88x |
| Input free | 0 | 345 | 81% | 2.76x |

Reverse-engineering the P&L from public anchors (capacity, output volume, input throughput,
reported EBITDA) is legitimate **provided every inferred line item is labelled inferred**. The
result is a sensitivity structure, not a reported margin — say which one you are presenting.

## Rule 6 — Delay and price are different levers; never merge them

- **Delay** shifts cash timing. Accrual earnings are unchanged. The gain is at most the float.
- **Price reduction** moves earnings permanently and compounds.

Run them as separate scenarios with separate magnitudes. Merged, the small effect hides inside
the large one and the reader concludes the deferral was the motive when it was not. Quantify
the float explicitly (interest on the deferred amount × average holding period) so its
smallness is on the record.

Corollary: when a counterparty is forced to pay but **offers to lodge the money in an
interest-bearing account** pending resolution, that is a signal it does not want the float.
Read the behaviour, not the headline.

## Rule 7 — Compare exit price to cumulative historical capital

Estimate build + rebuild + life-extension spend, then compare to the implied 100% valuation
of the asset being sold. **Selling below cumulative capital is a finding** — the vendor is
exiting at a realised loss, which reframes the motive question entirely and is usually the
real reason an asset moves when nothing else explains the timing.

Also compare the exit against a comparable asset the same owner retains. If the retained
twin is larger and wholly owned, the seller does not need the asset in question to hold the
strategic or intellectual position — only the volume — and volume is purchasable elsewhere.
That is the cleanest available answer to "why sell at all".

## Reporting rules

- **Label every number by class**: court-recorded / party-claimed / analyst-or-press estimate.
  Party assertions in filings are untested; press estimates sourced to unnamed parties are
  indicative only. Say which class each figure belongs to on the same line as the figure.
- **State assumptions on the face of the output**, not in a footnote. Inferred line items are
  named as inferred.
- **A range is more honest than a midpoint.** Where sources give RM70–80, present the range and
  compute both ends rather than silently using 75.
- **Report the direction of your own error.** If an approximation understates the number the
  argument relies on, that is worth flagging — it is the error a hostile reader finds first.

## Pitfalls

- **Turning a date into a fact.** A filing that says "pay by 6 October" establishes a deadline,
  not the date payment occurred. Same class of error as inferring a step-up date from a formula:
  the date exists in a document that means something else by it.
- **Inferring a settled balance from "continues to pay".** Ongoing payment is not evidence of
  zero arrears. Say "no arrears reported", not "balance is zero".
- **Treating a headline as the finding.** An interim or appellate order on procedural grounds is
  not a ruling on the underlying question. Read the order's own reservation clause — if it
  operates "subject to the final disposal" of the substantive matter, the headline decided nothing.
- **Forgetting who holds the money while a dispute runs.** Whoever holds the funds during
  litigation collects the time value even if it ultimately loses, unless the order provides for
  interest on repayment. Check whether it does. This is usually material and usually unstated.

## Related

- `financial-report-forensic` — auditing a company's own published numbers (source class, custom
  ratios, non-cash recognition). This skill covers flows across time and parties; that one covers
  a single reporting period's presentation.
