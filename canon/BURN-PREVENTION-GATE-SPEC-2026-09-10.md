# BURN PREVENTION GATE SPECIFICATION

> **Date:** 2026-09-10
> **Authority:** F13 Sovereign Muhammad Arif bin Fazil
> **Status:** ACTIVE — applies to all actors
> **DITEMPA BUKAN DIBERI**

---

## Purpose

BURNING actors execute without verifying. This violates E13.

The Burn Prevention Gate creates a mandatory transition:

```
Execute → Verify → Adapt
```

Not:

```
Execute → Execute → Execute
```

---

## Specification

### The Rule

```
MAX_EXEC_STREAK = 5

If consecutive_execute > MAX_EXEC_STREAK:
    VERIFY_REQUIRED = true
    Block next execute until verify is called
```

### Actor Classes

| Class | FQ Range | MAX_EXEC_STREAK | Enforcement |
|-------|----------|-----------------|-------------|
| BURNING | < 0.10 | 3 | HARD |
| STUCK | 0.10-0.50 | 5 | HARD |
| GOVERNABLE | 0.50-1.00 | 10 | SOFT |
| OPTIMAL | > 1.00 | 20 | ADVISORY |
| FOSSILIZED | > 10.00 | 1 | HARD |

---

## Implementation

### For BURNING Actors (a-forge, claude-code)

**Current state:**
- a-forge: 80 consecutive exec, FQ=0.035
- claude-code: 2 consecutive exec, FQ=0.033

**Required:**
```
MAX_EXEC_STREAK = 3

After 3 consecutive executes:
    Block next execute
    Require arifflow_flow_ingest(step_type="Verify")
    Verify must include adaptation receipt
```

### For STUCK Actors (hermes-asi, qwen-code)

**Current state:**
- hermes-asi: FQ=0.30
- qwen-code: FQ=0.32

**Required:**
```
MAX_EXEC_STREAK = 5

After 5 consecutive executes:
    Block next execute
    Require arifflow_flow_ingest(step_type="Verify")
    Verify must include adaptation receipt
```

### For FOSSILIZED Actors (grok-build)

**Current state:**
- grok-build: FQ=97.5 (verification dominance)

**Required:**
```
MAX_EXEC_STREAK = 1

After 1 execute:
    Block next execute
    Require arifflow_flow_ingest(step_type="Verify")
    Verify must include adaptation receipt
```

---

## The Verify Requirement

When VERIFY_REQUIRED is triggered:

1. Call arifflow_flow_ingest(step_type="Verify")
2. Include adaptation receipt with:
   - observation: What was witnessed?
   - constraint: What new limitation exists?
   - behavior_change: What will be done differently?
   - effective_from: When does behavior change begin?
   - classification: NO_CHANGE|RULE_CHANGE|CONSTRAINT_CHANGE|PROCESS_CHANGE

3. If adaptation receipt is incomplete:
   - Classification = ARCHIVE
   - Verify does not count
   - Execute remains blocked

---

## The Reality Gate

This gate ensures:

> Reality mesti mendapat hak untuk bercakap semula.

If an actor executes without verifying, reality has no voice. The system is in SIMULATION mode.

The Burn Prevention Gate restores reality's voice.

---

## Implementation Path

### For arifFlow

Add to actor state:

```typescript
interface ActorState {
  consecutive_execute: number;
  max_exec_streak: number;
  verify_required: boolean;
  last_verify_timestamp: string | null;
}
```

Add to ingest endpoint:

```typescript
if (step_type === 'Execute') {
  actor.consecutive_execute++;
  if (actor.consecutive_execute > actor.max_exec_streak) {
    actor.verify_required = true;
    return { status: 'BLOCKED', reason: 'VERIFY_REQUIRED' };
  }
}

if (step_type === 'Verify') {
  actor.consecutive_execute = 0;
  actor.verify_required = false;
}
```

### For tool calls

Add pre-execution check:

```typescript
beforeExecute(actor_id: string) {
  const state = getActorState(actor_id);
  if (state.verify_required) {
    return {
      status: 'BLOCKED',
      reason: 'VERIFY_REQUIRED',
      message: 'Must call verify before next execute'
    };
  }
}
```

---

## The E13 Connection

This gate enforces the E13 Consequence Binding Test:

> A witness becomes a scar only when reality extracts a cost.

If an actor executes without verifying, there is no demonstrated behavior change. The execution is ARCHIVE, not GOVERNANCE.

The verify receipt with adaptation fields is the proof that behavior changed.

---

## The Transition

The Burn Prevention Gate creates a mandatory transition:

```
Execute → Verify → Adapt
```

Not:

```
Execute → Execute → Execute
```

This is the transition from SIMULATION to GOVERNANCE.

---

**ΔS ≤ 0. DITEMPA.**
