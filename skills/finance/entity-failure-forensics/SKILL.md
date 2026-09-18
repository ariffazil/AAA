---
name: entity-failure-forensics
description: "Use when analysing if an entity will fail financially."
version: 1.0.0
license: MIT
---

# entity-failure-forensics

> Establish **how long an entity has**, what evidence supports it, and what would
> prove you wrong — then ship it as a verified artifact.

Applies to: listed companies, delisted/bankrupt companies, private companies,
state-owned enterprises / national oil companies, and an individual's own position.

## The core quantity

```
D = ln(V / B)          gap to the barrier
T = D / (lambda - mu)  time to that barrier
```

**Distance divided by rate.** Two consequences to state up front every time:

1. `T` is a **time**, not a probability. Humans plan in time. Answer in time.
2. Adding predictive sophistication changes neither `D` nor `lambda`. It only changes
   your confidence about the same number. When a user asks "can you predict X", the
   honest answer is usually that prediction is the wrong deliverable and
   **distance-over-rate is the right one**.

`lambda` is not exogenous: `lambda = lambda_market + lambda_governance + lambda_attention`.
See `references/failure-modes.md`.

## Procedure

### 1. Establish the barrier type before touching data

| Entity | V | B (barrier) |
|---|---|---|
| Listed company | total assets | total liabilities |
| Listed company (price only) | price | running max x 0.20 |
| Private company | total assets | total liabilities |
| State-owned / NOC | — | **fiscal**: `CFFO - dividend - capex` |

For an NOC the contractual barrier is usually irrelevant (debt a small fraction of
assets, distance measured in centuries). Asking whether a national oil company can
default is not the user's real question. Compute the **fiscal headroom** instead and
say plainly that the contractual figure is true and useless.

### 2. Route to the right data lane

Full lane table with endpoints and quirks: `references/data-lanes.md`.

- **Live listed ticker** -> price lane is fine.
- **Delisted / bankrupt / renamed entity** -> **go to filings, not prices.** Free price
  lanes do not serve history for dead symbols. Filed balance sheets are the lane that
  actually carries the dead, and they give a *contractual* barrier rather than a
  price proxy — strictly better anyway.
- **Run the inventory sweep before declaring any lane empty.** Probe several symbol
  variants and both asset classes before concluding data does not exist.

### 3. Verify entity identity on every filing record

**Filing identifiers are reused after a filer dies.** The same central-index number
that was one defunct retailer now belongs to an unrelated live company. A record
that resolves is not a record that is *yours*.

Therefore: pull `entityName` on every record and **reject any mismatch against the
expected filer**, even when the numbers look plausible. On a panel of ~25 dead
retailers/distributors, roughly two thirds were rejected this way. Treat entity-name
matching as a required field, never a nicety.

### 4. Compute both detectors — never just one

This is the rule that most changes conclusions. A model whose numerator is the line
item being falsified **cannot detect the falsification**: inflating assets inflates
`ln(A/L)`, which pushes the barrier *further away*, making the entity look safer at
exactly the moment it is most dangerous.

| Detector | Catches | Blind to |
|---|---|---|
| `T = D/lambda` (distance) | **erosion** — gap closing over years | fabrication, shock, transfer |
| `OCF / PAT` and `cash / borrowings` | **fabrication** — profit never arrives as cash | anything else |

Report both for every name. Passing one and failing the other is not "safe" —
it is **untested on the other axis**. Details and thresholds: `references/failure-modes.md`.

### 5. Check for the third failure mode before trusting your own arithmetic

If the claim on the asset itself is disputed or reassigned, `T` stays arithmetically
correct and empirically meaningless. No default occurs; no books are falsified; the
asset simply belongs to someone else. The only signals are **who invoices**, **whose
law governs**, and **who signs**. Look for duplicate claims on the same revenue
before concluding the numbers mean what they appear to mean.

### 6. Verify any named person before building an argument on them

**Rule: never state a role or tenure for a living named person without checking it
against a source, and correct the user's premise plainly when it is wrong.**

Both halves of a premise can be wrong at once (wrong title *and* wrong years). State
the record: what the person actually held, the dates, and who held the role the user
meant. Add the practical stake when the person is senior — a wrong claim about a
named executive is a reputational cost the user pays, not you.

**Never attribute malice to a named living person.** Convert the concern to
**structure**: which seats, which committees, which appointment mechanism. Structure
is checkable by anyone, survives scrutiny, and cannot be dismissed as a grudge.
Malice is unverifiable, is not evidence, and **weakens** the checkable finding sitting
next to it. If the fixable claim is "one director chairs both audit and risk and sits
on nomination", write that — not an insult. And when verification reverses the
inference (a person who *resigned* from a troubled body on governance grounds is not
the same as one who ran it), say so even though it costs the story.

### 7. Deliver the analysis in falsifiable shape

When the output is an analysis, a model, or a claim about how the world works:
**state axioms, propositions, falsifiable predictions, and explicit falsification
criteria.** Full structure and required sections: `references/falsifiable-theory-shape.md`.

A framework is not weaker for being untested. It is weaker for being untestable.
Label untested layers as **hypotheses with stated kill criteria** — not as
"formulations, not validated instruments", which reads as a hedge and tells the
reader nothing about how to break it.

### 8. Verify the rendered artifact before delivering

Rendered figures lie in ways the source data does not. Loop: render -> convert to a
viewable image -> inspect for clipped/overlapping/truncated text -> patch -> re-render.
Fix annotation crowding, not just correctness: stacked labels on one vertical band,
legends over trajectories, off-scale values that vanish instead of being marked.

Two rules for this loop:
- **Off-scale means mark it, never clip it silently.** Values beyond the axis need an
  arrow or an "exceeds scale" marker, or the reader assumes they do not exist.
- **Trust the visual read for layout; re-verify every figure from your own compute.**
  Image reads misread exact strings and numbers (company names, table headers). Layout
  findings are reliable; text content findings are not.

### 9. Never interpolate reported financials

If a period is missing, plot a **gap**. Interpolating a balance sheet makes a
fabricated or unaudited stretch look continuous, which is precisely the illusion the
analysis exists to detect. Use a gap-aware line helper that draws only contiguous
runs of finite values. `scripts/apex_t.py` provides one.

## Pitfalls

- **Infinities clustered in one category are a bug signature, not a finding.** A
  first pass returned `T = inf` for half the panel, and every one of those sat in the
  single quadrant the author expected to be most dangerous. The trust-decay term was
  inverted: first-passage is governed by the **long-run** drift, with the short-run
  signal entering as the unbacked-promise term. If a whole class of observations
  drops out structurally, suspect your formula before you interpret the result.
- **A model that returns clean numbers on the first run is suspect.** Inspect the
  distribution of missing and infinite values before reading any conclusion.
- **Survivorship is the default failure of any panel built from live sources.** If
  the dead are absent, say so and state the direction of the bias rather than
  resolving it away. Then build a second panel that *does* contain the dead.
- **Do not let a small sample masquerade as validation.** A handful of firms is
  enough to falsify a clean claim and not enough to establish a rate. Report `n`
  beside every percentage.
- **Separate "refuted" from "accepted" in the results.** Several tests in the origin
  session rejected their own hypothesis. An analysis that reports only its successes
  is not evidence.
- **A dividend or yield is the price of mortality, not a bonus.** An entity with
  infinite time (a commodity) pays nothing to wait; an entity with finite time pays
  you for holding something that can die. That framing is the bridge between the
  structural and the practical reading of the same number.
- **Distinguish an unresolved dispute from a lost one.** A litigated outcome that
  went in the entity's favour still tells you the claim was contested, which is the
  signal. Report the mechanism, not just the verdict.

## Support files

- `references/data-lanes.md` — which lane carries which entity class, endpoints,
  the identity trap, and how to route dead / private / state-owned entities.
- `references/failure-modes.md` — erosion vs fabrication vs transfer, detector per
  mode, cash-conversion thresholds, the fiscal barrier, governance and attention terms.
- `references/falsifiable-theory-shape.md` — required section structure for an
  analysis or model deliverable, with the axiom/proposition/prediction layout.
- `scripts/apex_t.py` — re-runnable distance-to-failure computation from reported
  balance sheets, plus a gap-aware plotting helper.
