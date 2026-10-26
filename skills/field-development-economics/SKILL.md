---
name: field-development-economics
id: field-development-economics
version: 1.0.0
description: "Upstream FDP screen: capex, NPV, IRR, go/no-go gate."
triggers:
  - "FDP"
  - "field development plan"
  - "is this field economic"
  - "economics ka tak"
  - "go or no-go"
  - "NPV this field"
  - "capex per boe"
  - "breakeven oil price"
  - "unit technical cost"
  - "should PETRONAS develop this"
  - "screen this discovery"
risk_tier: medium
autonomy_tier: T2
owner: F13 SOVEREIGN (Arif) — forged by AAA
---

# Field Development Economics — FDP-level screening

Governs any request that asks for a **development** decision on an upstream asset: capex, opex,
fiscal terms, NPV/IRR, breakeven, and a go/no-go. Distinct from *prospect* evaluation
(`geox-prospect-evaluation`, which is pre-drill drill-or-drop) and from *basin* work
(`geox-basin-evaluation`). Here the well is already planned or drilled and the question is capital.

**Core posture:** public data can *bound* a development decision; it almost never *validate* one.
Deliver a decision structure with explicit unknowns, not a confident number.

## PROCEDURE — in this order

### 0. Build the FACT_BASE before anything else

Write one shared file (`FACT_BASE.md`) and make every downstream agent read it first. It must carry:
project identity, volumes, design capacity, full schedule history, reservoir character, facilities,
commercial context — **each number tagged with an evidence class**:

| Tag | Meaning |
|---|---|
| `[M]` MEASURED | reported by a named source, cited with date |
| `[D]` DERIVED | computed by you from `[M]` inputs — show the arithmetic |
| `[A]` ASSUMED | industry benchmark or judgement — name the benchmark and its range |
| `[U]` UNKNOWN | not knowable from public domain — say so, never invent |

Add hard rules to the base: no fabricated well data, every cost carries a unit-rate basis, AACE
Class 4/5 accuracy declared on every total, and *"if you find a fact that contradicts this base,
say so loudly at the top of your output."* Agents do surface contradictions when invited — the
capacity/schedule conflict that decided the last case came from an agent told to flag it.

### 1. Fiscal basis — WHO IS THE INVESTOR (run this first, always)

The single highest-leverage question and the one most easily got wrong: **is the question being
asked on a contractor basis or a sovereign-operator consolidated basis?**

- A field held **100% by the national operator** pays tax to itself. "Government take" partially
  cancels. Contractor terms applied here is a category error that understates NPV by an order.
- A field with a **foreign PSC partner** is genuinely subject to take. The same field can be
  value-destructive to a partner and strongly positive to the host.

Run the model both ways and report both. The gap between them is itself the finding: if the
contractor basis needs an implausible oil price to clear hurdle, **that explains why the field sat
undeveloped for decades** better than any geological story.

### 2. Test the published capacity against the reserves

Government and tracker databases routinely publish **annualised nameplate** where readers assume a
daily rate. Test it arithmetically: annual figure ÷ 365 vs the stated daily unit. If the two agree
to three figures with a suspiciously round daily number, you have found nameplate, not forecast.

Then ask: **can that rate drain the booked reserves within a plausible field life?** A design
capacity that implies 100% uptime with zero decline for 10+ years is a nameplate, and the forecast
must sit below it.

### 3. Solve the host facility before the reservoir

On marginal developments the host usually dominates the answer. Model the host explicitly and
alternatives side by side (used-hull conversion / converted tanker / newbuild / subsea tie-back to
an existing hub). Expect the host choice to swing NPV by more than the oil price does.

**Check nameplate capacity against the required throughput.** A used vessel bought cheap is usually
cheap because it is undersized or lacks a process module. If host capacity is below the field
design rate, that caps the entire production profile and every downstream number — and the
acquisition price is not a bargain, it is the price of a hull that does not fit.

### 4. Capex: bottom-up AND benchmarked — a number below the range is a red flag

Build from unit rates (rig day-rate × days, per-km flowline, per-well tree) and then compare to
`capex per boe` for the analogue class. Global deepwater sits roughly **US$15–25/boe**. An estimate
that lands *below* that band is more likely to be missing scope than to be efficient — that is the
signal to go find the missing WBS element, not to celebrate.

Also: **a contractor's disclosed award value is a booking classification, not a cost estimate.**
Integrator awards are announced in bands ("significant", "$75–250M") that may cover only one scope
element or one phase. Escalate the older award to present-day money and see whether it converges
with your bottom-up build; convergence validates the build, divergence means you are comparing
different scopes.

### 5. State the production profile explicitly — never inherit the forecast

Every economics run writes its own ramp, plateau, plateau duration, decline and economic limit, in
its own words. Two sections silently sharing one profile is how a wrong rate propagates into a
confident NPV. Include an uptime assumption with a basis.

### 6. Run your own model in parallel; do not wait for the agents

While section agents work, build an independent cash-flow model yourself in plain Python (stdlib
only — no numpy dependency). This is the cross-check, and it is what lets you catch an agent's
basis error. At minimum compute: NPV10, IRR (bisection on the discount rate — no library needed),
payback, UTC per boe, and breakeven price by bisection over Brent.

### 7. Re-run every scenario through the technical findings — expect your first answer to be wrong

When the sections land, re-run the model with their numbers, not yours. Do it as a **scenario
table**, one row per coherent combination (central case, host-limited case, host-upgraded case,
high/low capex). Preserve your original answer as a row marked *retracted* so the correction is
visible rather than silently overwritten.

### 8. Close with a gated decision, not a verdict

Deliver **five conditions that must all be true**, each marked `MET` / `FAILS` / `UNKNOWN`, and for
every unknown the work required to resolve it with **cost and duration**. Then say plainly which
side of the line the project sits on: does it fail the hurdle, or does it merely fail *validation
from outside*? Those are different conclusions and conflating them is the main dishonesty available
in this task class.

## IRON RULES

1. **Declare the fiscal basis in the first table, not a footnote.** Every NPV is meaningless without
   knowing whose cash flow it is.
2. **A sanction is not a validation.** A project can be correctly sanctioned on information the
   public cannot see. The honest output is a bound plus the list of what would resolve it.
3. **Retract explicitly and in place.** When a later section overturns an earlier conclusion, rewrite
   the memo and mark the superseded figure as retracted. Never let v1 survive next to v2 — two live
   answers is worse than one wrong answer.
4. **Every number carries a class tag.** `[U]` is a legitimate output. An invented number is not.
5. **Never present a variance you did not compute.** If you did not run the sensitivity, do not
   describe it — run it, or say the range is a literature range.
6. **AACE class on every total.** Class 4/5 is honest for a public-data screen; presenting it as
   Class 2 is the fabrication.
7. **Check the milestone date before calling something news.** A contractor award is not the
   sanction. Confirm the FID date directly; a corpus that records the award as the event and misses
   the FID will invert the entire timeline.
8. **Split the gas question from the oil question.** Gas is often 30–40% of the boe and a thin
   fraction of the revenue; an unsigned gas agreement is a quantified hole, not a detail.

## PARALLEL FAN-OUT SHAPE

One agent per FDP section, all writing to `sections/S<n>-<topic>.md`, each reading `FACT_BASE.md`
first and returning a short summary rather than its full body. The eight that worked:

| # | Section | The question it must answer |
|---|---|---|
| S1 | Subsurface & static model | GRV → STOIIP → recoverable, with the arithmetic trail and P10/P50/P90 |
| S2 | Reservoir & production forecast | plateau, decline, field life, deliverability per well |
| S3 | Drilling & wells | well cost build-up, campaign duration, rig market reality |
| S4 | Facilities & host | host spec vs requirement, alternatives, conversion scope |
| S5 | Subsea & installation | layout, tie-back distance, SURF cost build-up |
| S6 | Cost & schedule | WBS capex with AACE range, first-oil date, benchmarking |
| S7 | Economics & fiscal | cash flow, NPV/IRR, breakeven, tornado |
| S8 | Risk & decision | quantified register, EMV, the five conditions |

Require a fixed output schema per section (headline ≤3 sentences, a NUMBERS table, falsifiable
judgements, what would change my mind, confidence, sources). Without a schema the sections arrive as
prose and cannot be merged.

## DELIVERABLE

One PDF, memo first. Order: CEO memo (verdict, corrections, scenario table, five conditions,
recommendations) → S1…S8 → an appendix carrying any external model used for calibration. Every
number tagged, every assumption visible, and a closing section stating exactly what an FDP-grade
study would need that this screen cannot supply.

Build: markdown sections → `pandoc` to HTML → headless browser to PDF. Use
`google-chrome --headless=new --no-pdf-header-footer --print-to-pdf` — and verify the output page
count and first page with a PDF reader before delivering.

## PITFALLS

- **Applying contractor fiscal terms to a wholly-owned national asset.** It understates NPV by an
  order of magnitude and produces exactly the wrong recommendation. Ask who the investor is before
  touching a spreadsheet.
- **Trusting a company's own headline metric over its own endpoint.** Corporate disclosures and
  status blocks go stale between releases; a headline claiming a perfect score while the live
  measurement reports partial is the most damaging thing an outside reviewer can find. Generate such
  blocks from the live source with a timestamp, and expire them.
- **Reading a contractor's award band as the project cost.** See rule in §4.
- **Letting a subagent's optimism become the central case.** Take the central case from the section
  that actually built the cost, not from the one that assumed the throughput.
- **Quoting a reserve number without its as-at year and source vintage.** Reserves are a dated claim.
- **Running a screen at spot price.** Screen at a defensible long-run reference deck (a major's
  published constant-price basis is a good one) and show the spot case separately. A project that
  only works at today's price is a price bet, and should be labelled one.

## REFERENCES

- `references/xom-modeling-toolkit.md` — how to use a major's published investor toolkit as a
  calibration benchmark (effective-take derivation, reference price deck, what it cannot do).
