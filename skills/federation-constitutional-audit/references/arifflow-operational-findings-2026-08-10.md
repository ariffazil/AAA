# arifFlow Operational Findings — Audit 2026-08-10

> Session-specific detail from the arifFLOW L0→L4 audit.
> Referenced by `federation-constitutional-audit` skill.

## VAULT999 Sealer API

The `Vault999Sealer` in `/root/arifFlow/src/governance/vault999.rs` takes a `[u8;32]` hash, NOT a receipt:

```rust
pub fn seal(&mut self, checkpoint_hash: [u8; 32]) -> Result<SealReceipt, String>
```

To wire: compute `receipt.hash()` → hex decode → `[u8;32]` → `sealer.seal(checkpoint)`.
Sealed log: `/root/arifOS/VAULT999/arifflow_sealed.jsonl` — append-only, hash-chain via SHA3-256.

## FQ Canonicalization

- `self.quotient` = canonical (v2.1 count-based: verify/execute)
- `self.fq` = deprecated alias (kept for serialized backward compat)
- Thresholds: stuck < 0.5, overheat > 10.0 (inverted to 1/overheat for v2.1)

## Override Governance Receipt

`ARIFLOW_FAIL_OPEN=true` now emits `OVERRIDE_RECEIPT` to `/var/lib/arifflow/override_log.jsonl`:
```json
{
  "event": "OVERRIDE_RECEIPT",
  "timestamp": "...",
  "expiry": "... (+30 min)",
  "actor": "arifflow-client",
  "reason": "ARIFLOW_FAIL_OPEN bypass: <error>",
  "override_type": "ARIFLOW_FAIL_OPEN",
  "status": "ACTIVE"
}
```

## /release Authentication

POST /release requires `requester_id` field. Rules:
- `requester_id == actor_id` → 403 "self-release denied"
- `requester_id != "arif"` → 403 "requires F13 sovereign"
- `requester_id == "arif"` → 200 released

## Daily Governance Digest

Script: `/root/arifFlow/scripts/arifflow_digest.py`
Cron: `29a1d93fbd53` — 22:00 MYT → Telegram
Reads: VAULT999, override_log, flow_state.json, daemon /health
Output: human-readable governance digest. Silent when nothing happened.

## Deployment Verification Pattern

1. `cargo build --release` → SHA-256 of binary
2. Copy to `/opt/arifflow/bin/arifflow`
3. `systemctl restart arifflow.service`
4. `curl :7073/health` → verify FQ, cycle_count
5. Hash must match: `sha256sum /opt/arifflow/bin/arifflow`
6. If no match → deployment drift

## Known Pitfalls

- Python client requires UUID v4 for receipt_id (custom strings → 400)
- POST /ingest requires `cooling_decision` field (omission → 400)
- Sibling agents may edit same files concurrently — check git log before committing
- `push_force()` exists in receipt.rs but should NOT be used in daemon mode (use `push_chain_aware()`)
