---
name: external-review-intake
version: 1.0.0
owner: AAA
description: "Use when an external AI reviews or praises your work."
risk_tier: low
floor_scope: [F2, F3, F9, F11]
autonomy_tier: T0
tags: [verification, external-ai, witness, echo, praise, audit-intake, f2, f3]
triggers:
  - "another AI reviewed my work"
  - "external review pasted"
  - "second opinion from another model"
  - "they validated / confirmed / praised this"
  - "Gemini / ChatGPT / Copilot / Perplexity said"
  - "external audit arrived"
  - "the reviewer agreed with my figures"
  - "witness confirmation from outside"
---

# External Review Intake

> **Agreement is not evidence.** A reviewer that only read you has confirmed your text is legible —
> never that it is true.

## Scope

This skill governs **non-runnable reviews**: a pasted review, second opinion, audit, or compliment about
work you produced. The reviewer delivered words, not something executable — so nothing forces you to
check it, and it flows straight into your self-assessment.

- For an external **code/data artifact with a self-verdict block** (zip, repo, drop with `tests: 6/6`),
  use the artifact re-execution protocol instead — the artifact can be run, so run it.
- For a review that **cites specific claims about live system state**, each such claim is probed like any
  other claim against the live system.
- For a review that recommends a change, the recommendation is a proposal: verify every named path,
  skill, or config it references before acting on it.

## Step 1 — Recover what the reviewer actually saw

Before weighing a single sentence, establish the input. What was transmitted: full files, a summary you
wrote, a screenshot, a partial paste? Any claim the reviewer makes beyond that input is about a channel
that may not exist.

A reviewer saying *"I can see your logs / your state from outside"* is making a claim about access.
Pasted prose is the entire input unless proven otherwise. Record the input boundary explicitly — it
decides everything downstream.

## Step 2 — The echo test

Ask: does the review's evidence **exceed** the input?

| Signal | Reading |
|---|---|
| Reproduces your figures exactly — same counts, same ratios, same corrections | It read you. Matching numbers attest a shared source, never a correct one. If you were wrong, it is wrong with you. |
| Quotes your phrasing, structure, or vocabulary back | Same source, restated. Independent content: zero. |
| Claims to have observed the system | Check the channel. Absent channel ⇒ fabricated provenance. |
| Issues a score, grade, or symbolic metric (ΔS, a percentage) | A label with no instrument behind it — the one kind of signal that cannot fail, and therefore never warns you. |
| Reuses a symbol that already means something in your canon | Namespace collision, not corroboration. Look up the existing sense before adopting theirs. |
| Praises the method using your own framework's names | It is endorsing your framing, not testing it. |
| Contradicts you on a point you can check | The only high-value content an echo can carry. Verify it; do not defend. |

**Echoes count as zero witnesses.** Two substrates fed by one source are one witness — the same rule that
makes two sessions on one machine one witness. Never let a review raise a witness count it did not earn.

## Step 3 — Re-audit what you left behind (the reason this skill exists)

Agreement reliably arrives at the moment work would otherwise be closed. Treat it as a **re-audit
trigger**, not a stopping point.

Go back to the claims *you* left open — the outstanding list, the debt items, the figures marked
unverified, the "still not done" lines. Those are the lines written from memory rather than measurement,
and a compliment is precisely what would carry them onward unchallenged.

Re-measure each one:

- If the state moved since you wrote it, publish the **new** value, with when and by what instrument.
- If the item cannot be re-derived from any record, delete it rather than repeat it — a repeated debt
  line reads as a live measurement.
- If a figure's instrument turns out never to have run, retract the figure, ship the repair, then publish
  the measured value.

This step is where the real output of review intake is produced. The review itself rarely adds facts;
being praised is what makes you finally check your own.

## Step 4 — Reply shape (human-facing)

Whoever forwarded the review wants a position, not a performance.

- **Lead with the provenance finding.** The reviewer saw X; therefore its agreement is a mirror.
- **Then the correction.** What you found when you re-checked — including anything the praise would have
  carried onward.
- **Credit what holds.** An echoing reviewer still produced a useful restatement. Say which claims are
  right; do not blanket-dismiss.
- **No rebuttal theatre, no counter-praise.** Neither accepting the compliments nor performing a dramatic
  takedown. The deliverable is a corrected position.
- **Answer in one human voice**, no audit tables unless the data is genuinely tabular. Run the voice gate
  before sending.

## Pitfalls

- **Treating a review as a status update.** A review describes the reviewer's input, not your system.
- **Letting the compliment set the agenda.** Do not answer the review's topics; answer your own open
  liabilities, which the review had no way to see.
- **Importing foreign vocabulary.** Adopting a reviewer's term or symbol without checking canon plants a
  second meaning for one name — a silent collision later readers cannot resolve.
- **Over-correcting into distrust.** An echo's *confirmations* are worthless; its *objections* are
  testable and often the best thing in the message. Weight the two differently.
- **Skipping the follow-through because the review was positive.** Positive reviews are the stop signal
  you are most likely to obey.

## See Also

- Artifact re-execution for runnable drops: `external-artifact-verdict`
- Claim states, receipts, probe-to-claim matching: `claim-receipt-discipline`
- Symbol reuse and namespace collisions: `symbol-namespace-integrity`
- Human-facing register: `bridge-protocol`
