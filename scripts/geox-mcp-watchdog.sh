#!/bin/bash
# GEOX MCP watchdog — host crontab
# Restart budget: max 2 restarts per 2-hour rolling window
# Telegram alert only on recovery or 888_HOLD

LOGFILE="/var/log/arifOS-watchdog.log"
STATEFILE="/tmp/geox-watchdog-state.json"
TELEGRAM_TOKEN="${TELEGRAM_BOT_TOKEN:-${TELEGRAM_TOKEN:-}}"
TELEGRAM_CHAT="267378578"
CONTAINER="geox_eic"
HEALTH_URL="http://localhost:8081/health"
RESTART_BUDGET=2
BUDGET_WINDOW_HOURS=2

log() { echo "$(date '+%Y-%m-%dT%H:%M:%S%Z') [GEOX_MCP-WATCHDOG] $*" >> "$LOGFILE"; }

check_budget() {
    python3 -c "
import json, os, time
d = json.load(open('$STATEFILE')) if os.path.exists('$STATEFILE') else {'restarts':[]}
cutoff = time.time()*1000 - $BUDGET_WINDOW_HOURS * 3600 * 1000
d['restarts'] = [r for r in d.get('restarts',[]) if r > cutoff]
print('OK' if len(d['restarts']) < $RESTART_BUDGET else 'BLOCKED')
" 2>/dev/null | grep -q "OK" && return 0 || return 1
}

record_restart() {
    python3 -c "
import json, os, time
d = json.load(open('$STATEFILE')) if os.path.exists('$STATEFILE') else {'restarts':[]}
d['restarts'].append(time.time()*1000)
with open('$STATEFILE','w') as f: json.dump(d,f)
" 2>/dev/null
}

send_telegram() {
    local msg="$1"
    [ -z "$TELEGRAM_TOKEN" ] && { log "TELEGRAM_ALERT_DROPPED: no token — $msg"; return; }
    local payload=$(python3 -c "import json; print(json.dumps({'chat_id':$TELEGRAM_CHAT,'text':$msg}))")
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
        -H "Content-Type: application/json" \
        -d "$payload" >> "$LOGFILE" 2>&1
}

log "START health check"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 8 "$HEALTH_URL" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    log "HEALTHY — exit silent"
    exit 0
fi

log "UNHEALTHY http_code=$HTTP_CODE"

if ! check_budget; then
    log "BUDGET_EXCEEDED — exit 888_HOLD"
    send_telegram "⚠️ GEOX_MCP watchdog: restart budget exceeded (2/$BUDGET_WINDOW_HOURS hours). Manual inspection required."
    exit 1
fi

log "ATTEMPT restart container $CONTAINER"
docker restart "$CONTAINER" >> "$LOGFILE" 2>&1
sleep 15

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 8 "$HEALTH_URL" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    record_restart
    log "RECOVERED after restart"
    send_telegram "✅ GEOX_MCP recovered after automatic restart. $(date '+%Y-%m-%d %H:%M UTC')"
    exit 0
fi

log "REPAIR_FAILED — 888_HOLD"
send_telegram "🚨 GEOX_MCP is unhealthy after restart attempt. Manual inspection required. Health: http://localhost:8081/health | HTTP: $HTTP_CODE"
exit 1