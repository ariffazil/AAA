# Routine and Handoff Policy

> **DITEMPA BUKAN DIBERI** — *Forged, Not Given*

## Alignment with OpenAI Agents SDK
AAA implements `handoff` and `guardrail` primitives following the OpenAI Agents SDK patterns, but with constitutional gating.

## 1. Governed Handoffs (Layer 3)
A handoff (transfer) occurs when one agent determines that a task is better suited for a different tier (e.g., ASI → AGI).

- **Requirement**: Every handoff must carry a **Transfer Card**:
  - `source_agent`: Requesting agent.
  - `target_agent`: Receiving agent.
  - `reason`: Justification for transfer.
  - `context_snapshot_hash`: Merkle hash of current working memory.
- **Gate**: The `aaa-agent-registrar` must verify the receiving agent has the `identity_scope` for the task.

## 2. Guardrails as Humility Bands (Layer 2)
F7 Humility is operationalized through input/output guardrails:
- **Input Guardrail**: Prevent prompt-injection or unauthorized scope escalation.
- **Output Guardrail**: Ensure responses carry epistemic tags and respect F9 Anti-Hantu.

## 3. Routine-to-Seal
A **Routine** is a sequence of tool calls.
- **Rule**: Every routine sequence **must** terminate in a `999 SEAL`.
- **Checkpoint**: No routine may exceed 3 steps without an intermediate `888 AUDIT` if the risk tier is MEDIUM or higher.

---
**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
