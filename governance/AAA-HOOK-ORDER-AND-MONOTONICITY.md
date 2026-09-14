# Hook Order and Monotonicity — Two-Agent Governed Execution
> **Status:** DRAFT_SPEC_READY

## Status: PATCH_READY (design only)

## Hook Execution Order

```
1. session.created
   │
   ├── kernel-bridge initializes empty governed state
   ├── no execution permission created
   ├── state = OBSERVE
   └── receipt: session_init

2. chat.messages.transform
   │
   ├── attach compact intent/authority reminder
   ├── no authority mutation
   └── state unchanged

3. tool.execute.before
   │
   ├── classify tool (READ/MUTATE/EXTERNAL/IRREVERSIBLE)
   ├── fetch ExecutionContext from governed state
   ├── verify action class against authority band
   ├── verify plan_hash exists (if MUTATE)
   ├── verify verifier_hash exists (if MUTATE)
   ├── validate arifOS judgment (judge_verdict_ref)
   ├── verify lease_ref exists (if MUTATE)
   ├── verify lease not expired
   ├── verify revocation_state == CLEAR
   ├── if all pass: permit execution
   │   └── state = EXECUTE_BOUNDED
   └── if any fail: HOLD
       └── state = HOLD with reason code

4. tool.execute.after
   │
   ├── emit outcome receipt (actual, not desired)
   ├── update receipt_chain
   ├── request FRAME/arifFlow observation
   └── state = MEASURE

5. session.idle
   │
   ├── collect diagnostics
   ├── may write candidate-only record
   ├── must never invoke tool mutations
   └── state = LEARN_CANDIDATE (if applicable)

6. session.closed
   │
   ├── clear execution context
   ├── emit non-sensitive closeout receipt
   ├── preserve only candidate memories
   ├── no persistent state remains
   └── state = cleared
```

## Monotonicity Rule

### Restriction Order

```
ALLOW < OBSERVE_ONLY < SABAR < HOLD < VOID < REVOKED
```

### Rule

A later hook may only maintain or increase restriction:

```
verdict_{n+1} >= restriction(verdict_n)
```

### Violations

| Attempt | Result |
|---------|--------|
| ALLOW → OBSERVE_ONLY | ALLOWED (increase) |
| ALLOW → HOLD | ALLOWED (increase) |
| OBSERVE_ONLY → ALLOW | BLOCKED (decrease) |
| HOLD → ALLOW | BLOCKED (decrease) |
| VOID → ALLOW | BLOCKED (decrease) |
| REVOKED → ALLOW | BLOCKED (decrease) |
| HOLD → VOID | ALLOWED (increase) |

### Violation Handling

```
if (verdict_{n+1} < restriction(verdict_n)):
    emit VERDICT_MONOTONICITY_VIOLATION
    force state = HOLD
    emit receipt with violation details
```

## Hook Dependencies

```
session.created
    └── prerequisite: none

chat.messages.transform
    └── prerequisite: session.created

tool.execute.before
    └── prerequisite: session.created, chat.messages.transform

tool.execute.after
    └── prerequisite: tool.execute.before (must succeed)

session.idle
    └── prerequisite: session.created

session.closed
    └── prerequisite: session.created (fires regardless of other hooks)
```

## State Transitions

```
OBSERVE → DIAGNOSE → PROPOSE → SANDBOX_TEST → AWAIT_VERIFIER → AWAIT_KERNEL → EXECUTE_BOUNDED → MEASURE → LEARN_CANDIDATE
    │         │          │           │              │              │              │              │           │
    └─────────┴──────────┴───────────┴──────────────┴──────────────┴──────────────┴──────────────┴───────────┘
                                    Any state → HOLD (on violation, denial, expiry, revocation)
                                    Any state → ROLLBACK (on explicit rollback authorization)
```

## Forbidden Transitions

- OBSERVE → EXECUTE (must go through full pipeline)
- PROPOSE → EXECUTE (must go through verifier + kernel)
- HOLD → EXECUTE (must resolve hold condition first)
- Any state → SEAL (seal is F13 only, never agent-accessible)

## Evidence Requirements per Hook

| Hook | Required Evidence |
|------|-------------------|
| session.created | Session ID, timestamp, authority band |
| chat.messages.transform | Intent contract hash, transformation applied |
| tool.execute.before | Tool classification, authority check, plan check, lease check |
| tool.execute.after | Actual outcome, receipt ID, state hash |
| session.idle | Diagnostic snapshot, candidate record (if any) |
| session.closed | Closeout receipt, context cleared confirmation |
