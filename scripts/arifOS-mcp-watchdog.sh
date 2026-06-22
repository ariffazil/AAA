#!/bin/bash
# arifOS_MCP watchdog — host crontab
# Restart budget: max 2 restarts per 2-hour rolling window
# Telegram alert only on recovery or 888_HOLD

LOGFILE="/var/log/arifOS-watchdog.log"
STATEFILE="/tmp/arifOS-watchdog-state.json"
TELEGRAM_TOKEN="${TELEGRAM_BOT_TOKEN:-${TELEGRAM_TOKEN:-}}"
TELEGRAM_CHAT="267378578"
CONTAINER="arifosmcp"
HEALTH_URL="http://localhost:8080/health"
RESTART_BUDGET=2
BUDGET_WINDOW_HOURS=2

log() { echo "$(date '+%Y-%m-%dT%H:%M:%S%Z') [arifOS_MCP-WATCHDOG] $*" >> "$LOGFILE"; }

# Throttle: rolling restart budget
check_budget() {
    local window_sec=$((BUDGET_WINDOW_HOURS * 3600))
    local now_ms=$(date +%s%3N)
    local last_restart_ms
    last_restart_ms=$(python3 -c "import json; d=json.load(open('$STATEFILE')) if os.path.exists('$STATEFILE') else {'restarts':[],'bucket':0}; print(d.get('last_restart_ms',0))" 2>/dev/null || echo "0")
    local count
    count=$(python3 -c "
import json, os, time
d = json.load(open('$STATEFILE')) if os.path.exists('$STATEFILE') else {'restarts':[],'bucket':0}
cutoff = time.time()*1000 - $window_sec * 1000
d['restarts'] = [r for r in d.get('restarts',[]) if r > cutoff]
print(len(d['restarts']))
" 2>/dev/null)
    [ "$count" -lt "$RESTART_BUDGET" ] && return 0 || return 1
}

record_restart() {
    python3 -c "
import json, os, time
d = json.load(open('$STATEFILE')) if os.path.exists('$STATEFILE') else {'restarts':[],'bucket':0}
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

# ── HEALTH CHECK ──────────────────────────────────────────────────────────────
log "START health check"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 8 "$HEALTH_URL" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    log "HEALTHY — exit silent"
    exit 0
fi

log "UNHEALTHY http_code=$HTTP_CODE — attempting repair"

# ── REPAIR ATTEMPT ──────────────────────────────────────────────────────────
# Budget check
if ! check_budget; then
    log "BUDGET_EXCEEDED — exit 888_HOLD"
    send_telegram "⚠️ arifOS_MCP watchdog: restart budget exceeded (2/$BUDGET_WINDOW_HOURS hours). Manual inspection required at http://localhost:8080/health"
    exit 1
fi

# Attempt: restart container once
log "ATTEMPT restart container $CONTAINER"
docker restart "$CONTAINER" >> "$LOGFILE" 2>&1
sleep 12  # wait for startup

# Re-check
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 8 "$HEALTH_URL" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    record_restart
    log "RECOVERED after restart"
    send_telegram "✅ arifOS_MCP recovered after automatic restart. $(date '+%Y-%m-%d %H:%M UTC')"
    exit 0
fi

# Still failing
log "REPAIR_FAILED — 888_HOLD"
send_telegram "🚨 arifOS_MCP is unhealthy after restart attempt. Manual inspection required. Health URL: http://localhost:8080/health | HTTP code: $HTTP_CODE"
exit 1