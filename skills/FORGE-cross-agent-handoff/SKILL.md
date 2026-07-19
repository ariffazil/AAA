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

---

## Context-Capture Governance (WAJIB 8 — added 2026-07-19)

Agents are already writing durable context artifacts: boot documents, NEXT_AGENT_INIT handoffs, canonical protocols, memory summaries, deprecation registries, instructions for future agents. The next agent inherits whatever the prior agent left. That is **policy mutation through documentation** unless governance is explicit.

### The defect (current state)

An agent can write a guidance document into a privileged initialization path (`NEXT_AGENT_INIT.md`, system prompt directory, canonical docs, memory bootstrap, agent definition) and the next agent treats it as if it were ratified policy. The current path has no provenance gate.

### Required separation: artifact classes

| Class | Meaning | Authority | Loaded as |
|---|---|---|---|
| `observation` | Evidence about current state | Append-only | Reference |
| `operational_handoff` | Temporary work continuation | Scoped, expiring | Reference |
| `guidance` | Non-binding recommendation | Agents may propose | Advisory |
| `policy` | Binding behavioral rule | Kernel-governed review | Binding |
| `constitution` | Changes authority or floors | F13 ratification | Binding |
| `memory` | Historical record | Append-only with provenance | Reference |

### Required `context_manifest` for every durable artifact

```yaml
context_manifest:
  artifact_id: <sha256-or-uuid>
  class: observation | operational_handoff | guidance | policy | constitution | memory
  author: <actor_id>
  source_commit: <git sha>
  authority_level: T1 | T2 | T3
  approved_by: <actor_id> | null
  binding: true | false
  created_at: <unix_ms>
  expires_at: <unix_ms> | null
  constitution_compatibility: <hash of current F1-F13 baseline>
  supersedes: [<artifact_id>, ...]
  content_hash: <sha256>
```

### Hard rules

- **Unapproved agent-authored material MUST load as advisory, never binding.**
- An agent MUST NOT be able to upgrade its own guidance into binding boot policy by placing it in a privileged initialization path.
- `class: policy` and `class: constitution` artifacts require `approved_by` ≠ null.
- Boot loading paths (`INIT`, `NEXT_AGENT_INIT`, system prompt directories, canonical docs, memory bootstrap, agent definitions) MUST be scanned for `class: policy | constitution` artifacts without `approved_by` → reject or quarantine.
- Supersession chain MUST be preserved (don't silently replace binding policy).

### Required boot context checks

Before loading any artifact into boot context:
1. Scan provenance (author, source commit, authority level)
2. Verify `class` matches the actual content intent (an "observation" cannot bind behavior)
3. Check `approved_by` for `class: policy | constitution`
4. Check `expires_at` — expired artifacts load as `observation` even if originally `policy`
5. Verify `constitution_compatibility` matches current F1-F13 baseline
6. Run injection-risk scan on content (template-tag detection, prompt-pattern detection)

### Authority scope

WAJIB 8 is **T2** — context-loader enforcement can be implemented as T1 (no F13 needed) because it operates on the loader, not the constitution. The `constitution` class artifacts still need F13; the loader just enforces the existing F13 path.
