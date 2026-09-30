---
name: institutional-spend-accountability
description: "Use when a spend line is challenged against human need."
version: 1.0.0
risk_tier: medium
floor_scope: [F2, F9]
autonomy_tier: T0
tags: [accountability, arithmetic, provenance, glc, civic]
---

# Institutional Spend Accountability

> The user takes a discretionary spend line — a sports title sponsorship, a brand activation, a junket
> — and asks *"if that money went elsewhere, how many human outcomes would it buy?"* Rhetorical in
> tone, literal in substance. They want a number they can carry into an argument.

It is a numeric artifact and it fails where every numeric artifact fails: a figure that reaches the
reader without its basis. Two things make it fail harder than usual:

- **The divisor, not the numerator, decides the answer.** Same spend, same population, an order of
  magnitude apart depending on which unit cost was chosen. Nothing in the arithmetic reveals the
  choice.
- **The counter-argument is predictable.** The institution always has a stated justification for the
  line. A reply that does not pre-empt it leaves the user exposed the first time someone raises it.

## When this applies

- A named institution's spend line is being measured against a public need (education, health,
  welfare, infrastructure).
- The user wants a defensible figure or comparison, not a slogan — they may repeat it, forward it, or
  put their name on it.
- Often the institution is the user's own employer or a state-linked body, so the numbers must
  survive colleagues who know the line item.

Not this skill: reconstructing the total cost of an event from comparables, or producing a poster or
viral caption. Those are separate shapes.

## Procedure

### 1. Fix the numerator and label its warrant

The spend line is usually **not disclosed** by the institution. Cite the reported figure together with
its reporter ("reported at USD X/yr by <outlet>") and say plainly that the body does not publish the
contract value. Quoting a reported figure as though it were disclosed is the one defect that kills the
entire argument.

State the currency conversion used, with its date.

### 2. Name the unit cost and its basis — give at least two

This is the divisor. Two defensible choices, an order of magnitude apart:

- **Average per-capita public cost** — the relevant budget ÷ the population it serves. Answers *"what
  would it cost to keep them in the system?"*
- **Marginal cost** — last-mile support (transport, meals, fee waivers, remedial hours) that prevents
  the specific outcome. Answers *"what would it cost to prevent this case?"* Always far smaller,
  always more flattering to the institution.

Label every result with which divisor produced it. A single divisor presented as *the* cost is the
failure shape: the reader supplies the other one and your number reads as inflated.

### 3. Source the affected population — never estimate it

A rate times a population, both from the same source ("the official dropout rate × the enrolled
count"), is a quotable derived figure. A round-number guess at the population is not, and it is the
first thing a hostile reader checks.

### 4. Give two or three framings, not one

- annual-cohort cost (cover everyone affected this year)
- whole-journey cost (rate × years in the system)
- per-person-year (the bare conversion)

Each answers a different question. A reader attacks whichever single frame you chose; two frames that
both survive beat one that is optimal.

### 5. Compare against the institution's own published line item

The strongest form needs no estimate at all: the body's **own disclosed numbers** do the accusing —
"its sponsorship ≈ its published scholarship budget, to the same order of magnitude." No comparables,
no assumptions, nothing to defend.

This is usually the payload. Lead with it when it exists.

### 6. Carry the standard counter *and* the rebuttal

Name the stated justification fairly (R&D, technology transfer, brand equity, inbound traffic), then
apply both tests:

1. Is there a **published** return figure for it?
2. Does the claimed benefit reach the population in the comparison line?

Pre-empting this is not fairness for its own sake — it is what stops the user being flattened.

### 7. Refuse the breakdown you do not have

When the ask is framed by ethnic, regional, religious, or other sub-category and no source splits the
population that way, say the cohort is the whole national pool and stop. An invented plausible split
converts a defensible argument into a falsifiable one, and it will be falsified.

### 8. Arithmetic comes from a tool, not the model

This shape is a chain of divisions (spend ÷ unit cost, rate × population, total ÷ years). Drift across
the steps is invisible, and a principal who distrusts model arithmetic may re-ask the same question to
test it. Every figure from a `python3 -c` call; show the working when it may be scrutinised.

### 9. Deliver the ammunition, then the artifact

The user asked for a number — it goes in the opening lines. If the ask also carries "tell them" /
"write it", the second deliverable is the ready-to-send paragraph: short, plain, no internal jargon.
Do not escalate to a formal letter unless a formal letter is what was asked for.

## Pitfalls

- **The divisor is the argument.** Same spend, same population, 10× different answer depending on a
  choice the arithmetic does not show. Label it or the number is unusable.
- **Reported ≠ disclosed.** A number from a reporter is a different object from a number from the
  body's own filing. Label which one you hold, every time.
- **A name attached to a structural critique is still a personal allegation.** Naming the institution
  or the decision is the critique. Naming an officer as *the villain of it* moves the sentence onto the
  defamation surface — keep the officer's name to the address line, never inside the accusation.
- **Label the result a scenario when any input is reported rather than disclosed.** A reported
  numerator over an average divisor is not a measurement, and may not be compared against a measured
  figure as though both were.
- **Lead with the scale comparison, not the shock total.** "One year of line A ≈ the entire annual
  cohort of outcome B, with change left over" survives scrutiny; a big scary total just invites the
  reader to attack the divisor.
- **Do not moralise.** The user is making the point, not asking for a sermon. Supply the sourced
  arithmetic, the counter-argument and the rebuttal, then stop.
- **Re-source the figures at use time.** Public budgets, enrolment counts and reported deal values all
  move. Never reuse a number from a previous session without re-checking it against the current
  primary source.

## Output shape that survives scrutiny

1. The headline comparison, with its warrant in the same breath.
2. The inputs, each labelled: reported vs disclosed; which divisor basis; which population source.
3. The honest caveats — average vs marginal, and any counter the user will face.
4. The ready-to-send paragraph, if the ask carried one.

## Related

This skill is the spend-versus-outcome shape. For general number discipline (provenance classes,
scenario-vs-measurement, never correcting another party's count) see the `auditable-numeric-artifacts`
skill. For reconstructing an event's total cost and turning it into a shareable surface, see
`public-source-cost-reconstruction`.

DITEMPA BUKAN DIBERI ⚒️
