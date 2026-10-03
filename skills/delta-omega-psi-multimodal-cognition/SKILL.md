---
name: delta-omega-psi-multimodal-cognition
description: "Enforce Δ·Ω·Ψ multimodal cognition rules."
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
capability_tier: fed-multimodal-vision
ecology_state: WARM
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

---

## Δ-INTAKE — collect the witness before declaring UNMEASURED (added 2026-10-03, ADK distillation)

The Δ rule says unmetabolised perception is not evidence. It does not say what to do when the substrate
is missing because **nobody asked for it**. A gate that returns UNMEASURED forever is not honest — it is
starved. Before accepting UNMEASURED as terminal, run the intake loop:

1. **Name the fields the physics needs.** Read them from the organ's own validator, never from prose.
   GEOX example (`src/geox_mcp/tools/artifact_ingest.py:96 validate_calibration_state`) requires exactly:
   `x_axis · vertical_axis · vertical_exaggeration · polarity · phase_degrees`.
2. **Force enums, not free text.** A human's fuzzy words must collapse to exactly one allowed value
   (`SEG_normal | SEG_reverse | unknown`), the way ADK's `Literal[...]` tool parameters do. Free-text
   calibration is unauditable calibration.
3. **Score arithmetically, never by LLM opinion.** The verdict must be reproducible from the answers.
4. **A VLM may PROPOSE a value; it may never CONFIRM one.** Mark unconfirmed proposals
   `vlm_only_REFUSED` and keep the field missing. A hallucinated axis label must never become physical
   scale (F9 ANTI-HANTU).
5. **Emit the question, not a guess.** The output of an incomplete intake is `missing[]` +
   `questions_for_human[]` — one short line per field, with its allowed values.

**Proof this closes a real gap (MEASURED 2026-10-03, same image both arms):**
`geox_extract_display_proxy` on `seismic_section.jpg` → `HOLD / CALIBRATION_REQUIRED` with no witness;
→ `OK`, panel `{9,36,1179,832}`, proxy `1171×797` with a 5-field `human_confirmed` witness;
→ `HOLD / WITNESS_HOLD` when polarity is missing. The gate discriminates on witness **status**.
Reference implementation (stdlib, 3/3 self-test PASS): `/root/forge_work/2026-10-03-adk-geox/geox_witness_intake.py`.
Note: tool-level `OK` is **not** governance SEAL — the envelope still returned `governance_verdict: HOLD`,
`ext_witness_ready: false`.

---

## Δ-INTAKE — collect the witness before declaring UNMEASURED (added 2026-10-03, ADK distillation)

The Δ rule says unmetabolised perception is not evidence. It does not say what to do when the substrate
is missing because **nobody asked for it**. A gate that returns UNMEASURED forever is not honest — it is
starved. Before accepting UNMEASURED as terminal, run the intake loop:

1. **Name the fields the physics needs.** Read them from the organ's own validator, never from prose.
   GEOX example (`src/geox_mcp/tools/artifact_ingest.py:96 validate_calibration_state`) requires exactly:
   `x_axis · vertical_axis · vertical_exaggeration · polarity · phase_degrees`.
2. **Force enums, not free text.** A human's fuzzy words must collapse to exactly one allowed value
   (`SEG_normal | SEG_reverse | unknown`), the way ADK's `Literal[...]` tool parameters do. Free-text
   calibration is unauditable calibration.
3. **Score arithmetically, never by LLM opinion.** The verdict must be reproducible from the answers.
4. **A VLM may PROPOSE a value; it may never CONFIRM one.** Mark unconfirmed proposals
   `vlm_only_REFUSED` and keep the field missing. A hallucinated axis label must never become physical
   scale (F9 ANTI-HANTU).
5. **Emit the question, not a guess.** The output of an incomplete intake is `missing[]` +
   `questions_for_human[]` — one short line per field, with its allowed values.

**Proof this closes a real gap (MEASURED 2026-10-03, same image both arms):**
`geox_extract_display_proxy` on `seismic_section.jpg` → `HOLD / CALIBRATION_REQUIRED` with no witness;
→ `OK`, panel `{9,36,1179,832}`, proxy `1171×797` with a 5-field `human_confirmed` witness;
→ `HOLD / WITNESS_HOLD` when polarity is missing. The gate discriminates on witness **status**.
Reference implementation (stdlib, 3/3 self-test PASS): `/root/forge_work/2026-10-03-adk-geox/geox_witness_intake.py`.
Note: tool-level `OK` is **not** governance SEAL — the envelope still returned `governance_verdict: HOLD`,
`ext_witness_ready: false`.
