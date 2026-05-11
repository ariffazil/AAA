#!/bin/bash
# Daily maintenance for arifOS OpenClaw
# Runs at 5 AM MYT (21:00 UTC)

LOG_FILE="/tmp/openclaw-daily-maintenance.log"
echo "=== $(date) ===" >> $LOG_FILE

# Self-heal
echo "Running openclaw doctor..." >> $LOG_FILE
openclaw doctor --fix >> $LOG_FILE 2>&1

# Health check
echo "Running health check..." >> $LOG_FILE
openclaw health >> $LOG_FILE 2>&1

# Verify workspace integrity (canonical path)
echo "Checking workspace..." >> $LOG_FILE
if [ -d /root/.openclaw/workspace ]; then
    echo "✓ workspace OK" >> $LOG_FILE
else
    echo "✗ workspace MISSING" >> $LOG_FILE
fi

# Verify active MCP servers
echo "Checking MCP servers..." >> $LOG_FILE
for port in 8080 8081 8082; do
    if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$port/health | grep -q "200"; then
        echo "✓ MCP:$port healthy" >> $LOG_FILE
    else
        echo "✗ MCP:$port DOWN" >> $LOG_FILE
    fi
done

echo "Maintenance complete" >> $LOG_FILE
echo "" >> $LOG_FILE
