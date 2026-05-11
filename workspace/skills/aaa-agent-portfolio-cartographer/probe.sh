#!/bin/bash
# aaa-agent-portfolio-cartographer — Probe Runner
# Phase 1–5 execution for portfolio cartographer skill

OUTPUT_FILE="${1:-/root/.openclaw/workspace/portfolio-map.json}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "=== AAA Portfolio Cartographer ==="
echo "Timestamp: $TIMESTAMP"
echo ""

# Phase 1: Docker containers
echo "[Phase 1] Docker containers..."
DOCKER_PS=$(docker ps --format "{{.Names}}\t{{.Status}}" 2>/dev/null || echo "DOCKER_UNAVAILABLE")
echo "$DOCKER_PS"

# Phase 2: Listening ports
echo ""
echo "[Phase 2] Listening ports..."
PORTS=$(ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null || echo "PORTS_UNAVAILABLE")
echo "$PORTS"

# Phase 3: Health endpoints
echo ""
echo "[Phase 3] Health endpoints..."

health_check() {
  local name=$1
  local url=$2
  local result
  result=$(curl -s --max-time 3 "$url" 2>/dev/null)
  if [ $? -eq 0 ] && [ -n "$result" ]; then
    echo "$name: CLAIM — $result"
  else
    echo "$name: PLAUSIBLE — unreachable"
  fi
}

health_check "arifOS" "http://localhost:8080/health"
health_check "GEOX" "http://localhost:8081/health"
health_check "WEALTH" "http://localhost:8082/health"
health_check "WELL" "http://localhost:8083/health"
health_check "AAA" "http://localhost:3001/health"
health_check "A-FORGE" "http://localhost:7071/health"

# Phase 4: OpenClaw gateway
echo ""
echo "[Phase 4] OpenClaw gateway..."
OPENCLAW_HEALTH=$(openclaw health --json 2>/dev/null || echo "OPENCLAW_UNAVAILABLE")
echo "$OPENCLAW_HEALTH"

# Phase 5: Tailscale
echo ""
echo "[Phase 5] Tailscale..."
TAILSCALE_STATUS=$(tailscale status 2>/dev/null || echo "TAILSCALE_UNAVAILABLE")
echo "$TAILSCALE_STATUS"

echo ""
echo "=== Probe Complete ==="
echo "Output saved to: $OUTPUT_FILE"