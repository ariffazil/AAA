#!/usr/bin/env python3
"""Output attestation: compute SHA-256 of a file, record to attestation ledger.

T0 operation (read-only). Use before delivering ANY artifact to the real world
(PDF, email, doc). The hash is REAL — computed from actual file content.
Deployed copy: /root/HERMES/scripts/output-attest.py
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

def record_to_ledger(entry: dict) -> None:
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")

def attest_file(file_path: str, label: str = "", agent_id: str = "hermes") -> dict:
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    file_hash = compute_sha256(file_path)
    file_size = os.path.getsize(file_path)
    timestamp = datetime.now(timezone.utc).isoformat()
    entry = {
        "type": "output_attestation",
        "file_path": os.path.abspath(file_path),
        "file_name": os.path.basename(file_path),
        "sha256": file_hash,
        "file_size": file_size,
        "timestamp": timestamp,
        "agent_id": agent_id,
        "label": label or f"output:{os.path.basename(file_path)}",
        "verbatim": True,  # This hash was COMPUTED, not generated
    }
    record_to_ledger(entry)
    return {
        "sha256": file_hash,
        "file_path": os.path.abspath(file_path),
        "file_size": file_size,
        "timestamp": timestamp,
        "ledger_recorded": True,
        "short_hash": file_hash[:16] + "...",
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: output-attest.py <file_path> [--label 'desc'] [--agent 'id']")
        sys.exit(1)
    file_path = sys.argv[1]
    label, agent_id = "", "hermes"
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--label" and i + 1 < len(sys.argv):
            label = sys.argv[i + 1]; i += 2
        elif sys.argv[i] == "--agent" and i + 1 < len(sys.argv):
            agent_id = sys.argv[i + 1]; i += 2
        else:
            i += 1
    print(json.dumps(attest_file(file_path, label=label, agent_id=agent_id), indent=2))
