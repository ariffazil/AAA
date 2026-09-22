# Operational Bug Patterns — discovered during federation sweep

Three recurring failure patterns found during the 2026-09-21 APEX stabilization sweep. These are structural bugs, not one-off incidents.

## 1. Emit-before-ack in queue workers

**Class:** Queue consumer re-executes side effects on redelivery.

**Mechanism:** A JetStream/NATS durable consumer calls `emit()` (append to log + notify human) BEFORE calling `msg.ack()`. If the ack does not land — restart, exception, timeout — the message is redelivered after `ack_wait` and the side effect fires again. `MAX_DELIVER` caps per-message retries, but service recreation resets the delivery counter.

**Proof signature:** first repeat lands exactly `ack_wait` seconds after a service restart. That is redelivery, not a new event.

**Fix:** swap order — `await msg.ack()` before `emit()`. Or key the emit on JetStream message metadata (deduplicate by sequence) so redelivery is a no-op.

## 2. Windowed dedup on large append-only files

**Class:** Idempotency guard scans tail of a file that has grown far beyond the window.

**Mechanism:** Guard reads `f.readlines()[-1000:]` on a file with 93,000+ lines. Entries before the window are invisible. Every organ whose marker drifted past the window was re-sealed on every hourly cron run.

**Proof signature:** duplicate markers appear in contiguous groups of 7 (one full pass over all organs). Markers are `COMMIT-<organ>-<hash>` in an append-only ledger.

**Fix:** full scan or indexed lookup. For chattr +a files the duplicates are permanent; only tombstone markers can neuter them.

## 3. Inverted dedup timestamp (first_seen vs last_notified)

**Class:** Dedup window measured from the wrong anchor.

**Mechanism:** A dedup function checks `(now - first_ts) > WINDOW` to decide whether to re-notify. For a standing condition, `first_ts` is fixed at first occurrence. Once `now - first_ts > WINDOW` the condition is permanently true and every emission notifies. The function's own docstring states the correct contract but the code contradicts it.

**Fix:** `(now - last_notify) > WINDOW`. One variable.

## Pattern across all three

All three bugs share a structure:
- Declared behavior matched the design document
- Actual behavior was the opposite
- The system's own instrumentation counted the problem but did not act on it
- Fix attempts landed mid-incident but did not take effect because the root cause was a different layer

The meta-lesson: when a system says it is deduplicating and the human sees duplicates, check whether the dedup is reading the right variable, scanning the whole file, and ordering side effects after acknowledgment.