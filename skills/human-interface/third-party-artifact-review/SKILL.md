---
name: third-party-artifact-review
description: "Use when reviewing a letter about a person before it goes."
version: 1.0.0
owner: curator
risk_tier: medium
floor_scope: [F1, F2, F4, F6, F9, F13]
triggers:
  - "what will X feel when he reads this"
  - "how will he read this"
  - "review this letter / PDF before I send it"
  - "is this OK to send to him"
  - "someone wrote this about a person"
  - "artifact addressed to a third party"
  - "a letter I wrote for [name]"
tags: [human-interface, artifact-review, provenance, delivery-state, rasa, third-party]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Third-Party Artifact Review

A class of task where the human hands you a document **addressed to or about a person who is not in the
room** (a letter, a nasihat PDF, a dossier, a profile, a deck about someone, a message being relayed)
and asks a question about its human impact — typically *"what will he feel when he reads this?"*

That question looks like a state read. It is not. The person is absent: no self-report channel exists,
nothing they say can correct you, nobody can falsify the answer. **The analysable object is the
artifact and its delivery state — never the absent person's interior.** Move the analysis there, and
the reply becomes checkable, useful, and honest.

## Procedure

Run these in order. Each step can end the task on its own.

### 1. Extract the artifact, and diff every version you were given

Get the real text out before reacting to it (see `references/delivery-state-probe.md` for the exact
commands). When two files share a title, they are almost always two drafts — diff the extracted text
and report the delta. The author's real decision lives in the delta, not in either version.

### 2. Establish delivery state BEFORE discussing impact

```
PRODUCED ≠ SENT ≠ DELIVERED ≠ READ
```

Probe the transport lane for an actual receipt to the recipient's address (recipe in the references
file). An artifact that has not left yet makes the whole turn a **decision still open**, not a
consequence already running — and saying that plainly is frequently the single most useful sentence in
the reply, because the human believes they are asking about the future while you are about to describe
one.

Never let the conversation slide from *"he will feel X"* to *"he felt X"* without a delivery receipt in
hand.

### 3. Read the provenance sentences separately from the tender ones

Artifacts in this class carry an origin line — *"I know you because [X] told me about you"* — and that
line is where the document stops being about the recipient. It tells the reader:

- who the author's source about them is,
- which of their private material was shared, and with whom,
- that they were described before they were addressed.

The reader meets that before the tenderness lands. Soft sentences built from someone else's account
still read as *"I became material"*. Warn on the source line, not on the tone, and do not let the
warmth of the prose talk you out of the observation.

### 4. Check every figure and private detail against the recipient's own words

A number, date, or habit the recipient never said out loud reads as **being watched**, not as being
known — and one wrong detail can close an otherwise careful document. Ask where each specific came
from: the recipient's own self-report, or a third party's account. The distinction is the difference
between witness and surveillance, and it is the thing the recipient computes first.

### 5. Give the impact reading — as a reading

Only now. Use the modes and hedging from the state-reading doctrine (`governed-uncertainty`,
`hermes-rasa`): bounded alternatives, named unknowns, no verdict on an absent person. Also report what
the artifact **asks** versus what it **gives** — a document that ends needing attention, reassurance,
or permission from the reader reverses the gift.

### 6. Offer the repair as a judgment, never as an edit

When the artifact is good and the provenance is undisclosed, the standard repair is a short
**sender-authored cover note** ahead of the file: who wrote it, whose closing line is whose, and
explicit permission not to reply. Two lines, in the sender's voice, sent by the sender.

Name it and offer it. Do not alter, soften, or withhold the artifact behind the author's back — the
artifact is theirs, and the decision to send is theirs.

## Pitfalls

- **Don't predict the absent person's interior.** You cannot see them, they cannot correct you, and a
  confident portrait is unfalsifiable. Analyse the artifact, the provenance, and the delivery state.
  Leave the human room to be the authority on himself.
- **Don't read a file title as its audience.** A document named for someone may be addressed to
  someone else entirely, may never have been sent, and may exist in several drafts with different
  endings. Extract the text and check the lane before reasoning from the name.
- **Don't treat tenderness as consent.** A warm, careful, non-judgemental document can still be built
  out of material the recipient never offered. Tone and provenance are independent axes.
- **Don't skip the delivery probe because the answer seems obvious.** Authors routinely assume they
  have sent something; the log knows.
- **Don't quote the artifact back as evidence of the human's motives.** The document is the author's
  construction, not the recipient's state.
- **Don't report a negative as a finding.** "No record of a send" needs the same warrant as a positive:
  name the lane searched and the window searched, and stop at `UNKNOWN — cannot witness`.

## Companion skills

Read for depth when the situation needs it (these are user-owned — read, do not edit):

- `governed-uncertainty` — state reads, ambiguity-bearing, the "why" question classifier.
- `hermes-rasa` — provenance classes (O/S/R/I/F/C), qualia caps, prohibited collapses.
- `wisdom-letter-for-loved-ones` — how such letters are authored, and the anchors they must keep.
- `third-party-advisory-doc` — procedural documents for a third party.
- `bridge-protocol` — the register/send gate the final reply must pass.

## Support files

- `references/delivery-state-probe.md` — extraction commands, version diffing, and how to read a
  transport log for a real send receipt.
