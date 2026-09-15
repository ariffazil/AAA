#!/bin/bash
# forge-artifact-publisher — Telegram delivery helper
# Usage: deliver_telegram.sh <pdf_path> [caption]
# Exit codes: 0=OK, 1=env missing, 2=file not found, 3=telegram API error
set -euo pipefail

PDF="$1"
CAPTION="${2:-📄 Artifact delivered by arifOS Federation}"

if [ ! -f "$PDF" ]; then
  echo "ERROR [FILE_NOT_FOUND]: $PDF"
  exit 2
fi

# Validate env before sending
if [ ! -f /root/.hermes/.env ]; then
  echo "ERROR [ENV_MISSING]: /root/.hermes/.env not found"
  echo "  Fix: Ensure Hermes is installed and configured"
  exit 1
fi

source /root/.hermes/.env

for var in ASI_ARIFOS_BOT_TOKEN HERMES_SESSION_CHAT_ID; do
  if [ -z "${!var:-}" ]; then
    echo "ERROR [ENV_VAR_MISSING]: $var is empty or unset"
    echo "  Fix: Check /root/.hermes/.env"
    exit 1
  fi
done

RESULT=$(curl -s -X POST "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/sendDocument" \
  -F "chat_id=${HERMES_SESSION_CHAT_ID}" \
  -F "document=@${PDF}" \
  -F "caption=${CAPTION}" \
  -F "parse_mode=HTML")

OK=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('ok', False))" 2>/dev/null || echo "False")

if [ "$OK" = "True" ]; then
  SIZE=$(stat -c%s "$PDF")
  echo "OK: Delivered $(basename $PDF) (${SIZE} bytes) to Telegram chat ${HERMES_SESSION_CHAT_ID}"
else
  ERROR_MSG=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('description', 'unknown'))" 2>/dev/null || echo "parse error")
  echo "ERROR [TELEGRAM_API]: $ERROR_MSG"
  exit 3
fi
