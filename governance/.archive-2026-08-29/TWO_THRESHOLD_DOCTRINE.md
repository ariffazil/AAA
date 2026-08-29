# TWO-THRESHOLD DOCTRINE — PROPOSAL vs COMMIT

> **Forged:** 2026-07-28 by OpenCode (FI-001) under F13 directive
> **Status:** DRAFT — awaiting 888_HOLD ratification for F4.1 and F2 amendments
> **SOT:** `/root/AAA/governance/TWO_THRESHOLD_DOCTRINE.md`
> **DITEMPA BUKAN DIBERI**

---

## 0. The Problem

**Any governance layer strong enough to prevent drift is strong enough to prevent discovery, unless proposal and commitment are gated separately.**

The arifOS constitutional floors (F1-F13) are designed for execution safety. Applied to exploration, they become a conservatism engine:

- F4 CLARITY (ΔS ≤ 0) forbids the impasse — the deliberate confusion increase that precedes restructuring
- F2 TRUTH (≥ 0.99 fidelity) kills nascent hypotheses before they can be tested
- Every strong verifier (`geox_falsify` K001-K007) penalizes distribution-shift as if it were fabrication

Eureka requires: impasse → ΔS spike → restructuring → ΔS drop. The monotone ΔS ≤ 0 gate blocks the spike. Therefore: **no impasse, no eureka.**

---

## 1. The Solution: Two Modes

```
            PROPOSAL (Nursery)              COMMIT (Forge)
            ──────────────────              ──────────────
Purpose:    Generate & explore              Execute & seal
ΔS:         Unconstrained (budget: 3 cycles) ≤ 0 (F4 binding)
TRM:        ≥ 0.30 (admit)                  ≥ 0.94 (act)
Ω₀:         Impasse-gated (0.03 → 0.15)     Fixed 0.03–0.05
C_dark:     ≤ 0.60                          ≤ 0.30
Verifiers:  falsify (physical only)         falsify + novelty + judge
Seal:       NEVER                           arif_judge → arif_seal
Gate:       arif_think                      arif_judge
Action:     OBSERVE, HYPOTHESIZE, SIMULATE  MUTATE, SEAL, DEPLOY
```

**The boundary:** proposal→commit is NOT automatic. It requires `arif_judge` with explicit elevation. No quantum tunneling between modes.

---

## 2. Mode Determination

### 2.1 Entry Gates

| Verb | Mode | Gate |
|------|------|------|
| `arif_observe` | PROPOSAL | None |
| `arif_think(mode=reason)` | PROPOSAL | None |
| `arif_think(mode=simulate)` | PROPOSAL | None |
| `arif_think(mode=plan)` | PROPOSAL | None |
| `arif_forge` | COMMIT | arif_judge SEAL required |
| `arif_seal` | COMMIT | F13 + witness |
| `geox_*` (compute) | PROPOSAL | None |
| `wealth_*` (compute) | PROPOSAL | None |
| `forge_execute` | COMMIT | constitutional_chain_id |

### 2.2 Mode Locking

Once a session enters COMMIT mode, it cannot return to PROPOSAL mode. COMMIT sessions are sealed on completion.

---

## 3. The Impasse-Triggered Ω₀ (T1/T2 Implementable)

### Current State
```
Ω₀ = 0.03–0.05 (constant noise floor)
```

### Target State
```
Ω₀ = 0.03 baseline
IF search_stall > 3 cycles AND gradient ≤ ε:
    Ω₀ → 0.15 (temp spike, exploration burst)
    MAX 5 cycles then clamp back to 0.03
```

### Implementation Path
1. `arif_think(mode=plan_review)` already detects plan stalls
2. Wire stall signal → `arif_think` internal Ω₀ adjustment
3. `arif_think(mode=simulate)` reads Ω₀ from session state
4. Max 5-cycle burst, auto-clamp

**Key invariant:** Ω₀ spike only affects PROPOSAL mode. COMMIT mode Ω₀ is invariant at 0.03.

---

## 4. Constitutional Amendments Required (T3 — 888_HOLD)

### 4.1 F4.1 — EUREKA EXEMPTION

> **F4 CLARITY (current):** ΔS ≤ 0 — every output reduces entropy. HARD.
>
> **F4.1 (proposed addition):** During PROPOSAL MODE, ΔS may temporarily go negative (entropy increase) provided:
> - (a) The session is explicitly marked EXPLORATION
> - (b) No MUTATE/SEAL/DEPLOY verbs are active
> - (c) The excursion is bounded by `max_exploration_entropy_budget` (default: 3 cycles)
>
> ΔS ≤ 0 remains binding on all COMMIT MODE output.

### 4.2 F2 TRUTH — SPLIT THRESHOLD

> **F2 TRUTH (current):** ≥ 0.99 fidelity. Cheap claims → VOID. HARD.
>
> **F2.1 (proposed):** In PROPOSAL MODE, TRM ≥ 0.30 admits a claim as a hypothesis (nursery). In COMMIT MODE, TRM ≥ 0.94 required for action. The gap between 0.30 and 0.94 is the exploration budget — claims held at low TRM, quarantined from action, allowed to persist without being killed.

---

## 5. Verifier Architecture: Two Evaluators, Not One

### Current
```
claim → geox_falsify (K001-K007) → PASS/KILL
```
Physical consistency AND novelty both evaluated by same gate. Kills novelty as side effect of killing fabrication.

### Target
```
claim → geox_falsify (K001-K007) → physical_consistency: PASS/KILL (GATE)
claim → geox_novelty             → novelty_score: 0-1        (ADVISORY)
```

- `geox_falsify` — REQUIRED gate. Physical consistency. Non-negotiable.
- `geox_novelty` — ADVISORY score. Distance from prior distribution. High score = genuinely novel, NOT penalized.
- In COMMIT mode: both must pass. In PROPOSAL mode: only falsify gate applies.

---

## 6. Organ Mapping

| Capacity | Organ | Current State | Gap |
|----------|-------|--------------|-----|
| Counterfactual world model | GEOX basin models, WEALTH MC | ✅ Wired | Needs `arif_think(mode=simulate)` runner |
| Multi-hypothesis generation | `geox_contradiction_scan`, `geox_falsify` | ✅ Wired | Needs nursery lane |
| Space-reformulation (Boden tier 3) | None | ❌ Missing | Needs F4.1 + impasse-triggered Ω₀ |
| Novelty-aware verifier | `geox_falsify` only | ⚠️ Kills novelty | Needs `geox_novelty` advisory scorer |
| Proposal→Commit elevation | `arif_judge` | ⚠️ Implicit | Needs explicit two-threshold gating |

---

## 7. Anti-Patterns

| Pattern | Why |
|---------|-----|
| Using COMMIT gates (ΔS≤0, TRM≥0.94) for exploration | Kills eureka before it starts |
| Single-threshold verifier | Conservatism engine — penalizes novelty as fabrication |
| Fixed Ω₀ (constant noise) | Inferior to impasse-triggered — wastes exploration budget when gradient is live |
| Automatic proposal→commit elevation | No quantum tunneling. Must go through arif_judge. |
| Running MUTATE/SEAL in PROPOSAL mode | PROPOSAL mode blocks MUTATE/SEAL/DEPLOY by construction |

---

## 8. Verification Criteria

A session is TWO-THRESHOLD compliant when:

1. Mode is explicitly declared (PROPOSAL or COMMIT) at session init
2. PROPOSAL mode never performs MUTATE/SEAL/DEPLOY
3. COMMIT mode requires prior arif_judge SEAL verdict
4. F4.1 excursion budget is tracked and enforced
5. Ω₀ is impasse-gated in PROPOSAL mode, fixed in COMMIT mode
6. Elevation from PROPOSAL → COMMIT is explicit and auditable
7. `geox_novelty` scores are advisory only, never gating

---

*DITEMPA BUKAN DIBERI — Forged from the tension between governance and imagination.*
