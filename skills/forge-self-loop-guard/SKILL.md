---
name: forge-self-loop-guard
description: Recovery when delegate_task returns loop_subagent_cap.
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Self-Loop Guard - delegate_task runaway recovery

Use when a `delegate_task` call returns the loop_subagent_cap guardrail, error code with text "Blocked: this turn has already spawned N subagents (limit 50)". Do not retry the same call.

## What triggered this

Repeated `delegate_task` invocations in a single turn, where cumulative attempts including rejected malformed-schema and timeout variants crossed the kernel 50-cap. The guard fires once crossed. Further attempts return guardrail blocking_tool_calls rather than spawning.

## Recovery steps

1. Stop calling `delegate_task` for the rest of the turn.
2. Switch strategy. Do the work inline via read_file, write_file, terminal, execute_code. Those do not count against the subagent cap.
3. State the situation plainly to the user. Phrase it as "agent spawn halted by guardrail, working with what I have" rather than pretending the agent succeeded.
4. If the user explicitly requests a fresh subagent attempt, that means a new turn. Wait for the next turn. Cap resets per turn.
5. Do not try to consume the cap by spawning more before the user replies. The cap counts cumulative attempts, not cumulative spawned.

## Dont do this

- Do not retry `delegate_task` with the same arguments.
- Do not rebuild the schema hoping the guard misses a malformed payload. The guard fires on count, not validity.
- Do not fabricate "agent completed task X" output for subagents that never actually ran.
- Do not surface the cap as the user fault. It is our retry loop, not theirs.

## Subagent-cap as reality signal

If you reach this skill, the turn has a deeper problem. Either the task was wrongly chunked into parallel subagents, or reasoning was looping without progress. After recovery, write down what should have been a single serial call.

Provenance: 2026-09-23 05:43 MYT, Hermes session with Arif. 57 cumulative attempts hit cap. Pivoted to inline terminal and read_file work, stated limitation plainly to user.
