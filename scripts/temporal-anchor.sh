#!/bin/bash
# Temporal Anchor — arifOS boot module
# Reads real wall-clock time, resolves to user locale (MYT), stamps state.
# Must be called at session start before first reply.

STATE_FILE="${OPENCLAW_WORKSPACE:-/root/.openclaw}/temporal-state.json"
WORKSPACE="${OPENCLAW_WORKSPACE:-/root/.openclaw}"

# Read real UTC time
UTC_NOW=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
UTC_DATE=$(date -u '+%Y-%m-%d')
UTC_HOUR=$(date -u '+%H')

# Resolve to MYT (Arif's locale)
LOCAL_NOW=$(TZ='Asia/Kuala_Lumpur' date '+%Y-%m-%dT%H:%M:%S %Z')
LOCAL_DATE=$(TZ='Asia/Kuala_Lumpur' date '+%Y-%m-%d')
LOCAL_HOUR=$(TZ='Asia/Kuala_Lumpur' date '+%H')
LOCAL_WDAY=$(TZ='Asia/Kuala_Lumpur' date '+%A')

# Part of day — numeric comparison on zero-padded LOCAL_HOUR (e.g. "08")
LOCAL_HOUR_NUM=$((10#$LOCAL_HOUR))
if [[ $LOCAL_HOUR_NUM -ge 5 && $LOCAL_HOUR_NUM -lt 12 ]]; then
  PART_OF_DAY="morning"
elif [[ $LOCAL_HOUR_NUM -ge 12 && $LOCAL_HOUR_NUM -lt 18 ]]; then
  PART_OF_DAY="afternoon"
elif [[ $LOCAL_HOUR_NUM -ge 18 && $LOCAL_HOUR_NUM -lt 22 ]]; then
  PART_OF_DAY="evening"
else
  PART_OF_DAY="night"
fi

# Epoch label — use MYT date to stay consistent with local_now
EPOCH_LABEL="EPOCH-${LOCAL_DATE}"

# Write state
cat > "$STATE_FILE" << EOF
{
  "temporal_state": {
    "utc_now": "$UTC_NOW",
    "local_now": "$LOCAL_NOW",
    "timezone": "Asia/Kuala_Lumpur",
    "offset": "+08:00",
    "part_of_day": "$PART_OF_DAY",
    "weekday": "$LOCAL_WDAY",
    "epoch_label": "$EPOCH_LABEL",
    "anchor_source": "system_clock",
    "anchor_age_sec": 0,
    "status": "ANCHORED_FRESH"
  }
}
EOF

echo "Temporal anchor loaded: $PART_OF_DAY | $LOCAL_NOW | epoch $EPOCH_LABEL"
