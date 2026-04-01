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

# Git status in waw
echo "Checking git status in waw..." >> $LOG_FILE
cd /root/waw && git status >> $LOG_FILE 2>&1

# Verify symlinks
echo "Verifying symlinks..." >> $LOG_FILE
cd /root/waw
for link in AGENTS.md SOUL.md USER.md HEARTBEAT.md IDENTITY.md TOOLS.md BOOT.md; do
    if [ -L "$link" ]; then
        target=$(readlink "$link")
        if [ -e "$target" ]; then
            echo "✓ $link -> $target" >> $LOG_FILE
        else
            echo "✗ $link -> $target (BROKEN)" >> $LOG_FILE
        fi
    fi
done

echo "Maintenance complete" >> $LOG_FILE
echo "" >> $LOG_FILE
