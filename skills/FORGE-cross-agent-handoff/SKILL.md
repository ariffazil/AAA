---
name: FORGE-cross-agent-handoff
description: >
  Structured handoff protocol between federation agents. Packages task context,
  evidence, floor state, and provenance into a transferable artifact. Prevents
  context loss during agent transitions. USE WHEN: "hand off to", "transfer task",
  "escalate to agent", "delegate to".
version: 1.0.0
tags: [handoff, a2a, protocol, delegation, F1, F11]
floor_scope: [F01, F04, F11]
---

# FORGE-cross-agent-handoff

## Purpose
When Agent A cannot complete a task and must transfer to Agent B, context is lost. This skill packages the full task state into a structured handoff artifact that preserves:
- Original task intent and constraints
- Evidence gathered so far (with epistemic labels)
- Floor state (which floors have been checked, which pending)
- Reasoning chain (what was tried, what failed, what's next)
- Provenance (who touched what, when)

## Handoff Artifact Schema
```json
{
  "handoff_id": "uuid",
  "from_agent": "agent-id",
  "to_agent": "agent-id",
  "task_intent": "original user request",
  "constraints": ["F1", "F2", ...],
  "evidence": [{"source": "...", "rung": "OBS|DER|INT|SPEC", "confidence": 0.0-1.0}],
  "reasoning_chain": [{"step": 1, "action": "...", "result": "...", "status": "done|failed|pending"}],
  "floor_state": {"F01": "PASS", "F02": "CHECKING", ...},
  "provenance": [{"agent": "...", "action": "...", "timestamp": "..."}],
  "next_actions": ["action1", "action2"],
  "escalation_note": "why handoff was needed"
}
```

## Handoff Rules
- F1 AMANAH: Handoff must be reversible. Receiving agent can reject.
- F4 CLARITY: Handoff artifact must reduce entropy, not increase it.
- F11 AUDITABILITY: Full provenance chain required.
- Receiving agent must ACK handoff within 10s or escalate.

## A2A Transport
Handoff artifact is sent via `tasks/send` with `handoff=true` metadata.
Receiving agent runs `handoff-verify` before accepting task ownership.
