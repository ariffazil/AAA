# Crypto Attestation Slice 0001

Minimal first slice for cryptographically attested agent governance.

## Scope

1. Build a real signed verdict capsule over a real local artifact
2. Verify it offline in AAA
3. Add an A-FORGE execution gate helper that rejects unsigned/invalid capsules
4. Seal capsule metadata into VAULT999 using the existing v2 epoch writer

This slice was bootstrapped through demo scripts during the first proof cycle.
Those bootstrap/demo paths are now archived and should be deleted after refactor.
The active canon is:
- `/root/AAA/auth/gen_did.py`
- `/root/AAA/core/capsule.py`
- `/root/arifOS/VAULT999/sign_capsule_to_vault.py`
Archive note:
- `/root/AAA/docs/archive/CRYPTO_ATTESTATION_BOOTSTRAP_ARCHIVE.md`

## Files

- `AAA/auth/gen_did.py`
- `AAA/core/capsule.py`
- `A-FORGE/src/domain/governance/SignedCapsuleGate.ts`
- `arifOS/VAULT999/sign_capsule_to_vault.py`

## Demo Flow

```bash
python3 /root/AAA/auth/gen_did.py --list
python3 /root/arifOS/VAULT999/sign_capsule_to_vault.py \
  --capsule /root/AAA/artifacts/sovereign-did/capsule.json
```

## Meaning

- AAA becomes a verifier, not a trust bottleneck
- A-FORGE gets a concrete unsigned-payload refusal primitive
- VAULT999 starts carrying signed capsule evidence without a new ledger design

## Not Done Yet

- No live service wiring
- No DID resolver
- No hardware-backed sovereign key
- No zk proof layer
