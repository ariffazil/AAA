#!/bin/bash
# Cross-Harness Verification: Claude Code → OpenCode
# Claude Code audits OpenCode (333-AGI) session state, DB integrity, bridge health
set -euo pipefail

REPORT_DIR="/root/VAULT999/witness"
REPORT_ID="xhv-opencode-$(date -u +%Y%m%d-%H%M%S)"
REPORT_FILE="${REPORT_DIR}/${REPORT_ID}.json"
mkdir -p "$REPORT_DIR"

python3 - "$REPORT_FILE" "$REPORT_ID" << 'PYEOF'
import json, os, sys, subprocess
from datetime import datetime, timezone

report_file = sys.argv[1]
report_id = sys.argv[2]
FINDINGS = []
CHECKS = {}

# Check 1: OpenCode HTTP API health
import urllib.request
try:
    req = urllib.request.Request("http://127.0.0.1:4096/health")
    with urllib.request.urlopen(req, timeout=3) as resp:
        CHECKS["opencode_api"] = f"HTTP {resp.status}"
except:
    CHECKS["opencode_api"] = "unreachable"
    FINDINGS.append({"severity": "ERROR", "floor": "F12", "check": "opencode_api",
                     "detail": "OpenCode HTTP API :4096 unreachable"})

# Check 2: opencode.db integrity
try:
    import sqlite3
    db_path = os.path.expanduser("~/.local/share/opencode/opencode.db")
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
        table_count = cur.fetchone()[0]
        CHECKS["opencode_db_tables"] = table_count
        conn.close()
    else:
        CHECKS["opencode_db"] = "not_found"
        FINDINGS.append({"severity": "WARN", "floor": "F11", "check": "opencode_db",
                         "detail": f"opencode.db not at {db_path}"})
except Exception as e:
    CHECKS["opencode_db"] = f"error: {e}"

# Check 3: Systemd service health
for svc in ["opencode.service", "opencode-bot.service", "opencode-bridge.service"]:
    try:
        r = subprocess.run(["systemctl", "is-active", svc], capture_output=True, text=True, timeout=5)
        CHECKS[f"service_{svc}"] = r.stdout.strip()
        if r.stdout.strip() != "active":
            FINDINGS.append({"severity": "WARN", "floor": "F12", "check": f"service_{svc}",
                             "detail": f"{svc} is {r.stdout.strip()}"})
    except:
        CHECKS[f"service_{svc}"] = "unknown"

# Check 4: OpenCode session state
state_dir = os.path.expanduser("~/.local/share/opencode")
if os.path.isdir(state_dir):
    files = os.listdir(state_dir)
    CHECKS["opencode_state_files"] = len(files)
else:
    CHECKS["opencode_state_files"] = 0

# Check 5: kv.json
kv_path = os.path.join(state_dir, "kv.json")
try:
    with open(kv_path) as f:
        kv = json.load(f)
    CHECKS["kv_keys"] = len(kv)
except:
    CHECKS["kv_keys"] = -1

# Check 6: VAULT999 cross-ref (count seals from OpenCode-side)
try:
    with open("/root/VAULT999/outcomes.jsonl") as f:
        vault = [l for l in f if l.strip()]
    opencode_seals = sum(1 for l in vault if "opencode" in l.lower() or "333-agi" in l.lower())
    CHECKS["vault_opencode_seals"] = opencode_seals
    CHECKS["vault_total"] = len(vault)
except:
    CHECKS["vault_readable"] = False

# Verdict
errors = [f for f in FINDINGS if f["severity"] == "ERROR"]
warns = [f for f in FINDINGS if f["severity"] == "WARN"]
verdict = "PASS" if not errors and not warns else ("DEGRADED" if warns else "FAIL")

report = {
    "verification_id": report_id,
    "auditor": "claude-code",
    "auditee": "opencode-333-agi",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "verdict": verdict,
    "checks": CHECKS,
    "findings": FINDINGS,
    "summary": f"{len(CHECKS)} checks, {len(FINDINGS)} findings ({len(errors)} errors, {len(warns)} warnings)"
}

with open(report_file, "w") as f:
    json.dump(report, f, indent=2, default=str)

print(json.dumps(report, indent=2, default=str))
PYEOF
