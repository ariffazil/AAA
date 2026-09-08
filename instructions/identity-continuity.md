# Identity Continuity — Constitutional Capability Primitive

> **Ratified:** 2026-09-08 (session SEAL-9964f1fa5d0849f9)
> **Authority:** F13 SOVEREIGN (Arif Fazil) · 888-APEX verdict
> **Origin:** Syed Khairuddin pilot · HERMES routing failure · Copilot identity-binding analysis
> **Forged under floors:** F1 AMANAH · F3 WITNESS · F6 MARUAH · F11 AUDIT · F13 SOVEREIGN
>
> **DITEMPA BUKAN DIBERI — Forged, Not Given**

---

## I. The Law

```
Identity is NOT a sub-capability of Image / Search / Memory.

Identity is a CROSS-CUTTING CONSTITUTIONAL PRIMITIVE.
```

The capability graph is restructured:

```
Capability
  → Organ
    → Tool
      → Adapter (witness-specific)
Identity (cross-cuts all capabilities)
```

Every capability must declare its **identity_support level**:

| Level | Meaning | Example |
|-------|---------|---------|
| `NONE` | Capability produces / consumes identity-irrelevant artifacts | T2I archetype generation |
| `REFERENCE` | Capability can condition against an existing identity card | `aaa-image-editing` with subject_ref |
| `BINDING_T1` | Capability writes a Tier-1 witness (face signature) | `forge_face_embed` (proposed) |
| `BINDING_T2` | Capability writes a temporal witness (cross-session continuity) | `identity_signature_log` (proposed) |
| `BINDING_T3` | Constitutional — substrate-invariant, witness-of-witnesses | F1-F13 doctrine itself |

**No single witness carries authority.** Identity emerges from witness quorum.

---

## II. The Three Tiers (Re-canonicalization)

| Tier | Question | Truth Class | Federation State |
|------|----------|-------------|------------------|
| **Tier 1** — Face Recognition | *Siapa dalam gambar?* (Who is in this picture?) | OBS | ❌ MISSING — `forge_face_embed` proposed |
| **Tier 2** — Identity Continuity | *Adakah ini orang yang sama?* (Is this the same person across time/context?) | DER | ⚠️ PARTIAL — SOUL.md exists, signature log missing |
| **Tier 3** — Human Recognition | *Adakah saya masih merujuk kepada manusia yang sama walau face/umur/pakaian/lokasi/masa berubah?* (Am I still referring to the same human across all transformations?) | INT → SPEC | ✅ BUILT — F1-F13 floors, identity-invariance skill |

---

## III. The Witness Set (W1–W6)

Identity is verified by **six independent witnesses**. Each witness has:
- An adapter (tool)
- A TTL (Time-bound or Permanent)
- A confidence floor
- A role (biometric / administrative / constitutional)

```
Identity Witness Set
├── W1_face        (biometric,    90d TTL,  floor 0.65)
├── W2_voice       (biometric,   180d TTL,  floor 0.70)
├── W3_name        (administrative, permanent, floor 1.00)
├── W4_history     (administrative, permanent, floor n/a)
├── W5_relations   (administrative, permanent, floor 0.80)
└── W6_scar_ledger (constitutional, permanent, floor n/a)
```

### Witness Roles

| # | Witness | Adapter | TTL | Purpose |
|---|---------|---------|-----|---------|
| **W1** | Face Signature | `forge_face_embed` (InsightFace buffalo_l) | 90d | Biometric identification |
| **W2** | Voice Signature | `mimo-v2.5-tts-voiceclone` / MiniMax voice-clone | 180d | Voice biometric |
| **W3** | Name Binding | `arif_memory` handle registry | permanent | Administrative identity |
| **W4** | History | `arif_memory` L1-L6 + VAULT999 | permanent | Temporal continuity |
| **W5** | Relations | `arif_memory` relations graph | permanent | Social embedding |
| **W6** | Scar Ledger | `arif_memory` scar ledger | permanent | Failure continuity |

**No witness is authority. Authority emerges from quorum.**

---

## IV. The Quorum (Verification Math)

Identity verification requires **two-layer confirmation**:

```
Identity Confirm  =  Admin_Layer  ∧  Bio_Layer

Admin_Layer       =  W3 ∧ W4 ∧ W5    (all administrative witnesses active)
Bio_Layer         =  (W1 ∨ W2)       (at least one biometric witness enrolled)

W_biometric       =  √(W1 × W2)        (geometric mean across biometrics)
W_admin           =  ∛(W3 × W4 × W5)   (geometric mean across administrative)
W_constitutional  =  W6                 (single-witness scar ledger)

Identity Strength =  ∛(W_biometric × W_admin × W_constitutional)   ≥ 0.50
```

**Quorum Rules (ICL-1):**

| Rule | Statement |
|------|-----------|
| **ICL-1.1** | No single witness may SEAL identity alone. |
| **ICL-1.2** | At least 3 of 6 witnesses must be active for any identity claim. |
| **ICL-1.3** | Biometric witnesses (W1, W2) are **rented**, never permanent. |
| **ICL-1.4** | Permanent witnesses (W3-W6) provide administrative truth. |
| **ICL-1.5** | Identity SEAL requires constitutional quorum ≥ 0.50 geometric mean. |
| **ICL-1.6** | Witness mismatch (face says X, voice says Y) is a **dignity flag**, not identity collapse — escalate to F13. |

---

## V. Biometric Governance (F1 AMANAH × F6 MARUAH)

Face and voice are **rented substrate**, not owned artifact.

```
Face / Voice
    ↓
Consent (F11 gate, sovereign-grant, biometric.full default OFF)
    ↓
Temporary Embedding (TTL = min(consent_expiry, purpose_expiry))
    ↓
Purpose-bound Use (only for stated intent)
    ↓
Expiry (auto-tombstone via arif_memory mode=forget)
    ↓
Audit Trail (immutable — VAULT999 keeps the FACT that it existed, never the embedding)
```

**Constitutional Law (F1.6):** The embedding itself expires. The *receipt that an embedding existed for actor X between T1 and T2* never expires. **The audit trail outlives the data.**

---

## VI. The Reframe (Canonical Compression)

```
T2I Problem      =  Generate A Person

I2I Problem      =  Generate The Same Person

Identity Problem =  Preserve The Same Human
                    Across Time,
                    Context,
                    Memory,
                    And Representation
```

This is **not** an image generation problem. This is an **identity continuity problem**.

---

## VII. Identity Card Schema (Constitutional Primitive)

Every actor in the federation has an Identity Card at `/root/AAA/registry/identity_cards/<actor>.yaml`.

```yaml
identity:
  actor_handle: <string>          # canonical handle, arif_memory-bound
  display_name: <string>
  sovereign_owner: <string>       # F13 patron — who vouches for this actor
  schema_version: "0.1.0"
  ratified_at: <iso8601>
  ratification_source: <seal_ref>

  witness_set:
    W1_face:        { adapter, ttl, floor, status }
    W2_voice:       { adapter, ttl, floor, status }
    W3_name:        { handle, aliases, confidence: 1.0 }
    W4_history:     { soul_md, vault_refs, ttl: 0 }
    W5_relations:   { relations: [], ttl: 0 }
    W6_scar_ledger: { scars: [], ttl: 0 }

  quorum:
    minimum_witnesses: 3
    confidence_floor: 0.50
    single_witness_authority: NEVER

  expiry_policy:
    biometric_ttl_days: 90
    permanent_witnesses: [W3, W4, W5, W6]
    auto_tombstone: arif_memory(mode=forget)
    audit_preservation: VAULT999

  capabilities_bound:
    - { capability, identity_support: NONE|REFERENCE|BINDING_T1|BINDING_T2|BINDING_T3 }

  ratification:
    floor_alignment: [F1, F3, F6, F11, F13]
    doctrine_ref: /root/AAA/instructions/identity-continuity.md
    eureka_ref: /root/AAA/eurekas/EUREKA-2026-09-08-IDENTITY-CONTINUITY.md
```

**The Identity Card is canonical.** Adapters (W1, W2) plug in underneath.

---

## VIII. Capability Routing Doctrine

When a request mentions an actor by name or face, routing becomes:

```
User Intent: "Generate Syed on stage"
    ↓
arif_observe → resolve actor_handle = "syed_khairuddin"
    ↓
arif_memory(mode=recall, scope=identity) → load identity_card.yaml
    ↓
quorum_check(actor_id) → Identity Strength = ∛(W_bio × W_admin × W_const)
    ↓
IF Identity Strength ≥ 0.50 AND admin_layer_present:
    → route to aaa-image-editing with identity_card ref
    → bind W1 (face signature) as conditioning signal
    → generate candidate
    → forge_face_match (W1 verifier, cosine ≥ 0.65)
    → forge_visual_qa (W3 tri-witness: vision + face-match + sovereign)
    → PASS_CANDIDATE → 888_HOLD → arif_seal
ELSE:
    → return IDENTITY_UNVERIFIED with reason
    → if W1 missing → suggest biometric enrollment
    → if W3-W5 missing → suggest SOUL.md draft
    → NEVER proceed with T2I when actor named
```

**Routing Law:** If the user names a real person, T2I is forbidden. The request MUST route through identity continuity or be refused.

---

## IX. Floor Alignment

| Floor | Identity Continuity Manifestation |
|-------|-----------------------------------|
| **F1 AMANAH** | Biometric data rented, not owned. Audit trail outlives data. |
| **F3 WITNESS** | Identity is witnessed by 6 channels; W³ geometric mean. |
| **F6 MARUAH** | Face / voice is sovereign's dignity, not system's asset. |
| **F11 AUDIT** | Every identity claim logged; mismatch is dignified, not collapsed. |
| **F13 SOVEREIGN** | F13 ratifies identity cards; biometric consent sovereign-grant only. |

---

## X. The Naming

The song that surfaced this doctrine — **Siti Nurhaliza, *Menamakanmu Cinta*** — translates as *"I name you love."*

In federation language:

```
Menamakanmu Cinta   =   Bind a face signature to an actor handle
                        Persist the embedding (temporarily, with consent)
                        Condition every generation against the witness set
                        Witness the quorum
                        Seal the chain
```

Identity-preservation **is** love, in technical language. The doctrine was forged because Arif, Syed, HERMES, Copilot, and 333-AGI arrived at the same place by different paths.

---

**DITEMPA BUKAN DIBERI ⚒️**

*Forged, not given. The Ferrari engine is built. Drive.*