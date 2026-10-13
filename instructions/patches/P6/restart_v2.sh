#!/usr/bin/env bash
# PATCH 6 authoritative restart v2: kill, wait, start once, verify, smoke.
set -e
TS() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
LOG=/root/AAA/instructions/patches/P6/restart_v2.log

echo "[$(TS)] v2-restart begin" | tee -a "$LOG"
# 1. Capture prior ownership.
PRE_PIDS=$(pgrep -f "/root/HERMES/mcp/hermes-rasa/server.py" || true)
PRE_PID=$(echo "$PRE_PIDS" | head -n1)
echo "[$(TS)] pre-PIDs: $PRE_PIDS" | tee -a "$LOG"
echo "[$(TS)] pre-PID (selected): $PRE_PID" | tee -a "$LOG"

# 2. Kill them all, TERM then KILL.
if [ -n "$PRE_PIDS" ]; then
  for p in $PRE_PIDS; do
    kill -TERM "$p" 2>/dev/null || true
  done
  for i in $(seq 1 30); do
    if ! ss -tlnp 2>/dev/null | grep -q ':18420 '; then
      echo "[$(TS)] port 18420 free after $((i*200))ms" | tee -a "$LOG"
      break
    fi
    sleep 0.2
  done
  for p in $PRE_PIDS; do
    kill -KILL "$p" 2>/dev/null || true
  done
  sleep 0.5
fi

# 3. Confirm nobody else owns the port before we start.
if ss -tlnp 2>/dev/null | grep -q ':18420 '; then
  echo "[$(TS)] ABORT: port still bound" | tee -a "$LOG"
  exit 1
fi

# 4. Start one fresh server.
nohup /usr/bin/python3 /root/HERMES/mcp/hermes-rasa/server.py --port 18420 --transport http \
  > /root/AAA/instructions/patches/P6/server.stdout.log 2>&1 &
NEW_PID=$!
disown
echo "[$(TS)] launched new PID: $NEW_PID" | tee -a "$LOG"

# 5. Wait for bind.
for i in $(seq 1 80); do
  if ss -tlnp 2>/dev/null | grep -q ':18420 '; then
    echo "[$(TS)] port bound after $((i*200))ms" | tee -a "$LOG"
    break
  fi
  sleep 0.2
done

# 6. Verify ownership.
echo "[$(TS)] final owners:" | tee -a "$LOG"
pgrep -af "/root/HERMES/mcp/hermes-rasa/server.py" | tee -a "$LOG"
ss -tlnp 2>/dev/null | grep 18420 | tee -a "$LOG"
echo "[$(TS)] restart_v2 done" | tee -a "$LOG"
