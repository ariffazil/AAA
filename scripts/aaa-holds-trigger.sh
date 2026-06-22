#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# AAA_HOLDS Trigger — reads AAA_HOLDS.md, triggers OpenClaw agent for
# APPROVED-but-unexecuted holds. Runs every 5 min via system cron.
# ═══════════════════════════════════════════════════════════════════════
set -euo pipefail

PARSER="/root/.openclaw/workspace/scripts/aaa-holds-parser.py"
STATE="/root/.openclaw/workspace/.aaa-holds-state.json"
LOG="/var/log/aaa-holds.log"
HOLDS_FILE="/root/.openclaw/workspace/AAA_HOLDS.md"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Ensure log dir exists
mkdir -p "$(dirname "$LOG")"

# Check OpenClaw gateway is up before attempting agent call
if ! systemctl is-active --quiet openclaw-gateway 2>/dev/null; then
    echo "[$TIMESTAMP] SKIP: openclaw-gateway not active" >> "$LOG"
    exit 0
fi

# Run parser
RESULT=$(/usr/bin/python3 "$PARSER" 2>/dev/null || echo '{"count":0,"status":"parser_error"}')
COUNT=$(echo "$RESULT" | /usr/bin/python3 -c "import sys,json; print(json.load(sys.stdin).get('count',0))")
STATUS=$(echo "$RESULT" | /usr/bin/python3 -c "import sys,json; print(json.load(sys.stdin).get('status','unknown'))")

echo "[$TIMESTAMP] check status=$STATUS count=$COUNT" >> "$LOG"

if [ "$COUNT" -eq 0 ]; then
    exit 0
fi

# Build agent message with hold details
# Note: we pass the JSON directly; the agent will parse and execute
MESSAGE=$(echo "$RESULT" | /usr/bin/python3 -c '
import sys, json
data = json.load(sys.stdin)
holds = data.get("holds", [])
if not holds:
    sys.exit(0)
lines = [
    "🛡️ 888_HOLD BATCH EXECUTION",
    "",
    "The following holds have been APPROVED by Arif and are queued for execution:",
    "",
]
for h in holds:
    lines.append(f"• ID: {h[\"id\"]}")
    lines.append(f"  Request: {h[\"request\"]}")
    lines.append(f"  Decided by: {h[\"decided_by\"]} at {h[\"when\"]}")
    lines.append("")
lines.extend([
    "INSTRUCTIONS:",
    "1. Execute each request using available tools (terminal, file, shell, etc.)",
    "2. After EACH execution, update the state file to mark it done:",
    f"   Run: python3 /root/.openclaw/workspace/scripts/aaa-holds-mark-executed.py <hold_id>",
    "3. Log every action to VAULT999 via arifOS MCP if possible.",
    "4. If a hold cannot be executed safely, write a new 888_HOLD explaining why.",
    "5. Reply to Arif (267378578) with a summary of what was executed.",
    "",
    "DO NOT execute irreversible actions without double-checking the request.",
])
print("\n".join(lines))
')

if [ -z "$MESSAGE" ]; then
    exit 0
fi

# Mark holds as PENDING in state file before triggering agent
echo "$RESULT" | /usr/bin/python3 -c "
import sys, json
result = json.load(sys.stdin)
state = json.load(open('$STATE')) if __import__('os').path.exists('$STATE') else {'executed': [], 'pending': []}
for h in result.get('holds', []):
    if h['id'] not in state['executed'] and h['id'] not in state['pending']:
        state['pending'].append(h['id'])
state['last_check'] = '$TIMESTAMP'
json.dump(state, open('$STATE', 'w'), indent=2)
"

echo "[$TIMESTAMP] Triggering agent for $COUNT holds" >> "$LOG"

# Trigger OpenClaw agent turn
# Using --deliver --to 267378578 to send result to Arif
/usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js agent \
    --message "$MESSAGE" \
    --deliver \
    --to 267378578 \
    --thinking medium \
    --timeout 600 \
    2>> "$LOG" || true

echo "[$TIMESTAMP] Agent trigger complete" >> "$LOG"
