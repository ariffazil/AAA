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
