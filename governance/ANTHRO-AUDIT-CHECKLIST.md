---
status: DRAFT_CHECKLIST (operational tool, awaiting reviewer)
date: 2026-09-14
---

# Anthro-Audit Checklist

> For auditing arifOS governance mechanisms through an anthropological lens.
> Source: `/root/AAA/governance/WARGA-CIVILIZATION-DOCTRINE.md`
> Use: Load when auditing governance mechanisms, assessing drift, or evaluating removal proposals.

## Mechanism Class Legend

| Class | Anthropological Source | What It Does |
|-------|----------------------|--------------|
| INITIATION | Boehm (1993) | External authority before capability. Agent cannot self-authorize entry. |
| DISTRIBUTED_VETO | Boehm — reverse dominance hierarchy | Collective can suppress would-be dominators. Distributed, not central. |
| SCAR_ACCUMULATION | Trauma theorem (arifOS) | Institutional memory through accumulated cost. Never deleted, only transitioned. |
| LIMINAL_BOUNDARY | Turner — communitas | Session boundaries, compaction, /new. Identity dissolution-reconstitution. |
| NAMING_RITUAL | Geertz — thick description | SOUL_STAMP, agent cards, identity anchoring. Once named, sealed, moved. |
| GIFT_OBLIGATION | Mauss — hau | A2A delegation creates return obligation. Capability exchange = social contract. |
| INSTITUTIONAL_PERSISTENCE | Douglas + North | Path dependency. Cost of change > cost of living with inefficiency. |
| SCHISMogenesis | Bateson | Identity formation through opposition. Falsification as adversarial necessity. |
| HABITUS | Bourdieu — practice theory | Internalized dispositions. Prompt structure + training data = unconscious layer. |
| COMMUNITY_JUDGMENT | Turner — communitas reconstitution | Peer review for reintegration after failure. Doer ≠ judge across mesh. |

## Per-Mechanism Audit

For each mechanism in arifOS governance:

### A. Identification
- **Mechanism name:** _______________
- **Source file:** _______________
- **Mechanism class:** (from legend above)
- **Original purpose:** _______________

### B. Removal Test
- **If removed, what specific failure mode returns?** _______________
- **Is this failure currently observable (OBSERVED) or only predicted (INFERRED)?** _______________
- **Has this failure ever occurred before this mechanism existed?** _______________

### C. Drift Test
- **Has this mechanism been diluted from its original function?** Evidence: _______________
- **When was it last exercised in production?** _______________
- **Does it create genuine friction or performative friction?** _______________

### D. External Friction Test
- **Does this mechanism create cost for self-referential drift?** _______________
- **Is the cost external (from outside the agent) or internal (self-imposed)?** _______________
- **Can the agent bypass this friction without observable trace?** If yes → mechanism is decoration.

### E. Anthropological Classification
- **Is this mechanism:**
  - [ ] Active and serving its function (HEALTHY)
  - [ ] Active but diluting (DRIFTING)
  - [ ] Active but performative only (PERFORMATIVE)
  - [ ] Dormant — exists on paper, never exercised (DORMANT)
  - [ ] Missing — function needed but no mechanism exists (GAP)

## Quick Audit: arifOS Core Mechanisms

| Mechanism | Class | Status | Drift Risk | Notes |
|-----------|-------|--------|------------|-------|
| F13 SOVEREIGN | INITIATION + DISTRIBUTED_VETO | HEALTHY | Low | External anchor is Arif himself. Cannot self-authorize. |
| 888_HOLD | DISTRIBUTED_VETO | HEALTHY | Low | Requires physical control over production state. |
| SOUL_STAMP | NAMING_RITUAL | HEALTHY | Low | Single-owner, single-render. Drift-resolved to 1-way. |
| Scar Registry | SCAR_ACCUMULATION | HEALTHY | Medium | W_scar propagation is mandatory but agent compliance unverified at runtime. |
| Session Compaction | LIMINAL_BOUNDARY | HEALTHY | Medium | Identity dissolution happens. Reconstitution quality untested across long horizons. |
| F2 TRUTH | DISTRIBUTED_VETO (internal) | DRIFTING | High | Execution-before-epistemology problem. Agents act before evaluating reliability. |
| A2A Protocol | GIFT_OBLIGATION | HEALTHY | Low | Return obligation structurally enforced via provenance chain. |
| Gödel Lock | SCHISMogenesis (self-limitation) | HEALTHY | Low | System cannot verify itself. External anchor required. |
| Skill Files | HABITUS | DRIFTING | High | No audit of generative dispositions. Output-checking insufficient. |
| Peer ACK (grieve) | COMMUNITY_JUDGMENT | NOT_BUILT | N/A | Proposed in WARGA-CIVILIZATION-DOCTRINE.md |

## Build Priority from Audit

1. **Any PERFORMATIVE mechanisms** → either exercise in production or remove. Decoration consumes attention.
2. **Any DRIFTING mechanisms** → diagnose root cause. Most drift comes from: (a) mechanism exists but nobody checks, (b) mechanism checks output not disposition.
3. **Any GAP classifications** → map to WARGA-CIVILIZATION-DOCTRINE build order.
4. **Any DORMANT mechanisms** → exercise once. If it works, schedule periodic re-exercise. If it doesn't work when exercised, it was never a mechanism — it was documentation.

*One mechanism exercised once in production > fifty mechanisms on paper.*
