---
name: artifact-source-reconciliation
description: "Use when auditing artifact numbers vs primary sources."
version: 1.0.0
risk_tier: low
floor_scope: [F2]
autonomy_tier: T1
tags: [audit, numbers, primary-source, correction, render]
---

# Artifact Source Reconciliation

> A derived sentence can be false while every component number is correct. Recompute the sentence,
> not just the inputs.

## When this applies

- A dossier, PDF, briefing, leaflet or article lands for verification — drafted by you earlier, by a
  sibling agent, or pasted by the principal from somewhere else.
- A story is being told *from* numbers and someone will open the source beside it.
- You are about to publish a corrected version of something already circulated.

The deliverable is never "here is a list of errors". It is the corrected artifact, re-rendered, plus a
short plain-language account of what changed and the document that settles each change.

## Procedure

1. **Extract every number and tag it.** `REPORTED` (stated in a named source), `DERIVED` (arithmetic),
   `INTERPRET` (thesis). Do this before judging any of them — an artifact that labels its thesis as
   interpretation is stronger than one that hides it, and saying so is part of the audit.
2. **Locate the primary for each figure.** Filing, regulator database, annual report, statistical
   release, the system's own logs. A news piece is a summariser, never a source of record.
3. **Run the five probes** (below) in order. They are ordered by yield.
4. **Fix, then re-render, then re-grep.** A correction that stays in the chat is not a correction.
   Rebuild the artifact and grep the rendered output for the old figure — it must return zero.
5. **Write the receipt beside the artifact** recording: what was checked against what, what failed,
   what was fixed, and what remains open. Name the open items explicitly rather than closing the
   document around them.
6. **Deliver in the principal's language, short.** One line per correction: the claim, what is true,
   which document settles it. Not a methodology essay.

## The five probes

**1. Grep the primary for every literal figure.** A number that appears nowhere in the source it is
attributed to is an **orphan** — not a rounding difference, not a stale version, an object with no
parent. Orphans are the highest-value finding: the rest of the document is usually sound, and this is
what a hostile reader finds first. Common shape — an operational split (how much is actually in
service) invented for a source that publishes only a blended total. Remove it, or name the document
that carries it.

**2. Recompute every visible equation literally.** Where the prose says "A minus B equals C", do the
subtraction. If it does not compute, the author's real decomposition differs from the lines printed.
The fix is not to delete the sentence but to write the true decomposition out with the identity
closing, so a reader can follow it. Showing the correction as `13.29 − 11.48 = 1.81` is a repair;
anchoring only the difference fixes the digit and leaves the reader unable to check it.

**3. Name the FX year and back out the implied rate.** Every currency conversion carries a rate and a
period; state both. Then divide the original amount by the printed foreign-currency figure to recover
the implied rate. If it implies a different year than the one claimed, the number belongs to that year
whatever the sentence says. Two figures for one transaction is not a typo to average — it is a
citation error you can date.

**4. Check each citation's year, entity and version**, not just its outlet. A correct number
attributed to the wrong year or the wrong subsidiary is still false, and it is what a reader holding
the same document catches instantly.

**5. Ask whether the frame is too harsh before defending the number.** Overstatement is a separate
defect from a wrong figure, and it hands opponents a cheap rebuttal that discredits the true parts.
Measured case: describing committed under-construction capacity as "land, contracts and promises"
overstates — committed capex is not a promise. The honest version, "one blended bag; the split is not
published", is *sharper*, because it is unanswerable. Softening an overreach usually strengthens the
piece. Never soften a figure the source actually states.

## Loss taxonomy — where summarisers and drafts go wrong

| Loss | Signature | Recovery |
|---|---|---|
| **Metric collapse** | One word — commonly "cash" — standing for a balance, a net position and a flow at once | Pull the primary, match the *label* |
| **Series collapse** | Two published series for one period presented as one | Read the source table row by row |
| **Scope collapse** | A subsidiary's figures quoted at the size of the segment containing it, or the reverse | Find whether the entity has its own line; print both, labelled |
| **Wording collapse** | An accounting event reported as an operating outcome | Quote the primary's sentence verbatim |
| **Definition drift** | A metric's meaning changes between reporting years, in a footnote under the chart | Quote the footnote; say what it does to the delta |

**Scope collapse** looks like generosity and reads as inflation — a mixed segment's revenue attached to
one child entity makes that entity look ten times its size. The tell: the same document gives the child
a revenue an order of magnitude smaller somewhere else. Print both numbers and keep the word "segment"
beside the big one.

**Definition drift is the one that survives every other check.** When a source changes what a metric
measures between years, the year-on-year delta is not a delta — part of it is a change of ruler. Quote
the footnote in the source's own words, then state the consequence, including "the split is not
published, so the size of the definitional component is unknown" when that is the truth. That sentence
is stronger than the growth claim it replaces.

## Reporting a correction set

- Keep the count honest in both directions: a document with three bad numbers and thirty good ones is a
  document with three bad numbers. Do not let the corrections read as though the whole thing was rotten,
  and do not let a clean preface hide the three.
- Name what survives. Readers extend credit from the parts that held.
- Where a claim was right but attributed to the wrong year or the wrong entity, say exactly that —
  "right number, wrong year" is a different repair from "wrong number".
- Never silently patch. A version bump plus a short change account is what lets a reader holding the old
  copy know which document they have.
- When the correction removes a figure entirely, check what argument was resting on it. Deleting the
  number while leaving the conclusion is half a correction.

## Pitfalls

- **Do not accept the artifact's own sourcing as proof the figure exists.** A footnote naming the right
  document is not evidence the number is in it. Open the document.
- **Do not audit only the numbers the artifact flags.** Errors concentrate in the figures presented
  without ceremony — the ones in a summary paragraph, an opening line, a caption.
- **Re-grep after re-render.** Converters drop blocks (tables, boxed panels, columns) silently; a
  correction can be present in the source file and absent from the PDF that ships.
- **Do not let a rendering tool's failure look like a content problem.** Currency symbols and math
  delimiters in prose can break a typesetting build — fix the escaping, not the sentence.
- **Do not hand back a defect list when you hold the pen.** If you can fix and re-render in the same
  pass, doing so is the deliverable.

## Reference

`references/petronas-gentari-verified-anchors.md` — worked example of the probes applied to a PETRONAS
subsidiary dossier: the verified anchors, the probes that caught real errors, and the two source traps
(blended capacity reporting, definition drift) worth knowing before writing anything about that
institution again.
