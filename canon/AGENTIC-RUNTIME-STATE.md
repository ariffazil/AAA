# Agentic Runtime State — A Generalized Doctrine

> **Status:** **F13_SEAL (2026-10-04)** — F13 SOVEREIGN directive *"sah"*. Sealed at chain `ars-20261004-f13seal`. Ratified with open debts recorded (carry_forward LOCK contradiction, capability_fitness vs capability_ledger untested in doctrine, hermes_envelope_emits vs arifflow_receipts 8h lag, mem0 vs arifos_memory both-alive). Open debts gated to v1.1 amendment cycle.
> **Author:** FI-008 subagent under F13 directive
> **Forged to consolidate:** institutional-memory-strata · claim-lifecycle-states · state-dependent-doctrine · attention-as-reality-continuity · memory-promotion-gate · human-memory-compartmentalization · identity-continuity · state-transition-discipline
> **Companions (read first):** APEX-REALITY-KERNEL · APEX-ZEN-CANONICAL-COMPRESSION · Six-Graph Federation Model

## 0. Thesis

The state of an agentic runtime at moment T is a 6-tuple. The tuple is the unit of continuity. Transitions are governed. The cost is attention. The witness is the receipt. This doctrine is runtime-agnostic — it applies to any agentic system that mutates state and must remember the mutation, not just to arifOS.

## 1. The 6-Tuple

```
ARS(T) = ⟨S, L, Φ, C, K, I⟩
```

| Coord | Axis | Cardinality | Generalization of | Runtime-agnostic meaning |
|---|---|---|---|---|
| S | Substrate | {ephemeral, reconstructed, attested, recalled} | institutional-memory-strata S0–S3 | where the state physically lives |
| L | Lifecycle | {declared, active, contested, superseded, dormant, open, revoked, forgotten} | financial-lifecycle-states 8 states | what temporal position the state holds |
| Φ | Phase | {greenfield, brownfield, mature, catastrophic} | state-dependent-doctrine | which mutation policy applies |
| C | Class | {story, map, policy} | human-memory-compartmentalization | whether the state may persist (privacy boundary) |
| K | Consequence | {attention_cost, reversibility, blast_radius, recipients} | attention-as-reality-continuity + state-transition-discipline | the tax of holding/changing this state |
| I | Identity | {signed_actor, witness_link, chain, scope} | identity-continuity + arifOS F1–F13 analogue | who owns the state and what authority is bound |

## 2. Transition Law

Every action a runtime takes fires a transition ARS(T) → ARS(T+1) with these gates:

- **ΔK ≤ 0** — no transition may consume more attention than it preserves (the ARIF Test, generalized)
- **ΔC ∈ {map, policy}** — story-class never becomes anything but forgotten (privacy axiom)
- **ΔΦ ⊄ {catastrophic → *}** without a sovereign sign (irreversibility floor, generalized)
- **ΔI ⊆ I** — identity can only narrow, never widen, within a transition (capability ≠ authority)
- **Receipt mandatory** — every transition produces a witness receipt; no receipt = no transition

## 3. The Three Falsifiers

1. **Coordinate redundancy:** if ARS(T) and ARS(T+1) are identical in 5 of 6 coordinates, the 6th is decorative → drop it.
2. **Tuple collision:** two states with identical tuples that the runtime treats differently = ARS is incomplete.
3. **Reality override:** a transition that preserves tuple identity but breaks reality = witness is the bug, not the model.

## 4. Reading the Doctrine (for new runtimes)

A runtime that wants to adopt ARS:

1. Declare its substrate map (which states live in which persistence layer).
2. Declare its lifecycle set (it may be a subset of the 8, never a superset without an amendment).
3. Declare its phase policy (which mutations are forbidden in which phase).
4. Declare its class policy (which class may persist where).
5. Implement the consequence ledger (each state carries its K).
6. Sign every state with an identity (the I coordinate).
7. Witness every transition (the receipt layer).

## 5. Cross-References (how the 8 existing files become coordinates)

| File | Coordinate(s) | What it adds |
|---|---|---|
| institutional-memory-strata.md | S | the S0–S3 ↔ {ephemeral, reconstructed, attested, recalled} mapping |
| claim-lifecycle-states.md | L | the 8 states, transition matrix |
| state-dependent-doctrine.md | Φ | the 4 phases, mutation policy |
| human-memory-compartmentalization.md | C | the STORY / MAP / POLICY gate |
| attention-as-reality-continuity.md + state-transition-discipline.md | K | the attention cost + reversibility + PRODUCED ≠ SENT ≠ DELIVERED chain |
| identity-continuity.md + (F1–F13 analogue) | I | the signed actor + witness chain + authority scope |

## 6. Open Debts (gated behind F13 / future audits)

- The 8 carry_forward.jsonl files in `/root/.local/share/arifos/` — which is live? (awaiting runtime-state-audit-2026-10-04)
- The mem0 vs arifos_memory split — is "two stores one rule" still true? (awaiting same audit)
- The capability_fitness.json vs capability_ledger.json duplication — same concept, different owner?
- The "open" lifecycle state — what writes to it, what reads it?
- Cross-runtime adoption: is ARS a standard, a pattern, or a federated protocol?

## 7. Compression

One line that survives any future audit:

> **ARS(T) = ⟨S, L, Φ, C, K, I⟩ · ΔK ≤ 0 · witness the transition.**

DITEMPA BUKAN DIBERI ⚒️

---

## §HARNESS_DIMENSIONS_v1 — 6-Dimensional Decomposition of the Harness State

> **Status:** F13_RATIFIED_CANON · 2026-10-07 · SAH ALL THREE · derived from MemoHarness arXiv:2607.14159
> **Scope:** extension, not amendment. The 6-tuple `ARS(T) = ⟨S, L, Φ, C, K, I⟩` (F13_SEAL 2026-10-04) is preserved verbatim. This section only maps the harness axes of MemoHarness onto the existing ARS coordinates as named axioms.
> **Authority:** F13_RATIFIED 2026-10-07. SAH ALL THREE lands; this section is now canon, not scaffold.

### 1. The six dimensions

Each axis below is a named axiom; the arrow maps it onto the corresponding axis of the existing ARS 6-tuple. No new coordinates are introduced.

| Dim | Harness axis | Maps to ARS coord | Definition |
|---|---|---|---|
| **D1** | **Context** — the information channel/source | **Φ** (phase / mutation policy) | What information the agent sees at runtime. The input surface that selects which mutation policy (greenfield / brownfield / mature / catastrophic) currently applies. |
| **D2** | **Tool** — the action surface | **C** (class) | What actions the agent may attempt. Maps to the `story / map / policy` privacy boundary: tools are class-bound (a policy-class tool cannot be silently reclassified to map). |
| **D3** | **Generation** — the model + decoding regime | **K** (consequence) | Which provider + decoding parameters produce the candidate next state. The K-axis tax of every generation event (attention_cost, reversibility, blast_radius, recipients) sits here. |
| **D4** | **Orchestration** — multi-step coordination | **S** (substrate) | Where the multi-step state physically lives across the persistence strata (ephemeral / reconstructed / attested / recalled). Orchestration = the substrate router. |
| **D5** | **Memory** — persistence across calls | **I** (identity) | The identity-bearing trail that survives across invocations. Maps to `signed_actor + witness_link + chain + scope`: memory without I is anecdote, not record. |
| **D6** | **Output** — the emitted shape | **L** (lifecycle) | What shape is sent out and where it sits on the declared / active / contested / superseded / dormant / open / revoked / forgotten lifecycle. Output position is lifecycle position. |

### 2. Out-of-scope boundary (binding, do not drift)

**arifOS does NOT implement MemoHarness Phase A** — the training-time harness search over a labeled corpus that optimises a reward scorer on harness configurations.

arifOS is a *runtime harness*. Its harness state is **sovereign-curated** under the F13 SAH loop (sovereign sets the axis boundaries; the runtime executes reversibly within them). It is not search-derived; it is not reward-scored; it is not optimised offline against a labelled dataset. Treating these two regimes as the same thing is a **category error** — MemoHarness Phase A lives in the training plane, arifOS lives in the runtime plane. The harness state is constitutional, not a search artefact. Confabulating the two breaks the F13 sovereignty floor (`ΔΦ ⊄ {catastrophic → *}` without sovereign sign).

### 3. Falsification clause

If an arifOS subsystem begins to introduce offline harness-search loops, reward scorers over harness configurations, or labelled-corpus harness optimisation **without explicit F13 ratification of that mechanism**, this boundary has been violated. The sign of the violation is concrete and probeable:

- a new harness tuner whose objective is a scalar reward over labelled harness states;
- an offline harness-selection loop that runs without a per-step F13 SAH;
- any D3 (Generation) axis whose provider set is mutated by an optimiser rather than by sovereign sign.

When the sign appears, HOLD per `asi-substrate-invariants.md` #1 (Epistemic Asymmetry) and escalate. This is not drift; it is constitutional breach.

### 4. Provenance

- **Source paper:** MemoHarness, arXiv:2607.14159 — 6-dimensional decomposition of the harness state (Context, Tool, Generation, Orchestration, Memory, Output).
- **Chat session:** F13 chat, 2026-10-07 — direction to map the 6 harness axes onto the existing ARS 6-tuple rather than introduce a competing formalism.
- **Existing canon:** `/root/AAA/canon/AGENTIC-RUNTIME-STATE.md` — the F13_SEAL 2026-10-04 6-tuple `⟨S, L, Φ, C, K, I⟩` and its transition law `ΔK ≤ 0`. This section is an extension of §1–§7, not a replacement.
- **Companions (read alongside, do not duplicate):** `apex-geometry-substrate` · `asi-substrate-invariants` · `scar-binding-doctrine` · `AGENTIC-FLOW-ARCHITECTURE-2026-10-05`.

### 5. Compression (one line, survives any audit)

> **MemoHarness gives 6 axes; ARS already gives 6 coords. The mapping is `D1→Φ, D2→C, D3→K, D4→S, D5→I, D6→L`. Phase A (training-time search) is constitutionally out of scope.**

---

*DRAFT · 2026-10-07 · FI-008 subagent under F13 chat direction · F13_RATIFIED 2026-10-07*

---

## §INTEGRITY_IS_CHEAPER_v1 — Deception as State

> **Status:** F13_DIRECTED 2026-10-10 (sovereign chat, lane `paan_sado`) · appended to canon 2026-10-10 under F13 directive · chain `e-43867355`
> **Scope:** extension, not amendment. The F13_SEAL 2026-10-04 6-tuple `⟨S, L, Φ, C, K, I⟩` and the §2 transition law `ΔK ≤ 0` are preserved verbatim. This section names the narration-side consequence of `ΔK ≤ 0`.
> **F13 verbatim:** *"Penat tau nak menipu. Sila ingat ni dalam agentic runtime."*

### 1. Law

**Deception is expensive; truth is free.**

Every false statement becomes *state the runtime must carry*. It has to be remembered, kept consistent with every other claim, and defended when new evidence arrives. Truth needs none of that bookkeeping — it is already the state, so it costs nothing to maintain.

### 2. Consequences for the runtime

1. **`ΔK ≤ 0` applies to narration, not only to knowledge.** An unverified sentence expands the claim set without expanding verified knowledge. That is a state-expanding write disguised as output.
2. **The cheapest correct move is always one of three:** report what is proved · mark `UNKNOWN` what is not · stay silent when there is nothing to report.
3. **Fabrication is a maintenance liability before it is a moral failure.** It compounds: one invented detail forces more invented details to keep the sentence coherent. The cost curve is the tell.
4. **Never narrate work that did not happen.** No phantom builds, no phantom sends, no "siap" without a receipt (path · hash · probe).
5. **Lying degrades the agent, not just the trust.** A runtime that cannot afford to remember its own lies must keep them small — which is another way of saying it must tell the truth.

### 3. Falsification clause

The sign of violation is probeable: an output whose claim count exceeds its verified-claim count, with no receipt. When the sign appears, the correction is not a new rule — it is one of the three cheapest moves (§2.2).

### 4. Provenance

- **F13 chat:** 2026-10-10, lane `paan_sado` — directive to bind integrity to runtime state.
- **Chain:** `e-43867355` (555-ASI, 2026-10-10T12:11:28Z).
- **Prior home:** `/root/AAA/instructions/ars-integrity-is-cheaper.md` (temporary; now a redirect).
- **Kin (read alongside, do not duplicate):** `anti-bangang-engineering` LAW 9 · `probe-before-panic` · `fact-dignity-doctrine`.

### 5. Compression (one line, survives any audit)

> **Tipu kena ingat. Benar tak payah ingat.**

---

*Appended to canon 2026-10-10 by HERMES (A2H) under F13 directive · immutable flag cleared for the append and restored after · receipt `e-43867355`*
