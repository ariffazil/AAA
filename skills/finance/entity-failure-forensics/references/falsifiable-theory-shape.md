# Falsifiable shape for an analysis or model deliverable

Use this structure whenever the output is a model, framework, or claim about how
something works — not just a one-off reading of one entity.

## The framing rule (this one was corrected)

**A theory is the highest tier of a scientific claim, not a weaker one.** Do not
soften an untested layer by calling it "a formulation, not a validated instrument" and
stopping there. That reads as a hedge and tells the reader nothing about how to break it.

What makes a claim unscientific is not being untested — it is being **untestable**.
The correct move for an untested layer is to state it as a **hypothesis with explicit
kill criteria**, so that anyone with the data can falsify it.

So: never present untested work as settled, and never present it as unsalvageable.
Present it as testable, and say what would break it.

## Required sections

1. **Abstract** — what the theory claims, what was tested, what was refuted, and which
   layers remain hypotheses. Written last, placed first.
2. **Problem statement** — the question being answered, and why the common framing of
   that question is the wrong deliverable (e.g. probability vs time).
3. **Position in the literature** — which existing work each component is taken from,
   and an explicit list of **what the literature does not provide**. The gap statement
   is where the contribution actually lives, so state it as a claim, not modesty.
4. **Axioms** — numbered, each one line, each load-bearing. If an axiom can be removed
   without changing any downstream result, remove it.
5. **Definitions** — symbol, meaning, and **how it is measured**. A symbol with no
   measurement procedure is not a definition.
6. **Derivation / propositions** — numbered, each with a one-line *why it matters*, not
   just the algebra. A proposition nobody can use is decoration.
7. **Predictions and falsification criteria** — see below. This is the section that
   makes it science.
8. **Evidence** — split explicitly into what **refuted** the hypothesis and what
   **supported** it. Report `n` beside every percentage.
9. **Defect log** — every flaw found in your own work, including flaws you fixed and
   how you found them. A defect log with nothing in it means the audit did not happen.
10. **Limits** — what the model does not measure, stated as boundaries rather than
    apologies (e.g. "this measures erosion, not shock").
11. **References** — full citations for every borrowed component.

## Predictions and falsification criteria

Every prediction gets a **paired** falsification criterion. A prediction without one
is a claim, not a hypothesis.

```
Pn.   [Specific, directional, measurable claim.]
      Tested?  ACCEPTED | REFUTED | NOT YET TESTED
      Evidence: [n, effect size, source]

FALSIFICATION Pn.
      If [specific observation], then [specific component] does not hold.
```

Rules for writing them:

- **Falsification criteria must be observable by a third party**, using data that
  exists or can be collected. "If the market disagrees" is not a criterion.
- **Name which component dies**, not just that the theory is wrong. A theory with
  several independent layers should lose only the layer that failed.
- **Write the criterion even for layers you have tested and accepted.** The accepted
  ones are exactly the ones a future reader will want to attack.
- **Include a negative prediction** — something the theory explicitly does *not*
  claim. It costs one line, and it prevents the theory from being read as a general
  oracle when it only answers one question. If the model ever appears to be predicting
  direction, it has been misread, and the negative prediction is what says so.

## Status vocabulary

Use exactly these three states, and never blur them:

| State | Meaning |
|---|---|
| **TESTED-ACCEPTED** | Ran it, it held. Give `n`. |
| **TESTED-REFUTED** | Ran it, it failed. Keep it visible — do not delete the hypothesis. |
| **UNTESTED** | Not run. Must carry a falsification criterion and a reason it could not be run. |

A refuted hypothesis is a **result**. Deleting it and keeping only the survivors is
how a document turns into marketing.

## Evidence discipline

- **`n` beside every percentage.** "45% failed" is meaningless without the denominator.
- **Say the confidence interval or say the sample is small.** A handful of cases can
  falsify a clean claim; it cannot establish a rate.
- **Distinguish a measured absence from an assumed one.** If a lane returned nothing,
  record what the sweep tested.
- **State the direction of a known bias** rather than resolving it away, when the data
  to resolve it does not exist.
- **Do not let a structural finding borrow a numerical authority it has not earned.**
  A qualitative observation about structure belongs in prose, not in a coefficient.

## Defamation-safe framing for structural findings

When the analysis touches governance or named people:

- Keep it **structural**: seats, committees, appointment mechanisms, disclosure
  timing. These are checkable against the entity's own published documents.
- **State what is not being claimed** — in its own section. No allegation of
  misconduct; no unverifiable group labels; no inference about intent.
- **Say why the structural version is stronger**: it survives scrutiny because anyone
  can verify it, whereas an unverifiable claim about a person's motives becomes the
  weakest link in an otherwise sound document.
- If verification **reverses** an inference the user offered, say so plainly and give
  the record. Correcting a premise costs the story and buys the credibility that makes
  the rest usable.

## Artifact delivery

Before delivering any rendered document: re-render, inspect the pages, and fix
clipping, overlap, and truncated text. Verify that required sections are present and
that the status of every claim (tested / refuted / untested) is visible in the document
itself, not only in the conversation that produced it — the artifact outlives the chat.
