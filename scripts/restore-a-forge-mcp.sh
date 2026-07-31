#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
# restore-a-forge-mcp.sh — Restore a-forge-mcp systemd service
# ══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# 1. Kill manual processes on port 7072
echo "Killing manual processes on port 7072..."
# Kill any node process listening or running serve.js on port 7072
PID=$(ps aux | grep "serve.js --transport=http --port=7072" | grep -v grep | awk '{print $2}' || echo "")
if [ -n "$PID" ]; then
    echo "Found manual process PID: $PID. Killing..."
    kill -9 $PID || true
else
    echo "No manual port 7072 process found."
fi

# 2. Start systemd service
echo "Starting a-forge-mcp.service..."
systemctl stop a-forge-mcp 2>/dev/null || true
systemctl start a-forge-mcp

# 3. Print status
echo "Checking service status..."
systemctl status a-forge-mcp --no-pager | head -n 15

# 4. Verify health response
echo "Verifying health..."
sleep 2
curl -s http://127.0.0.1:7072/health | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f'status={d.get(\"status\")} tools={d.get(\"stateless_tools\",\"?\")}')
except Exception as e:
    print('Failed to parse health:', e)
" || echo "Curl to port 7072 failed"
