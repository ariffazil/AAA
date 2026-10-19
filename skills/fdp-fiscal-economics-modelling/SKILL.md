---
name: fdp-fiscal-economics-modelling
description: "Use when building a field-development economics model."
version: 1.0.0
tags: [economics, psc, monte-carlo, npv, irr, oil-gas, fdp, validation, reconciliation]
capability_tier: fed-long-context
ecology_state: WARM
triggers:
  - asked to produce or review an FDP economics or risk workstream
  - building a PSC / cost-recovery cash-flow model
  - asked for NPV, IRR, EMV, breakeven or Monte Carlo on a field development
  - several workstreams emit different headline numbers for one project
  - asked which parts of a plan are solid and which need work
---

# FDP Fiscal Economics Modelling

A field development plan's economics section is not a spreadsheet exercise. It is a set of
falsifiable claims about cash that a board will commit billions against. The failure mode is never
"an input was slightly off" — it is **a model that runs, prints a plausible number, and is
internally inconsistent in a way nothing in the output detects.** Every rule below exists because a
model produced a confident wrong answer.

## When this applies

- Producing or reviewing any workstream that emits NPV / IRR / EMV / breakeven for a development
- Building a PSC or cost-recovery cash-flow engine
- Running Monte Carlo over project variables
- Reconciling economics across workstreams written in parallel
- Answering "which parts are solid, which need refinement"

---

## Procedure

### 1. Fix the basis before writing code

- **Find the workstream that owns each input domain and adopt its numbers verbatim.** The first cost
  estimate you encounter is not authoritative — it is the one that landed first. A top-down six-line
  capex sketch and a bottom-up WBS roll-up for the same project can differ by 70%+, and the detailed
  one wins on evidence even when it is less convenient. Search the deliverables directory for the
  domain owner before committing a basis.
- **State every deviation from the basis of design with its reason**, in the model docstring and in
  the deliverable. A silent deviation is indistinguishable from an error.
- **Never average two conflicting estimates.** Basis documents commonly forbid it, and it is wrong
  anyway: an average of a top-down guess and a bottom-up build is a number with no method behind it.
  Price both, tabulate both, and name which one the verdict rests on.
- **Adopt the whole basis, not the convenient lines.** Taking a cost workstream's capex while keeping
  your own opex and abandonment produces a hybrid that belongs to neither and flatters or punishes the
  project for reasons nobody can trace. If you cite a source's capex, take its opex and abandonment too.

### 2. Build the cash-flow engine

PSC waterfall mechanics, cost-recovery ceilings, PITA treatment, leasing-inside-a-PSC and state
participation mechanics: `references/psc-fiscal-mechanics.md`.

The engine must emit a **full fiscal line array**, not just a net cash-flow vector: gross, royalty,
net revenue, opex, capex, abandonment, cost recovery, profit, contractor share, host share, PITA,
entitlement, NCF. You cannot validate what you cannot see, and every "why is this number odd"
question is answered by one of those lines.

### 3. Run the validation pack before believing any number

`references/model-validation-pack.md`. This is not optional and not a final step — it is what
turns a script that runs into a model you may quote. Every headline error found in this class was
caught by one of those assertions.

### 4. Monte Carlo

- **Sample inputs, not outputs**, and record the seed in the artifact.
- **Run both independent and correlated sampling.** Correlated (a latent adversity factor coupling
  cost, schedule and subsurface) is the realistic case; independent is the conventional presentation.
  Report both and state which the verdict rests on. The gap between them is itself the finding — a
  correlated run fattens the extreme tail several-fold while barely moving the median.
- **Report P10/P50/P90 plus the probability of loss**, not the mean. A left-skewed distribution has
  its mean below its median, so the arithmetic expectation is a worse guide to the outcome than the
  median. Say so when it is true.
- **Percentiles must be defined before they are quoted.** For reserves, P10 is conventionally the
  *high* case; for cost, P10 is conventionally the *low* case. Two parties can each quote a correct
  P10 and disagree. Print the distribution's shape next to any percentile you cite.

### 5. Reconcile across workstreams

- **To separate "we disagree on inputs" from "we disagree on machinery", feed both engines the same
  input vector.** If two models diverge on identical inputs, the gap is in the engine, not the
  assumptions — and that is a two-hour fix that resolves a four-hundred-million question.
- **Tabulate the conflicting headline numbers side by side and name the dominant fork.** Do not
  smooth them. A pack that contains 30,000 and 37,800 bopd for the same field is not "approximately
  right" — every NPV downstream of it is provisional.
- **Prefer the finding that dissolves a problem over the one that prices it.** A vessel specification
  that makes a "2.4x capacity gap" evaporate is worth more than a careful costing of the upgrade.
- **Re-run the basis after a structural discovery.** A red-team or risk section written before a
  specification was settled is stale, not authoritative — say that rather than citing it.

### 6. Grade confidence by claim type, not by section

When asked what is solid and what needs work, organise by **warrant**, not by document structure:

1. **Almost certain** — public record facts, arithmetic identities, formula structure, and directional
   conclusions that survived every model built. Say plainly that this is a small share of the pack.
2. **Contradictions between sections** — the highest-value finding. Lead with these; they are not
   gaps, they are live disagreements the pack has not noticed.
3. **Needs iteration** — ranked by value per unit of effort, with the number attached to each.
4. **Genuinely unknown** — closable only by money, drilling, or law. No amount of modelling moves
   these; say so and name what would close each.

---

## Always-on traps

These produced wrong headline numbers. Each is a mechanism, not a preference.

- **The economic limit must zero the fixed operating cost, not only the production.** Truncating
  output while leaving facility-lease-style fixed opex running charges decades of negative cash flow
  after the field is dead, collapses NPV, and inflates government take to an absurd figure because the
  apparent cost base dwarfs revenue. Terminate the cost line with the production line.
- **IRR is the highest real root, and `nan` means fail.** Cash flows with capex continuing past first
  oil plus a terminal abandonment outflow are non-monotone in the discount rate, so several roots
  exist. A solver that returns the lowest root reports a negative IRR beside a positive NPV. Scan
  downward from a high rate and take the first sign change; treat an unbracketed result as failing the
  hurdle rather than silently excluding it from the probability.
- **Government take is not `(gross - net_cash_flow) / gross`.** That formula counts the contractor's
  own recovered costs as government revenue and can report 90%+ for a 30% fiscal regime. Build it
  from the fiscal lines: royalty + PITA + host profit share.
- **PITA is charged on entitlement (cost recovery + profit share), not on the profit share alone.**
  Taxing only the profit share leaves the early, cash-heavy cost-recovery years untaxed and overstates
  IRR by several points. Apply a capital allowance against the entitlement base.
- **Never finite-difference a marginal sensitivity on a re-normalised profile.** If the production
  profile is solved to deliver a fixed recovery, perturbing price shifts the economic limit, which
  re-normalises the profile, which can cancel the perturbation and return a sensitivity of exactly
  zero. Compute marginal retention analytically — `(1 - cash_payment) x profit_share x (1 - tax)` —
  and state the fraction for a mid-life year.
- **Unit economics need a mid-life year, not a capex-heavy one.** Unit earnings struck in a year still
  carrying capital spend and unabsorbed allowances can come out negative for a profitable project.
  Pick a year after capex completes and after allowances are exhausted, and label the metric a cash
  proxy when it is not reported earnings.
- **Check every MMscfd-to-volume factor.** The difference between `/1e6` and `/1000` is a factor of a
  thousand — it will spread a decade of gas across fourteen thousand years and still produce a
  plausible-looking total. Assert the annual total against a hand calculation.
- **A lognormal fitted from two percentiles needs `p_low < p50`.** Passing them inverted yields a
  negative sigma and a hard failure at draw time — or, worse, silently inverts the distribution.
- **IRR is invariant to a uniform time translation; NPV is not.** Slipping every cash flow by the same
  interval moves every term including abandonment, so the root is unchanged while NPV falls. This is
  arithmetic, not a bug — do not "fix" it, and explain it in the deliverable before a reviewer finds
  it and assumes an error.
- **`None` is a legitimate breakeven result.** NPV saturates as a cost input falls, so a bisection for
  "the capex at which NPV is zero" can have no root. Check for a sign change and return `None`; a
  solver that silently returns its bound manufactures a threshold that does not exist.

---

## Deliverable shape

- **Verdict first**, in one paragraph, with the number that matters — and if the pack has a
  contradiction, that contradiction *is* the verdict.
- **Numbers table** with parameter, value, basis/method, and an epistemic tag on every row. No naked
  figures.
- **Declare which entity view every NPV belongs to.** A 100%-working-interest asset NPV, a
  contractor-after-fiscal NPV, a group NPV and a total-national-rent NPV can differ by a factor of
  four. A single unlabelled figure is a defect, not a simplification.
- **Ranked uncertainties**, each with what would resolve it and whether that is modelling, money or law.
- **Levers in order of leverage**, with the NPV or capital attached to each.
- **Falsifiers** — the specific observations that would break the conclusion.
- **What you did not model**, stated plainly. Optionality, phasing, price correlation and fiscal
  stability risk each move the answer; naming them is what makes the rest trustworthy.
- **A summary must carry its five headline numbers**, not a narrative of how you got them.

---

## Pitfalls

- **Do not quote one NPV without saying whose cash flow it is.** The most common reviewer objection to
  this class of document is not a wrong input — it is an undeclared entity view.
- **Do not let a section's number survive that a sibling section contradicts.** Cross-reading the pack
  for conflicting plateaus, well counts, economic limits and cost totals is part of the job, and the
  conflicts are invisible from inside any single section.
- **Do not present a farm-out at cost as value-accretive.** Pro-rata dilution leaves IRR and NPV per
  unit of capital unchanged and reduces absolute NPV. It is justified by capital rationing, risk
  transfer or capability — say which, and say that the NPV falls.
- **Do not present a state participation percentage without its mechanic.** Paid, recoverable-carry and
  free-carry are the same headline number and differ by an order of magnitude in cost to the operator.
- **Do not let a smoothing assumption carry a structural problem.** Holding recovery constant as a
  plateau varies silently renormalises the profile and makes almost any plateau look adequate; apply an
  explicit recovery penalty when the physical mechanism says one is due.
- **Tag judgement probabilities as judgement.** Risk-register likelihoods are usually interpretation,
  while the impacts are model-derived. The impacts are more defensible than the probabilities attached
  to them, and conflating the two overstates the rigour of the register.

---

## References

- `references/psc-fiscal-mechanics.md` — the PSC waterfall, cost-recovery ceiling, PI slider, PITA
  base and allowances, why government take is regressive with cost, leasing versus owning inside a
  PSC, and the three state-participation mechanics with their relative cost.
- `references/model-validation-pack.md` — the assertions to run before quoting any number: NPV at IRR,
  monotonicity, breakeven round-trip, line-by-line waterfall instrumentation, and the hand-calc anchors.
