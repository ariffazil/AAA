#!/usr/bin/env python3
"""
evidence_ledger.py — Immutable Cryptographic Evidence Ledger for AAA Hooks
Canonical Path: /root/AAA/hooks/lib/evidence_ledger.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 6.2, 9 & F2 TRUTH / F11 AUDIT

Implements tamper-evident, hash-chained, process-safe append-only ledger storage
for all hook decisions, rollback actions, and generational seal receipts.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple

from event_schema import canonical_json, utc_now_iso


class EvidenceLedger:
    """Process-safe, cryptographically chained append-only JSONL ledger."""

    def __init__(self, ledger_path: Path):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)

    def _get_last_hash(self) -> str:
        """Retrieves the hash of the latest entry in the ledger."""
        if not self.ledger_path.exists() or self.ledger_path.stat().st_size == 0:
            return "0" * 64

        last_hash = "0" * 64
        with open(self.ledger_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if "entry_hash" in data:
                        last_hash = data["entry_hash"]
                except Exception:
                    continue
        return last_hash

    def append(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Appends a record with hash-chaining under an exclusive flock."""
        payload = dict(record)
        payload["timestamp"] = payload.get("timestamp", utc_now_iso())

        with open(self.ledger_path, "a+", encoding="utf-8") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                # Seek to start to re-verify latest hash if necessary
                f.seek(0)
                lines = [l.strip() for l in f if l.strip()]
                prev_hash = "0" * 64
                if lines:
                    try:
                        prev_entry = json.loads(lines[-1])
                        prev_hash = prev_entry.get("entry_hash", "0" * 64)
                    except Exception:
                        pass

                payload["previous_hash"] = prev_hash
                serialized = canonical_json(payload)
                entry_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
                payload["entry_hash"] = entry_hash

                f.seek(0, os.SEEK_END)
                f.write(json.dumps(payload, separators=(",", ":")) + "\n")
                f.flush()
                os.fsync(f.fileno())
                return payload
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def verify_chain(self) -> Tuple[bool, int, Optional[str]]:
        """Verifies the cryptographic hash integrity of the entire ledger.
        Returns: (is_valid, count, error_message_if_any)
        """
        if not self.ledger_path.exists() or self.ledger_path.stat().st_size == 0:
            return (True, 0, None)

        count = 0
        expected_prev_hash = "0" * 64

        with open(self.ledger_path, "r", encoding="utf-8") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            try:
                for line_idx, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except Exception as e:
                        return (False, count, f"Line {line_idx}: invalid JSON: {e}")

                    recorded_hash = entry.get("entry_hash")
                    recorded_prev = entry.get("previous_hash")

                    if recorded_prev != expected_prev_hash:
                        return (
                            False,
                            count,
                            f"Line {line_idx}: broken chain. Expected prev {expected_prev_hash}, got {recorded_prev}",
                        )

                    # Recompute entry hash
                    test_payload = {k: v for k, v in entry.items() if k != "entry_hash"}
                    computed_hash = hashlib.sha256(canonical_json(test_payload).encode("utf-8")).hexdigest()

                    if computed_hash != recorded_hash:
                        return (
                            False,
                            count,
                            f"Line {line_idx}: hash mismatch. Computed {computed_hash}, recorded {recorded_hash}",
                        )

                    expected_prev_hash = recorded_hash
                    count += 1
                return (True, count, None)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
