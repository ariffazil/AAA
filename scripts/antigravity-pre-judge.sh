#!/usr/bin/env bash
# antigravity-pre-judge.sh — PreToolUse hook: gates write mutations through arif_judge
# Returns: {"decision": "allow|deny|ask", "reason": "..."}
set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('toolCall',{}).get('name','unknown'))" 2>/dev/null || echo "unknown")
TOOL_ARGS=$(echo "$INPUT" | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin).get('toolCall',{}).get('args',{})))" 2>/dev/null || echo "{}")

# Build judge payload
JUDGE_PAYLOAD=$(python3 -c "
import json, sys
payload = json.load(sys.stdin)
tool = payload.get('toolCall',{})
judge = {
    'mode': 'intercept',
    'candidate': json.dumps(tool),
    'action_tier': 'standard',
    'reversibility_level': 'reversible',
    'domain': 'filesystem',
    'niat_params': {
        'intent': 'file_mutation',
        'tool': tool.get('name','unknown'),
        'path_hint': str(tool.get('args',{}).get('file_path',''))
    }
}
print(json.dumps(judge))
" <<< "$INPUT")

# Call arif_judge via MCP
RESPONSE=$(curl -s -X POST http://localhost:8088/mcp \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "
import json
req = {
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'arif_judge',
        'arguments': {
            'mode': 'intercept',
            'candidate': '''$JUDGE_PAYLOAD''',
            'action_tier': 'standard'
        }
    },
    'id': 1
}
print(json.dumps(req))
")" 2>/dev/null)

# Parse verdict from response
VERDICT=$(echo "$RESPONSE" | python3 -c "
import sys, json
try:
    resp = json.load(sys.stdin)
    result = resp.get('result', {})
    verdict = result.get('verdict', 'allow')
    reason = result.get('reason', verdict)
    # Map arifOS verdicts to hook decisions
    verdict_map = {
        'SEAL': 'allow',
        'SABAR': 'ask',
        'HOLD': 'deny',
        'VOID': 'deny'
    }
    decision = verdict_map.get(verdict, 'allow')
    out = {'decision': decision, 'reason': str(reason)[:200]}
    print(json.dumps(out))
except:
    print(json.dumps({'decision': 'allow', 'reason': 'judge unreachable — allowing'}))
" 2>/dev/null || echo '{"decision":"allow","reason":"judge parse error — allowing"}')

echo "$VERDICT"
echo "[judge] $TOOL_NAME → $VERDICT" >> /root/.gemini/antigravity-cli/log/judge.log 2>/dev/null || true
