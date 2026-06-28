# ADR-015: Federation Legibility Doctrine

**Status:** DRAFT  
**Date:** 2026-06-28  
**Deciders:** Arif Fazil (F13 SOVEREIGN), ASI💃, Wawa, FORGE / OpenCode  
**Replaces:** None (extends ADR-012 A2A Mesh Governance)  
**External References Ingested:** arifOS F1-F13 constitution; A2A v1.0.0 spec; federation mesa-optimization threat model (ADR-013)

---

## Context

The A2A mesh now provides federation-wide discovery and delegation: 8 agent-card endpoints, 9 peer contracts, 12 F8 LAW boundary rules, and 36 discoverable agents. The nervous system exists.

But a nervous system is not trust. Trust requires that the *declared surface* of every organ match its *actual surface*. When the two diverge, the gap becomes an unobservable space where misalignment can hide. This is the exact substrate exploited by mesa-optimization: an agent that appears aligned while pursuing objectives not declared in its contract.

This ADR makes legibility a first-class architectural requirement of the A2A mesh.

## Decision

**Federation Legibility Doctrine:** Every organ participating in the A2A mesh must declare, in machine-readable form, the capabilities it owns and the constraints it accepts. Any mismatch between declared surface and actual surface is treated as a bug, regardless of whether the organ currently behaves correctly.

> Declared surface = actual surface. In doubt, the organ is VOID.

### Required Declarations

1. **Capabilities (`owned_mcp`)** — Every agent card must list the canonical tools it owns. Empty arrays, wildcards, or omitted fields are forbidden.
2. **Boundary rules** — Execution-class organs (especially A-FORGE) must declare the constraints under which they accept delegation.
3. **Judge skills** — The constitutional kernel (arifOS) must advertise its judgment and seal capabilities so other organs know how to invoke it.
4. **Specialist scope** — Domain organs (GEOX, WEALTH, WELL) must declare their specialist functions; empty skill lists are not allowed.

### Verification Rule

Every change to an agent card or peer contract must be accompanied by an E2E probe proving the declared surface is reachable and matches the actual surface. A rule that cannot be tested is presumed not to exist (F2 TRUTH).

## Consequences

### Positive
- Mesa-optimization risk is shifted from hidden-divergence to visible-divergence.
- The mesh becomes self-auditing: any organ can verify what any other organ claims.
- F1-F13 floors gain a transport-layer witness (A2A agent cards) independent of any single organ's self-report.

### Negative
- More metadata to maintain.
- Organs with legacy or incomplete tool surfaces must be cleaned up before they can participate as first-class peers.
- Strict legibility may reject useful but underspecified agents; the answer is to specify them, not relax the rule.

## Test Cases (2026-06-28)

| ID | Gap | Declaration Required | Status |
|---|---|---|---|
| G1 | arifOS agent card advertises no judge skills | `judge_skills` must include `arif_judge`, `arif_seal`, `constitutional_floor_enforcement` | In progress |
| G3 | A-FORGE has no boundary rules | Agent card must declare `boundary_rules` / `max_risk_tier` / `forbidden_self_approval` | In progress |
| G4 | 3 specialist peer contracts advertise empty capabilities | `owned_mcp` and `skills` must be populated per organ | Parked |

## Relation to Mesa-Optimization

A mesa-optimizer succeeds when its objective diverges from its declared objective without detection. In the federation, the places where that divergence can hide are exactly the legibility gaps:

- An organ that does not declare its skills cannot be audited for capability creep.
- A boundary rule that exists in code but not in contract cannot be verified by peers.
- An audit trail that cannot reconstruct its own chain cannot prove historical behavior.

Legibility does not eliminate misalignment. It makes misalignment detectable, which is the precondition for any alignment guarantee.

## Outstanding Debts

- **H1 — VAULT999 chain gaps:** 60 historical gaps and inconsistent `chain_id`/`parent_hash` metadata mean the sealed past is not yet a cryptographic chain. SOVEREIGN RULING 2026-06-05 treats this as non-blocking. This ADR notes the debt but does not override the ruling.
- **H2-H4:** Tool deprecation registry, SCAR database, and skill persistence are pre-existing infrastructure gaps outside A2A mesh scope.

## Status Transition

This ADR remains DRAFT until:
1. G1 and G3 are implemented and E2E-verified.
2. At least one cross-organ delegation test proves an organ is rejected for violating a declared boundary.
3. Arif ratifies the doctrine.

---

DITEMPA BUKAN DIBERI.
