---
name: grilling
id: grilling
version: 1.0.0
description: "Use when a plan, design, or decision is underspecified — interview the human one question at a time until every branch of the design tree is resolved. Trigger: 'grill me', 'stress-test this', 'what am I missing', 'before we build'."
owner: AAA/333-AGI
risk_tier: low
floor_scope: [F2, F4, F7, F13]
tags: [interview, planning, design, decision, pre-build]
---

# Grilling — resolve the design tree before the build

A user-invoked interview primitive. It does not plan, build, or decide for the human.
It asks until the plan has no unresolved branch that would change the build, then hands
the decision ledger to `writing-plans` / `AGI-plan-dag`.

**Trigger:** "grill me", "stress-test this", "what am I missing", "before we build",
or any plan where two competent engineers could build different things and both claim
they followed the brief.

## When NOT to use

- The decision is already measured or reversible and cheap — just do it.
- The gap is machine-answerable (file, config, live probe, repo history) — probe it, do not ask.
- The human is in a hurry and the decision is theirs alone — present the binary, not an interview.
- You are using questions to avoid work. A question must change a decision.

## The loop

1. **Name the artifact.** One sentence: what will exist after this work that does not exist now?
2. **Map the branches.** List the decisions that could change the artifact. Keep it private; do not dump it.
3. **Ask one question at a time.** Each question targets the branch with the highest consequence × uncertainty.
4. **Record the answer** in a decision ledger: `{decision, answer, consequence, reversible?}`.
5. **Stop** when no remaining branch changes the artifact, or the human says stop.
6. **Hand off** the ledger + unresolved unknowns. Do not start building inside the interview.

## Question classes (pick one per turn)

| Class | Ask | Why |
|---|---|---|
| Goal | "What must be true when this is done that is not true now?" | prevents proxy goals |
| Constraint | "What must not change?" | finds the real boundary |
| Failure | "What would make this a waste of your time?" | surfaces the acceptance test |
| Reversibility | "If this is wrong, how do we get back?" | sets the authority tier |
| Evidence | "What would you accept as proof?" | prevents narrative success |
| Human | "Who bears the cost if this fails?" | F6/F13 consequence check |
| Scope | "What are we explicitly NOT doing?" | kills scope drift |

## Rules

- **One question per turn.** A numbered questionnaire is a form, not a grilling.
- **Never ask what a machine can answer.** Probe first; ask only the human residue.
- **No permission requests.** "Shall I proceed?" is not a grilling question; it is a request to be managed.
- **No leading questions.** Offer the real branch, including the option that kills your preferred design.
- **Cap the loop.** 4–8 rounds. If a branch is still open after that, name it as an unknown and
  decide who owns it.
- **Preserve disagreement.** If the human contradicts an earlier answer, record both and ask which
  one wins; do not silently overwrite.

## Output shape

```
DECISION LEDGER
- D1 <decision> → <answer> | consequence: <...> | reversible: yes/no
- D2 ...
UNRESOLVED
- U1 <unknown> — owner: <human|agent|probe> — needed by: <date>
NEXT
- <writing-plans | AGI-plan-dag | probe | stop>
```

## Failure modes

- Turning the interview into a 20-question form (the human becomes a parser).
- Asking questions whose answers are already on disk.
- Asking "do you want A or B?" when the agent should recommend one.
- Starting implementation mid-interview, then asking forgiveness.
- Recording answers in chat only; the next session loses the ledger.

## Provenance

Adapted from `mattpocock/skills` `grilling` (MIT), re-authored for the arifOS federation:
one question per turn, machine-answerable questions are probed not asked, and the output
is a decision ledger handed to the existing planning owners — no second planner.
