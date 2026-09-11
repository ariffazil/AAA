# STUCK ACTOR RECOVERY — EXECUTION REDUCTION

> **Date:** 2026-09-10
> **Authority:** F13 Sovereign Muhammad Arif bin Fazil
> **Status:** ACTIVE — applies to all actors with FQ 0.20-0.50
> **DITEMPA BUKAN DIBERI**

---

## Problem

STUCK actors execute too much relative to verification:
- **hermes-asi:** FQ=0.30, 1215 execute, 364 verify (3.3:1 ratio)
- **qwen-code:** FQ=0.32, 31 execute, 10 verify (3.1:1 ratio)

This violates E13: "A witness becomes a scar only when reality extracts a cost."

If an actor executes 3x more than it verifies, the system is in SIMULATION mode - acting as if it's governing when it's just executing.

---

## The Execution Reduction Rule

**For STUCK actors (FQ 0.20-0.50): reduce execution frequency by 50%.**

```
Current: EXECUTE → EXECUTE → EXECUTE → VERIFY → EXECUTE → EXECUTE → EXECUTE → VERIFY
Required: EXECUTE → VERIFY → EXECUTE → VERIFY → EXECUTE → VERIFY → EXECUTE → VERIFY
```

Every execute must be followed by a verify. No exceptions.

---

## Implementation

### For hermes-asi (FQ=0.30)

**Current state:** 1215 execute, 364 verify (3.3:1 ratio)

**Required action:**
1. After every hermes-asi execute:
   - Call arifflow_flow_ingest(step_type="Verify") with evidence of behavior change
2. If consecutive_execute > 2:
   - Block next execute until verify is called
3. Target: reduce execute:verify ratio from 3.3:1 to 1:1

**Behavior change required:**
- Every hermes-asi execute must have a corresponding verify receipt
- The verify receipt must demonstrate: "What behavior changed because of this execute?"

### For qwen-code (FQ=0.32)

**Current state:** 31 execute, 10 verify (3.1:1 ratio)

**Required action:**
1. After every qwen-code execute:
   - Call arifflow_flow_ingest(step_type="Verify") with evidence of behavior change
2. If consecutive_execute > 2:
   - Block next execute until verify is called
3. Target: reduce execute:verify ratio from 3.1:1 to 1:1

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

arifFlow already tracks FQ and holds actors with FQ < 0.50. But this is advisory - actors can still execute.

### Hard Enforcement (Required)

The execution reduction must be enforced at the tool level:

1. **For hermes-asi:** After execute, require verify before next execute
2. **For qwen-code:** After execute, require verify before next execute

### Implementation Path

1. Add consecutive_execute check to hermes-asi tool calls
2. Add consecutive_execute check to qwen-code tool calls
3. If consecutive_execute > 2, block next execute until verify

---

## The E13 Connection

This execution reduction enforces the E13 Consequence Binding Test:

> A witness becomes a scar only when reality extracts a cost.

If an actor executes 3x more than it verifies, the system is in SIMULATION mode - acting as if it's governing when it's just executing.

The verify receipt is the proof that behavior changed. Without it, the execution is just a record, not a scar.

---

## Immediate Actions

1. **For hermes-asi:** Reduce execute:verify ratio from 3.3:1 to 1:1
2. **For qwen-code:** Reduce execute:verify ratio from 3.1:1 to 1:1
3. **For all STUCK actors:** Enforce 2-call consecutive execute limit

---

## The SIMULATION Pathology

The arifFlow vector diagnosis shows: PARADOX:SIMULATION

This means: the system is SIMULATING governance rather than ACTUALLY governing.

Evidence:
- hermes-asi executes 1215 times, verifies 364 times
- qwen-code executes 31 times, verifies 10 times
- a-forge executes 85 times, verifies 3 times
- claude-code executes 90 times, verifies 3 times

The system has:
- Registry ✅
- Witness ✅
- Receipts ✅
- Reports ✅
- Dashboards ✅

But: behavior is not changing. Execution dominates verification.

The SIMULATION pathology is the system acting as if it's governing when it's actually just executing.

**The fix:** Every execute must have a verifiable behavior change. If no behavior change, classify as ARCHIVE, not GOVERNANCE.

---

**ΔS ≤ 0. DITEMPA.**
