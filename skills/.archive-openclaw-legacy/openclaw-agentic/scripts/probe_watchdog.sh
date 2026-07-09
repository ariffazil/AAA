#!/bin/bash
# probe_watchdog.sh — verify autonomous_probe.py is actually running.
# Runs every 30 min. Posts Telegram alert if probe heartbeat is stale.
# Tier-0: pure shell, no LLM.
#
# Reversible: rm /etc/cron.d/openclaw-agentic and this script becomes inert.
set -euo pipefail

HEARTBEAT="/run/openclaw_probe.heartbeat"
STALE_THRESHOLD_S=600   # 10 min
NOW=$(date +%s)

post_tg() {
  local msg="$1"
  local token
  token=$(python3 -c "import json; print(json.load(open('/root/.openclaw/openclaw.json'))['channels']['telegram']['botToken'])" 2>/dev/null || echo "")
  if [[ -n "$token" ]]; then
    curl -s -m 5 -X POST "https://api.telegram.org/bot${token}/sendMessage" \
      -d chat_id="267378578" \
      -d text="$msg" \
      -d parse_mode="HTML" >/dev/null 2>&1 || \
      echo "[probe-watchdog] Telegram delivery failed: $msg" >&2
  fi
}

# Heartbeat file present?
if [[ ! -f "$HEARTBEAT" ]]; then
  post_tg "🫀 probe-watchdog: no heartbeat file at $HEARTBEAT — probe never ran since reboot"
  exit 1
fi

LAST=$(cat "$HEARTBEAT" 2>/dev/null || echo 0)
AGE=$((NOW - LAST))

if [[ $AGE -gt $STALE_THRESHOLD_S ]]; then
  post_tg "🫀 probe-watchdog: probe stale ${AGE}s (threshold ${STALE_THRESHOLD_S}s) at $(TZ=Asia/Kuala_Lumpur date '+%H:%M:%S MYT')"
  exit 1
fi

# Healthy — append to log only
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] probe heartbeat fresh age=${AGE}s"
exit 0
