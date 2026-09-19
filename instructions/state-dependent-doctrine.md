# State-Dependent Doctrine — Thermodynamic Phases of Engineered Systems

> **Status:** DRAFT_AWAITING_F13 — extracted from AGENT-STACK-2026 spec-kit vs OpenSpec contrast (2026-09-19)
> **Source eureka:** Greenfield and brownfield are not tool categories. They are thermodynamic states.
> **Applies to:** Tool selection, contract design, federation wiring, scar handling, mutation policy.
> **Filter test passed:** ✅ survives implementation changes ✅ re-examinable in 2 years ✅ not vendor-specific ✅ changes future architecture decisions ✅ not merely tool preference.

## The Observation

Two flagship spec-driven tools exist:

| Tool | Philosophy | Optimised for |
|---|---|---|
| **github/spec-kit** | Phase-gated, ceremonial, executable slash commands, constitution-first | Greenfield |
| **Fission-AI/OpenSpec** | Action-based, fluid, "deltas not rewrites", brownfield-first | Brownfield |

Read as competitors, they contradict. Read as **two thermodynamic states**, they are complementary:

```text
spec-kit    →  Low history, high freedom, low inertia     →  First architecture
OpenSpec    →  High history, high constraints, high scar   →  Evolution architecture
```

A system at first architecture has low inertia — easy to push into any direction. A system at evolution architecture has accumulated scar — mutations must preserve what history has earned.

## The Doctrine

The right mutation policy depends on the **state** of the system being mutated, not on the tool used to mutate it.

| State | History | Inertia | Mutation policy | Forbidden pattern |
|---|---|---|---|---|
| **Greenfield** | Low | Low | Bold, speculative, fast | Hoarding premature scars |
| **Brownfield** | High | High | Scar-preserving, delta-based, reversible | Rewriting from scratch |
| **Mature** | Very high | Very high | Consensus-driven, attestation-gated | Any mutation without receipt |
| **Catastrophic** | Variable | Variable | HOLD | Speculation |

These are **not phases in a lifecycle**. They are **observables that can co-exist** within the same system. A greenfield microservice may sit next to a brownfield monolith in the same federation.

## Why Spec-Kit and OpenSpec Are Not Competitors

| Concern | Greenfield answer (spec-kit) | Brownfield answer (OpenSpec) |
|---|---|---|
| *What should exist?* | ✅ spec-kit: constitution → specify → plan → tasks → implement | ❌ |
| *What should change?* | ❌ | ✅ OpenSpec: deltas → changes → merge |
| *Which is canonical?* | Both. State declares. |

A greenfield project using OpenSpec would over-document evolution that has not yet happened. A brownfield project using spec-kit would re-constitute what already exists. **The tool must match the state.**

## Federation Mapping

The federation has its own state-dependent machinery:

| State primitive | Federation answer |
|---|---|
| Greenfield | `arif_init(mode=init)` — fresh substrate, low scar-weight. |
| Brownfield | `arif_forge(mode=query)` — load canon before mutation. |
| Mature | `arif_seal` — receipt-anchored, immutable. |
| Catastrophic | `arif_judge(mode=hold)` — governance halt. |

The doctrine declares these are **state-conditional paths**, not interchangeable tools.

## Falsifiability

If "greenfield vs brownfield" is shown to be a false dichotomy (e.g., most real systems are always both), the doctrine needs subdivision. If the same tool can serve both without state-aware adaptation, the doctrine is over-specified.

## Related Doctrines

- State-Transition Discipline — PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ ACKNOWLEDGED.
- Consequence-Bearing Identity — actions have owners, owners have history.
- Trauma Theorem — scar-weight propagation, scar preservation.
- Six-Graph Federation Model — Reality is observed through state.

## Compression

> **Greenfield and brownfield are not tool categories. They are thermodynamic states. The mutation policy must match the state, not the tool.**

DITEMPA BUKAN DIBERI ⚒️