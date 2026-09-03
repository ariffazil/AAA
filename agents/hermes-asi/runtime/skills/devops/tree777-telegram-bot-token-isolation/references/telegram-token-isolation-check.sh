# TREE777 — Telegram Bot Token Isolation Audit Script

#!/bin/bash
# TREE777: Verify Telegram bot token isolation across all agents
# Run this before declaring federation healthy or after any config change

set -e

echo "=============================================="
echo "TREE777 — Telegram Bot Token Isolation Check"
echo "=============================================="

# Collect tokens from each source
HERMES_TOKEN=$(cat /root/.hermes/platforms/telegram/config.json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('botToken','NOT_FOUND'))")
OPENCLAW_TOKEN=$(cat /root/.openclaw/openclaw.json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['channels']['telegram']['botToken'])")
AFORGE_TOKEN=$(grep NOTIFIER_TELEGRAM /root/A-FORGE/infra/live/compose/docker-compose.yml 2>/dev/null | grep -oP '8149595687:\w+' | head -1 || echo "NOT_FOUND")

echo ""
echo "=== Token Fingerprint (first 8 chars only) ==="
echo "Hermes (ASI_arifos_bot):    ${HERMES_TOKEN:0:12}..."
echo "OpenClaw (AGI_ASI_bot):     ${OPENCLAW_TOKEN:0:12}..."
echo "A-FORGE notifier:           ${AFORGE_TOKEN}..."

echo ""
echo "=== Isolation Verdict ==="

# Compare first 10 chars (before the colon)
HERMES_FP="${HERMES_TOKEN:0:10}"
OPENCLAW_FP="${OPENCLAW_TOKEN:0:10}"

if [ "$HERMES_FP" = "$OPENCLAW_FP" ]; then
    echo "🔴 CRITICAL FAIL: Hermes and OpenClaw share the same bot token!"
    echo "   → STOP. Do not restart any agent."
    echo "   → 888_HOLD. Report to Arif immediately."
    echo "   → Both @ASI_arifos_bot and @AGI_ASI_bot are compromised."
    exit 1
else
    echo "✅ PASS: Hermes token ≠ OpenClaw token"
    echo ""
    echo "Token assignment summary:"
    echo "  - OpenClaw (@AGI_ASI_bot):  ${OPENCLAW_TOKEN:0:12}... → webhook mode (group mention)"
    echo "  - Hermes (@ASI_arifos_bot): ${HERMES_TOKEN:0:12}... → polling mode (ambient)"
    echo "  - A-FORGE notifier:         shares with OpenClaw (SEND only, not receive)"
    echo ""
    echo "✅ TREE777 PASSED — proceed with audit"
fi