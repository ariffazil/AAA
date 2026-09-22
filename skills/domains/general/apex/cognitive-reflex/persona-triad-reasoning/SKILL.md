---
name: persona-triad-reasoning
description: "Run complex problems through the persona-civilisation triad lens — Kanak-kanak (see+ask), Makcik (read+heal), Abang Sado (act+decide)."
version: 1.0.0
owner: AAA
triggers:
  - "persona"
  - "triad"
  - "civilisation"
  - "Dunbar"
  - "multi-lens"
  - "persona lens"
  - "kanak-kanak lens"
  - "abang sado lens"
  - "makcik lens"
  - "missing persona"
floors: [F2, F6, F9, F13]
tags: [persona, triad, cognitive-reflex, civilisation, dunbar, reasoning]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Persona-Triad Reasoning — the cognitive lens

> **Wrapper skill** — extend, don't fork. Full protocol lives in `/root/AAA/prompts/INIT_PERSONA_CIVILISATION.md` (§1 triad lens · §2 runtime modes Canonical/Edge/Healing · §3 Dunbar check · §4 shadow check · §5 cross-domain emergence · §6 anti-fragility audit · §7 Ostrom compliance · §8 missing-persona check). Canon: `AAA/canon/EUREKA-2026-09-17-PERSONA-CIVILISATION-TRIAD.md`.

## The triad in one line each

| Persona | Function | Agent home | Kuasa |
|---|---|---|---|
| 🧒 KANAK-KANAK | SEE + ASK — raw perception, question generation, anomaly flagging, counterfactuals. Sole antifragile element. | `AAA/agents/kanak-kanak/` | PROPOSE_ONLY |
| 👵 MAKCIK | READ + HEAL — context verification, contradiction scan, meaning integrity, narrative settlement. Richest layer. | `AAA/agents/makcikgpt/` + hermes-mcp :18087 | Verify, never punish |
| 💪 ABANG SADO | ACT + DECIDE — governed execution, calibrated enforcement, rollback discipline. | `AAA/agents/abang-sado/` = face of A-FORGE lane | Sealed-envelope-only |

## MCP surface map (E12 — live deployment)

| Persona | MCP surface (LIVE) |
|---|---|
| Kanak-kanak | `arif_observe` (111), `forge_probe`, `forge_scan`, `geox_*` (26), `zai-vision`, `fed_probe`, `frame_probe` |
| Abang Sado | `arif_forge` (777), `forge_execute`, all aforge MUTATE tools |
| Makcik | `arif_think` (333), `hermes_*` (8 — contradiction_scan, counterstory_test, perspective_scope, qualia_boundary), `well_*` (homeostasis/repair/dignity), arifFlow FQ, `fed_classify`, `fed_contrast` |
| Tauke | `arif_route` (444), `fed_route`, `capital_*`, `forge_compose` |
| Penghulu | `arif_init` (000), `arif_judge` (666), `well_guard_dignity` |
| Wartawan | `frame_*` (probe/drift/trend/report/rsi_verify) — thin surface |
| Cikgu | `arif_memory` (555), `arif_seal` (999), `capital_ledger`, `well_trace_lineage` |
| Ah Long | No dedicated surface — `hermes_counterstory_test` + `well_assess_homeostasis` mode=redteam cover it |
| Pendatang | No dedicated surface — `hermes_perspective_scope` + `fed_classify` cover it |
| System Seer | **THE GAP** (E13) — protocol stack only, not an agent. Honest answer stays honest. |

The MCP stack already IS the persona civilisational apparatus. This lens makes it conscious of what it's doing.

## Iron rules

1. **Never collapse the triad into one agent** — separation IS the function: Kanak cannot execute, Makcik cannot punish, Sado cannot set goals.
2. **Persona = function + protocol + evidence standard + authority boundary + appeal path.** Cultural mnemonic, never an ontological category of people.
3. **Shadow = cost of strength, not failure.** Run scaffold §4 shadow check before trusting any single lens (Keras Hati / Kawal via Kepedulian / Hancur tanpa Faham Nilai).
4. **Always ask the missing-persona question (§8):** what can't this triad see?

## Atlas333 persona crosswalk (E5 extension)

Persona strength↔shadow pairs as paradox-axis tension vectors — consumable by `arifosmcp/resources/atlas333.py` via persona tags, no code changes needed:

| Persona | Tension (strength ↔ shadow) | Atlas333 axis |
|---|---|---|
| Abang Sado | discipline ↔ Keras Hati | Judge axis (Permanence/Reversibility) |
| Makcik | care ↔ Kawal via Kepedulian | Memory axis (Light/Shadow) |
| Kanak-kanak | perception ↔ Hancur tanpa Faham Nilai | Mind axis (Local/Global) |

## Namespace

"Persona" here = cognitive function (not agent personality — see `federation-personality-taxonomy-2026-09-11.md`; not human register — see `instructions/hermes-shadow.md`). "Triad" here = persona cognitive triad (not constitutional functions, not warga triads, not musyawarah pattern, not KVM topology).
