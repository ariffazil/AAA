# Sovereign Key Locations

> **Updated:** 2026-07-13 — CIV-33 final seal

## Ed25519 Keys

| Key | Path | Purpose |
|-----|------|---------|
| `omega_private.key` | `/root/AAA/auth/keys/omega_private.key` | Sovereign signing — Arif's Ed25519 key for nonce signatures |
| `omega_public.key` | `/root/AAA/auth/keys/omega_public.key` | Sovereign verification — published in DID document |
| `arif_private.pem` | `/root/.secrets/aaa-identity/keys/arif_private.pem` | Legacy identity key |
| `arif_public.pem` | `/root/.secrets/aaa-identity/keys/arif_public.pem` | Legacy verification key |

## SOVEREIGN_KEY_IDS (kernel)

Defined in `/root/arifOS/arifosmcp/runtime/governance_identity.py:44`:

```python
SOVEREIGN_KEY_IDS: set[str] = {
    "ed25519:sha256:a8fbb5ae8b4772b0",  # Arif /000/ DID key (did:web:arif-fazil.com)
    "ed25519:sha256:9c35a833fef25f17",  # Arif AAA identity key (2026-07-12)
}
```

## IMAGE_SEAL Handling

IMAGE_SEAL entries (GEOX well renders) use a separate schema and MUST NOT share the main `seal_chain.jsonl` file. They should go to `image_seal_chain.jsonl` instead. The main chain requires strict `seq` + `prev_seal_hash` chain integrity.

## Verification

```bash
# Test sovereign signing
python3 /root/AAA/auth/gen_did.py --list

# Sign a nonce
python3 -c "
from nacl.signing import SigningKey
key = SigningKey(open('/root/AAA/auth/keys/omega_private.key').read().strip())
sig = key.sign(b'test').signature.hex()
print(f'Signing works: {sig[:16]}...')
"
```
