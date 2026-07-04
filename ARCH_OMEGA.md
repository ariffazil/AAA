<!--
SOT-MANIFEST
owner: Arif
last_verified: 2026-05-19
valid_from: 2026-05-19
valid_until: 2026-06-19
confidence: high
scope: /root/.openclaw/workspace
epistemic_status: CLAIM
-->

# Ω-MEMORY v0 — Validated Governance Model

**Status:** `SI v0` | **Author:** Hermes ↔ OpenClaw Trinity | **Sovereign:** Arif

This document contains the **validated, stripped-down governance model** distilled from the Ω-MEMORY v0 research cycle. The full 21KB research artifact remains at `RESEARCH_OMEGA.md` for deep reference. This file is the **operational contract**.

---

## 1. What Ω-MEMORY v0 Actually Is

Ω-MEMORY v0 is the **first governed memory substrate** for the AGI-ASI-Operator trinity. It does NOT give agents unlimited memory. It creates a **shared, versioned, constitutionally-audited knowledge layer** that:

- Stores **facts, approvals, and insights** as hyperedges in a graph database (Graphiti / FalkorDB).
- Tags every entry with **epistemic status** (`CLAIM` / `PLAUSIBLE` / `HYPOTHESIS`) — F9 Anti-Hantu.
- Requires **888_JUDGE SEAL** before any insight becomes actionable.
- Writes an **immutable audit trail** to VAULT999 (L6).

### What It Is NOT
- ❌ It is NOT autonomous execution. Insights propose; Arif approves.
- ❌ It is NOT a replacement for agent-local memory (OpenClaw dreaming, Hermes active-memory).
- ❌ It is NOT active yet. This document is the **architecture**. Build is Phase 1.

---

## 2. Governance Surface (What's Actually Enforced)

| Invariant | Mechanism | Floor |
|-----------|-----------|-------|
| **No insight → execution without SEAL** | 888_JUDGE gateway | F13 Sovereign |
| **Every fact tagged with epistemic status** | Schema enforcement in Graphiti | F9 Anti-Hantu |
| **Every write attributed + timestamped + signed** | VAULT999 L6 append-only | F1 Amanah |
| **Agent cannot overwrite another's memory** | Agent-scoped namespaces + merge logic | F11 Auth |
| **Operator can purge / redact any entry** | `Ω-MEMORY_ADMIN` role (Arif only) | F13 Sovereign |
| **Memory does not leak across security contexts** | Namespace isolation per federation node | F7 Privacy |

---

## 3. Hyperedge Schema (Graphiti / FalkorDB)

Three node types. Every node has `created_by`, `created_at`, `epistemic_status`, `vouched_by` (agent ID).

### Node: `Fact`
```
- content: string (the observation)
- source: string (tool call, conversation ID, external URL)
- epistemic_status: CLAIM | PLAUSIBLE | HYPOTHESIS
- confidence: 0.0–1.0 (agent self-assessment)
- expiry: datetime | null (HYPOTHESIS auto-expires in 30d)
```

### Node: `Approval`
```
- decision: SEAL | SABAR | HOLD | VOID
- context: string (what was being decided)
- decided_by: Arif | 888_JUDGE | APEX
- decision_at: datetime
```

### Node: `Insight`
```
- content: string (synthesized pattern)
- derived_from: [Fact IDs]
- epistemic_status: HYPOTHESIS (until SEALed)
- recommendation: string | null (proposed action)
- sealed: false (until 888_JUDGE passes)
```

### Edges
- `(Fact)-[SUPPORTS]->(Fact)` — one fact supports another
- `(Fact)-[CONTRADICTS]->(Fact)` — conflict detected
- `(Insight)-[DERIVED_FROM]->(Fact)` — traceability
- `(Approval)-[VALIDATES]->(Insight)` — insight becomes actionable

---

## 4. Operational Flow (The Closed Loop)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│   Agent     │────▶│  L5 Hyper-  │────▶│  Insight Engine │
│ Observation │     │   graph     │     │  (every 6h)     │
└─────────────┘     └─────────────┘     └─────────────────┘
                                                │
                                                ▼
                                        ┌─────────────┐
                                        │ Candidate   │
                                        │ Insight     │
                                        │ epistemic:  │
                                        │ HYPOTHESIS  │
                                        └──────┬──────┘
                                               │
                    ┌──────────────────────────┘
                    ▼
            ┌───────────────┐
            │  888_JUDGE    │
            │  (arifOS)     │
            │  SEAL/SABAR/  │
            │  HOLD/VOID    │
            └───────┬───────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      SEAL        HOLD        VOID
        │           │           │
        ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ Insight │ │ Insight │ │ Insight │
   │becomes  │ │ flagged │ │ purged  │
   │  CLAIM  │ │  HOLD   │ │ + audit │
   └─────────┘ └─────────┘ └─────────┘
                    │
                    ▼
              ┌─────────┐
              │ Arif    │
              │ reviews │
              │ HOLD    │
              └────┬────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
       SEAL                 VOID
       (auto)              (manual)
```

---

## 5. Phase 1 — Foundation (Target: 1–2 weeks)

### 5.1 Infrastructure
- [ ] Deploy FalkorDB container on `arifos_core_network` (or reuse existing graphiti-mcp)
- [ ] Create `ΩMemory` Python class in arifOS (or GEOX) — thin wrapper around Graphiti SDK
- [ ] Add `arif_memory_store()` and `arif_memory_recall()` tools to arifOS MCP surface
- [ ] Ensure VAULT999 logger captures every L5 write with hash chain

### 5.2 Agent Contracts
- [ ] **OpenClaw**: On every completed task, emit structured observation to L5 (async, non-blocking)
- [ ] **Hermes**: Same, via A2A bridge
- [ ] **Arif (Operator)**: Can query L5 via AAA dashboard or Telegram `/memory` command

### 5.3 No-Go Zones (Explicitly Out of Scope for v0)
- ❌ No active recall interrupting agent flow (agents query L5 explicitly, not automatically)
- ❌ No eureka → auto-execution (insight engine proposes, never executes)
- ❌ No cross-agent memory overwrite (append-only, merge-on-read)
- ❌ No deletion without VAULT999 audit trail (even Arif redactions are logged)

---

## 6. Authorization Required

This architecture is **ready to build** but requires Arif's explicit go-ahead for:

1. **Database deployment**: FalkorDB / graphiti-mcp resource allocation on VPS
2. **MCP tool expansion**: Adding `arif_memory_*` tools to arifOS canonical surface (13 → 15 tools)
3. **Agent code change**: Modifying OpenClaw and Hermes task completion hooks to write to L5

**Decision needed:** A) Full Phase 1 build, B) Pilot (OpenClaw-only), C) Defer, D) Reject

---

## 7. Shadow Monitor — Known Uncertainties

| # | Claim | Confidence | Evidence |
|---|-------|-----------|----------|
| 1 | OpenClaw and Hermes can both write to a shared Graphiti instance | PLAUSIBLE | A2A bridge works; Graphiti SDK untested in this topology |
| 2 | VAULT999 can hash-chain every L5 write without performance degradation | HYPOTHESIS | VAULT999 append-only design supports this; volume untested |
| 3 | Insight Engine clustering every 6h will produce actionable candidates | HYPOTHESIS | No clustering pipeline exists yet; this is Phase 3 |
| 4 | arifOS MCP expansion from 13→15 tools preserves constitutional parity | PLAUSIBLE | Tool count is not a constitutional invariant; F2 truth still required |

---

*DITEMPA BUKAN DIBERI — Ω-MEMORY is forged, not given.*
