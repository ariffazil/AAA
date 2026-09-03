#!/bin/bash
# SCALPEL — Telegram Bot Token Isolation Audit
# TREE777 enforcement script
# Validates that agent Telegram tokens are properly isolated.
# Run after every config change that touches bot tokens.
#
# Usage: bash /root/.hermes/scripts/telegram-token-isolation-check.sh

set -euo pipefail

ERRORS=0

echo "=== SCALPEL | Telegram Token Isolation Audit ==="
echo "Timestamp: $(date -Iseconds)"
echo ""

# ── 1. Extract tokens from ACTUAL config locations ──
OPENCLAW_TOKEN=""
HERMES_TOKEN=""
A_FORGE_TOKEN=""

# OpenClaw token — from openclaw.json (not .env)
OPENCLAW_TOKEN=$(python3 -c "
import json
with open('/root/.openclaw/openclaw.json') as f:
    d = json.load(f)
    print(d.get('channels', {}).get('telegram', {}).get('botToken', ''))
" 2>/dev/null || true)

# Hermes token — from HERMES/.env (canonical), not config.yaml
HERMES_TOKEN=$(grep -E '^TELEGRAM_BOT_TOKEN=' /root/HERMES/.env 2>/dev/null | cut -d= -f2 | tr -d '"' || true)

# A-FORGE token — from docker-compose.yml (NOTIFIER_TELEGRAM_BOT_TOKEN)
A_FORGE_TOKEN=$(python3 -c "
import re
with open('/root/A-FORGE/infra/live/compose/docker-compose.yml') as f:
    content = f.read()
match = re.search(r'NOTIFIER_TELEGRAM_BOT_TOKEN:\s*[\'\"]([^\'\"]{10,})[\'\"]', content)
print(match.group(1).split(':')[0] if match else '')
" 2>/dev/null || true)

# ── 2. Normalize (keep only prefix for comparison) ──
OPENCLAW_PREFIX="${OPENCLAW_TOKEN%%:*}"
HERMES_PREFIX="${HERMES_TOKEN%%:*}"
A_FORGE_PREFIX="${A_FORGE_TOKEN%%:*}"

echo "Agents detected:"
echo "  OpenClaw:  ${OPENCLAW_PREFIX:-<none>}"
echo "  Hermes:    ${HERMES_PREFIX:-<none>}"
echo "  A-FORGE:   ${A_FORGE_PREFIX:-<none>}"
echo ""

# ── 3. Rule: OpenClaw ≠ Hermes (CRITICAL — TREE777 core rule) ──
if [ -n "$OPENCLAW_PREFIX" ] && [ -n "$HERMES_PREFIX" ]; then
    if [ "$OPENCLAW_PREFIX" = "$HERMES_PREFIX" ]; then
        echo "❌ VIOLATION: OpenClaw and Hermes share the same Telegram bot token!"
        echo "   OpenClaw: $OPENCLAW_PREFIX"
        echo "   Hermes:   $HERMES_PREFIX"
        echo "   ACTION: Generate new token for one agent. Do NOT proceed."
        ERRORS=$((ERRORS + 1))
    else
        echo "✅ Rule: OpenClaw token ≠ Hermes token ($OPENCLAW_PREFIX vs $HERMES_PREFIX)"
    fi
else
    echo "⚠️  Warning: Could not verify OpenClaw/Hermes token isolation (one or both missing)"
fi

# ── 4. Rule: OpenClaw can share with A-FORGE (send-only exception) ──
if [ -n "$OPENCLAW_PREFIX" ] && [ -n "$A_FORGE_PREFIX" ]; then
    if [ "$OPENCLAW_PREFIX" = "$A_FORGE_PREFIX" ]; then
        echo "✅ Rule: OpenClaw/A-FORGE token sharing is INTENTIONAL (A-FORGE send-only, no receive)"
    fi
fi

# ── 5. Rule: No duplicate tokens across RECEIVING agents ──
# Only agents that RECEIVE messages need unique tokens
# A-FORGE is send-only, so it's excluded from this rule
ALL_PREFIXES=""
[ -n "$OPENCLAW_PREFIX" ] && ALL_PREFIXES="$ALL_PREFIXES
$OPENCLAW_PREFIX"
[ -n "$HERMES_PREFIX" ] && ALL_PREFIXES="$ALL_PREFIXES
$HERMES_PREFIX"

DUPLICATES=$(echo -e "$ALL_PREFIXES" | grep -v '^$' | sort | uniq -d)
if [ -n "$DUPLICATES" ]; then
    echo "❌ VIOLATION: Duplicate Telegram bot tokens detected across receiving agents:"
    echo "$DUPLICATES" | while read -r dup; do
        echo "    - $dup"
    done
    ERRORS=$((ERRORS + 1))
else
    echo "✅ Rule: No duplicate Telegram bot tokens across receiving agents"
fi

# ── 6. Verify Telegram bot usernames ──
echo ""
echo "=== Telegram Bot Identity Verification ==="

verify_bot() {
    local token="$1"
    local label="$2"
    if [ -z "$token" ]; then
        echo "  $label: <no token>"
        return
    fi
    local result
    result=$(curl -s "https://api.telegram.org/bot${token}/getMe" 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
if d.get('ok'):
    print(d['result']['username'])
else:
    print('ERROR:' + d.get('description', 'unknown'))
" 2>/dev/null || echo "CURL_FAILED")
    echo "  $label: @$result"
}

verify_bot "$OPENCLAW_TOKEN" "OpenClaw"
verify_bot "$HERMES_TOKEN" "Hermes"
verify_bot "$A_FORGE_TOKEN" "A-FORGE"

# ── 7. Summary ──
echo ""
if [ $ERRORS -eq 0 ]; then
    echo "=== AUDIT PASS | No violations found ==="
    exit 0
else
    echo "=== AUDIT FAIL | $ERRORS violation(s) found ==="
    exit 1
fi