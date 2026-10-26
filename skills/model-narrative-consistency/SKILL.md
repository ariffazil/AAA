---
name: model-narrative-consistency
description: "Use when describing a model in prose. Test each claim."
version: 1.0.0
risk_tier: low
floor_scope: [F2]
autonomy_tier: T1
tags: [verification, modelling, epistemic, quantitative, audit]
metadata:
  hermes:
    tags: [verification, modelling, epistemic, quantitative, audit]
    related_skills: [auditable-numeric-artifacts, field-development-plan, verify-before-report]
---

# Model–Narrative Consistency

Companion to provenance discipline, covering a different failure. Provenance asks *where did this
number come from*. This asks *does the model actually do what the document says it does*.

The two diverge silently. A model can be correct and its description of itself false; a document can be
fully sourced and still assert a mechanism that appears nowhere in the code. Both survive review because
each looks like diligence: citations in one column, a formula in the next.

## When this applies

Any situation where you compute something and then write sentences about it — cashflow and fiscal
models, risk simulations, production profiles, backtests, forecasts, scoring systems, capacity plans.
Load it before writing the conclusions section, not after.

---

## Procedure

### 1. Assert each case reaches the parameter that distinguishes it

Before reading any result off a scenario, check it actually got there. The failure is a clamp inside a
shared helper that quietly caps the case at the base case's limit. A case labelled "capacity raised to X"
that is internally pinned below X will report *less* output at plateau and *more* cumulative recovery —
because a decline clock started from the requested rate while the duration came from the clamped rate —
inverting the conclusion the case was built to test.

```
assert max(rates) == expected_peak, f"{label}: peaked {max(rates)}, not {expected_peak}"
```

Run this for every case, every time. A scenario that cannot reach its own premise is not a scenario.

### 2. Vary the driver your prose names, and confirm the output moves

For every sentence of the shape "X is an output of Y" or "Y governs X": hold everything else fixed, run
two values of Y, and compare. If the output is identical, the mechanism you described is not in the
calculation.

This catches a specific and common divergence: the prose describes the causal story the author has in
mind while the code implements a different one, and both are plausible enough that neither looks wrong.
A document can claim a result is driven by replacement ratio while the model returns an identical result
for both values of it — the real driver being a separate capacity constraint. The narrative was
coherent, the code was correct, and the sentence bridged them falsely.

### 3. Check that closed forms match the shape of the profile

A closed form carries an implicit assumption about the curve it describes. `EUR = q/Di` is a
decline-from-day-one profile. Applied to a plateau-then-decline well it understates required decline,
because it credits the whole recovery to the tail:

```
plateau then decline:   EUR = q·Tp + q/Di      →   Di = q / (EUR − q·Tp)
```

Same inputs, and the two forms differ enough to flip a verdict — one number reads as an unremarkable
normal case, the other as an implausible one. Before using any closed form, write down the profile it
assumes and compare it to the profile you actually run.

### 4. Declare every truncation, cutoff and break

Any loop that stops early is a parameter doing work on the headline figure. Two different plausible
cutoffs can move a total by 15–20%, which is enough to change a decision.

If the document states a quantity is absent — "no cutoff is applied", "no limit is assumed" — and a
function applies one anyway, the document is misdescribing its own model. That is a different and worse
defect than an unstated assumption, because it asserts a negative the reader cannot check without reading
the code.

Declare the cutoff beside the result, and show the sensitivity in the same table.

### 5. Recompute from corrected input — never merely delete the line

When an input turns out wrong, removing the sentence that quoted it leaves the *conclusion the wrong
input induced* still standing, now unsupported and unlabelled. The correction is not complete until
everything downstream has been re-run.

### 6. Separate claims that depend on the contested input from claims that do not

The most useful move after an input is discredited. Sort your findings into two piles:

- **rests on the contested input** — withdraw, or re-present across the range;
- **rests only on independently verified inputs** — survives, and is now your strongest material.

A finding that survives this sort is worth more than the original headline, because it no longer
inherits the uncertainty. Say so explicitly: the reader needs to know which claims moved and which did
not, or they will assume everything moved.

---

## Receiving an audit of your own model

1. **Open the primary yourself before conceding or defending.** Agreeing quickly is as unreliable as
   refusing, and both are cheap substitutes for checking.
2. **Classify each finding** — wrong input, wrong arithmetic, wrong mechanism, wrong provenance. They
   need different fixes and they have different severities. An auditor can be right about the input and
   wrong about the arithmetic in the same item; untangle it rather than accepting or rejecting wholesale.
3. **Reject with evidence where the auditor is wrong, in the document.** A correction table that shows
   both the accepted and the rejected findings is more credible than one that accepts everything, and it
   protects a correct number from being retracted to look compliant.
4. **Version the artifact and carry a change table** — previous value, new value, reason. A reader
   holding the old copy cannot otherwise tell which they have.
5. **Re-run the argument, not just the number.** A corrected figure usually supported a larger claim;
  fixing the figure and leaving the claim is half a correction.

---

## Pitfalls

- **A ratio of two estimated totals is not a measured property.** Dividing one estimate by another gives
  an identity carrying the uncertainty of both inputs and the physical meaning of neither. It is not a
  measured ratio and not a composite. Label it as a ratio of totals, and if a conclusion rests on it,
  show the conclusion across the range of both inputs — it may invert.
- **A case that can't reach its premise will lie in whichever direction is least expected.** Clamps
  usually cap upward movement, so an "improved" case silently becomes a degraded one, or vice versa
  through a timing offset. Assert the premise.
- **Identical output across cases that should differ is a bug signal, not robustness.** If two scenarios
  built to diverge return the same figure, either the differentiating input is not wired in or it is
  being overwritten. Investigate before reporting the agreement as a finding.
- **Do not let a plausible narrative substitute for a tested mechanism.** A causal sentence is a claim
  about the code. If you have not varied the variable, you do not know it.
- **Beware the finding that rests entirely on one contested input.** It is the most fragile thing in the
  document and usually the most prominent. Find it deliberately and mark it, rather than discovering it
  when someone else does.
