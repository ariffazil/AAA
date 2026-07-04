# 04-vault-receipt-completion

**Sub-forge ID:** 04-vault-receipt-completion
**Parent forge:** GEOX-C1-CONSTITUTIONAL-INTEGRATION
**Priority:** P2
**Status:** SPEC DRAFT
**Created:** 2026-06-06

---

## Problem

GEOX emits `audit_receipt.vault999_ref: "VAULT999-PENDING"`. The Vault write never happens. The receipt is dangling.

**Live receipt (2026-06-06T14:06Z):**
```json
{
  "audit_receipt": {
    "vault999_ref": "VAULT999-PENDING",
    "session_id": "geox-no-session",
    "actor_id": "geox-unknown",
    "trace_id": "trace-06da059dfa424b9e",
    "tool_name": "geox_query_intake"
  }
}
```

`VAULT999-PENDING` means: "I tried to write a Vault entry, but the federation contract didn't carry it through." Either:
- GEOX is calling `arif_vault_seal` but the call fails (F11 gate)
- GEOX is supposed to call it but never does
- The contract is unclear

In all three cases, the audit loop is broken. Every GEOX call is constitutionally anonymous in the Vault.

## Goal

Close the audit loop. Every GEOX tool call produces a persistent record. The record is either:
- (a) Sealed to Vault999 (if F11 is satisfied)
- (b) Queued locally with `VAULT999-PENDING` status (if F11 is not yet satisfied)

Either way, the record exists. The federation can roll up (b) → (a) once F11 is propagated.

## Design

### Local receipt queue

**File:** `/var/log/geox/receipts.jsonl` (newline-delimited JSON, append-only)

```json
{"ts": "2026-06-06T14:06:54.058Z", "session_id": "geox-no-session", "actor_id": "geox-unknown", "trace_id": "trace-06da059dfa424b9e", "tool_name": "geox_query_intake", "vault_ref": "VAULT999-PENDING", "claim_state": "INTERPRETED", "evidence_refs": []}
```

### Two options for Vault write

| Option | Description | Pros | Cons |
|---|---|---|---|
| (a) **OpenClaw connector proxies** | Connector receives GEOX audit receipt, forwards to `arif_vault_seal` | Tighter integration | More code, more failure modes, requires F11 propagation through OpenClaw |
| (b) **Local queue + federation cron** | GEOX writes to local JSONL. A cron reads PENDING rows, calls `arif_vault_seal` | Looser integration, no federation contract change | Latency (cron interval = drift window) |

**Recommendation:** (b) for now.

Reasoning: same pattern as arifOS's `outcomes.jsonl` (Phase 1 work showed 19,636 lines, most PENDING → SEALED via cron). Federation-level Vault sealing is a Phase 3 concern. This sub-forge is about closing the loop locally, not federating it.

### Federation cron

**File:** `geox/cron/vault_rollup.py` (new, ~50 lines)

```python
import json
import time
import requests

RECEIPTS_PATH = "/var/log/geox/receipts.jsonl"
PENDING_PATH = "/var/log/geox/receipts.pending.jsonl"
SEALED_PATH = "/var/log/geox/receipts.sealed.jsonl"
ARIFOS_VAULT_SEAL = "http://127.0.0.1:8088/arif_vault_seal"
CRON_INTERVAL_SEC = 300  # 5 min

def rollup():
    """Move PENDING receipts to federation Vault. Move SEALED to archive."""
    pending = open(PENDING_PATH).readlines() if os.path.exists(PENDING_PATH) else []
    for line in pending:
        receipt = json.loads(line)
        try:
            r = requests.post(ARIFOS_VAULT_SEAL, json={
                "mode": "seal",
                "payload": json.dumps(receipt),
                "session_id": receipt["session_id"],
                "actor_id": receipt["actor_id"],
                "ack_irreversible": False,  # PENDING is not irreversible yet
            }, timeout=10)
            if r.json().get("verdict") == "SEAL":
                receipt["vault_ref"] = r.json()["vault_entry_id"]
                with open(SEALED_PATH, "a") as f:
                    f.write(json.dumps(receipt) + "\n")
            else:
                # Stay PENDING
                pass
        except Exception as e:
            # Log and move on
            print(f"WARN: Vault seal failed for {receipt['trace_id']}: {e}")
    # Truncate PENDING
    open(PENDING_PATH, "w").close()

if __name__ == "__main__":
    while True:
        rollup()
        time.sleep(CRON_INTERVAL_SEC)
```

**Wire-up:** add as systemd timer (`geox-vault-rollup.timer`), every 5 min.

### Failure modes

| Condition | Behavior |
|---|---|
| Local queue full (disk) | `888_HOLD: RECEIPT_QUEUE_FULL` (alert) |
| Federation cron fails | PENDING row stays PENDING, retry next interval |
| `arif_vault_seal` returns 888_HOLD | PENDING row stays PENDING, log warning |
| `arif_vault_seal` returns SEAL | Move to SEALED, update `vault_ref` |

## Implementation sketch

**File:** `geox/audit/local_queue.py` (new, ~30 lines)

```python
import json
import os
import time

RECEIPTS_DIR = "/var/log/geox"

def write_receipt(audit_receipt):
    """Append audit receipt to local queue."""
    path = os.path.join(RECEIPTS_DIR, "receipts.jsonl")
    os.makedirs(RECEIPTS_DIR, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            **audit_receipt,
        }) + "\n")
```

**Wire-up:** `geox/server.py` (modify, ~3 lines) — call `write_receipt()` after every tool call completes.

## Acceptance criteria

1. **W0 self-report:** `geox_system_registry_status` reports `audit_receipt_local_queue: /var/log/geox/receipts.jsonl, count: N` where N > 0.
2. **W1 raw probe:** After a tool call, `wc -l /var/log/geox/receipts.jsonl` increases by 1.
3. **W2 connector probe:** Same.
4. **Cron test:** After 5 min, PENDING rows with `vault_ref: VAULT999-PENDING` either get a real `vault_ref` (if F11 satisfied) or stay PENDING with a warning.
5. **Disk test:** Filling the disk to 100% makes GEOX return `888_HOLD: RECEIPT_QUEUE_FULL` on the next call.

## Reversibility

✅ Local queue + cron. No federation contract.
- Rollback: stop cron, delete queue file, revert `geox/server.py` change.
- Federation contract: unchanged. arifOS doesn't know about this yet.

## Sunset policy

This sub-forge is the **local-receipt tactical bridge** (sunset epoch-2026.09). After sunset:
- (a) Federation Vault sealing is a first-class GEOX feature (no local queue).
- (b) Or: GEOX is replaced by a native arifOS organ that uses arifOS Vault directly.

Either way, the receipt contract survives — only the implementation layer changes.

## Out of scope

- Does not federate Vault999 across all organs. This is local queue, not cross-organ.
- Does not add Vault entries for non-GEOX tools. arifOS, WEALTH, WELL have their own patterns.
- Does not change `arif_vault_seal` semantics. Just calls it as a federation client.
- Does not deduplicate receipts. Each call gets a row. (Deduplication is a downstream concern.)

---

**Status:** DRAFT — awaiting Arif review and seal.
**Pairs with:** 01-connector-identity-propagation (uses `session_id` + `actor_id` for queue key).
**Gated on:** F11 FederationEnvelope propagation (out of scope for this forge, but needed for full SEAL).
