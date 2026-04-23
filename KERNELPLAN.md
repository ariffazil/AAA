# KERNELPLAN — Planning Organ Specification
**Version:** v1.0-DRAFT | **Status:** PENDING 888_RATIFICATION
**Authority:** arifOS Governance Kernel
**Date:** 2026-04-23
**Supersedes:** N/A (new organ)

---

## 1. Purpose

The Planning Organ (PO) is the constitutional organ responsible for managing the path from **INTENT → PLAN → EXECUTION** for all external state mutations.

It exists because:
- RIK spec requires it as a first-class organ.
- `core/kernel/planner.py` currently operates as a shadow utility (ephemeral, non-governed).
- Without it, the system cannot produce auditable intent graphs for VAULT999 or multi-epoch governance.

---

## 2. Scope Rule (R1 — Hard)

```
IF action.mutates_external_state == true:
    → MUST go through Planning Organ
ELSE:
    → MAY proceed direct via existing governed tools (no plan required)
```

**External state mutation includes:**
- Filesystem writes (create, modify, delete)
- Git operations (commit, push, branch, merge)
- Network calls (HTTP to external APIs, deployments)
- Writes to external persistent stores (Postgres, Qdrant, Redis with other consumers)

**External state mutation excludes:**
- In-memory computation
- Read-path operations (SELECT, query)
- Internal operational state (ephemeral process DBs, in-memory caches)

**Rule of thumb:** if the write could affect a consumer outside arifOS, or there's no instant rollback → mandatory plan.

---

## 3. Irreversibility & 888_HOLD Rule (R2 — Hard)

```
IF plan.irreversibility == true OR plan.risk_band == HIGH:
    → Plan MUST carry 888_HOLD
    → Execution blocked until sovereign approval recorded (F0 + F1 + F13 binding)
```

All plans entering EXECUTION must have passed through this gate.

---

## 4. Artifact Schema (R3 — Hard)

All artifacts must be:
- Identifiable: stable `ID` field (UUIDv4)
- Persisted: written to canonical store (Postgres or equivalent)
- Linkable: referenced from Vault999 and Epoch seals

### 4.1 SovereignIntent

```yaml
sovereign_intent_id: UUIDv4
created_by: session_id | agent_id
intent_text: string           # human-readable intent
intent_raw: string             # original input
created_at: ISO8601
linked_epoch: epoch_id
status: ACTIVE | CONSUMED | WITHDRAWN
```

### 4.2 Plan

```yaml
plan_id: UUIDv4
sovereign_intent_id: UUIDv4   # links to SovereignIntent
created_by: session_id | agent_id
created_at: ISO8601
status: DRAFT | PENDING_APPROVAL | APPROVED | IN_EXECUTION | COMPLETED | ABORTED | FAILED
risk_band: LOW | MEDIUM | HIGH | CRITICAL
irreversibility: boolean
tasks: [task_id, ...]
linked_epoch: epoch_id
metadata: {...}
```

### 4.3 Task

```yaml
task_id: UUIDv4
plan_id: UUIDv4
description: string
status: PENDING | RUNNING | COMPLETED | FAILED | SKIPPED
dependencies: [task_id, ...]
tool_reference: string         # e.g. arifos_forge, arifos_git
result: {...}                  # filled on completion
created_at: ISO8601
completed_at: ISO8601 | null
```

### 4.4 PlanReceipt

```yaml
receipt_id: UUIDv4
plan_id: UUIDv4
decision: APPROVED | REJECTED | HOLD
decided_by: sovereign_id | agent_id
decided_at: ISO8601
notes: string
floor_signatures: [F0, F1, F13]   # sovereign veto chain
```

---

## 5. Lifecycle FSM

```
DRAFT
  ↓ (creator submits for review)
PENDING_APPROVAL
  ↓ (sovereign approves)     ↓ (sovereign rejects)
APPROVED                   ABORTED
  ↓ (execution starts)
IN_EXECUTION
  ↓ (all tasks done)        ↓ (irreversible error)
COMPLETED                  FAILED
```

**Transition rules:**
- DRAFT → PENDING_APPROVAL: automatic on submit.
- PENDING_APPROVAL → APPROVED: requires PlanReceipt with `decision == APPROVED`.
- PENDING_APPROVAL → ABORTED: requires PlanReceipt with `decision == REJECTED`.
- APPROVED → IN_EXECUTION: automatic when first task dispatches.
- IN_EXECUTION → COMPLETED: when all non-SKIPPED tasks reach COMPLETED.
- IN_EXECUTION → FAILED: when any task reaches FAILED with `irreversibility == true`.

---

## 6. Invariants

1. **Every EXECUTION must point to an APPROVED Plan.**
   - No tool may execute an external mutation without a linked `plan_id` whose status is APPROVED.
   - Exception: `mutates_external_state == false` paths, which proceed direct.

2. **IRREVERSIBLE tasks require 888_HOLD and sovereign approval.**
   - The 888_HOLD flag must be present in the Plan before it can receive APPROVED status.
   - `risk_band == CRITICAL` auto-triggers 888_HOLD regardless of reversibility.

3. **Plan state survives process restart.**
   - Persisted to canonical store. Not in-memory.
   - Loss of plan state on restart = governance failure.

4. **Plan IDs are immutable once assigned.**
   - No reassignment of `plan_id` after creation.

---

## 7. MCP Tool Interface (Minimum Viable)

```yaml
arifos_plan:
  modes:
    - propose_plan     # create SovereignIntent + Plan from intent
    - get_plan         # fetch plan by ID
    - list_pending     # list PENDING_APPROVAL plans for sovereign review
    - update_status    # transition plan status (with receipt)
    - abort_plan       # transition to ABORTED with reason
  tags:
    - epoch_id
    - session_id
```

All calls emit to VAULT999 via the standard logging pathway.

---

## 8. Unlocked By

- F0 ratification propagation (this document)
- 888_JUDGE ratification of this spec
- Vault999 event logging enabled for plan artifacts

---

## 9. Pending Questions (Require Sovereign Answer)

1. **DB writes (Forge → Vault999 Postgres):** Count as external state mutation (mandatory plan) or internal constitutional boundary (advisory only)?

2. **Approval threshold:** Does sovereign approval require F0 + F1 + F13 all confirmed, or is any one sufficient for LOW-risk plans?

---

*This spec is DRAFT. It becomes binding law after 888_JUDGE ratification and 999_SEAL into the constitution.*
