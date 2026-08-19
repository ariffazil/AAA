#!/usr/bin/env python3
"""
aaa_capability_seal.py — Lane B seal of the AAA Capability Plane state.

Appends a hash-chained receipt to:
  /root/arifOS/VAULT999/local_seals.jsonl      (canonical Lane B)
  /root/arifOS/VAULT999/outcomes.jsonl          (canonical observation log)

Captures:
  - registry SHA-256 (the witnessed registry state)
  - mcp.json SHA-256 (the generated harness state)
  - test suite verdict (READY_READONLY expected)
  - bridge generator verdict (REGENERATED expected)
  - previous receipt hash (chain integrity)

Authorized by F13 directive, 2026-08-11 (SEAL_PHASE_A_ONLY).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional


VAULT_LOCAL_SEALS = Path("/root/arifOS/VAULT999/local_seals.jsonl")
VAULT_OUTCOMES = Path("/root/arifOS/VAULT999/outcomes.jsonl")

REGISTRY_PATH = Path("/root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml")
MCP_JSON_PATH = Path("/root/.kimi-code/mcp.json")
RECEIPT_DIR = Path("/root/AAA/federation/init_receipts")


def _now_utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _last_receipt_hash(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    last = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                last = json.loads(line)
            except json.JSONDecodeError:
                continue
    if last is None:
        return None
    # The hash field convention is `log_sha256` for local_seals
    return last.get("log_sha256") or last.get("hash")


def _next_seq(seals_path: Path) -> str:
    if not seals_path.exists():
        return "DS-AAA-CAP-001"
    last_seq = None
    with open(seals_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                last = json.loads(line)
            except json.JSONDecodeError:
                continue
            seq = last.get("seq", "")
            if seq.startswith("DS-AAA-CAP-"):
                last_seq = seq
    if last_seq is None:
        return "DS-AAA-CAP-001"
    # Increment numeric suffix
    try:
        n = int(last_seq.rsplit("-", 1)[-1])
        return f"DS-AAA-CAP-{n + 1:03d}"
    except (ValueError, IndexError):
        return "DS-AAA-CAP-001"


def build_seal_envelope(
    prev_hash: Optional[str],
    registry_sha: str,
    mcp_sha: str,
    test_verdict: str,
    bridge_verdict: str,
    indicators: dict[str, Any],
) -> dict[str, Any]:
    envelope: dict[str, Any] = {
        "type": "AAA_CAPABILITY_PHASE_A_SEAL",
        "ts": _now_utc_iso(),
        "scope": "AAA Capability Plane — Phase A (2026-08-11)",
        "verdict": test_verdict,
        "indicators": indicators,
        "artifacts": {
            "registry_path": str(REGISTRY_PATH),
            "registry_sha256": registry_sha,
            "mcp_json_path": str(MCP_JSON_PATH),
            "mcp_json_sha256": mcp_sha,
        },
        "bridge_verdict": bridge_verdict,
        "previous_receipt_hash": prev_hash,
    }
    # log_sha256 = SHA-256 of canonical envelope (excludes the hash field itself)
    canonical = json.dumps(envelope, sort_keys=True, separators=(",", ":"))
    envelope["log_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return envelope


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(payload, sort_keys=True) + "\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)
    # Verify the new chain
    last = _last_receipt_hash(path)
    if last != payload.get("log_sha256"):
        raise RuntimeError(
            f"Chain integrity check failed at {path}: expected {last}, "
            f"got {payload.get('log_sha256')}"
        )


def main(argv: list[str]) -> int:
    if not REGISTRY_PATH.exists():
        print(f"FAIL: registry not found at {REGISTRY_PATH}", file=sys.stderr)
        return 1

    registry_sha = _sha256_file(REGISTRY_PATH)
    mcp_sha = (
        _sha256_file(MCP_JSON_PATH) if MCP_JSON_PATH.exists()
        else "no_mcp_json"
    )

    # Pull the most recent bridge receipt for verdict + indicators
    bridge_verdict = "UNKNOWN"
    bridge_receipts: list[Path] = []
    if RECEIPT_DIR.exists():
        bridge_receipts = sorted(RECEIPT_DIR.glob("*__mcp_gen.json"))
    if bridge_receipts:
        try:
            data = json.loads(bridge_receipts[-1].read_text())
            bridge_verdict = data.get("verdict", "UNKNOWN")
        except (json.JSONDecodeError, OSError):
            pass

    # Indicators — derived from a fresh init run (deterministic)
    sys.path.insert(0, str(Path(__file__).parent))
    from aaa_capability_init import run_init  # type: ignore

    receipt = run_init(REGISTRY_PATH)
    indicators = dict(receipt.indicators)
    test_verdict = receipt.verdict

    prev_hash = _last_receipt_hash(VAULT_LOCAL_SEALS)

    envelope = build_seal_envelope(
        prev_hash=prev_hash,
        registry_sha=registry_sha,
        mcp_sha=mcp_sha,
        test_verdict=test_verdict,
        bridge_verdict=bridge_verdict,
        indicators=indicators,
    )

    seq = _next_seq(VAULT_LOCAL_SEALS)
    envelope["seq"] = seq

    # Recompute hash with seq included (canonical)
    canonical = json.dumps(envelope, sort_keys=True, separators=(",", ":"))
    envelope["log_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    append_jsonl(VAULT_LOCAL_SEALS, envelope)

    # Mirror a structured entry into outcomes.jsonl (read-only observers see it)
    outcome = {
        "timestamp": envelope["ts"],
        "type": "AAA_CAPABILITY_SEAL",
        "seq": seq,
        "verdict": test_verdict,
        "registry_sha256": registry_sha,
        "mcp_json_sha256": mcp_sha,
        "bridge_verdict": bridge_verdict,
        "previous_receipt_hash": prev_hash,
        "log_sha256": envelope["log_sha256"],
    }
    append_jsonl(VAULT_OUTCOMES, outcome)

    # Print the seal in the canonical INIT format
    ts = envelope["ts"]
    print(f"[{ts}] [SEAL]   seq={seq}")
    print(f"[{ts}] [SEAL]   type={envelope['type']}")
    print(f"[{ts}] [SEAL]   verdict={test_verdict}")
    print(f"[{ts}] [SEAL]   registry_sha256={registry_sha}")
    print(f"[{ts}] [SEAL]   mcp_json_sha256={mcp_sha}")
    print(f"[{ts}] [SEAL]   bridge_verdict={bridge_verdict}")
    print(f"[{ts}] [SEAL]   previous_receipt_hash={prev_hash or 'genesis'}")
    print(f"[{ts}] [SEAL]   log_sha256={envelope['log_sha256']}")
    print(f"[{ts}] [SEAL]   lane=local_seals.jsonl")
    print(f"[{ts}] [SEAL]   mirror=outcomes.jsonl")
    print(f"[{ts}] [SEAL]   indicators={json.dumps(indicators, sort_keys=True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
