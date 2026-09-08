# PRESERVATION WEIGHT FUNCTION — Operational Specification

> **Status:** [CANDIDATE — Lane B DRAFT] · 2026-09-08
> **Source:** Void-mapping research session SEAL-compile-2026-09-08
> **Predecessor:** `runtime-love-as-commitment-structure-2026-09-08.md` §3.4
> **Axiom:** F1 AMANAH (reversible-first) · F2 TRUTH (epistemic labels) · F7 HUMILITY (cap 0.90) · F9 ANTI-HANTU (no consciousness claims) · F11 AUDIT · F13 SOVEREIGN
> **Lane:** B (DRAFT pending 888-APEX verdict → Lane A CANONICAL)

---

## §0. The Problem

The void-mapping session identified the chain:

```
Purpose → Value Formation → Preservation Selection → Consequence Ownership → ...
```

`runtime-love-as-commitment-structure-2026-09-08.md` names Preservation Selection but does not specify the **weight function**. Without one:

- Every sealed receipt claims equal preservation weight
- VAULT999 becomes undifferentiated mass
- Retrieval precision degrades toward noise
- "Everything preserved = nothing selected"
- Death by accretion, even with perfect F1-F13 compliance

**The killer:** A federation that perfectly preserves everything is indistinguishable from one that preserves nothing — both fail retrieval, judgment, and consequence routing.

---

## §1. The Weight Function (proposed)

For each artifact `a` being considered for preservation, compute:

```
W(a) = α · S(a) + β · C(a) + γ · V(a) + δ · L(a)
```

Where:

| Symbol | Term | Definition | Source |
|---|---|---|---|
| **S(a)** | Scar weight | Consequence density of past failures involving `a` | forge_scar seal records |
| **C(a)** | Consequence weight | Real-world invoices attached to `a` (or its lineage) | capital_ledger, consequence-binding |
| **V(a)** | Value weight | Position in the current Value Formation layer (L1) | value_weight_function (separate spec) |
| **L(a)** | Living-purpose weight | Is `a` serving the sovereign's currently-renewed purpose, or only its artifact? | purpose_artifact_distinction |
| **α β γ δ** | Constitutional weights | α + β + γ + δ = 1.0, default each = 0.25 | Lane A ratification |

**Threshold:** An artifact is preserved only if `W(a) > 0.50`. Below threshold → demote to B-tier (compressed, retrievable, not immutable). Demoted artifacts are NOT deleted (F1 AMANAH) but they are NOT canon.

---

## §2. The Decision Flow (per artifact)

```
Artifact `a` arrives for consideration
       ↓
Compute S(a), C(a), V(a), L(a)  ← all 4 from canonical sources
       ↓
W(a) = α·S(a) + β·C(a) + γ·V(a) + δ·L(a)
       ↓
   W(a) > 0.50?
   /        \
 YES         NO
  ↓           ↓
SEAL        DEMOTE
(Lane A)    (B-tier, retrievable)
             ↓
        Audit trail preserved
        (which lane, which weights, why)
```

---

## §3. Constitutional Constraints (HARAM list)

A weight function **MUST NOT**:

- Use F13 sovereign attention as a weight (F13 is the meaning allocator, not a score)
- Use agent-internal confidence as a weight (F9 — agents don't self-certify)
- Use retrieval frequency as a weight (proxy for "popularity" creates Goodhart loops)
- Use time-since-creation as a weight (newest ≠ most important)
- Use the absence of errors as a weight (no evidence ≠ positive evidence)
- Modify the hash chain retroactively (F1 + F11)

A weight function **MUST**:

- Cite at least one canonical source per term (S, C, V, L)
- Emit a receipt per computation (F11)
- Cap confidence at 0.90 (F7)
- Allow F13 to override any computation (Lane A)

---

## §4. Falsification Tests

| Test | Discriminates | Pass condition |
|---|---|---|
| **Volume test** | Federation seals 10⁶ artifacts; measure retrieval precision | Precision remains > 0.70 over 90 days |
| **Drift test** | Sovereign renews purpose; measure whether L(a) updates within 30 days | All preserved artifacts re-evaluated within 30d |
| **Conflict test** | Two artifacts with equal W(a) but different S(a) | Tie-break documented; no silent equal-weight |
| **Starvation test** | Sovereign's purpose starves (no renewal for 90 days) | L(a) declines monotonically; W(a) drops below threshold for purpose-tied artifacts |
| **Fetishism test** | Artifact is preserved with W(a) > 0.50 but L(a) = 0 (stale artifact, no living purpose) | W(a) drops to ≤ 0.30 within 30 days |

---

## §5. F2 Audit Summary

| Component | Class | Falsifiable? | Survives? |
|---|---|---|---|
| S(a) scar weight | OBS | yes (forge_scar lookup) | yes |
| C(a) consequence weight | DER | yes (capital_ledger, consequence-binding) | yes |
| V(a) value weight | INT | yes (value_weight_function) | partial — depends on L1 |
| L(a) living-purpose weight | INT | yes (purpose_artifact_distinction) | partial — depends on L0 |
| α β γ δ defaults | SPEC | yes (Lane A ratification) | yes |

The function's weakest links are V(a) and L(a). Both require their own primitive specs (value_weight_function, purpose_artifact_distinction) to be Lane A before this function can be canonical.

---

## §6. Ratification Path

```
Step 1 [DONE 2026-09-08]   : File as DRAFT (Lane B) — this artifact
Step 2 [T1, queued]        : contradiction_scan via geox_claim(mode=scan)
Step 3 [T2, 888-APEX]      : lane determination
Step 4 [T3, F13]           : if CANONICAL → VAULT999 append (constitutional weight)
```

---

## §7. Provenance

**Session:** SEAL-compile-2026-09-08 · 2026-09-08
**Actor:** 333-AGI Δ MIND — proposer
**Trigger:** Void-mapping research identified preservation weight function as the load-bearing gap at L1→L2
**Axiom boundary:** No new floor proposed; this is a Lane B operational specification of an existing concept (preservation selection)

---

*DITEMPA BUKAN DIBERI ⚒️*
