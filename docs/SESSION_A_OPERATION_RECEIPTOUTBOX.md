# Session A — Operation + ReceiptOutbox (SQLAlchemy + VAULT Worker)

**Status:** READY — execute when arifOS server is stable and PostgreSQL is up.
**Authority:** F1 AMANAH (reversible) · F11 AUDIT · F13 SOVEREIGN for deployment.
**Blast radius:** HIGH (changes execution path across all organs).

## Scope
- Add `Operation` + `ReceiptOutbox` tables via SQLAlchemy migration.
- Implement VAULT worker that seals receipts from the outbox.
- Replace direct VAULT calls in A-FORGE with `enqueue_receipt()`.

## Requirements
- States: `APPROVED → EXECUTING → EXECUTED_PENDING_RECEIPT → SEALED → FAILED → COMPENSATION_REQUIRED`.
- One `operation_id` per mutation, used as idempotency key.
- No `SUCCESS`/`COMPLETE`/`SEALED` status until VAULT999 confirms the receipt.

## Tasks
1. Design and apply PostgreSQL migration for `Operation` + `ReceiptOutbox`.
2. Patch A-FORGE executor to:
   - persist `execution_intent` + outbox entry before mutation,
   - update `Operation.result` and state after mutation,
   - return `EXECUTED_PENDING_RECEIPT` when sealing is pending.
3. Implement VAULT worker:
   - claim pending receipts with `FOR UPDATE SKIP LOCKED`,
   - write to VAULT999,
   - mark `sealed=true` and `Operation.state=SEALED`.
4. Add tests for crash, retry, idempotency, and hash mismatch → HOLD.

## Output
- `SESSION_A_OPERATION_RECEIPTOUTBOX_REPORT.md` with schema, code diffs, test results.

## Change Control
```yaml
 reversible: true
 blast_radius: high
 authority_required: F13_SOVEREIGN_FOR_DEPLOYMENT
 judge_receipt_required: true
 human_ack_required: true
 rollback: revert migration + restore prior VAULT write path
 post_change_probe: run isolated 8-stage canary, verify VAULT replay
```
