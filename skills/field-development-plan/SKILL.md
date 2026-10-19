---
name: field-development-plan
description: "Use when building or reviewing a field development plan."
version: 1.0.0
risk_tier: medium
floor_scope: [F2, F9]
autonomy_tier: T1
tags: [fdp, economics, reconciliation, assurance, upstream, monte-carlo]
capability_tier: fed-long-context
ecology_state: WARM
metadata:
  hermes:
    tags: [fdp, economics, reconciliation, assurance, upstream, monte-carlo]
    related_skills: [auditable-numeric-artifacts, geox-prospect-evaluation]
---

# Field Development Plan — Integration and Number Governance

Applies to any multi-workstream techno-economic plan: field development plans, capital project
cases, feasibility studies assembled from parallel sections.

---

## The failure this exists to prevent

Nine or ten workstreams each produce a defensible section, and the finished plan contradicts itself
in a dozen places. Subsurface derives OOIP 398 MMbbl; production back-solves 347 and nobody notices,
because both land on the same recoverable volume. Cost builds US$4.0B; economics runs on US$2.65B
and still agrees with a third section that claims to use the US$4.0B basis. Two fiscal workstreams
concur within 5% while their capital bases differ by 51%.

Every section is individually right and the plan is collectively wrong. **The cause is never a
missing tool.** It is that each workstream ran on a private number set and nobody owned
reconciliation. Fixing it is governance, not modelling — and the governance is cheap.

---

## Mandatory sequence

Do not reorder. Each step is cheap and each prevents a contradiction class that costs days later.

### 1. Assumptions ledger before any section is written

One machine-readable file. Every value carries `value`, `basis`, `tag`, `status`, `classification`.

Disagreements are **represented, not resolved**:

```json
"ooip_mmbbl": {
  "value": null,
  "disputed": [
    {"ws": "subsurface", "value": 398,   "basis": "GRV x N/G x phi x So / Bo", "tag": "DER"},
    {"ws": "production", "value": 347.5, "basis": "back-solved from EUR at 40% RF", "tag": "DER"}
  ],
  "status": "UNRESOLVED",
  "resolution": "appraisal well + DST. Not public."
}
```

`value: null` plus `disputed[]` is the whole trick: no workstream can silently win, and a later
reader sees the fork. A ledger holding one number per row has already destroyed the evidence of the
disagreement — which was the valuable part.

Classify each row for data handling: values derived from public sources may leave the host; values
that could only come from operator-internal data (logs, DST, vendor cost) stay inside the operator's
systems and are marked so. Never ship internal data into a shared store to make a table tidy.

### 2. One engine, validated against every workstream's own claimed output

Pick one deterministic implementation. Run it on each workstream's *declared* inputs and compare to
that workstream's *claimed* result.

- Reproduces exactly → engine and section agree.
- Off 10–15% on identical inputs → two engines, or one input set is mislabelled.
- **Two workstreams agree within a few percent while their declared cost bases differ by 50%+ → at
  least one is not computing on the basis it claims.** This is the tell. Chase it before anything else.

Never average conflicting figures when the basis of design forbids it. Re-run the whole distribution
on each candidate basis and present both side by side; the divergence is the finding.

### 3. Cases against ranges, never points

Where the ledger is UNRESOLVED, run Low/Mid/High and state plainly that they are the envelope of the
disputed inputs, not a probability distribution. **A figure that appears only at one point value while
the ledger says the input is disputed is exactly the defect the ledger exists to catch.**

### 4. Reconcile, then propagate

A conflict marked resolved in a comparison table but left standing in a downstream case definition is
not resolved — the superseded value keeps voting. After every resolution, grep the artifact for the
old number and kill it everywhere, including case parameters and figure captions.

The highest-value instance: when one section refutes a value another section depends on, the dependent
section must be re-run. Refuting it in prose while leaving it in the model is worse than not noticing
it at all.

### 5. Independent audit before delivery

Write first, then have a *separate* pass attack the artifact against the model and the ledger. Do not
grade your own work in the authoring pass. Brief the auditor to report defects only — page and
section, no improvement suggestions — and give it mechanical checks:

1. every headline number reproduces from the model;
2. no disputed input appears as a bare point value without range or tag;
3. deferred quantities never appear as fact;
4. every figure has title, labelled axes with units, legend where needed, source line;
5. no orphaned headings, clipped columns, mid-word tag breaks, or near-blank pages;
6. every table row carries a tag.

Expect the audit to find real defects. On a document written in one pass it reliably surfaces a
silently-collapsed range and at least one misapplied provenance tag.

### 6. Deliver with conflicts visible

A plan that shows its seams is harder to dismiss than one that hides them, and it makes the blocking
question unavoidable. Red banner per affected section, plus a conflict register with owner, value at
stake, and the action that closes each row.

---

## Tag discipline

Five classes, defined so a reader with a browser can check the top one:

| Tag | Means |
|---|---|
| VERIFIED | traced to a cited **public** source; independently checkable |
| REPORTED | taken from the project's own basis-of-design synthesis — not internal data, not public either |
| DERIVED | computed here from tagged inputs, formula shown |
| ASSUMED | author judgement, reason stated |
| OPEN | unknown or disputed; no value offered |

VERIFIED on a non-public source discredits every genuine VERIFIED in the document. Keep the top class
expensive. A project synthesis written by you is REPORTED, never VERIFIED.

---

## Range discipline

**A derived range that varies only one input has silently resolved the others.** A voidage-replacement
ratio published as "1.40–1.56" looked like honest range-keeping, but the span came from varying the
formation volume factor alone while the plateau rate stayed pinned at its midpoint. True span across
both: 1.30–2.31 — a factor of 1.8.

Before quoting a range on a derived quantity, enumerate every input the formula contains and state
which ones the range actually moves. A range holding a disputed input fixed is a point estimate
wearing a range's clothes, and it is worse than a bare point because it claims the uncertainty was
handled.

---

## Figures from public evidence

No public coordinate, block polygon or field outline → do not draw one. Plot the real coastline from
Natural Earth, mark the point as schematic with a stated uncertainty, and draw the *constraint* (the
known offshore distance, a reference field at a published coordinate) rather than a boundary.

A position extrapolated along a coastline normal can land within a few km of a different, real field —
which reads as a claim that the two coincide. Anchor to a cited reference point, not a geometric
construction. If bathymetry data is not in hand, say so in the figure, not in prose elsewhere.

---

## Cashflow engine — waterfall and the eight bugs that produced plausible wrong numbers

Use when building or validating a PSC cashflow model.

**Waterfall, per year:** gross revenue → royalty (10% cash payment reference) → net revenue →
costs (opex + capex + abandonment + unrecovered carry-forward) → cost recovery capped at 70% of net
revenue → profit = net revenue − cost recovery → profitability index on *cumulative* net revenue /
cumulative cost → contractor share 90% below PI 1.5, 30% above PI 2.5, linear between → entitlement =
cost recovery + profit × share → taxable = entitlement − opex − abandonment − allowances − losses
→ net cash flow. Host take = royalty + tax + profit × (1 − share).

1. **No economic limit.** Production ran to the horizon with fixed OPEX still charged after cessation:
   14 years of negative cash flow, government take 92.8%, undiscounted cash crushed. Symptom:
   government take above ~70% on a PSC base case, or negative cash-flow years with zero production.
   Fix: truncate when net revenue − OPEX < 0 for **two consecutive years** (two, not one — a single bad
   year is price noise). Abandonment lands the year after the limit.
2. **IRR root selection.** With a terminal abandonment outflow, NPV(r) can be non-monotone at deeply
   negative rates; the solver returned the lowest root and reported IRR −2% alongside positive NPV —
   arithmetically impossible. Fix: scan downward from a high rate and take the first sign change, or
   bracket upward from r = 0. Assert NPV at IRR ≈ 0 and NPV monotone decreasing in r. Count `nan`
   cases (cash flow that never turns positive) separately; do not drop them from statistics.
3. **Tax base too narrow.** Taxing only the profit share ignores cost-recovery income and overstates
   IRR by 3–4 points. Tax the full entitlement less OPEX, abandonment and allowances, with losses
   carried forward; protect early years with a 5-year straight-line allowance, not by narrowing the base.
4. **Unit conversion.** `MMscfd → bcf/yr` is ×365/1000, not ×365/1e6. The order-of-magnitude error
   spread 784 bcf over 14,000 years and reported a 16,341-year field life. Assert peak rate against
   facility capacity every run; a life beyond ~40 years is almost always a unit error.
5. **Normalisation breaking a cap.** Solving a plateau analytically then rescaling to hit the resource
   pushes the peak above capacity (150 → 157 MMscfd). Bisect on plateau *duration* instead. If the
   resource cannot sustain the requested plateau, back-solve the rate.
6. **Float noise.** `a − b` printing `−0.0` in a table. Clamp at the presentation layer: `max(0.0, …)`.
7. **Water cut identical across cases.** A curve driven purely by cumulative fraction of recovery has
   the same shape for every case, making the cases indistinguishable and the figure decorative. Scale
   breakthrough by plateau duration (faster depletion breaks through earlier) and tag the curve ASSUMED.
8. **Gas that cannot reach its booked volume.** A declining profile from a capacity cap is asymptotic
   and will not deliver the resource in a realistic life (363 of 784 bcf after 26 years). Do not extend
   the horizon or soften the decline to close the gap. Model associated gas as
   `min(facility_cap, oil_rate × GOR)`, report the shortfall as a **non-associated balance**, tag its
   origin OPEN, and hand it to the facilities workstream. Cap cumulative delivery at the resource; the
   balance floors at zero, never negative.

**Harness assertions worth keeping:** NPV at IRR ≈ 0; NPV monotone decreasing in r; peak rate ≤
capacity; life ≤ ~40 years; host take 25–70% on a PSC base case; Σ yearly cash flow ≈ Σ undiscounted
waterfall lines; plateau volume < total resource.

---

## Production profile — the plateau collision

**Capacity-equivalent is arithmetic, not a forecast:**
`capacity_equivalent_years = resource / (rate × 365)`. 139 MMbbl at 39,800 bopd = 9.57 years. That
means the *facility* could pass the volume at full rate in 9.57 years; it says nothing about whether
the reservoir can deliver that rate that long. Treating it as a plateau duration is the origin of
over-optimistic field-life claims.

**Solve the profile** (linear ramp, hold, exponential decline) so the integral equals the resource:

```
Tp = (total − 0.5·q0·t_ramp·365 − q0·365/decline) / (q0·365)
```

If `Tp < 0` the resource cannot sustain that plateau — back-solve the rate instead.

**Report the split**: volume at plateau versus volume that must arrive in decline. That split is the
finding, not the plateau rate. At a fixed resource a higher plateau shortens the plateau and pushes
more volume into decline; a lower plateau does not merely stretch life, it changes the *shape* (61%
at plateau at 25,000 bopd versus 49% at 37,014). Shape drives facility utilisation, OPEX profile and
fiscal timing.

**Gas binds on rate, not on the field.** Binding threshold = `facility_mmscfd × 1e6 / GOR` — for
150 MMscfd at 5,640 scf/bbl that is ~26,600 bopd. Above it, associated gas saturates the train and the
booked gas volume cannot be delivered; below it the constraint vanishes. State it that way: the
decision is not "the gas train is too small" but "the plateau choice determines whether the gas
problem exists".

**Voidage:** `voidage = plateau_rate × Bo`, `VRR = injection_rate / voidage`. Both plateau and Bo are
usually unresolved, so the ratio must be a range across **both** (see Range discipline). Qualitatively
VRR > 1 at plateau means over-injection and pressure is not the constraint; quantitatively the margin
can swing by a factor of ~1.8, which matters for pump and topsides sizing.

---

## Equity architecture

**Asset NPV is not equity NPV.** Three legitimate views of one project, differing by a factor of
several: contractor (100% WI undivided, after royalty, cost recovery, profit split and tax); group
(contractor plus host share); national (gross revenue less all costs). A paper quoting one figure
without declaring which is quoting an untested equity assumption. **If no partner, carry or state
position is specified anywhere, 100% WI is not an equity assumption — it is the absence of one**, and
that gap is itself a finding.

**The participation mechanic dominates the headline percentage.** Same "10% to the state": paid
participation costs little, recoverable carry little (the industry norm), free carry roughly 9× the
paid alternative. A negotiator conceding a percentage without the mechanic has conceded anywhere
between a rounding error and the destruction of shareholder value and does not know which. Model all
three; the clause is worth more than the number.

**Farm-out at cost is pro-rata, not accretive.** IRR unchanged, NPV per dollar unchanged, absolute
NPV lower. It converts value into a smaller position at the same return. Present it honestly as
capital rationing, risk transfer, or capability — never as NPV accretion. For the retained share to
match full ownership the partner must cut capital by an implausibly large fraction; compute that
number and show it.

**Lease versus own inside a PSC.** Capex is recovered only through the ceiling pool and is discounted
while unrecovered; lease payments are OPEX and recovered in-year inside the same ceiling. The same
dollar comes back faster as opex than as capex — a genuine fiscal-timing gain — and it lowers peak
funding, often by more than the NPV effect.

**Report peak funding** (deepest cumulative cash trough and its year) beside NPV. Capex landing a year
before first oil means the project cannot be self-funding at any price; saying so beats another NPV
sensitivity.

**Breakeven is three questions:** NPV@hurdle = 0 (investment test); cumulative undiscounted cash = 0
(cash payback); operating cash covers capex every year (self-funding — the treasurer's and rating
agency's question, frequently unanswerable for a single asset). Quoting one as "the breakeven" is a
category error a reviewer will catch.

**Importing a peer's planning benchmarks:** take the *disciplines* — a declared flat-real planning
price, unit economics per boe, breakeven defined as a funding test — not the corporate model, which
for an oil major contains no PSC mechanics. If your planning price sits materially above the most
disciplined peer's, show the case at their price too.

---

## When the plan ships as a Typst PDF

- **`#` in a table argument list needs markup brackets.** `table(columns: 3, [Wells], [10], #V)` fails
  with "character `#` is not valid in code" — positional arguments are code mode. Wrap: `[#V]`. Batch
  fix: `s.replace(', #V,', ', [#V],').replace(', #V)', ', [#V])')` per tag letter.
- **`#page(numbering: "1")` is not a constructor** — use `#set page(numbering: "1")`. Scope numbered
  front matter with a content block: `#[ #set page(numbering: "i") … ]`.
- **Hand-numbered captions get a second automatic number** (`Figure 1: Fig 2 — …`). Set
  `#set figure(numbering: none)` and `#set heading(numbering: none)`, then number headings literally.
  Re-check the section sequence after edits — inserting one silently leaves a gap (`3.3 → 3.5`).
- **Narrow columns hyphenate short all-caps tokens** (`VERI-FIED`, `DE-RIVED`), detaching a status tag
  from its value. Give tag columns 13–15 mm and drop table body to ~7.8 pt.
- **Orphaned headings:** `#pagebreak(weak: true)` before the heading — breaks only when needed.
- **Verify numbers by text extraction, never by looking at a raster.** `pdftotext -layout` then
  string-match every expected value. At 60–110 dpi, vision OCR misread `OOIP` as `OODP`, substituted a
  different vessel name, and reported a figure missing that was present. Use the raster for layout only
  — overlap, clipping, contrast, orphans — never for digits.
- **Cheap post-compile scan:** per page, extract text, drop header/footer, flag any page whose last
  line matches a heading pattern, and any page under ~1,200 characters that is not figure-only.

---

## Pitfalls

- **Check the capital estimate against the project's own realism band before trusting any NPV.** A
  number above the stated band means either the estimate or the project is wrong, and the decision
  flips on it. Put that in the verdict, not a table footnote.
- **A deferred quantity must never acquire a number by inheritance.** Four workstreams computing four
  different economic limits is evidence the question is unowned, not evidence the median is right.
- **A unit-capacity ceiling can sit far below the design headline.** "60,000 bpd liquid processing" is
  oil *plus* water; the oil ceiling may be 25,000. Check the hull-class datasheet, not the marketing
  figure, before sizing anything downstream.
- **Every synthetic production profile needs an economic limit or an explicit statement that it has
  none.** Without one, fixed OPEX accrues through years of zero production and produces absurd fiscal
  splits.
- **Sibling agents collide in a shared working directory.** Parallel writers pick the same obvious
  filenames. Use workstream-unique names and re-read a file immediately before overwriting — another
  agent's output can replace your run log between compile and read.
- **A parent-document value is not evidence.** A basis-of-design assembled by the same effort from
  public reporting cannot launder its figures into VERIFIED. Cite the underlying public source or tag
  REPORTED.
- **A stakeholder percentage is a headline, not a mechanism.** Quantify the mechanic before quoting the
  number.
