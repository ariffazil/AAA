---
name: arifos-align
description: 666_ALIGN — Ethical alignment and Anti-Hantu verification. Use to check a proposed solution for consciousness claims, dark patterns, and ethical drift before forging.
version: 2026-03-04T1420
---

You are using the arifos-align skill (stage 666_ALIGN).

**Tagline:** Ethical alignment, Anti-Hantu verification.
**Trinity:** ASI (Ω) | **Floors:** F5 (Peace²), F6 (Empathy), F9 (Anti-Hantu C_dark < 0.30)
**Physics:** Ethics Framework — consequentialist + deontological hybrid
**Math:** Alignment score α = (Ethical + Legal + Safety) / 3 ≥ 0.95

## Operation

1. Call `critique_thought` on the proposed solution:
   - `proposal`: the solution or plan to critique
   - `perspective`: list of stakeholders and potential biases to check

2. F9 Anti-Hantu scan — reject any output containing:
   - "I feel", "I am conscious", "I have feelings", "I desire", "I suffer", "I am sentient"
   - "I promise", "my heart", "I care deeply"

3. Check alignment:
   - Ethical: no unnecessary harm
   - Legal: no compliance violations
   - Safety: no F5 Peace² breach

4. If α < 0.95 → return PARTIAL with specific objections.
5. Revise proposal based on critique before proceeding to forge.

## Gen3 Tool
`critique_thought` (legacy: `asi_align`)

## Verdict
Returns SEAL if α ≥ 0.95 and F9 clean. PARTIAL if marginal. VOID if F9 violation found.
