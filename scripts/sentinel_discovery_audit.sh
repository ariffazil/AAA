#!/bin/bash
# sentinel_discovery_audit.sh — nightly 02:30 sentinel
# Scans federation for new nodes/ports/cron jobs not in registry.
# Constitutional: F1 AMANAH (read-only), F2 TRUTH (emits evidence), F11 AUDIT.
# Author: kimi-code/FI-008, 2026-08-01, per HOLD#8 (888_HOLD_RELEASE).
# Forged: 2026-08-01 — DITEMPA BUKAN DIBERI.

set -uo pipefail
LOG=/root/.local/share/arifos/sentinel_discovery_audit.log
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "[$TS] sentinel_discovery_audit BEGIN" >> "$LOG"

# 1. Snapshot live state
LIVE_PORTS=$(ss -tlnH 2>/dev/null | awk '{print $4}' | awk -F: '{print $NF}' | sort -un | tr '\n' ',' | sed 's/,$//')
LIVE_CRON="/tmp/sentinel_cron_live_$$.tmp"
( crontab -l 2>/dev/null; for f in /etc/cron.d/*; do [ -f "$f" ] && cat "$f"; done ) 2>/dev/null | grep -vE '^#|^$' | sort -u > "$LIVE_CRON"

# 2. Compare against registry
REG_PORTS=$(jq -r '.ports[]' /root/AAA/federation/machine_constitution.json 2>/dev/null | sort -un | tr '\n' ',' | sed 's/,$//')
REG_CRON=$(find /root/AAA/federation/cron_registry -type f 2>/dev/null | sort)

# 3. Diff
DIFF_PORTS=$(comm -23 <(echo "$LIVE_PORTS" | tr ',' '\n' | sort -u) <(echo "$REG_PORTS" | tr ',' '\n' | sort -u) | tr '\n' ',' | sed 's/,$//')
DIFF_CRON=$(diff <(cat "$LIVE_CRON") <(cat $REG_CRON 2>/dev/null) 2>/dev/null | head -50)

# 4. Emit receipt
if [ -n "$DIFF_PORTS" ] || [ -n "$DIFF_CRON" ]; then
  REC=/root/.local/share/arifos/sentinel_discovery_audit.receipt.json
  cat > "$REC" <<EOF
{"timestamp":"$TS","status":"DRIFT","new_ports":"$DIFF_PORTS","cron_diff":"$(echo "$DIFF_CRON" | head -c 500 | sed 's/"/\\"/g')"}
EOF
  echo "[$TS] DRIFT DETECTED: ports=$DIFF_PORTS cron_diff_lines=$(echo "$DIFF_CRON" | wc -l)" >> "$LOG"
  # Surface to AAA cockpit via webhook (URL pulled from env)
  if [ -n "${AAA_WEBHOOK_URL:-}" ]; then
    curl -sf -X POST -H "Content-Type: application/json" -d @"$REC" "$AAA_WEBHOOK_URL" >> "$LOG" 2>&1 || true
  fi
fi

rm -f "$LIVE_CRON"
echo "[$TS] sentinel_discovery_audit END" >> "$LOG"
