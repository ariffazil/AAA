#!/usr/bin/env bash
# ==============================================================================
# generate-session-briefing.sh — arifOS Multi-Agent Handoff & Session Aggregator
# Canon: /root/AAA/governance/ARCHITECTURAL_DOCTRINE_OBSERVABILITY.md
# First Law: LIVE PROBE OR UNKNOWN. Never Pretend.
# ==============================================================================

set -uo pipefail

HOURS="${1:-24}"
SINCE="${HOURS} hours ago"

# Formatting Colors
C="\033[36m"
G="\033[32m"
Y="\033[33m"
R="\033[31m"
W="\033[1;37m"
D="\033[90m"
B="\033[1m"
X="\033[0m"

NOW_MYT=$(TZ="Asia/Kuala_Lumpur" date "+%Y-%m-%d %H:%M:%S MYT")
NOW_UTC=$(date -u "+%Y-%m-%dT%H:%M:%SZ")

printf "\n${C}═══════════════════════════════════════════════════════════════════════${X}\n"
printf "  ${B}${W}arifOS SESSION BRIEFING & HANDOFF ENGINE${X}  ${D}(Window: ${HOURS}h)${X}\n"
printf "  ${D}MYT: ${NOW_MYT}  ·  UTC: ${NOW_UTC}${X}\n"
printf "${C}═══════════════════════════════════════════════════════════════════════${X}\n\n"

# ── 1. CONTINUITY & CARRY-FORWARD STATE ──────────────────────────────
printf "  ${W}📌 STATE CONTINUITY (CARRY FORWARD)${X}\n"
CF_FILE="/root/.local/share/arifos/carry_forward.json"
if [ -f "$CF_FILE" ]; then
  python3 -c "
import json
try:
    with open('$CF_FILE') as f:
        d = json.load(f)
    print(f\"  ${D}Last Updated:${X}  {d.get('last_updated', 'UNKNOWN')}\")
    print(f\"  ${D}Summary:${X}       {d.get('session_summary', 'None recorded')}\")
    if 'current_focus' in d:
        print(f\"  ${D}Focus:${X}         {d.get('current_focus')}\")
    if 'active_task' in d:
        print(f\"  ${D}Active Task:${X}   {d.get('active_task')}\")
except Exception as e:
    print(f\"  ${R}Error reading carry_forward.json: {e}${X}\")
"
else
  printf "  ${Y}carry_forward.json: UNKNOWN [NO_FILE]${X}\n"
fi

# ── 2. SEALS & GOVERNANCE HOLDS ──────────────────────────────────────
printf "\n  ${W}⚖️ SEALS & ACTIVE HOLDS${X}\n"

# Count holds
HOLDS_FOUND=0
for h in $(find /root/ -maxdepth 3 -name "*.hold" -o -name "*_HOLD.json" 2>/dev/null); do
  HOLDS_FOUND=$((HOLDS_FOUND + 1))
done

if [ "$HOLDS_FOUND" -eq 0 ]; then
  printf "  ${D}Active Holds:${X}  ${G}0 Pending Holds (Clean)${X}\n"
else
  printf "  ${D}Active Holds:${X}  ${R}⚠️ ${HOLDS_FOUND} PENDING HOLD(S)${X}\n"
fi

# Recent Seals in VAULT999
SEAL_LOG="/root/VAULT999/SEALED_EVENTS.jsonl"
if [ -f "$SEAL_LOG" ]; then
  SEAL_COUNT=$(wc -l < "$SEAL_LOG" 2>/dev/null || echo 0)
  printf "  ${D}VAULT999 Total Sealed Events:${X} ${G}${SEAL_COUNT}${X}\n"
  printf "  ${D}Latest 3 Sealed Events:${X}\n"
  tail -n 3 "$SEAL_LOG" 2>/dev/null | python3 -c "
import sys, json
for line in sys.stdin:
    if not line.strip(): continue
    try:
        data = json.loads(line)
        sid = data.get('session_id') or data.get('id') or 'SEAL'
        action = data.get('action') or data.get('type') or data.get('event') or 'EVENT'
        ts = data.get('timestamp') or data.get('ts') or ''
        print(f\"    • [{ts}] {sid} - {action}\")
    except:
        print(f\"    • {line.strip()[:90]}\")
"
else
  printf "  ${D}VAULT999 Sealed Events:${X} ${Y}UNKNOWN [NO_FILE]${X}\n"
fi

# ── 3. GIT DELTA ACROSS 7 REPOSITORIES ───────────────────────────────
printf "\n  ${W}📦 GIT DELTA (COMMITS IN LAST ${HOURS}h)${X}\n"
REPOS=(
  "arifOS:/root/arifOS"
  "AAA:/root/AAA"
  "GEOX:/root/GEOX"
  "WEALTH:/root/WEALTH"
  "WELL:/root/WELL"
  "A-FORGE:/root/A-FORGE"
  "arif-fazil.com:/root/arif-fazil.com"
)

TOTAL_COMMITS=0

for item in "${REPOS[@]}"; do
  RNAME="${item%%:*}"
  RPATH="${item##*:}"

  if [ -d "$RPATH/.git" ]; then
    COMMITS=$(git -C "$RPATH" log --since="$SINCE" --oneline 2>/dev/null || true)
    COUNT=$(echo -n "$COMMITS" | grep -c '^' || echo 0)
    TOTAL_COMMITS=$((TOTAL_COMMITS + COUNT))

    DIRTY=$(git -C "$RPATH" status --porcelain 2>/dev/null | wc -l)
    DIRTY_STR=""
    if [ "$DIRTY" -gt 0 ]; then
      DIRTY_STR="${Y}[${DIRTY} uncommitted]${X}"
    else
      DIRTY_STR="${G}[clean]${X}"
    fi

    printf "  ${B}%-15s${X} ${G}%2d commits${X}  %b\n" "$RNAME" "$COUNT" "$DIRTY_STR"
    if [ "$COUNT" -gt 0 ]; then
      echo "$COMMITS" | head -n 3 | while read -r line; do
        printf "    ${D}↳ ${line}${X}\n"
      done
    fi
  else
    printf "  ${B}%-15s${X} ${D}[not a git repo]${X}\n" "$RNAME"
  fi
done

printf "  ${D}Total Commits in Window:${X} ${W}${TOTAL_COMMITS}${X}\n"

# ── 4. RSI RECURSIVE METRIC ──────────────────────────────────────────
printf "\n  ${W}♻️ RSI & MEMORY METRIC${X}\n"
RSI_FILE="/root/VAULT999/rsi_ledger.jsonl"
if [ -f "$RSI_FILE" ]; then
  LAST_RSI=$(tail -n 1 "$RSI_FILE" 2>/dev/null)
  if [ -n "$LAST_RSI" ]; then
    python3 -c "
import json
try:
    d = json.loads('''$LAST_RSI''')
    print(f\"  ${D}Latest RSI Entry:${X} {d.get('timestamp', 'UNKNOWN')} · Delta: {d.get('entropy_delta', '0')}\")
except:
    print(f\"  ${D}Latest RSI Entry:${X} Active (raw stream)\")
"
  fi
fi

printf "\n${C}───────────────────────────────────────────────────────────────────────${X}\n"
printf "  ${D}Single Source of Truth: /root/AAA/governance/ARCHITECTURAL_DOCTRINE_OBSERVABILITY.md${X}\n\n"
