#!/bin/bash
# watchdog-heartbeat.sh — direct shell-based gateway health check
# Bypasses model entirely. No LLM, no session stall risk.
set -e

GATEWAY_URL="${GATEWAY_URL:-http://127.0.0.1:18789}"
TIMEOUT=5
WATCHDOG_FILE="/tmp/watchdog_last_beat"

# Primary check: gateway health endpoint
HEALTH=$(curl -sf --max-time "$TIMEOUT" "$GATEWAY_URL/health" 2>/dev/null || echo '{"ok":false}')

# Check if health endpoint returned ok
if echo "$HEALTH" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('ok') else 1)" 2>/dev/null; then
    echo "WATCHDOG_BEAT_OK"
    date +%s > "$WATCHDOG_FILE"
    exit 0
fi

# UNHEALTHY — try doctor + restart
curl -sf --max-time "$TIMEOUT" "$GATEWAY_URL/doctor" >/dev/null 2>&1 || true
sleep 5

# Re-check health after doctor
HEALTH2=$(curl -sf --max-time "$TIMEOUT" "$GATEWAY_URL/health" 2>/dev/null || echo '{"ok":false}')
if echo "$HEALTH2" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('ok') else 1)" 2>/dev/null; then
    echo "WATCHDOG_RESTORE_TRIGGERED"
    exit 0
fi

# Still unhealthy — try openclaw restart
openclaw gateway restart 2>/dev/null || true
sleep 15

# Final check
HEALTH3=$(curl -sf --max-time "$TIMEOUT" "$GATEWAY_URL/health" 2>/dev/null || echo '{"ok":false}')
if echo "$HEALTH3" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('ok') else 1)" 2>/dev/null; then
    echo "WATCHDOG_RESTORE_TRIGGERED"
else
    echo "WATCHDOG_UNHEALTHY"
    exit 1
fi
