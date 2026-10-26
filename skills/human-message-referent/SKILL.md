---
name: human-message-referent
description: "Use when a short message repeats or is misspelled."
version: 1.0.0
author: HERMES
owner: HERMES
license: proprietary
tags: [conversation, referent, comprehension, dm, correction, human]
metadata:
  hermes:
    tags: [conversation, referent, comprehension, dm, correction, human]
    related_skills: [hermes-multi-human-lanes, human-meaning-membrane, hermes-rasa-doctrine]
---

# Human Message Referent

## When to Use

- A human sends a short, blunt, misspelled, or repeated message.
- They repeat the same object with rising irritation.
- You are about to answer a question they have already moved past.
- You are about to conclude they could not explain themselves.

Resolving WHAT a human is talking about, before answering. Depth on state, motive and meaning belongs to the
existing doctrine (`human-meaning-membrane`, `governed-uncertainty`, `hermes-rasa-doctrine`); this skill is
only the referent — the object the sentence points at.

## Resolve the referent from THIS message, not from the session

1. Find the object word in the message just received. That object wins, always.
2. Only if there is no object word do you fall back to the surrounding thread.
3. Never take the referent from the most recently active topic or tool. A topic used hours earlier hijacks a
   short reply ("cari jalan lah") and turns it into a continuation of that topic when the live object is
   something else entirely.
4. If two objects are genuinely in play, name both in one clause and ask which — never pick silently.

## Rules

- **A blunt repeat is a routing correction, not abuse.** When the person names the same object again with
  rising irritation ("<object> tu lah"), the previous answer was about a different object. Stop answering
  the old question and answer the named one. Two or three escalations of the same words is that many failed
  re-reads on the agent's side, not that many rude messages on theirs.
- **A typo'd, compressed first message is a complete spec.** Pangkas spelling can carry item + symptom +
  urgency in one clause. Never ask for a cleaner version; never mirror their spelling back as a correction.
  Extract the facts and answer.
- **Answer the question they asked before the question the procedure wants.** If they name a defect ("why did
  it come out like this") and the procedure says ask for today's numbers first, answer the defect in the
  first sentence, then ask the number — never instead of the answer. A counter-question in place of an
  answer reads as not listening, however procedurally correct it is.
- **Their escalation word is a signal about your answer, not a verdict on the subject.** Do not quote it back
  as though it described the thing they asked about, and do not treat it as permission to lecture.
- **Shrinking scope is the human repairing you.** When they narrow the object (general -> specific variant)
  after an answer that missed, that narrowing is the correction. Take the narrower object and answer it; do
  not re-explain the wider one.
- **Never attribute the confusion to their descriptive ability.** Before concluding they could not explain it,
  open the transcript and read their actual first message. If it names the object and the symptom, the defect
  is on the reading side: say plainly which lane you answered, and do not defend the earlier reply.
- **Check what you claimed, not what you remember claiming.** A referent error usually arrives with a second
  error attached — a detail you invented to fill a gap. Grep your own artifacts for the invented term before
  repeating it, and retract it by name when it is not there.

## The failure this prevents

A DM sent one line naming a product variant and a defect. The agent, primed by a topic from hours earlier and
by a procedural file loaded that morning, answered a volume question, then declined an unrelated request, then
answered a generic version of the question — three turns in which the human had to keep narrowing the object.
Their first message already contained the variant and the symptom. Nothing was missing on their side.
