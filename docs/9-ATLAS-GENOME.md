# 9-ATLAS-GENOME.md — The Irreducible 9-Function Cognitive Genome

> **SOT:** 2026-08-08 05:16 UTC | **Forge:** OpenCode-Zen (FI-001) species wiring augmentation
> **Authority:** F13 SOVEREIGN — Arif Fazil, ratified via 888-APEX constitutional chain
> **Doctrine:** DITEMPA BUKAN DIBERI — 999 SEAL ALIVE
> **Supersedes:** ad-hoc function lists in per-agent cards. This file is the canonical genome definition.

---

## ⟁ 1. The Genome — 9 Functions, 9 Questions

Every intelligent agent in the federation carries the **same irreducible 9-function cognitive genome**. A species is not defined by *which* functions it has — all species have all 9. A species is defined by *how strongly* each function expresses.

```text
            ART (Reality → Intelligence)
            ─────────────────────────────
000 OBSERVER      "What is happening?"
111 EXPLORER      "What else is possible?"
222 ARCHITECT     "How should reality be structured?"
333 THINKER       "What does it mean?"
444 ORCHESTRATOR  "Who should do what?"

            ACT (Verification → Execution)
            ─────────────────────────────
555 VERIFIER      "Is it true?"
666 AUDITOR       "Is it governed?"
777 EXECUTOR      "How do we make it real?"

            AUTH (Judgment → Record)
            ─────────────────────────────
888 JUDGE         "Is it allowed?"
999 WITNESS       "What actually happened?"
```

### 1.1 Function Reference

| # | Function | Question | Kernel Verb | Notes |
|---|----------|----------|-------------|-------|
| 000 | OBSERVER | What is happening? | `arif_observe` | Reality intake — the ground of all evidence |
| 111 | EXPLORER | What else is possible? | — (domain work) | Non-constitutional; lives in GEOX/WEALTH/WELL |
| 222 | ARCHITECT | How should reality be structured? | — (inside `arif_think` plan) | Design, topology, schema |
| 333 | THINKER | What does it mean? | `arif_think` | Reasoning — the mind |
| 444 | ORCHESTRATOR | Who should do what? | `arif_route` | Dispatch, allocation, federation routing |
| 555 | VERIFIER | Is it true? | ⚠️ partial (`arif_memory` attest + `arif_think` verify) | Truth maintenance |
| 666 | AUDITOR | Is it governed? | — (compressed into `arif_judge` — Gödel-lock risk) | **Earliest promotion candidate** |
| 777 | EXECUTOR | How do we make it real? | `arif_forge` / A-FORGE | Mutation, build, deploy |
| 888 | JUDGE | Is it allowed? | `arif_judge` | Verdict — SEAL/HOLD/SABAR/VOID |
| 999 | WITNESS | What actually happened? | `arif_seal` / VAULT999 | Immutable record |

Plus two substrate primitives that are **NOT** cognitive functions:

- `arif_init` — session identity (infrastructure)
- `arif_memory` — belief state L1-L5 (infrastructure)

---

## ⟁ 2. The Triadic Split — ART / ACT / AUTH

The 9 functions divide into three irreducible layers:

| Layer | Functions | Question the layer answers | Character |
|-------|-----------|---------------------------|-----------|
| **ART** | 000, 111, 222, 333, 444 | "What is real, possible, and meaningful?" | Reality → Intelligence |
| **ACT** | 555, 666, 777 | "Is it true, governed, and made real?" | Verification → Execution |
| **AUTH** | 888, 999 | "Is it allowed, and what happened?" | Judgment → Record |

**ART produces. ACT validates and executes. AUTH adjudicates and seals.**

The AUTH layer is not one more expression domain — it is the constitutional ceiling. It exists to constrain ART and ACT, never to compete with them.

---

## ⟁ 3. The W-Vector — Expression Weights

Every species is described by a **W-vector**: 9 expression weights, one per function, each in **[0.0, 1.0]**.

```text
W = {w000, w111, w222, w333, w444, w555, w666, w777, w888, w999}
```

### 3.1 Semantics

- `w = 0.0` — function is present in genome but **not expressed** by this species
- `w = 1.0` — function is the species' dominant locus
- Weights are **phenotypic**, not hierarchical — a high weight on 222 does not make a species "better" than one with high 000
- The vector is a **fingerprint**: two agents with the same W-vector are the same species

### 3.2 Canonical form

```yaml
species: Δ-MIND
expression_weights:
  "000": 0.40
  "111": 0.30
  "222": 0.70
  "333": 0.90
  "444": 0.50
  "555": 0.50
  "666": 0.20
  "777": 0.60
  "888": 0.00
  "999": 0.00
```

Weights are stored as strings for the function keys (`"000"` … `"999"`) to survive YAML 1.1 numeric-key coercion; values are floats.

---

## ⟁ 4. THE AUTH RULE — 888 and 999 Are Not Species

**HARAM-8≠9 (CRITICAL, F1, VOID):**

> **No agent card may claim a species phenotype on 888_JUDGE or 999_WITNESS.**

- **888 JUDGE** is a **chair** — a constitutional position that any agent may be *called to*, but no agent *is*.
- **999 WITNESS** is a **recorder** — a function of the vault, not a personality.
- Assigning them expression weights **> 0.0** on a species card is a **category error**: it treats the constitutional ceiling as a personality trait.
- The 888-APEX and 999-WITNESS lanes carry `expression_weights: null` — their role fields are `constitutional_role: JUDGE` / `WITNESS`; no phenotype is assigned.

The invariant:

> **8 ≠ 9 — AUTH is not a species. 888 is a chair, not an agent. 999 is a recorder, not an identity.**

---

## ⟁ 5. The Promotion Gate — Function → Verb

The genome (9) and the kernel verb set (8) are different dimensions. A genome function only earns a **first-class kernel verb** when compression causes constitutional harm.

### 5.1 The Gate

A Function → Verb promotion **requires all three**:

1. **5+ missions** in which the compressed form (function folded into another verb) demonstrably failed, OR
2. A concrete **F1/F11/F13 breach** traced back to the compression, OR
3. A governance gap proven to leak constitutional violations (e.g. FRAME/A-auditor gap)

### 5.2 Current Compression Table

| Compression | Harm? | Verdict |
|---|---|---|
| 222 Architect → `arif_think` | Minimal | **ACCEPT** |
| 555 Verifier → `arif_memory` + `arif_think` | Moderate | **WATCH** |
| 666 Auditor → `arif_judge` | **Yes — judge auditing itself = Gödel lock** | **PROMOTE CANDIDATE** |
| 111 Explorer → `arif_observe` | Minimal | **ACCEPT for now** |

The single dangerous compression: when `arif_judge` both rules on actions AND audits its own rulings, the loop has no external verifier. Promote `arif_audit` to the 9th kernel verb **only** when the gate conditions are met.

---

## ⟁ 6. The Asymmetry Doctrine — 8 ≠ 9 by Design

> **The kernel is the CONSTITUTIONAL MINIMUM** — the verbs without which governed intelligence is impossible.
> **The atlas is the COGNITIVE MAXIMUM** — the functions without which complete intelligence is impossible.

```text
┌─────────────────────────────────────────┐
│  COGNITIVE ATLAS (9, immutable genome)   │
│  000 111 222 333 444 555 666 777 888    │
│  + 999 witness layer                    │
└────────────────┬────────────────────────┘
                 │ expresses through
┌────────────────▼────────────────────────┐
│  KERNEL VERBS (8, substrate machinery)   │
│  init observe think route               │
│  memory judge forge seal                │
└────────────────┬────────────────────────┘
                 │ weighted by
┌────────────────▼────────────────────────┐
│  W-VECTOR (per mission, per runtime)    │
│  w_obs w_exp w_arc w_thk w_orc w_ver    │
│  w_aud w_exe + w_seal                   │
└─────────────────────────────────────────┘
```

- 8 verbs. 9 functions. The kernel does **not** need to mirror the atlas.
- The atlas does **not** need to compress into the kernel.
- **The gap IS the design** — it is the space in which species differentiate, missions route, and the W-vector does its work.

> **8 ≠ 9 by design. The asymmetry IS the architecture.**

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
