#!/bin/bash
# federation-parity-probe.sh
# arifOS Federation MCP transport parity probe
# Forged: 2026-06-12 by Hermes
# Run: bash /root/AAA/scripts/federation-parity-probe.sh
#
# If public /mcp returns 404, deployment is DOMAIN_HOLD.
# If local /mcp works but public /mcp fails, ingress is broken.
# If public initialize works but tools/call fails, tool runtime is broken.
# If tool runtime returns isError=true, domain logic is broken.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

TARGETS=(
  "arifos:https://arifos.arif-fazil.com/mcp:8088"
  "geox:https://geox.arif-fazil.com/mcp:8081"
  "wealth:https://wealth.arif-fazil.com/mcp:18082"
  "well:https://well.arif-fazil.com/mcp:18083"
)

INIT_PAYLOAD='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"federation-parity","version":"1.0"}}}'
TOOLS_PAYLOAD='{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'

PASS=0
FAIL=0

echo "════════════════════════════════════════════════════"
echo "  arifOS Federation MCP Parity Probe"
echo "  $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "════════════════════════════════════════════════════"
echo ""

for target in "${TARGETS[@]}"; do
  IFS=':' read -r NAME URL LOCAL_PORT <<< "$target"
  
  echo "── ${NAME} ──────────────────────────────────────────"
  
  # 1. Local health
  LOCAL_HEALTH=$(curl -sS -o /dev/null -w "%{http_code}" "http://127.0.0.1:${LOCAL_PORT}/health" 2>/dev/null || echo "000")
  if [ "$LOCAL_HEALTH" = "200" ]; then
    echo -e "  ${GREEN}[PASS]${NC} local health → ${LOCAL_HEALTH}"
    ((PASS++))
  else
    echo -e "  ${RED}[FAIL]${NC} local health → ${LOCAL_HEALTH}"
    ((FAIL++))
  fi

  # 2. Public initialize
  PUBLIC_INIT=$(curl -sS -o /dev/null -w "%{http_code}" \
    -X POST \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -H "MCP-Protocol-Version: 2025-06-18" \
    -d "$INIT_PAYLOAD" \
    "$URL" 2>/dev/null || echo "000")
  
  case "$PUBLIC_INIT" in
    200)
      echo -e "  ${GREEN}[PASS]${NC} public initialize → ${PUBLIC_INIT}"
      ((PASS++))
      ;;
    307)
      echo -e "  ${YELLOW}[WARN]${NC} public initialize → ${PUBLIC_INIT} (redirect — retry with trailing slash or follow)"
      # Retry with -L
      PUBLIC_INIT2=$(curl -sS -o /dev/null -w "%{http_code}" -L \
        -X POST \
        -H "Content-Type: application/json" \
        -H "Accept: application/json, text/event-stream" \
        -d "$INIT_PAYLOAD" \
        "$URL" 2>/dev/null || echo "000")
      if [ "$PUBLIC_INIT2" = "200" ]; then
        echo -e "  ${GREEN}[PASS]${NC} public initialize (follow redirect) → ${PUBLIC_INIT2}"
        ((PASS++))
      else
        echo -e "  ${RED}[FAIL]${NC} public initialize (follow redirect) → ${PUBLIC_INIT2}"
        ((FAIL++))
      fi
      ;;
    404)
      echo -e "  ${RED}[FAIL]${NC} public initialize → ${PUBLIC_INIT} (DOMAIN_HOLD — ingress broken)"
      ((FAIL++))
      ;;
    *)
      echo -e "  ${YELLOW}[WARN]${NC} public initialize → ${PUBLIC_INIT} (unexpected)"
      ((FAIL++))
      ;;
  esac

  # 3. Public tools/list
  TOOLS_RESULT=$(curl -sS \
    -X POST \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d "$TOOLS_PAYLOAD" \
    "$URL" 2>/dev/null || echo '{"error":"curl_failed"}')
  
  TOOL_COUNT=$(echo "$TOOLS_RESULT" | python3 -c "import sys,json; r=json.load(sys.stdin); print(len(r.get('result',{}).get('tools',[])))" 2>/dev/null || echo "0")
  
  if [ "$TOOL_COUNT" -gt 0 ] 2>/dev/null; then
    echo -e "  ${GREEN}[PASS]${NC} public tools/list → ${TOOL_COUNT} tools"
    ((PASS++))
  else
    echo -e "  ${RED}[FAIL]${NC} public tools/list → ${TOOL_COUNT} tools"
    ((FAIL++))
  fi

  echo ""
done

echo "════════════════════════════════════════════════════"
TOTAL=$((PASS + FAIL))
echo "  Results: ${PASS}/${TOTAL} PASS"
if [ "$FAIL" -gt 0 ]; then
  echo -e "  ${RED}${FAIL} FAILURES DETECTED${NC}"
  echo "  DOMAIN_HOLD if public /mcp returned 404"
else
  echo -e "  ${GREEN}ALL CHECKS PASSED${NC}"
fi
echo "════════════════════════════════════════════════════"
echo ""

exit $FAIL
