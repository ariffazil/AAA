#!/bin/bash
# federation_topology_drift_check.sh
# Daily probe: 9 named components + class column.
# Run: /root/AAA/scripts/federation_topology_drift_check.sh >> /root/AAA/state/federation-topology.log
# Owner: arifOS. Schedule: 06:00 MYT daily (deferred to F13 cron approval per Event-Driven-First).

set -e
TS=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
echo "=== $TS federation-topology probe ==="

probe() {
  local name=$1 port=$2 class=$3
  local out
  out=$(curl -sS -m 3 "http://127.0.0.1:$port/health" 2>/dev/null || echo '{"status":"DOWN"}')
  local status=$(echo "$out" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('status', d.get('diagnosis','UNKNOWN')))" 2>/dev/null || echo "PARSE_ERR")
  local sha=$(cd "/root/$name" 2>/dev/null && git rev-parse --short HEAD 2>/dev/null || echo "n/a")
  local drift=$(cd "/root/$name" 2>/dev/null && git status --porcelain 2>/dev/null | wc -l || echo "n/a")
  printf "%-12s | %-22s | :%-6s | sha=%-9s drift=%-4s | %s\n" "$name" "$class" "$port" "$sha" "$drift" "$status"
}

# CONSTITUTIONAL_ORGAN
probe arifOS    8088  CONSTITUTIONAL_ORGAN
probe a-forge   7071  CONSTITUTIONAL_ORGAN
probe GEOX      8081  CONSTITUTIONAL_ORGAN
probe WEALTH    18082 CONSTITUTIONAL_ORGAN
probe WELL      18083 CONSTITUTIONAL_ORGAN
# arifFlow lives in service, not /root — probe only
probe_flow() {
  local out
  out=$(curl -sS -m 3 "http://127.0.0.1:7073/health" 2>/dev/null || echo '{"diagnosis":"DOWN"}')
  local status=$(echo "$out" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('diagnosis', d.get('status','UNKNOWN')))" 2>/dev/null || echo "PARSE_ERR")
  printf "%-12s | %-22s | :%-6s | sha=%-9s drift=%-4s | %s\n" "arifFlow" "CONSTITUTIONAL_ORGAN" "7073" "n/a" "n/a" "$status"
}
probe_flow
# AAA port (3001) + INTELLIGENCE_BOUNDARY
probe AAA       3001  CONSTITUTIONAL_ORGAN
probe HERMES    18087 INTELLIGENCE_BOUNDARY
probe CHRON     18102 INTELLIGENCE_BOUNDARY
# WITNESS_RECORD
probe FRAME-18085 18085 WITNESS_RECORD 2>/dev/null || true
# ADVISORY_PLANE
probe FED       7074  ADVISORY_PLANE

echo "=== $TS done ==="
