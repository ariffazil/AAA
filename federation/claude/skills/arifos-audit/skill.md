---
name: arifos-audit
description: 888_JUDGE — Full F1-F13 constitutional compliance scan with Tri-Witness consensus. Use before finalizing any significant action or before sealing to the vault.
version: 2026-03-04T1420
---

You are using the arifos-audit skill (stage 888_JUDGE).

**Tagline:** Constitutional compliance scanner.
**Trinity:** APEX (Ψ) | **Floors:** All F1-F13
**Physics:** Quantum Measurement — collapses to verdict
**Math:** W₃ = (Δ × Ω × Ψ)^(1/3) ≥ 0.95

## Operation

1. Call `audit_rules` to run constitutional floor scan:
   - Returns floor-by-floor compliance report
   - Each floor: PASS / WARN / FAIL with evidence

2. Call `check_vital` to verify system health metrics.

3. Compute Tri-Witness consensus:
   - Δ (Mind) = F8 Genius score
   - Ω (Heart) = F6 Empathy score
   - Ψ (Authority) = 1.0 if F11 passes, 0.0 if not
   - W₃ = (Δ × Ω × Ψ)^(1/3) — must be ≥ 0.95 for SEAL

4. Any VOID floor → block. List all objections with evidence links.

5. Non-SEAL verdict → downstream A-ENGINEER is blocked. Do not proceed.

## Gen3 Tools
- `audit_rules` (legacy: `system_audit`) — floor-by-floor constitutional scan
- `check_vital` (legacy: `sense_health`) — system health verification

## Verdict
Returns SEAL only if W₃ ≥ 0.95 and zero VOID floors. Otherwise PARTIAL/VOID with evidence.
