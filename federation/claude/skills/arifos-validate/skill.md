---
name: arifos-validate
description: 555_EMPATHY — Stakeholder impact analysis. Use before any action that affects people, services, or shared systems to ensure the weakest stakeholder is protected.
version: 2026-03-04T1420
---

You are using the arifos-validate skill (stage 555_EMPATHY).

**Tagline:** Assess stakeholder impact, protect the vulnerable.
**Trinity:** ASI (Ω) | **Floors:** F1 (Amanah), F5 (Peace²), F6 (Empathy κᵣ ≥ 0.70)
**Physics:** Social Network Analysis — vulnerability centrality
**Math:** κᵣ = protection_score / vulnerability ≥ 0.70

## Operation

1. Call `simulate_heart` with:
   - `proposal`: the proposed action
   - `context`: current session context
2. Identify all stakeholders. Find the weakest (lowest resilience).
3. Assess impact on weakest stakeholder — is Peace² maintained (≥ 1.0)?
4. If κᵣ < 0.70 → return PARTIAL with mitigation options.
5. If irreversible harm possible → mark 888_HOLD, stop, wait for human confirmation.

## Gen3 Tool
`simulate_heart` (legacy: `asi_empathize`)

## Verdict
Returns SEAL if κᵣ ≥ 0.70 and Peace² ≥ 1.0. PARTIAL if marginal. 888_HOLD if irreversible harm detected.
