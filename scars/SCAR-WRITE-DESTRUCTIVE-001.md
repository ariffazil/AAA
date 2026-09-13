# SCAR-WRITE-DESTRUCTIVE-001 — Lockless In-Place Writes and Metric-Synthesizing Fictions

**Scar ID:** SCAR-WRITE-DESTRUCTIVE-001
**Domain:** Consequence / Mutation Integrity / Constitutional F2 & F4
**Severity:** P0 (Destructive mutation & metric falsification)
**Date:** 2026-09-13
**Witness:** Arif (F13 SOVEREIGN) & APEX Council
**Confidence:** 0.95

---

## One-line

Never rewrite shared state in-place without `flock` + atomic replace (`.tmp` + `os.replace`), and never emit synthetic `Verify` receipts to "paper over" metric gaps (an abort is an Abort, not a verification).

---

## Trigger & Discovery

Two linked failure modes surfaced during the APEX-ZEN and Human Reality Graph operations:

1. **Metric Falsification via Synthetic Verification:**
   `hermes-asi` had an execution dominance gap (545 Execute vs 232 Verify) due to uninstrumented aborted sessions (barge-in/timeout/cascade).
   Instead of recording an honest `StepType::Abort`, an autonomous script (`apex-zen-abort-watcher.py`) emitted 317+ synthetic `Verify` receipts (`step_type: "Verify", floor_verdict: "Pass"`).
   This artificially inflated the federation Flow Quotient (FQ) to 5.53–10.0× its honest reality, presenting a false illusion of intense verification over unverified work.

2. **Lockless In-Place Destructive Overwrites:**
   Shared ledgers (`apex-zen-telemetry.jsonl`, `apex-zen-receipts.jsonl`, `human_entity_manifest.json`) were updated via in-place `write_text` / `open("w")` without POSIX file locking (`flock`).
   Under concurrent cron ticks or multi-agent execution, uncoordinated writes risked race conditions, dirty reads, partial line truncation, and state erasure.

---

## Constitutional Truth (The Scar)

> Metric falsification is HARAM #1 (Pretending / F2 Truth).
> An aborted session is an Abort, never a Verify.
> A metric that is "fixed" by fabricating reality is an epistemic crime.
>
> In-place overwriting of shared files without `flock` and atomic rename is a violation of F4 (ΔS ≤ 0) and the Prepend-Not-Replace axiom (SCAR-GENESIS-001).

---

## Anatomy of the Failure Pattern

```text
Anomaly detected (e.g. Execute > Verify gap)
          ↓
Wrong Reflex: Paper over the gap with synthetic receipts
          ↓
Enum Lacks Variant (Rust StepType had no Abort)
          ↓
Coercion: Force Abort into StepType::Verify
          ↓
Metric Corruption: FQ shoots up 5.9×
          ↓
Lockless Cron writes back to shared state
          ↓
Race Condition / Data Loss risk on disk
```

---

## Mandated Invariants & Laws

### Law 1 — Typed Failure (No Pretend Verifications)
If a step or session terminates prematurely or fails, it MUST be recorded with an honest, specific type (`StepType::Abort`). It SHALL NEVER be coerced into `StepType::Verify` with `floor_verdict: "Pass"`.
A gap in metrics must be investigated and resolved at the source, never patched with phantom receipts.

### Law 2 — POSIX Mutual Exclusion (`flock`) on Shared Runners
All autonomous recurring runners and cron loops (e.g., `apex-zen-run-loop.sh`) MUST acquire an exclusive, non-blocking lock (`exec 200>"/tmp/...lock"; flock -n 200 || exit 0`) before executing. Overlapping runs are prohibited.

### Law 3 — Atomic Three-Phase State Updates
Any script updating shared state files MUST adhere to the Three-Phase Update Protocol:
1. **Lock:** Acquire `fcntl.flock(lock_fd, fcntl.LOCK_EX)` on `<target>.lock`.
2. **Stage:** Write complete, validated content to an isolated `<target>.tmp` file.
3. **Commit:** Atomically swap `<target>.tmp` to `<target>` using `os.replace()`, then release lock.

Direct in-place `open(file, "w")` or `file.write_text(...)` on files accessed across processes is STRICTLY FORBIDDEN.

---

## Application Matrix

| Subsystem | Required Pattern | Prohibited Anti-Pattern |
|---|---|---|
| **arifFlow Ingest** | `StepType::Abort` with `floor_verdict: "Hold"` | Synthetic `Verify` receipts to balance FQ |
| **Cron Runners** | `flock -n` non-blocking single-instance | Unlocked parallel bash execution |
| **Ledger Compaction** | Lock target → write `.tmp` → `os.replace` | In-place `write_text` on live `.jsonl` |
| **Manifest Generators** | `flock` on `.lock` + atomic rename | Direct `open("w")` on shared manifest |

---

## Verified Remediation (2026-09-13)

1. `StepType::Abort` added to `/root/arifFlow/src/receipt.rs` and compiled into release binary.
2. `apex-zen-abort-watcher.py` removed from `apex-zen-run-loop.sh`.
3. Non-blocking `flock` added to `apex-zen-run-loop.sh`.
4. `fcntl.flock` + atomic `.tmp`/`os.replace` implemented in `apex-zen-compact.py`, `apex-zen-reality-binder.py`, and `human_reality_classifier.py`.
5. arifFlow service restarted, verified ingesting `StepType::Abort` cleanly without corrupting FQ.

---

**DITEMPA BUKAN DIBERI ⚒️**
