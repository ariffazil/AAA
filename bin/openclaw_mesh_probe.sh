#!/usr/bin/env bash
# /root/AAA/bin/openclaw_mesh_probe.sh
# OpenClaw Mesh Probe — cross-node health sensor.
# Cron: */5 * * * * /root/AAA/bin/openclaw_mesh_probe.sh >> /root/AAA/state/mesh.log 2>&1
# Silent on green. One line on red.
# set -euo pipefail  # disabled — remote probes can fail, that's data not error

REGISTRY="/root/AAA/state/nodes.json"
TIMEOUT=2
TS="$(date -u +%FT%TZ)"

# Fast TCP probe. timeout + nc -z. 2 seconds max per probe.
probe() { timeout "$TIMEOUT" nc -z "$1" "$2" 2>/dev/null && echo "online" || echo "down"; }

ORGANS=("arifos:8088" "aforge:7071" "arifflow:7073" "aaa:3001" "geox:8081" "wealth:18082" "well:18083")

echo "{"
echo '  "mesh_id": "arifos-federation-v1",'
echo "  \"updated\": \"$TS\","
echo '  "nodes": {'

# ── af-forge (local) ──
echo '    "af-forge": {'
echo '      "tailscale_ip": "100.64.0.2",'
echo '      "hostname": "af-forge",'
echo '      "online": true,'
echo '      "organs": {'
FIRST=true; ONLINE_COUNT=0
for od in "${ORGANS[@]}"; do
  name="${od%%:*}"; port="${od##*:}"
  s="$(probe 127.0.0.1 "$port")"
  [[ "$s" == "online" ]] && ((ONLINE_COUNT++))
  $FIRST || echo ","; FIRST=false
  echo -n "        \"$name\": {\"port\": $port, \"status\": \"$s\"}"
done
echo ""
echo "      },"
# FQ
FQ_RAW="$(curl -sf --max-time "$TIMEOUT" http://127.0.0.1:7073/health 2>/dev/null)"
FQ="null"
if [ -n "$FQ_RAW" ]; then
  FQ="$(echo "$FQ_RAW" | python3 -c "
import json,sys
try:
 d=json.load(sys.stdin);fq=d.get('fq',{})
 print(json.dumps({'quotient':fq.get('quotient'),'verdict':fq.get('verdict'),'execute_count':fq.get('execute_count'),'verify_count':fq.get('verify_count')}))
except: print('null')
" 2>/dev/null)"
fi
echo "      \"fq\": $FQ,"
echo "      \"organs_online\": $ONLINE_COUNT"
echo "    },"

# ── flow-edge (remote, SSH-based probe) ──
FLOW_IP="100.64.0.4"
FLOW_ONLINE=false
timeout "$TIMEOUT" nc -z "$FLOW_IP" 22 2>/dev/null && FLOW_ONLINE=true

echo '    "flow-edge": {'
echo "      \"tailscale_ip\": \"$FLOW_IP\","
echo "      \"hostname\": \"flow-edge\","
echo "      \"online\": $FLOW_ONLINE,"

if $FLOW_ONLINE; then
  # Single SSH call to probe all organs
  FLOW_JSON=$(ssh -o ConnectTimeout=5 -o BatchMode=yes root@"$FLOW_IP" "/usr/local/bin/federation-health.sh" 2>/dev/null)
  if [ -n "$FLOW_JSON" ]; then
    echo "$FLOW_JSON" | python3 -c "
import json,sys
d=json.load(sys.stdin)
orgs=d.get('organs',{})
ol=sum(1 for o in orgs.values() if o.get('status')=='online')
fq=d.get('fq') or {}
print(f'      \"organs\": {json.dumps(orgs)},')
print(f'      \"fq\": {json.dumps(fq)},')
print(f'      \"organs_online\": {ol}')
" 2>/dev/null
  else
    echo '      "organs": {},'
    echo '      "fq": null,'
    echo '      "organs_online": 0'
  fi
else
  echo '      "organs": {},'
  echo '      "fq": null,'
  echo '      "organs_online": 0'
fi
echo "    },"

# ── arifs-s24 (mobile) ──
S24_IP="100.64.0.1"
S24_ONLINE=false
timeout "$TIMEOUT" nc -z "$S24_IP" 22 2>/dev/null && S24_ONLINE=true

echo '    "arifs-s24": {'
echo "      \"tailscale_ip\": \"$S24_IP\","
echo "      \"hostname\": \"arifs-s24\","
echo "      \"online\": $S24_ONLINE,"
echo '      "organs": {},'
echo '      "fq": null,'
echo '      "organs_online": 0'
echo "    }"

echo "  }"
echo "}"

# Alert on red
$FLOW_ONLINE || echo "[$TS] NODE_OFFLINE: flow-edge ($FLOW_IP)" >&2
exit 0