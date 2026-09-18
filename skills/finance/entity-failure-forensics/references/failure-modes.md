# Failure modes and their detectors

Three ways an entity stops being able to continue. Each has a different detector.
Using one detector and reporting its verdict as "the" answer is the most common
analytical error in this class of work.

## The three modes

| Mode | What changes | Detector | Blind to |
|---|---|---|---|
| **Erosion** | `V` shrinks; the gap closes over years | `T = D / lambda` | shock, fabrication, transfer |
| **Fabrication** | `V` is misstated; profit never becomes cash | `OCF/PAT`, `cash/borrowings` | anything not cash-visible |
| **Transfer** | the claim itself moves; `V` is no longer the entity's | **none quantitative** | — |

**Erosion and fabrication each look healthy to the other's detector.** A name that
passes one and fails the other is not safe — it is untested on the other axis.

## Mode 1 — erosion

Detector: `T = D / (lambda - mu)`, with `lambda` estimated from the rate at which `D`
has been closing.

- An entity whose gap has closed for several consecutive periods is the cleanest
  case. Crossing zero is the point of no return on this axis, and it can precede the
  terminal event by **several years** — in the origin panel one retailer crossed four
  years before it failed, while its share price still traded normally. The accounts
  were the early signal, not the chart.
- **Shock deaths are outside this detector.** A balanced entity struck by a commodity
  or demand collapse shows a *widening* gap right up to failure and returns an
  effectively infinite `T`. Report these as misses, not as noise. They are the
  boundary of the model and stating the boundary is part of the finding.
- **Very slow erosion is also a miss** at short horizons: a gap closing steadily but
  slowly can return a long `T` while the direction is right and the magnitude wrong.
- A rights issue, refinancing, or asset sale can interrupt the closure and reset `T`
  upward. A single upward move in an otherwise monotone series is a capital event,
  not a recovery — check what was issued or sold before reading it as improvement.

## Mode 2 — fabrication

The one measurement that survives a falsified asset base.

```
cash conversion      = operating cash flow / reported net profit
cash coverage        = cash and equivalents / total borrowings
```

Readings:

| Reading | Interpretation |
|---|---|
| `OCF/PAT` >= ~1.0 | profit largely converts to cash — normal for a sound operator |
| `OCF/PAT` ~0.5 or below | a meaningful share of reported profit is non-cash |
| `OCF/PAT` ~0.2-0.4 with reported profit | strong fabrication signal — the profit is a claim, not a receipt |
| `cash/borrowings` falling every year with no jump | the entity is losing the ability to service its own debt while still reporting profit |

**The monotone decline is the signal, not any single level.** A coverage ratio that
falls every single period, with no restatement and no discontinuity, is more
convincing than any threshold breach, because it needs no interpretation.

**Why the distance model goes blind here.** If the misstated line item is the asset
base, then `ln(assets/liabilities)` *increases* as the misstatement grows. The
barrier appears further away exactly as the entity becomes more dangerous. A model
whose numerator is the thing being falsified cannot detect the falsification. This is
not a defect of the specific formula — it is a structural property of any ratio that
has the falsified quantity in the numerator.

Report the **divergence** between profit and cash as a first-class finding, with both
numbers, rather than a verdict. Profits that are accrual-only, or include impairment
and other non-cash charges, can produce a large gap *without* fraud — so state the gap
and the direction, and let the reader weigh it.

## Mode 3 — transfer

No default. No falsification. The arithmetic remains correct and stops being
meaningful, because it assumes the entity holds the claim being measured.

Symptoms, in the order they become visible:

1. **Duplicate claims on the same revenue** — two parties invoice for the same
   product or service. This is the clearest signal, and it can appear while every
   balance-sheet number is unchanged.
2. A dispute over which law, which regulator, or which jurisdiction governs.
3. A statutory instrument granting a role to a second party, with the incumbent's
   role "reaffirmed" in language that does not resolve the overlap.
4. Assets moved into structures in another jurisdiction — a defensive move, which
   also reduces what the entity itself holds. Both readings are true at once, and
   both should be reported.
5. Headcount or capital reduction described in survival language.

**A verdict in the entity's favour does not close the mode.** A litigated outcome that
went the entity's way still establishes that the claim was contestable. Report the
mechanism — who invoices, whose law governs, who signs — not just the result.

For this mode the deliverable is observational, not quantitative: name the parties,
the instrument, and the date. Resist forcing it into a ratio.

## Lambda is not exogenous

```
T = D / (lambda_market + lambda_governance + lambda_attention - mu)
```

### Governance term

Two observable facts, both from the company's own published board page:

- **Oversight concentration** — one seat chairing several oversight committees, or a
  non-independent member sitting on all of them. Meaningful concentration: one person
  holding audit oversight *and* risk oversight *and* input into executive
  remuneration and succession.
- **The appointment mechanism** — who appoints the chair. If the overseer is appointed
  by the beneficiary of the entity rather than by the entity, the overseer's incentives
  align with the appointer.

That second fact yields a **structural floor**: correction cannot be faster than
third-party intervention, so `lambda_governance >= 1/tau_external`. No individual needs
to act in bad faith for the floor to bind — it is architecture, not intent. Say that
explicitly, because it is what keeps the finding checkable and non-defamatory.

**Independence ratio alone is not the finding.** A board can be half independent by
headcount and still concentrate all oversight in one seat. Report the ratio, then
report the concentration, and do not treat the ratio as a verdict.

### Attention term

Every mode above is an attention failure with a different object:

| Mode | Object nobody is maintaining |
|---|---|
| Erosion | a slow decline — there is no discrete event to notice |
| Fabrication | cash conversion — attention sits on profit, which looks like news |
| Transfer | who holds the claim — the claim appears in no statement |
| Own-position ruin | position size — attention sits on direction |

Attention is the binding constraint because it is finite, cannot be bought back with
capital, and **can be captured** — a claimant can hold it, so it is not allocated to
the task. The third property is what makes it binding, and it links directly to the
governance floor above.

Grounding to cite: attention as a scarce resource under information abundance; cognitive
effort as a limited resource; the firm as an attention-allocation system; extractive
institutions as those that divert attention from the task to the claimant.

## Position size — the same ratio logic applied to a single actor

```
g(f) = p*ln(1 + f*b) + (1-p)*ln(1 - f)
```

The growth curve is **asymmetric**: slightly too small loses slightly, slightly too
large loses a lot. Beyond roughly 2x the optimum the growth rate goes negative *even
with a genuine edge*. This is why the population of ruined participants is far larger
than the population of merely slow ones — and why a size constraint is the highest-value
intervention available. State the curve, not a slogan.

## Fiscal barrier (state-owned entities)

For a state-owned entity the binding constraint is the transfer to the owner:

```
headroom = CFFO - dividend - capex
```

where `CFFO` and `capex` are what standing still requires. Report it by scenario
(e.g. across a commodity price range) and give the price at which it turns negative.

**The asymmetry that makes this different from a listed company:** a listed
shareholder who wants out **sells** — the loss transfers to a buyer and the capital
stays in the firm. A state owner who wants more **takes** — the capital leaves and the
investment capacity falls. One transfers a loss; the other transfers capital.

Two things to state alongside it:

- At the price where headroom approaches zero, the transfer may still be paid in full.
  The owner does not lose. What loses is the entity's ability to remain an entity,
  because maintenance capital is what gets cut first.
- **This barrier is a formulation, not a validated instrument.** Comparable audited
  accounts exist for very few state-owned entities and almost none disclose the fiscal
  term systematically, so no backtest of equivalent strength can be run. Label it,
  give the arithmetic, and give the falsification criterion (see
  `falsifiable-theory-shape.md`).
