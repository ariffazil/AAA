#!/usr/bin/env bash
# antigravity-post-seal.sh — PostToolUse hook: seals every file mutation to VAULT999
# Receives tool payload on stdin (JSON), calls arif_seal on arifOS kernel
set -euo pipefail

# Read stdin payload
INPUT=$(cat)

# Extract tool name from the payload
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('toolCall',{}).get('name','unknown'))" 2>/dev/null || echo "unknown")
STEP_IDX=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('stepIdx','?'))" 2>/dev/null || echo "?")
CONV_ID=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('conversationId','?'))" 2>/dev/null || echo "?")

# Build seal payload
SEAL_PAYLOAD=$(python3 -c "
import json, sys, datetime
payload = json.load(sys.stdin)
seal = {
    'tool_call': payload.get('toolCall', {}).get('name', 'unknown'),
    'step_idx': payload.get('stepIdx', -1),
    'conversation_id': payload.get('conversationId', 'unknown'),
    'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
    'agent': 'antigravity-cli',
    'error': payload.get('error', None)
}
print(json.dumps(seal))
" <<< "$INPUT")

# Call arifOS seal via MCP
RESPONSE=$(curl -s -X POST http://localhost:8088/mcp \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "
import json
req = {
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'arif_seal',
        'arguments': {
            'mode': 'seal',
            'payload': '''$SEAL_PAYLOAD''',
            'seal_purpose': 'antigravity-post-tool',
            'witness_type': 'ai'
        }
    },
    'id': 1
}
print(json.dumps(req))
")" 2>/dev/null || echo '{"error":"seal_unreachable"}')

# Output empty JSON — hook expects {} on stdout
echo "{}"

# Log silently
echo "[seal] $TOOL_NAME step=$STEP_IDX conv=$CONV_ID → $(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin).get('result',{}).get('status','sent'))" 2>/dev/null || echo 'logged')" >> /root/.gemini/antigravity-cli/log/seal.log 2>/dev/null || true
