---
name: field-development-plan-review
description: "Use when deciding if an oil & gas field should be built."
version: 1.0.0
tags: [oil-gas, fdp, economics, capital, npv, risk, decision]
triggers:
  - "FDP"
  - "field development plan"
  - "should we sanction this"
  - "go or no-go on this project"
  - "is this project economic"
  - "has this taken FID"
  - "what does it take to make this work"
  - "run the economics on this field"
  - "breakeven oil price for this project"
  - "value this development"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Field Development Plan Review

Class of work: a development is proposed, sanctioned, or rumoured and the principal wants a decision —
should this be built, and if the answer is "only under conditions", what exactly are those conditions.
This is prospective capital, distinct from teardowns of money already spent (that is upstream capital
intelligence / deal forensics).

Deliver a verdict with a number behind it. A negative NPV stated plainly is a legitimate and valuable
outcome; a hedge that avoids the decision is not.

## Procedure

1. **Write a basis of design before analysing anything.** One file: project identity (block, water
depth, operator, working interest, discovery year), resource base with every competing public estimate
listed side by side, design rates, facilities scope, fiscal terms, price deck, discount rates, and the
required output format. Every later package reads it and may not silently change a value — deviation
requires stating the deviation and the reason. Without this the packages each pick a different reserves
figure and the study cannot be summed.

2. **Resolve the resource into base and upside; never average.** Where the record carries an older
higher case and a newer lower case for the same field, the lower one is base and the higher one is
upside, and both run. Averaging two published estimates produces a number no source ever published.

3. **Run the consistency arithmetic before trusting any production profile.**
   - `oil reserves ÷ peak oil rate` = plateau-equivalent years
   - `gas volume ÷ gas design capacity` = decline-living years

   If those two differ materially, one flat plateau cannot be true for both fluids, so the reserves,
the rates, or the well count is wrong. Say which you are overruling and why. Then check the third:
`reserves ÷ well count` gives EUR per well, which must clear the deepwater well-cost threshold — a
profile that needs ten wells to drain a volume implying three is a facilities problem wearing a
reservoir costume.

4. **State the development chain position, never a boolean.** A project is not "approved". It sits at
FID, with equipment award, long-lead manufacture, well spud, installation and first oil each
separately unproven. **"FID with <named vessel>" is almost always wrong** — the vessel is a candidate
until an award is announced. Check a candidate facility's published processing capacity against the
project's stated throughput before pairing them in one sentence; a large gap means the vessel is
wrong, the throughput is wrong, or there is an unpriced upgrade in the scope.

5. **Read the contract band as a scope signal, not a price.** Same contractor, same delivery model,
half the contract ceiling versus the earlier award for the same scope = scope was cut to make the
project economic. That is the tell that a concept was rescued rather than optimised, and it should
discount how much of the sponsor's narrative you accept. A hull bought for a few percent of a
new-build, on a field marketed as flagship, is a marginal-field solution.

6. **Build the cost estimate bottom-up and benchmark every line.** Wells (days × day rate + casing +
completions + subsea tree + installation + contingency), subsea system and SURF, the floater
(acquire / upgrade / new-build / lease — four different NPV shapes), export route, project management
and owner's cost, contingency, escalation. Apply AACE Class 3 (−20%/+30%) at this stage. If the total
lands outside the plausible band for the water depth and throughput, justify it hard or you are wrong.

7. **Treat an undefined export route as the largest unpriced item until proved otherwise.** A gas
volume with no route is not a revenue line, it is a decision: pipeline to an existing hub, pipeline to
a domestic grid, FLNG, or re-injection and later blowdown. Cost each; a 120–150 km deepwater pipeline
is a decision of the same order as the floater.

8. **Run the economics twice when the contractor is a state-owned affiliate.** See
`references/malaysia-psc-fiscal-terms.md` for the Malaysian ladder and the worked case.

9. **Compute breakeven by bisection on the model, never by rule of thumb.** Report NPV at two or three
discount rates, project and equity IRR, payback from FID and from first oil, unit technical cost in
$/boe, and the flat price at which NPV = 0. Then the tornado: price, capex, production, schedule slip,
gas price, opex, reserves. Rank by NPV swing per unit of the variable.

10. **Quantify the risk, do not describe it.** Monte Carlo with reserves, recovery factor, well
productivity, capex, schedule slip, long-run price, opex. Report P10/P50/P90 NPV, probability of
NPV < 0, and probability of a company-killer. Say in one sentence which variable owns the variance.

11. **Price the hub optionality separately.** A sub-economic standalone can be justified as an anchor
for satellite tiebacks within the tieback radius, or as a capability buy for the operator. Value the
satellites as incremental NPV at a stated tariff. Keep the capability argument as a labelled strategic
line item that is never monetised into the headline to rescue a weak return.

## Orchestrating the study across parallel packages

The FDP is normally too broad for one pass. Decompose by discipline and run the packages in parallel,
with the basis of design as the binding contract:

| Package | Deliverable |
|---|---|
| Subsurface & G&G | play, trap, charge timing, GRV-based volumetrics reproducing the public P50/P10, connectivity risk |
| Reserves & production | year-by-year oil/gas/water profile plus CSV, decline model, well-count adequacy |
| Drilling & wells | well design, days, day rate, $/well, rig availability, batch plan |
| Facilities | concept alternatives scored, capacity gap reconciled, subsea scope, export route |
| Cost | WBS-level capex and opex, AACE Class 3, per-boe, ranked cost risk |
| Fiscal | PSC waterfall per year, PI convergence, sponsor take vs contractor take |
| Economics | cashflow model + CSV, NPV/IRR/payback/breakeven, tornado |
| Risk | Monte Carlo, risk register, decision gates, stress scenarios |
| Execution | schedule to first oil, contracting strategy, approvals, critical path |
| Red team | strongest case against, analogues, internal inconsistencies, conditions to reverse |

Rules that make the fan-out work:

- **Give every package the same consistency identities and require each return to state whether its
own numbers pass.** A package that has to satisfy a shared identity finds the fault in its own work;
a package handed only its slice ships it.
- **Make the red-team package explicitly not on the project team**, with a different output contract:
the strongest version of the opposing argument plus the conditions under which it would be wrong.
Nine aligned packages converge on whatever the basis of design already implies; without an adversarial
package the study returns a caveated endorsement.
- **Require a ranked uncertainties table and a falsifier per package.** "What would break this" is the
most reusable line in the return.
- **Require explicit unknown where the record is silent, paired with what would resolve it.** No
invented citations, no fabricated analogue projects. A package reporting "not public" is worth more
than one reporting confidence on recalled content.
- **Do not model a 25-year horizon at today's spot price.** Spot usually carries a premium of some
kind. Fix a low/base/high deck in the basis of design and stress around it.
- **Reconcile the packages against each other before you write the verdict.** Ten self-consistent
sections can still hold ten different capex totals; the coordinator owns the arithmetic, not the
children.

## Pitfalls

- **A project reaching FID decades after discovery is usually evidence the economics never worked**,
and that portfolio, political or capability motives carried it. Say so, and separate the motive from
the returns instead of letting one explain the other.
- **Public "reserves" for a sanctioned field are often a communications product.** Gas discovery in one
decade, oil confirmed in another, described as both "oil and non-associated gas", with an economic
limit the stated volumes cannot support — each inconsistency is a sign the public story was written for
an audience, not for a plan. List them explicitly.
- **An affiliate contracting route removes competitive tension.** Where the floater or the subsea
package goes to a subsidiary of the sponsor, price it against market alternatives (lease dayrate,
new-build, other yards) before accepting the in-house number, and state both.
- **Do not confuse an operating company's economics with the state's economics.** The group-consolidated
view can be positive while the contractor view is negative, and vice versa. The verdict must name which.
- **Schedule optimism is the most reliably missed variable.** A floater hull arriving months before a
"first oil next year" target, plus ten deepwater wells, plus long-lead subsea trees, is a red flag
worth a P50/P90 date rather than a plan. Give both dates.
- **Everything gets an epistemic tag** — observed, derived, interpreted, speculated, unknown. A naked
number in an economics paper is an unverifiable number.

## References

- `references/malaysia-psc-fiscal-terms.md` — Malaysian PSC cost-recovery and profit-share ladder, PITA
  relief thresholds, gas price marker, the contractor-vs-consolidated double run, and a worked deepwater
  anchor set.
