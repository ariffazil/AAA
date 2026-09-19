---
name: human-response-witness
description: "Use when reading a third party's reply to Arif's message."
version: 1.0.0
author: Hermes
license: arifOS internal
tags: [witness, human-interface, screenshots, rasa, evidence, review]
triggers:
  - "what will he feel when he reads this"
  - "describe the reality that happened here"
  - "tersurat dan tersirat"
  - "he replied — expand"
  - Arif pastes a chat screenshot of his conversation with a third party
  - Arif relays an emoji reaction in place of a reply
---

# Human Response Witness

Arif relays a third party's response to something he sent — usually a screenshot plus a claimed
reaction, sometimes only "dia bagi emoji 😢". He then asks one of two things: what the other person
feels, or for an account of what happened *tersurat dan tersirat*. That is a **witness task, not a
production task**: the deliverable is an accurate account, never a next action or a new artifact.

Doctrine siblings (load them; they are authoritative on the underlying epistemics):
`governed-uncertainty`, `hermes-rasa`, `relationship-kernel`, `wisdom-letter-for-loved-ones`.
This skill governs the *procedure for the account itself*.

## Procedure

### 1. Transcribe before interpreting — from the image, not from memory

Read the screenshot with a vision pass that returns every bubble in order: sender side, timestamp,
forward arrows, reply-quote context, reactions. Ask for verbatim text explicitly — a summary
silently destroys the evidence you were asked to weigh.

Record these before any interpretation:
- **Bubble direction.** If every bubble is outgoing, there are no utterances from the other person.
- **Reactions and their anchors.** An emoji is attached to a *specific message*, not to the person
  or the conversation. Which bubble carries it is the datum.
- **Timestamps.** Gaps and order carry information; a ten-minute pause is not the same as a reply.
- **What is cut off.** Header-clipped bubbles, missing earlier context, the other side of the thread.

### 2. Two labelled halves — record first, reading second, never interleaved

Arif's ask "tersurat dan tersirat" is a format request. Honour it literally:

1. **Tersurat** — the literal sequence, timestamped, quoted. Evidence only; a reader should be able
   to reconstruct the exchange from this half alone.
2. **Tersirat** — the reading. Open it by stating it is a reading and not a fact, and keep every
   sentence falsifiable by the person it describes.

Interpretation placed inside the record destroys the record. If a sentence cannot stay free of
inference in the first half, it belongs in the second.

### 3. Declare the visibility limit inside the account

One-sided screenshots are the norm. Say so in the account itself: which side you can see, which you
cannot, and therefore which conclusions are simply unavailable. Also mark any claim that rests on
Arif's own report of a reaction rather than on the screenshot.

### 4. Probe the falsifiable parts instead of hedging

Some claims in the account are cheap to test. Test them:
- **Is this artifact published?** Before treating any document as public, prove it is a route. On an
  SPA host every unknown path returns HTTP 200 with identical shell bytes, so status code and size
  prove nothing about existence. Use byte-identity against a known-absent path, and grep the hashed
  JS bundle (`curl -s <site>/ | grep -o '/assets/[^"]*\.js'`, then search the bundle for a unique
  slug or content string). Content absent from both the bundle and any static route is not published.
- **What time is it?** Screenshot timestamps are past tense; "now" must be verified, never inferred.
- **Is a later message present?** Do not announce an absence without looking.

Deployment and site detail belong to the site-ops skill; this step exists because the result belongs
in the account as a checked fact.

### 5. Retract explicitly — do not quietly revise

When a later screenshot or message contradicts a reading you already gave, open the next reply with
the correction: one line, unhedged, then the updated account. Folding new evidence in silently is
the same failure as the original wrong read, with better manners. New evidence is the only thing
that moves a human-state claim upward; the retraction is what makes the next account trustworthy.

### 6. When the same artifact arrives twice, diff it before reading either

A resend with a `(2)` suffix is usually a deliberate edit, not a re-export. Extract the text from
both and diff before commenting:

```python
import pymupdf, difflib
a = '\n'.join(p.get_text() for p in pymupdf.open('v1.pdf'))
b = '\n'.join(p.get_text() for p in pymupdf.open('v2.pdf'))
print('\n'.join(difflib.unified_diff(a.split('\n'), b.split('\n'), lineterm='', n=0)))
```

Report the delta and which direction it moved — a changed line is the intent. Do not re-read the
whole artifact as new, and do not report the unchanged remainder as findings.

### 7. What to advise once it has been read

- **An emoji-only reply is a complete reply.** Minimal is not reduced. A written sentence is a
  commitment the sender cannot withdraw; an emoji is not. Do not describe it as partial.
- **Never advise Arif to ask "are you ok?"** It forces the other person to choose between an honest
  answer and a safe one. Both are expensive, and the cost lands on them.
- **Recipients answer one line of a long message** — usually the line that was about the writer, not
  the one about themselves. Silence on the rest is not rejection; do not read unmentioned sections
  as refused.
- **A reply that redirects to a third person may be the artifact working.** When the reader turns
  toward someone else (a parent, a sibling, a call the writer has been avoiding), name it as the
  outcome rather than as deflection.
- **No second artifact.** Once something has landed, the next message should be shorter, not longer.
  Offering a follow-up letter converts care into pressure.
- **Close on what is still open and who owns it.** The open item is usually on Arif's side; state it
  plainly and stop. Do not manufacture a next step.

## Pitfalls

- **Do not answer the literal question "what will he feel" with a feeling.** Answer with what the
  artifact does, what is on record, and what remains unavailable. A named emotion is a fabrication
  with a name.
- **Do not let the artifact's framing pass unexamined.** If a letter says it knows the recipient
  because the writer told its author about them, then the recipient received the writer's view of
  themselves, not an independent witness. Say that once, as a property, not as a fault.
- **Do not unsource a specific figure.** A number in a personal artifact (an amount, a frequency, a
  time) is either traceable to something the person actually said, or it reads as surveillance
  instead of attention. Flag it; the fix is upstream.
- **Do not treat silence as a reply.** A person who said nothing said nothing. Reading the silence as
  disappointment, approval, or understanding is fabrication with extra steps.
- **Do not turn the account into a diagnosis.** Describe conduct and evidence. The interior belongs
  to the person, and a named UNKNOWN class is a valid output of this task.
- **Do not persist the personal content.** The exchange is STORY-class: it stays in the reply, never
  in agent memory, session harvest, or a skill. If a durable fact is needed, keep only the MAP-level
  operational rule.
