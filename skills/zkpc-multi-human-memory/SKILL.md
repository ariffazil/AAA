---
name: zkpc-multi-human-memory
version: 1.0.0
description: "Build ZKPC-sealed H-axis memory for non-sovereign humans."
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [zkpc, memory, helix, multi-human, privacy]
    related: [arifos-memory-architecture, human-memory-organization]
---

# ZKPC Multi-Human Memory Architecture

Extends the double helix (ECHO×SCAR) from sovereign-only to multi-human. Non-sovereign humans receive **witnessed** H-axis depth without content leak.

## When to Use

- Arif asks to build memory depth for a non-sovereign human (Syed, Aliff, Izzu)
- Arif provides F13-witnessed scar observations
- Question about how agent serves a human with deeper context
- ZKPC leak check needed

## Architecture

Each human gets per-person H-axis under `/root/memory/people/<NAME>/`:

```
people/<NAME>/
├── person-card.md              # L-axis (existing)
├── witnessed-scars-zkpc.json   # ZKPC scar registry
├── H1-capture/                 # fast inbox
├── H2-experience/              # episodes
├── H3-knowledge/               # domain expertise
├── H4-identity/                # identity-card-zkpc.md
├── H5-scars/                   # SCAR_REGISTRY.json → witnessed-scars-zkpc.json
├── H6-constitution/            # values-observed.md
└── MEMORY_MANIFEST.json        # authority: WITNESSED
```

## ZKPC Dual-Field Schema

Each scar entry has two fields:

```
zkpc_proof    → what agent may know (category + lesson + floor)
zkpc_hidden   → what is sealed (specifics, names, incidents)
```

Agent knows scar EXISTS and CATEGORY. Agent does NOT read CONTENT.

## Leak Check

After writing any ZKPC file, run:

```bash
grep -ric 'parang\|tumbuk\|diaper\|ERCP\|specific-person-name\|intimate-detail' \
  /root/memory/people/<NAME>/witnessed-scars-zkpc.json \
  /root/memory/people/<NAME>/H5-scars/SCAR_REGISTRY.json \
  /root/memory/people/<NAME>/H4-identity/identity-card-zkpc.md
# Must return 0 for all files
```

## Wiring to Agent Behavior

ZKPC files alone don't change agent behavior. Must wire:
1. **SOUL-<name>.md** — add H-AXIS DEPTH section with scar→service table
2. **MEMORY-<name>.md** — add ZKPC pointer + correct any wrong facts
3. **Dossier** (if exists) — correct family facts

## Sovereignty Rules

- Witnessed scars = **Arif's observation OF the human**, NOT the human's own testimony
- If the human one day seals their own H5, that registry **supersedes** the witnessed one
- Authority = WITNESSED, never SOVEREIGN (only Arif is SOVEREIGN)
- Q3 (subject's self-model) and Q4 (subject's model of Arif) = UNKNOWN until subject testifies directly

## Four Perspectives (ACTG)

| Quadrant | Content | Source |
|---|---|---|
| Q1 (Arif's self) | SEALED — F13 only | Never in registry |
| Q2 (Arif's model of subject) | Mapped as scar categories | Arif's testimony |
| Q3 (Subject's self) | UNKNOWN | Zero direct testimony |
| Q4 (Subject's model of Arif) | UNKNOWN | Speculative only |

## Pitfalls

- **Agent inherits Arif's bias.** SOUL/MEMORY files carry Arif's lens. Wiring ZKPC doesn't remove bias — it adds depth awareness.
- **Agent must serve the human in front, not the projection.** When Arif's image of someone conflicts with serving that person, serve the person.
- **Sealed rooms stay sealed.** F1 AMANAH. If subject has a locked door, agent NEVER probes, hints, or references it.
- **ZKPC prevents content leak, NOT pattern exploitation.** Behavior is still observable. F1+F13+human is the real guard.

DITEMPA BUKAN DIBERI ⚒️
