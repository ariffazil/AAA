---
name: company-failure-analysis
description: "Use when judging if a firm is heading for failure."
tags: [finance, credit, bankruptcy, distress, sec-edgar, valuation, malaysia, bursa, falsifiability]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Company Failure Analysis

Judging whether a firm is heading for failure — and producing an artifact that survives
attack. Covers listed, delisted, private and state-owned entities; the data lanes for
entities with no live ticker; the distance-to-barrier calculation; the failure-mode
classification; and the write-up shape that makes the result falsifiable.

## When to use

- "Will this company go bankrupt?", "how long has it got?", "is X safe?"
- Analysing a company that already failed (post-mortem, or validating a method).
- Building or validating any distress score, distance-to-default, or survival-horizon model.
- Pressure-testing a claim of the form "this cannot fail" or "this is heading to zero".

## Stance — settle this before computing anything

1. **Answer in time, not probability.** People ask "how long do I have?", not "what is
   P(default)?". A horizon in years is actionable; a dimensionless probability is not.
   State the horizon, its unit, and the rate it assumes.
2. **Never assert a direction.** These models measure geometry, not direction. If the request
   is for a price call, say the method does not do that and show the test that proved it.
3. **Separate the entity's barrier from the asker's barrier.** "The firm is solvent" is not
   "your role, ladder or equity is safe". A shrinking firm and a shrinking function are two
   different barriers, and only one of them is usually being modelled.
4. **Report every test that refuted the hypothesis.** A results section that lists only
   supporting evidence is a sales document.
5. **State the direction of every unresolved bias** instead of resolving it by assertion.

## Procedure

### 1. Probe for data before declaring any lane absent

Sweep lanes, then record which returned data. Do not announce a capability as missing until at
least one alternate lane has been tried. See `references/data-sources.md` for endpoints, fields
and rate limits.

### 2. Verify entity identity before trusting any series

Providers key on an identifier, and identifiers get **reused** after a filer dies or delists.
Pull the provider's returned entity name alongside the numbers and reject any record whose name
does not match the entity you asked for. Record the rejection count. An unverified identifier is
a silent substitution, not a data gap.

### 3. Build the barrier from filed statements, not from price

The contractual barrier is total liabilities; the entity's value is total assets. Compute:

```
D = ln(Assets / Liabilities)        distance to the contractual barrier
lambda = rate at which D is closing  (use a 3-year window)
T = D / lambda                       horizon to the barrier
survival iff  mu > lambda            value must be built faster than trust decays
```

Price-based barriers are a proxy. Use them only when statements are unavailable, and label them
as a proxy. For entities with no ticker (private, state-owned) the statement form is the only form
that works — which is a reason to prefer it generally.

**Never interpolate a missing year.** A gap is evidence. A smoothed line through a company's
balance sheet is a fabrication, and it will be the first thing an attacker finds.

### 4. Run the cash detectors alongside the distance model

Distance-to-barrier cannot see falsification — its numerator is the item being falsified. Pair
every distance reading with:

```
OCF / reported profit      < 0.5 warning, < 0.3 strong warning
cash / total borrowings    monotone decline is the signal, not the level
```

A firm reporting profit while cash coverage falls every year is a different diagnosis from a firm
whose equity ratio is eroding. Both need reporting.

### 5. Classify the failure mode before crediting the signal

See `references/failure-modes.md`. At minimum separate:

- **Erosion** — the distance closes over years. Distance models catch this.
- **Fabrication** — the distance looks fine while cash never arrives. Cash detectors catch this.
- **Shock** — a healthy balance sheet is hit by a price or demand event. Nothing in either
  detector catches this; say so rather than crediting the model.
- **Transfer** — the asset changes hands legally. No quantitative detector catches this, because
  no number changes. Investigate who holds the right, under which jurisdiction, and who is
  permitted to invoice.

### 6. For state-owned entities, switch the barrier

A single-owner state entity does not face the contractual barrier that kills listed firms. Its
binding constraint is fiscal:

```
headroom = operating cash flow - dividend to the owner - maintenance capex
```

The asymmetry that matters: a listed shareholder who wants out **sells**, moving the loss to a
buyer and leaving capital in the firm. A state owner who wants more **takes**, moving capital out
of the firm. Model the second as a rate set outside the entity's control. Label it as a
formulation with unrun tests unless you have actually back-tested it.

### 7. Write it up so it can be falsified

See "Deliverable shape" below.

## Deliverable shape when asked to be "scientific"

When the request is to make an analysis scientific, formal or defensible, the expected structure is:

1. **Axioms** — what the framework assumes, stated as assumptions that could be denied.
2. **Definitions** — every symbol, with how each is measured.
3. **Propositions** — what follows, with proofs where the proof is short.
4. **Falsifiable predictions** — each numbered, each with its own **explicit falsification
   criterion** written directly beneath it.
5. **Tests run** — including the refutations, with the null baseline shown.
6. **Defect log** — defects found, and how each was found.
7. **Limits** — what the framework does not cover.

**Do not hedge an untested part as "only a formulation".** Attach falsification criteria to it and
present it as an untested hypothesis. A framework with testable predictions is the strongest form
of the work; only an untestable claim is weak. Hedging the language instead of naming the test is
what makes output read as unscientific.

Always include the **null baseline** for any predictive claim — for a binary call, the score from
giving every item the same answer. If the analysis does not beat that baseline, say so plainly.

## Figure and artifact production

- Produce dark-background multi-panel figures, then **verify each one with a vision read** before
  delivering. Check specifically for clipped footer text and for annotation clusters colliding
  with axis lines — both recur.
- Put coverage gaps in the figure as gaps. Add a note that un-sourced years are gaps, not
  interpolations.
- When the analysis is a test or quiz, **seal the answer in a separate file** and commit the guess
  before revealing. An unsealed answer is not a test.
- Keep a defect log inside the artifact itself, so a later reader sees the defect rather than
  having to rediscover it.

## Pitfalls

- **Reused identifiers silently substitute a different company.** Verify the returned entity name
  on every record; the failure mode is quiet and looks like valid data.
- **Price history for delisted tickers is often unavailable from free lanes.** Say which lanes were
  tried before concluding, and prefer filed statements — they are available for the dead and are
  the better barrier anyway.
- **A price-panel built from free data contains survivors only.** The dead are the ones that
  delisted. State the direction of this bias explicitly; do not resolve it by assertion.
- **A formula whose first run gives clean, well-behaved output is suspect.** If infinities or
  exclusions cluster non-randomly inside one category, that is a bug signature, not a finding —
  especially when the excluded category is the one you expected to be most dangerous.
- **A model whose numerator is the falsified item cannot detect the falsification.** Inflated
  assets widen the apparent distance. Say which detector is blind to which failure mode.
- **Do not attribute causation across a long lag without saying so.** Debt taken in one era
  produces losses five to eight years later, by which time the people holding office have changed.
  Attribute by the signature date on the decision, not by who holds the seat when the bill lands.
- **A slow shrinking firm is not a failing firm.** Erosion without a cash break is survivable
  indefinitely. Distinguish before alarming.
- **Announced benefits are not contractual terms.** A public statement about a package or capital
  measure is not a filed obligation.
- **Do not present a person's behaviour as a mechanism.** See named-entity discipline below.

## Named-entity discipline

Analysis of institutions frequently touches named living people. Apply these without exception:

- **Verify role, employer and dates before asserting any of them.** A wrong role or a wrong year
  inverts the inference — a person recorded as exiting on governance grounds is not evidence of the
  conduct they exited over.
- **Give the structural version when asked to characterise a person.** Committee concentration,
  appointment mechanism, independence ratios and incentive alignment are checkable by anyone reading
  the same public source. Character judgements are not.
- **Never amplify a personal attack on a named person, even when the user is its source.** The
  structural finding beside it is verifiable; attaching an unverifiable characterisation to it
  destroys the credibility of the part that could have survived scrutiny.
- **Name what is not claimed.** State explicitly that the finding is structural, that no criminal or
  collusive conduct is alleged, and that the source is the entity's own published material.

## References

- `references/data-sources.md` — EDGAR endpoints and fields, the entity-verification recipe, rate
  limits, first-party sources for Malaysian listed firms, state-owned entity reports.
- `references/failure-modes.md` — the failure-mode classification table, the detector for each mode,
  and what each detector is blind to.
