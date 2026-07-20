---
type: Specification
title: Federation Map — 6 Realities Coordination
description: How the 6 realities (Evidence, Memory, Earth, Economic, Human, Operational) coordinate across the 7 organs of the arifOS federation
tags: [federation, map, coordination, realities, architecture]
timestamp: 2026-07-20T08:00:00Z
links:
  - index.md
  - skills/layers.md
  - atlas333.md
---
# Federation Map — 6 Realities Coordination

## The Coordination Flow

```
                    ┌─────────────┐
                    │   ARIF      │
                    │  (F13)      │
                    └──────┬──────┘
                           │ sovereign veto
                           ▼
              ┌────────────────────┐
              │    arifOS Kernel   │
              │  (Judge + Vault)   │
              └──┬──┬──┬──┬──┬───┘
                 │  │  │  │  │
        ┌────────┘  │  │  │  └────────┐
        ▼           ▼  ▼  ▼          ▼
   ┌────────┐ ┌──────┐ ┌────┐ ┌──────────┐
   │ GEOX   │ │WEALTH│ │WELL│ │   AAA    │
   │ Earth  │ │Capital│ │Human│ │Operations│
   └────────┘ └──────┘ └────┘ └────┬─────┘
                                    │
                                    ▼
                              ┌──────────┐
                              │ A-FORGE  │
                              │ Execution│
                              └──────────┘
```

## Decision Path (Constitutional)

```
1. INIT   — arif_init binds session + identity
2. OBSERVE — arif_observe gathers evidence (or GEOX/WEALTH/WELL domain compute)
3. REASON  — arif_think structures reasoning
4. ROUTE   — arif_route dispatches to correct domain organ
5. CRITIQUE — arif_critique runs maruah/ethics review
6. JUDGE   — arif_judge issues SEAL/HOLD/SABAR/VOID
7. FORGE   — A-FORGE executes under lease
8. SEAL    — arif_seal appends to VAULT999
```

## Cross-Reality Dependencies

| Decision Type | Requires | From |
|--------------|----------|------|
| Geological | Earth evidence | GEOX |
| Financial | Capital computation | WEALTH |
| Operational | Human readiness | WELL |
| Constitutional | Floor compliance | arifOS |
| Execution | Lease + judge path | A-FORGE |
| Coordination | Work state | AAA |
| Memory | Prior context | VAULT999 |
