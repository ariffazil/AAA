#!/bin/bash
# arifOS Gateway watchdog — runs inside OpenClaw cron agent
# Action-based. Silent on healthy. Telegram only on recovery or 888_HOLD.
# Uses curl direct to gateway /health (shell HTTP, no model call).
# Correct restart: openclaw restart (not systemctl)

TELEGRAM_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT="267378578"
STATEFILE="/tmp/openclaw-watchdog-state.json"
BUDGET_WINDOW_HOURS=2
RESTART_BUDGET=2

log() { echo "$(date '+%Y-%m-%dT%H:%M:%S%Z') [OC-WATCHDOG] $*" >> /var/log/arifOS-watchdog.log; }

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
        -d "$payload" >> /var/log/arifOS-watchdog.log 2>&1
}

# HEALTH CHECK — curl direct, bypass model entirely
HEALTH_JSON=$(curl -sf --max-time 8 http://127.0.0.1:18789/health 2>/dev/null)
HEALTH_OK=$(echo "$HEALTH_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print('1' if d.get('ok') else '0')" 2>/dev/null)

if [ "$HEALTH_OK" = "1" ]; then
    log "GATEWAY_HEALTHY"
    exit 0
fi

log "GATEWAY_UNHEALTHY — attempting repair"

# Try openclaw doctor first
openclaw doctor 2>/dev/null >> /var/log/arifOS-watchdog.log 2>&1
sleep 5

# Re-check after doctor
HEALTH_JSON=$(curl -sf --max-time 8 http://127.0.0.1:18789/health 2>/dev/null)
HEALTH_OK=$(echo "$HEALTH_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print('1' if d.get('ok') else '0')" 2>/dev/null)
if [ "$HEALTH_OK" = "1" ]; then
    log "RECOVERED after doctor"
    send_telegram "✅ arifOS Gateway recovered after openclaw doctor. $(date '+%Y-%m-%d %H:%M UTC')"
    exit 0
fi

# Budget check before restart
if ! check_budget; then
    log "RESTART_BUDGET_EXCEEDED — 888_HOLD"
    send_telegram "⚠️ arifOS Gateway restart budget exceeded. openclaw doctor did not recover. Manual inspection required."
    exit 1
fi

# Correct restart path for OpenClaw gateway
log "ATTEMPT openclaw restart"
openclaw restart 2>/dev/null >> /var/log/arifOS-watchdog.log 2>&1
sleep 15

# Final re-check
HEALTH_JSON=$(curl -sf --max-time 8 http://127.0.0.1:18789/health 2>/dev/null)
HEALTH_OK=$(echo "$HEALTH_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print('1' if d.get('ok') else '0')" 2>/dev/null)
if [ "$HEALTH_OK" = "1" ]; then
    record_restart
    log "RECOVERED after openclaw restart"
    send_telegram "✅ arifOS Gateway recovered after openclaw restart. $(date '+%Y-%m-%d %H:%M UTC')"
    exit 0
fi

log "REPAIR_FAILED — 888_HOLD"
send_telegram "🚨 arifOS Gateway unhealthy after restart. openclaw restart did not recover. Manual inspection required."
exit 1