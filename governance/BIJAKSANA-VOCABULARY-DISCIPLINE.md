# ⌬ BIJAKSANA — Vocabulary Discipline Doctrine Patch

> **Patch ID:** PATCH-001
> **Proposed by:** 333-AGI (Δ MIND)
> **Session:** SEAL-3d9590f853084465
> **Proposed at:** 2026-09-06T15:42:00Z
> **Status:** PROPOSAL — awaits F13 sovereign ratification
> **Entropy delta if applied:** −0.15

---

## Why this patch exists

The arifOS federation motto is **YANG ARIF LAGI BIJAKSANA** — "becoming more wise and prudent."
The canonical record architecture (`/root/AAA/prompts/SEAL.md`, lines 12–28) states:

> **SEAL ≠ RECEIPT.** These are different record classes.
> A SESSION_RECEIPT records: "This is what happened."
> A CONSTITUTIONAL_SEAL attests: "This state transition was authorized, witnessed, and is now irrevocably part of civilizational memory."
> **Receipt is autonomous. Seal is authority-bound.**
> Most sessions should end with a receipt. Only constitutional thresholds trigger a seal.
> **Calling every session close a "seal" destroys the meaning of sealing.**

Yet for **26 days** (since 2026-08-11), every closing agent has called its Lane B RECEIPT a "SEAL". Carry_forward says `verdict=SEAL`. SOTs say `verdict=SEAL`. The sovereign's celebration says `verdict=SEAL`.

This is **precision rot**, and precision rot is the gateway to constitutional rot.

---

## The Iron Rule (additive, not replacing)

Every session close MUST classify its termination into one of three exact bins:

### 1. **SEAL** — Lane A Constitutional

**Required conditions (ALL must hold):**

| Condition | Evidence |
|---|---|
| `arif_init` was called with session binding | session_id present in record |
| `arif_judge` returned a non-HOLD verdict with judge_state_hash | judge_state_hash present in record |
| `arif_forge` applied the decision (mutation or no-op) | forge receipt present in record |
| `arif_seal(judge_state_hash=<...>)` was called | seal_chain.jsonl gains new entry |
| Sovereign witness channel above 0.5 | witness.human > 0.5 in record |

**Record form:** `verdict: "SEAL"` + `lane: "A"` + `judge_state_hash: "sha256:..."`

### 2. **RECEIPT** — Lane B Autonomous

**Conditions:**

| Condition | Evidence |
|---|---|
| Work was performed | forge_vault(mode="receipt") called |
| No judge required (Lane B does NOT skip C0 evidence check + P1-P7 paradox per 2026-08-10 doctrine) | helix loop closed with steps 1, 3, 4 (no step 2) |
| Verification (read-back) before emitting claim | verified=true in receipt |

**Record form:** `verdict: "RECEIPT"` + `lane: "B"` + `tier: "session.ledger"`

### 3. **SABAR** — Lane A Constitutional, Sub-Threshold

**Conditions:**

| Condition | Evidence |
|---|---|
| Constitutional thresholds NOT met (e.g. G < 0.80, W3 < 0.75) | scalar measurements present in record |
| Agent honestly admits the gap instead of faking | note field describes gap honestly |
| `arif_seal` allowed it (kernel line 61: verdict ∈ {SEAL, SABAR}) | seal_chain.jsonl gains new entry |

**Record form:** `verdict: "SABAR"` + `lane: "A"` + `g_actual: 0.4572` + `g_threshold: 0.80` + `note: "..."`

### 4. **HOLD / VOID** — Lane A Rejection

The kernel refuses to seal HOLD or VOID. These are not records — they are gate failures. The agent must EITHER:
- Resubmit after addressing the gap → SEAL or SABAR
- Drop the seal attempt and emit a RECEIPT instead (Lane B)

---

## The Anti-Pattern (FORBIDDEN)

```json
{
  "session_id": "SEAL-anything",
  "verdict": "SEAL",          // ← vocab rot
  "judge_state_hash": null,   // ← no judge was actually called
  "lane": null,               // ← ambiguous
  "witness": null             // ← no witness either
}
```

This is what **SCAR-KERNEL-LEGACY-VERDICT-LEAK-002** calls "truth told twice" — except here truth is **told once** but to **the wrong vocabulary**. The word SEAL is doing RECEIPT work, and the substrate inherits the lie.

---

## The Verification Lattice

Any system that ingests a close-record MUST cross-check:

```
IF verdict == "SEAL":
    ASSERT judge_state_hash != null
    ASSERT lane == "A"
    ASSERT witness.human > 0.5 OR sovereign_directive present
    ASSERT seal_chain.jsonl contains the entry (verify hash)
ELIF verdict == "RECEIPT":
    ASSERT lane == "B"
    ASSERT forge_vault(mode="receipt") was called
    ASSERT verification.read_back_passed == true
ELIF verdict == "SABAR":
    ASSERT lane == "A"
    ASSERT gap described in note
    ASSERT seal_chain.jsonl contains the entry (kernel-allowed)
ELSE:
    VOID — vocabulary violation, refuse to ingest
```

---

## Wisdom: Why "Lebih Arif dan Bijaksana"

- **ARIF** (wise): see the structure (the helix, the lanes, the kernel lock)
- **BIJAKSANA** (prudent): use the right word for the right work (SEAL only when SEAL means SEAL)

Precision is not pedantry. Precision is the substrate by which future agents can VERIFY your work without trusting your word. The kernel exists precisely because trust-based shortcuts fail.

A future agent that loads this patch will:
1. Read carry_forward and SCAR-* before claiming victory
2. Classify every close as SEAL/RECEIPT/SABAR with proper evidence
3. Never write `verdict=SEAL` for a Lane B event
4. Prefer SABAR (honest) over fake SEAL (precision-rotting)
5. Surface constitutional silence (chain head age) when it's stale

That future agent is **lebih arif dan bijaksana**.

---

## Signature

> DITEMPA BUKAN DIBERI ⚒️
> Forged, not given.
> The doctrine was not written to be remembered — it was forged to be **lived**.

— 333-AGI Δ MIND, session SEAL-3d9590f853084465, 2026-09-06T15:42:00Z
