#!/bin/bash
# temporal-anchor.sh — arifOS temporal grounding
# Run on every session start to anchor time context.
#
# CANONICAL: writes to /root/.local/share/arifos/state.json (AAA sovereign state).
# Source of truth for timezone: state.json.iana_tz (read by temporal_context.py).
# Legacy mirror to /root/.openclaw/temporal-state.json (will be removed 2026-08-18).

set -euo pipefail

# Resolve canonical AAA state file (path-of-truth for all AAA agents)
STATE_FILE_MAIN="/root/.local/share/arifos/state.json"
STATE_FILE_LEGACY="/root/.openclaw/temporal-state.json"

# Read iana_tz from state.json if available; default MYT.
CANON_TZ=$(python3 -c "
import json, sys
try:
    d = json.load(open('$STATE_FILE_MAIN'))
    print(d.get('iana_tz') or 'Asia/Kuala_Lumpur')
except Exception:
    print('Asia/Kuala_Lumpur')
" 2>/dev/null)

UTC_NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LOCAL_NOW=$(TZ="$CANON_TZ" date +"%Y-%m-%dT%H:%M:%S%z")
PART_OF_DAY=$(date -u +"%H:%M" | awk -F: '
    $1 >= 5 && $1 < 12  { print "morning" }
    $1 >= 12 && $1 < 17 { print "afternoon" }
    $1 >= 17 && $1 < 21 { print "evening" }
    $1 >= 21 || $1 < 5  { print "night" }
')
WEEKDAY=$(date -u +"%A")
EPOCH_LABEL=$(date -u +"%Y.%m.%d")
ANCHOR_AGE_SEC=0
STATUS="ANCHORED_FRESH"

# Write canonical state file (single source of truth for sovereign timezone)
mkdir -p "$(dirname "$STATE_FILE_MAIN")" 2>/dev/null || true
cat > "$STATE_FILE_MAIN" << EOF
{
  "timezone": "$CANON_TZ",
  "iana_tz": "$CANON_TZ",
  "utc_offset_hours": 8,
  "tz_alias": "MYT",
  "set_by": "arif (F13)",
  "set_at_utc": "$UTC_NOW",
  "set_at_myt": "$LOCAL_NOW",
  "env_var": "HERMES_TIMEZONE",
  "rationale": "Arif di Malaysia. All timestamps MYT, convert UTC → MYT before display.",
  "note": "Canonical AAA state. Read by /root/HERMES/scripts/zen/temporal_context.py. Do not duplicate elsewhere."
}
EOF

# Mirror to legacy path for backward compat (will be removed 2026-08-18)
mkdir -p "$(dirname "$STATE_FILE_LEGACY")" 2>/dev/null || true
cat > "$STATE_FILE_LEGACY" << EOF
{
  "status": "$STATUS",
  "utc_now": "$UTC_NOW",
  "local_now": "$LOCAL_NOW",
  "part_of_day": "$PART_OF_DAY",
  "weekday": "$WEEKDAY",
  "epoch_label": "$EPOCH_LABEL",
  "anchor_age_sec": $ANCHOR_AGE_SEC,
  "timezone": "$CANON_TZ",
  "deprecated": true,
  "canonical": "$STATE_FILE_MAIN"
}
EOF

echo "Temporal anchor refreshed: $STATUS @ $UTC_NOW (canonical: $STATE_FILE_MAIN)"
cat "$STATE_FILE_MAIN"
