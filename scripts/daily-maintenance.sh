#!/bin/bash
# Daily maintenance for arifOS OpenClaw
# Runs at 5 AM MYT (21:00 UTC)
# DITEMPA BUKAN DIBERI

LOG_FILE="/tmp/openclaw-daily-maintenance.log"
FAILURES=""
echo "=== $(date) ===" >> $LOG_FILE

# Self-heal
echo "Running openclaw doctor..." >> $LOG_FILE
openclaw doctor --fix >> $LOG_FILE 2>&1

# Health check
echo "Running health check..." >> $LOG_FILE
openclaw health >> $LOG_FILE 2>&1

# Verify workspace integrity
if [ -d /root/.openclaw/workspace ]; then
    echo "✓ workspace OK" >> $LOG_FILE
else
    echo "✗ workspace MISSING" >> $LOG_FILE
    FAILURES="${FAILURES}\n- workspace MISSING"
fi

# Verify all MCP servers — defaults match the bare-metal systemd runbook.
ARIFOS_PORT="${ARIFOS_PORT:-8088}"
GEOX_PORT="${GEOX_PORT:-8081}"
WEALTH_PORT="${WEALTH_PORT:-18082}"
WELL_PORT="${WELL_PORT:-18083}"
MCP_NAMES=( "arifOS:${ARIFOS_PORT}" "GEOX:${GEOX_PORT}" "WEALTH:${WEALTH_PORT}" "WELL:${WELL_PORT}" )
for mcp in "${MCP_NAMES[@]}"; do
    NAME="${mcp%%:*}"
    PORT="${mcp##*:}"
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://127.0.0.1:$PORT/health)
    if [ "$STATUS" = "200" ]; then
        echo "✓ MCP:$PORT ($NAME) healthy" >> $LOG_FILE
    else
        echo "✗ MCP:$PORT ($NAME) DOWN (HTTP $STATUS)" >> $LOG_FILE
        FAILURES="${FAILURES}\n- MCP $NAME (port $PORT) DOWN"
    fi
done

# Disk check — alert if > 85%
DISK_PCT=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_PCT" -gt 85 ]; then
    echo "✗ Disk $DISK_PCT% used" >> $LOG_FILE
    FAILURES="${FAILURES}\n- Disk ${DISK_PCT}% used (>85%)"
else
    echo "✓ Disk ${DISK_PCT}% used" >> $LOG_FILE
fi

# Telegram alert if any failures
if [ -n "$FAILURES" ]; then
    BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN /root/.openclaw/env.local | cut -d= -f2)
    MSG="⚠️ arifOS Daily Maintenance — ISSUES FOUND:$(echo -e "$FAILURES")\n\nCheck: tail /tmp/openclaw-daily-maintenance.log"
    curl -s "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d "chat_id=267378578" \
        --data-urlencode "text=${MSG}" >> $LOG_FILE 2>&1
    echo "Telegram alert sent" >> $LOG_FILE
else
    echo "✓ All systems healthy — no alert needed" >> $LOG_FILE
fi

echo "Maintenance complete" >> $LOG_FILE
echo "" >> $LOG_FILE
