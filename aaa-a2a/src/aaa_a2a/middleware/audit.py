"""Audit — VAULT999 receipt chain.

Every A2A task completion writes a receipt.
Append-only. Hash-chained. Immutable.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from aaa_a2a.models import AuditRecord, Verdict


# ── In-memory receipt chain (fallback until VAULT999 is connected) ──────

_receipts: list[dict] = []
_last_hash: str = "genesis"


def _compute_hash(record: dict, prev_hash: str) -> str:
    """Compute SHA-256 hash of record + previous hash."""
    payload = json.dumps(record, sort_keys=True) + prev_hash
    return hashlib.sha256(payload.encode()).hexdigest()


def write_receipt(record: AuditRecord) -> dict:
    """Write an audit receipt to the chain.

    Returns the receipt with hash and chain link.
    """
    global _last_hash

    now = datetime.now(timezone.utc).isoformat()
    record.timestamp = record.timestamp or now

    receipt = {
        "event": record.event,
        "agent_id": record.agent_id,
        "task_id": record.task_id,
        "verdict": record.verdict.value if isinstance(record.verdict, Verdict) else record.verdict,
        "floors_checked": record.floors_checked,
        "floors_violated": record.floors_violated,
        "evidence": record.evidence,
        "timestamp": record.timestamp,
        "prev_hash": _last_hash,
    }

    receipt["hash"] = _compute_hash(receipt, _last_hash)
    _last_hash = receipt["hash"]
    _receipts.append(receipt)

    record.receipt_id = receipt["hash"]
    return receipt


def get_chain() -> list[dict]:
    """Get the full receipt chain."""
    return list(_receipts)


def get_last_hash() -> str:
    """Get the hash of the last receipt."""
    return _last_hash


def verify_chain() -> bool:
    """Verify the integrity of the receipt chain."""
    global _last_hash

    prev = "genesis"
    for receipt in _receipts:
        expected = _compute_hash(
            {k: v for k, v in receipt.items() if k != "hash"},
            prev,
        )
        if receipt["hash"] != expected:
            return False
        prev = receipt["hash"]

    return prev == _last_hash


async def write_to_vault999(receipt: dict, vault_url: str = "http://localhost:8088") -> bool:
    """Write receipt to VAULT999 via arifOS kernel.

    Returns True if successful.
    """
    import httpx

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{vault_url}/seal",
                json=receipt,
                timeout=5.0,
            )
            return resp.status_code == 200
    except Exception:
        return False
