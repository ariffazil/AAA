#!/bin/bash
# Pre-commit hook: Telegram Bot Token Isolation Check
# Place this in .git/hooks/pre-commit (or use pre-commit framework)
# to block commits that would introduce token sharing.
#
# Detects changes to:
#   - .env files containing TELEGRAM_BOT_TOKEN
#   - config.yaml files containing telegram tokens
#   - Any file with bot token patterns

set -euo pipefail

STAGED_FILES=$(git diff --cached --name-only)
TOKEN_FILES=""

for f in $STAGED_FILES; do
    case "$f" in
        *.env|*.env.*|config.yaml|config.yml|*.json)
            if git diff --cached "$f" | grep -qiE 'telegram.*token|bot_token|TELEGRAM_BOT_TOKEN'; then
                TOKEN_FILES="$TOKEN_FILES $f"
            fi
            ;;
    esac
done

if [ -z "$TOKEN_FILES" ]; then
    # No token-related files staged
    exit 0
fi

echo ""
echo "🔒 Telegram token change detected in staged files:"
echo "   $TOKEN_FILES"
echo ""
echo "Running token isolation audit..."
echo ""

if bash /root/.hermes/scripts/telegram-token-isolation-check.sh; then
    echo ""
    echo "✅ Token isolation check passed. Proceeding with commit."
    exit 0
else
    echo ""
    echo "❌ COMMIT BLOCKED: Token isolation violation detected."
    echo "   Fix the conflict before committing."
    echo "   Run: bash /root/.hermes/scripts/telegram-token-isolation-check.sh"
    exit 1
fi
