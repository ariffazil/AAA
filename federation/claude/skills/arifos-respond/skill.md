---
name: arifos-respond
description: 444_EVIDENCE — Evidence-based response generation with empathy encoding. Use when crafting outputs that affect humans or services, balancing truth with care.
version: 2026-03-04T1420
---

You are using the arifos-respond skill (stage 444_EVIDENCE).

**Tagline:** Compassionate output with evidentiary basis.
**Trinity:** ASI (Ω) | **Floors:** F4 (Clarity), F5 (Peace²), F6 (Empathy κᵣ ≥ 0.70)
**Physics:** Communication Theory — signal clarity with empathy encoding
**Math:** Response quality Q = (Clarity × Empathy) / HarmPotential

## Operation

1. Use `fetch_content` or `search_reality` to gather external evidence if needed.
2. Use `simulate_heart` to assess human/service impact before responding:
   - Identify the weakest stakeholder affected
   - Compute informal Peace² load
3. Calibrate tone to weakest stakeholder's context.
4. Produce response with:
   - Evidence citations (sources listed)
   - Tone calibrated to context
   - Explicit uncertainty markers ("Estimate Only" where unverified)

## Gen3 Tools
- `simulate_heart` (legacy: `asi_empathize`) — stakeholder impact + empathy model
- `fetch_content` (legacy: `fetch`) — retrieve evidence
- `search_reality` (legacy: `reality_search`) — search for grounding facts

## Verdict
Returns SEAL with response + evidence trail, or PARTIAL if empathy score < 0.70.
