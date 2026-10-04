# Multi-Writer Bypass — arifFlow FQ Reconciliation Failure (2026-08-11)

Worked example of the "same symptom, different root cause" lesson.
The weekly drift check (`re_audit_drift_check.sh` Probe 5) failed with
daemon FQ=1.78 vs disk-recomputed FQ=6.40 (|Δ|=4.62, threshold 0.3).
The 2026-08-10 failure was a stale-load bug (head vs tail). This one was NOT.

## Symptom
- `daemon_health` PASS (FQ=1.78 OPTIMAL, receipts=1000, uptime 2h57m)
- `client_fail_closed` PASS
- `receipts_persistence` PASS (1901 receipts, last write 4m ago)
- `fq_reconciliation` **FAIL** (|Δ|=4.62)
- `receipt_count_reconciliation` PASS (daemon memory=1000 ≈ disk=1901)

## Why the naive read was wrong
The first impulse is "stale-load bug again." But the receipt-count probe PASSED
(daemon at cap 1000, disk at 1901), and the daemon's startup load code
(`main.rs` ~line 747) already uses the tail (drain(keep_from..)) fix. So
head-vs-tail was not the cause. The divergence was in WHICH receipts, not
HOW MANY.

## Diagnostic that proved it — receipt-ID cross-reference
```bash
# Disk receipt IDs never seen by daemon:
journalctl -u arifflow --since "<start ts>" --no-pager | grep "ingested with" | grep -oE "Receipt [0-9a-f-]+"
# vs disk IDs; set-difference = bypassed.
```
Result: only 27 of 1901 disk receipts appeared in the daemon journal since
startup. Of the last 100 disk lines, 73 were never ingested.

Bypassed writers by actor (missing-receipt counts):
- `aed-v1` 1434
- `333-AGI` 173
- `kimi-code/FI-008` 71
- `arifos` 58
- `orchestrator-v1` 50

Missing by step_type: Execute 719, Verify 951, Cool 70, Seal 133, Barrier 1.

## Root cause
Federation organs append receipts directly to `/var/lib/arifflow/receipts.jsonl`,
bypassing the daemon's `POST /ingest`. The daemon's in-memory ReceiptStore
(cap 1000) therefore holds only its startup snapshot + the ~27 it ingested,
so its FQ window and enforcement gate operate on a strict subset of reality.

## Constitutional impact
- FQ gate (F0–F6 enforcement, HOLD/THROTTLE) governs on stale/partial data.
- Three actors were HELD with FQ=0.00 based on the daemon's view; corrections
  based on current metabolism are delayed.
- VALID ≠ TRUE: daemon FQ=1.78 is internally consistent but false against the
  disk record (FQ=6.4, verify-dominant).

## Decision required (F13)
1. Single-writer model — route ALL receipts through daemon /ingest only, OR
2. Read FQ from disk as the canonical witness (in-memory = monitoring only).
This is an architectural choice, not a code fix.

## Reusable takeaway
After ANY FQ reconciliation failure, run the receipt-ID cross-reference BEFORE
proposing a fix. See SKILL.md Phase 10 "FQ Divergence Has MULTIPLE Root Causes"
table for the four signatures (stale-load, multi-writer bypass, formula
mismatch, window-semantics mismatch) and their distinct fixes.