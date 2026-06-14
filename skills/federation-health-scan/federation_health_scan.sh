#!/usr/bin/env bash
# federation_health_scan.sh — single-command federation diagnostic
# Forged: 2026-06-14 — P3 mesh wiring complete
# DITEMPA BUKAN DIBERI

set -o pipefail

ORGANS=(
  "arifOS|8088|/health"
  "GEOX|8081|/health"
  "WEALTH|18082|/health"
  "WELL|18083|/health"
  "A-FORGE|7071|/health"
  "AAA|3001|/health"
)

check_organ() {
  local name=$1 port=$2 path=$3
  local start=$(date +%s%N 2>/dev/null || echo 0)
  local resp=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "http://127.0.0.1:${port}${path}" 2>/dev/null)
  local end=$(date +%s%N 2>/dev/null || echo 0)
  local latency=0
  if [ "$start" != "0" ] && [ "$end" != "0" ]; then
    latency=$(( (end - start) / 1000000 ))
  fi
  case "$resp" in
    200) echo "OK|${latency}" ;;
    000) echo "DOWN|${latency}" ;;
    *)   echo "WARN|${latency}|HTTP_${resp}" ;;
  esac
}

check_nats() {
  local conns=$(curl -s http://127.0.0.1:8222/connz 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('num_connections',0))" 2>/dev/null || echo "0")
  local gov_msgs=$(curl -s "http://127.0.0.1:8222/streams/arifos-governance" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin).get('state',{}); print(d.get('messages',0))" 2>/dev/null || echo "0")
  local org_msgs=$(curl -s "http://127.0.0.1:8222/streams/arifos-organs" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin).get('state',{}); print(d.get('messages',0))" 2>/dev/null || echo "0")
  echo "${conns}|${gov_msgs}|${org_msgs}"
}

check_drift() {
  local drift_files=""
  for f in server.py governance_pipeline.py; do
    if [ -f "/root/arifOS/arifosmcp/${f}" ] && [ -f "/opt/arifos/app/arifosmcp/${f}" ]; then
      if ! diff -q "/root/arifOS/arifosmcp/${f}" "/opt/arifos/app/arifosmcp/${f}" > /dev/null 2>&1; then
        drift_files="${drift_files} ${f}"
      fi
    fi
  done
  if [ -n "$drift_files" ]; then
    echo "DRIFTING|${drift_files}"
  else
    echo "OK|none"
  fi
}

check_vault() {
  local resp=$(curl -s --max-time 3 http://127.0.0.1:5001/health 2>/dev/null)
  if [ -n "$resp" ]; then
    echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"{d.get('chain_height','?')}|{d.get('last_seal_timestamp','?')}\")" 2>/dev/null || echo "?|parse_error"
  else
    echo "?|unreachable"
  fi
}

OUTPUT_MODE="${1:-text}"
ORGANS_JSON=""
WARN_COUNT=0
DOWN_COUNT=0

if [ "$OUTPUT_MODE" != "--json" ]; then
  echo "═══ FEDERATION HEALTH SCAN ═══"
  echo ""
  echo "─── ORGANS ───"
fi

for entry in "${ORGANS[@]}"; do
  IFS='|' read -r name port path <<< "$entry"
  result=$(check_organ "$name" "$port" "$path")
  IFS='|' read -r status latency extra <<< "$result"
  
  case "$status" in
    WARN) ((WARN_COUNT++)) ;;
    DOWN) ((DOWN_COUNT++)) ;;
  esac
  
  if [ "$OUTPUT_MODE" = "--json" ]; then
    ORGANS_JSON+="\"${name}\":{\"status\":\"${status}\",\"latency_ms\":${latency}},"
  else
    printf "  %-12s %-6s %4sms\n" "$name" "$status" "$latency"
  fi
done

NATS_RESULT=$(check_nats)
IFS='|' read -r nats_conns gov_msgs org_msgs <<< "$NATS_RESULT"

DRIFT_RESULT=$(check_drift)
IFS='|' read -r drift_status drift_details <<< "$DRIFT_RESULT"

VAULT_RESULT=$(check_vault)
IFS='|' read -r vault_height vault_last <<< "$VAULT_RESULT"

if [ $DOWN_COUNT -gt 0 ]; then
  SUMMARY="CRITICAL"
elif [ $WARN_COUNT -gt 0 ] || [ "$drift_status" = "DRIFTING" ]; then
  SUMMARY="WARN"
else
  SUMMARY="OK"
fi

if [ "$OUTPUT_MODE" = "--json" ]; then
  cat <<JSONEOF
{
  "organs": {${ORGANS_JSON%,}},
  "nats": {
    "connections": ${nats_conns},
    "streams": {
      "arifos-governance": {"messages": ${gov_msgs}},
      "arifos-organs": {"messages": ${org_msgs}}
    }
  },
  "drift": {
    "status": "${drift_status}",
    "details": "${drift_details}"
  },
  "vault": {
    "chain_height": "${vault_height}",
    "last_seal": "${vault_last}"
  },
  "summary": "${SUMMARY}",
  "warn_count": ${WARN_COUNT},
  "down_count": ${DOWN_COUNT},
  "recommendation": "$([ "$SUMMARY" = "CRITICAL" ] && echo "IMMEDIATE_888_HOLD — down organs detected" || [ "$SUMMARY" = "WARN" ] && echo "Investigate warnings before critical operations" || echo "All clear — proceed")"
}
JSONEOF
else
  echo ""
  echo "─── NATS ───"
  echo "  Connections: ${nats_conns}"
  echo "  arifos-governance: ${gov_msgs} msgs"
  echo "  arifos-organs: ${org_msgs} msgs"
  echo "─── DRIFT ───"
  echo "  Status: ${drift_status}"
  echo "─── VAULT ───"
  echo "  Chain height: ${vault_height}"
  echo "  Last seal: ${vault_last}"
  echo ""
  echo "VERDICT: ${SUMMARY} (W:${WARN_COUNT} D:${DOWN_COUNT})"
fi
