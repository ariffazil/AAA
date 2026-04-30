#!/bin/bash
# hermes-restart.sh — apply all FORGE fixes + restart Hermes
# Run as: sudo bash /root/AAA/hermes-restart.sh

set -e
set -o pipefail

ARIFOS_ENV="/root/arifOS/.env"
HERMES_ENV="/root/.hermes/.env"
COMPOSE_OV="/root/arifOS/deployments/af-forge/docker-compose.override.yml"
COMPOSE_BASE="/root/arifOS/deployments/af-forge/docker-compose.yml"

echo "=== HERMES ASI RESTART — FORGE FIX CYCLE ==="

# ── Step 1: Generate and distribute secret ─────────────────────────────────────
if grep -q "ARIFOS_INTERNAL_SECRET_HERMES" "$HERMES_ENV" 2>/dev/null; then
  SECRET=$(grep ARIFOS_INTERNAL_SECRET_HERMES "$HERMES_ENV" | cut -d= -f2)
  echo "✓ Secret already exists in Hermes .env"
else
  SECRET=$(openssl rand -hex 32)
  echo "ARIFOS_INTERNAL_SECRET_HERMES=$SECRET" >> "$HERMES_ENV"
  echo "✓ Secret written to Hermes .env"
fi

if grep -q "ARIFOS_INTERNAL_SECRET_HERMES" "$ARIFOS_ENV" 2>/dev/null; then
  echo "✓ Secret already exists in arifOS .env"
else
  echo "ARIFOS_INTERNAL_SECRET_HERMES=$SECRET" >> "$ARIFOS_ENV"
  echo "✓ Secret written to arifOS .env"
fi

HERMES_SECRET=$(grep ARIFOS_INTERNAL_SECRET_HERMES "$HERMES_ENV" | cut -d= -f2)
ARIFOS_SECRET=$(grep ARIFOS_INTERNAL_SECRET_HERMES "$ARIFOS_ENV" | cut -d= -f2)

if [ "$HERMES_SECRET" != "$ARIFOS_SECRET" ]; then
  echo "ERROR: Secret mismatch between Hermes and arifOS MCP"
  exit 1
fi
echo "✅ Secrets verified identical in both .env files"

# ── Step 2: Create docker-compose override ───────────────────────────────────────
cat > "$COMPOSE_OV" << 'EOF'
# arifOS MCP JWT auth — observe mode (verify before enforce)
services:
  arifosmcp:
    environment:
      ARIFOS_INTERNAL_SECRET_HERMES: "${ARIFOS_INTERNAL_SECRET_HERMES:-}"
      JWT_ENFORCE_MODE: "observe"
EOF
echo "✅ docker-compose override written"

# ── Step 3: Enable Hermes plugins + MCP servers in config.yaml ─────────────────
python3 - << 'PYEOF'
import re

config_path = "/root/.hermes/config.yaml"
with open(config_path) as f:
    content = f.read()

content = re.sub(r'plugins:\s*\n(?:[^\n]*\n)*', '', content)

mcp_block = """
mcp:
  enabled: true
  servers:
    arifosmcp:
      name: arifosmcp
      url: http://127.0.0.1:8080
      transport: streamable-http
      timeout: 30
      auth:
        type: jwt
        algorithm: HS256
        issuer: hermes-gateway
        audience: arifOS-mcp
        secret_env: ARIFOS_INTERNAL_SECRET_HERMES
    geoxmcp:
      name: geoxmcp
      url: http://127.0.0.1:8081
      transport: streamable-http
      timeout: 30
    brave-search:
      name: brave-search
      command: mcp-server-brave-search
      transport: stdio
      env:
        BRAVE_API_KEY: \\${BRAVE_API_KEY}
    context7:
      name: context7
      command: context7-mcp
      transport: stdio
      env:
        CONTEXT7_API_KEY: \\${CONTEXT7_API_KEY}
      tools:
        resources: false
        prompts: false
    github:
      name: github
      command: github-mcp-server
      transport: stdio
      env:
        GITHUB_PERSONAL_ACCESS_TOKEN: \\${GITHUB_PERSONAL_ACCESS_TOKEN}
      tools:
        include: [create_issue, list_issues, get_issue, search_code, search_repositories]
        resources: true
        prompts: false

"""

# Remove existing mcp section if any
content = re.sub(
    r'mcp:\s*\n\s*enabled:\s*true\s*\n(?:.*?\n)*?(?=\ncontext_compression:|\nplugins:|\ncode_execution:|\Z)',
    '',
    content,
    flags=re.DOTALL
)

# Insert mcp block before context_compression
content = content.replace('context_compression:', mcp_block + 'context_compression:')

# Append/replace plugins at end
content = content.rstrip() + "\n\nplugins:\n  enabled:\n    - hermes-jwt-auth\n    - aaa-governance\n    - vault999-wrapper\n    - a2a-coord\n    - session-lock\n    - memory-integrity\n    - workspace-guard\n    - skillset-audit\n"

with open(config_path, "w") as f:
    f.write(content)

print("✅ config.yaml updated: plugins + MCP servers (brave-search, context7, github)")
PYEOF

# ── Step 4: Reload arifOS MCP with override ─────────────────────────────────────
cd /root/arifOS
docker compose -f "$COMPOSE_BASE" -f "$COMPOSE_OV" up -d arifosmcp
echo "✅ arifOS MCP reloaded (observe mode)"

sleep 5

if docker ps --format '{{.Names}}' | grep -q arifosmcp; then
  echo "✅ arifOS MCP container healthy"
else
  echo "WARNING: arifOS MCP container not running"
fi

# ── Step 5: Verify MCP responds (observe mode = 200 without token) ───────────────
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' 2>/dev/null)

echo "arifOS MCP HTTP status: $HTTP_STATUS (expect 200 in observe mode)"

# ── Step 6: Restart Hermes gateway ──────────────────────────────────────────────
echo "Restarting Hermes gateway..."
pkill -f "hermes.*gateway.*run" 2>/dev/null || true
sleep 2
/root/.hermes/venv/bin/python -m hermes_cli.main gateway run --replace &
HERMES_PID=$!
sleep 5

if kill -0 $HERMES_PID 2>/dev/null; then
  echo "✅ Hermes gateway restarted (PID $HERMES_PID)"
else
  echo "ERROR: Hermes gateway failed to start"
  exit 1
fi

echo ""
echo "=== FORGE FIX CYCLE COMPLETE ==="
echo "Secret: $(echo $SECRET | cut -c1-8)..."
echo "Plugins enabled: hermes-jwt-auth, aaa-governance, vault999-wrapper,"
echo "                 a2a-coord, session-lock, memory-integrity,"
echo "                 workspace-guard, skillset-audit"
echo "Next: await Hermes validation (auto-announce)"
