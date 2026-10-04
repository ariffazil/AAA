#!/usr/bin/env python3
"""
recon_fq_from_disk.py — Independent FQ recomputation from durable disk file.

Used by re_audit_drift_check.sh Probe 5 (Reality Reconciliation).
The daemon's /health reports FQ computed from its IN-MEMORY store (window=100).
This script recomputes FQ directly from the durable JSONL file — the disk is
the independent witness of reality.

Output: machine-readable `key=value` lines for easy bash parsing.
"""
import json
import os
import sys

PATH = "/var/lib/arifflow/receipts.jsonl"
WINDOW = 100

if not os.path.exists(PATH):
    print("status=NO_FILE")
    sys.exit(0)

execute = 0
verify = 0
parse_errors = 0
try:
    with open(PATH) as f:
        lines = f.readlines()
except Exception as e:
    print(f"status=READ_ERROR error={e}")
    sys.exit(0)

window_lines = lines[-WINDOW:]
for line in window_lines:
    line = line.strip()
    if not line:
        continue
    try:
        r = json.loads(line)
        st = r.get("step_type", "")
        if st == "Execute":
            execute += 1
        elif st == "Verify":
            verify += 1
    except Exception:
        parse_errors += 1
        continue

fq = (verify / execute) if execute > 0 else 0.0
print(f"status=OK recon_fq={fq:.4f} execute={execute} verify={verify} window={len(window_lines)} parse_errors={parse_errors}")
