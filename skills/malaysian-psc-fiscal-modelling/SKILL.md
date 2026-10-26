---
name: malaysian-psc-fiscal-modelling
description: "Use when modelling Malaysian PSC oil & gas fiscal terms."
version: 1.0.0
tags: [oil-gas, fiscal, psc, petronas, npv, economics]
triggers:
  - "PSC terms"
  - "cost recovery ceiling"
  - "profit split Malaysia"
  - "PITA 38%"
  - "marginal field tax"
  - "EPT PSC"
  - "MRP gas price"
  - "contractor take vs government take"
  - "model the fiscal on this field"
capability_tier: fed-agent-subagent
ecology_state: WARM
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Malaysian PSC Fiscal Modelling

Class of work: an upstream development, acquisition or divestment in Malaysia needs a fiscal model —
cost recovery, profit split, petroleum income tax, gas pricing, or the split between what the
contractor keeps and what the state keeps. Self-contained reference; no external files needed.

Where the executed PSC text is confidential, model on the published reference terms and label the
output as such. Never present a modelled term as the contract term.

## When to use

- Building or auditing a cashflow model for a Malaysian PSC asset.
- Answering "what does the government take" or "what is the contractor's net".
- Assessing whether a marginal development can be made economic by fiscal levers.
- Sanity-checking a third party's fiscal model or a press claim about take.

## The ladder

| Step | Term | Value |
|---|---|---|
| 1 | Cash payment to Federal + State | 10% of gross production |
| 2 | Cost recovery ceiling | fixed 70% of gross production under EPT; historically 50% under the 1976-era PSC, raised to 70% in later contracts |
| 3 | Cost pool | EPT: single oil+gas pool. Legacy R/C PSC: separate oil and gas accounts |
| 4 | Profit split | contractor share tied to Profitability Index (PI) — see below |
| 5 | PITA 1967 | 38% of petroleum-operations income |
| 6 | Marginal-field relief | effective 25% if oil ≤30 MMstb **or** gas ≤500 bcf, as determined by the Minister of Finance |

Administration sits with PETRONAS via Malaysia Petroleum Management (MPM) as host authority; the
contractor bears exploration, development and production cost and risk. Contractors are not lessees —
there is no concession system.

## Profit-share interpolation

The EPT profit-sharing mechanism is a self-adjusting function of PI:

```
PI ≤ 1.5        → contractor share 90%
1.5 < PI < 2.5  → Contractor Profit Share = 1.8 − 0.6 × PI
PI ≥ 2.5        → contractor share 30%
```

```
PI = cumulative contractor entitlement (cost recovery + profit share)
     ÷ cumulative recoverable cost from inception
```

The definition is circular: the split depends on PI, which depends on the split. **Converge it
iteratively and show the iteration in the model.** Picking a first-year share and freezing it for
project life is the single most common error in a hand-built Malaysian fiscal model, and it biases the
answer toward whichever regime the first year happens to resemble.

Under EPT the Supplementary Payment and Threshold Volume provisions **do not apply** — if a model
carries either line, it is running legacy terms while claiming EPT.

Legacy revenue-over-cost (R/C) PSC: the recovery ceiling moves with an R/C index — a higher ceiling
when contractor profitability is low, lower as it improves. Model whichever term set governs and run
the other as the sensitivity; state which you assume governs and why (PSC vintage, amendments,
field-size designations).

## Cost recoverability

Recoverable cost is defined by a **negative list** — anything not listed and relating to petroleum
operations is recoverable. Common non-recoverable categories: governance and common issues, items
pending PETRONAS approval, and certain operational/business risks. Cost-recovery policy also caps
items such as expatriate headcount and benefits.

Abandonment: contractors submit an annual abandonment work programme and budget, and pay an annual
abandonment cess in cash to PETRONAS, drawn down when abandonment is executed. Model the cess as a
cash outflow during production, not as a lump at end of life.

## Gas pricing

Gas prices off the **Malaysia Reference Price (MRP)** — the weighted average FOB price of LNG exported
from Malaysia, computed as total LNG export value ÷ total LNG export volume, published monthly by DOSM.
Market conversion: 52 MMBtu per tonne of LNG.

MRP is a marker, not a guarantee. Domestic and state-level sales can sit below it by negotiation, so
model a discount band rather than assuming MRP, and show revenue at three gas prices.

## The double run — contractor view vs consolidated view

When the PSC contractor is a wholly-owned subsidiary of the host authority (a national oil company
operating its own block), cost recovery and profit split are **largely transfers from the group to
itself**. Only two lines leak out of the group:

- the government/state cash payment on gross production
- petroleum income tax

Consequences:

1. Build one model with a view switch. Do not maintain two models that will drift.
2. The sanctioned FDP economics paper is normally written in the contractor view — that is the decision
   document's convention.
3. The go/no-go recommendation usually belongs to the consolidated view, because that is where the
   money actually is.
4. Compute breakeven for both. The gap between them is the price of being inside the state.
5. Name the view inside the verdict, not in a footnote. A verdict that does not say which view it used
   is not actionable.

## Levers that move a marginal development

Rank by value to project NPV and name the approving body for each:

| Lever | Effect | Approver |
|---|---|---|
| Investment tax allowance / accelerated capital allowance | defers or reduces PITA | Ministry of Finance / IRB |
| Marginal-field designation | 38% → 25% PITA | Minister of Finance |
| Gas price guarantee or floor | removes MRP downside from the revenue line | PETRONAS / Government |
| State participation arrangement | shifts take; jurisdictional precedent matters | State government + Federal |
| Cost-recovery timing (front-loading) | pulls cash forward, improves IRR more than NPV | PSC terms / MPM |

A reserve-threshold manoeuvre to reach marginal-field status is a legitimate **sensitivity** and a bad
recommendation. Present it as "what the fiscal break would be worth", with the threshold named, and
leave the policy call to the principal.

## Fiscal term variants in the current regime

Beyond the standard R/C PSC, MPM offers tailored terms for specific asset classes introduced from 2021
onward: Small Field Assets (SFA), Late Life Assets, and the shallow-water Enhanced Profitability Terms.
The EPT features a single oil+gas cost bank, a fixed 70% cost recovery ceiling, and a responsive
profit-sharing mechanism that removes the Supplementary Payment and Threshold Volume provisions. If a
field's reserve size or life stage might qualify for a variant, model it as a scenario — do not assume
eligibility without naming the threshold.

## Modelling checklist

- [ ] Term set identified and the assumption stated (executed PSC is confidential)
- [ ] PI converged iteratively, iteration shown
- [ ] Cash payment applied to gross production, not to profit
- [ ] Cost recovery capped per year, not cumulatively uncapped
- [ ] Single vs separate oil/gas pools consistent with the term set claimed
- [ ] PITA at the correct rate, with marginal-field eligibility tested against both thresholds
- [ ] Abandonment cess as a production-phase cash outflow
- [ ] Both views run, both breakevens computed
- [ ] Every number tagged observed / derived / interpreted / unknown

## Pitfalls

- **Freezing the profit share.** The circular PI definition is the mechanism, not a rounding detail.
- **Confusing royalty with the cash payment.** The EPT instrument is a 10% cash payment on gross; a
  model that adds a separate royalty on top double-counts the state's take.
- **Applying the 38% PITA rate without testing marginal-field eligibility.** Both the oil threshold and
  the gas threshold must be tested — a field can fail one and pass the other.
- **Treating MRP as a fixed domestic gas price.** It is an export-linked marker; sales can be discounted.
- **Adding Supplementary Payment or Threshold Volume to an EPT model.** They were removed by design.
- **Modelling the contractor view and calling it the project view.** For a state-owned contractor the
  two answers can differ in sign, and the principal will act on the wrong one.
