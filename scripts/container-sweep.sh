#!/bin/bash
# Container health sweep — host crontab /30min
# CORE containers only. Silent on success. Telegram on action taken or still failing.

LOGFILE="/var/log/arifOS-watchdog.log"
STATEFILE="/tmp/container-sweep-state.json"
TELEGRAM_TOKEN="${TELEGRAM_BOT_TOKEN:-${TELEGRAM_TOKEN:-}}"
TELEGRAM_CHAT="267378578"

# Core stack only (present on this machine)
# arifosmcp, geox_eic, wealth-organ, well, redis, postgres, caddy, openclaw
# Note: openclaw is native process (not container) — skip for container check
CORE_CONTAINERS="arifosmcp geox_eic wealth-organ well redis postgres"

log() { echo "$(date '+%Y-%m-%dT%H:%M:%S%Z') [CONTAINER-SWEEP] $*" >> "$LOGFILE"; }

# Budget: max 2 restarts per container per 2-hour window
check_budget() {
    local container="$1"
    python3 -c "
import json, os, time
d = json.load(open('$STATEFILE')) if os.path.exists('$STATEFILE') else {}
cutoff = time.time()*1000 - 2*3600*1000
bucket = [r for r in d.get('$container',[]) if r > cutoff]
print('OK' if len(bucket) < 2 else 'BLOCKED')
" 2>/dev/null | grep -q "OK" && return 0 || return 1
}

record_restart() {
    local container="$1"
    python3 -c "
import json, os, time
d = json.load(open('$STATEFILE')) if os.path.exists('$STATEFILE') else {}
d.setdefault('$container',[]).append(time.time()*1000)
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

ACTION_TAKEN=0

for container in $CORE_CONTAINERS; do
    STATUS=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null)
    if [ "$STATUS" = "exited" ] || [ "$STATUS" = "restarting" ]; then
        log "DETECTED $container status=$STATUS — attempting restart"
        if ! check_budget "$container"; then
            log "BUDGET_EXCEEDED for $container — skipping"
            send_telegram "⚠️ $container restart budget exceeded. Manual inspection required."
            ACTION_TAKEN=1
            continue
        fi
        docker start "$container" >> "$LOGFILE" 2>&1
        sleep 8
        NEW_STATUS=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null)
        if [ "$NEW_STATUS" = "running" ]; then
            record_restart "$container"
            log "$container RESTARTED successfully"
            send_telegram "✅ $container restarted automatically. $(date '+%Y-%m-%d %H:%M UTC')"
            ACTION_TAKEN=1
        else
            log "$container still $NEW_STATUS after restart — alert"
            send_telegram "🚨 $container still $NEW_STATUS after restart. Manual inspection required."
            ACTION_TAKEN=1
        fi
    fi
done

if [ "$ACTION_TAKEN" -eq 0 ]; then
    log "ALL_CORE_CONTAINERS_HEALTHY — exit silent"
fi

exit 0