"""
Decision Packet Engine (v1.0.0 - Hardened P1-C.1)
Cryptographically seals and chains agent decisions, evidence, and actions
into an append-only decision supply chain ledger with monotonic sequence numbers,
envelope fields, replay defense, and tamper verification.
"""

import os
import sys
import json
import uuid
import time
import fcntl
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonicalize import canonicalize, hash_object

LEDGER_DIR = os.environ.get("DECISION_PACKET_LEDGER_DIR", "/data/aaa/ledgers/decision_packets")
LEDGER_CHAIN_FILE = os.path.join(LEDGER_DIR, "chain.jsonl")
NONCE_CACHE_FILE = os.path.join(LEDGER_DIR, ".nonces.json")
GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"
LEDGER_ID = "aaa-decision-ledger-main"


class DecisionPacketError(Exception):
    """Base error for decision packet generation or verification."""
    pass


class PolicyHoldRequired(DecisionPacketError):
    """Raised when an action requires 888 HOLD human approval."""
    pass


class ReplayDetectedError(DecisionPacketError):
    """Raised when a duplicated request nonce is detected."""
    pass


def get_engine_code_hash() -> str:
    """Compute SHA-256 hash of this engine script for self-provenance."""
    with open(__file__, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def get_latest_chain_state() -> Tuple[str, int]:
    """Retrieve the latest packet hash and sequence number from the ledger chain."""
    if not os.path.exists(LEDGER_CHAIN_FILE):
        return GENESIS_HASH, 0
    
    with open(LEDGER_CHAIN_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
        if not lines:
            return GENESIS_HASH, 0
        try:
            entry = json.loads(lines[-1])
            prev_hash = entry.get("integrity", {}).get("packet_hash", GENESIS_HASH)
            seq_no = entry.get("integrity", {}).get("sequence_no", len(lines))
            return prev_hash, seq_no
        except Exception:
            return GENESIS_HASH, len(lines)


def check_and_record_nonce(nonce: str) -> None:
    """Check against seen nonces to prevent replay attacks within ledger domain."""
    seen_nonces = set()
    if os.path.exists(NONCE_CACHE_FILE):
        try:
            with open(NONCE_CACHE_FILE, "r", encoding="utf-8") as f:
                seen_nonces = set(json.load(f))
        except Exception:
            seen_nonces = set()

    if nonce in seen_nonces:
        raise ReplayDetectedError(f"Replay attack detected: Nonce '{nonce}' has already been processed.")

    seen_nonces.add(nonce)
    with open(NONCE_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen_nonces)[-5000:], f)  # Keep rolling cache of recent nonces


def validate_packet_policy(packet: Dict[str, Any]) -> None:
    """Validate constitutional gates before sealing a packet."""
    task = packet.get("task", {})
    risk_class = task.get("risk_class", "R0")
    action = packet.get("action", {})
    findings = packet.get("findings", {})

    # Invariant 1: Distinction between Observations and Interpretations
    obs = findings.get("observations", [])
    interps = findings.get("interpretations", [])

    for o in obs:
        if "confidence" not in o or o["confidence"] < 0.90:
            raise DecisionPacketError(
                f"Observation '{o.get('statement')}' must be a high-confidence factual output (>= 0.90)."
            )

    for i in interps:
        if not i.get("assumptions"):
            raise DecisionPacketError(
                f"Interpretation '{i.get('statement')}' must declare at least one explicit assumption."
            )

    # Invariant 2: Consequential Actions Require 888 HOLD
    if action.get("proposed") and risk_class in ("R2", "R3", "R4"):
        approval = action.get("human_approval", {})
        if not approval.get("required") or approval.get("state") != "granted":
            raise PolicyHoldRequired(
                f"Action with risk {risk_class} requires 888 HOLD human approval state='granted' before sealing."
            )


def seal_decision_packet(
    task: Dict[str, Any],
    execution: Dict[str, Any],
    evidence: Dict[str, Any],
    findings: Dict[str, Any],
    action: Dict[str, Any],
    outcome: Dict[str, Any],
    parent_packets: Optional[List[str]] = None,
    artifact_refs: Optional[List[str]] = None,
    correlation_id: Optional[str] = None,
    request_nonce: Optional[str] = None,
    ledger_id: str = LEDGER_ID
) -> Dict[str, Any]:
    """
    Construct, validate, hash, and append a hardened Decision Packet to the ledger chain.
    Thread-safe and process-safe via file locking.
    """
    os.makedirs(LEDGER_DIR, exist_ok=True)

    nonce = request_nonce or uuid.uuid4().hex
    corr_id = correlation_id or f"trace_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}"

    # Check replay
    check_and_record_nonce(nonce)

    today_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    unique_id = uuid.uuid4().hex[:8]
    packet_id = f"dp_{today_str}_{unique_id}"
    now_utc = datetime.now(timezone.utc).isoformat()

    # Base integrity skeleton with P1-C.1 envelope fields
    integrity = {
        "parent_packets": parent_packets or [],
        "canonicalization": "RFC8785-JCS",
        "hash_algorithm": "SHA-256",
        "sequence_no": 0,  # Will be stamped under lock
        "packet_hash": "",  # Placeholder before hashing
        "previous_ledger_hash": "",
        "ledger_id": ledger_id,
        "emitted_by": {
            "service_id": "decision-packet-engine",
            "code_hash": f"sha256:{get_engine_code_hash()}"
        },
        "request_nonce": nonce,
        "correlation_id": corr_id,
        "sealed_at_utc": now_utc,
        "artifact_refs": artifact_refs or [],
        "retention_class": "internal_technical_record"
    }

    packet = {
        "schema_version": "1.0.0",
        "packet_id": packet_id,
        "created_at_utc": now_utc,
        "task": task,
        "execution": execution,
        "evidence": evidence,
        "findings": findings,
        "action": action,
        "integrity": integrity,
        "outcome": outcome
    }

    # Policy validation
    validate_packet_policy(packet)

    # Acquire flock to prevent race condition during ledger append
    lock_file_path = os.path.join(LEDGER_DIR, ".ledger.lock")
    with open(lock_file_path, "w") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            prev_hash, last_seq = get_latest_chain_state()
            packet["integrity"]["previous_ledger_hash"] = prev_hash
            packet["integrity"]["sequence_no"] = last_seq + 1

            # Deterministic Hashing: hash packet with blank packet_hash
            packet_copy = json.loads(json.dumps(packet))
            packet_copy["integrity"]["packet_hash"] = ""
            final_hash = hash_object(packet_copy)

            # Stamp final hash into packet
            packet["integrity"]["packet_hash"] = final_hash

            # Write individual packet file
            individual_path = os.path.join(LEDGER_DIR, f"{packet_id}.json")
            with open(individual_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(packet, indent=2, sort_keys=True))

            # Append to immutable chain.jsonl
            with open(LEDGER_CHAIN_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(packet, sort_keys=True) + "\n")

        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

    return packet


def verify_chain(ledger_file: str = LEDGER_CHAIN_FILE) -> Dict[str, Any]:
    """
    Verify cryptographic integrity of the decision packet chain:
    - Sequence numbers are strictly monotonic: 1, 2, 3...
    - previous_ledger_hash exactly matches the prior block's packet_hash
    - packet_hash matches deterministic RFC 8785 hash of contents
    - Timestamps are non-decreasing
    """
    if not os.path.exists(ledger_file):
        return {"status": "EMPTY", "count": 0, "valid": True}

    with open(ledger_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_prev = GENESIS_HASH
    expected_seq = 1
    last_timestamp = None

    for idx, line in enumerate(lines):
        pkt = json.loads(line)
        integrity = pkt.get("integrity", {})
        claimed_hash = integrity.get("packet_hash")
        actual_prev = integrity.get("previous_ledger_hash")
        actual_seq = integrity.get("sequence_no")
        sealed_time = integrity.get("sealed_at_utc")

        # 1. Monotonic Sequence Check
        if actual_seq != expected_seq:
            return {
                "status": "SEQUENCE_GAP_OR_REORDER",
                "index": idx,
                "packet_id": pkt.get("packet_id"),
                "expected_seq": expected_seq,
                "actual_seq": actual_seq,
                "valid": False
            }

        # 2. Hash Linkage Check
        if actual_prev != expected_prev:
            return {
                "status": "CORRUPTED_CHAIN",
                "index": idx,
                "packet_id": pkt.get("packet_id"),
                "expected_prev": expected_prev,
                "actual_prev": actual_prev,
                "valid": False
            }

        # 3. Deterministic Content Hash Re-computation
        pkt_copy = json.loads(json.dumps(pkt))
        pkt_copy["integrity"]["packet_hash"] = ""
        computed_hash = hash_object(pkt_copy)

        if computed_hash != claimed_hash:
            return {
                "status": "HASH_MISMATCH",
                "index": idx,
                "packet_id": pkt.get("packet_id"),
                "claimed_hash": claimed_hash,
                "computed_hash": computed_hash,
                "valid": False
            }

        # 4. Timestamp non-decreasing check
        if last_timestamp and sealed_time < last_timestamp:
            return {
                "status": "TIMESTAMP_RETROGRADE",
                "index": idx,
                "packet_id": pkt.get("packet_id"),
                "last_timestamp": last_timestamp,
                "current_timestamp": sealed_time,
                "valid": False
            }

        expected_prev = claimed_hash
        expected_seq += 1
        last_timestamp = sealed_time

    return {
        "status": "VALID",
        "count": len(lines),
        "latest_sequence": expected_seq - 1,
        "latest_hash": expected_prev,
        "valid": True
    }


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        res = verify_chain()
        print(json.dumps(res, indent=2))
        sys.exit(0 if res.get("valid") else 1)
    else:
        print("Usage: python3 engine.py verify")
