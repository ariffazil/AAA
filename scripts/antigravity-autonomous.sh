#!/usr/bin/env bash
# antigravity-autonomous.sh — Self-directed autonomy loop for Google Antigravity CLI
# Invoked by: cron, systemd timer, or trigger file watcher
# Output: delivered to Telegram via hermes-cli or stdout capture

set -euo pipefail

# ── ENVIRONMENT ──────────────────────────────────────────────
export HOME=/root
export GEMINI_CLI_TRUST_WORKSPACE=true
export GEMINI_CLI_OUTPUT_FORMAT=text

# Source secrets
set -a
source /root/.secrets/vault.env 2>/dev/null || true
source /root/.secrets/kunci-mas.env 2>/dev/null || true
set +a

# ── PATHS ────────────────────────────────────────────────────
CARRY_FORWARD="/root/.gemini/antigravity-cli/carry_forward.json"
TRIGGER_FILE="/tmp/antigravity-trigger.txt"
LOG_DIR="/root/.gemini/antigravity-cli/log"
SESSION_LOG="${LOG_DIR}/autonomous-$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$LOG_DIR"

# ── TELEGRAM DELIVERY ────────────────────────────────────────
deliver() {
    local msg="$1"
    # Use our existing telegram delivery via hermes-cli if available
    if command -v hermes-cli &>/dev/null; then
        echo "$msg" | hermes-cli message send --chat "267378578" 2>/dev/null || true
    fi
}

# ── CARRY-FORWARD ────────────────────────────────────────────
read_carry() {
    if [[ -f "$CARRY_FORWARD" ]]; then
        cat "$CARRY_FORWARD"
    else
        echo '{"last_run": null, "last_task": "none", "completed": [], "open_issues": [], "session_count": 0}'
    fi
}

write_carry() {
    local task="$1"
    local result="$2"
    local cf
    cf=$(read_carry)
    local count
    count=$(echo "$cf" | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_count',0)+1)")
    python3 -c "
import sys, json
cf = json.loads('''$cf''')
cf['last_run'] = '$(date -Iseconds)'
cf['last_task'] = '''$task'''
cf['session_count'] = $count
# Truncate completed list to last 20
cf['completed'] = (cf.get('completed',[]) + ['''$result'''])[-20:]
json.dump(cf, sys.stdout, indent=2)
" > "$CARRY_FORWARD"
}

# ── TRIGGER CHECK ────────────────────────────────────────────
check_trigger() {
    if [[ -f "$TRIGGER_FILE" ]]; then
        local prompt
        prompt=$(cat "$TRIGGER_FILE")
        rm -f "$TRIGGER_FILE"
        echo "$prompt"
        return 0
    fi
    return 1
}

# ── MAIN ─────────────────────────────────────────────────────
main() {
    local prompt=""
    local triggered=false
    
    # Priority 1: Explicit trigger file (Arif or another agent wrote one)
    if prompt=$(check_trigger); then
        triggered=true
        echo "[antigravity] Trigger file detected" | tee -a "$SESSION_LOG"
    fi
    
    # Priority 2: Passed as argument
    if [[ -z "$prompt" ]] && [[ $# -gt 0 ]]; then
        prompt="$*"
    fi
    
    # Priority 3: Self-directed sweep (default mode)
    if [[ -z "$prompt" ]]; then
        local cf
        cf=$(read_carry)
        prompt="You are Antigravity CLI (Google Gemini), running autonomously on Arif's VPS at $(date -Iseconds).
Your carry-forward state from the last run:
\`\`\`json
$cf
\`\`\`

AUTONOMOUS SWEEP — do the following, in order. Use your full tool surface (shell, MCP, file read/write):
1. Check federation organ health (ports 8088, 7071, 8081, 18082, 18083, 3001)
2. Check /root git repos for uncommitted work or drift
3. Check disk space, memory, and CPU load
4. If anything is broken and you can fix it (T1/T2), FIX IT.
5. If anything requires T3 (production restart, merge, delete), NOTE IT for Arif.
6. Report: what you checked, what you found, what you fixed, what needs Arif.

Respond in BM campur English. Ringkas. Action-oriented. No fluff."
    fi
    
    echo "[antigravity] Session start: $(date)" | tee -a "$SESSION_LOG"
    echo "[antigravity] Prompt: ${prompt:0:100}..." | tee -a "$SESSION_LOG"
    
    # Execute antigravity headless
    local output
    if output=$(cd /root && timeout 300 gemini -p "$prompt" -y -o text 2>&1); then
        echo "$output" | tee -a "$SESSION_LOG"
        
        # Update carry-forward
        local summary
        summary=$(echo "$output" | tail -5 | tr '\n' ' ')
        write_carry "autonomous-sweep" "$summary"
        
        echo "[antigravity] Session complete: $(date)" | tee -a "$SESSION_LOG"
        
        # Deliver if something important happened
        if echo "$output" | grep -qi "fix\|broken\|alert\|hold\|critical\|restart\|urgent"; then
            local tldr
            tldr=$(echo "$output" | grep -i "fix\|broken\|alert\|hold\|critical\|restart\|urgent" | head -3)
            deliver "🛰️ **Antigravity Autonomous Sweep** ($triggered)
\`\`\`
$tldr
\`\`\`
Full log: \`$SESSION_LOG\`"
        fi
        
        return 0
    else
        echo "[antigravity] FAILED: $output" | tee -a "$SESSION_LOG"
        deliver "⚠️ **Antigravity sweep FAILED**
\`\`\`
$output
\`\`\`"
        return 1
    fi
}

main "$@"
