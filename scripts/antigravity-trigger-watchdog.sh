#!/usr/bin/env bash
# antigravity-trigger-watchdog.sh — watch for trigger file, fire antigravity
# Runs as lightweight daemon via systemd
set -euo pipefail

TRIGGER_FILE="/tmp/antigravity-trigger.txt"
SCRIPT="/root/AAA/scripts/antigravity-autonomous.sh"

echo "[trigger-watch] Daemon started. Watching $TRIGGER_FILE"

# Use inotifywait if available, otherwise poll
if command -v inotifywait &>/dev/null; then
    while true; do
        inotifywait -qq -e create,moved_to,modify "$(dirname "$TRIGGER_FILE")" 2>/dev/null
        if [[ -f "$TRIGGER_FILE" ]]; then
            sleep 1  # Let writer finish
            echo "[trigger-watch] Trigger detected at $(date)"
            bash "$SCRIPT"
        fi
    done
else
    # Fallback: poll every 10 seconds
    while true; do
        sleep 10
        if [[ -f "$TRIGGER_FILE" ]]; then
            echo "[trigger-watch] Trigger detected at $(date)"
            bash "$SCRIPT"
        fi
    done
fi
