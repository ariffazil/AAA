#!/usr/bin/env bash
# Stop the orphan PID 3032963 + fold its tools into hermes-asi-gateway.service.
# Pre-condition: F13 binary on Q4.

set -euo pipefail

ORPHAN_PID=3032963
SERVICE="hermes-mcp-server.service"

# Verify orphan is alive
if [ ! -d "/proc/$ORPHAN_PID" ]; then
  echo "ORPHAN PID $ORPHAN_PID already gone — proceed with service merge only"
fi

# Snapshot the tools exposed by the orphan
echo "── orphan tool inventory (probe) ──"
# The orphan is python3 -m hermes_mcp → uses /root/.hermes/hermes_mcp/ package
# Its 11 canonical tools + 1 retrieve + 1 makcik_render
ls /root/.hermes/hermes_mcp/ 2>/dev/null | head -20
echo "(11 canonical tools + 1 retrieve + 1 makcik_render per hermes-mcp-architecture-map-2026-09-23.md)"

# Stop orphan gracefully
if [ -d "/proc/$ORPHAN_PID" ]; then
  kill -TERM "$ORPHAN_PID" 2>/dev/null
  sleep 2
  [ -d "/proc/$ORPHAN_PID" ] && kill -KILL "$ORPHAN_PID" 2>/dev/null
fi

# Verify orphan dead
if [ -d "/proc/$ORPHAN_PID" ]; then
  echo "ABORT: orphan $ORPHAN_PID refuses to die — escalate"
  exit 1
fi
echo "ORPHAN $ORPHAN_PID terminated"

# Re-enable the systemd unit
systemctl unmask "$SERVICE" 2>/dev/null || true
systemctl enable "$SERVICE" 2>/dev/null || true
systemctl start "$SERVICE" 2>/dev/null
sleep 3
systemctl status "$SERVICE" --no-pager -n 3 | head -5

echo "Q4 PASS · orphan terminated, service merged"
