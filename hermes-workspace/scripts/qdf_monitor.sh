#!/bin/bash
# QDF Autonomous Monitor — runs every 30min via heartbeat infrastructure
LOGFILE="/root/waw/state/qdf_monitor.jsonl"
STATEFILE="/root/waw/state/qdf_monitor_current.json"

count_a2a() {
    # Check vault log for federation activation events
    spawned=$(grep -c "A2A_FEDERATION_LIVE\|A2A_FEDERATION_PROBE" /root/waw/state/vault999_action_log.jsonl 2>/dev/null || echo "0")
    # Count live subagent sessions in last 30 min
    active=$(cd /root/waw && openclaw sessions list --active 30 2>/dev/null | grep -cE "subagent|a-architect|a-engineer|a-auditor" || echo "0")
    total=$(python3 -c "print(max(int('$spawned'), int('$active')))")
    echo "$total"
}

check_vault() { [ -f "/root/waw/state/vault999_action_log.jsonl" ] && [ -s "/root/waw/state/vault999_action_log.jsonl" ] && echo "0.5" || echo "0.0"; }
check_audit() { [ -f "/root/waw/state/qdf_monitor.jsonl" ] && [ -s "/root/waw/state/qdf_monitor.jsonl" ] && echo "0.4" || echo "0.1"; }
check_memory() { curl -s --connect-timeout 3 http://localhost:6333/ > /dev/null 2>&1 && echo "0.7" || echo "0.3"; }
check_deploy() { grep -q "DEPLOY_EXECUTED" /root/waw/state/vault999_action_log.jsonl 2>/dev/null && echo "0.7" || echo "0.3"; }
check_idle() { grep -q "IDLE_BUILDER_TRIGGERED" /root/waw/state/vault999_action_log.jsonl 2>/dev/null && echo "0.5" || echo "0.3"; }

a2a_raw=$(count_a2a | tr -d ' \n')
vault_raw=$(check_vault)
audit_raw=$(check_audit)
memory_raw=$(check_memory)
deploy_raw=$(check_deploy)
idle_raw=$(check_idle)

# Map a2a count to score
a2a_int=$(echo "$a2a_raw" | tr -cd '0-9' 2>/dev/null || echo "0")
case "$a2a_int" in
    0) a2a_score=0.0 ;;
    1) a2a_score=0.33 ;;
    2) a2a_score=0.66 ;;
    *) a2a_score=1.0 ;;
esac

vault_score=$vault_raw
audit_score=$audit_raw
memory_score=$memory_raw
deploy_score=$deploy_raw
idle_score=$idle_raw

qdf=$(python3 -c "
qdf = 0.20*$a2a_score + 0.25*$vault_score + 0.15*$audit_score + 0.15*$memory_score + 0.15*$deploy_score + 0.10*$idle_score
print(round(qdf, 3))
")

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
status=$(python3 -c "print('NOMINAL' if float('$qdf') >= 0.50 else 'DEGRADED')")

cat > "$STATEFILE" << EOF
{
  "lastRun": "$timestamp",
  "qdf": $qdf,
  "dimensions": {
    "a2a_federation": $a2a_score,
    "vault999": $vault_score,
    "self_audit": $audit_score,
    "memory_qdrant": $memory_score,
    "arifos_deploy": $deploy_score,
    "idle_builder": $idle_score
  },
  "raw": { "a2a_sessions": "$a2a_raw" },
  "status": "$status"
}
EOF

echo "{\"timestamp\":\"$timestamp\",\"qdf\":$qdf,\"a2a\":$a2a_score,\"vault\":$vault_score,\"audit\":$audit_score,\"memory\":$memory_score,\"deploy\":$deploy_score,\"idle\":$idle_score}" >> "$LOGFILE"
echo "QDF: $qdf | Status: $status"
