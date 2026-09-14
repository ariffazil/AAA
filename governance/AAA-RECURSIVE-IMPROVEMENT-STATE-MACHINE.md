# Recursive Improvement State Machine
> **Status:** DRAFT_SPEC_READY

## Status: PATCH_READY (design only)

## Purpose

Enable the institution to autonomously sense, diagnose, draft, test, verify, and queue improvements — while preventing autonomous consequential execution.

## State Machine

```
                    ┌─────────────┐
                    │   OBSERVE   │ ← session.created
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   DIAGNOSE  │ ← identify bounded issue
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   PROPOSE   │ ← create candidate
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ SANDBOX_TEST│ ← test isolated fixture
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │AWAIT_VERIFIER│ ← verifier reviews
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │AWAIT_KERNEL │ ← arifOS judges
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌──▼───┐ ┌──────▼──────┐
       │EXECUTE_BOUNDED│ │ HOLD │ │ AWAIT_HUMAN │
       └──────┬──────┘ └──────┘ └─────────────┘
              │                       │
       ┌──────▼──────┐                │
       │   MEASURE   │                │
       └──────┬──────┘                │
              │                       │
       ┌──────▼──────┐                │
       │LEARN_CANDIDATE│              │
       └──────┬──────┘                │
              │                       │
       ┌──────▼──────┐                │
       │   ROLLBACK  │ ← explicit auth only
       └─────────────┘                │
                                      │
                               ┌──────▼──────┐
                               │   OBSERVE   │ ← restart cycle
                               └─────────────┘
```

## State Definitions

| State | Builder | Verifier | Kernel/A-FORGE | Description |
|-------|---------|----------|----------------|-------------|
| OBSERVE | Read only | Read only | None | Gather evidence, read live state |
| DIAGNOSE | Draft analysis | Read only | None | Identify one bounded issue |
| PROPOSE | Create candidate | Review candidate | None | Single improvement proposal |
| SANDBOX_TEST | Test isolated fixture | Observe/verify | No production lease | Safe local testing |
| AWAIT_VERIFIER | No | Yes | None | Independent evidence review |
| AWAIT_KERNEL | No | No | arifOS judgment | Constitutional validation |
| AWAIT_HUMAN | No | No | F13 if required | Sovereign approval for irreversible |
| EXECUTE_BOUNDED | Through A-FORGE | Observe only | Valid lease, clear revocation | One narrow effect |
| MEASURE | No repair | Measure | arifFlow + FRAME evidence | Outcome measurement |
| LEARN_CANDIDATE | Candidate only | Validate provenance | No promotion | Create non-promoted candidate |
| HOLD | No | No | Resolve named condition | Blocked pending resolution |
| ROLLBACK | Under exact authorization | Verify result | Bounded rollback plan | Revert to baseline |

## Transition Rules

### Allowed Transitions

```
OBSERVE → DIAGNOSE
DIAGNOSE → PROPOSE
PROPOSE → SANDBOX_TEST
SANDBOX_TEST → AWAIT_VERIFIER
AWAIT_VERIFIER → AWAIT_KERNEL (if VERIFIED)
AWAIT_KERNEL → EXECUTE_BOUNDED (if APPROVED)
EXECUTE_BOUNDED → MEASURE
MEASURE → LEARN_CANDIDATE
LEARN_CANDIDATE → OBSERVE (new cycle)

Any state → HOLD (on violation, denial, expiry, revocation)
Any state → ROLLBACK (on explicit rollback authorization)
HOLD → OBSERVE (after resolving hold condition)
ROLLBACK → OBSERVE (after rollback verified)
```

### Forbidden Transitions

```
OBSERVE → EXECUTE_BOUNDED (must go through full pipeline)
PROPOSE → EXECUTE_BOUNDED (must go through verifier + kernel)
HOLD → EXECUTE_BOUNDED (must resolve hold condition first)
Any state → SEAL (seal is F13 only, never agent-accessible)
Any state → DEPLOY (deployment is F13 + human confirmation)
Any state → PROMOTE (memory promotion is gated)
```

## Autonomy Boundaries

### Autonomous (left side of loop)

```
observe → measure → diagnose → propose → draft → sandbox test → independently verify → await governed decision
```

These are safe, local, reversible, and do not require human intervention.

### Non-autonomous (right side of loop)

```
commit → deploy → alter authority → alter identity → expand capability → promote durable memory → seal
```

These require human confirmation, F13 authorization, or explicit lease.

## Improvement Candidate Format

```json
{
  "schema": "aaa.improvement_candidate.v1",
  "candidate_id": "cand_...",
  "trace_id": "trc_...",
  "created_at": "timestamp",
  "builder_id": "AAA-GEA-01",
  "verifier_id": "AAA-GEV-01",
  "problem": "string",
  "evidence": "string",
  "proposed_change": {
    "files": ["string"],
    "expected_effect": "string",
    "test": "string",
    "rollback": "string"
  },
  "plan_hash": "sha256:...",
  "verdict": "VERIFIED|HOLD|REJECTED",
  "promoted": false,
  "promotion_date": null,
  "review_date": null
}
```

## Receipt Structure

```json
{
  "schema": "aaa.recursive_improvement_receipt.v1",
  "receipt_id": "rcpt_...",
  "trace_id": "trc_...",
  "timestamp": "timestamp",
  "cycle_state": "OBSERVE|DIAGNOSE|PROPOSE|...|LEARN_CANDIDATE",
  "actor": "AAA-GEA-01|AAA-GEV-01|arifos|aforge|ariflow|frame",
  "action": "string",
  "result": "SUCCESS|FAILURE|HOLD|DENIED",
  "evidence_ref": "string",
  "candidate_id": "cand_..."
}
```
