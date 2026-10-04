#!/usr/bin/env python3
"""Ad-hoc verification for a morning-pulse state file (no canonical suite exists).

Usage: python3 verify_pulse.py [YYYY-MM-DD]   # default: today in MYT
Checks: JSON parses, required schema keys, color enum, organs_alive<=organs_total,
exactly 3 macro items, ledger line exists for date and color matches.
Exit 0 = pass, 1 = fail. Prints one-line PASS/FAIL summary.
"""
import json
import sys
from datetime import datetime, timezone, timedelta

MYT = timezone(timedelta(hours=8))
STATE_DIR = "/root/.local/share/arifos/state"
LEDGER = f"{STATE_DIR}/pulse-ledger.tsv"

date = sys.argv[1] if len(sys.argv) > 1 else datetime.now(MYT).strftime("%Y-%m-%d")
path = f"{STATE_DIR}/pulse-{date}.json"
errors = []

try:
    with open(path) as f:
        d = json.load(f)
except Exception as e:
    print(f"FAIL: {path} unreadable/unparseable: {e}")
    sys.exit(1)

for k in ["ts_myt", "day", "date", "readiness", "federation", "macro_top3", "focus_today"]:
    if k not in d:
        errors.append(f"missing top-level key: {k}")

r = d.get("readiness", {})
for k in ["color", "vitality_index", "sleep_hours", "hrv_ms", "fatigue_flag"]:
    if k not in r:
        errors.append(f"readiness missing: {k}")
if r.get("color") not in ("GREEN", "YELLOW", "RED"):
    errors.append(f"bad color: {r.get('color')}")

f = d.get("federation", {})
for k in ["organs_alive", "organs_total", "ollama_up", "aaa_dirty_files", "last_seal_id"]:
    if k not in f:
        errors.append(f"federation missing: {k}")
if f.get("organs_alive", -1) > f.get("organs_total", 0):
    errors.append("organs_alive > organs_total")

m = d.get("macro_top3", [])
if len(m) != 3:
    errors.append(f"macro_top3 has {len(m)} items, expected 3")
for i, item in enumerate(m):
    if not isinstance(item, dict) or "headline" not in item or "why_it_matters" not in item:
        errors.append(f"macro_top3[{i}] malformed")

ledger_line = None
try:
    with open(LEDGER) as lf:
        for line in lf:
            if line.startswith(date + "|"):
                ledger_line = line.strip()
except FileNotFoundError:
    errors.append(f"ledger not found: {LEDGER}")
if not ledger_line:
    errors.append(f"ledger entry for {date} not found")
elif ledger_line.split("|")[1] != r.get("color"):
    errors.append(f"ledger color {ledger_line.split('|')[1]} != state color {r.get('color')}")

if errors:
    print("FAIL:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"PASS: schema valid, 3 macro items, ledger color matches, ts={d['ts_myt']}, day={d['day']}")
