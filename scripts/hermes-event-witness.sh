#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# OpenClaw — Hermes Event Witness
# Phase 2B v2: Validates Hermes events, witnesses locally, queues for human ratification
#
# Flow:
#   1. Scan /tmp/hermes-pending-events/
#   2. Validate structure + HMAC signature
#   3. Mark as "witnessed" → /tmp/hermes-sealed-events/ (local, NOT VAULT999)
#   4. Send Telegram notification to Arif for ratification
#   5. Arif replies with /ratify <event_id> to seal to VAULT999
#
# Run frequency: every 30 minutes via cron (or manual trigger)
# Authority: OpenClaw (AGI-tier) witnesses; Arif (SOVEREIGN) ratifies
#
# DITEMPA BUKAN DIBERI
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

PENDING_DIR="/tmp/hermes-pending-events"
SEALED_DIR="/tmp/hermes-sealed-events"
REJECTED_DIR="/tmp/hermes-rejected-events"
RATIFY_QUEUE="/tmp/hermes-ratify-queue.jsonl"
SECRET_FILE="/root/.arifos/shared-secrets/hermes-openclaw-bridge.key"
LOG_FILE="/var/log/hermes-event-witness.log"

HERMES_BOT_TOKEN="8410138119:AAHrXysyxI8yuBM7QW6QTafKsgpqEyd19DA"
AAA_GROUP_ID="-1003753855708"
OPENCLAW_BOT_TOKEN="8149595687:AAGycp7nzl1-D8mzZKOkUJWiWxg3Ok-wy70"

ARIFOS_MCP_URL="http://127.0.0.1:8080/mcp"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log() {
    local msg="[$(date -Iseconds)] $1"
    echo -e "$msg" | tee -a "$LOG_FILE" 2>/dev/null || echo "$msg"
}

# ── Load shared secret ──
load_secret() {
    if [ ! -f "$SECRET_FILE" ]; then
        log "${RED}FATAL: Shared secret not found at $SECRET_FILE${NC}"
        exit 1
    fi
    SHARED_SECRET=$(cat "$SECRET_FILE" | tr -d '\n')
}

# ── Validate JSON structure ──
validate_event() {
    python3 -c "
import sys, json

def validate(event):
    required_top = ['event_id', 'timestamp', 'actor', 'session_id', 'type', 'payload', 'hermes_signature']
    for key in required_top:
        if key not in event:
            return False, f'Missing required field: {key}'
    if event['actor'] != 'Hermes ASI':
        return False, f'Invalid actor: {event[\"actor\"]}'
    if event['type'] not in ['observation', 'preference_update', 'project_state_change']:
        return False, f'Invalid type: {event[\"type\"]}'
    payload = event.get('payload', {})
    if 'description' not in payload:
        return False, 'Missing payload.description'
    return True, 'Valid'

try:
    with open('$1', 'r') as f:
        event = json.load(f)
    ok, msg = validate(event)
    print(f'{int(ok)}|{msg}')
except Exception as e:
    print(f'0|JSON parse error: {e}')
"
}

# ── Verify HMAC signature ──
verify_hmac() {
    python3 -c "
import json, hmac, hashlib

with open('$1', 'r') as f:
    event = json.load(f)

claimed_sig = event.pop('hermes_signature', '')
payload_bytes = json.dumps(event, sort_keys=True, ensure_ascii=False).encode('utf-8')

with open('$SECRET_FILE', 'r') as sf:
    secret = sf.read().strip().encode('utf-8')

computed = hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()
print('1' if hmac.compare_digest(computed, claimed_sig) else '0')
"
}

# ── Notify Arif via Telegram (Hermes bot — uses ASI_arifos_bot) ──
notify_arif() {
    local event_id="$1"
    local description="$2"
    local event_type="$3"
    local session_id="$4"

    local msg="🏛️ <b>VAULT999 Ratification Required</b>

📋 <b>Event:</b> ${event_id}
📁 <b>Type:</b> ${event_type}
📝 <b>Description:</b> ${description}
🔗 <b>Session:</b> ${session_id}

⚠️ <b>VAULT999 is immutable.</b> Reply with:
✅ <code>/ratify ${event_id}</code> — to SEAL
❌ <code>/reject ${event_id}</code> — to VOID"

    curl -s -X POST "https://api.telegram.org/bot${HERMES_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${AAA_GROUP_ID}" \
        -d "text=${msg}" \
        -d "parse_mode=HTML" \
        -d "reply_to_message_id=" > /dev/null 2>&1
    log "  📱 Telegram notification sent to AAA group"
}

# ── Add to ratification queue ──
queue_for_ratification() {
    local event_file="$1"
    local witnessed_payload="$2"
    local event_id=$(echo "$witnessed_payload" | python3 -c "import sys,json; print(json.load(sys.stdin)['event_id'])")

    # Append to ratification queue
    echo "$witnessed_payload" >> "$RATIFY_QUEUE"
    log "  📋 Queued for ratification: $event_id"
}

# ── Send Hermes confirmation via OpenClaw bot ──
notify_hermes_ok() {
    local event_id="$1"
    local msg="✅ Hermes event witnessed and queued for ratification.

🔗 Event: ${event_id}
⏳ Awaiting Arif's /ratify to seal to VAULT999."

    curl -s -X POST "https://api.telegram.org/bot${OPENCLAW_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${AAA_GROUP_ID}" \
        -d "text=${msg}" \
        -d "parse_mode=HTML" > /dev/null 2>&1
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

log "${YELLOW}═══ Hermes Event Witness v2 started ═══${NC}"

# Ensure dirs exist
mkdir -p "$SEALED_DIR" "$REJECTED_DIR"
touch "$RATIFY_QUEUE"

load_secret

pending_count=$(find "$PENDING_DIR" -maxdepth 1 -type f \( -name '*.json' -o -name '*.jsonl' \) | wc -l)
log "Pending events found: $pending_count"

if [ "$pending_count" -eq 0 ]; then
    log "${GREEN}No pending events. Exiting.${NC}"
    exit 0
fi

processed=0
witnessed=0
rejected=0

for event_file in "$PENDING_DIR"/*.json "$PENDING_DIR"/*.jsonl; do
    [ -f "$event_file" ] || continue

    basename_file=$(basename "$event_file")
    log "── Processing: $basename_file ──"

    # 1. Validate structure
    validation=$(validate_event "$event_file")
    valid=$(echo "$validation" | cut -d'|' -f1)
    valid_msg=$(echo "$validation" | cut -d'|' -f2-)

    if [ "$valid" != "1" ]; then
        log "${RED}REJECT (validation): $valid_msg${NC}"
        mv "$event_file" "$REJECTED_DIR/$basename_file" 2>/dev/null || true
        rejected=$((rejected + 1))
        continue
    fi
    log "  ✅ Structure valid"

    # 2. Verify HMAC signature
    hmac_ok=$(verify_hmac "$event_file")
    if [ "$hmac_ok" != "1" ]; then
        log "${RED}REJECT (HMAC): Signature mismatch${NC}"
        mv "$event_file" "$REJECTED_DIR/$basename_file" 2>/dev/null || true
        rejected=$((rejected + 1))
        continue
    fi
    log "  ✅ HMAC valid"

    # 3. Build witnessed payload
    witnessed_payload=$(python3 -c "
import json, datetime
with open('$event_file', 'r') as f:
    event = json.load(f)
event['status'] = 'witnessed'
event['witnessed_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
event['witnessed_by'] = 'OpenClaw'
print(json.dumps(event, ensure_ascii=False))
")
    event_id=$(echo "$witnessed_payload" | python3 -c "import sys,json; print(json.load(sys.stdin)['event_id'])")
    event_type=$(echo "$witnessed_payload" | python3 -c "import sys,json; print(json.load(sys.stdin)['type'])")
    description=$(echo "$witnessed_payload" | python3 -c "import sys,json; print(json.load(sys.stdin)['payload']['description'])")
    session_id=$(echo "$witnessed_payload" | python3 -c "import sys,json; print(json.load(sys.stdin)['session_id'])")

    # 4. Store as witnessed (local, NOT VAULT999)
    echo "$witnessed_payload" > "$SEALED_DIR/$basename_file"
    log "  ✅ Witnessed locally: $SEALED_DIR/$basename_file"

    # 5. Queue for ratification
    queue_for_ratification "$event_file" "$witnessed_payload"

    # 6. Notify Arif via Hermes bot (AAA group)
    notify_arif "$event_id" "$description" "$event_type" "$session_id"

    # 7. Confirm to Hermes via OpenClaw bot
    notify_hermes_ok "$event_id"

    # 8. Remove from pending
    rm -f "$event_file"

    witnessed=$((witnessed + 1))
    processed=$((processed + 1))
done

log "${GREEN}═══ Witness v2 complete: $processed processed, $witnessed witnessed, $rejected rejected ═══${NC}"
log "   Ratification queue: $RATIFY_QUEUE ($(wc -l < "$RATIFY_QUEUE") entries)"