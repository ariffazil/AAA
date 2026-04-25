#!/bin/bash
# temporal-anchor.sh — arifOS temporal grounding
# Run on every session start to anchor time context

set -euo pipefail

STATE_FILE="/root/.openclaw/temporal-state.json"
UTC_NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LOCAL_NOW=$(TZ=Asia/Kuala_Lumpur date +"%Y-%m-%dT%H:%M:%S%z")
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

cat > "$STATE_FILE" << EOF
{
  "status": "$STATUS",
  "utc_now": "$UTC_NOW",
  "local_now": "$LOCAL_NOW",
  "part_of_day": "$PART_OF_DAY",
  "weekday": "$WEEKDAY",
  "epoch_label": "$EPOCH_LABEL",
  "anchor_age_sec": $ANCHOR_AGE_SEC,
  "timezone": "Asia/Kuala_Lumpur"
}
EOF

echo "Temporal anchor refreshed: $STATUS @ $UTC_NOW"
cat "$STATE_FILE"
