# Path-5 Telemetry & Witness Event Catalog
**Document:** `PATH5_WITNESS_EVENTS.md`  
**Standard:** QQQ Protocol · F1 Truth · Witness-First Doctrine  
**Date:** 2026-09-14T09:50:00+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::PATH5_OPERATIONALIZATION::v1`

---

## 1. Core Law: Witness > Narrative

*No swarm capability exists until witnessed. Every state transition in the worktree and lease lifecycle emits an immutable, hash-bound event to the federation witness substrates.*

---

## 2. Event Taxonomy & Schemas

| Event Type | Trigger | Target Substrate | Payload Summary |
|---|---|---|---|
| `path5.lease.issued` | Lease creation | VAULT999 / arifFlow | `lease_id`, `actor_id`, `scope`, `ttl_seconds`, `issued_at` |
| `path5.lease.heartbeat` | Agent heartbeat ping | Local state / arifFlow | `lease_id`, `actor_id`, `timestamp` |
| `path5.lease.expired` | Lease passes TTL | VAULT999 / arifFlow | `lease_id`, `expired_at`, `uncommitted_files` |
| `path5.lease.revoked` | 888/F13 kill signal | VAULT999 / arifFlow | `lease_id`, `revoked_by`, `reason` |
| `path5.worktree.created` | Physical worktree setup | Local log / arifFlow | `lease_id`, `worktree_path`, `branch_name` |
| `path5.worktree.destroyed` | Worktree removed | Local log / arifFlow | `lease_id`, `cleanup_status`, `duration_sec` |
| `path5.merge.requested` | Reconciler submission | arifFlow / FRAME | `lease_id`, `actor_id`, `diff_files`, `commit_sha` |
| `path5.merge.approved` | Reconciler merge PASS | VAULT999 / arifFlow | `lease_id`, `merged_commit_sha`, `test_results` |
| `path5.merge.rejected` | Reconciler gate FAIL | VAULT999 / arifFlow | `lease_id`, `rejection_stage`, `failure_reason` |

---

## 3. Canonical Event Receipt Example

```json
{
  "event_id": "evt_7f8a9b0c1d2e",
  "event_type": "path5.merge.approved",
  "timestamp": "2026-09-14T01:50:00Z",
  "lease_id": "lease_8a2b3c4d5e6f",
  "actor_id": "FI-009/AGY",
  "repository": "AAA",
  "branch_merged": "swarm/lease_8a2b3c4d5e6f",
  "target_branch": "main",
  "commit_sha": "d4e5f6a1b2c3",
  "tests_passed": 94,
  "tests_failed": 0,
  "witness_receipt_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "routed_organ": "A-FORGE",
  "reconciled_by": "A-FORGE-RECONCILER"
}
```
