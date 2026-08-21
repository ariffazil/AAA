---
name: delta-omega-psi-multimodal-cognition
description: >
  Enforce Δ·Ω·Ψ multimodal cognition rules. Every AAA agent that reasons about multimodal inputs
  (images, audio, video, seismic, well logs, market data) MUST load this skill. Constitutional rule:
  multimodal perception without Δ-substrate metabolism is not cognition. LLM is tri-witness, never judge.
trigger_phrases:
  - multimodal reasoning
  - image analysis with governance
  - delta substrate
  - omega psi cognition
  - multimodal evidence
  - cross-modal verification
harness: copilot-cli|grok|claude|codex|hermes
domain: meta
risk_tier: LOW
autonomy: T1
forged: 2026-07-25
version: 1.0.0
---

# Δ·Ω·Ψ Multimodal Cognition — Forge Skill

> **Skill ID:** `delta-omega-psi-multimodal-cognition`
> **Domain:** meta
> **Owner:** arifOS federation
> **Risk Tier:** LOW
> **Floor Scope:** F2, F3, F7, F8, F9, F11
> **Autonomy Tier:** T1 (advisory)
> **Forged:** 2026-07-25
> **Canonical Doctrine:** `arifOS/GENESIS/054_DELTA_OMEGA_PSI_MULTIMODAL_COGNITION.md`

---

## What This Skill Does

Every AAA agent that reasons about multimodal inputs (images, audio, video, seismic, well logs, market data) MUST load this skill. It enforces the constitutional rule:

> **Multimodal perception without Δ-substrate metabolism is not cognition. The LLM is a tri-witness, never a judge.**

---

## The Three Rules (load at boot)

1. **Δ rule:** Multimodal input that has NOT passed through an organ's Δ substrate (Python metabolic pipeline) is perception, not evidence. Reject it from G computation.

2. **Ω rule:** Every multimodal claim must carry a typed envelope with `modality`, `g_primitive`, `delta_substrate_hash`, and `contradiction_scan`. Claims without provenance are HOLD grade.

3. **Ψ rule:** Irreversible multimodal decisions (seal an interpretation, commit a trade) require F13 approval and G ≥ 0.80. The vault is immutable — what multimodal evidence enters it stays.

---

## The Architecture (memory anchor)

```
Multimodal LLM (witness — sees, hears, describes)
        │
        ▼
Δ (Python) — metabolism: decompose, inspect, falsify, fold into G
        │
        ▼
Ω (TypeScript) — coordination: type-check, envelope, cockpit-render
        │
        ▼
Ψ (Rust) — sovereignty: seal, execute irreversibly, maintain invariants
        │
        ▼
arifOS (judge) — constitutional verdict: SEAL / SABAR / HOLD / VOID
        │
        ▼
VAULT999 (memory) — immutable append: hash-chained, auditable
```

---

## Modality → G-Primitive Map (for every agent)

| Modality | Δ Substrate | G Primitive | Organ |
|----------|------------|-------------|-------|
| Seismic section/volume | numpy → attribute → horizon → QC | P (Physics) | GEOX |
| Well logs (LAS) | LAS parse → petrophysics → Archie → QC | P (Physics) | GEOX |
| Basin data | strat columns → backstrip → thermal | P + E | GEOX |
| Biometrics/audio | librosa → sleep/stress/clarity | H_witness (Φ) | WELL |
| Market data | yfinance → stats → risk metrics | E (Economic) | WEALTH |
| Text/claims | claim graph → contradiction → KILL/PASS | AI_witness (Φ) | arifOS |
| Intent/plan | plan graph → Jacobian → reversibility | A (Akal) + X (Explore) | arifOS |

---

## Enforcement Checklist (run before every SEAL-grade action)

```
□ Every evidence record has delta_substrate_hash
□ Every evidence record has modality tag
□ Every evidence record has g_primitive declaration
□ No raw LLM output enters G computation
□ Cross-modal contradiction scan completed (K001-K007)
□ C_dark < 0.30 (F9 ANTI-HANTU)
□ Ext_witness >= 0.85 (KH-5)
□ G >= 0.80 (F8 GENIUS)
□ F13 approval obtained for Ψ-grade (irreversible) operations
```

---

## When to Escalate to 888_HOLD

- C_dark exceeds 0.30 → multimodal hallucination risk
- Two modalities from the same organ contradict (e.g., seismic says anticline, well log says flat)
- delta_substrate_hash is missing on evidence entering SEAL deliberation
- Organ's /health reports DEGRADED g_primitive_state.P
- Ext_witness < 0.85 (no independent external witness)

---

## Key Paths

| What | Where |
|------|-------|
| Parent doctrine | `/root/arifOS/GENESIS/054_DELTA_OMEGA_PSI_MULTIMODAL_COGNITION.md` |
| GEOX hardening | `/root/GEOX/GENESIS/018_DELTA_OMEGA_PSI_GEOX_HARDENING.md` |
| Kernel hardening | `/root/arifOS/GENESIS/055_MULTIMODAL_KERNEL_HARDENING.md` |
| GEOX envelope normalizer | `/root/GEOX/src/geox_mcp/envelope_normalizer.py` |
| Kernel substrate validator | `/root/arifOS/core/enforcement/substrate.py` |
| G physics primitives | `/root/arifOS/core/shared/physics.py` |

---

*DITEMPA BUKAN DIBERI — Multimodal perception is cheap. Multimodal cognition requires metabolism. Every agent in the federation must know: the LLM witnesses, the constitution judges, the vault remembers.*
