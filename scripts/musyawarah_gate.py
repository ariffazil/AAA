#!/usr/bin/env python3
"""Musyawawah NO-Gate — E-3 instance of Gate Promotion doctrine.

F13-ratified 2026-09-08 (DUAL_GO → SEAL via direct implementation directive).
Scans arifFlow ledger for T2/T3 receipts lacking musyawawah_reference.
Pre-MIGRATION_GRACE receipts are exempt.

Fails closed: ledger missing/unreadable OR violations found → exit 1.

Usage:
  musyawawah_gate.py --scan-ledger         scan /var/lib/arifflow/receipts.jsonl
  musyawawah_gate.py --path FILE           scan arbitrary ledger JSONL
  musyawawah_gate.py --since DATE          override MIGRATION_GRACE date (YYYY-MM-DD)
  musyawawah_gate.py --dry-run             report violations without exiting non-zero

Constitutional: F1 AMANAH (fail-closed), F2 TRUTH (real-catch via ledger scan),
                F11 AUDIT (denial log), F13 SOVEREIGN (override pathway preserved).

Per musyawawah.md §4 + §6: "Dual GO is not a SEAL" — this gate enforces the
SEAL phase, after F13 has ratified the underlying musyawawah verdict.

DITEMPA BUKAN DIBERI — Forged 2026-09-08 by FI-003 under F13 APEX Verdict.
"""
import json
import sys
from pathlib import Path

LEDGER = Path("/var/lib/arifflow/receipts.jsonl")
MIGRATION_GRACE = "2026-09-08"

# step_type → action_class mapping (conservative: assume Execute = T2 unless overridden)
T2_T3_STEP_TYPES = {"Seal", "Barrier", "Execute"}


def is_post_grace(created_at: str, grace_date: str) -> bool:
    """Receipt created on/after grace date → subject to gate."""
    if not created_at or len(created_at) < 10:
        return False
    return created_at[:10] >= grace_date


def action_class_of(step_type: str) -> str:
    if step_type in T2_T3_STEP_TYPES:
        return "T2/T3"
    return "T0/T1"


def scan_ledger(ledger: Path, grace_date: str) -> list:
    """Return list of violation tuples: (receipt_id, actor_id, step_type, created_at).

    Fails closed: missing/unreadable ledger → sys.exit(1) before returning.
    """
    if not ledger.is_file():
        print(f"MUSYAWARAH GATE [FAIL-CLOSED]: ledger missing: {ledger}", file=sys.stderr)
        sys.exit(1)
    violations = []
    try:
        with ledger.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue  # malformed row, skip
                step_type = r.get("step_type")
                if step_type not in T2_T3_STEP_TYPES:
                    continue
                created_at = r.get("created_at", "")
                if not is_post_grace(created_at, grace_date):
                    continue  # legacy, exempt under migration grace
                payload = r.get("payload") or {}
                if "musyawawah_reference" in payload:
                    continue  # has reference, OK
                violations.append((
                    r.get("receipt_id", "?"),
                    r.get("actor_id", "?"),
                    step_type,
                    created_at,
                ))
    except OSError as exc:
        print(f"MUSYAWARAH GATE [FAIL-CLOSED]: ledger unreadable: {exc}", file=sys.stderr)
        sys.exit(1)
    return violations


def emit_holds(violations: list, grace_date: str) -> None:
    """Emit holds.txt lines for downstream audit / 666 attention."""
    holds_path = Path("/root/VAULT999/musyawarah/holds.txt")
    holds_path.parent.mkdir(parents=True, exist_ok=True)
    with holds_path.open("a") as f:
        for rid, actor, step, ts in violations:
            f.write(f"HOLD\t{ts}\t{step}\t{actor}\t{rid}\tno_musyawawah_reference\tgrace={grace_date}\n")


def main() -> None:
    args = sys.argv[1:]
    if "--scan-ledger" in args:
        ledger = LEDGER
    elif "--path" in args:
        ledger = Path(args[args.index("--path") + 1])
    else:
        print(__doc__)
        sys.exit(2)

    grace_date = MIGRATION_GRACE
    if "--since" in args:
        grace_date = args[args.index("--since") + 1]

    dry_run = "--dry-run" in args
    emit = "--emit-holds" in args

    violations = scan_ledger(ledger, grace_date)

    if violations:
        if emit:
            emit_holds(violations, grace_date)
        for rid, actor, step, ts in violations:
            action = action_class_of(step)
            print(
                f"MUSYAWARAH GATE [BLOCK]: {action} receipt without musyawawah_reference "
                f"— receipt_id={rid} actor={actor} step={step} created_at={ts}",
                file=sys.stderr,
            )
        if not dry_run:
            sys.exit(1)
        print(f"MUSYAWARAH GATE [DRY-RUN]: {len(violations)} violation(s) (would have blocked)", file=sys.stderr)
    else:
        print(f"MUSYAWARAH GATE [PASS]: all T2/T3 receipts since {grace_date} carry musyawawah_reference")


if __name__ == "__main__":
    main()
