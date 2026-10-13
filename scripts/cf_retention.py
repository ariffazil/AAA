#!/usr/bin/env python3
"""
carry_forward retention: hourly=24, daily=14, weekly=8, sealed=permanent.
Run by cron daily. Removes backups older than retention window.
Sealed entries (session_seal) are NEVER deleted.

Usage: python3 /root/AAA/scripts/cf_retention.py
"""
import os, glob, time, json
from datetime import datetime, timezone, timedelta

BACKUP_DIRS = {
    "/root/.hermes/carry_forward_backups": {"hourly": 24, "daily": 14, "weekly": 8},
}

KEEP_TOKEN = "sealed"  # session_seal entries (immutable, keep forever)

now = time.time()
removed = 0
kept = 0

for backup_dir, windows in BACKUP_DIRS.items():
    if not os.path.isdir(backup_dir):
        continue
    for f in glob.glob(os.path.join(backup_dir, "*")):
        if not os.path.isfile(f):
            continue
        age_hours = (now - os.path.getmtime(f)) / 3600
        # Check if this is a sealed snapshot
        is_sealed = KEEP_TOKEN in os.path.basename(f).lower()
        if is_sealed:
            kept += 1
            continue
        # Apply retention: hourly<24h, daily<14d, weekly<8w
        if age_hours > windows["weekly"] * 24 * 7:
            os.remove(f)
            removed += 1
        elif age_hours > windows["daily"] * 24:
            os.remove(f)
            removed += 1
        elif age_hours > windows["hourly"]:
            os.remove(f)
            removed += 1
        else:
            kept += 1

print(f"carry_forward retention: kept={kept} removed={removed} ts={datetime.now(timezone.utc).isoformat()}")
