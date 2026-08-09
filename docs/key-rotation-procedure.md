<!-- SATELLITE | tier:satellite | sot:STATE.md | 2026-08-09 -->
> **Satellite** — historical elaboration / design note / prior draft.  
> **Canonical SOT:** [`STATE.md`](./STATE.md) (§1–16).  
> If this file conflicts with STATE.md, **STATE wins**. Do not fork law here.  
> *One truth · Many projections · 0 contradictions* · DITEMPA BUKAN DIBERI.

# AAA Federation — Key Rotation & Revocation Procedure

> **Authority:** F13 SOVEREIGN  
> **Forged:** 2026-08-07 by 333-AGI under F13 directive  
> **Scope:** Ed25519 signing keys for AAA warga agents (OpenClaw, Hermes, A-FORGE, etc.)

## When to rotate

| Trigger | Action |
|---------|--------|
| Key age > 90 days | Schedule rotation |
| Suspected compromise | **Immediate rotation + revocation** |
| Agent identity change | Rotate as part of re-registration |
| Pre-production deployment | Fresh key for production environment |

## Procedure

### 1. Generate new Ed25519 keypair

```bash
# Generate 32-byte seed + derive keypair
python3 -c "
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import os

seed = os.urandom(32)
key = Ed25519PrivateKey.from_private_bytes(seed)
pubkey = key.public_key()

# Save private key (seed format, compatible with arifOS convention)
with open('/root/AAA/auth/keys/openclaw_private.key', 'wb') as f:
    f.write(seed)
os.chmod('/root/AAA/auth/keys/openclaw_private.key', 0o600)

# Save public key (raw 32 bytes)
pub_bytes = pubkey.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)
with open('/root/AAA/auth/keys/openclaw_public.key', 'wb') as f:
    f.write(pub_bytes)
os.chmod('/root/AAA/auth/keys/openclaw_public.key', 0o644)
"
```

### 2. Compute new DID

```bash
python3 -c "
import base64
with open('/root/AAA/auth/keys/openclaw_public.key', 'rb') as f:
    pubkey = f.read()
multicodec = b'\xed\x01' + pubkey  # ed25519-pub
did = 'did:key:z' + base64.b64encode(multicodec).decode().rstrip('=').replace('+','-').replace('/','_')
print(f'New DID: {did}')
"
```

### 3. Update DID registry

```bash
# Edit /root/AAA/secrets/did/registry.json
# Replace old DID entry with new DID
# Update updated_at timestamp
```

### 4. Update organs.yaml

```bash
# Edit /root/AAA/federation/organs.yaml
# Update did: field for the agent
# Update live_probe timestamp
```

### 5. Update bridge config (OpenClaw)

```bash
# Edit /root/AAA/agents/openclaw/config/intent-router.yaml (if DID embedded)
# Update DID reference in agent-card.json
```

### 6. Restart affected services

```bash
systemctl restart aaa-a2a
systemctl restart openclaw-gateway  # if key used for signing
```

### 7. Verify

```bash
# Test A2A dispatch with new key
python3 /root/AAA/agents/openclaw/bridge/tests/test_bridge_e2e.py

# Verify DID registry
python3 -c "import json; r=json.load(open('/root/AAA/secrets/did/registry.json')); print(r['dids'].keys())"

# Run rejection matrix to confirm old key is rejected
# (old DID should return 403)
```

## Revocation

### Immediate revocation (compromise)

1. Remove old DID entry from `/root/AAA/secrets/did/registry.json`
2. Remove old public key from `/root/AAA/auth/keys/`
3. Restart AAA service immediately
4. Audit security receipts for any accepted envelopes from compromised key in the compromise window
5. Rotate to new keypair

### Graceful revocation (scheduled rotation)

1. Generate new keypair following rotation procedure above
2. Add new DID to registry alongside old DID (dual-entry window)
3. Update bridge/agent to use new key
4. Verify new key works (rejection matrix pass)
5. Remove old DID from registry
6. Archive old keypair to cold storage (VAULT999 backup)
7. Update rotation log

## Rotation log

Maintain at `/root/AAA/secrets/did/rotation-log.jsonl`:

```json
{"ts":"2026-08-07T15:00:00Z","agent":"openclaw","old_did":"did:key:zOld...","new_did":"did:key:zNew...","reason":"scheduled_90_day","verified":true}
```

## Security properties

| Property | Guarantee |
|----------|-----------|
| Old key invalidation | Immediate upon DID registry removal + AAA restart |
| Zero-downtime rotation | Supported via dual-DID window |
| Audit trail | Rotation log + security receipts + git history |
| Compromise detection | Security receipts show all rejected envelopes with old DID |
| Recovery | Old key archived to cold storage; restorable if needed |

## F13 sovereign approval

Key rotation for any agent that handles MUTATE-class or ATOMIC-class operations requires F13 sovereign approval before execution. Document the approval in the rotation log.

---

*Forged: 2026-08-07 · Part of AAA production gate completion · DITEMPA BUKAN DIBERI*
