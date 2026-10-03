#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  mcp-lifeguard probe — Federation MCP health monitor           ║
# ║  Updated: 2026-05-26 — added Hermes A2A + Redis telemetry     ║
# ║  Targets: arifOS:8088, WEALTH:18082, arifosd:18081, Hermes   ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

LOGFILE="/root/.openclaw/logs/mcp-lifeguard.log"
ALERT_LOG="/root/.openclaw/logs/mcp-lifeguard-alerts.log"
mkdir -p "$(dirname "$LOGFILE")"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; echo "[$(TS)] ALERT: $*"; }

# ─── MCP endpoint registry (updated 2026-05-25) ─────────────────
declare -A MCP_ENDPOINTS=(
    ["arifOS MCP"]="http://localhost:8088/health"
    ["WEALTH MCP"]="http://localhost:18082/health"
    ["arifosd"]="http://localhost:18081/health"
)

declare -A MCP_SERVICE=(
    ["arifOS MCP"]="arifos.service"
    ["WEALTH MCP"]="wealth-organ.service"
    ["arifosd"]="arifosd.service"
)

log "=== mcp-lifeguard probe start ==="

FAILURES=0
declare -A RESTART_COUNT
declare -A TOTAL_RESTARTS

for svc in "${!MCP_ENDPOINTS[@]}"; do
    url="${MCP_ENDPOINTS[$svc]}"
    svc_name="${MCP_SERVICE[$svc]}"
    
    # Try health endpoint
    http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null || echo "000")
    
    if [ "$http_code" = "200" ]; then
        log "OK: $svc ($url) → HTTP $http_code"
        RESTART_COUNT[$svc]=0
        continue
    fi
    
    # Fallback: try MCP JSON-RPC initialize
    mcp_url="${url%/health}/mcp"
    mcp_resp=$(curl -s -X POST "$mcp_url" \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"mcp-lifeguard","version":"2.0.0"}}}' \
        --max-time 5 2>/dev/null || true)
    
    if echo "$mcp_resp" | grep -q '"jsonrpc"'; then
        log "OK: $svc ($mcp_url) → MCP responds"
        RESTART_COUNT[$svc]=0
        continue
    fi
    
    alert "CRITICAL: $svc unreachable (HTTP $http_code, MCP no response)"
    FAILURES=$((FAILURES + 1))
    
    # Track restarts
    RESTART_COUNT[$svc]=$(( ${RESTART_COUNT[$svc]:-0} + 1 ))
    TOTAL_RESTARTS[$svc]=$(( ${TOTAL_RESTARTS[$svc]:-0} + 1 ))
    
    # Auto-heal via systemd
    log "Auto-healing: systemctl restart $svc_name"
    systemctl restart "$svc_name" >> "$LOGFILE" 2>&1 || alert "Failed to restart $svc_name via systemd"
    
    # Wait and re-verify
    sleep 8
    retry_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null || echo "000")
    if [ "$retry_code" = "200" ]; then
        log "RECOVERED: $svc after restart"
        RESTART_COUNT[$svc]=0
    else
        alert "PERSISTENT: $svc still down after restart (HTTP $retry_code)"
        
        # Escalation: 3+ restarts = alert with details
        if [ "${TOTAL_RESTARTS[$svc]:-0}" -ge 3 ]; then
            alert "ESCALATION: $svc has failed ${TOTAL_RESTARTS[$svc]} times — manual intervention required"
            alert "  Last error: HTTP $retry_code on $url"
            alert "  Service: $svc_name"
            alert "  PID: $(systemctl show -p MainPID --value $svc_name 2>/dev/null)"
        fi
    fi
done

# ─── Check OpenClaw Gateway ───────────────────────────────────────
openclaw_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "http://localhost:18789/health" 2>/dev/null || echo "000")
if [ "$openclaw_code" != "200" ]; then
    alert "WARNING: OpenClaw Gateway (localhost:18789) → HTTP $openclaw_code"
else
    log "OK: OpenClaw Gateway (localhost:18789) → HTTP $openclaw_code"
fi

# Deliberation is part of the canonical AAA service already probed on :3001.

# ─── Check Hermes A2A Bridge (port 18001) ─────────────────────────
hermes_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "http://localhost:18001/.well-known/agent-card.json" 2>/dev/null || echo "000")
if [ "$hermes_code" != "200" ]; then
    alert "WARNING: Hermes A2A bridge (localhost:18001) → HTTP $hermes_code"
else
    log "OK: Hermes A2A bridge (localhost:18001) → HTTP $hermes_code"
fi

# ─── Check Hermes Telemetry via Redis ───────────────────────────────
# federation:hermes:session_telemetry — written by federation-memory-broker plugin
if command -v redis-cli &>/dev/null; then
    telemetry=$(redis-cli get federation:hermes:session_telemetry 2>/dev/null || echo "ERR")
    if [ "$telemetry" = "ERR" ] || [ -z "$telemetry" ]; then
        alert "WARNING: Hermes Redis telemetry key empty or Redis unreachable"
    else
        active_sessions=$(echo "$telemetry" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('active_sessions','?'))" 2>/dev/null || echo "?")
        tool_calls=$(echo "$telemetry" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_calls_24h','?'))" 2>/dev/null || echo "?")
        log "OK: Hermes telemetry → sessions=$active_sessions tool_calls_24h=$tool_calls"
    fi
else
    log "SKIP: redis-cli not available — Hermes telemetry not reachable"
fi

# ─── Check Ollama ─────────────────────────────────────────────────
ollama_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "http://localhost:11434/api/tags" 2>/dev/null || echo "000")
if [ "$ollama_code" != "200" ]; then
    alert "WARNING: Ollama (localhost:11434) → HTTP $ollama_code"
else
    log "OK: Ollama (localhost:11434) → HTTP $ollama_code"
fi

log "Probe complete. failures=$FAILURES"
echo ""
if [ $FAILURES -gt 0 ]; then
    echo "⚠️  $FAILURES service(s) had issues — see $ALERT_LOG"
else
    echo "✅ All MCP services healthy"
fi
