---
name: retro
id: retro
version: 1.0.0
description: "Use after a completed unit of work — inspect the session evidence and improve the agent environment (navigation, checks, standards, steering files, tooling), most severe first, with one patch per finding. Trigger: 'retro', 'what should we improve', 'why was this slow', 'post-session'."
owner: AAA/333-AGI
risk_tier: low
floor_scope: [F2, F4, F7, F11]
tags: [retro, improvement, agent-environment, session, tooling]
---

# Retro — improve the environment, not the narrative

A retro is not a feelings report. It inspects the evidence of a completed unit and changes
the agent's working environment so the next unit is cheaper and less error-prone.

**Trigger:** "retro", "what should we improve", "why was this slow", "post-session",
"the agent kept stumbling", or immediately after a SEAL-grade unit closes.

## When NOT to use

- The unit is still running — finish it, then retro.
- The finding is a one-off human preference — record it in the person's lane, not the environment.
- The finding needs a constitutional change — route to F13, not a skill patch.
- You cannot name the evidence — do not invent a lesson.

## Evidence to gather (read-only)

1. **Session evidence:** tool calls that failed, retried, or were abandoned; files rewritten
   more than once; long gaps; context compactions.
2. **Git evidence:** diff size, reverted commits, files touched outside the declared scope.
3. **Queue evidence:** tasks opened/closed, blocked items, carry_forward entries.
4. **Human evidence:** what the human had to repeat, re-explain, or correct.

No evidence, no finding. A retro that starts from vibes is a diary.

## Classify every finding

| Class | Question | Typical fix |
|---|---|---|
| Navigation | Did the agent look in the wrong place? | pointer in AGENTS.md / index, not a new doc |
| Checks | Did a bad state pass a gate? | strengthen the existing test/gate |
| Standards | Did the agent do something the repo forbids? | one rule in the existing standard |
| Steering | Did the agent not know the priority? | patch the existing instruction fragment |
| Tooling | Did a tool fail or mislead? | fix the tool or its contract, not a wrapper |
| Human | Did the human become the bus? | remove the question, automate the relay |

## Procedure

1. **List findings with evidence.** Each row: finding → evidence → class → severity.
2. **Rank by cost × recurrence.** A one-off annoyance is not a fix; a repeated tax is.
3. **Propose the smallest patch per finding.** One owner, one file, one measurable change.
4. **Reject environment sprawl.** No new dashboard, registry, or ledger when a line in an
   existing file will do.
5. **Assign and schedule.** Put the patch in the existing queue (`/root/work/tasks.json`)
   with an owner and a deadline. Do not create a retro backlog file.
6. **Measure next unit.** Name the signal that will show the fix worked (fewer retries,
   fewer questions, faster path, zero gate misses).
7. **Close.** One paragraph: what changed, what will be measured, what was deliberately
   left alone.

## Output shape

```markdown
RETRO: <unit> — <date>
FINDINGS
1. <finding> | evidence: <path/probe> | class: <...> | severity: high/med/low
...
PATCHES
1. <file> — <change> — owner: <...> — measured by: <signal>
LEFT ALONE
- <finding> — reason: <one-off | no owner | F13-gated>
```

## Rules

- **No blame.** The finding is about the environment, not the person.
- **No retro theatre.** A retro that produces only prose has failed.
- **One patch per finding.** Bundling hides which change worked.
- **Do not rewrite history.** Supersede, do not erase the prior decision.
- **The human is not the backlog owner.** If a fix needs a human, name the decision and
  the default, not a standing request.

## Provenance

Adapted from `mattpocock/skills` `retro` (MIT), re-authored for arifOS: evidence-first,
environment classes, smallest patch per finding, and the existing tasks queue as the only
backlog.
