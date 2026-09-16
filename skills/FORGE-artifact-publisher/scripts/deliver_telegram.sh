#!/bin/bash
# forge-artifact-publisher — Telegram delivery helper
# Usage: deliver_telegram.sh <pdf_path> <caption>
set -euo pipefail

PDF="$1"
CAPTION="${2:-📄 Artifact delivered by arifOS GEOX}"

if [ ! -f "$PDF" ]; then
  echo "ERROR: File not found: $PDF"
  exit 1
fi

source /root/.hermes/.env

RESULT=$(curl -s -X POST "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/sendDocument" \
  -F "chat_id=${HERMES_SESSION_CHAT_ID}" \
  -F "document=@${PDF}" \
  -F "caption=${CAPTION}" \
  -F "parse_mode=HTML")

OK=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('ok', False))")

if [ "$OK" = "True" ]; then
  SIZE=$(stat -c%s "$PDF")
  echo "OK: Delivered $(basename $PDF) (${SIZE} bytes) to Telegram chat ${HERMES_SESSION_CHAT_ID}"
else
  echo "ERROR: Telegram delivery failed"
  echo "$RESULT"
  exit 1
fi
