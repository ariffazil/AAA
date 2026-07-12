#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
# SOVEREIGN KEY GENERATION + MANIFEST SIGNING
# Run this on an AIR-GAPPED machine or HSM-backed device.
# NEVER run this on a networked machine.
# DITEMPA BUKAN DIBERI.
# ─────────────────────────────────────────────────────────
set -euo pipefail

MANIFEST_PATH="${1:-/root/AAA/kernel/bootstrap_manifest.json}"
KEY_DIR="${2:-/root/.secrets/sovereign}"
KEY_NAME="root-arif-888"

echo "══════════════════════════════════════════════════════"
echo "  SOVEREIGN KEY GENERATION — root-arif-888"
echo "  AIR-GAPPED ONLY. Disconnect network before running."
echo "══════════════════════════════════════════════════════"

# Step 0: Safety check
read -p "Is this machine air-gapped? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "ABORT. Disconnect network first."
    exit 1
fi

# Step 1: Generate Ed25519 keypair
mkdir -p "$KEY_DIR"
chmod 700 "$KEY_DIR"

echo ""
echo "[1/5] Generating Ed25519 keypair..."
ssh-keygen -t ed25519 \
    -f "${KEY_DIR}/${KEY_NAME}" \
    -C "${KEY_NAME}" \
    -a 100 \
    -N ""

echo "  Private key: ${KEY_DIR}/${KEY_NAME}"
echo "  Public key:  ${KEY_DIR}/${KEY_NAME}.pub"
echo "  ⚠️  BACK UP THE PRIVATE KEY IMMEDIATELY"

# Step 2: Compute manifest hash
echo ""
echo "[2/5] Computing manifest hash..."
MANIFEST_HASH=$(sha256sum "$MANIFEST_PATH" | awk '{print $1}')
echo "  sha256:${MANIFEST_HASH}"

# Step 3: Sign the manifest hash
echo ""
echo "[3/5] Signing manifest hash..."
SIGN_INPUT=$(mktemp)
echo -n "sha256:${MANIFEST_HASH}" > "$SIGN_INPUT"

ssh-keygen -Y sign \
    -f "${KEY_DIR}/${KEY_NAME}" \
    -n "manifest" \
    "$SIGN_INPUT"

SIGNATURE_FILE="${SIGN_INPUT}.sig"
SIGNATURE=$(cat "$SIGNATURE_FILE")
echo "  Signature: ${SIGNATURE:0:64}..."

# Step 4: Create ratification object
echo ""
echo "[4/5] Creating ratification object..."
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
PUB_KEY_FP=$(ssh-keygen -lf "${KEY_DIR}/${KEY_NAME}.pub" | awk '{print $2}')

RATIFICATION_FILE="${KEY_DIR}/sovereign_signature.json"
cat > "$RATIFICATION_FILE" << EOF
{
  "manifest_hash": "sha256:${MANIFEST_HASH}",
  "ratifier_id": "${KEY_NAME}",
  "public_key_fingerprint": "${PUB_KEY_FP}",
  "timestamp": "${TIMESTAMP}",
  "signature": "${SIGNATURE}",
  "algorithm": "ed25519",
  "signed_by": "ARIF",
  "note": "Sovereign signature for AAA bootstrap manifest. This file is the root of trust."
}
EOF

echo "  Ratification: ${RATIFICATION_FILE}"

# Step 5: Verify
echo ""
echo "[5/5] Verifying signature..."
if ssh-keygen -Y verify \
    -f "${KEY_DIR}/${KEY_NAME}.pub" \
    -n "manifest" \
    -s "$SIGNATURE_FILE" \
    "$SIGN_INPUT" 2>/dev/null; then
    echo "  ✅ SIGNATURE VERIFIED"
else
    echo "  ❌ VERIFICATION FAILED"
    exit 1
fi

# Cleanup
rm -f "$SIGN_INPUT" "$SIGNATURE_FILE"

echo ""
echo "══════════════════════════════════════════════════════"
echo "  DONE. Next steps:"
echo "  1. Copy ${RATIFICATION_FILE} to the kernel node"
echo "  2. Place it at /root/AAA/kernel/sovereign_signature.json"
echo "  3. Run: python3 /root/AAA/kernel/kernel_boot.py"
echo "  4. Verify: Status should be SIGNED"
echo ""
echo "  ⚠️  BACK UP THE PRIVATE KEY:"
echo "     ${KEY_DIR}/${KEY_NAME}"
echo "  Use Shamir Secret Sharing for split backup."
echo "══════════════════════════════════════════════════════"
