# A-FORGE UNKNOWN_OUTCOME — Execution Outcome Class Spec

> **Status:** F13_RATIFIED_CHAT (2026-09-25) — sovereign quote: "ratify all. do it. F13 ratified. semua empat." · implementation spec v1
> **Grounding:** audit CONFIRMED 2026-09-25 — `UNKNOWN_OUTCOME` had 0 hits in `/root/A-FORGE/src/` (grep-verified). Timeout was silently conflated with failure.
> **Scope:** A-FORGE execution state machine (`/root/A-FORGE/src/` — integration point: forge_execute / actuator receipt path). Implementation is T2; this document is the ratified contract the implementation must satisfy.

## 1. OutcomeClass — first-class enum

```ts
enum OutcomeClass {
  SUCCESS         = "SUCCESS",          // execute completed, result verified at boundary
  FAILURE         = "FAILURE",          // execute completed with known failure cause
  UNKNOWN_OUTCOME = "UNKNOWN_OUTCOME",  // execute dispatched, result UNVERIFIED — timeout, response truncation, transport drop
  RECOVERY        = "RECOVERY",         // execute failed, system self-recovered
  DENIED          = "DENIED",           // auth/policy deny BEFORE dispatch (no side effect possible)
}
```

Every actuator receipt MUST carry `outcome_class`. Absence of `outcome_class` on a dispatched action = receipt invalid (F2).

## 2. Behaviour rules (binding)

1. **UNKNOWN_OUTCOME never auto-retries.** No retry loop, no fallback re-dispatch, no "assume failed and redo."
2. **Reconcile-before-retry:** resolution requires a same-`action_hash` verification probe — check the external system's actual state against `evidence_before_action`, then promote to SUCCESS / FAILURE with the probe receipt attached.
3. **Status stays not-verified** until FRAME independent check or human attestation. Executor self-report cannot promote UNKNOWN_OUTCOME (Q9 anti-self-seal).
4. **Timeout ≠ FAILURE.** The request may have succeeded on the external system with the response lost. Partial execution is never attributed SUCCESS by default.
5. **Idempotency pairing:** actions whose destination supports idempotency keys (`amanahEnvelope.idempotency_key`) SHOULD retry-safe resolve via key lookup; destinations without idempotency MUST reconcile via state probe, never blind re-send.
6. **Ledger honesty:** arifFlow receipts for UNKNOWN_OUTCOME carry `floor_verdict: Caution` until resolved — FQ accounting counts them as neither execute-success nor failure.

## 3. State transitions

```
DISPATCHED ──ack──► RUNNING ──result──► SUCCESS | FAILURE
                       │
                       └─timeout/drop─► UNKNOWN_OUTCOME
                                          │ reconcile probe (same action_hash)
                                          ├─ external state == postcondition ──► SUCCESS (probe receipt)
                                          ├─ external state != postcondition ──► FAILURE (probe receipt)
                                          └─ probe indeterminate ──────────────► UNKNOWN_OUTCOME (escalate human/FRAME)
```

## 4. Minimal implementation footprint (for the T2 patch)

1. Add `OutcomeClass` to the actuator receipt type (`forge_execute` path).
2. Map existing timeout/transport-drop outcomes to `UNKNOWN_OUTCOME` instead of `FAILURE`.
3. Add `reconcile(action_hash)` primitive: state probe + promote/demote with receipt.
4. arifFlow ingest: accept `outcome_class` field; UNKNOWN receipts get `floor_verdict: Caution`.
5. Tests: (a) simulated timeout → UNKNOWN_OUTCOME → reconcile → exact-once resolution (no double payment/write); (b) DENIED before dispatch never emits receipt with side-effect claim.

## 5. Long-run actuator companion rule

Checkpoint + resumable + honest-incompleteness is the DEFAULT for long-run actuators (registry walker precedent: `walkComplete:false` + cursor recorded = honest partial). A run that ends early reports what it saw, not what it was asked to see.
