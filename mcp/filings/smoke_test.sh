#!/usr/bin/env bash
# filings-mcp smoke test — starts the server, drives it with a real MCP client,
# stops the server. Exits non-zero on any failed check.
#
#   ./smoke_test.sh            # uses cached responses where warm
#   FRESH=1 ./smoke_test.sh    # wipes cache/ first (proves live fetch)
set -uo pipefail
cd "$(dirname "$0")"

PY=/opt/arifos/venv/bin/python
PORT=18410
LOG=/tmp/filings-mcp-smoke.log

if [[ "${FRESH:-0}" == "1" ]]; then
  echo ">> FRESH=1: clearing cache/ to prove live network fetch"
  rm -rf cache; mkdir -p cache
fi

echo ">> starting filings-mcp on 127.0.0.1:$PORT"
"$PY" server.py >"$LOG" 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null; wait $SRV 2>/dev/null' EXIT

for i in $(seq 1 40); do
  if "$PY" - <<'EOF' 2>/dev/null
import socket,sys
s=socket.socket(); s.settimeout(0.4)
sys.exit(0 if s.connect_ex(("127.0.0.1",18410))==0 else 1)
EOF
  then break; fi
  sleep 0.5
done

if ! kill -0 $SRV 2>/dev/null; then
  echo ">> SERVER DIED. log:"; cat "$LOG"; exit 2
fi
echo ">> server up (pid $SRV), running MCP client checks"
echo "-----------------------------------------------------"

"$PY" smoke_test.py
RC=$?
echo "-----------------------------------------------------"
echo ">> client exit code: $RC"
if [[ $RC -ne 0 ]]; then echo ">> server log:"; cat "$LOG"; fi
exit $RC
