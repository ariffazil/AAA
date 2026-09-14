# Two-Agent Governed Execution — Integration Plan
> **Status:** DRAFT_SPEC_READY

## Status: PATCH_READY (draft only, no mutations)

## Architecture

```
User/Arif (F13 SOVEREIGN)
    │
    ▼
Hermes (Human Reality Edge Bridge)
    │ intent + multimodal evidence
    ▼
AAA-GEA-01 (Builder) ←──→ AAA-GEV-01 (Verifier)
    │ propose/test/execute         │ verify/measure/recommend
    ▼                              ▼
arifOS Kernel (JUDGE)
    │ validate authority, issue lease
    ▼
A-FORGE (EXECUTE)
    │ bounded execution under lease
    ▼
arifFlow ← receipts ← FRAME (MEASURE)
    │
    ▼
Improvement candidate (not auto-promoted)
```

## Role Separation

| Agent | Role | Can Do | Must Never Do |
|-------|------|--------|---------------|
| AAA-GEA-01 | Builder | Observe, diagnose, draft patches, sandbox test, prepare packets, execute under lease | Verify own work, self-authorize, self-seal, widen scope, modify identity/authority, promote memory |
| AAA-GEV-01 | Verifier | Read-only review, validate hashes/diffs/tests/receipts, detect drift, recommend HOLD/PASS | Write code, execute deployment, issue binding judgment, self-seal |
| arifOS | Judge | Bind sessions, validate authority, issue verdicts, authorize leases | Delegate final legality to agents |
| A-FORGE | Executor | Apply exact permitted effect under lease | Create own authority |
| F13/Arif | Sovereign | Approve consequential changes, seal | Be replaced by agent consensus |

## Shared State Schema

```json
{
  "schema": "aaa.governed_execution_state.v1",
  "trace_id": "trc_...",
  "session_id": "sess_...",
  "actor_id": "AAA-GEA-01",
  "primary_human_id": "arif",
  "authority_band": "LIMITED_MUTATE",
  "intent_contract_hash": "sha256:...",
  "action_class": "READ|MUTATE|EXTERNAL|IRREVERSIBLE",
  "plan_hash": "sha256:...",
  "verifier_hash": "sha256:...",
  "judge_verdict_ref": "opaque-ref",
  "lease_ref": "opaque-ref",
  "lease_expiry": "timestamp",
  "revocation_state": "CLEAR|REVOKED|UNKNOWN",
  "policy_version": "arifos-...",
  "runtime_surface_hash": "sha256:...",
  "state": "OBSERVE|PLAN|VERIFY|AWAIT_APPROVAL|EXECUTE|MEASURE|LEARN_CANDIDATE|HOLD",
  "issued_at": "timestamp",
  "expires_at": "timestamp",
  "receipt_chain": []
}
```

## Execution Gate

```
mayExecute = 
  authority_band != OBSERVE_ONLY
  AND action_class == MUTATE
  AND plan_hash != ""
  AND judge_verdict_ref != ""
  AND lease_ref != ""
  AND revocation_state == CLEAR
  AND now < lease_expiry

EXTERNAL or IRREVERSIBLE → always HOLD (F13 required)
UNKNOWN → HOLD
```

## Hook Order

```
session.created
  → kernel-bridge init empty governed state
  → no execution permission

chat.messages.transform
  → attach compact intent/authority reminder
  → no authority mutation

tool.execute.before
  → classify tool
  → fetch ExecutionContext
  → verify action class
  → verify plan
  → verify verifier state
  → validate arifOS judgment
  → verify lease + revocation
  → permit or HOLD

tool.execute.after
  → emit outcome receipt
  → request FRAME/arifFlow observation

session.idle
  → collect diagnostics
  → candidate-only record
  → no tool mutations

session.closed
  → clear execution context
  → emit closeout receipt
  → preserve only candidate memories
```

## Monotonicity Rule

A later hook may only maintain or increase restriction:

```
ALLOW < OBSERVE_ONLY < SABAR < HOLD < VOID < REVOKED
```

Violation → HOLD

## Recursive Improvement State Machine

| State | Builder | Verifier | Kernel/A-FORGE |
|-------|---------|----------|----------------|
| OBSERVE | Read only | Read only | None |
| DIAGNOSE | Draft analysis | Read only | None |
| PROPOSE | Create candidate | Review candidate | None |
| SANDBOX_TEST | Test isolated fixture | Observe/verify | No production lease |
| AWAIT_VERIFIER | No | Yes | None |
| AWAIT_KERNEL | No | No | arifOS judgment |
| AWAIT_HUMAN | No | No | F13 if required |
| EXECUTE_BOUNDED | Through A-FORGE | Observe only | Valid lease |
| MEASURE | No repair | Measure | arifFlow + FRAME |
| LEARN_CANDIDATE | Candidate only | Validate provenance | No promotion |
| HOLD | No | No | Resolve condition |
| ROLLBACK | Under exact auth | Verify result | Bounded plan |

## Files to Create

1. AAA-TWO-AGENT-GOVERNED-EXECUTION.md (this file)
2. AAA-GEA-01-MODEL-INIT.md (builder agent prompt)
3. AAA-GEV-01-MODEL-INIT.md (verifier agent prompt)
4. AAA-GOVERNED-EXECUTION-STATE.schema.json
5. AAA-HOOK-ORDER-AND-MONOTONICITY.md
6. AAA-SANDBOX-TEST-A-AND-B.md

## Deployment Sequence

1. Create agent model-init files (AAA-GEA-01, AAA-GEV-01)
2. Create governed execution state schema
3. Create hook order spec
4. Create sandbox test plans
5. Test A: denied mutation (OBSERVE_ONLY → HOLD)
6. Test B: bounded sandbox mutation (valid lease → execute → receipt)
7. Wire into Hermes plugin/hook system
8. Independent verification pass

## Rollback

All artifacts are in /root/AAA/governance/ or /root/.hermes/patches/.
No runtime, no service, no Git, no authority changes.
Full rollback: delete the artifacts.
