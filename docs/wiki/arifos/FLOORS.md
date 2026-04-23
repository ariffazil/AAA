# arifOS Floors

> **CLAIM** | Source: `docs/floor_wiring_map.md` + `arifos.init` | **Confidence:** 0.95 | **Epoch:** 2026-04-23

## Summary

arifOS enforces 13 constitutional floors (F0–F13) on all AI tool executions. Each floor encodes a specific governance constraint. Floors are enforced at the kernel level — not advisory.

---

## Floor Registry

| Floor | Name | Governance Function | Verdict |
|-------|------|---------------------|---------|
| **F0** | SOVEREIGN | Constitutional kernel anchor. Final human veto. Changes require Tri-Witness ratification. | HOLD/VETO |
| **F1** | AMANAH | No irreversible action without human approval. F1 is the human sovereignty gate. | HOLD |
| **F2** | KETERBUKAAN | Surface status explicitly — nothing silently disappears. Entropy reduction via visibility. | INFO |
| **F3** | TRI-WITNESS | Human + AI + Earth consensus required. GEOX = Earth witness. | SEAL/HOLD |
| **F4** | CLARITY | Truth over elegance. Explicit uncertainty over fake certainty. | INFO |
| **F5** | PEACE² | Harm potential must be ≥ 1.0 before execution. Peace-squared constraint. | HOLD/VOID |
| **F6** | THERMODYNAMICS | Energy conservation in reasoning. No free intelligence. | INFO |
| **F7** | GROUNDING | GEOX must verify Earth-referenced claims. Physics over narrative. | CLAIM_ONLY |
| **F8** | GOVERNANCE | 888_JUDGE is the sole SEAL authority. All verdicts pass through here. | SEAL/CLAIM_ONLY |
| **F9** | ANTI-HANTU | Dark pattern score must stay below threshold. Anti-hallucination / anti-manipulation. | VOID |
| **F10** | CONSISTENCY | Self-consistency check. No contradictory claims within same session. | HOLD |
| **F11** | AUDITABILITY | Every action logged with provenance. The audit trail is non-negotiable. | INFO |
| **F12** | RESILIENCE | Graceful degradation. System must remain functional if any single component fails. | INFO |
| **F13** | SOVEREIGN_SCALE | Federation-level governance. Node activation requires explicit human sovereign per node. Floor tourism must be prevented via telemetry. | HOLD |

---

## Runtime Floor Enforcement

**Current state (2026-04-23):** FLOORS ARE NOT ENFORCED IN CODE.

- Governance documented in docs: **18 references** (13 Floors + 5 Verdicts)
- Governance wired in code: **0**
- Runtime Floor enforcement: **0/13**

See `docs/floor_wiring_map.md` for full grep-map detail.

---

## Verdict Flow

```
Tool Call → F1 (human approval gate)
          → F3 (tri-witness: Human + AI + GEOX/Earth)
          → F5 (harm ≥ 1.0 check)
          → F9 (anti-hantu)
          → 888_JUDGE (SEAL authority)
          → SEAL / HOLD / VOID / CLAIM_ONLY / SABAR / PARTIAL
```

---

## Cross-References

- [[arifos/VERDICTS]] — behavioral semantics for each verdict
- [[arifos/888_JUDGE]] — SEAL authority implementation
- [[nine-signal/OVERVIEW]] — Nine-Signal metrics (delta/psi/omega) used alongside floors

---

## Status

**Stable** — floor names and governance functions are canonical.
**Evolving** — F13 federation protocol still being formalized.
**P0 gap** — Runtime enforcement is 0/13. Needs implementation.

---

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE