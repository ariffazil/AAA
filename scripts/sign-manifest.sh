#!/bin/bash
# sign-manifest.sh — Sign the bootstrap manifest with root-arif-888
# Usage: bash /root/AAA/scripts/sign-manifest.sh
# Requires: /root/.secrets/bootstrap/root-arif-888 (private key)

set -euo pipefail

MANIFEST="/root/AAA/skills/BOOTSTRAP_MANIFEST.json"
KEY="/root/.secrets/bootstrap/root-arif-888"
PUBKEY="/root/.secrets/bootstrap/root-arif-888.pub"

if [ ! -f "$KEY" ]; then
    echo "❌ Private key not found: $KEY"
    exit 1
fi

if [ ! -f "$MANIFEST" ]; then
    echo "❌ Manifest not found: $MANIFEST"
    exit 1
fi

# Compute hash
HASH=$(sha256sum "$MANIFEST" | awk '{print $1}')
echo "Manifest hash: sha256:${HASH:0:32}"

# Sign using Python (more reliable than ssh-keygen -Y)
python3 -c "
import json, hashlib, base64
from cryptography.hazmat.primitives.serialization import load_ssh_private_key

with open('$KEY', 'rb') as f:
    private_key = load_ssh_private_key(f.read(), password=None)

with open('$MANIFEST', 'rb') as f:
    manifest_bytes = f.read()

manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
signature = private_key.sign(manifest_hash.encode())
sig_b64 = base64.b64encode(signature).decode()

manifest = json.loads(manifest_bytes)
manifest['signatures'] = [{
    'key_id': 'root-arif-888',
    'algorithm': 'ed25519',
    'signature': sig_b64,
    'signed_at': '$(date -u +%Y-%m-%dT%H:%M:%SZ)',
    'covers': 'full_manifest',
    'fingerprint': '$(ssh-keygen -lf $PUBKEY | awk "{print \$2}")'
}]
manifest['status'] = 'SIGNED'

with open('$MANIFEST', 'w') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print('✅ Manifest signed and updated')
"

echo "Done. Manifest: $MANIFEST"
