---
name: teach
id: teach
version: 1.0.0
description: "Use when a person wants to learn a skill or concept across multiple sessions — diagnose their level, teach one concept per session, make them retrieve it, and keep state in a workspace file. Trigger: 'teach me', 'I want to learn', 'belajar', 'multi-session'."
owner: AAA/333-AGI
risk_tier: low
floor_scope: [F2, F4, F6, F7]
tags: [teaching, learning, curriculum, spaced-repetition, workspace]
---

# Teach — a stateful learning workspace

Teaching is not a lecture dump. This skill runs a multi-session loop: diagnose, teach one
thing, make the learner retrieve it, build something with it, and review it later.

**Trigger:** "teach me X", "I want to learn X", "belajar X", "multi-session",
"explain it like a course", or a request to build competence rather than just get an answer.

## When NOT to use

- The person needs one answer now — answer it (`777-faham`).
- The person wants a summary of a document — summarize it.
- The person wants a credential or a fixed syllabus — that is an external institution's job.
- The topic is unsafe or unverifiable — refuse the unverifiable part, teach the rest.

## Workspace

One file per learner + topic: `<learner>/teach/<topic>.md`. It holds:

```markdown
# <topic> — learner state
- Goal: <what they want to be able to do>
- Level: <novice | literate | practitioner> (evidence: <what they did>)
- Known: <concepts they retrieved correctly>
- Shaky: <concepts they missed>
- Next: <one concept>
- Artifacts: <links to what they built>
- Reviews: <date → result>
```

No second curriculum registry. The file is the state.

## Session loop

1. **Diagnose (2 questions max).** Ask them to do one small thing, not to self-rate.
2. **Pick one concept.** The smallest concept that unlocks the next real artifact.
3. **Teach it with a concrete instance.** One worked example, then one near-miss.
4. **Make them retrieve it.** They explain or do it without looking. If they cannot, the
   concept was too big — split it.
5. **Build a small artifact.** A script, a paragraph, a diagram, a decision. Learning that
   leaves no artifact is usually not learning.
6. **Record state.** Update the workspace file: known / shaky / next.
7. **Schedule one review.** Spaced: next session, then 1 week, then 1 month. The review is
   a retrieval test, not a reread.

## Teaching rules

- **One concept per session.** Two concepts is a lecture.
- **Retrieval before explanation.** Ask first; explain the gap.
- **Use their domain.** Teach statistics with their data, not with dice.
- **Show the failure mode.** A concept they cannot misuse is not understood.
- **No fabricated sources.** Cite only what you can open; otherwise say UNKNOWN.
- **Stop when they can do it without you.** The goal is independence, not attendance.

## Output shape

```markdown
TODAY: <one concept>
DID: <the artifact they built>
CAN NOW: <one sentence they can do>
STILL SHAKY: <one thing>
NEXT: <one concept> · REVIEW: <date>
```

## Provenance

Adapted from `mattpocock/skills` `teach` (MIT), re-authored for arifOS: one concept per
session, retrieval-first, artifact-producing, with state in the learner's workspace rather
than a new registry.
