#!/usr/bin/env bash
# void_rotation_send.sh <AGENT_NAME> <BOT_ENV_VAR>  — questions on stdin (markdown), posts to AAA group
# Single point of config: chat id, ledger, receipt. All three rotation crons use this.
set -euo pipefail
source /root/.secrets/kunci-mas.env
AGENT="${1:?agent name}"; BOTVAR="${2:?bot env var}"
CHAT_ID="-1003753855708"   # AAA group @arifOS (verified 2026-08-15)
LEDGER="/root/AAA/arifOS/RESOURCES/10_RECEIPTS/AIA/VOID_ROTATION/asked.jsonl"
TOKEN="${!BOTVAR:?token env missing}"
BODY="$(cat)"
PAYLOAD=$(python3 -c "
import json,sys
print(json.dumps({'chat_id':'$CHAT_ID','text':sys.stdin.read(),'parse_mode':'Markdown'}))" <<<"$BODY")
curl -s -m 10 -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" -H 'Content-Type: application/json' -d "$PAYLOAD" | head -c 200
python3 - "$AGENT" "$BOTVAR" <<PY
import json, time, sys
rec={"ts":time.strftime("%Y-%m-%dT%H:%M:%S%z"),"agent":sys.argv[1],"bot_env":sys.argv[2],"delivered":True}
open("$LEDGER","a").write(json.dumps(rec,ensure_ascii=False)+"\n")
PY
