#!/usr/bin/env python3
"""RSI Cycle — Recursive Self-Improvement ledger writer.
SKILL: RSI-recursive-improvement · Version: 2026.07.23
DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone


LEDGER_PATH = "/root/.local/share/arifos/rsi-ledger.jsonl"


def parse_args():
    p = argparse.ArgumentParser(description="RSI Cycle — session-end ledger writer")
    p.add_argument("--session-id", required=True, help="Governing session ID")
    p.add_argument("--actor-id", required=True, help="Calling actor ID")
    p.add_argument(
        "--phase",
        required=True,
        choices=["session_end", "phase_boundary", "retry_limit", "manual"],
        help="RSI phase trigger",
    )
    p.add_argument(
        "--entropy-delta", default="0.0", help="ΔS measured for this session (float)"
    )
    p.add_argument(
        "--bottlenecks", default="", help="Comma-separated list of observed bottlenecks"
    )
    p.add_argument(
        "--fixes", default="", help="Comma-separated list of fixes installed"
    )
    p.add_argument("--ledger-path", default=LEDGER_PATH, help="Override ledger path")
    return p.parse_args()


def ensure_ledger(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def compute_checksum(entry):
    """Minimal integrity stub — hash the JSON-sorted keys."""
    import hashlib

    raw = json.dumps(entry, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def main():
    args = parse_args()

    try:
        delta_s = float(args.entropy_delta)
    except ValueError:
        delta_s = 0.0

    bottlenecks = [b.strip() for b in args.bottlenecks.split(",") if b.strip()]
    fixes = [f.strip() for f in args.fixes.split(",") if f.strip()]

    entry = {
        "session_id": args.session_id,
        "actor_id": args.actor_id,
        "phase": args.phase,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "entropy_delta": delta_s,
        "bottlenecks": bottlenecks,
        "fixes_installed": fixes,
        "verdict": "SEAL"
        if fixes and delta_s <= 0
        else ("HOLD" if delta_s > 0 else "OBSERVE_ONLY"),
    }
    entry["checksum"] = compute_checksum(entry)

    ensure_ledger(args.ledger_path)
    with open(args.ledger_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Phase 5: emit SEAL receipt
    print(
        json.dumps(
            {
                "status": "SEAL",
                "session_id": args.session_id,
                "phase": args.phase,
                "entropy_delta": delta_s,
                "bottleneck_count": len(bottlenecks),
                "fix_count": len(fixes),
                "ledger_path": args.ledger_path,
                "checksum": entry["checksum"],
            },
            indent=2,
        )
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
