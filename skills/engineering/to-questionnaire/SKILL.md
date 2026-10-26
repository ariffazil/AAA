---
name: to-questionnaire
id: to-questionnaire
version: 1.0.0
description: "Use when a decision needs one specific person's input but they are not in the room — turn it into a short async Markdown questionnaire with context, options, deadline, and a default. Trigger: 'ask them', 'need X's call', 'questionnaire', 'decision I cannot make alone'."
owner: AAA/333-AGI
risk_tier: low
floor_scope: [F2, F4, F6, F13]
tags: [questionnaire, async, decision, human, handoff]
---

# To questionnaire — one decision, one person, one page

A decision that needs a human should not become a chat interrogation. This skill turns
the decision into a compact Markdown questionnaire the person can answer asynchronously.

**Trigger:** "ask them", "need X's call", "questionnaire", "decision I cannot make alone",
"send this to the client/doctor/lawyer/Arif", or any decision where the agent lacks the
authority or the facts.

## When NOT to use

- The decision is machine-answerable — probe the file, config, or live system.
- The decision is yours to make under existing authority — decide it, do not outsource.
- The person is not the decision owner — find the owner first.
- A single yes/no is enough — send a one-line binary, not a questionnaire.

## Procedure

1. **Name the decision in one sentence.** "Should we do X, given Y, by Z?"
2. **Name the one person** who can answer it, and why them. If there are two, split into
   two questionnaires or get one owner.
3. **State the context the person needs** — facts only, no persuasion. Include the cost of
   waiting and what happens if they do not answer by the deadline.
4. **Write 5–12 questions, max.** Each question must change the decision. For each:
   - the question in plain language;
   - 2–4 concrete options, including "none of these";
   - one optional free-text line;
   - the consequence of each option, in one clause.
5. **Set a deadline and a default.** "If no answer by <date>, we proceed with <default>
   because <reason>." A questionnaire without a default is a blocker.
6. **Deliver as one Markdown block** the person can reply to inline. No forms, no portals,
   no attachments unless the decision needs them.
7. **Close the loop.** Record the answer, the date, and the decision in the existing
   decision ledger / carry_forward. Do not leave it in chat only.

## Output shape

```markdown
# Decision needed: <one sentence>
**For:** <person> · **By:** <date> · **Default if silent:** <default>

## Context
<3–6 facts, each with a source or "unknown">

## Questions
1. <question>
   - A) <option> — <consequence>
   - B) <option> — <consequence>
   - C) None of these — <what happens>
   - Notes: ___________

...

## What I need back
Reply inline with the numbers (e.g. `1A 2B 3C`) plus any notes.
```

## Rules

- **One decision per questionnaire.** Two decisions means two documents.
- **No leading options.** Include the option that kills your preferred plan.
- **No question the agent can answer.** Probe first; ask only the human residue.
- **Never leak another person's private data** to make the question concrete.
- **No second ledger.** The answer goes into the existing carry_forward / tasks SOT.
- **Silence is data, not consent.** The default is declared in advance, not inferred later.

## Provenance

Adapted from `mattpocock/skills` `to-questionnaire` (MIT), re-authored for arifOS: one
decision, one owner, a declared default, and the answer recorded in the existing ledger.
