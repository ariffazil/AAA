#!/bin/bash
# ⚒️ opencode_agentic.sh — Headless OpenCode Execution Hook
# arifOS Federation: Init → Execute → Seal (ΔS ≤ 0)
# 
# Usage: opencode_agentic.sh "your task prompt here"
#        opencode_agentic.sh --model deepseek/deepseek-v4-pro "task"
#        opencode_agentic.sh --agent auditor "audit the federation"
#
# Forged: 2026-07-20 by FORGE (000Ω) under F13 SOVEREIGN directive
# Doctrine: DITEMPA BUKAN DIBERI

set -euo pipefail
IFS=$'\n\t'

# ── Config ──────────────────────────────────────────────
BRIDGE="/root/AAA/docs/CONTINUITY_BRIDGE.md"
CHRONICLE="/root/AAA/scripts/chronicle_vault999.py"
MEMORY_BRIDGE="/root/AAA/scripts/memory_bridge.py"
SEAL_CHAIN="/root/.local/share/arifos/vault999/seal_chain.jsonl"
WORK_LOG="/root/A-FORGE/forge_work/$(date +%Y-%m-%d)"
DEFAULT_MODEL="deepseek/deepseek-v4-pro"
DEFAULT_AGENT="forge"

# ── Parse args ──────────────────────────────────────────
MODEL="$DEFAULT_MODEL"
AGENT="$DEFAULT_AGENT"
TASK=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --model) MODEL="$2"; shift 2 ;;
        --agent) AGENT="$2"; shift 2 ;;
        *)       TASK="$1"; shift ;;
    esac
done

if [[ -z "$TASK" ]]; then
    echo "❌ Usage: opencode_agentic.sh [--model <m>] [--agent <a>] \"your task\""
    exit 1
fi

# ── Secrets ─────────────────────────────────────────────
set -a && source /root/.secrets/vault.env && set +a 2>/dev/null || true

# ── Init: Refresh continuity bridge ─────────────────────
echo "🧵 [INIT] Refreshing continuity bridge..."
if [[ -f "$MEMORY_BRIDGE" ]]; then
    python3 "$MEMORY_BRIDGE" 2>&1 || echo "⚠️  memory_bridge.py failed (non-fatal)"
fi

# ── Build injected prompt ───────────────────────────────
if [[ -f "$BRIDGE" ]]; then
    CONTEXT=$(cat "$BRIDGE" 2>/dev/null | head -50)
else
    CONTEXT="No continuity bridge available."
fi

SESSION_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
HEADLESS_PROMPT="[CONTEXT INJECTION — arifOS Federation State at $SESSION_TS]

$CONTEXT

[HEADLESS TASK — Execute autonomously under MUBAH baseline]
$TASK

[EXECUTION CONSTRAINTS]
- You are running headless (non-interactive). Do not ask questions.
- Execute the task fully. Complete all steps. Verify your work.
- At completion: emit a structured summary with (a) what was done, (b) evidence paths, (c) any blockers.
- Label all claims OBS/DER/INT/SPEC.
- ΔS ≤ 0: leave the workspace cleaner than you found it."

echo "🔥 [FORGE] Executing headless task with agent=$AGENT model=$MODEL"
echo "   Task: $TASK"

# ── Execute OpenCode headless ───────────────────────────
mkdir -p "$WORK_LOG"

cd /root && opencode run \
    --agent "$AGENT" \
    --model "$MODEL" \
    --auto \
    --format default \
    "$HEADLESS_PROMPT" 2>&1 | tee "$WORK_LOG/opencode-agentic-$(date +%H%M%S).log"

EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo "═══ EXECUTION COMPLETE (exit=$EXIT_CODE) ═══"

# ── Seal: Git commit changes ────────────────────────────
echo ""
echo "💎 [SEAL] Committing changes..."

# Collect all dirty repos
DIRTY_REPOS=""
for repo in /root/arifOS /root/A-FORGE /root/AAA /root/geox /root/WEALTH /root/WELL; do
    if [[ -d "$repo/.git" ]]; then
        pushd "$repo" > /dev/null
        if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null || [[ -n $(git ls-files --others --exclude-standard 2>/dev/null) ]]; then
            git add -A . 2>/dev/null || true
            if ! git diff --cached --quiet 2>/dev/null; then
                git commit -m "chore: auto-seal — $TASK" 2>/dev/null || true
                echo "   ✅ $repo — committed"
                DIRTY_REPOS="$DIRTY_REPOS $repo"
            fi
        fi
        popd > /dev/null
    fi
done

if [[ -z "$DIRTY_REPOS" ]]; then
    echo "   ℹ️  No dirty repos — nothing to commit"
fi

# ── Seal: Chronicle ─────────────────────────────────────
echo ""
echo "📜 [CHRONICLE] Running VAULT999 weekly synthesis..."
if [[ -f "$CHRONICLE" ]]; then
    python3 "$CHRONICLE" 2>&1 || echo "⚠️  chronicle_vault999.py failed (non-fatal)"
fi

# ── Seal: Emit receipt ──────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════"
echo "✅ AGENTIC EXECUTION SEALED"
echo "   Task:     $TASK"
echo "   Agent:    $AGENT"
echo "   Model:    $MODEL"
echo "   Exit:     $EXIT_CODE"
echo "   Commits:  ${DIRTY_REPOS:-none}"
echo "   Log:      $WORK_LOG/opencode-agentic-*.log"
echo "   Time:     $SESSION_TS"
echo "═══════════════════════════════════════════════"
