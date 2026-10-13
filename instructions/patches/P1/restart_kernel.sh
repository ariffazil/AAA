#!/usr/bin/env bash
# PATCH 1+2+3 bounded kernel restart.
set -e
TS() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
LOG=/root/AAA/instructions/patches/P1/restart.log

# Pin the active owner.
PORT=8088
OLD_PID=$(ss -tlnp 2>/dev/null | awk -v p=":$PORT" '$4 ~ p {match($6, /pid=([0-9]+)/, a); print a[1]}' | head -1)
[ -z "$OLD_PID" ] && OLD_PID=123528
echo "[$(TS)] old PID: $OLD_PID" | tee -a "$LOG"

# Stop it cleanly.
kill -TERM "$OLD_PID" 2>/dev/null || true
sleep 1
for i in $(seq 1 30); do
  if ! ss -tlnp 2>/dev/null | awk -v p=":$PORT" '($4 ~ p){exit 0}' | grep -q .; then break; fi
  sleep 0.2
done
kill -KILL "$OLD_PID" 2>/dev/null || true
sleep 1

# Confirm port is free.
if ss -tlnp 2>/dev/null | awk -v p=":$PORT" '($4 ~ p){exit 0}' | grep -q .; then
  echo "[$(TS)] ABORT: port still bound" | tee -a "$LOG"
  exit 2
fi

# Start a fresh supervisor with the patched source on disk.
nohup /bin/su -s /bin/bash arifos -c "/opt/arifos/current/venv/bin/python -c 'from arifosmcp.runtime.__main__ import main; main()'" \
  > /root/AAA/instructions/patches/P1/kernel.stdout.log 2>&1 &
NEW_PID=$!
disown
echo "[$(TS)] launched new PID: $NEW_PID" | tee -a "$LOG"

# Wait for bind.
for i in $(seq 1 100); do
  if ss -tlnp 2>/dev/null | awk -v p=":$PORT" '($4 ~ p){exit 0}' | grep -q .; then
    echo "[$(TS)] port $PORT bound after $((i*200))ms" | tee -a "$LOG"
    break
  fi
  sleep 0.2
done

# Verify ownership.
echo "[$(TS)] final owners:" | tee -a "$LOG"
ss -tlnp 2>/dev/null | grep -E ":$PORT " | tee -a "$LOG"
# Confirm the new process has the patched judge.py in memory.
sleep 1
ls -la /proc/$(pgrep -f "from arifosmcp.runtime.__main__" | head -1)/cwd 2>/dev/null | tee -a "$LOG"
sha256sum /opt/arifos/current/venv/lib/python3.13/site-packages/arifosmcp/tools/judge.py | tee -a "$LOG"
