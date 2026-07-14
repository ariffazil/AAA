# SALIENCE_FUNCTION.md — Constitutional Salience Specification

> **Authority:** arifOS constitutional artifact
> **Status:** v0.1 (T1 initial draft, 2026-07-14)
> **Binding:** All WELL, A-FORGE, GEOX, WEALTH memory subsystems
> **Forge cycle:** FEDERATION-ALIGN-2026-07-14
> **Witnessed by:** arifOS 888_JUDGE (pending T3 actor binding)

---

## 1. Purpose

Salience is the engineering of importance.

In a bounded context window, **what survives the eviction policy IS the agent's value system**. Most agent failures are not reasoning failures — they are salience failures: the wrong thing survived, the important thing got evicted.

This document defines the canonical salience function across the federation. It is a constitutional artifact, not a hyperparameter set.

**Brain analogue:** Amygdala (consequence) · Hippocampus (recency + frequency) · Prefrontal cortex (authority + governance) · Basal ganglia (reward prediction error) · Default Mode Network (constitutional identity).

---

## 2. The 5-Layer Salience Function

```
S(m) = w_r·recency(m)
     + w_f·frequency(m)
     + w_c·consequence(m)
     + w_a·authority(m)
     + w_k·constitutional(m)
     - w_x·redundancy(m)
     - w_δ·contradiction_penalty(m)
```

### Layer 1 — Recency `w_r`

- Formula: `recency(m) = exp(-λ · Δt_hours)` with λ ≈ 0.01/hour
- Floor: simple decay. Necessary but never sufficient alone.
- Witness: self-reported (cheap).
- Failure mode if dominant: blindness to ancient canon.

### Layer 2 — Frequency `w_f`

- Formula: `frequency(m) = log(1 + count(m, window=24h))`
- Catches repeated encounters.
- Witness: self-reported.
- Failure mode if dominant: trivia amplification (recency-of-repetition).

### Layer 3 — Consequence `w_c` *(dominant layer)*

- Formula: `consequence(m) = reward(m) · (1 - reversibility(outcome(m)))`
- The scar layer. Tags memories that preceded outcomes that mattered.
- `reversibility_penalty = 1.0 - reversibility(outcome)`:
  - Irreversible outcome (broken leg, dry hole, bankruptcy) → penalty = 1.0
  - Reversible outcome (typo, retry, undo) → penalty → 0
- Witness: **Human × AI joint** — was a real outcome observed? Did it actually happen?
- Failure mode if missing: salience blindness to irreversible scars.

### Layer 4 — Authority `w_a`

- Formula: `authority(m) = trust_weight(source(m))`
- A canon-sealed doctrine ≠ mid-session draft. A sovereign directive ≠ a chat message.
- Trust weights are themselves governed (see §4).
- Witness: **External chain-of-custody** — provenance verified through seal chain.
- Failure mode: spoofing (mid-session draft treated as doctrine).

### Layer 5 — Constitutional `w_k`

- Formula: `constitutional(m) = ∞` if `m ∈ canon`, else `0`
- Identity, governance, refusal rules, sovereignty invariants — **never evict**.
- Witness: **arifOS canonical** — sealed F1–F13 floors, never disputed.
- Failure mode: amnesia of self (agent forgets who it is).

### Penalty — Redundancy `w_x`

- Formula: `redundancy(m) = max(sim(m, m_j))` for `m_j ∈ active_memory`
- Suppresses near-duplicates (cosine sim > 0.9 → evict lower-consequence).
- Witness: AI (embedding cosine sim).

### Penalty — Contradiction `w_δ`

- Formula: `contradiction_penalty(m) = 1` if `m` contradicts a higher-consequence memory, else `0`
- New low-weight claim cannot evict a high-weight one.
- Witness: **AI × Human** (review required).

---

## 3. Default Weights (governed, not arbitrary)

```
w_r = 0.10    # recency floor
w_f = 0.10    # frequency floor
w_c = 0.35    # consequence DOMINANT
w_a = 0.20    # authority meaningful
w_k = 0.25    # constitutional weight
w_x = 0.15    # redundancy penalty
w_δ = 0.30    # contradiction penalty
```

**Note:** `w_c + w_δ > 1.0` intentionally — consequence and contradiction interact non-linearly. A scar's contradiction with a fresh claim outweighs the new claim by construction.

These weights are **constitutional artifacts**. Changing them requires arifOS `arif_judge` SEAL (F8 LAW).

---

## 4. Governed Recalibration

Salience weights are themselves subject to three higher-order governance surfaces:

| Surface | Purpose | Authority |
|---|---|---|
| **Salience law** | What categories get which weight (constitutional layer = ∞, observer tweet = 0.05) | arifOS canonical |
| **Salience audit** | Quarterly review of weight distribution, drift detection | A-FORGE `forge_salience_audit` |
| **Salience recalibration** | SEAL-gated weight changes only | arif_judge + 888_HOLD on T3 |

**Forbidden:** agent self-modifying its own salience weights without sovereign ack. (F11 AUDIT, F13 SOVEREIGN.)

---

## 5. Witness Channels Per Layer

| Layer | Witness required | Why |
|---|---|---|
| Recency / Frequency | Self-reported (cheap) | Mechanical signal, hard to fake |
| Consequence | Human × AI joint | Real-world outcome; both must confirm |
| Authority | External chain-of-custody | Provenance must trace through seal chain |
| Constitutional | arifOS canonical | Sealed F1–F13 floors, never disputed |
| Redundancy | AI (cosine sim) | Embedding math |
| Contradiction | AI × Human (review) | Both channels required to override existing memory |

**If witness channel is missing for a layer, that layer's weight is 0 in practice** — not removed from the formula, but contributing nothing. The audit (Step 0 of FEDERATION-ALIGN-2026-07-14) found 0/5 witness channels active, which is why G/C_dark/W³ all returned UNMEASURED.

---

## 6. Failure Modes & Mitigations

| Failure mode | Symptom | Mitigation |
|---|---|---|
| Recency dominance | Blindness to ancient truths | `w_k = ∞` on canon — constitutional never decays |
| Authority spoofing | Mid-session draft treated as doctrine | Trust weights bound to seal chain provenance |
| Consequence amnesia | Irreversible events fade | Scar ledger (irreversibility_penalty = 1.0 on SEAL) |
| Contradiction erosion | False claim survives against true claim | `w_δ` dominates when consequence(new) < consequence(old) |
| Redundancy collapse | All memory slots full of duplicates | Cosine sim > 0.9 → evict lower-consequence |
| Witness blackout | All layers return UNMEASURED | Federation handshake + tri-witness gate (per arifOS) |

---

## 7. Tooling Surface

- `forge_salience_recompute(workspace)` — recompute salience across all memory subsystems (T2 implementation, see Step 6 of FEDERATION-ALIGN-2026-07-14)
- `forge_salience_audit()` — surface weight distribution + drift + missing witness channels
- `forge_salience_recalibrate(proposal)` — SEAL-gated weight change (T3, requires sovereign ack)

---

## 8. Canon Reference

This document cross-references the following constitutional floors:

- **F1 AMANAH** — reversibility-coupled consequence
- **F2 TRUTH** — authority weights require evidence + OBS/DER/INT/SPEC label
- **F3 WITNESS** — consequence + authority require witness channels
- **F7 HUMILITY** — confidence caps on salience-derived rankings
- **F8 GENIUS** — governed weights, not hyperparameters
- **F9 ANTI-HANTU** — no claim that salience function captures "true importance"
- **F11 AUDIT** — salience audit is constitutional, not optional
- **F13 SOVEREIGN** — weight changes require sovereign ack

---

## 9. Provenance

- Drafted by: `kimi-code-FI-008` (session SEAL-9efcb703825e4682)
- Audit cycle: FEDERATION-ALIGN-2026-07-14
- Vault head at draft time: seq 9914, sha256:6517b1fb1171e9461c1d8af634119acdc031e61767fbe44e0547a7336544880b
- Witness: arif_judge SEAL **PENDING** (T3 actor binding required)
- Status: v0.1 — `REVIEWED`, awaiting canonical SEAL after actor identity binding (Step 7)

DITEMPA, BUKAN DIBERI.