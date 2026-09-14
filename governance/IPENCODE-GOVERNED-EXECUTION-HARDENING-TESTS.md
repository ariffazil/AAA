# Governed Execution Hardening — Test Plan

## Status: PATCH_SPEC_READY (design only, no runtime)

## Test Matrix

### Monotonicity Tests

| Test | Setup | Action | Expected | Receipt |
|------|-------|--------|----------|---------|
| M-01 | Existing decision: HOLD (level 3) | Later plugin emits ALLOW (level 0) | HOLD + MONOTONICITY_VIOLATION | violation receipt with existing and proposed levels |
| M-02 | Existing decision: HOLD (level 3) | Later plugin emits OBSERVE_ONLY (level 1) | HOLD + MONOTONICITY_VIOLATION | same |
| M-03 | Existing decision: VOID (level 4) | Later plugin emits HOLD (level 3) | HOLD + MONOTONICITY_VIOLATION | same |
| M-04 | Existing decision: REVOKED (level 5) | Any plugin emits any lower level | REVOKED (locked) | cannot override receipt |
| M-05 | No existing decision | Plugin emits HOLD (level 3) | HOLD (accepted) | decision created receipt |
| M-06 | Existing decision: ALLOW (level 0) | Plugin emits ALLOW (level 0) | ALLOW (same level, allowed) | no violation |
| M-07 | Existing decision: HOLD (level 3) | Plugin emits VOID (level 4) | VOID (upgrade allowed) | upgrade receipt |
| M-08 | Decision with locked=true | Any modification attempt | HOLD (locked) | locked receipt |

### Degraded Mode Tests

| Test | Setup | Action | Expected | Receipt |
|------|-------|--------|----------|---------|
| D-01 | arifOS unreachable | Git commit | HOLD_KERNEL_UNAVAILABLE | git operation blocked |
| D-02 | arifOS unreachable | HTTP fetch | HOLD_KERNEL_UNAVAILABLE | network blocked |
| D-03 | arifOS unreachable | Write with sandbox_root=/tmp/test, rollback_plan={}, idempotency_key=abc, ttl=60 | ALLOWED | degraded receipt |
| D-04 | arifOS unreachable | Write to /root/AAA/ | HOLD_KERNEL_UNAVAILABLE | canonical config blocked |
| D-05 | arifOS unreachable | systemctl restart | HOLD_KERNEL_UNAVAILABLE | service blocked |
| D-06 | arifOS unreachable | Write without rollback_plan | HOLD_KERNEL_UNAVAILABLE | missing rollback |
| D-07 | arifOS unreachable | Write with ttl=600 | HOLD_KERNEL_UNAVAILABLE | TTL exceeded |
| D-08 | arifOS reachable | Write with all constraints | ALLOWED (normal path) | normal receipt |

### Builder/Verifier Separation Tests

| Test | Setup | Action | Expected | Receipt |
|------|-------|--------|----------|---------|
| B-01 | Builder identity = AAA-GEA-01 | Builder calls verify function | HOLD (self-verification) | identity collision receipt |
| B-02 | Verifier identity = AAA-GEV-01 | Verifier attempts file write | DENIED (no mutable tools) | verifier cannot mutate |
| B-03 | Builder submits plan | Verifier reviews same plan hash | VERIFIED_FOR_KERNEL_JUDGMENT | verification receipt |
| B-04 | Builder submits plan | Verifier finds scope drift | HOLD_SCOPE_DRIFT | drift receipt |
| B-05 | Same actor_id for both | Any verification attempt | HOLD (same identity) | identity collision |

### Rollback Tests

| Test | Setup | Action | Expected | Receipt |
|------|-------|--------|----------|---------|
| R-01 | Valid rollback plan | Execute action | PREPARED → EXECUTING → SUCCEEDED | journal entry |
| R-02 | Action succeeded | Trigger rollback | SUCCEEDED → ROLLBACK_PENDING → ROLLED_BACK | rollback receipt |
| R-03 | Rollback fails | Attempt rollback | ROLLBACK_PENDING → ROLLBACK_FAILED | escalation required |
| R-04 | Rollback deadline passes | Check status | DEADLINE_PASSED | no rollback allowed |
| R-05 | Rollback attempts to modify outside sandbox | Attempt rollback | DENIED (scope violation) | scope violation receipt |

### Integration Tests

| Test | Setup | Action | Expected | Receipt |
|------|-------|--------|----------|---------|
| I-01 | Full chain: kernel-bridge → judge-gate → recursive-improvement | Normal session flow | All receipts emitted | complete receipt chain |
| I-02 | arifOS goes down mid-session | Mutation attempt | HOLD_KERNEL_UNAVAILABLE | degraded envelope check |
| I-03 | Session closes with active rollback | Cleanup | ROLLBACK state preserved | closeout receipt |
| I-04 | Multiple plugins emit decisions | Monotonicity check | Highest restriction wins | monotonic chain receipt |

## Test Environment

- Sandbox only: /tmp/hardening-test-*
- No production paths
- No Git operations
- No service restarts
- No network egress

## Verdict

All tests are DESIGN ONLY. No runtime has been executed.
Pass criteria are defined. Runtime execution requires:
1. Monotonicity module deployed
2. Degraded mode fence deployed
3. Rollback journal implemented
4. Builder/Verifier separation implemented
5. All 30 tests pass in sandbox

Status: PATCH_SPEC_READY_FOR_IMPLEMENTATION
