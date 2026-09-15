#!/bin/bash
# rollback-v9.sh — i-ARIF V9 F13 REJECT rollback
# Owner: Hang (AGI) · F13 verdict: REJECT · Awaiting ARIF approval to execute
set -euo pipefail

BACKUP="/tmp/config-bak-1787643897.yaml"
CONFIG="$HOME/.hermes/config.yaml"
PIPELINE="/root/AAA/engines/iarif_tts_pipeline.sh"
DEFAULT_VOICE_ID="i-ARIF-20260819T084602"
REVOKED_VOICE_ID="ttv-voice-2026082515384726-njTJ5yOR"
MANIFEST="/root/AAA/audio/i-arif-v9-manifest.json"
TUKKI_FILTER="/root/.openclaw/workspace/media/arif-voice-archive/tukki-iarif-sopan-v9-preset.ogg"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "i-ARIF V9 ROLLBACK — F13 REJECT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Restore config from backup
if [ -f "$BACKUP" ]; then
    cp -p "$BACKUP" "$CONFIG"
    echo "[✓] Restored $CONFIG from $BACKUP"
else
    echo "[✗] BACKUP MISSING: $BACKUP — ABORT"
    exit 1
fi

# 2. Restore default VOICE_ID in pipeline
if [ -f "$PIPELINE" ]; then
    sed -i.bak "s/VOICE_ID=\"\${IARIF_VOICE_ID:-ttv-voice-2026082515384726-njTJ5yOR}\"/VOICE_ID=\"\${IARIF_VOICE_ID:-$DEFAULT_VOICE_ID}\"/" "$PIPELINE"
    echo "[✓] Restored VOICE_ID=$DEFAULT_VOICE_ID in $PIPELINE"
fi

# 3. Mark manifest as REJECTED
if [ -f "$MANIFEST" ]; then
    python3 -c "
import json, sys
p = '$MANIFEST'
with open(p) as f:
    m = json.load(f)
m['vault_seal'] = 'F13_REJECTED'
m['rejected_at'] = '2026-08-25T07:49:00Z'
m['rejection_reason'] = 'Ear-test fail — rasa tidak hits'
m['revoked_voice_id'] = '$REVOKED_VOICE_ID'
with open(p, 'w') as f:
    json.dump(m, f, indent=2)
print('[✓] Manifest stamped F13_REJECTED')
"
fi

# 4. Mark voice as revoked in VAULT999 (append-only ledger entry)
VAULT="/root/VAULT999/voice-revocations.jsonl"
mkdir -p "$(dirname "$VAULT")"
echo "{\"timestamp\":\"2026-08-25T07:49:00Z\",\"voice_id\":\"$REVOKED_VOICE_ID\",\"reason\":\"F13 reject by ARIF\",\"action\":\"revoke\"}" >> "$VAULT"
echo "[✓] Voice revocation logged to $VAULT"

# 5. Note: Tukki filter rename was audit-clean per Hermes report — no orphan to restore

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ROLLBACK COMPLETE — Gateway restart required (F13)"
echo "Next: ARIF restart gateway dari luar session ni"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
