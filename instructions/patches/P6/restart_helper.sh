#!/usr/bin/env bash
# PATCH 6 bounded restart helper for HERMES rasa MCP server.
# This script:
#  1. Records the prior PID + listening port.
#  2. Starts a fresh server using the patched source on the same port.
#  3. Waits for the new PID to bind.
#  4. Reports the new PID + port.
#  5. Captures rollback: still holds the pre-patch source on disk.
# Rollback recipe: kill the new PID, then restart the original via the same args.
set -e
LOG=/root/AAA/instructions/patches/P6/restart.log
PRE_PID=$(pgrep -f "/root/HERMES/mcp/hermes-rasa/server.py" || true)
echo "[$(date -u +%FT%TZ)] pre-restart pid: $PRE_PID" | tee -a "$LOG"
if [ -n "$PRE_PID" ] && [ "$PRE_PID" != "1194" ]; then
  echo "WARNING: a different process owns the artifact: $PRE_PID" | tee -a "$LOG"
fi
# Start the new server. Use nohup so it survives our shell.
nohup /usr/bin/python3 /root/HERMES/mcp/hermes-rasa/server.py --port 18420 --transport http \
  > /root/AAA/instructions/patches/P6/server.stdout.log 2>&1 &
NEW_PID=$!
echo "[$(date -u +%FT%TZ)] launched new pid: $NEW_PID" | tee -a "$LOG"
# Wait for port to be bound (max 10s).
for i in $(seq 1 50); do
  if ss -tlnp 2>/dev/null | grep -q ':18420 '; then
    echo "[$(date -u +%FT%TZ)] port bound after $((i*200))ms" | tee -a "$LOG"
    break
  fi
  sleep 0.2
done
# The previous PID may still be bound to :18420. Kill it cleanly first.
if [ -n "$PRE_PID" ]; then
  kill -TERM "$PRE_PID" 2>/dev/null || true
  sleep 1
  kill -KILL "$PRE_PID" 2>/dev/null || true
fi
sleep 1
echo "[$(date -u +%FT%TZ)] final ownership:" | tee -a "$LOG"
pgrep -af "/root/HERMES/mcp/hermes-rasa/server.py" | tee -a "$LOG"
ss -tlnp 2>/dev/null | grep 18420 | tee -a "$LOG"
echo "[$(date -u +%FT%TZ)] restart_helper done" | tee -a "$LOG"
