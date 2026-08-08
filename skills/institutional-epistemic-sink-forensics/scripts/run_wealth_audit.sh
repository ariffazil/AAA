#!/usr/bin/env bash
# run_wealth_audit.sh — bash wrapper for activating GEOX venv and running an institutional epistemic-sink audit
#
# Usage: bash scripts/run_wealth_audit.sh /path/to/audit_script.py
#
# The audit script must:
#   1. Import from fastmcp.client
#   2. Connect to http://127.0.0.1:18082/mcp (WEALTH)
#   3. Drive the 11-tool pattern: conservation, flow, emv, survival,
#      collapse_signature, beautiful_mouse, capture_scan, power_audit,
#      omni_wisdom, judge_handoff, vault_write
#   4. Output results as JSON to stdout (or write to a Markdown receipt)
#
# Validated 2026-07-03 against the live WEALTH daemon (port 18082).

set -euo pipefail

# Find the GEOX venv (it has fastmcp pre-installed)
VENV_PATH="/root/GEOX/.venv"
if [ ! -d "$VENV_PATH" ]; then
  VENV_PATH="/root/geox/.venv"
fi
if [ ! -d "$VENV_PATH" ]; then
  echo "ERROR: GEOX venv not found at /root/GEOX/.venv or /root/geox/.venv"
  echo "Activate the WEALTH venv manually or install fastmcp."
  exit 1
fi

# Verify WEALTH is alive
echo "Probing WEALTH at http://127.0.0.1:18082/health..."
HEALTH=$(curl -sf -m 5 http://127.0.0.1:18082/health || echo "")
if [ -z "$HEALTH" ]; then
  echo "ERROR: WEALTH daemon not reachable on port 18082"
  echo "Start it with: cd /root/WEALTH && source .venv/bin/activate && python internal/monolith.py"
  exit 1
fi
echo "WEALTH alive: $(echo "$HEALTH" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("status", "?"))')"

# Run the audit script
AUDIT_SCRIPT="${1:-/tmp/wealth_audit.py}"
if [ ! -f "$AUDIT_SCRIPT" ]; then
  echo "ERROR: Audit script not found: $AUDIT_SCRIPT"
  echo "Usage: bash $0 /path/to/audit_script.py"
  exit 1
fi

echo "Activating GEOX venv at $VENV_PATH..."
# shellcheck disable=SC1091
source "$VENV_PATH/bin/activate"

echo "Running audit script: $AUDIT_SCRIPT"
python3 "$AUDIT_SCRIPT"
echo "Audit script complete."