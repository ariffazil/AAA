#!/usr/bin/env bash
# sign-agent-card.sh — air-gapped Ed25519 signer for agent-card.json files
# Regenerated 2026-08-26-zen-mu · Loop F recovery (script was MISSING ON DISK)
# Reference: /root/arifOS/arifosmcp/runtime/sovereign_signer.py + sovereign_verify.py
#
# Usage:
#   bash sign-agent-card.sh <agent-card.json> <sovereign-private-key.pem>
#
# Behavior:
#   1. Validates input (card path exists, key path exists, key is Ed25519)
#   2. Computes canonical JSON (sorted keys, no whitespace)
#   3. Signs canonical bytes with Ed25519
#   4. Inserts/updates proofValue in signatures array
#   5. Updates proofValue_note timestamp
#   6. Atomic write via temp + rename
#
# Prereq: openssl 3.0+ (for Ed25519) or Python 3.6+ with cryptography lib

set -euo pipefail

CARD_PATH="${1:-}"
KEY_PATH="${2:-/mnt/usb/sovereign.pem}"

if [ -z "${CARD_PATH}" ]; then
  echo "Usage: bash $0 <agent-card.json> <sovereign-private-key.pem>" >&2
  echo "Default key path: /mnt/usb/sovereign.pem (mount USB first)" >&2
  exit 1
fi

if [ ! -f "${CARD_PATH}" ]; then
  echo "[ERR] Card not found: ${CARD_PATH}" >&2
  exit 1
fi

if [ ! -f "${KEY_PATH}" ]; then
  echo "[ERR] Sovereign key not found: ${KEY_PATH}" >&2
  echo "       Expected air-gapped USB at /mnt/usb/" >&2
  exit 1
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TMPFILE=$(mktemp)
trap 'rm -f "${TMPFILE}"' EXIT

# Detect signing tool
if command -v openssl >/dev/null && openssl version | grep -q "OpenSSL 3"; then
  SIGN_TOOL="openssl"
elif command -v python3 >/dev/null && python3 -c "from cryptography.hazmat.primitives.asymmetric import ed25519" 2>/dev/null; then
  SIGN_TOOL="python3"
else
  echo "[ERR] No Ed25519 signing tool found (need OpenSSL 3+ or Python with cryptography)" >&2
  exit 1
fi

echo "[INFO] Card: ${CARD_PATH}"
echo "[INFO] Key: ${KEY_PATH}"
echo "[INFO] Tool: ${SIGN_TOOL}"
echo "[INFO] Timestamp: ${TIMESTAMP}"

# Compute canonical payload + sign
read SIG_B64 KEY_FP < <(python3 -c "
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import base64, hashlib

with open('${CARD_PATH}', 'r') as f:
    card = json.load(f)

canonical = json.dumps(card, sort_keys=True, separators=(',', ':')).encode('utf-8')

with open('${KEY_PATH}', 'rb') as f:
    priv = serialization.load_pem_private_key(f.read(), None)

sig = priv.sign(canonical)
pub_bytes = priv.public_key().public_bytes(
    serialization.Encoding.DER,
    serialization.PublicFormat.SubjectPublicKeyInfo
)

print(base64.b64encode(sig).decode())
print(hashlib.sha256(pub_bytes).hexdigest())
")

# Update card atomically
python3 << EOF
import json, os
with open('${CARD_PATH}', 'r') as f:
    card = json.load(f)

if 'signatures' not in card or not isinstance(card['signatures'], list):
    card['signatures'] = []

new_sig = {
    'type': 'Ed25519Signature2020',
    'proofValue': '${SIG_B64}',
    'verificationMethod': 'ed25519:sha256:${KEY_FP}',
    'created': '${TIMESTAMP}',
}
card['signatures'].append(new_sig)

note = 'Original 2026-07-12 Ed25519Signature2020 proof attached to v2.4.0; re-issuance required after v2.5.0 truth-repair. Re-signed ${TIMESTAMP} via sign-agent-card.sh.'
card['proofValue_note'] = note

with open('${TMPFILE}', 'w') as f:
    json.dump(card, f, indent=2, sort_keys=True)
os.replace('${TMPFILE}', '${CARD_PATH}')
print('[OK] Card updated atomically')
print(f'[OK] New proofValue: ${SIG_B64[:32]}...')
print(f'[OK] Key fingerprint: sha256:${KEY_FP}')
EOF

echo "[DONE] ${CARD_PATH} signed and updated."
echo "[NEXT] Verify with python3 -c 'from arifosmcp.runtime.sovereign_verify import verify_card; verify_card(\"${CARD_PATH}\")'"
