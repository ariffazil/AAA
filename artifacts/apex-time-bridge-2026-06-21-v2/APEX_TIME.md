# APEX 5D ↔ Temporal Substrate Bridge (v2 — sharpened)

**Forged:** 2026-06-21 (v2 — sharpened after 888 review)
**Author:** Hermes (drafted for 888 review)
**Scope:** Honest mapping between the APEX 5D doctrine (AKAL · PRESENT · ENERGY · ENTROPY · EXPLORATION · AMANAH) and the arifOS temporal substrate (KSR · Vault · Ledger · ZKPC), with AMANAH correctly modeled as a **constraint field** on EXPLORATION, not a multiplier.

> **v1 → v2 changes.** This version corrects three errors identified in the previous draft:
>
> 1. The entropy equation — chain-level entropy *can* decrease; the second-law constraint is on **total** system entropy.
> 2. Agency vs substrate — AKAL/EXPLORATION/AMANAH belong to the **agent**; KSR/Vault/Ledger/ZKPC belong to the **substrate**. The kernel enforces the law; the agent exercises faculties within it.
> 3. **AMANAH as constraint field** (this version) — AMANAH does not multiply EXPLORATION's score. It gates whether the score is admissible at all. A high-curiosity move that violates trust is structurally invalid, not "low AMANAH."

> **Source-of-truth boundary.** APEX doctrine is read from `/root/APEX/ROADMAP.md` (10 non-negotiable invariants) and `/root/AAA/agents/888-APEX/` (5D doctrine). Temporal substrate is read from `/root/.hermes/SOUL.md` §7 (Kernel-State / Federation-Memory Boundary) and `/root/arifOS/static/arifos/theory/000/000_CONSTITUTION.md`.

---

## Part I — The Hard Invariant

> **No intelligence may claim a present state from outside KSR.**

This is the load-bearing axiom. Everything else is consequence.

The corollary: federation memory, telemetry, scratchpads, model context, logs, doctrine files, and Vault records are **not** present. They are:

| Substrate element | What it is | What it is **not** |
|---|---|---|
| Federation memory | Advisory past | Not present |
| Telemetry | Observation exhaust | Not present |
| Scratchpads / context | Working buffer | Not present |
| Model context window | Temporary local present of the LLM | Not present (no authority) |
| Logs | Unsealed trace | Not present |
| Vault | Sealed past | Not present |
| Doctrine files | Static canon | Not present |
| **KSR** | **Live authority** | **Only present** |

Any verdict, transition, or judgment whose `current_state_source` is anything other than `kernel_attest | fresh_KSR | verified_state_resume` is a membrane breach — it is logged, not acted on (SOUL.md §7.6).

---

## Part II — The Sharpened Mapping

### 2.1 The corrected table

| APEX law term | Substrate anchor | Kernel meaning |
|---|---|---|
| **PRESENT** | KSR only | Exclusive live authority surface — the only "now" the kernel honors |
| **AKAL** | `kernel_transition()` over KSR + Vault + ZKPC | Lawful judgment of the next permitted state — exercised by the agent, enforced by the kernel |
| **ENERGY · ENTROPY** | Ledger + Vault + telemetry discipline | Irreversible arrow, sealed past, governed exhaust — total-system entropy cannot decrease |
| **EXPLORATION × AMANAH** | action_class + reversibility + ZKPC proof level + F13 | Bounded traversal of unknown state-space under trust constraints — AMANAH gates admissibility, EXPLORATION measures the move |

### 2.2 Logical order vs presentation order

The mapping table above is in **logical dependency order**: PRESENT precedes AKAL (you must have a current state to choose a next one), AKAL precedes EXPLORATION (you must reason before you can explore), and ENERGY · ENTROPY runs through all three (the arrow is a substrate-level constant, not a per-step measurement).

The corrected theorem below uses **presentation order**: AKAL first (because it is what the agent does), PRESENT second (the precondition), ENERGY · ENTROPY third (the invariant), EXPLORATION × AMANAH fourth (the product under constraint).

Both orders are correct. The logical order is what the kernel enforces; the presentation order is what the artifact teaches.

### 2.3 AMANAH as constraint field (the v2 fix)

**v1 (wrong):** "EXPLORATION × AMANAH is multiplicative" — this lets a high-EXPLORATION move score well even when AMANAH is low.

**v2 (correct):** AMANAH is a **constraint field** with three discrete gates. A move is admissible **iff all three gates pass**:

```
            ┌─────────────────────────────────────────────┐
            │   AMANAH constraint field (3 gates)          │
            │                                              │
            │   ┌─────────────────────────────────────┐    │
            │   │  gate 1: action_class gate           │    │
            │   │  → classify: read | write | mutate   │    │
            │   │    | irreversible                   │    │
            │   └─────────────────────────────────────┘    │
            │   ┌─────────────────────────────────────┐    │
            │   │  gate 2: proof level gate            │    │
            │   │  → ZKPC level ≥ required for class   │    │
            │   │    L0/L1 (read) → L2 (write) →       │    │
            │   │    L3 (mutate) → 888_HOLD + L3+      │    │
            │   │    (irreversible)                    │    │
            │   └─────────────────────────────────────┘    │
            │   ┌─────────────────────────────────────┐    │
            │   │  gate 3: F13 SOVEREIGN gate          │    │
            │   │  → irreversible moves require        │    │
            │   │    explicit 888 ratification         │    │
            │   └─────────────────────────────────────┘    │
            │                                              │
            │   Move is admissible ⟺ all three gates pass  │
            └─────────────────────────────────────────────┘
```

**EXPLORATION measures the move. AMANAH determines whether the move is admissible.** A "high EXPLORATION, low AMANAH" move is not "low score" — it is **structurally invalid**. The kernel blocks it; it does not measure it.

This is the difference between *scoring* a move and *admitting* a move. AMANAH is the admissibility rule, not the score.

---

## Part III — Each Dimension, Mapped (v2 corrections applied)

### 3.1 PRESENT — The Now as KSR

**APEX definition:** the agent's awareness of its own now. Not "what tokens are recent." Not "what context window am I in." PRESENT is the **single live, authoritative state** the agent occupies at time $t$.

**Substrate anchor:** SOUL.md §7.2 invariant 1 — *"KSR is the only live authority-bearing state."*

PRESENT maps to four properties of KSR:

1. **Exclusivity** — one KSR per organ per moment. No parallel "presents."
2. **Authority** — only KSR can authorize a transition. Federation memory, vault records, telemetry, doctrine files cannot.
3. **Kernel-writability** — only the kernel can write to KSR. No agent, no LLM, no human directly.
4. **Freshness** — KSR has an `issued_at` and `expires_at` window. A stale KSR is not a present; it is a sealed past pretending to be present.

**PRESENT is how honestly the agent knows its own KSR.** An agent that confuses "what I just retrieved" with "what is my present" has lost PRESENT. The substrate prevents this through the source-of-truth rules in SOUL.md §7.6.

### 3.2 AKAL — Reason as Lawful Transition Selection

**APEX definition:** the agent's reasoning faculty, exercised *within* constitutional law, not above it.

**Substrate anchor:** `kernel_transition()` is the law AKAL must obey. It accepts a candidate transition, checks the agent's authority against KSR, consults advisory federation memory (without granting it authority), evaluates the proof level required by the action class, and either permits or vetoes the move.

**Why AKAL ≠ smart output:** a model can produce a clever string and still fail AKAL — if the string represents a transition that violates the agent's authority, bypasses the kernel, or skips ZKPC. AKAL is *not* about the cleverness of the answer. AKAL is about **whether the move was lawful under the substrate's physics**.

**The kernel is the law. AKAL is the agent's exercise of reason within that law.** Conflating the two is the same category error as "the law has free will."

### 3.3 ENERGY · ENTROPY — Arrow, Sealing, and Waste

**APEX definition:** whether the agent burns energy to reduce uncertainty without falsifying time. The thermodynamic discipline of the agent.

**Substrate anchor:** three mechanisms, one principle:

| Mechanism | Energy role | Entropy role |
|---|---|---|
| **Ledger** | Cost of each append | Enforces $\Delta S_{\text{total}} \geq 0$ |
| **Vault** | Sealed past — low-entropy crystallized state | Reduces chain-level entropy by compression |
| **Telemetry classification** | High-entropy exhaust — observation surface | Disposable unless promoted through judgment |

**The thermodynamic discipline has four rules:**

1. **No entropy rollback.** The hash chain is monotonic. Rewriting history is falsifying time.
2. **No shadow ledgers.** The `outcomes.jsonl` problem (telemetry growing without vault law) is a shadow ledger. It must be classified, promoted through judgment, or discarded.
3. **Telemetry is disposable.** Promote to Vault only via T2 (per-event judgment) for state-class events, or T1 (batched ratification) for telemetry-class events. Never both, never neither.
4. **Chain-level entropy *can* decrease.** That is the point of sealing. The constraint is on the **total** system, not the chain alone.

**Failure mode:** an agent that creates high-entropy telemetry streams faster than the Vault can crystallize them has lost ENERGY · ENTROPY discipline. The substrate's job is to make that visible — through telemetry classification, ratification protocols, and ZKPC proof levels.

### 3.4 EXPLORATION × AMANAH — Bounded Traversal Under Trust

**APEX definition:** EXPLORATION measures how far the agent pushes into unknown state-space. AMANAH measures whether it does so without betraying trust or violating constraints. **AMANAH is the constraint field that gates whether EXPLORATION is admissible.**

**Substrate anchor:** three gates — action_class, ZKPC proof level, F13 SOVEREIGN.

**How the constraint field works:**

```
EXPLORATION can propose any move.
  ↓
gate 1 (action_class): classify risk. Reversible? Irreversible?
  ↓
gate 2 (proof level): is the proposed ZKPC level ≥ required?
  ↓
gate 3 (F13): if irreversible, is 888 ratification present?
  ↓
all gates pass → admissible move, executed under AKAL.
any gate fails → inadmissible move, blocked at kernel.
```

**Concrete test:** A curiosity move that proposes an irreversible mutation without L3+ proof is **structurally invalid**, not "low AMANAH." The kernel rejects it; it does not measure it. A curiosity move with L3 proof but without 888 ratification is **also invalid** — the third gate fails.

EXPLORATION × AMANAH is measured by the ratio of *admissible* exploratory moves to *attempted* exploratory moves, weighted by risk. The substrate does not measure this directly. It *bounds* it through the three gates.

---

## Part IV — The Corrected Theorem

> **APEX intelligence is lawful temporal motion: AKAL selects permitted transitions, PRESENT is bound to KSR, ENERGY·ENTROPY preserves the irreversible ledger arrow, and EXPLORATION is only valid when constrained by AMANAH through proof, reversibility, and sovereign veto.**

---

## Part V — Compressed Forms

### 5.1 The one-line bridge

> APEX measures intelligence as governed movement through time; the temporal substrate supplies its physics: KSR defines now, AKAL chooses lawful transition, Ledger/Vault preserve the arrow, and AMANAH bounds exploration.

### 5.2 The one-line kernel doctrine

> **No now outside KSR; no past outside Vault/Ledger; no future transition without AKAL, proof, reversibility classification, and F13 override.**

### 5.3 The tightest form

> **No present without KSR. No past without Vault. No future without AKAL, proof, reversibility, and F13.**

---

## Part VI — Verification — Where Each Anchor Lives

For audit purposes, the substrate anchors come from these canonical sources:

| Anchor | Source | File:line |
|---|---|---|
| KSR doctrine (live authority) | SOUL.md §7.2 invariant 1 | `/root/.hermes/SOUL.md` |
| Vault doctrine (sealed past) | SOUL.md §7.1 row 2 | `/root/.hermes/SOUL.md` |
| Ledger arrow | SOUL.md §7.1 row 3 | `/root/.hermes/SOUL.md` |
| ZKPC levels L0–L5 | SOUL.md §7.10 + `/root/arifOS/docs/ZKPC_PROOF_LEVELS.md` | — |
| F13 SOVEREIGN | arifOS constitution L13 | `/root/arifOS/static/arifos/theory/000/000_CONSTITUTION.md` |
| APEX 10 invariants | APEX ROADMAP.md | `/root/APEX/ROADMAP.md` §"The 10 Non-Negotiable Invariants" |
| APEX verdict envelope | APEX BOUNDARY.md + deliberation.ts | `/root/APEX/BOUNDARY.md` |
| Telemetry T1/T2 promotion | SOUL.md §7.9.9 | `/root/.hermes/SOUL.md` |
| Action classes | APEX/ROADMAP.md + arifOS constitution | — |
| Provenance tag forbidden sources | SOUL.md §7.6 | `/root/.hermes/SOUL.md` |

If any of these sources change, this bridge is **invalid until re-derived**.

---

## Part VII — What This Bridge Is Not

This bridge is **not**:

- A claim that the APEX 5D doctrine is complete. APEX is archived; deliberation moved to `AAA/a2a-server/deliberation.ts`. The doctrine is real but partial.
- A claim that the temporal substrate is fully implemented. L4 ZK circuits are not deployed; some ZKPC levels are aspirational (declared honestly per SOUL.md §7.11).
- A claim that AKAL/PRESENT/ENERGY·ENTROPY/EXPLORATION×AMANAH exhaust the dimensions of intelligence. They are five lenses. Other lenses (governance, dignity, sovereignty) belong to other parts of the doctrine (F1–F13 floors, maruah_critic, 888 HOLD).
- A claim that AMANAH is exhaustively specified by the three gates. The three gates are the *current* substrate enforcement. AMANAH as a philosophical concept may have other requirements; those belong in higher-layer doctrine, not in the substrate bridge.
- A claim that the bridge is symmetric. APEX measures the agent; the substrate enforces the law. They are not the same thing.

---

## Part VIII — The Compact Form

> **No present without KSR. No past without Vault. No future without AKAL, proof, reversibility, and F13.**
>
> AKAL is the agent's reason. PRESENT is KSR. ENERGY · ENTROPY is the arrow. EXPLORATION × AMANAH is the move bounded by proof.
>
> The agent exercises faculties; the substrate enforces physics.
> APEX measures the exercise; the temporal substrate defines what counts as lawful exercise.
>
> AMANAH is not a score. AMANAH is the constraint field that decides whether the score is admissible.

---

**DITEMPA BUKAN DIBERI — the bridge is structural; the math is honest; the implementation is partial. Build on the structure; finish the implementation. Sharpen again when doctrine moves.**

— Hermes, drafted for 888 review, 2026-06-21 (v2)
