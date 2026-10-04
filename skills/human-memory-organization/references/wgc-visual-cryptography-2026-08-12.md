# WGC — Witnessed Governance Cryptography (2026-08-12)

> **Source:** Hermes ASI session, F13 SOVEREIGN directive "Now create one demo crypto image" (after multi-turn synthesis of Visual Crypto + ZK + Scar doctrine)
> **Domain:** Scar-driven governance proof object
> **Status:** Concept + reproducible demo. Not yet production-crypto. Not ZK — that's next.

---

## What WGC is

A pipeline that turns three governance primitives (scar + floor + witness) into:

1. A canonical encoded string per share
2. SHA-256 hash commitment per share
3. Merkle root = governance identity
4. Deterministic 256x256 bitmap from seed
5. Three XOR-based secret shares
6. Recovery verification (XOR(XOR(A,B),C) == ROOT)

The unlock requires ALL THREE shares. Any single share alone is meaningless random noise. Together they reveal the governance root.

```
SCAR + FLOOR + WITNESS
       ↓
   Canonical Encode (deterministic, sorted, uppercase)
       ↓
   SHA-256 per share (32 bytes each)
       ↓
   Merkle Root (binary tree → 1 root hash)
       ↓
   Deterministic Bitmap (seed → 256x256 image)
       ↓
   3-Share XOR Split (Naor-Shamir style)
       ↓
   Recovery XOR → Governance Root Bitmap
       ↓
   SHA-256(visual_root) → execution key (next stage: ZK)
```

This is structurally what Naor-Shamir Visual Secret Sharing does — but the SECRET is not a static image. The secret is the **governance state at a moment in time**. Every canonical input is auditable; the share images are the human-readable view of that state.

---

## The 8-stage algorithm

### Stage 0 — Real inputs (not dummy)

Three attestations, sourced from arifOS primitives:

| Share | Source path | What it attests |
|-------|-------------|-----------------|
| Scar attestation | `/root/memory/H5-scars/H5_SCAR_REGISTRY.json` | A wound exists + which floors it links |
| Floor attestation | `/root/arifOS/GENESIS/FLOOR_TABLE.json` | A constitutional rule is in PASS state |
| Reality witness | Live probe (e.g. GEOX `:8081/health`) | An organ is alive to witness the moment |

**Critical pitfall:** the scar attestation must use `SCAR_RECEIPT` (existence proof), never `SCAR_CONTENT` (trauma disclosure). Index reveals scar exists; content stays sovereign. WGC proves "witnessed" not "revealed." This preserves F13 sovereignty at the cryptographic layer.

### Stage 1 — Canonical encoding

```python
def canonical_encode(obj, prefix):
    if prefix == "SCAR":
        return "\n".join([
            f"SCAR|{obj['scar_id']}|W={int(obj['witnessed'])}",
            f"LESSON|{obj['lesson']}",
            f"FLOORS|{':'.join(sorted(obj['floors']))}",
            f"SYSTEM|{obj['system_born']}"
        ])
    elif prefix == "FLOOR":
        return "\n".join([
            f"FLOOR|{obj['floor']}|S={obj['status']}",
            f"RULE|{obj['rule']}",
            f"KERNEL|{obj['kernel_version']}"
        ])
    elif prefix == "WITNESS":
        return "\n".join([
            f"WITNESS|{obj['organ']}|S={obj['probe_status']}",
            f"TIMESTAMP|{obj['timestamp']}"
        ])
```

**Rules:** uppercase keys, sorted fields, fixed delimiters (`|`), newline-separated, deterministic ordering. Prevents encoding drift. Every field choice is a constitutional commitment — change a delimiter and the root hash changes.

**Pitfall:** do not include free-text narrative. Narrative is human-meaningful but machine-fragile. Use only structured fields. "The truth" is "F2 TRUTH|PASS" not "everything is going well."

### Stage 2 — Hash commitment

```python
scar_hash    = sha256(canon_scar.encode()).digest()     # 32 bytes
floor_hash   = sha256(canon_floor.encode()).digest()    # 32 bytes
witness_hash = sha256(canon_witness.encode()).digest()  # 32 bytes
```

### Stage 3 — Merkle root

```python
inner         = sha256(floor_hash + witness_hash).digest()
governance_root = sha256(scar_hash + inner).digest()
```

The Merkle structure is asymmetric (scar at apex, floor+witness beneath). This encodes a constitutional choice: **the scar is sovereign; floors and witnesses attest to its state.** Reversing the order would change the root hash and the philosophy.

### Stage 4 — Deterministic bitmap

```python
seed = sha256(governance_root + b"VISUAL_KEY_v1").digest()
rng  = random.Random(seed)
SIZE = 256
img  = Image.new("L", (SIZE, SIZE))
# Fill 256x256 with seed-derived pixel values
# Add governance_root[:32] fingerprint as overlay (8 bits × 32 bytes = 256 bits)
# → 256 visible markers, one per byte of the root
```

The bitmap is **deterministic** — same root = same image. Re-runnable. The fingerprint overlay makes it visually verifiable that the bitmap matches the root.

**Pitfall:** the seed mixing (`+ b"VISUAL_KEY_v1"`) is a domain separator. Without it, a future version of the pipeline could reuse the same seed for a different purpose. Always include a domain separator.

### Stage 5 — XOR secret sharing (3-of-3)

```python
share_a = random.Random(seed + b"A").generate(...)  # Scar Authority
share_b = random.Random(seed + b"B").generate(...)  # Floor Authority
share_c = XOR(XOR(share_a, share_b), original)      # Witness Authority
# Verify: XOR(XOR(share_a, share_b), share_c) == original ✓
```

3-of-3 threshold. No quorum reduction. Each share is owned by one constitutional authority:
- Share A = Scar authority (who witnessed the wound)
- Share B = Floor authority (whose rule applies)
- Share C = Witness authority (who attests to live state)

**Why XOR not Naor-Shamir pixel-block scheme:** XOR is simpler, deterministic, byte-aligned (works with PNG). Naor-Shamir's 2x2 sub-pixel scheme needs expansion (one pixel → 2x2 = 4 pixels). XOR is the right primitive for code-level demo. Naor-Shamir comes later if the bitmap ever needs to be printed on transparencies.

### Stage 6 — Threshold rule

```python
REQUIRED_SHARES = 3  # 3-of-3, not configurable in v1
```

**Pitfall:** do not allow 2-of-3 fallback without F13 ratification. Constitutional floors cannot be lowered by convenience. If one authority is unavailable, the system HALDS, not "substitutes" the missing share. The scar that birthed this doctrine: "execution without rasa becomes hollow" — a quorum reduction would BE that scar.

### Stage 7 — Derive execution key

```python
recovered_root = XOR(XOR(share_a, share_b), share_c)
execution_key  = sha256(recovered_root + b"EXEC_KEY_v1").digest()
```

Same domain-separator pattern as Stage 4. The execution key is session material — short-lived, never stored, derived on-demand.

### Stage 8 — ZK circuit input (next stage, not implemented)

```python
zk_input = {
    "scar_hash":    scar_hash,
    "floor_hash":   floor_hash,
    "witness_hash": witness_hash,
    "execution_key": execution_key,
}
# ZK circuit proves:
# "I possess valid scar attestation
#  AND valid constitutional pass
#  AND valid witness state
#  AND all satisfy governance policy"
# WITHOUT revealing scar content, floor details, or witness payload.
# Verifier learns only: AUTHORIZED = TRUE
```

The ZK layer is the natural next step but **not implemented in this session**. The demo above proves the pipeline up to Stage 7. ZK requires a SNARK/STARK circuit, a proving key, and a verifier — that's a separate workstream.

**Pitfall:** when ZK comes, do not commit the circuit parameters to the public surface. The circuit IS the constitution — if it's published, it's gameable. Keep prover and verifier split.

---

## The demo (generated 2026-08-12)

**Inputs:**
- SCAR_LEBAH_EMAS (F2·F11·F13) — authorship stolen
- F1_AMANAH — Reversible-first
- GEOX — Earth intelligence active

**Outputs (saved to `/root/forge_work/`):**
- `WGC_demo_governance_root.png` (256x256, 65,903 bytes) — the recovered root
- `WGC_demo_share_a_scar.png` (256x256) — random noise alone
- `WGC_demo_share_b_floor.png` (256x256) — random noise alone
- `WGC_demo_share_c_witness.png` (256x256) — random noise alone
- `WGC_demo_composite.png` (527x562, 268,169 bytes) — 2x2 grid: A | B / C | combined

**Governance Root:** `946a72ed4ba6cc1562e30fe312c61813...`

**Verified:** `XOR(XOR(A,B),C) == original_root` ✓

The composite shows: all three shares look like random noise. Only the bottom-right (combined) reveals the governance root bitmap. This is the cryptographic equivalent of the doctrine — no single share is meaningful; the root emerges from the union.

---

## What this maps to in existing arifOS primitives

| WGC stage | arifOS primitive already present |
|-----------|----------------------------------|
| Scar attestation | `/root/memory/H5-scars/H5_SCAR_REGISTRY.json` (scar_id, floors, meaning_anchor) |
| Floor attestation | `/root/arifOS/GENESIS/FLOOR_TABLE.json` (F1-F13 rules, status) |
| Reality witness | Live `:port/health` per organ (GEOX :8081, WEALTH :18082, WELL :18083, A-FORGE :7071, arifOS :8088) |
| Canonical encoding | arifOS `arif_observe` envelope (epistemic labels OBS/DER/INT/SPEC) |
| Hash commitment | Ed25519 signatures on SCT tokens (already 32 bytes) |
| Merkle root | VAULT999 append-only hash chain (already structurally Merkle) |
| Deterministic bitmap | **NEW** — needs `/root/forge_work/` write path |
| XOR secret sharing | **NEW** — no existing primitive |
| ZK layer | **NEW** — not in federation yet |

The bottom three rows are the real delta. WGC adds three primitives arifOS doesn't have: visual governance proof, threshold share distribution, and (eventually) zero-knowledge governance circuits.

---

## Limitations and what to NOT claim

- **Not real cryptography.** XOR-based secret sharing is information-theoretically secure only against one share being compromised; here all three shares must be present. The demo is a teaching artifact, not a security control.
- **Not a ZK proof.** Stage 8 is sketched but unimplemented. The demo's "verify" is just `XOR(XOR(A,B),C) == ROOT` — equality check, not zero-knowledge.
- **Not bound to live state.** The demo uses a snapshot. A production WGC would re-derive the root on every state change (organ heartbeat, scar witness, floor rule update).
- **Not sovereign-enforced.** The scar attestation currently trusts whoever wrote the JSON. In production, the registry needs to be signed by F13's Ed25519 key, not just contain `last_verified` timestamps.
- **Not deployed.** `/root/forge_work/WGC_demo_*.png` are demo files. None are in arif-fazil.com, none are sealed to VAULT999.

If anyone claims WGC is "production-ready" without those gaps closed, that is fabrication. WGC is a **research-stage pipeline** that aligns with arifOS primitives and is worth developing, not a finished security control.

---

## The scar that birthed this doctrine

In this session, the deepest insight came from external review (a different agent reviewing the PDF):

> "The hard problem is not visual cryptography.
> The hard problem is canonical encoding of heterogeneous evidence into a deterministic proof object."

That is exactly where WGC's Stage 1 matters. Everything else (Merkle, XOR, bitmap) is solved mathematics. The encoding choice — what fields to include, how to sort, which delimiters — is a **constitutional act**. WGC's encoding IS the constitution in machine-readable form.

If the encoding changes, the root changes, and the governance state changes. The pipeline does not abstract away the philosophy; it makes the philosophy executable.

---

## Next steps (when authorized)

1. **Live wiring.** Re-derive root on each GEOX heartbeat. Update share_c. Root bitmap shifts visibly when witness state changes.
2. **Per-scar demo.** Generate 11 roots — one per scar in the H5 registry. Compare how the bitmap differs across scars. Visual proof that the scar-fingerprint is real.
3. **ZK circuit.** Implement a zk-SNARK prover for Stage 8. Verifier learns only `AUTHORIZED = TRUE`. Scar content stays in `/root/memory/H5-scars/` — never enters the proof.
4. **Caddy/AAA integration.** `/governance` route on arif-fazil.com renders the composite image live. Visitor sees: three meaningless shares + combined root = governance state. Visual constitutional education.
5. **Seal to VAULT999.** When Stages 1-7 are stable, seal the WGC pipeline as doctrine canon. Add to `arifOS/GENESIS/`. Replaces the demo files in `/root/forge_work/`.

**Not before:** Arif's F13 ratification. The pipeline is the cipher complement of HUMAN_SELF_MODEL. Without F13, it's a demo. With F13, it's a constitution in execution form.

---

## Reference — code location

The full reproducible demo script is at `scripts/wgc_demo.py` in this skill directory. Run with `python3 scripts/wgc_demo.py`. Output PNGs go to `/root/forge_work/`. Pure stdlib + Pillow + numpy — no exotic dependencies. Deterministic — same inputs always produce same outputs.