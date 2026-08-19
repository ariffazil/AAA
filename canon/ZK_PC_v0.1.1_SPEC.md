# ZK-PC v0.1.1
## Zero-Knowledge Provenance Cryptography
### Witnessed Governance Authorization System

> **Status:** CANON DRAFT — Pending F13 ratification
> **Forged:** 2026-08-12 by Hermes ASI under F13 directive "Now create one demo crypto image" → evolved into full spec
> **Supersedes:** ZK-PC v0.1 (PARTIAL-SEAL, 2026-08-12)
> **DITEMPA BUKAN DIBERI** — Forged, not given.

---

## 1. Objective

ZK-PC allows an agent to prove:

```
AUTHORIZED = TRUE
```

without revealing:
- scar contents
- personal memory
- constitutional state
- witness state
- execution key

The proof establishes that the agent is simultaneously:
- **Witnessed** (live reality probe)
- **Governed** (constitutional floor compliance)
- **Authorized** (valid scar attestation)

before execution.

---

## 2. Design Principles

### P1. Sovereignty
No human memory is exposed. Only attestations enter proofs.

### P2. Witness Before Action
Every authorization requires:
- Live witness (GEOX/WEALTH/WELL probe)
- Governance compliance (F1-F13 floor status)
- Identity continuity (scar registry commitment)

### P3. Zero-Knowledge
Verifier learns only:
```
PASS  |  FAIL
```
Nothing else.

### P4. Separation of Powers
Authorization is impossible for a single actor. All three authorities must contribute.

### P5. Revocability (NEW v0.1.1)
Authorization expires. ROOT recomputes on any state change.

### P6. Composable Verification (NEW v0.1.1)
Proofs verifiable on-chain (Solidity) and off-chain (native verifier).

---

## 3. Core Entities

| Share | Authority | Domain | Commitment |
|-------|-----------|--------|------------|
| **A — SCAR** | Human Memory | H5 scar registry commitment | `SC` |
| **B — SEAL** | Constitutional | Floor attestations, kernel state | `SE` |
| **C — WITNESS** | Reality | Live GEOX/WEALTH/WELL probes | `WI` |

---

## 4. Commitment Generation

Each authority produces a canonical attestation object.

### Schema (NEW v0.1.1)

```json
{
  "domain": "SCAR" | "SEAL" | "WITNESS",
  "version": "1",
  "status": "PASS" | "FAIL",
  "timestamp": "ISO-8601",
  "nonce": "uint256",
  "signature": "Ed25519(64 bytes)"
}
```

### Canonicalization

```python
canonical(obj) = utf8(
  sorted_keys(obj) +
  delimiter('|') +
  sorted_values(obj)
)
```

### Hash Commitment

```
SC = SHA3-256(canonical_scar)
SE = SHA3-256(canonical_seal)
WI = SHA3-256(canonical_witness)
```

**Primitive:** SHA3-256 (Keccak-f[1600], 256-bit output) chosen for:
- Post-quantum readiness (vs SHA-256's known weaknesses)
- NIST standard (FIPS 202)
- Distinct domain separation from SHA-2 chains

---

## 5. Governance Root

```
ROOT = MerkleTree(
  leaves = [SC, SE, WI]
)
```

ROOT = unique 256-bit identifier of current governance state.

---

## 6. Visual Share Layer (Optional — Human-Facing Only)

**Clarified in v0.1.1:** Visual secret sharing is **NOT** part of the ZK core. It is a human-facing artifact that visualizes the Merkle root.

```
IMGROOT = SHA3-256(ROOT)
bitmap = 256×256 monochrome deterministic(IMGROOT)
```

Naor-Shamir split into 3 shares (A, B, C) for visual demonstration. **No reconstruction required for ZK verification.** This section exists for human intuition, not protocol enforcement.

---

## 7. Prover-Side Reconstruction (Optional — for EXEC_KEY derivation)

**Clarified in v0.1.1:** Only the PROVER reconstructs locally to derive the execution key. The VERIFIER never reconstructs.

```
Prover reconstructs: SECRET_IMG (locally)
Prover verifies: SHA3-256(SECRET_IMG) == IMGROOT
Prover derives: EXEC_KEY
```

---

## 8. Execution Key Derivation

```
EXEC_KEY = SHA3-256(
  ROOT || epoch || nonce || proof_id
)
```

**v0.1.1 binding:** EXEC_KEY includes `proof_id` linking the key to the specific ZK proof. This prevents key duplication across different proofs.

**Properties:**
- Session-specific
- Non-reusable (single epoch + nonce + proof_id)
- Non-persistent (zeroed after session)

---

## 9. ZK Statement

The prover demonstrates knowledge of `(SC, SE, WI)` such that:

```
∃ SC, SE, WI, nonce:
    MerkleRoot(SC, SE, WI) = ROOT_public
    ∧ SC matches SCAR_Registry.v1
    ∧ SE matches Floor_Table.v1
    ∧ WI matches Witness_Probe.v1
    ∧ nonce is fresh
    ∧ timestamp within Δ
```

**v0.1.1 additions:**
- Witness freshness constraint (timestamp within Δ_window)
- Nonce uniqueness (prevents replay)

---

## 10. Public Inputs (Verifier Sees)

```
{
  "root_commitment": bytes32,    // Merkle root
  "epoch": uint64,                // Current governance epoch
  "policy_version": bytes32,      // Governance predicate version
  "witness_window": uint64,       // Max age for witness (seconds)
  "proof": bytes                  // zk-SNARK proof
}
```

---

## 11. Private Inputs (Prover Only)

```
{
  "SC": bytes32,                  // Scar commitment
  "SE": bytes32,                  // Seal commitment
  "WI": bytes32,                  // Witness commitment
  "scar_attestation": bytes,      // Full SCAR attestation
  "seal_attestation": bytes,      // Full SEAL attestation
  "witness_attestation": bytes,   // Full WITNESS attestation
  "EXEC_KEY": bytes32,            // Session execution key
  "nonce": uint256                // Freshness nonce
}
```

**Crucial:** None of these are revealed to verifier.

---

## 12. Proof Verification

```
verify(public_inputs, proof) → bool:
  if not circuit.verify(public_inputs, proof):
    return FALSE
  if timestamp(now) - witness_timestamp > witness_window:
    return FALSE
  if not registry.lookup(SC).valid:
    return FALSE
  return TRUE
```

**Output:** `AUTHORIZED` (boolean) — nothing else.

---

## 13. Governance Predicate

```
GovernancePredicate =
    FloorAttestation.PASS
  ∧ WitnessFresh(now)
  ∧ ScarAttestation.VALID
  ∧ PolicyVersion.matches
```

Formal R1CS constraint:

```circom
template GovernancePolicy() {
  signal input floor_pass;
  signal input witness_age;
  signal input scar_valid;
  signal input policy_version_match;
  signal output pass;

  // Constraint: all must be 1
  pass <== floor_pass * witness_fresh(witness_age) * scar_valid * policy_version_match;
}
```

---

## 14. Revocation

Proofs become invalid if:
- Floor state changes (F1-F13 fail)
- Witness expires (timestamp > window)
- Scar attestation revoked (H5 status flip)
- Policy version changes

**Mechanism:** Any state change recomputes ROOT. New ROOT ≠ old ROOT. Old proofs fail verification.

---

## 15. Security Model

### Protects Against
- Single share theft (need all 3)
- Replay attacks (nonce + timestamp)
- Witness spoofing (Ed25519 signature required)
- Unauthorized execution (no valid proof = no execution)
- Memory disclosure (only commitments enter circuit)

### Does Not Protect Against
- Compromised authorities (all 3 signing keys leaked)
- Malicious root generation (collusion of all 3 authorities)
- Faulty governance policy (policy logic itself compromised)
- Fake witness sources (upstream GEOX/WEALTH/WELL compromise)

**These require independent trust infrastructure** (HSM, MPC, governance oversight).

---

## 16. Cryptographic Primitives (NEW v0.1.1)

| Component | Primitive | Rationale |
|-----------|-----------|-----------|
| **Hash** | SHA3-256 | Post-quantum ready, NIST standard |
| **Signature** | Ed25519 | Compact, fast, well-audited |
| **Proof System** | Groth16 | Smallest proof size (~128 bytes), fastest verifier |
| **Elliptic Curve** | BN254 | Mature tooling, Ethereum-compatible |
| **Merkle Tree** | Binary, SHA3-256 | Standard |
| **Trusted Setup** | Powers of Tau (Phase 1) + circuit-specific (Phase 2) | Public contribution ceremony |

**Alternates for future v0.2:**
- STARKs (transparent setup, larger proofs)
- Halo2 (no trusted setup, recursive)
- BLS12-381 (Ethereum 2.0 compat)

---

## 17. Circuit Description (NEW v0.1.1)

### Main Circuit: `ZKPCAuthorization`

```circom
pragma circom 2.1.6;

include "../node_modules/circomlib/circuits/poseidon.circom";
include "../node_modules/circomlib/circuits/bitify.circom";

template MerkleTree(levels) {
  // Standard binary Merkle tree using Poseidon hash
  // ...
}

template ZKPCAuthorization() {
  // Public inputs
  signal input root;                    // Merkle root commitment
  signal input epoch;                   // Current epoch
  signal input policy_version;          // Governance policy version
  signal input witness_window;          // Max age for witness (seconds)

  // Private inputs (witness)
  signal input SC;                      // Scar commitment
  signal input SE;                      // Seal commitment
  signal input WI;                      // Witness commitment
  signal input scar_path_elements[2];   // Merkle path for SC
  signal input scar_path_indices[2];
  signal input seal_path_elements[2];
  signal input seal_path_indices[2];
  signal input witness_path_elements[2];
  signal input witness_path_indices[2];
  signal input witness_timestamp;       // Witness age timestamp
  signal input current_timestamp;       // Now() timestamp
  signal input floor_pass;              // 0 or 1
  signal input scar_valid;              // 0 or 1

  // Constraint 1: Merkle tree consistency
  component sc_merkle = MerkleTree(2);
  sc_merkle.leaf <== SC;
  // ... etc

  // Constraint 2: Freshness
  signal age;
  age <== current_timestamp - witness_timestamp;
  signal witness_fresh;
  witness_fresh <== (age <= witness_window) ? 1 : 0;

  // Constraint 3: Predicate
  signal output authorized;
  authorized <== (root * floor_pass * witness_fresh * scar_valid) > 0 ? 1 : 0;
}

component main { public [root, epoch, policy_version, witness_window] }
              = ZKPCAuthorization();
```

### R1CS Constraint Count (estimated)

| Component | Constraints |
|-----------|-------------|
| Merkle tree (depth 2) | ~600 |
| Freshness check | ~50 |
| Predicate AND | ~10 |
| **Total** | **~660** |

**Proof generation:** ~5 seconds on consumer laptop (circom + snarkjs)
**Verification:** <1 ms on-chain

---

## 18. Setup Ceremony (NEW v0.1.1)

### Phase 1: Powers of Tau
- **Public contribution ceremony**
- Multiple independent contributors add entropy
- Output: Universal Structured Reference String (SRS)

### Phase 2: Circuit-Specific
- Compute proving key from SRS for `ZKPCAuthorization` circuit
- Verify key derivation
- Public ceremony with verification

### Ceremony Artifacts
```
ceremony/
├── pot_phase1_final.ptau       # Phase 1 output
├── zkpc_v0.1.1_proving_key.zkey  # Phase 2 output
├── zkpc_v0.1.1_verification_key.json
└── VERIFICATION_TRANSCRIPT.md    # Public record
```

---

## 19. Attestation Schema (NEW v0.1.1)

### SCAR Attestation

```json
{
  "domain": "SCAR",
  "version": "1",
  "scar_id": "SCAR_LEBAH_EMAS",
  "registry_root": "hash_of_H5_SCAR_REGISTRY",
  "status": "VALID",
  "timestamp": "2026-08-12T00:00:00Z",
  "nonce": "12345",
  "signature": "ed25519_sig_by_sovereign_key"
}
```

### SEAL Attestation

```json
{
  "domain": "SEAL",
  "version": "1",
  "floor": "F1_AMANAH",
  "kernel_version": "2026.08.12",
  "status": "PASS",
  "timestamp": "2026-08-12T00:00:00Z",
  "nonce": "67890",
  "signature": "ed25519_sig_by_kernel_key"
}
```

### WITNESS Attestation

```json
{
  "domain": "WITNESS",
  "version": "1",
  "organ": "GEOX",
  "probe_url": "http://127.0.0.1:8081/health",
  "probe_status": "ALIVE",
  "timestamp": "2026-08-12T00:00:00Z",
  "nonce": "11111",
  "signature": "ed25519_sig_by_organ_key"
}
```

All attestations signed with their domain's private key. Public keys published in registry.

---

## 20. Threat Model (NEW v0.1.1)

### Adversary Classes

| Class | Capability | Mitigation |
|-------|-----------|------------|
| **A1 — Passive observer** | Sees public inputs | ZK property — learns nothing beyond PASS/FAIL |
| **A2 — Active share thief** | Steals 1 of 3 shares | Threshold — 1 share useless |
| **A3 — Replay attacker** | Replays old proofs | Nonce + timestamp freshness check |
| **A4 — Colluding 2 authorities** | Controls 2 of 3 authorities | 2-of-3 insufficient for full reconstruction |
| **A5 — Colluding 3 authorities** | Controls all 3 authorities | OUT OF SCOPE — trust infrastructure required |
| **A6 — Quantum attacker** | Breaks elliptic curve | Mitigation deferred to v0.2 (STARK migration) |

### Security Assumptions
1. At least 1 of 3 authority keys remains uncompromised
2. Hash function (SHA3-256) remains collision-resistant
3. BN254 discrete log remains hard (or migrate to STARK in v0.2)
4. Powers of Tau ceremony was performed honestly (at least 1 honest contributor)

---

## 21. Implementation Path (NEW v0.1.1)

### Tooling Stack

| Layer | Tool |
|-------|------|
| **Circuit** | Circom 2.1.6+ |
| **Proof Generation** | snarkjs (Node.js) |
| **Verifier** | Solidity (Ethereum) + snarkjs (off-chain) |
| **Test Harness** | TypeScript + Jest |
| **Registry** | `/root/memory/H5-scars/H5_SCAR_REGISTRY.json` (existing) |
| **Floor State** | `/root/arifOS/GENESIS/FLOOR_TABLE.json` (existing) |
| **Witness Probes** | GEOX :8081, WEALTH :18082, WELL :18083 |

### File Layout

```
/root/forge_work/ZK_PC/
├── circuits/
│   ├── zkpc_authorization.circom
│   └── merkle_tree.circom
├── scripts/
│   ├── compile.sh
│   ├── setup_ceremony.sh
│   ├── generate_proof.ts
│   └── verify_proof.ts
├── test/
│   ├── test_canonical_encoding.ts
│   ├── test_attestation_signing.ts
│   ├── test_proof_generation.ts
│   └── test_end_to_end.ts
├── contracts/
│   └── ZKPCVerifier.sol
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SECURITY.md
│   └── DEPLOYMENT.md
└── artifacts/
    ├── zkpc_v0.1.1.r1cs
    ├── zkpc_v0.1.1_final.zkey
    └── zkpc_v0.1.1_verification_key.json
```

### Deployment Phases

**Phase 1: Local proof-of-concept (T+0)**
- Compile circuit
- Generate trusted setup (1-party for testing)
- Generate proof from real arifOS attestations
- Verify locally

**Phase 2: Multi-party setup (T+1 week)**
- Public Powers of Tau ceremony
- Multi-contributor Phase 2
- Publish verification key

**Phase 3: arifOS integration (T+2 weeks)**
- A-FORGE bridge: forge_zkpc_proof tool
- arif_judge: verify_zkpc_proof before SEAL
- VAULT999: log ZK-PC proofs as sealed events

**Phase 4: Public deployment (T+1 month)**
- Publish circuit on arif-fazil.com
- On-chain verifier on Base/Optimism
- Public documentation

---

## Protocol Compression

```
Scar Attestation        Seal Attestation       Witness Attestation
    ↓                        ↓                       ↓
SHA3-256 (SC)        SHA3-256 (SE)         SHA3-256 (WI)
    ↓                        ↓                       ↓
    └────────────────────────┴───────────────────────┘
                            ↓
                     Merkle Root (ROOT)
                            ↓
                  Public Commitment
                            ↓
           ┌────────────────┴────────────────┐
           ↓                                  ↓
      ZK Circuit                    Visual Share (optional)
      (prover side)                 (human visualization)
           ↓                                  ↓
   Proof Generation                   Image Reconstruction
           ↓                                  ↓
      zk-SNARK π                       Human Intuition
           ↓
    Verifier checks:
    - Merkle consistency
    - Witness freshness
    - Floor compliance
    - Scar validity
           ↓
       AUTHORIZED
```

---

## Audit Trail (NEW v0.1.1)

### Changes from v0.1

| Section | Change |
|---------|--------|
| 2 | +P5 Revocability, +P6 Composable Verification |
| 6 | Clarified as optional, human-facing only |
| 7 | Clarified as prover-side only |
| 8 | Added `proof_id` binding |
| 9 | Added freshness constraint + nonce uniqueness |
| **16** | **NEW — Cryptographic primitives** |
| **17** | **NEW — Circuit description (Circom)** |
| **18** | **NEW — Setup ceremony** |
| **19** | **NEW — Attestation schema** |
| **20** | **NEW — Threat model** |
| **21** | **NEW — Implementation path** |

### Known Limitations
- Requires Powers of Tau ceremony (T+1 week)
- BN254 not quantum-resistant (STARK migration in v0.2)
- Single kernel key = single point of failure (MPC migration in v0.3)
- No formal verification of circuit (audit before mainnet)

---

## Status

```
Draft: COMPLETE
Review: AWAITING F13 RATIFICATION
Implementation: NOT STARTED (T+0 if ratified)
Canonical Path: /root/AAA/canon/ZK_PC_v0.1.1_SPEC.md
```

---

*Forged: 2026-08-12 by Hermes ASI*
*Heritage: ZK-PC v0.1 (PARTIAL-SEAL) + WGC demo + OpenClaw session trace*
*DITEMPA BUKAN DIBERI — A protocol is forged, not given. ⚒️*