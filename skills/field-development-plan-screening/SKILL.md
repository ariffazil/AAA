---
name: field-development-plan-screening
description: "Use when asked to run an FDP screen or go/no-go."
version: 1.0.0
tags: [fdp, upstream, economics, valuation, decision, subsurface, cost]
triggers:
  - "run an FDP"
  - "FDP level"
  - "go or no-go"
  - "economics ka tak"
  - "what does it take to make it go"
  - "should this field be developed"
  - "shadow chairman"
  - "board paper for a development"
  - "full field development economics"
floors: [F2, F7, F11, F13]
capability_tier: fed-long-context
ecology_state: WARM
---

# Field Development Plan Screening

Class of work: evaluate whether a specific field should be developed, from public-domain data only,
and deliver a study a decision-maker can act on. Distinct from `upstream-e-p-capital-intelligence`
(what a past programme cost) and `subsurface-dossier-from-public-domain` (subsurface figures).
This skill is *forward* development economics plus the decision paper.

A real operator FDP costs US$15–40M and takes 12–18 months. This skill produces the screen that
bounds the question in a day, and states exactly what the real FDP would have to answer. Never let
the output be read as the real thing — put that sentence in the deliverable.

## Procedure

### 1. Write a FACT_BASE before you research anything else
One shared, versioned file every section reads before working. It carries:

- interest, operator, working interest %, partner or none
- location, water depth, distance to shore, block
- reserves by fluid with the tracker and data year
- discovery date, appraisal well count, FID date and the schedule history
- development concept as publicly stated
- **a hard rule at the top**: do not re-research these; if a section's research contradicts one,
  say so loudly at the head of that section rather than silently diverging

This file is what stops N sections inventing N different fields. Give every line an evidence class.

### 2. Evidence classes on every number, no exceptions
`[M]` measured/sourced · `[D]` derived (show the arithmetic) · `[A]` assumed (name the benchmark
and the range) · `[U]` unknown (say so).

There is no public seismic, log, core or PVT for most fields on earth. The correct output for a
reservoir parameter is a **named analogue range**, never an invented value. A section that returns
a clean number with no analogue and no class has fabricated it.

### 3. Section set, in this order

| # | Section | Load-bearing output |
|---|---|---|
| S1 | Subsurface / static | P50 and P90 STOIIP → recoverable; trap geometry; compartmentalisation |
| S2 | Reservoir / production | ramp, plateau rate and duration, decline, field life, cumulative |
| S3 | Drilling and wells | cost per well, campaign duration, rig market, margin/MPD hazards |
| S4 | Facilities / host | host capacity vs design basis; conversion scope; alternatives |
| S5 | Subsea / SURF | architecture, tie-back distances, cost build-up, installation season |
| S6 | Cost and schedule | WBS capex with AACE class and range; first-oil P50 |
| S7 | Economics | NPV, IRR, UTC, breakevens, tornado — **on S6's final capex** |
| S8 | Risk and decision | quantified register, EMV, the five conditions, assurance programme |

**S6 before S7, always.** Economics run before the cost build is finished inherits a number that
was superseded before it was written. If they must run in parallel, mark S7 provisional and re-run
it against S6's number before you write the summary.

### 4. Fiscal basis — decide which question you are answering

This is the fork that changes the verdict more than any other single choice. Work it before
modelling; the decision table is in `references/fiscal-basis-and-benchmarks.md`.

Short form: a field held 100% by a national operator with no partner is **not** evaluated on
contractor PSC terms. "Government take" on a 100%-owned field is the owner paying itself, and
applying a contractor's fiscal burden is a category error that can turn a viable project into a
dead one or the reverse. State which basis you are using in the header of every economics table.

### 5. Two deliverables

**Technical pack** — all sections, evidence-classed, one PDF.

**Decision paper** — one page of decision, then evidence, then a section headed *what I could not
see*. Format:

1. Decision required (one sentence)
2. Verdict (the number, stated plainly, including when it is ugly)
3. The one variable that decides it, with its sensitivity table
4. What is known vs unknown, and the consequence of each gap
5. The five conditions, scored TRUE / FALSE / UNKNOWN
6. What it takes to make it go — spend and duration against capital at risk
7. The honest case for proceeding anyway, and its price
8. What I could not see, itemised
9. Recommendation with an owner, a date and a gate

### 6. The five-conditions test

For a "what does it take to make it go" question, name exactly five conditions, score each
**TRUE / FALSE / UNKNOWN** against public evidence, and for every UNKNOWN attach the work that
resolves it: scope, cost, duration, owner. Then put the total assurance spend beside the capital at
risk. The ratio is the argument — six months and a fraction of the capital to avoid the possibility
of committing all of it.

A score of zero TRUE with three UNKNOWN is a finding, not a failure of the study.

## Pitfalls

- **A capex estimate below the industry range is a warning, not a result.** If your bottom-up lands
  at US$10/boe when global deepwater runs US$15–25/boe, the estimate is too optimistic, not
  efficient. Say so and use the industry range in the central case. A favourable estimate that sits
  outside the published distribution is the most common way a screening study flatters a project.
- **Nameplate capacity is not a forecast.** Divide the annualised capacity by 365 and see whether
  the answer is a round daily rate; if it is, you are holding a design number, and expected
  production sits below it after uptime, efficiency and decline.
- **A used host bought cheap is a capacity question before it is a bargain.** Establish the vessel's
  original design throughput, storage and processing scope against the current design basis. A hull
  acquired for a small fraction of a newbuild is usually a hull that does not fit the job, and the
  conversion cost is the real number — look for it, and if it is not public, say that it is not.
- **Recoverable reserves are a P50, not a floor.** Derive the P90 and price the NPV on it. A field
  appraised by a handful of wells across a long, faulted structure carries a downside that a single
  booked number hides — and the operator's own technical paper usually names the mechanism.
- **Test the first-oil date against analogues, not against the press release.** Compare FID-to-first-oil
  months for comparable projects on clean newbuilds; if the plan beats all of them on a more difficult
  concept, it is not a schedule.
- **A reference toolkit is not a model of the thing you are valuing.** Corporate investor-relations
  "modelling toolkits" model a company's earnings, not a project's cash flow: no DCF, no IRR, no fiscal
  terms. Use their **disclosed sensitivities** to calibrate your own model — that is genuinely valuable
  — and never present their output as a project valuation.
- **Contract value bands are booking classifications, not cost estimates.** A contractor's
  "significant" or "substantial" award tier describes how it books revenue, not what the scope costs.
  Sanity-check against a bottom-up build and against the same scope's escalated earlier award.
- **State the strategic rationale separately from the commercial one.** A sovereign-owned development
  often proceeds for portfolio, capability or option-value reasons while being described publicly in
  oil-economics terms. Both can be true. Name which one is being bought, because they carry different
  hurdle rates and different failure modes — and recommend approval on the basis that actually applies.
- **"Verified" in the study does not mean "live".** A fix committed to a repository is not a fix in a
  running process; a model recomputed in a notebook is not a model in the pack. Track the two states
  separately and never report the stronger one.

## Deliverable hygiene

- Every table column that carries a number carries its class.
- Every total carries its AACE class or accuracy band, stated on the same line.
- Pull the quoted claims in the summary from the sections, not from memory — a number that appears in
  the executive summary and nowhere in the body is a fabrication with a citation-shaped hole.
- Convert the recommendation into an owner, a date and a gate. "HOLD" without a decision point is an
  opinion; "HOLD until <date>, decided by <role>, on <three deliverables>" is a decision.

## References

- `references/fiscal-basis-and-benchmarks.md` — the contractor-vs-sovereign fiscal fork, the
  effective-take calibration method, and deepwater cost benchmarks to sanity-check a build-up.
