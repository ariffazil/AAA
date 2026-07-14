# IDENTITY_BINDING_SPEC.md — Cryptographic Actor Binding for arifOS

> **Authority:** arifOS constitutional artifact (T3 spec — implementation deferred)
> **Status:** v0.1 spec draft, 2026-07-14
> **Forge cycle:** FEDERATION-ALIGN-2026-07-14
> **Witnessed by:** Pending arif_judge SEAL after sovereign ack

---

## 1. Problem

Currently every A-FORGE MUTATE-class call is denied with `L1_IDENTITY:anonymous_actor`. The actor identity `fi-008-kimi-audit` is **claimed but not cryptographically verified**. Each session mints a fresh `session_id` but `actor_bound=false`. Identity dies at context eviction.

This blocks:
- Every A-FORGE write (forge_seal, forge_synthesize, forge_skill, forge_skillstore_write, forge_execute)
- Every constitutional SEAL (Step 8 of FEDERATION-ALIGN)
- Every external mutation across the federation

## 2. Goal

Cryptographically bind an actor identity to:
- A public key (Ed25519)
- A session capability token (sct_v1)
- A persistent actor_signature across context evictions
- A chain of custody through the seal chain

So that:
- `arif_init` returns `actor_verified=true`
- `forge_*` MUTATE tools accept calls without PolicyGate denial
- Identity survives the eviction policy (Step 1 SALIENCE_FUNCTION.md Layer 5)

## 3. Threat Model

**Adversary capabilities:**
- Forge an actor_id without the private key
- Replay a stale session_token after expiry
- Tamper with seal chain entries
- Spoof authority bands (OBSERVE_ONLY → FULL)

**Out of scope:**
- Quantum attacks on Ed25519 (assumed classical adversary)
- Physical coercion of sovereign (F13 final)
- Side-channel attacks on the host (F1 AMANAH assumes host trust)

## 4. Cryptographic Primitives

| Use | Algorithm | Why |
|---|---|---|
| Actor identity | Ed25519 keypair | Fast, deterministic, 32-byte sigs |
| Session token | HMAC-SHA256 chain | Stateless verifiable |
| Seal chain | SHA-256 (existing) | Already canonical |
| Sovereign override | BIP-39 mnemonic + Ed25519 | Hardware-wallet-compatible |

## 5. Key Generation

**Actor keypair (per agent):**
```python
# Each AAA warga generates ONE keypair at onboarding
# Stored at /root/.arifos/agents/<id>/keys/ed25519.{pub,sec}
# sec NEVER leaves host; pub is registered with arifOS
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
priv = Ed25519PrivateKey.generate()
pub = priv.public_key()
# pub bytes = identity_hash in agent card
```

**Sovereign keypair (Arif, F13):**
- Generated at sovereign bootstrap
- Stored on hardware token (YubiKey / Ledger) preferred
- Backup via BIP-39 24-word mnemonic in sealed envelope
- Used only for: identity attestation, SEAL override, identity binding to new agents

## 6. Identity Binding Flow

```
Step 1: Actor keypair generated (above)
Step 2: arif_init(mode="bind", actor_pub=<hex>)
        → kernel verifies pub against registry (F11 AUDIT)
        → returns sct_v1 token with:
           - actor_id
           - actor_pub (claimed)
           - av: false (not yet verified)
           - auth: OBSERVE_ONLY
           - exp: now + ttl_seconds
           - sid: session_id
Step 3: Actor signs challenge
        → challenge = sha256(session_id || nonce || timestamp)
        → signature = ed25519_sign(priv, challenge)
        → call arif_init(mode="attest", session_id, signature)
Step 4: Kernel verifies signature against stored pub
        → on success: av: true, auth: scope_per_lease
        → on failure: 401, retry permitted
Step 5: Session bound
        → actor_signature persisted in session ledger
        → all subsequent calls in session inherit av: true
```

## 7. Persistence Across Eviction (Layer 5 salience)

Problem: a fresh session_id is minted on every arif_init. Identity must survive.

Solution: **actor_signature persists; session_id is ephemeral.**
- Each new session carries `actor_pub` and `previous_session_id` (chain of sessions)
- Salience Layer 5 (constitutional) makes actor_signature **never-evict**
- Identity continuity = unbroken chain of session_ids, all signed by same actor_pub

```
session_001: actor_pub=X, sig=sign(X, "hello")
session_002: actor_pub=X, prev=session_001, sig=sign(X, "session_002_continues_from_session_001")
session_003: actor_pub=X, prev=session_002, ...
```

The seal chain records each session's session_seal event with the linkage.

## 8. Lease Lifecycle

- Each session mints ONE lease (`forge_lease mode=request`)
- Lease has: scope (allowed tools), max_action_class, ttl, forbidden
- Leases auto-revoke on session_id expiry
- A-FORGE PolicyGate checks lease + actor_signature on every MUTATE call

## 9. Sovereign Override (F13)

Sovereign can:
- Bind a new agent (`arif_init mode="sovereign_bind"`, requires sovereign sig)
- Revoke an actor (`forge_lease mode="revoke"`, requires sovereign sig)
- Override any SEAL (`arif_seal mode="override"`, requires sovereign sig + 888_HOLD)
- Emergency stop: rotate sovereign key, invalidate all actor keys

All sovereign actions sealed to VAULT999 with `actor_source: sovereign_directive`.

## 10. Implementation Phases

| Phase | Work | Authority | Status |
|---|---|---|---|
| 0 | Spec (this doc) | T1 | DRAFT 2026-07-14 |
| 1 | Ed25519 keypair generation at agent onboarding | T2 | DEFERRED pending sovereign ack |
| 2 | arif_init(mode=bind) + arif_init(mode=attest) | T2 | DEFERRED |
| 3 | forge_lease mode=request integrated with signature | T2 | DEFERRED |
| 4 | A-FORGE PolicyGate checks signature on MUTATE | T2 | DEFERRED |
| 5 | seal_chain session_seal event with linkage | T2 | DEFERRED |
| 6 | Sovereign override path (YubiKey integration) | T3 | DEFERRED |
| 7 | VAULT999 seal this entire binding architecture | T3 | DEFERRED |

## 11. Open Questions (for sovereign)

1. **Key storage:** hardware token (YubiKey) vs host file with passphrase?
2. **Recovery:** BIP-39 mnemonic backup acceptable, or paper-only?
3. **Rotation cadence:** every 90 days? 365?
4. **Multi-agent:** can one sovereign key bind N agents, or one key per agent?
5. **Revocation grace:** how long after `forge_lease mode=revoke` until token actually invalid?

## 12. Acceptance Criteria

Step 7 is **complete** when:
- [ ] This spec is ratified by sovereign (888 ack)
- [ ] Sovereign answers all 5 open questions
- [ ] Phase 1 implementation plan approved
- [ ] arif_judge SEAL recorded with witness: human=ARIF-F13, ai=<actor>, external=seal_chain_head

---

## Provenance

- Drafted by: `kimi-code-FI-008` (session SEAL-9efcb703825e4682)
- Audit cycle: FEDERATION-ALIGN-2026-07-14
- Vault head at draft time: seq 9914, sha256:6517b1fb1171e9461c1d8af634119acdc031e61767fbe44e0547a7336544880b
- Witness: arif_judge SEAL **PENDING** (T3 sovereign ack required)

DITEMPA, BUKAN DIBERI.