# SCT_V1_PHASE1_SHADOW.md — Ed25519 Actor Binding (Shadow Build)

> **Authority:** Phase 1 of IDENTITY_BINDING_SPEC.md
> **Status:** SHADOW MODE — does not affect production authority decisions
> **Forge cycle:** FEDERATION-ALIGN-2026-07-14
> **Cutover:** GATED — requires 7-day parity report + second sovereign ack

---

## 1. Goal

Add Ed25519 actor signatures to sct_v1 alongside the existing HMAC. The shadow build:
- Generates an Ed25519 keypair per actor at bind time
- Signs the SCT payload with the actor's Ed25519 key
- Verifies the signature at attest time
- Records shadow results alongside production results
- Does **NOT** gate any authority decision until cutover

After 7 days of parity (shadow verdict = production verdict for ≥99% of calls), second sovereign ack authorizes cutover.

## 2. Why Ed25519 (not HMAC, not RSA, not ECDSA-P256)

| Algorithm | Sign | Verify | Key size | Notes |
|---|---|---|---|---|
| **HMAC-SHA256** (current) | symmetric — both sides need key | symmetric | 32 bytes secret | No non-repudiation; server can forge |
| **Ed25519** (this phase) | asymmetric — private signs | public verifies | 32-byte priv, 32-byte pub | Fast, deterministic, non-repudiable |
| RSA-2048 | asymmetric | asymmetric | 2048+ byte | Slow; large signatures |
| ECDSA-P256 | asymmetric | asymmetric | 32-byte priv | Non-deterministic (requires RFC 6979); patent issues |

Ed25519 wins on speed, determinism, key size, and non-repudiation. Reference: Bernstein 2011, IRTF RFC 8032.

## 3. Architecture (Shadow Mode)

```
Current production:
   client → arif_init(mode="init") → HMAC-signed sct → kernel decides

Shadow build (parallel):
   client → arif_init(mode="bind")   → Ed25519 keypair generated
         → arif_init(mode="attest") → Ed25519-signed shadow_sct
         → kernel decides (production HMAC path)
         → ALSO computes shadow verdict (Ed25519 path)
         → logs both: production_decision, shadow_decision, parity_match
```

Production never reads shadow_sct. Shadow never gates authority. They run in parallel.

## 4. Implementation Files

### 4.1 New module: `/root/arifOS/arifosmcp/runtime/actor_binding.py`

```python
"""
Shadow-mode Ed25519 actor binding for sct_v1.

Phase 1 of FEDERATION-ALIGN-2026-07-14 identity binding architecture.
Runs in PARALLEL with HMAC-signed production sct. Does not gate
authority until cutover (7-day parity + sovereign ack).
"""

from __future__ import annotations

import base64
import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization

logger = logging.getLogger(__name__)

ACTOR_KEYS_DIR = Path("/root/.arifos/agents/{actor_id}/keys")


@dataclass
class ActorKeypair:
    actor_id: str
    private_key: Ed25519PrivateKey
    public_key: Ed25519PublicKey
    pub_hex: str
    created_at: str

    def sign(self, payload: bytes) -> bytes:
        return self.private_key.sign(payload)

    @classmethod
    def verify(cls, pub_hex: str, signature: bytes, payload: bytes) -> bool:
        try:
            pub_bytes = bytes.fromhex(pub_hex)
            pub = Ed25519PublicKey.from_public_bytes(pub_bytes)
            pub.verify(signature, payload)
            return True
        except Exception as e:
            logger.warning(f"actor_binding.verify failed: {e}")
            return False


def generate_keypair(actor_id: str) -> ActorKeypair:
    """Generate Ed25519 keypair; store on host. Private key NEVER leaves."""
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    pub_raw = pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    pub_hex = pub_raw.hex()

    keydir = ACTOR_KEYS_DIR.format(actor_id=actor_id)
    keydir.mkdir(parents=True, exist_ok=True)
    # Store private key with restrictive perms (host filesystem trust assumed)
    priv_path = keydir / "ed25519.sec"
    priv_path.write_bytes(
        priv.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    priv_path.chmod(0o600)
    pub_path = keydir / "ed25519.pub"
    pub_path.write_text(pub_hex)
    pub_path.chmod(0o644)

    return ActorKeypair(
        actor_id=actor_id,
        private_key=priv,
        public_key=pub,
        pub_hex=pub_hex,
        created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )


def load_keypair(actor_id: str) -> Optional[ActorKeypair]:
    """Load existing keypair. Returns None if not present."""
    keydir = ACTOR_KEYS_DIR.format(actor_id=actor_id)
    priv_path = keydir / "ed25519.sec"
    pub_path = keydir / "ed25519.pub"
    if not priv_path.exists() or not pub_path.exists():
        return None
    priv_bytes = priv_path.read_bytes()
    priv = Ed25519PrivateKey.from_private_bytes(priv_bytes)
    pub_hex = pub_path.read_text().strip()
    pub_bytes = bytes.fromhex(pub_hex)
    pub = Ed25519PublicKey.from_public_bytes(pub_bytes)
    return ActorKeypair(
        actor_id=actor_id,
        private_key=priv,
        public_key=pub,
        pub_hex=pub_hex,
        created_at=str(priv_path.stat().st_mtime),
    )
```

### 4.2 New modes in `/root/arifOS/arifosmcp/runtime/tools_internal.py`

```python
async def arif_init_bind(arguments: dict) -> RuntimeEnvelope:
    """Phase 1 shadow mode: bind actor to Ed25519 public key."""
    actor_id = arguments.get("actor_id")
    if not actor_id:
        return RuntimeEnvelope(tool="arif_init_bind", ok=False, errors=[
            CanonicalError(code="MISSING_ACTOR", message="actor_id required")
        ])

    from .actor_binding import generate_keypair, load_keypair

    kp = load_keypair(actor_id)
    if kp is None:
        kp = generate_keypair(actor_id)
        logger.info(f"actor_binding: generated new keypair for {actor_id}")
    else:
        logger.info(f"actor_binding: loaded existing keypair for {actor_id}")

    return RuntimeEnvelope(
        tool="arif_init_bind",
        platform_context="stdio",
        ok=True,
        payload={
            "actor_id": actor_id,
            "actor_pub": kp.pub_hex,
            "created_at": kp.created_at,
            "shadow_mode": True,
            "phase": "phase_1_bind",
        },
        verdict="SHADOW_BIND_OK",
        status=RuntimeStatus.SUCCESS,
    )


async def arif_init_attest(arguments: dict) -> RuntimeEnvelope:
    """Phase 1 shadow mode: attest actor possession of private key."""
    actor_id = arguments.get("actor_id")
    actor_pub = arguments.get("actor_pub")
    challenge = arguments.get("challenge")  # hex-encoded
    signature = arguments.get("signature")  # hex-encoded

    if not all([actor_id, actor_pub, challenge, signature]):
        return RuntimeEnvelope(tool="arif_init_attest", ok=False, errors=[
            CanonicalError(code="MISSING_PARAMS", message="actor_id, actor_pub, challenge, signature all required")
        ])

    from .actor_binding import load_keypair, ActorKeypair
    kp = load_keypair(actor_id)
    if kp is None:
        return RuntimeEnvelope(tool="arif_init_attest", ok=False, errors=[
            CanonicalError(code="NO_KEYPAIR", message=f"no keypair for {actor_id}; run arif_init_bind first")
        ])

    # Verify signature
    challenge_bytes = bytes.fromhex(challenge)
    signature_bytes = bytes.fromhex(signature)
    valid = ActorKeypair.verify(actor_pub, signature_bytes, challenge_bytes)

    # Shadow verdict: matches production observation
    parity = valid == (arguments.get("production_verdict") == "SEAL")

    return RuntimeEnvelope(
        tool="arif_init_attest",
        platform_context="stdio",
        ok=valid,
        payload={
            "actor_id": actor_id,
            "attest_valid": valid,
            "shadow_parity": parity,
            "shadow_mode": True,
            "phase": "phase_1_attest",
        },
        verdict="SHADOW_ATTEST_OK" if valid else "SHADOW_ATTEST_FAIL",
        status=RuntimeStatus.SUCCESS if valid else RuntimeStatus.FAILURE,
    )
```

### 4.3 Tool registration (manifests)

Add to `/root/arifOS/arifosmcp/tool_registry.json`:

```json
{
  "arif_init_bind": {
    "stage": "000",
    "organ": "arifos",
    "mutation": false,
    "auth_required": false,
    "witness_required": "AI",
    "phase": "1",
    "shadow_mode": true
  },
  "arif_init_attest": {
    "stage": "000",
    "organ": "arifos",
    "mutation": false,
    "auth_required": true,
    "witness_required": "AI",
    "phase": "1",
    "shadow_mode": true
  }
}
```

## 5. Shadow Parity Logging

For every production call where shadow mode is active, log:

```json
{
  "epoch": "2026-07-14T...",
  "production_verdict": "SEAL" | "HOLD" | "VOID",
  "shadow_verdict": "SEAL" | "HOLD" | "VOID",
  "parity_match": true | false,
  "actor_id": "...",
  "session_id": "...",
  "tool": "..."
}
```

Daily parity report: aggregate last 24h, compute match rate.

**Cutover threshold:** ≥99% match over 7 days.

## 6. Rollout

| Day | Action | Authority |
|---|---|---|
| Day 0 | Code shipped in shadow; both modes run; no production decision uses shadow | T2 ANNOUNCE |
| Day 1-7 | Daily parity report; monitor drift | T1 |
| Day 7 | 7-day parity report → sovereign | T3 review |
| Day 7+ (if ack) | Cutover: shadow path becomes primary | T3 second ack |
| Day 7+ (if fail) | Investigate drift; iterate | T2 |

## 7. YubiKey Hardware-Backed Signing (Phase 6)

Phase 1 uses host-stored Ed25519 keys. **Phase 6** moves signing to hardware:
- YubiKey 5 (FIDO2 / PIV) — recommended
- Ledger Nano S/X — alternative

Sovereign procurement (Step 2 of next actions): buy 3-5 YubiKeys, one per agent + 2 sovereign spares. Phase 6 work is DEFERRED to Step 2 completion.

## 8. Acceptance Criteria (Phase 1 Done)

- [ ] actor_binding.py module implemented
- [ ] arif_init_bind tool callable via MCP
- [ ] arif_init_attest tool callable via MCP
- [ ] Tool manifests registered
- [ ] Shadow parity logging active
- [ ] 7-day parity report ≥99% match
- [ ] Sovereign second ack → cutover

---

## Provenance

- Phase 1 of IDENTITY_BINDING_SPEC.md
- Implementation: /root/arifOS/arifosmcp/runtime/actor_binding.py (new)
- Manifest: /root/arifOS/arifosmcp/tool_registry.json (additions)
- Audit cycle: FEDERATION-ALIGN-2026-07-14
- Vault head: seq 9914, sha256:6517b1fb1171e9461c1d8af634119acdc031e61767fbe44e0547a7336544880b

DITEMPA, BUKAN DIBERI.