#!/usr/bin/env python3
"""Verify a file's SHA-256 against a claimed hash AND the attestation ledger.

Returns VERIFIED (hash matches + ledger entry) / FABRICATED (claimed hash
doesn't match actual file digest) / COMPUTED (no claim, hash computed only).
Deployed copy: /root/HERMES/scripts/output-verify.py
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

LEDGER_PATH = "/root/HERMES/attestation-ledger.jsonl"

def compute_sha256(file_path: str) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def find_ledger_entry(file_path: str) -> dict | None:
    abs_path = os.path.abspath(file_path)
    if not os.path.exists(LEDGER_PATH):
        return None
    last_entry = None
    with open(LEDGER_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get("file_path") == abs_path:
                    last_entry = entry
            except json.JSONDecodeError:
                continue
    return last_entry

def verify(file_path: str, claimed_hash: str = None) -> dict:
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}", "verdict": "ERROR"}
    actual_hash = compute_sha256(file_path)
    result = {
        "file_path": os.path.abspath(file_path),
        "file_name": os.path.basename(file_path),
        "file_size": os.path.getsize(file_path),
        "actual_sha256": actual_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    ledger_entry = find_ledger_entry(file_path)
    if ledger_entry:
        result["ledger_entry"] = {
            "timestamp": ledger_entry.get("timestamp"),
            "agent_id": ledger_entry.get("agent_id"),
            "label": ledger_entry.get("label"),
            "ledger_hash": ledger_entry.get("sha256"),
        }
        result["ledger_match"] = (actual_hash == ledger_entry.get("sha256"))
    else:
        result["ledger_entry"] = None
        result["ledger_match"] = None

    if claimed_hash:
        claimed_clean = claimed_hash.strip().lower()
        result["claimed_hash"] = claimed_hash
        result["claim_match"] = (claimed_clean == actual_hash.lower())
        if result["claim_match"]:
            result["verdict"] = "VERIFIED"
            result["message"] = "✅ Hash matches — attestation is genuine"
        else:
            result["verdict"] = "FABRICATED"
            result["message"] = "❌ Hash MISMATCH — attestation is FABRICATED"
            result["evidence"] = {
                "claimed": claimed_clean[:32] + "...",
                "actual": actual_hash[:32] + "...",
                "first_divergence": next(
                    (i for i, (a, b) in enumerate(zip(claimed_clean, actual_hash)) if a != b),
                    "different length",
                ),
            }
    else:
        result["verdict"] = "COMPUTED"
        result["message"] = f"Hash computed: {actual_hash[:16]}..."
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: output-verify.py <file_path> [claimed_hash]")
        sys.exit(1)
    print(json.dumps(verify(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None), indent=2))
