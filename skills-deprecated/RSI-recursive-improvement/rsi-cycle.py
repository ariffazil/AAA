#!/usr/bin/env python3
"""
rsi-cycle.py — Recursive Self-Improvement Cycle Executor
Executes Phase 1-4 of the RSI protocol and writes to rsi-ledger.jsonl.

Usage:
    python3 rsi-cycle.py \
      --session-id "SEAL-xxx" \
      --actor-id "333-AGI" \
      --phase "session_end" \
      --trace-json '{"tool_calls":{"total":10,"success":9,"failed":1}}' \
      --bottleneck "EVIDENCE_GAP" \
      --fix "Patched identity_hash probe" \
      --delta-entropy -0.3

Returns: JSON receipt to stdout
Writes:  /root/.local/share/arifos/rsi-ledger.jsonl (append)
"""

import argparse, json, os, sys, hashlib
from datetime import datetime, timezone

LEDGER_PATH = "/root/.local/share/arifos/rsi-ledger.jsonl"
BOTTLENECKS = [
    "REPETITION",
    "EVIDENCE_GAP",
    "TOOL_DRIFT",
    "SCOPE_CREEP",
    "OVERCONFIDENCE",
    "SKILL_BLOAT",
    "ABANDONED_PATH",
    "ORPHAN_RESULT",
    "RECURRENCE",
    "ENTROPY_GAIN",
    "NONE",
]
PHASES = [
    "session_end",
    "phase_boundary",
    "repetition_alert",
    "gate_fire",
    "mid_session",
]


def parse_args():
    p = argparse.ArgumentParser(description="RSI Cycle — Recursive Self-Improvement")
    p.add_argument("--session-id", required=True)
    p.add_argument("--actor-id", required=True)
    p.add_argument("--phase", required=True, choices=PHASES)
    p.add_argument("--trace-json", default="{}", help="JSON string of trace data")
    p.add_argument("--bottleneck", required=True, choices=BOTTLENECKS)
    p.add_argument("--bottleneck-detail", default="", help="One-line explanation")
    p.add_argument(
        "--fix", required=True, help="What was installed to fix the bottleneck"
    )
    p.add_argument("--fix-reversible", type=bool, default=True)
    p.add_argument(
        "--delta-entropy", type=float, required=True, help="ΔS from before to after"
    )
    p.add_argument(
        "--next-session-hint", default="", help="What next session should watch for"
    )
    p.add_argument(
        "--confidence-band", default="HIGH", choices=["HIGH", "MEDIUM", "LOW"]
    )
    return p.parse_args()


def main():
    args = parse_args()

    try:
        trace = json.loads(args.trace_json)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid trace-json: {e}"}), file=sys.stderr)
        sys.exit(1)

    entry = {
        "schema": "rsi.v2",
        "session_id": args.session_id,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "actor_id": args.actor_id,
        "phase": args.phase,
        "trace": trace,
        "bottleneck": args.bottleneck,
        "bottleneck_detail": args.bottleneck_detail or args.bottleneck,
        "fix_installed": args.fix,
        "fix_reversible": args.fix_reversible,
        "delta_entropy": args.delta_entropy,
        "confidence_band": args.confidence_band,
        "next_session_hint": args.next_session_hint,
    }

    # Validate
    if (
        args.phase in ("session_end", "phase_boundary", "gate_fire")
        and not args.bottleneck_detail
    ):
        print(
            json.dumps(
                {"warning": "No bottleneck_detail provided for mandatory phase"}
            ),
            file=sys.stderr,
        )

    # Write ledger
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    line = json.dumps(entry, sort_keys=True)
    with open(LEDGER_PATH, "a") as f:
        f.write(line + "\n")

    # Compute hash for receipt
    entry_hash = hashlib.sha256(line.encode()).hexdigest()[:16]

    # Emit receipt
    receipt = {
        "status": "RSI_CYCLE_COMPLETE",
        "entry_hash": f"sha256:{entry_hash}",
        "ledger_path": LEDGER_PATH,
        "bottleneck": args.bottleneck,
        "fix_installed": args.fix,
        "delta_entropy": args.delta_entropy,
        "doctrine": "DITEMPA BUKAN DIBERI",
    }
    print(json.dumps(receipt, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
