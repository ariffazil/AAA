#!/usr/bin/env bash
# Probe the Hermes Telegram webhook with a synthetic group message.
# Usage: bash sado_probe.sh [chat_id] [user_id] [text]
# Defaults: chat_id=-1003815535761 (SADO), user_id=267378578 (Arif), text=SYNTHETIC_PROBE
#
# Requires: running hermes-asi-gateway.service, curl, strings
#
# Returns:
#   HTTP status code from the webhook endpoint
#   "PROCESSED" if gateway.log gains an inbound/flush entry within 5s
#   "SILENT DROP" if HTTP 200 but no new log entries appear
#   "AUTH FAIL" if HTTP 403

set -euo pipefail

CHAT_ID="${1:--1003815535761}"
USER_ID="${2:-267378578}"
TEXT="${3:-SYNTHETIC_PROBE_$(date +%s)}"
PORT="${WEBHOOK_PORT:-8444}"

PID=$(systemctl show -p MainPID hermes-asi-gateway.service 2>/dev/null | cut -d= -f2 || true)
if [ -z "$PID" ] || [ "$PID" = "0" ]; then
  echo "ERROR: hermes-asi-gateway.service not running" >&2
  exit 1
fi

SECRET=$(strings /proc/"$PID"/environ 2>/dev/null | grep '^TELEGRAM_WEBHOOK_SECRET=' | cut -d= -f2 || true)
if [ -z "$SECRET" ]; then
  echo "ERROR: no TELEGRAM_WEBHOOK_SECRET in process env" >&2
  exit 1
fi

LOG="/usr/local/lib/hermes-agent/profiles/aaa-hermes/logs/gateway.log"
BEFORE=$(wc -l < "$LOG" 2>/dev/null || echo 0)
UPDATE_ID=$(( RANDOM * RANDOM ))

RESPONSE=$(curl -sS -w "\n%{http_code}" \
  -H "X-Telegram-Bot-Api-Secret-Token: $SECRET" \
  -H "Content-Type: application/json" \
  -d "{\"update_id\":$UPDATE_ID,\"message\":{\"message_id\":$UPDATE_ID,\"from\":{\"id\":$USER_ID,\"is_bot\":false,\"first_name\":\"TESTER\"},\"chat\":{\"id\":$CHAT_ID,\"title\":\"TEST\",\"type\":\"supergroup\"},\"date\":$(date +%s),\"text\":\"$TEXT\"}}" \
  "http://127.0.0.1:${PORT}/telegram/webhook" 2>/dev/null) || true

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
echo "HTTP $HTTP_CODE  |  update_id=$UPDATE_ID"

if [ "$HTTP_CODE" = "403" ]; then
  echo "→ AUTH FAIL (secret mismatch)"
  exit 1
fi

sleep 3

AFTER=$(wc -l < "$LOG" 2>/dev/null || echo 0)
NEW=$(( AFTER - BEFORE ))

if [ "$NEW" -gt 0 ]; then
  echo "→ PROCESSED ($NEW new log line(s))"
  tail -n +"$((BEFORE+1))" "$LOG" | grep -v "Blocked unauthorized user 8410138119" | head -5
else
  echo "→ SILENT DROP (HTTP $HTTP_CODE, no new log entries)"
  echo "  The webhook accepted the update but the handler did not fire."
  echo "  Check adapter.py gating chain or python-telegram-bot update dispatch."
fi
