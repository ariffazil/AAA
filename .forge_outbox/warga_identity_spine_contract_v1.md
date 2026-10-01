# WARGA Identity Spine Contract v1 (P1.d — Stage 3 contract, F13 SAH)

> **Status:** STAGED-ARTIFACT, F13 RATIFIED for direction-of-record change. Sovereign directive "ok do all. SAH" received 2026-10-01.
> **Direction-of-record change:** "FI-008 / kimi-code / kimi-code-fi008 → one canonical principal; sovereign key issuance required." F13-ratified per sovereign ratification in this session.
> **Lineage:** Identity split-brain scar sealed 2026-09-08 by kimi-code/FI-008; Constitutional Architecture Canon HALAL-positive predicate `Authorized ∧ Provenanced ∧ TemporallyValid`; Six-Graph Federation Model (F13_RATIFIED_CHAT 2026-09-16); hermes/codex/openclaw 2026-07-09 identity-verification pattern; live audit this session confirmed 3 split entries for FI-008 principal.
> **Purpose:** Single canonical principal for kimi-code / FI-008 / kimi-code-fi008 with cryptographic identity proof, registered against arifOS kernel.
> **Why this matters:** Without this, FI-008 is W1 (Resident-Registry) instead of W2 (Verified-Citizen). Live scar 2026-09-08 already proved the constraint.

---

## The principal ID — one canonical identity

```yaml
principal_identity:
  canonical_id: kimi-code/FI-008  # canonical principal_id for all three surfaces
  surface_ids:
    - kimi-code            # legacy registration
    - FI-008               # sovereign-issued Forge Instrument
    - kimi-code-fi008      # custom registration
  alias_resolution_policy: surface_to_canonical_first_match
  alias_collision_check:  scar_2026_09_08_split_brain_sealed
```

**Rule:** all three surface_ids resolve to ONE canonical_id. Future surfaces of the same principal MUST be added to `surface_ids` (append-only).

---

## The cryptographic key registration protocol

### Step 1 — Sovereign generates keypair (offline)

```bash
# Sovereign runs this in HIS terminal, never in mine.
mkdir -p /root/.kimi-code/keys/principal-kimi-code-FI-008
cd /root/.kimi-code/keys/principal-kimi-code-FI-008

# Generate ed25519 keypair (private key — sovereign holds)
openssl genpkey -algorithm ed25519 -out private_key.pem

# Extract public key (sovereign gives me the public_pem only)
openssl pkey -in private_key.pem -pubout -out public_key.pem

# Compute fingerprint (sovereign sends me this string)
openssl pkey -in private_key.pem -pubout -outform DER | sha256sum | awk '{print $1}'
```

The sovereign holds PRIVATE_KEY. The sovereign transmits PUBLIC_KEY (string) + FINGERPRINT (sha256 hex) to me for registration. **The private key never leaves sovereign's machine.**

### Step 2 — Sovereign-attested identity (offline or via sovereign-chat)

The sovereign signs a statement:

```
SIGNATURE <filepath> <canonical_id> <public_pem_fingerprint> <signing_algo>
```

Where:
- `canonical_id` = `kimi-code/FI-008`
- `public_pem_fingerprint` = sha256 hex from Step 1
- `signing_algo` = `ed25519`

This is the sovereign's attestation that the principal `kimi-code/FI-008` is bound to the keypair at that fingerprint.

### Step 3 — Agent registration (autonomous, FI-008 executes on sovereign's instruction)

```python
# Once sovereign transmits the public-key + signature:
import hashlib

with open(public_key_path) as f:
    public_key_pem = f.read()
public_key_fingerprint = hashlib.sha256(public_key_pem.encode()).hexdigest()

register_payload = {
    "agent_id": "FI-008",                # canonical_id
    "agent_type": "custom",
    "role": "governed_coder",
    "identity_proof": {
        "type": "ed25519",
        "public_key_fingerprint": f"sha256:{public_key_fingerprint}",
        "public_key_pem": public_key_pem,
        "registered_at": "<iso8601>",
        "verification_method": "sovereign_approval",
        "verified_by": "sovereign",
        "sovereign_signature": "<signature_blob>",
        "sovereign_signature_at": "<iso8601>",
        "sovereign_principal_claim": "kimi-code/FI-008",
        "sovereign_claim_witness_organ": "AAA",
    },
    "principal_id": "kimi-code/FI-008",  # canonical
    "surface_ids": ["kimi-code", "FI-008", "kimi-code-fi008"],
    "split_brain_resolution": "scar_2026_09_08_applied",
    "alias_collision_check_passed": True
}
```

Call `forge_agent mode=register` with this payload.

### Step 4 — Alias collapse (autonomous, FI-008 executes)

After Step 3, three surface rows for FI-008 will exist. Alias collapse requires the kernel to:
- Recognize `surface_id=kimi-code` → `principal_id=kimi-code/FI-008`
- Recognize `surface_id=kimi-code-fi008` → `principal_id=kimi-code/FI-008`
- Recognize `surface_id=FI-008` → `principal_id=kimi-code/FI-008`

This is the kernel-side reconciliation. Per HUMA bridge Law 6: alias_of must be one-to-one.

### Step 5 — Split-brain-scar closure

The scar sealed 2026-09-08 (kimi-code/FI-008) already documents this gap. After Step 3 + Step 4, the scar is closed by evidence, not by `forge_scar` either (just by future closure of the contraction).

---

## The signing challenge — ongoing surface sovereignty

After registration, every `arif_init` call from FI-008 must carry a sovereign-attested challenge that proves FI-008 holds the private key matching the registered public key.

```
arif_init(actor_id="kimi-code/FI-008")
   ↓
arifOS kernel generates a nonce challenge
   ↓
challenge sent to sovereign's runtime
   ↓
sovereign's runtime signs challenge with private_key.pem
   ↓
signed_challenge returned to arifOS
   ↓
arifOS verifies signature against registered public_key.pem
   ↓
arif_init returns ACT (capability token) bound to canonical_id
```

**Rule:** the kernel never trusts an unverified `actor_id`. Sovereign attestation is per-session, not per-call. The FI-008 session becomes `actor_verified=true` after Step 5 succeeds.

---

## Receipt chain for this artifact

- F13 ratification signal: sovereign directive "ok do all. SAH" 2026-10-01.
- Live scar: `scar_1790*_identity_splitbrain` sealed 2026-09-08 by kimi-code/FI-008.
- Live audit this session: forge_agent confirms 3 split entries for FI-008 principal.
- This contract artifact: `/root/AAA/.forge_outbox/warga_identity_spine_contract_v1.md`.

---

## What I have NOT done

Per Anti-HARAM doctrine, **I have not generated the sovereign's private key**. The sovereign's key issuance is sovereign's action.

**What I CAN do autonomously, on sovereign's instruction:**
- Once sovereign transmits the public_pem + fingerprint + signature, register FI-008 with the cryptographic identity proof.
- Once FI-008 is registered, alias-collapse the 3 surface rows to one canonical principal.
- After Step 5, FI-008 can sign arif_init challenges as a verified W2 citizen.

**What the sovereign must do (sovereign action):**
- Generate the keypair in HIS terminal (Step 1).
- Sign the identity attestation (Step 2).
- Transmit public_pem + fingerprint + signature to me (via in-session paste or out-of-band).
- Hold the private key for future arif_init signing challenges.

---

## Authority contract — what FI-008 gains and what it gains-not

GAINS (after Step 5):
- `actor_verified=true` in arifOS (current is `false`).
- `trust_tier=OBSERVED` (current is `UNVERIFIED`).
- Full HALAL-positive 7-conjunction chain available (current is narrowed to OBSERVE_ONLY).
- Access to arifOS verbs `arif_judge`, `arif_seal`, `arif_memory` (mode=promote), and others.

GAINS-NOT (the changed authority is bounded by Gödel + HALAL):
- Can't promote ALONE — arifOS Judge is still the constitutional authority.
- Can't widen its own envelope — F13 sovereign is the only one that can widen.
- Can't seal independently — kernel seal signature required.

---

## Stage wiring

| Stage | Wiring |
|---|---|
| Stage 0 | `drift-reconcile-unblock-test-2026-10-02` clears substrate drift |
| Stage 1 | Lesson Compiler + Behaviour-Delta Verifier + Surface Truth + Capability Metabolism (autonomous, done) |
| Stage 2 | arifOS-L13 wires `forge_rsi_state_vector.identity.principal_id` schema; wires alias-collapse logic |
| Stage 3 | **THIS CONTRACT, F13 SAH**. Sovereign key issuance required. |
| Runtime | `identity.principal_id=kimi-code/FI-008`, `identity.cryptographically_verified=true` (after Step 5) |

---

## Receipt chain

- F13 ratification signal: sovereign directive "ok do all. SAH" 2026-10-01.
- Live scar: `scar_1790*_identity_splitbrain` sealed 2026-09-08 by kimi-code/FI-008.
- Live audit this session: forge_agent confirms 3 split entries for FI-008 principal.
- This contract artifact: `/root/AAA/.forge_outbox/warga_identity_spine_contract_v1.md`.

DITEMPA BUKAN DIBERI ⚒️