# CHRON × arifFlow — Organ Boundary Doctrine

> **Status:** DESIGN — sovereign architectural analysis, 2026-09-18
> **Authority:** F13 sovereign analysis (third message in CHRON reality compression session)
> **Key principle:** Same machine = fine. Same process = possibly fine. Same database = maybe, with separate schemas. Same capability/ownership boundary = bad idea.

---

## 0. The One Rule

```
CHRON depends on arifFlow evidence.
arifFlow must not depend on CHRON interpretation to continue recording reality.
```

**If CHRON dies, history still flows.**
**If arifFlow dies, CHRON knows it has become partially blind.**

That is excellent fault isolation.

---

## 1. Why They Must Not Merge

### Different semantics

| arifFlow | CHRON |
|----------|-------|
| event | episode |
| receipt | belief |
| trace | prediction |
| cycle | supersession |
| latency | retraction |
| flow | relevance |
| health | outcome |
| provenance | calibration |
| | forgetting |

### Different questions

| arifFlow asks | CHRON asks |
|---------------|------------|
| "What moved through the federation?" | "What does that movement mean across time?" |

### Different time scales

| arifFlow | CHRON |
|----------|-------|
| milliseconds, seconds, minutes | seconds, hours, days, months, years |
| streaming, append, routing, low latency | bitemporal queries, graph traversals, historical reconstruction |

### Different failure domains

If CHRON's prediction engine crashes, you still want:
- receipts flowing
- telemetry flowing
- FRAME observations flowing
- A-FORGE traces flowing

because those are the very things you will use to reconstruct what happened.

If CHRON and arifFlow are one inseparable system, a temporal-cognition failure destroys the transport evidence needed to diagnose that same failure. **Circular dependency.**

### Different authority boundaries

| arifFlow | CHRON |
|----------|-------|
| OBSERVATION / TRANSPORT | INTERPRETATION / TEMPORAL COMPUTE |
| "This happened." | "This matters now." / "This prediction failed." |
| Mostly descriptive | Partly interpretive |

If arifFlow also becomes CHRON, transport starts silently acquiring interpretive authority. That's the kind of semantic drift the federation has been auditing.

---

## 2. The Clean Organ Model

| Organ | Role |
|-------|------|
| **FRAME** | Independent witness |
| **arifFlow** | Experience circulation |
| **CHRON** | Temporal cognition |
| **HERMES** | Semantic membrane |
| **AAA** | Orchestration / routing / coordination |
| **arifOS** | Constitutional authority |
| **A-FORGE** | Actuation |
| **GEOX** | Physical / Earth reality |
| **WEALTH** | Incentives / capital |
| **WELL** | Human vitality |

---

## 3. The Architecture (corrected from linear)

```
REALITY
    │
    ▼
  FRAME (independent witness)
    │
    ▼
arifFlow (experience transport)
    │
    ▼
  CHRON (temporal reconciliation)
    │
    ├─── arifOS (authority / judgment)
    │         │
    └─── AAA (orchestration / routing)
              │
              ▼
          A-FORGE (action)
              │
              ▼
           REALITY
              │
              └──→ FRAME (loop closes)
```

HERMES sits across the semantic boundary: validates claims, separates perspectives, protects qualia/privacy.

---

## 4. Shared Infrastructure, Separate Capabilities

### Acceptable

- Same machine
- Same process (initially)
- Same database (with separate schemas)

### Unacceptable

- Same capability/ownership boundary
- Shared mutable state everywhere
- arifFlow depending on CHRON interpretation

### Internal package structure (if same process)

```
arifflow.service
    flow/        ← arifFlow owns: FlowEvent, FlowReceipt, Trace, Transport
    chron/       ← CHRON owns: ChronEpisode, Prediction, BeliefState, Supersession, Calibration, AttentionDecision
```

### API boundary

```
arifFlow → CHRON:  subscribe(events)
CHRON → arifFlow:  emit(temporal_receipt)
```

Not shared mutable state.

---

## 5. Ownership Boundary

| Object | Owner |
|--------|-------|
| FlowEvent | arifFlow |
| FlowReceipt | arifFlow |
| Trace | arifFlow |
| Transport | arifFlow |
| ChronEpisode | CHRON |
| Prediction | CHRON |
| BeliefState | CHRON |
| Supersession | CHRON |
| Calibration | CHRON |
| AttentionDecision | CHRON |

---

## 6. The Deepest Reason

arifFlow represents: **time as sequence**
CHRON represents: **time as meaning**

arifFlow knows: A happened before B

CHRON eventually knows:
- When A happened, we believed X
- After B, X became contradicted
- At C, we superseded X with Y
- That changed which signals mattered

That is a qualitatively different layer.

---

## 7. Compression

> CHRON should consume arifFlow heavily, but not become arifFlow.

> Same machine: fine. Same process: possibly fine. Same database: maybe, with separate schemas. Same capability/ownership boundary: bad idea.

---

DITEMPA BUKAN DIBERI ⚒️
