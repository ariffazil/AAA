#!/usr/bin/env bash
# event-bridge.sh — delta-gated event delivery for scheduled jobs.
#
# Posts ONLY when the evaluated content changes. Silent when unchanged, so a job that
# reports the same state daily costs zero messages.
#
# Usage: event-bridge.sh <source_name> <content_file> [P0|P1|P2]
#
# Wire as a SEPARATE cron entry one minute AFTER the job that produces the content,
# so the producer and the bridge never race:
#   0 2 * * *  /path/job.sh          >> /var/log/job.log 2>&1
#   1 2 * * *  /path/event-bridge.sh my_job /var/log/job.log P2
#
# State: <STATE_DIR>/<source>.last_hash   last successfully delivered content hash
#        <STATE_DIR>/events.jsonl         append-only event record (the real trace)
#
# F1 AMANAH: reads the source only; writes only its own state dir.
# F2 TRUTH:  every post carries the content hash it was derived from.

set -euo pipefail

SOURCE="${1:?usage: event-bridge.sh <source> <content_file> [P0|P1|P2]}"
CONTENT_FILE="${2:?usage: event-bridge.sh <source> <content_file> [P0|P1|P2]}"
SEVERITY="${3:-P2}"

# ---- site config: point these at your own notifier and state dir -----------------
NOTIFY="${EVENT_BRIDGE_NOTIFY:-/usr/local/bin/notify.sh}"
STATE_DIR="${EVENT_BRIDGE_STATE:-/var/lib/event-bridge}"
# ---------------------------------------------------------------------------------

HOST_ID="$(hostname -f 2>/dev/null || hostname)"
mkdir -p "$STATE_DIR"

[ -f "$CONTENT_FILE" ] || { echo "[event-bridge] no content file: $CONTENT_FILE"; exit 0; }
CONTENT="$(cat "$CONTENT_FILE")"
[ -n "$CONTENT" ]      || { echo "[event-bridge] empty content — nothing to evaluate"; exit 0; }

HASH="$(printf '%s' "$CONTENT" | sha256sum | cut -c1-16)"
LAST_FILE="$STATE_DIR/${SOURCE}.last_hash"

# ---- delta gate: unchanged since last successful delivery => stay silent ---------
if [ -f "$LAST_FILE" ] && [ "$(cat "$LAST_FILE")" = "$HASH" ]; then
  echo "[event-bridge] ${SOURCE}: no delta (${HASH:0:8}) — silent"
  exit 0
fi

# ---- classify by consequence of the CONTENT, not by the source job --------------
TYPE="STATE_CHANGED"
if   printf '%s' "$CONTENT" | grep -qiE 'DOWN|FAIL|CRITICAL|breach|unauthor|rogue|lost'; then
  TYPE="DETECTED"; SEVERITY="P0"
elif printf '%s' "$CONTENT" | grep -qiE 'REPAIRED|RESTORED|RESOLVED|SEALED|HEALTH'; then
  TYPE="VERIFIED"
fi

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
EVENT_ID="evt_$(date -u +%Y%m%dT%H%M%S)_${HASH:0:8}"

MSG="$(printf 'FORGE | %s | %s\nevent: %s\nscope: node\nhost: %s\nsource: %s\ndedupe: %s\ntime: %s\n\n%s' \
  "$SEVERITY" "$TYPE" "$EVENT_ID" "$HOST_ID" "$SOURCE" "$HASH" "$TS" "$CONTENT")"

# ---- append-only record FIRST: the channel is a projection, not the source -------
printf '{"ts":"%s","event_id":"%s","source":"%s","severity":"%s","type":"%s","hash":"%s","host":"%s"}\n' \
  "$TS" "$EVENT_ID" "$SOURCE" "$SEVERITY" "$TYPE" "$HASH" "$HOST_ID" \
  >> "$STATE_DIR/events.jsonl"

# ---- deliver, then record the hash ONLY on success so failure retries next tick --
if "$NOTIFY" "$MSG" >/dev/null 2>&1; then
  printf '%s' "$HASH" > "$LAST_FILE"
  echo "[event-bridge] ${SOURCE}: posted ${TYPE}/${SEVERITY} (${HASH:0:8})"
else
  echo "[event-bridge] ${SOURCE}: DELIVERY FAILED — hash not recorded, will retry"
  exit 1
fi
