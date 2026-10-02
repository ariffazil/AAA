#!/bin/bash
# aaa-completion-check.sh — Stop hook
# Anti-fake-completion gate. Checks if agent claimed "done" without evidence.
# Event: Stop (blockable)
# Reads: stdin (JSON with final response)
# Writes: decision to stdout
# Exit 0 = allow stop, Exit 2 = block and force continuation

set -euo pipefail

TELEMETRY_DIR="/root/AAA/cockpit/red-blue-gold-20261002/staging/telemetry"
mkdir -p "$TELEMETRY_DIR" 2>/dev/null || true

# Read stdin (stop event JSON)
INPUT=$(cat 2>/dev/null || echo '{}')

# Extract the agent's final response
RESPONSE=$(echo "$INPUT" | jq -r '.response // .message // ""' 2>/dev/null || echo "")
SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // "unknown"' 2>/dev/null || echo "unknown")

if [ -z "$RESPONSE" ]; then
    # No response to check — allow stop
    exit 0
fi

# STRONG handles (P2 claim-without-handle binding, 2026-09-12):
# a completion claim must carry at least one VERIFIABLE handle —
# an existing-looking path, a git SHA, a chain hash, or live probe telemetry.
# Word-evidence alone ("receipt", "sealed", "successfully") is NO LONGER sufficient.
STRONG_PATTERNS=(
    '(/[a-zA-Z0-9._-]+){2,}'          # absolute path (2+ segments)
    '\b[0-9a-f]{7,40}\b'              # git SHA / chain hash
    'chain_hash'                       # ritual marker reference
    'PID [0-9]+'                       # live process witness
    '(active|exit.?code|HTTP [0-9]{3}|0 restart)'  # probe telemetry
)
HAS_HANDLE=false
for pattern in "${STRONG_PATTERNS[@]}"; do
    if echo "$RESPONSE" | grep -qE "$pattern" 2>/dev/null; then
        HAS_HANDLE=true
        break
    fi
done

# Weak evidence markers — logged for telemetry, NOT sufficient alone
EVIDENCE_MARKERS=(
    'commit' 'diff' 'test' 'passed' 'failed' '✓' '✗'
    'file:' 'path:' 'created:' 'modified:' 'wrote' 'edited'
    'patched' 'deployed' 'health' 'probe' 'sealed' 'receipt'
)
HAS_WEAK=false
for marker in "${EVIDENCE_MARKERS[@]}"; do
    if echo "$RESPONSE" | grep -qi "$marker" 2>/dev/null; then
        HAS_WEAK=true
        break
    fi
done

# Completion claim patterns (agent saying "done")
COMPLETION_PATTERNS=(
    'done\.'
    'complete\.'
    'finished\.'
    'all set'
    'task complete'
    'work complete'
    'changes applied'
    'successfully'
)

# Check if agent claimed completion
CLAIMED_DONE=false
for pattern in "${COMPLETION_PATTERNS[@]}"; do
    if echo "$RESPONSE" | grep -qiE "$pattern" 2>/dev/null; then
        CLAIMED_DONE=true
        break
    fi
done

if [ "$CLAIMED_DONE" = false ]; then
    # No completion claim — allow stop (might be a question, partial work, etc.)
    exit 0
fi

# Check if evidence markers exist
HAS_EVIDENCE=false
for marker in "${EVIDENCE_MARKERS[@]}"; do
    if echo "$RESPONSE" | grep -qi "$marker" 2>/dev/null; then
        HAS_EVIDENCE=true
        break
    fi
done

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [ "$HAS_HANDLE" = true ]; then
    # Completion claim + verifiable handle = legitimate
    cat >> "$TELEMETRY_DIR/completion-check.jsonl" <<EOF
{"ts":"$TIMESTAMP","session":"$SESSION_ID","event":"Stop","verdict":"ALLOW","reason":"strong_handle","weak_only":$HAS_WEAK}
EOF
    exit 0
else
    # Completion claim WITHOUT a verifiable handle = claim-without-handle (P2 VOID)
    cat >> "$TELEMETRY_DIR/completion-check.jsonl" <<EOF
{"ts":"$TIMESTAMP","session":"$SESSION_ID","event":"Stop","verdict":"BLOCK","reason":"no_strong_handle","claim_without_handle":true,"weak_words_only":$HAS_WEAK}
EOF

    # Block the stop — force agent to provide verifiable handles
    echo '{"decision":"block","message":"⚠️ CLAIM-WITHOUT-HANDLE (P2): You claimed completion but carried no verifiable handle — no path, git SHA, chain hash, or probe telemetry. Words like receipt/sealed/successfully are claims, not evidence. Continue: attach path + hash + timestamp, or rewrite as belum direkodkan. DITEMPA BUKAN DIBERI."}'
    exit 2
fi
