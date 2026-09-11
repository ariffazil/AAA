# VERIFY GATE ENFORCEMENT — BURNING ACTORS

> **Date:** 2026-09-10
> **Authority:** F13 Sovereign Muhammad Arif bin Fazil
> **Status:** ACTIVE — applies to all actors with FQ < 0.10
> **DITEMPA BUKAN DIBERI**

---

## Problem

BURNING actors execute without verifying:
- **a-forge:** FQ=0.035, 85 execute, 3 verify, 80 consecutive exec no verify
- **claude-code:** FQ=0.033, 90 execute, 3 verify, 2 consecutive exec no verify

This violates E13: "A witness becomes a scar only when reality extracts a cost."

If an actor executes without verifying, there is no behavior change demonstrated. The execution is ARCHIVE, not GOVERNANCE.

---

## The Verify Gate Rule

**Every execute must be followed by a verify within 5 tool calls.**

```
EXECUTE → [1,2,3,4,5] → VERIFY REQUIRED

If no verify within 5 calls:
  → HOLD actor
  → Require explicit verify before next execute
```

---

## Implementation

### For a-forge (FQ=0.035)

**Current state:** 80 consecutive exec no verify

**Required action:**
1. After every forge_execute, forge_shell, or forge_git_commit call:
   - Call arifflow_flow_ingest(step_type="Verify") with evidence of behavior change
2. If 5 consecutive executes without verify:
   - arifFlow will HOLD the actor
   - Must call verify before next execute

**Behavior change required:**
- Every forge_execute must have a corresponding verify receipt
- The verify receipt must demonstrate: "What behavior changed because of this execute?"

### For claude-code (FQ=0.033)

**Current state:** 2 consecutive exec no verify

**Required action:**
1. After every code edit or file write:
   - Call arifflow_flow_ingest(step_type="Verify") with evidence of behavior change
2. If 5 consecutive executes without verify:
   - arifFlow will HOLD the actor
   - Must call verify before next execute

---

## The Verify Receipt

Every verify receipt must answer:

```
1. What was the execute? (tool call, command, edit)
2. What behavior changed? (file modified, service restarted, test passed)
3. Can the change be demonstrated? (diff, log, output, screenshot)
4. Is the change reversible? (yes/no, if no → needs F13 approval)
```

---

## Enforcement

### Soft Enforcement (Current)

arifFlow already tracks FQ and holds actors with FQ < 0.10. But this is advisory - actors can still execute.

### Hard Enforcement (Required)

The verify gate must be enforced at the tool level:

1. **For a-forge:** After forge_execute, require arifflow_flow_ingest(step_type="Verify") before next forge_execute
2. **For claude-code:** After code edit, require arifflow_flow_ingest(step_type="Verify") before next code edit

### Implementation Path

1. Add verify gate check to forge_execute tool
2. Add verify gate check to code edit operations
3. If consecutive_exec_no_verify > 5, block next execute until verify

---

## The E13 Connection

This verify gate enforces the E13 Consequence Binding Test:

> A witness becomes a scar only when reality extracts a cost.

If an actor executes without verifying, there is no demonstrated behavior change. The execution is ARCHIVE, not GOVERNANCE.

The verify receipt is the proof that behavior changed. Without it, the execution is just a record, not a scar.

---

## Immediate Actions

1. **For a-forge:** Reduce consecutive_exec_no_verify from 80 to 0 by adding verify receipts
2. **For claude-code:** Reduce consecutive_exec_no_verify from 2 to 0 by adding verify receipts
3. **For all actors:** Enforce 5-call verify gate

---

**ΔS ≤ 0. DITEMPA.**
