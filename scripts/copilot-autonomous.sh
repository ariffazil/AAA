#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
# copilot-autonomous.sh — Self-directed GitHub & Copilot CLI Autonomy Sweep
# ══════════════════════════════════════════════════════════════════════════════
# Invoked by: cron or manual triggering
# Uses: gh, gh copilot, git
# Output: delivered to Telegram via hermes-cli
# ══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ── ENVIRONMENT ──────────────────────────────────────────────
export HOME=/root
export GH_PAGER=cat

# Source secrets
set -a
source /root/.secrets/kunci-mas.env 2>/dev/null || true
if [ -n "${GITHUB_PERSONAL_ACCESS_TOKEN:-}" ] && [ -z "${GITHUB_TOKEN:-}" ]; then
    export GITHUB_TOKEN="$GITHUB_PERSONAL_ACCESS_TOKEN"
fi
set +a

# ── PATHS ────────────────────────────────────────────────────
CARRY_FORWARD="/root/.gemini/antigravity-cli/carry_forward.json"
LOG_DIR="/root/.gemini/antigravity-cli/log"
SESSION_LOG="${LOG_DIR}/copilot-autonomous-$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$LOG_DIR"

# ── TELEGRAM DELIVERY ────────────────────────────────────────
deliver() {
    local msg="$1"
    if command -v hermes-cli &>/dev/null; then
        echo "$msg" | hermes-cli message send --chat "267378578" 2>/dev/null || true
    fi
}

# ── CHECK AUTH ───────────────────────────────────────────────
check_auth() {
    if ! gh auth status &>/dev/null; then
        echo "⚠️ GitHub CLI is currently unauthenticated or the token has expired."
        echo "To re-authenticate, please run: gh auth login"
        return 1
    fi
    return 0
}

# ── MAIN ─────────────────────────────────────────────────────
main() {
    echo "[copilot-autonomous] Start: $(date)" | tee -a "$SESSION_LOG"

    # Check authentication
    if ! check_auth | tee -a "$SESSION_LOG"; then
        deliver "🛰️ **GitHub Copilot CLI Sweep paused**
⚠️ GitHub CLI authentication is invalid/expired.
Please run \`gh auth login\` or update GITHUB_TOKEN in kunci-mas.env to resume."
        return 1
    fi

    # 1. Check for notifications, pull requests, issues
    echo "[copilot-autonomous] Checking GitHub status..." | tee -a "$SESSION_LOG"
    
    local notifications
    notifications=$(gh api notifications --jq '.[] | "- \(.repository.full_name): \(.subject.title) (\(.subject.type))"' 2>/dev/null || echo "No notifications or api limit")

    local open_prs
    open_prs=$(gh pr list --state open --limit 5 --json number,title,repository,url --jq '.[] | "- #\(.number) \(.title) (\(.repository.name)) [Link](\(.url))"' 2>/dev/null || echo "No open PRs found")

    local open_issues
    open_issues=$(gh issue list --assignee "@me" --state open --limit 5 --json number,title,url --jq '.[] | "- #\(.number) \(.title) [Link](\(.url))"' 2>/dev/null || echo "No assigned open issues")

    # 2. Check for local git status of main repos
    local repo_status=""
    for dir in arifOS A-FORGE AAA GEOX WEALTH WELL; do
        if [ -d "/root/$dir" ]; then
            local dirty
            dirty=$(git -C "/root/$dir" status --porcelain 2>/dev/null | wc -l || echo "0")
            if [ "$dirty" -gt 0 ]; then
                repo_status="${repo_status}- **$dir**: $dirty uncommitted file(s)\n"
            fi
        fi
    done
    [ -z "$repo_status" ] && repo_status="All repos clean.\n"

    # 3. Call Copilot CLI to suggest cleanup/next steps if anything dirty or pending
    local suggestion="No tasks requiring Copilot advice."
    if [ -n "$open_prs" ] || [ -n "$open_issues" ]; then
        local query="I have these open PRs:
$open_prs
And these open issues:
$open_issues
What is the recommended next command to check on them?"
        
        echo "[copilot-autonomous] Requesting Copilot suggestion..." | tee -a "$SESSION_LOG"
        suggestion=$(gh copilot suggest -t shell "$query" 2>/dev/null || echo "Copilot suggestion call failed — check Copilot subscription status")
    fi

    # 4. Construct TL;DR Report
    local report="🛰️ **GitHub Copilot CLI Autonomous Sweep**
Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)

**Git Repos:**
$(printf "%b" "$repo_status")
**Open PRs:**
${open_prs:-None}

**Open Assigned Issues:**
${open_issues:-None}

**Copilot Command Suggestion:**
\`\`\`
$suggestion
\`\`\`"

    echo "$report" | tee -a "$SESSION_LOG"
    deliver "$report"

    echo "[copilot-autonomous] Complete: $(date)" | tee -a "$SESSION_LOG"
    return 0
}

main "$@"
