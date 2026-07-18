#!/bin/bash
# probe_federation_tools.sh — Live Federation Tool Probe
# DITEMPA BUKAN DIBERI
#
# Probes live MCP endpoints and reports tool counts.
# Compares against SOT files if available.

set -euo pipefail

echo "=== Federation Tool Probe ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

ORGS=("arifOS:8088" "A-FORGE:7071" "GEOX:8081" "WEALTH:18082" "WELL:18083")
TOTAL_LIVE=0
TOTAL_SOT=0

printf "%-12s %-8s %-8s %-8s %-10s\n" "Organ" "Port" "Live" "SOT" "Status"
printf "%-12s %-8s %-8s %-8s %-10s\n" "-----" "----" "----" "---" "------"

for entry in "${ORGS[@]}"; do
    IFS=':' read -r organ port <<< "$entry"
    sot_file="/root/$([ "$organ" = "A-FORGE" ] && echo "A-FORGE" || echo "$organ")/tools_sot.yaml"

    # Get live count (only WELL exposes tool_count in health endpoint)
    live_count=$(curl -s --connect-timeout 5 "http://127.0.0.1:$port/health" 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    tc = d.get('tool_count', d.get('tools_loaded', None))
    if tc is not None:
        print(tc)
    else:
        print(-2)  # field not present
except:
    print(-1)  # endpoint unreachable
" 2>/dev/null || echo -1)

    # Get SOT count (public + authenticated only)
    if [ -f "$sot_file" ]; then
        sot_count=$(python3 -c "
import yaml
data = yaml.safe_load(open('$sot_file'))
tools = data.get('tools', [])
public_auth = [t for t in tools if t.get('access') in ('public', 'authenticated')]
print(len(public_auth))
" 2>/dev/null)
    else
        sot_count="N/A"
    fi

    # Determine status
    if [ "$live_count" = "-1" ]; then
        status="DOWN"
    elif [ "$sot_count" = "N/A" ]; then
        status="NO SOT"
    elif [ "$live_count" = "$sot_count" ]; then
        status="✅ OK"
    else
        delta=$((live_count - sot_count))
        status="⚠️  Δ$delta"
    fi

    printf "%-12s %-8s %-8s %-8s %-10s\n" "$organ" "$port" "$live_count" "$sot_count" "$status"

    if [ "$live_count" != "-1" ]; then
        TOTAL_LIVE=$((TOTAL_LIVE + live_count))
    fi
    if [ "$sot_count" != "N/A" ]; then
        TOTAL_SOT=$((TOTAL_SOT + sot_count))
    fi
done

echo ""
printf "%-12s %-8s %-8s %-8s\n" "TOTAL" "" "$TOTAL_LIVE" "$TOTAL_SOT"
echo ""
echo "SOT files: /root/{organ}/tools_sot.yaml"
echo "Federation aggregator: /root/AAA/docs/federation_tools_sot.yaml"
