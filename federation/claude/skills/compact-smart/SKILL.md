---
name: compact-smart
description: Intelligently compact context while preserving constitutional knowledge and active task state
user-invocable: true
---

# Smart Compaction

Optimize context window usage while preserving essential knowledge.

## Invocation

- `/compact-smart` — Assess and compact with constitutional preservation
- `/compact-smart [focus]` — Compact with specific focus area

## When to Trigger

- Context exceeds 60% usage
- Before starting deep reasoning or complex implementation
- After completing a major feature or task
- Before running `/session-seal`

## Execution Steps

1. **Assess current state**: Tell the user the approximate conversation length and density.

2. **Identify what to compact** (safe to summarize/drop):
   - Old tool outputs and file reads no longer relevant
   - Verbose error messages (keep only root cause)
   - Exploratory searches that didn't yield results
   - Redundant explanations already captured in code

3. **Identify what to NEVER compact** (preserve always):
   - Constitutional floor definitions and governance rules
   - Active task requirements and acceptance criteria
   - Recent user decisions and preferences
   - Unresolved questions or blockers
   - File paths and architecture context for current work

4. **Execute compaction**: Run `/compact` with a focus prompt:
   - Default: `/compact "Preserve: constitutional governance, active tasks, user decisions, file paths. Summarize: old tool outputs, resolved errors, exploration results."`
   - With user focus: `/compact "Focus on [user's focus]. Preserve constitutional governance and active task context."`

5. **Confirm** to user what was preserved and what was compacted.

## Constitutional Alignment

- **F4 (delta-S)**: Compaction reduces entropy, increases clarity
- **F1 (Amanah)**: Essential knowledge preserved, nothing lost silently
- **F7 (Humility)**: Acknowledging context limits is honest
