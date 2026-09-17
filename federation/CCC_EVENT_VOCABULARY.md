# CCC Event Vocabulary — Provider-Neutral Federation Event Schema

> **Status:** F13_OBSERVED (2026-09-18) — forged from ChatGPT Deep Research contrast.
> **Binding:** All A2A task exchanges between CCC workers and AAA/FED.
> **Grounding:** A2A v1.0 task/message/artifact semantics · arifFlow receipt chain · state-transition-discipline.md.

## The Law

Raw proprietary transcripts must NOT be routed through the federation. They contain secrets, vendor reasoning, and provider-specific formats. All inter-agent task exchanges must use this normalized event vocabulary.

## Event Vocabulary

```
TASK_ACCEPTED      — Agent acknowledges task assignment
PLAN               — Agent produces execution plan
TOOL_REQUESTED     — Agent requests tool invocation
TOOL_DENIED        — Tool invocation blocked by policy
FILE_READ          — Agent reads a file (with path hash, not content)
PATCH_PROPOSED     — Agent proposes code changes (diff hash)
COMMAND_EXECUTED   — Agent runs a command (command hash, exit code)
TEST_RESULT        — Test execution outcome (pass/fail + count)
REVIEW_FINDING     — Reviewer identifies issue (severity + location)
ARTIFACT           — Agent produces deliverable (type + hash)
TASK_COMPLETED     — Agent declares task done (with evidence refs)
TASK_FAILED        — Agent declares task failed (with failure reason)
```

## Event Envelope

```json
{
  "event": "TASK_ACCEPTED",
  "task_id": "tsk_...",
  "agent_profile": "qwen-code@0.24.0+glm-5.3",
  "timestamp": "2026-09-18T...",
  "trace_id": "...",
  "payload": {}
}
```

## What This Prevents

| Problem | How the vocabulary fixes it |
|---|---|
| Raw transcript leakage | Events carry hashes, not content |
| Vendor-specific format coupling | Provider-neutral vocabulary |
| Secret exposure | No raw text in events, only hashes and structured metadata |
| Model identity confusion | `agent_profile` field in every event |
| Transition lies | Each event is a specific state transition, not a Boolean |

## State-Transition Grounding

Per state-transition-discipline.md: "PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ ACKNOWLEDGED"

The event vocabulary maps to these transitions:
- `TASK_ACCEPTED` = acknowledgment of receipt
- `PLAN` through `ARTIFACT` = production chain
- `TASK_COMPLETED` = delivered (not yet verified)
- arifFlow receipt = observed
- VAULT999 seal = acknowledged

## Usage

1. CCC workers emit events to arifFlow on every significant state transition
2. AAA/FED consume events for routing and telemetry
3. Raw transcripts stay local to the agent's workspace
4. Only events (with hashes) cross federation boundaries

DITEMPA BUKAN DIBERI ⚒️
