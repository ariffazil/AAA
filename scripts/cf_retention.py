#!/usr/bin/env python3
"""
carry_forward retention: keep the last KEEP_HOURS of regular backups plus ALL
sealed snapshots; delete the rest. Run by cron daily.

Sealed entries (session_seal) are NEVER deleted. The live filename convention is
"...-SEAL-<hash>.json", so the guard matches "seal", not "sealed".

Void Guard: a missing target directory is recorded and surfaced, never silently
skipped. "No data" is not "all clear" — it means the pruner cannot witness.

Usage: python3 /root/AAA/scripts/cf_retention.py [--dry-run]
Exit: 0 ok · 1 primary dir missing · 2 unexpected error
"""
import glob
import json
import os
import sys
import time
from datetime import datetime, timezone

# First entry is PRIMARY: its absence is a hard failure, not a skip.
BACKUP_DIRS = [
    "/root/.local/share/arifos/carry_forward_backups",
    "/root/.hermes/carry_forward_backups",
]

KEEP_HOURS = 24
SEAL_TOKEN = "seal"  # matches -SEAL-<hash>, _seal_, sealed
RECEIPT = "/root/.local/share/arifos/cf_retention_receipt.jsonl"


def is_sealed(path: str) -> bool:
    return SEAL_TOKEN in os.path.basename(path).lower()


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    now = time.time()
    per_dir = []
    total_removed = 0
    total_kept = 0
    total_bytes_freed = 0

    for idx, backup_dir in enumerate(BACKUP_DIRS):
        primary = idx == 0
        if not os.path.isdir(backup_dir):
            # Witnessed absence, not a silent continue.
            per_dir.append({"dir": backup_dir, "status": "ABSENT", "primary": primary})
            continue

        removed = kept = sealed_kept = bytes_freed = 0
        for f in glob.glob(os.path.join(backup_dir, "*")):
            if not os.path.isfile(f):
                continue
            if is_sealed(f):
                sealed_kept += 1
                kept += 1
                continue
            age_hours = (now - os.path.getmtime(f)) / 3600
            if age_hours > KEEP_HOURS:
                if not dry_run:
                    try:
                        size = os.path.getsize(f)
                        os.remove(f)
                        bytes_freed += size
                    except OSError:
                        continue
                else:
                    bytes_freed += os.path.getsize(f)
                removed += 1
            else:
                kept += 1

        per_dir.append(
            {
                "dir": backup_dir,
                "status": "DRY_RUN" if dry_run else "OK",
                "primary": primary,
                "removed": removed,
                "kept": kept,
                "sealed_kept": sealed_kept,
                "bytes_freed": bytes_freed,
            }
        )
        total_removed += removed
        total_kept += kept
        total_bytes_freed += bytes_freed

    receipt = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "keep_hours": KEEP_HOURS,
        "removed": total_removed,
        "kept": total_kept,
        "bytes_freed": total_bytes_freed,
        "dirs": per_dir,
    }

    if not dry_run:
        try:
            os.makedirs(os.path.dirname(RECEIPT), exist_ok=True)
            with open(RECEIPT, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(receipt, separators=(",", ":")) + "\n")
        except OSError:
            pass

    absent_primary = any(d.get("primary") and d["status"] == "ABSENT" for d in per_dir)
    receipt_json = json.dumps(receipt, separators=(",", ":"))

    if absent_primary:
        # Fail loud so cron surfaces a non-zero exit instead of a green no-op.
        print(f"carry_forward retention FAILED: primary dir absent — {receipt_json}")
        return 1

    print(f"carry_forward retention: {receipt_json}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 — cron must see the failure, not a traceback-less 0
        print(f"carry_forward retention ERROR: {type(exc).__name__}: {exc}")
        sys.exit(2)
