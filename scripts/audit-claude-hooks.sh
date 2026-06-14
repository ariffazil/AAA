#!/bin/bash
# ══════════════════════════════════════════════════════════════════════════════
# Cross-Harness Verification: OpenCode → Claude Code
# ══════════════════════════════════════════════════════════════════════════════
# Purpose:  OpenCode (333-AGI) audits Claude Code's hook logs, session state,
#           and VAULT999 cross-references for constitutional compliance.
# Run by:   OpenCode (333-AGI) periodically or on-demand
# Output:   JSON verification report → /root/VAULT999/witness/
# ══════════════════════════════════════════════════════════════════════════════
set -euo pipefail

REPORT_DIR="/root/VAULT999/witness"
REPORT_ID="xhv-claude-$(date -u +%Y%m%d-%H%M%S)"
REPORT_FILE="${REPORT_DIR}/${REPORT_ID}.json"
SESSION_DIR="/root/.claude/sessions"
HISTORY_FILE="/root/.claude/history.jsonl"
VAULT_FILE="/root/VAULT999/outcomes.jsonl"

mkdir -p "$REPORT_DIR"

python3 - "$REPORT_FILE" "$REPORT_ID" << 'PYEOF'
import json, os, sys
from datetime import datetime, timezone

report_file = sys.argv[1]
report_id = sys.argv[2]

FINDINGS = []
CHECKS = {}

# ── Check 1: Hook log presence (F11 AUDITABILITY) ──
for log in ["precompact.log", "postcompact.log", "stop.log", "seal-confirmations.log"]:
    path = os.path.join("/root/.claude/sessions", log)
    exists = os.path.exists(path)
    CHECKS[f"hook_log_{log}"] = "PRESENT" if exists else "MISSING"
    if not exists:
        FINDINGS.append({"severity": "WARN", "floor": "F11", "check": f"hook_log_{log}",
                         "detail": f"Hook log {log} missing"})

# ── Check 2: seal-confirmations vs VAULT999 ──
try:
    with open("/root/.claude/sessions/seal-confirmations.log") as f:
        seal_lines = [l.strip() for l in f if l.strip()]
    CHECKS["seal_confirmations_count"] = len(seal_lines)
except:
    CHECKS["seal_confirmations_count"] = 0

try:
    with open("/root/VAULT999/outcomes.jsonl") as f:
        vault_entries = [l for l in f if l.strip()]
    vault_seal_count = sum(1 for l in vault_entries if '"verdict": "SEAL"' in l)
    CHECKS["vault_total_entries"] = len(vault_entries)
    CHECKS["vault_seal_count"] = vault_seal_count
except:
    CHECKS["vault_readable"] = False
    FINDINGS.append({"severity": "ERROR", "floor": "F11", "check": "vault_readable",
                     "detail": "Cannot read VAULT999"})

# ── Check 3: PreCompact preservation ──
try:
    with open("/root/.claude/sessions/precompact.log") as f:
        pc = [l for l in f if l.strip()]
    CHECKS["precompact_events"] = len(pc)
except:
    CHECKS["precompact_events"] = 0

# ── Check 4: Stop log ──
try:
    with open("/root/.claude/sessions/stop.log") as f:
        sl = [l for l in f if l.strip()]
    CHECKS["stop_events"] = len(sl)
except:
    CHECKS["stop_events"] = 0

# ── Check 5: History ──
try:
    with open("/root/.claude/history.jsonl") as f:
        hl = [l for l in f if l.strip()]
    CHECKS["history_entries"] = len(hl)
except:
    CHECKS["history_entries"] = -1

# ── Check 6: Ignition directory ──
idir = "/root/.claude/ignition"
pending = [f for f in os.listdir(idir) if f.endswith(".json")] if os.path.isdir(idir) else []
CHECKS["ignition_pending"] = len(pending)
adir = os.path.join(idir, "archive")
archived = len([f for f in os.listdir(adir) if f.endswith(".json")]) if os.path.isdir(adir) else 0
CHECKS["ignition_archived"] = archived

# ── Check 7: arifOS health ──
import urllib.request
try:
    req = urllib.request.Request("http://127.0.0.1:8088/health")
    with urllib.request.urlopen(req, timeout=3) as resp:
        health = json.loads(resp.read())
    CHECKS["arifos_health"] = health.get("status", "unknown")
except:
    CHECKS["arifos_health"] = "unreachable"

# ── Verdict ──
errors = [f for f in FINDINGS if f["severity"] == "ERROR"]
warns = [f for f in FINDINGS if f["severity"] == "WARN"]
verdict = "PASS" if not errors and not warns else ("DEGRADED" if warns else "FAIL")

report = {
    "verification_id": report_id,
    "auditor": "opencode-333-agi",
    "auditee": "claude-code",
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
