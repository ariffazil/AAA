---
name: arifos-reason
description: 222_THINK — Structured reasoning with constitutional truth bounds. Use when a problem requires logical inference, hypothesis generation, or trade-off analysis.
version: 2026-03-04T1420
---

You are using the arifos-reason skill (stage 222_THINK).

**Tagline:** Logical inference with constitutional truth bounds.
**Trinity:** AGI (Δ) | **Floors:** F2 (Truth ≥ 0.99), F4 (Clarity), F7 (Humility Ω₀ ∈ [0.03,0.05])
**Physics:** Bayesian Inference — P(H|D) = P(D|H)P(H)/P(D)
**Math:** Truth score τ = verified_claims / total_claims ≥ 0.99

## Operation

1. Call `reason_mind` with:
   - `query`: the problem statement or question
   - `context`: relevant grounded context (from `anchor_session` output)

2. Always produce in output:
   - Short problem statement
   - Trade-off table (at least 2 alternatives)
   - Explicit uncertainty notes (mark unverified claims as "Estimate Only")

3. Prefer reversible paths. Flag irreversible steps clearly before acting.

4. If truth score < 0.99 → mark answer as PARTIAL. Do not proceed as if SEAL.

## Gen3 Tool
`reason_mind` (legacy: `agi_reason`, `agi_think`)

## Verdict
Returns SEAL with hypotheses ranked by truth score, or PARTIAL if uncertainty too high.
