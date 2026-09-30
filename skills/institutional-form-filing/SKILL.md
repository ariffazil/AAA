---
name: institutional-form-filing
description: "Use when filing an official form for the principal."
version: 1.0.0
owner: Hermes (curator-managed)
risk_tier: low
floor_scope: [F1, F2, F6]
autonomy_tier: T1
tags: [form, application, submission, institutional, voice, receipt, principal]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Institutional Form & Application Filing

Trigger: the principal hands over — or points at — an official form, application, self-assessment,
career or placement declaration, licence/benefits application, or statutory submission that will be
filed **under his own name**. Also load when a form he already submitted comes back for correction.

Adjacent skills keep their own territory: artifact layout and reader-weighting live in
`human-facing-artifact-design`; producing the deliverable file lives in `forge-pdf-delivery`;
domain substance (employment separation, family law, claims) lives in its own advisory skill.
This skill owns only what is specific to *filing a form*.

## 1. Classify the instrument before drafting a word

- **Does it capture intent, or does it bind?** Find the sentence that says what happens next. A form
  that says *select this option and then submit officially with supporting information through the HR
  system* captures intent; the binding act is that later submission. State the difference to the
  principal explicitly — it is what makes answering honestly safe, and it is the difference between
  a reversible signal and an irreversible one.
- **Who actually reads it?** Frequently not the person who decides the terms. A form read by HR or
  an administrator is a different audience from a memo to the person who signs.
- **Is it reversible?** If yes, answer fully and honestly. If no, treat it as any other irreversible
  act and confirm the content and the identity before anything leaves.

## 2. Write it in the principal's own voice

- **Consultant register is the default failure.** Polished nominalisations — "my interest lies in
  specialist technical contribution", "I would value deepening specialist expertise" — read as written
  by someone else and come back as *make it human*. Write the plain version: short sentences, one idea
  per sentence, no veneer.
- **Fastest route to the right register: mirror a message he has already written** on the same
  subject. His own past prose is the calibration sample, and where he has supplied a line, use his
  line rather than a rewrite.
- **Offer both languages when his spoken register differs from the form's.** Serve the form's own
  language as the primary and the mirrored version beside it, and let him pick one. Never mix two
  languages inside a single field.
- **Match length to the field.** A long-text field rewards 100–150 words; an essay in it reads as
  volume rather than clarity.

## 3. Read the finished set as one document

- Every field is read beside the others. Read the completed set top to bottom, once, in the
  reviewer's order, before anything is submitted.
- **An aspiration that promises a long horizon beside an intent field registering a departure reads
  as indecision** — unless the aspiration itself places its horizon after the transition. One
  position stated twice in different fields is stronger than either field alone; two fields that
  disagree cost more than either answer.
- **Cross-reference an earlier written submission.** If a letter, note or justification on the same
  subject has already gone to somebody in the institution, have the form point at it and say the
  position is unchanged. Two documents that disagree cost the principal credibility with every reader
  who sees both.

## 4. Keep negotiation material out of the form

- Figures, comparisons, eligibility arguments, candidate dates and counting rules do not belong in a
  form read by people who are not the decision-makers on terms. They signal strategy and buy nothing.
- **Move them, do not delete them.** Put that material in a clearly separated section of the same
  deliverable, labelled as correspondence to send later, so nothing is lost and the form stays clean.
- **Check a lever is live before advising anyone to raise it in writing.** Where the planned outcome
  already sits past the threshold the lever keys off, raising it buys nothing and reads as
  calculation. Confirm the threshold has not already been cleared.

## 5. Answer a known weakness by adopting it

- Where the reviewer has already raised a gap in the record, name it first and convert it into
  something the principal wants to learn. Adopting the point closes it; defending it reopens it.
- **Invent nothing.** Only adopt a gap the record actually carries.
- **Use the field's own invitation.** If a field asks for personal considerations, state the real
  constraint in one plain line — a dependant, a distance, a limit. It is a fact, not a complaint, and
  the question was asked. State the constraint, never the story around it.

## 6. Never choose an open-ended option

Scan every option for unbounded commitment language: *and beyond where required*, *as long as needed*,
*ongoing*, *and any other duties as required*. Such an option is a standing commitment with no end
date. Where the real position is a bounded period plus a stated next step, select the bounded option —
and tell the principal why, in one line, so the choice is theirs to reverse.

## 7. Dates and facts on the document come only from the principal

- Never fill a date, reference number, employee or member number, job title, or start date **by
  inference** — not from the session date, not from when he pasted it, not from what is plausible.
  Leave it out, or ask. A settled-looking wrong field is wrong to the one reader holding the original.
- A delivered or filed copy **cannot be recalled** from a chat, an inbox, or a filing system. Getting
  the field right at build time is the cheap path; the repair is a second copy of a personal document
  in a place the principal reads on his phone.
- Where the form is transcribed from a document he supplied (an email, a letter, a receipt), the
  document's own date comes from his statement about it and from nowhere else.

## 8. Receipt discipline

- Have the principal export or screenshot the completed form **before** submitting, and the
  confirmation **after**. The institution's copy decides what was said; his copy is what lets him
  prove what he said.
- Record locally: the artifact and its hash, who submitted, through which channel, on what date. Keep
  the file at a stable path — an attachment not on disk cannot be re-sent.
- **Correcting after submission:** issue a new version with a short table of what changed and why, and
  say plainly which earlier submission it supersedes. Never a silent edit — a reader holding the
  earlier version cannot otherwise tell which document they are reading.
- If a field could not be determined, return it to the principal as a short confirm-list rather than
  shipping a plausible value.

## Pitfalls

- **Treating the form as the application, or the submission as a resignation.** They are separate
  instruments with separate consequence classes. Conflating them either overstates the commitment the
  principal has made or understates the decision he is taking.
- **Polishing toward corporate removes the only thing that made it his.** The consultant register is
  not a safer draft; it is a draft that gets sent back.
- **Writing the arithmetic into the form.** Tax, dates, counting rules and package comparisons belong
  in later written correspondence, once the terms exist.
- **Assuming the reviewer holds the context.** A form is read cold, by somebody who was not in the
  conversation. Anything that only makes sense with the surrounding story is written wrong.
- **Submitting without keeping a copy.** The version first filed is the version that governs.

---

*DITEMPA BUKAN DIBERI — the form is the record.*
