# Path-5 Merge Flood Governance & Concurrency Policy
**Document:** `MERGE_POLICY.md`  
**Standard:** QQQ Protocol · F1 Truth · System Stability  
**Date:** 2026-09-14T09:49:00+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::PATH5_OPERATIONALIZATION::v1`

---

## 1. Concurrency Limits & Caps (KVM8 Reality)

To prevent resource starvation, disk ballooning, or reconciler thrashing, hard resource bounds are enforced:

| Dimension | Hard Limit | Enforcement Action if Exceeded |
|---|---|---|
| **Max Active Worktrees** | **4 concurrent** | New `worktree_create` requests are queued or rejected (`CONCURRENCY_LIMIT_REACHED`). |
| **Max Pending Reconciliations** | **8 in queue** | Additional mutation submissions blocked until queue drains. |
| **Max Lease Duration (TTL)** | **14,400s (4 hours)** | Enforced by auto-expiry loop; forces incremental checkpointing. |
| **System Resource Tripwire** | Load > 8.0 OR Free RAM < 3GB | Worktree spawn throttled; active runs throttled to prevent swap thrashing. |

---

## 2. Priority Queue Ordering

When multiple worktrees submit reconciliation requests, the queue processes them by strict priority:

```text
Priority 0 (P0): F13 Sovereign Directive / Critical Security Hotfix (Immediate Preempt)
Priority 1 (P1): Kernel (:8088) Constitutional & Integrity Fixes
Priority 2 (P2): Standard Task Deliverables & Organ Feature Work
Priority 3 (P3): Background Documentation, Grooming & Metric Sweeps
```

---

## 3. Reconciliation Serial Lock

Reconciliation into the canonical branch (`main`) must be strictly serialized:
- A file lock (`/root/forge_work/worktrees/.reconcile.lock`) is acquired by the Reconciler.
- Only one worktree merges into `main` at any given millisecond.
- After merge, unit tests and drift guards re-validate on `main` before releasing the lock and admitting the next worktree.
- If a downstream worktree becomes stale due to an earlier merge, the Reconciler commands an automated `git rebase` within the isolated worktree before admitting it to `main`.
