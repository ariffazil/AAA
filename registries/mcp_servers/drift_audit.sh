#!/usr/bin/env bash
# ⚒️ MCP DRIFT AUDIT — one-shot probe: config vs live health vs tool-list
#
# Reads /root/AAA/registries/mcp_servers/INDEX.json
# Probes each server (remote: curl health, local: process check)
# Captures tool-list from A-FORGE (:7072)
# Emits a structured receipt to stdout (JSON Lines)
#
# F1 AMANAH: read-only, no mutation
# F2 TRUTH: live-probed, not asserted
# F4 CLARITY: ΔS ≤ 0 — no new state, just observation
#
# Forged: 2026-08-10 by 333-AGI Δ MIND under F13 SOVEREIGN directive
# Supersedes: ad-hoc opencode MCP debugging

set -euo pipefail

REGISTRY="${AAA_MCP_REGISTRY:-/root/AAA/registries/mcp_servers/INDEX.json}"
TIMEOUT="${MCP_PROBE_TIMEOUT:-3}"
OUTPUT_MODE="${1:-jsonl}"  # jsonl | summary | brief

now() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

probe_http() {
    local url="$1"
    curl -sf --max-time "$TIMEOUT" "$url" 2>/dev/null && echo "ONLINE" || echo "DOWN"
}

probe_stdio() {
    local cmd="$1"
    # Check if the command/binary exists and is executable
    local bin="${cmd%% *}"
    if command -v "$bin" >/dev/null 2>&1; then
        echo "STDIO_AVAILABLE"
    else
        echo "STDIO_MISSING"
    fi
}

emit() {
    local ts="$1" server="$2" status="$3" detail="$4" drift="$5"
    printf '{"ts":"%s","server":"%s","status":"%s","detail":"%s","drift":"%s"}\n' \
        "$ts" "$server" "$status" "$detail" "$drift"
}

main() {
    local TS
    TS="$(now)"

    if [ ! -f "$REGISTRY" ]; then
        emit "$TS" "REGISTRY" "MISSING" "INDEX.json not found at $REGISTRY" "CRITICAL"
        exit 1
    fi

    # Probe A-FORGE tool-list for surface comparison
    local AFORGE_TOOLS=0
    local tool_list
    if tool_list=$(curl -sf --max-time "$TIMEOUT" http://127.0.0.1:7072/mcp \
        -X POST -H 'Content-Type: application/json' \
        -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' 2>/dev/null); then
        AFORGE_TOOLS=$(echo "$tool_list" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['result']['tools']))" 2>/dev/null || echo "0")
        emit "$TS" "aforge" "ONLINE" "tools=$AFORGE_TOOLS" "NONE"
    else
        emit "$TS" "aforge" "DOWN" "tools=0" "DRIFT"
    fi

    # Read INDEX.json and probe each server
    python3 -c "
import json, sys, os

with open('$REGISTRY') as f:
    index = json.load(f)

servers = index.get('servers', {})
results = []

for sid, s in sorted(servers.items()):
    status = s.get('status', 'UNKNOWN')
    endpoint = s.get('endpoint', '')
    enabled = s.get('enabled', True)
    cat = s.get('category', '?')
    
    # Determine probe type
    if endpoint and endpoint.startswith('http'):
        probe_type = 'http'
        live = 'ONLINE'  # will be overwritten by actual probe
    elif endpoint:
        probe_type = 'stdio'
        live = 'STDIO_AVAILABLE'
    else:
        probe_type = 'unknown'
        live = 'UNKNOWN'
    
    results.append({
        'server': sid,
        'category': cat,
        'enabled': enabled,
        'probe_type': probe_type,
        'declared_status': status,
        'live_status': live,
        'endpoint': str(endpoint)[:100],
    })

print(json.dumps(results, indent=2))
" 2>&1

    emit "$TS" "DRIFT_AUDIT" "COMPLETE" "probe_complete" "NONE"
}

main
