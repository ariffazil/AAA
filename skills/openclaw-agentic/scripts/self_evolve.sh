#!/bin/bash
# openclaw-agentic: self_evolve.sh  (v2 — recursive)
# =====================================================
# Daily 04:00 MYT self-evolve digest. Tier-0: pure shell, no LLM.
# Probes live state, appends to daily note, posts to Telegram ONLY on actionable.
#
# Recursive improvements over v1 (2026-06-06):
#  - Uses probe heartbeat at /run/openclaw_probe.heartbeat to detect
#    probe drift (last probe > 10 min ago = warning).
#  - Uses watchdog-heartbeat.sh marker at /tmp/watchdog_last_beat to detect
#    gateway watchdog drift.
#  - Compact 1-line digest + Telegram post only if anything actionable.
#  - Adds: uptime, load, last 24h error grep on gateway journal.
#  - Reversible: shell-only, no other state touched.
set -euo pipefail

NOTE="/root/.openclaw/memory/$(TZ=Asia/Kuala_Lumpur date +%Y-%m-%d).md"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
MYT_STAMP="$(TZ=Asia/Kuala_Lumpur date '+%Y-%m-%d %H:%M:%S MYT')"
PROBE_VERSION="v2-2026-06-08"

# --- Live state probes (all read-only) ---
OPENCLAW_VER=$(openclaw --version 2>/dev/null | head -1 || echo "?")
GATEWAY_HEALTH=$(curl -s -m 3 http://127.0.0.1:18789/health 2>/dev/null || echo "DOWN")
GATEWAY_OK=$(echo "$GATEWAY_HEALTH" | python3 -c "import json,sys; print('1' if json.load(sys.stdin).get('ok') else '0')" 2>/dev/null || echo "0")

TELEGRAM_PENDING=$(curl -s -m 3 "https://api.telegram.org/bot$(python3 -c "import json; print(json.load(open('/root/.openclaw/openclaw.json'))['channels']['telegram']['botToken'])")/getWebhookInfo" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('result',{}).get('pending_update_count','?'))" 2>/dev/null || echo "ERR")

SKILL_COUNT=$(openclaw skills list 2>/dev/null | grep -cE "ready|enabled" 2>/dev/null || echo "0")
PLUGIN_COUNT=$(openclaw plugins list 2>/dev/null | grep -cE "enabled" 2>/dev/null || echo "0")
UPDATE_NOTE=$(openclaw status 2>&1 | grep -i "update available" || true)
DISK_PCT=$(df -h /root 2>/dev/null | tail -1 | awk '{print $5}' | tr -d '%')
MEM_SQLITE_MB=$(du -sm /root/.openclaw/memory/main.sqlite 2>/dev/null | awk '{print $1}')
OPENCLAW_LOGS_MB=$(du -sm /root/.openclaw/logs/ 2>/dev/null | awk '{print $1}')
UPTIME_S=$(awk '{print int($1)}' /proc/uptime 2>/dev/null || echo "0")
LOAD_1=$(awk '{print $1}' /proc/loadavg 2>/dev/null || echo "?")
LOAD_5=$(awk '{print $2}' /proc/loadavg 2>/dev/null || echo "?")
LOAD_15=$(awk '{print $3}' /proc/loadavg 2>/dev/null || echo "?")

# --- Watchdog drift detection ---
WATCHDOG_BEAT="/tmp/watchdog_last_beat"
PROBE_BEAT="/run/openclaw_probe.heartbeat"
NOW=$(date +%s)
PROBE_AGE_S=$([ -f "$PROBE_BEAT" ] && echo $((NOW - $(cat "$PROBE_BEAT"))) || echo "missing")
WATCHDOG_AGE_S=$([ -f "$WATCHDOG_BEAT" ] && echo $((NOW - $(cat "$WATCHDOG_BEAT"))) || echo "missing")

# --- Last 24h error scan on gateway journal (count UNIQUE error lines, not all matches) ---
GW_ERRORS_24H=$(journalctl -u openclaw-gateway --since "24 hours ago" --no-pager 2>/dev/null | grep -iE "error|fail" | sort -u | wc -l || echo "0")
GW_OVERLOADED_24H=$(journalctl -u openclaw-gateway --since "24 hours ago" --no-pager 2>/dev/null | grep -ciE "overloaded_error|server is busy" || echo "0")

# --- Append digest to daily note ---
{
  echo ""
  echo "## openclaw self-evolve digest — $STAMP ($MYT_STAMP) [v2]"
  echo "  - version:         $OPENCLAW_VER"
  echo "  - gateway ok:      $GATEWAY_OK (${GATEWAY_HEALTH:0:50})"
  echo "  - tg pending:      $TELEGRAM_PENDING"
  echo "  - skills ready:    $SKILL_COUNT"
  echo "  - plugins loaded:  $PLUGIN_COUNT"
  echo "  - disk %:          ${DISK_PCT}%"
  echo "  - mem SQLite:      ${MEM_SQLITE_MB}MB"
  echo "  - logs size:       ${OPENCLAW_LOGS_MB}MB"
  echo "  - uptime:          ${UPTIME_S}s  load: ${LOAD_1} / ${LOAD_5} / ${LOAD_15}"
  echo "  - probe age:       ${PROBE_AGE_S}s (heartbeat $PROBE_BEAT)"
  echo "  - watchdog age:    ${WATCHDOG_AGE_S}s (heartbeat $WATCHDOG_BEAT)"
  echo "  - gw errors 24h:   $GW_ERRORS_24H unique (overloaded: $GW_OVERLOADED_24H)"
  echo "  - update:          ${UPDATE_NOTE:-(none)}"
  echo ""
} >> "$NOTE" 2>/dev/null

# --- Decide if Telegram post is warranted ---
ACTIONABLE=""
[[ "$GATEWAY_OK" != "1" ]] && ACTIONABLE+="Gateway degraded. "
if [[ "$TELEGRAM_PENDING" =~ ^[0-9]+$ ]] && [[ "$TELEGRAM_PENDING" -gt 20 ]]; then
  ACTIONABLE+="Telegram pending=$TELEGRAM_PENDING. "
fi
if [[ "${DISK_PCT:-0}" =~ ^[0-9]+$ ]] && [[ "$DISK_PCT" -gt 85 ]]; then
  ACTIONABLE+="Disk ${DISK_PCT}%. "
fi
if [[ "${MEM_SQLITE_MB:-0}" =~ ^[0-9]+$ ]] && [[ "$MEM_SQLITE_MB" -gt 200 ]]; then
  ACTIONABLE+="Memory SQLite ${MEM_SQLITE_MB}MB. "
fi
if [[ "${OPENCLAW_LOGS_MB:-0}" =~ ^[0-9]+$ ]] && [[ "$OPENCLAW_LOGS_MB" -gt 500 ]]; then
  ACTIONABLE+="Logs ${OPENCLAW_LOGS_MB}MB. "
fi
if [[ "$PROBE_AGE_S" =~ ^[0-9]+$ ]] && [[ "$PROBE_AGE_S" -gt 600 ]]; then
  ACTIONABLE+="Probe silent ${PROBE_AGE_S}s. "
fi
if [[ "$WATCHDOG_AGE_S" =~ ^[0-9]+$ ]] && [[ "$WATCHDOG_AGE_S" -gt 900 ]]; then
  ACTIONABLE+="Watchdog silent ${WATCHDOG_AGE_S}s. "
fi
if [[ "${GW_ERRORS_24H:-0}" =~ ^[0-9]+$ ]] && [[ "$GW_ERRORS_24H" -gt 1000 ]]; then
  ACTIONABLE+="Gateway errors 24h=$GW_ERRORS_24H unique. "
fi
if [[ "${GW_OVERLOADED_24H:-0}" =~ ^[0-9]+$ ]] && [[ "$GW_OVERLOADED_24H" -gt 50 ]]; then
  ACTIONABLE+="LLM overloaded ${GW_OVERLOADED_24H}x/24h. "
fi
if [[ -n "$UPDATE_NOTE" ]]; then
  ACTIONABLE+="OpenClaw update available. "
fi

if [[ -n "$ACTIONABLE" ]]; then
  MSG="🫀 self-evolve: $ACTIONABLE (full digest in $NOTE)"
  # Direct Telegram API (no LLM session). Token from openclaw.json.
  TOKEN=$(python3 -c "import json; print(json.load(open('/root/.openclaw/openclaw.json'))['channels']['telegram']['botToken'])" 2>/dev/null || echo "")
  if [[ -n "$TOKEN" ]]; then
    curl -s -m 5 -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
      -d chat_id="267378578" \
      -d text="$MSG" \
      -d parse_mode="HTML" >/dev/null 2>&1 || \
      echo "[self-evolve] Telegram delivery failed: $MSG" >&2
  else
    echo "[self-evolve] No token, skipped post: $MSG" >&2
  fi
fi

echo "[self-evolve] $STAMP — v=$PROBE_VERSION actionable='$ACTIONABLE' gateway_ok=$GATEWAY_OK"
exit 0
