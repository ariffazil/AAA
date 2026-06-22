---
superseded_by: /root/arifOS/skills/health-probe/SKILL.md
superseded_category: constitutional-duplicate
superseded_date: 2026-06-22
superseded_authority: Hermes-ASI-for-Arif-F13-SOVEREIGN
superseded_status: DRAFT-pending-Cycle-B-888-ratification
---

# Federation Health Scan — OpenClaw Operational Skill

**Skill ID:** `federation-health-scan`  
**Agent:** OpenClaw (AGI — Operational Gateway)  
**Priority:** P0  
**Forged:** 2026-06-14 — arifOS P3 mesh wiring complete  
**DITEMPA BUKAN DIBERI**

## Purpose

Single-command federation health diagnostic. Returns structured JSON verdict on all 6 organs, NATS mesh, drift status, and vault staleness. Replaces ad-hoc `curl` + `systemctl` + `nats stream info` manual checking.

## Trigger

- User says: "health scan", "federation status", "check all organs", "is everything running?"
- Agent needs pre-flight check before critical operation
- Drift detected — need to assess blast radius
- Daily briefing / cron job

## Implementation

### Primary Method: Live HTTP Endpoints + NATS CLI

```bash
#!/usr/bin/env bash
# federation_health_scan.sh — single-command federation diagnostic
# Forged: 2026-06-14
# Usage: bash federation_health_scan.sh [--json]

set -o pipefail

ORGANS=(
  "arifOS|8088|/health"
  "GEOX|8081|/health"
  "WEALTH|18082|/health"
  "WELL|18083|/health"
  "A-FORGE|7071|/health"
  "AAA|3001|/health"
)

# ── Organ health probes ──────────────────────────────────────────────
check_organ() {
  local name=$1 port=$2 path=$3
  local start=$(date +%s%N)
  local resp=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "http://127.0.0.1:${port}${path}" 2>/dev/null)
  local end=$(date +%s%N)
  local latency=$(( (end - start) / 1000000 ))
  
  case "$resp" in
    200) echo "OK|${latency}" ;;
    000) echo "DOWN|${latency}" ;;
    *)   echo "WARN|${latency}|HTTP_${resp}" ;;
  esac
}

# ── NATS probe ───────────────────────────────────────────────────────
check_nats() {
  local conns=$(curl -s http://127.0.0.1:8222/connz 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('num_connections',0))" 2>/dev/null || echo "0")
  local gov_msgs=$(curl -s http://127.0.0.1:8222/streams/arifos-governance 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin).get('state',{}); print(d.get('messages',0))" 2>/dev/null || echo "0")
  local org_msgs=$(curl -s http://127.0.0.1:8222/streams/arifos-organs 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin).get('state',{}); print(d.get('messages',0))" 2>/dev/null || echo "0")
  echo "${conns}|${gov_msgs}|${org_msgs}"
}

# ── Drift check ──────────────────────────────────────────────────────
check_drift() {
  # Compare key files between /root/arifOS and /opt/arifos/app
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

# ── Vault probe ──────────────────────────────────────────────────────
check_vault() {
  local resp=$(curl -s --max-time 3 http://127.0.0.1:5001/health 2>/dev/null)
  if echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('chain_height','unknown'))" 2>/dev/null; then
    echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"{d.get('chain_height','?')}|{d.get('last_seal_timestamp','?')}\")" 2>/dev/null
  else
    echo "?|unreachable"
  fi
}

# ── Main ─────────────────────────────────────────────────────────────
OUTPUT_MODE="${1:-text}"

ORGANS_JSON=""
WARN_COUNT=0
DOWN_COUNT=0

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

# ── Summary ──────────────────────────────────────────────────────────
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
  echo "  Files: ${drift_details}"
  echo "─── VAULT ───"
  echo "  Chain height: ${vault_height}"
  echo "  Last seal: ${vault_last}"
  echo ""
  echo "VERDICT: ${SUMMARY}"
  echo "  Warnings: ${WARN_COUNT}, Down: ${DOWN_COUNT}"
fi
```

### Deployment

```bash
cp federation_health_scan.sh /root/AAA/skills/federation-health-scan/
chmod +x /root/AAA/skills/federation-health-scan/federation_health_scan.sh
```

### Integration

OpenClaw invokes via bash tool:
```bash
bash /root/AAA/skills/federation-health-scan/federation_health_scan.sh --json
```

### Expected Output (Sample)

```json
{
  "organs": {
    "arifOS": {"status": "OK", "latency_ms": 8},
    "GEOX": {"status": "OK", "latency_ms": 12},
    "WEALTH": {"status": "OK", "latency_ms": 15},
    "WELL": {"status": "OK", "latency_ms": 10},
    "A-FORGE": {"status": "OK", "latency_ms": 7},
    "AAA": {"status": "OK", "latency_ms": 5}
  },
  "nats": {
    "connections": 6,
    "streams": {
      "arifos-governance": {"messages": 51},
      "arifos-organs": {"messages": 8957}
    }
  },
  "drift": {
    "status": "OK",
    "details": "none"
  },
  "vault": {
    "chain_height": "62",
    "last_seal": "2026-06-14T06:17:00Z"
  },
  "summary": "OK",
  "warn_count": 0,
  "down_count": 0,
  "recommendation": "All clear — proceed"
}
```

### Self-Test

```bash
# Run health scan and verify required keys exist
RESULT=$(bash /root/AAA/skills/federation-health-scan/federation_health_scan.sh --json)
echo "$RESULT" | python3 -c "
import sys,json
d = json.load(sys.stdin)
assert 'organs' in d, 'Missing organs'
assert 'nats' in d, 'Missing nats'
assert 'drift' in d, 'Missing drift'
assert 'vault' in d, 'Missing vault'
assert 'summary' in d, 'Missing summary'
assert len(d['organs']) >= 6, 'Not enough organs'
print('SELFTEST PASSED')
"
```

### Constraints

- Read-only — no mutations, no restarts
- Uses only existing curl endpoints + nats CLI
- No new services or daemons
- Runs in <5 seconds
- Fail-silent on individual organs (one DOWN doesn't crash the scan)
