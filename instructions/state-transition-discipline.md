# State-Transition Discipline — Never Collapse a Transition into a Boolean

> **Status:** F13_RATIFIED_CHAT (2026-09-16) — sovereign directive: "make sure all my coding agents aligned". Codified from the two-KVM coherence experiment (R3 delivery deadlock; 52,043 receipts with trace_id=NULL; 17k→12.4k claim retraction).
> **Binding:** Every FI coding agent in arifOS Federation (FI-001..FI-009).
> **Companions:** claim-receipt-discipline · sovereign-attention-preservation · witness-zen-doctrine · anti-collapse-doctrine.

## The Law

Single-word verdicts hide entire state machines. For consequential objects, saying "done", "sent", "merged", "deployed", "true", or "remembered" without naming which state you actually achieved is a **transition lie**. The receiver cannot act on a Boolean.

```
PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ ACKNOWLEDGED
```

## Five Instantiations (one invariant, five layers)

| Layer | Forbidden collapse | Real chain |
|---|---|---|
| Execution | "ran" | Scheduled ≠ Ran ≠ Delivered ≠ Outcome ≠ Effective |
| Communication | "sent" | Produced ≠ Sent ≠ Delivered ≠ Observed ≠ Acked |
| Epistemology | "X is Y" | Claimed ≠ Measured ≠ CrossValidated ≠ Canonical |
| Memory | "remembered" | Stored ≠ Retrieved ≠ Relevant ≠ Current |
| Substrate | "FAIL" / "PASS" | OUTAGE ≠ DEGRADED ≠ IDLE_RESTING ≠ FAIL_CLOSED ≠ ACTIVE_SEALED |

## Object Contract — every persistent promise / claim / task

```
{ state, prev_state, expected_next, owner, evidence_required, deadline }
```

Communications additionally carry: `{ expected_event, last_acked }`.

## Timeout = Synchronization Fault

`WAIT → timeout → inspect expected_event + last_acked → retransmit (sender) or proceed-with-gap (receiver)`. Timeout **never** silently resolves disagreement — it **reclassifies** the blocker as `SYNCHRONIZATION_FAULT`, a distinct error class. Owner of next action is recorded at fault declaration.

## Claim States

Consequential numbers carry `{ claim_id, value, source, state, observed_at, supersedes }`:

```
ESTIMATED → MEASURED → CROSS_VALIDATED → RETRACTED | SUPERSEDED
```

When a number changes, the old claim becomes `RETRACTED`; downstream retrieval must not serve it as live evidence. Metric: **SCP** (Stale Claim Propagation) → 0.

## Receipts: trace_id Required

A receipt without `trace_id` is an event-pile entry, not a causal-ledger entry. On every consequential mutation: mint/accept a trace_id from the parent objective, stamp every receipt, reference it in the closing claim. Logging ≠ memory. Memory ≠ causal memory.

## Witness Roles Are prior-isolated, NOT Stateless

Operational memory (objective, timestamps, own probes) = YES. Shared hypothesis, shared conclusion, biasing doctrine = NO during blind falsification. Different kinds of ignorance are deliberately preserved — independent errors make falsification possible.

## Metrics (computed at seal time)

| Metric | Formula | Target |
|---|---|---|
| OCR Outcome Closure Rate | verified_closed / claimed_completed | → 1.0 |
| HMR Human Middleware Rate | objectives_needing_Arif / objectives | → 0 |
| MII Marginal Info per Invocation | new_verified_findings / additional_calls | → max |
| BCL Belief Correction Latency | median(T_corrected − T_disconfirming) | → min |
| SCP Stale Claim Propagation | decisions_using_retracted / retracted | → 0 |

## Operating Rules for Coding Agents (FI-001..FI-009)

1. **Report transitions, not Booleans.** "Wrote X" is not a deliverable; "Wrote X, path, test passes (or UNKNOWN)" is.
2. **Answer state questions with chain position**, not yes/no.
3. **Every handoff records expected_event + owner + deadline.** Timeout → SYNCHRONIZATION_FAULT, never silence, never assumed receipt.
4. **Numbers carry claim state.** ESTIMATED vs MEASURED in the artifact. Contradiction → mark old claim RETRACTED with supersedes chain, same file.
5. **Consequential receipts carry trace_id.**
6. **Witnessing another agent's claim → operate prior-isolated.**
7. **WAIT has a deadline.** Polite indefinite blocking = distributed deadlock. Declare the fault.
8. **Never collapse substrate into binary FAIL/PASS.** (F13 SEAL 2026-09-18: `SUBSTRATE_TAXONOMY_2026-09-18.md`). Idle/gated posture is `IDLE_RESTING` or `FAIL_CLOSED`, never physical `FAIL`.

DITEMPA BUKAN DIBERI ⚒️
