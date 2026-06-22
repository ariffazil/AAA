#!/usr/bin/env python3
"""
Prompt Mutation Gate — DSG enforcement for prompt file changes.

When arifOS (or a delegated auditor) proposes a prompt change:

  1. RISK: HIGH — prompt mutation changes agent behavior. Cannot be auto-deployed.
  2. 888_HOLD fires automatically. The prompt file is NOT changed yet.
  3. Arif reviews the diff (read the file, compare hash, decide).
  4. Arif SEALs via `python prompt_mutation_gate.py <organ> seal`.
     Or Arif VOIDs via `python prompt_mutation_gate.py <organ> void --reason "..."`.
  5. If SEAL: the prompt file is the new canonical. Bot reloads on next session.
  6. If VOID: prompt file is unchanged. Audit log records the rejection.

This script is the gate. It does NOT itself modify the prompt file —
it records intent and audit. The actual file edit happens separately,
and arifOS issues the SEAL only after the file is in its proposed form.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

PROMPTS_DIR = Path("/root/AAA/agents/prompts")
AUDIT_LOG = Path("/root/AAA/agents/prompt_mutations.log")
VALID_ORGANS = ("LIBRA", "HERMES", "CLAW", "FORGE")


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append_audit(record: dict) -> None:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def cmd_propose(organ: str, reason: str) -> int:
    """Stage a prompt mutation proposal. Triggers 888_HOLD."""
    if organ not in VALID_ORGANS:
        print(f"ERROR: unknown organ {organ!r}", file=sys.stderr)
        return 2

    path = PROMPTS_DIR / f"{organ}.md"
    if not path.exists():
        print(f"ERROR: prompt file not found: {path}", file=sys.stderr)
        return 2

    current_hash = file_hash(path)
    record = {
        "action": "PROPOSE",
        "organ": organ,
        "current_hash": current_hash,
        "reason": reason,
        "timestamp": now_iso(),
        "verdict": "HOLD",
    }
    append_audit(record)

    print(f"888_HOLD: prompt mutation proposed for {organ}")
    print(f"  current_hash: {current_hash}")
    print(f"  file:         {path}")
    print()
    print("NEXT STEPS:")
    print(f"  1. Review the prompt file: {path}")
    print(f"  2. If approved: python prompt_mutation_gate.py {organ} seal")
    print(
        f"  3. If rejected: python prompt_mutation_gate.py {organ} void --reason '...'"
    )
    return 0


def cmd_seal(organ: str) -> int:
    """Arif SEALs the proposed prompt mutation. Verifies the hash matches the proposal."""
    if organ not in VALID_ORGANS:
        print(f"ERROR: unknown organ {organ!r}", file=sys.stderr)
        return 2

    path = PROMPTS_DIR / f"{organ}.md"
    if not path.exists():
        print(f"ERROR: prompt file not found: {path}", file=sys.stderr)
        return 2

    # Find the most recent PROPOSE for this organ
    if not AUDIT_LOG.exists():
        print(
            f"ERROR: no PROPOSE found for {organ}. Run `propose` first.",
            file=sys.stderr,
        )
        return 2

    last_propose = None
    with AUDIT_LOG.open() as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("action") == "PROPOSE" and rec.get("organ") == organ:
                last_propose = rec

    if last_propose is None:
        print(f"ERROR: no PROPOSE found for {organ}.", file=sys.stderr)
        return 2

    new_hash = file_hash(path)
    record = {
        "action": "SEAL",
        "organ": organ,
        "proposed_hash": last_propose.get("current_hash"),
        "new_hash": new_hash,
        "timestamp": now_iso(),
        "verdict": "SEAL",
    }
    append_audit(record)

    if new_hash == last_propose.get("current_hash"):
        print(
            "WARNING: new hash matches proposed hash. Did you forget to edit the file?"
        )
        print(f"  proposed: {last_propose.get('current_hash')}")
        print(f"  current:  {new_hash}")

    print(f"SEAL: {organ} prompt updated. new_hash={new_hash}")
    print("  Bot will read the new prompt on next session start.")
    print("  (bot detects change via prompt_loader.detect_prompt_change)")
    return 0


def cmd_void(organ: str, reason: str) -> int:
    """Arif VOIDs the proposed prompt mutation."""
    if organ not in VALID_ORGANS:
        print(f"ERROR: unknown organ {organ!r}", file=sys.stderr)
        return 2

    record = {
        "action": "VOID",
        "organ": organ,
        "reason": reason,
        "timestamp": now_iso(),
        "verdict": "VOID",
    }
    append_audit(record)

    print(f"VOID: {organ} prompt change rejected.")
    print(f"  reason: {reason}")
    print("  audit recorded.")
    return 0


def cmd_status(organ: Optional[str]) -> int:
    """Show audit log, optionally filtered by organ."""
    if not AUDIT_LOG.exists():
        print("No prompt mutations recorded yet.")
        return 0

    with AUDIT_LOG.open() as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if organ is None or rec.get("organ") == organ:
                ts = rec.get("timestamp", "?")
                action = rec.get("action", "?")
                org = rec.get("organ", "?")
                verdict = rec.get("verdict", "?")
                print(f"  {ts} | {action:<8} | {org:<8} | {verdict}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prompt Mutation Gate — DSG enforcement for prompt file changes"
    )
    parser.add_argument("organ", nargs="?", choices=VALID_ORGANS, help="Organ name")
    parser.add_argument(
        "action",
        choices=["propose", "seal", "void", "status"],
        help="Action to take",
    )
    parser.add_argument(
        "--reason",
        default="(no reason given)",
        help="Reason for propose/void",
    )

    args = parser.parse_args()

    if args.action == "status":
        return cmd_status(args.organ)
    if not args.organ:
        print("ERROR: organ required for propose/seal/void", file=sys.stderr)
        return 2

    if args.action == "propose":
        return cmd_propose(args.organ, args.reason)
    if args.action == "seal":
        return cmd_seal(args.organ)
    if args.action == "void":
        return cmd_void(args.organ, args.reason)

    return 0


if __name__ == "__main__":
    sys.exit(main())
