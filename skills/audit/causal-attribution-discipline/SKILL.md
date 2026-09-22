---
name: causal-attribution-discipline
description: "Use when asked WHY an event happened from indirect evidence."
version: 1.0.0
tags: [evidence, causation, attribution, forensics, witness]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Causal Attribution from Indirect Evidence

**Class of task:** someone asks "why did X happen / why is he like this / why did it fail" and the only evidence is an artifact trail — chat logs, timestamps, tickets, an unmeasured night, a business outcome. There is no instrument behind it. The deliverable is not a theory: it is a defensible statement of what the record supports, plus the ONE question that would collapse the remaining ambiguity.

Why this needs its own discipline: a plausible mechanism stated as fact gets acted on, and the moment it is falsified the reader stops trusting every later read from the same source. A confident wrong cause costs more than an honest "cannot tell from this".

Domain-specific reads live in their own skills (sleep phases, human state, relationship verdicts, service forensics) — this skill governs the reasoning that sits ABOVE them: which candidate causes the evidence is even allowed to carry.

## Procedure

1. **Fix the event and its clock first.** Name exactly what is being explained and pin the window (the night of A→B, the week of the failure, the run that died). Every candidate cause is tested against that window, so ambiguity here poisons everything downstream.
2. **Pull the record by identity + window, broadly.** Query by uid / chat_id / target + time range and print EVERY matching line. Keep the call **probe-led** — the execution gate exempts a `terminal` command only when it begins with a probe verb, so `grep -a '<uid>' <log>` passes and `cd … && grep` does not. Put topic keywords in your reasoning, not in the query. Mechanics, measured gate rule, and the log-shape traps (size-driven rotation, ledger staleness, masked senders, duplicate chat ids) are in `references/record-extraction-command-shape.md`.
3. **Enumerate candidates, then date-filter.** Require each candidate's timestamp to PRECEDE the event it is meant to explain. A stressor that surfaces the following day cannot explain last night. State which candidates you filtered — the filtered one is often what the asker had already privately settled on, and naming it is what makes the correction land.
4. **Separate baseline from delta.** Routine conditions are not causes. A substance taken daily, a workload that never changes, a chronic condition, a permanently broken process — that is the background. Only a CHANGE inside the window carries causal weight. "He uses X" is not evidence that X did it.
5. **Separate the clock from the content.** That someone was awake, active, or posting at a given hour proves the state at that hour; it does not prove the reason. Report both and label which is which.
6. **Say what the record cannot carry.** Any surviving candidate with no timestamp of its own is UNKNOWN, not implied. Name it unreadable rather than choosing the most narratively satisfying option.
7. **Close on the ONE discriminating question.** Where the branches differ in remedy (cannot start vs cannot stay; supply vs demand; voluntary vs forced), ask the question that splits them. One question, then stop — do not also ship an answer for every branch.

## Output contract

Three beats, in this order: **what the record shows** (facts, with hours) → **what it cannot show** (named plainly, out loud) → **the single question**. No tables, no mechanism asserted as fact, no numbered programme. Cap the epistemic status explicitly — this is read from what was written down, nothing more.

When the asker is emotionally invested, the witness posture governs the delivery (see `sovereign-worry-witness`, `loved-one-worry-support`); this skill only fixes the content.

## Pitfalls

- **Plausible ≠ supported.** The mechanism that best fits the story is the one most likely to be invented. Ground every step in a timestamp, or label it as your read. Falsified mechanism = the reader discounts your next five reads, not just this one.
- **Same-window tells are the symptom, not the reason.** "He was up late, so he slept badly" is circular and reads as analysis. A tell proves the state; it never explains itself.
- **Not-yet-happened causes.** A dispute, bill, diagnosis or decision that surfaces AFTER the event is context, never cause. Date-check candidates the asker volunteers too — instant agreement converts your read into their assumption with your signature on it.
- **Substance / single-factor fixation.** Naming one input (a supplement, a migration, a staff member) as the cause requires its timing to fall inside the window AND to differ from baseline. Otherwise it is context.
- **Mechanism when the ask was for answer.** If the question has a factual part (was he awake? did the job run? when?), answer that in the first line. The mechanism is at most a labelled read, and often should be withheld until the discriminating question is answered.
- **The artifact trail is not the deliverable.** A long forensic dump about a person or a bond lands as callous; about a system it buries the finding. Facts in, posture out, stop.

DITEMPA BUKAN DIBERI ⚒️
