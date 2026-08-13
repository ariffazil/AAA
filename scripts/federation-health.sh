#!/usr/bin/env bash
#
# federation-health.sh — Unified federation health check
#
# Probes: arifOS :8088 · A-FORGE :7071 · arifFlow :7073
#         WEALTH :18082 · WELL :18083 · GEOX :8081
#
# Checks: organ liveness · git clean · dream timer · VVV count · apex replication
# Output: single-line GREEN/YELLOW/RED + reason summary
#
# Forged by CCC-OPENCODE · 2026-08-14
# Dependencies: bash, curl, git, systemctl, python3 (all standard on the host)
#
set -euo pipefail

# ── config ────────────────────────────────────────────────────────────────────
CURL_TIMEOUT=5

declare -A ORGANS=(
    ["arifOS:8088"]=""
    ["A-FORGE:7071"]=""
    ["arifFlow:7073"]=""
    ["WEALTH:18082"]=""
    ["WELL:18083"]=""
    ["GEOX:8081"]=""
)

declare -A REPOS=(
    ["A-FORGE"]="/root/A-FORGE"
    ["arifOS"]="/root/arifOS"
    ["arif-fazil.com"]="/root/arif-fazil.com"
)

VVV_FILE="/root/memory/VVV/void_entries.json"
VVV_EXPECTED_MIN=1          # minimum VVV entries for GREEN
DREAM_TIMER="arif-dream.timer"
DREAM_MAX_HOURS=96          # 72h cadence + 24h grace → YELLOW over this

# ── colour helpers (no tput dependency) ───────────────────────────────────────
RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# ── counters ──────────────────────────────────────────────────────────────────
FAIL_COUNT=0
WARN_COUNT=0
DETAILS=()

# ── helper: HTTP probe ────────────────────────────────────────────────────────
probe_organ() {
    local name="$1" port="$2"
    local resp
    resp=$(curl -sf --max-time "$CURL_TIMEOUT" "http://localhost:${port}/health" 2>/dev/null) || {
        ((FAIL_COUNT++))
        DETAILS+=("DOWN:${name}")
        return 1
    }
    # Check for a health status field in the JSON
    local status
    status=$(echo "$resp" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    s = d.get('status', d.get('ok', 'unknown'))
    print(s)
except:
    print('parse_error')
" 2>/dev/null)
    case "$status" in
        healthy|ok|true|HEALTHY)
            : # all good
            ;;
        degraded|DEGRADED)
            ((WARN_COUNT++))
            DETAILS+=("DEGRADED:${name}")
            ;;
        *)
            ((WARN_COUNT++))
            DETAILS+=("WARN:${name}=${status}")
            ;;
    esac
    return 0
}

# ── 1. Probe all organs ───────────────────────────────────────────────────────
for entry in "${!ORGANS[@]}"; do
    IFS=':' read -r name port <<< "$entry"
    probe_organ "$name" "$port" || true
done

# ── 2. Git clean status for 3 repos ───────────────────────────────────────────
for repo_name in "${!REPOS[@]}"; do
    repo_path="${REPOS[$repo_name]}"
    if [[ ! -d "$repo_path/.git" ]]; then
        ((FAIL_COUNT++))
        DETAILS+=("NOGIT:${repo_name}")
        continue
    fi
    if ! (cd "$repo_path" && git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null); then
        ((WARN_COUNT++))
        DETAILS+=("DIRTY:${repo_name}")
    fi
done

# ── 3. Dream engine timer cadence ─────────────────────────────────────────────
if systemctl is-active --quiet "$DREAM_TIMER" 2>/dev/null; then
    : # timer active — good
    # Check last trigger wasn't too long ago
    last_trigger=$(systemctl show "$DREAM_TIMER" -p LastTriggerUSec --value 2>/dev/null)
    if [[ "$last_trigger" == "n/a" || -z "$last_trigger" ]]; then
        ((WARN_COUNT++))
        DETAILS+=("DREAM:never_triggered")
    else
        # Convert to epoch and compute age in hours
        last_epoch=$(date -d "$last_trigger" +%s 2>/dev/null || echo 0)
        now_epoch=$(date +%s)
        age_hours=$(( (now_epoch - last_epoch) / 3600 ))
        if (( age_hours > DREAM_MAX_HOURS )); then
            ((WARN_COUNT++))
            DETAILS+=("DREAM:stale_${age_hours}h")
        fi
    fi
else
    ((WARN_COUNT++))
    DETAILS+=("DREAM:timer_inactive")
fi

# ── 4. VVV entry count ────────────────────────────────────────────────────────
if [[ -f "$VVV_FILE" ]]; then
    vvv_count=$(python3 -c "
import json, sys
try:
    d = json.load(open('$VVV_FILE'))
    print(len(d) if isinstance(d, list) else len(d.get('entries', d)))
except:
    print(0)
" 2>/dev/null)
    if (( vvv_count < VVV_EXPECTED_MIN )); then
        ((WARN_COUNT++))
        DETAILS+=("VVV:${vvv_count}_entries")
    fi
else
    ((FAIL_COUNT++))
    DETAILS+=("VVV:file_missing")
    vvv_count=0
fi

# ── 5. Apex scalar replication ────────────────────────────────────────────────
forge_health=$(curl -sf --max-time "$CURL_TIMEOUT" "http://localhost:7071/health" 2>/dev/null || echo "")
if [[ -n "$forge_health" ]]; then
    # Check that apex_scalars contain REPLICATED status
    replicated_count=$(echo "$forge_health" | grep -o '"status":"REPLICATED"' | wc -l)
    if (( replicated_count >= 5 )); then
        : # all 5 scalars replicated — GREEN
    elif (( replicated_count > 0 )); then
        ((WARN_COUNT++))
        DETAILS+=("APEX:${replicated_count}/5_replicated")
    else
        ((FAIL_COUNT++))
        DETAILS+=("APEX:no_replication")
    fi
else
    ((FAIL_COUNT++))
    DETAILS+=("APEX:forge_unreachable")
fi

# ── 6. Single-line summary ────────────────────────────────────────────────────
detail_str=$(IFS=','; echo "${DETAILS[*]}")
[[ -z "$detail_str" ]] && detail_str="all_checks_passed"

if (( FAIL_COUNT > 0 )); then
    VERDICT="RED"
    COLOR="$RED"
elif (( WARN_COUNT > 0 )); then
    VERDICT="YELLOW"
    COLOR="$YELLOW"
else
    VERDICT="GREEN"
    COLOR="$GREEN"
fi

# Print summary line (colourised for TTY, plain for pipes)
if [[ -t 1 ]]; then
    printf "${COLOR}%-6s${NC} | organs:6 | vvv:%d | apex_replicated:%d/5 | %s\n" \
        "$VERDICT" "$vvv_count" "$replicated_count" "$detail_str"
else
    printf "%-6s | organs:6 | vvv:%d | apex_replicated:%d/5 | %s\n" \
        "$VERDICT" "$vvv_count" "${replicated_count:-0}" "$detail_str"
fi

# Exit code reflects severity
case "$VERDICT" in
    GREEN)  exit 0 ;;
    YELLOW) exit 1 ;;
    RED)    exit 2 ;;
esac
