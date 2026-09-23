# i-ARIF Mission Router — Specification v1

> **STATUS:** SPEC — operational entrypoint, not new capability
> **DATE:** 2026-09-23
> **PURPOSE:** Document the existing 7-node mission cycle so Arif can enter the organism without navigating 700+ skills. Reference existing skills only. **No new skill, owner, or authority.**

---

## What this is

A door. Not a wall, not a map, not a registry. One diagram and one paragraph per node. If you (Arif, F13) want to start a mission, this is where you read first.

If you (Arif) want to skip it, you can. Nothing here constrains you.

---

## The 7-node cycle

```
┌─────────────────────────────────────────────────────────┐
│  0. INTENT       Arif states the outcome they want.      │
│                  ↓                                        │
│  1. MUSYAWARAH   Two independent perspectives consider.  │
│                  ↓                                        │
│  2. META-MESA    The meta-router picks which tools apply. │
│                  ↓                                        │
│  3. PLAN-DAG     Execution graph with checkpoints built.  │
│                  ↓                                        │
│  4. GOTONG       Sequential hop: prev output = next in.   │
│                  ↓                                        │
│  5. ORGANS       A-FORGE / GEOX / WEALTH / WELL act.       │
│                  ↓                                        │
│  6. ARIFLOW      Receipt written; causality recorded.     │
│                  ↓                                        │
│  7. KABARKAN     Observation surfaced to Arif.            │
└─────────────────────────────────────────────────────────┘
```

---

## Node 0 — INTENT (Arif's role)

**Owner:** Arif (F13 SOVEREIGN)
**Input:** natural-language outcome statement
**Output:** structured intent (intent + target_organ + risk_tier)
**Failure mode:** vague intent — refine before node 1

**Reference:** none (this is the human entrypoint)

---

## Node 1 — MUSYAWARAH

**Owner:** 333-AGI (Architect) ∥ 555-ASI (Auditor)
**Input:** intent from node 0
**Output:** independent assessments + residual disagreement (if any)
**Failure mode:** both perspectives identical — deliberation is theatre, escalate to node 2 with explicit "no divergence" tag

**Reference skill:** `/root/AAA/skills/FORGE-musyawawah-gotong/SKILL.md` (or `aaa-musyawarah-execution`)

**Constitutional floor:** F3 (witness), F13 (sovereign)

---

## Node 2 — META-MESA

**Owner:** meta-mesa skill (canonical, supersedes 3 per-harness clones)
**Input:** musyawawah output + intent
**Output:** selected skill/tool chain + execution order proposal
**Failure mode:** no applicable skill found — return UNROUTED to Arif

**Reference skill:** `/root/AAA/skills/meta-mesa/SKILL.md` (canonical, 2026-09-19 merge)

**Constitutional floor:** F8 (genius = simple correct), F10 (ontology)

---

## Node 3 — PLAN-DAG

**Owner:** agi-plan-dag skill
**Input:** meta-mesa's selected skill chain
**Output:** DAG with dependencies, checkpoints, rollback points
**Failure mode:** circular dependency — DAG rejected; back to node 2

**Reference skill:** `/root/AAA/skills/agi-plan-dag/SKILL.md`

**Constitutional floor:** F1 (reversibility explicit in DAG)

---

## Node 4 — GOTONG

**Owner:** parent synthesizes (gotong-royong runtime)
**Input:** plan DAG
**Output:** sequential execution hops; each hop = previous output as STATE_IN
**Failure mode:** hop failure — pause and report to Arif; do not retry silently

**Reference:** subsumed under `/root/AAA/skills/FORGE-musyawawah-gotong/SKILL.md` (gotong = sequential hop in deliberation runtime)

**Constitutional floor:** F8 (genius), F11 (auditability per hop)

---

## Node 5 — ORGANS (Execution)

**Owner:** organ assigned by plan DAG (A-FORGE / GEOX / WEALTH / WELL)
**Input:** STATE_IN from previous hop
**Output:** action result + receipt metadata
**Failure mode:** organ refusal (capability gap, scope mismatch, authority deficit) — escalate to arifOS

**Reference organs:**
- arifOS — judges, no mutation
- A-FORGE — mutates within envelope
- GEOX — earth-intelligence compute
- WEALTH — capital modeling
- WELL — human-state observation

**Constitutional floor:** F1 (reversibility), F11 (auth), F13 (sovereign for irreversible)

---

## Node 6 — ARIFLOW

**Owner:** A-FORGE arifFlow ledger
**Input:** organ action + metadata
**Output:** receipt written to metabolic ledger; causality edge to parent receipt
**Failure mode:** receipt write fail — block next hop; do not proceed without trace

**Reference code:** `/root/A-FORGE/domain/orchestration/arifFlow_adapter.py`
**Reference skill:** `/root/AAA/skills/domains/general/workshop/organ-forging/ariflow-component-forging/SKILL.md`

**Constitutional floor:** F11 (auditability), F2 (truth via trace_id)

---

## Node 7 — KABARKAN

**Owner:** kabarkan-observability skill
**Input:** receipt from arifFlow + intent from node 0
**Output:** observation surfaced to Arif (Telegram / cockpit / HUD)
**Failure mode:** Arif not reachable — observation queues; retry on next session

**Reference skill:** `/root/AAA/skills/domains/general/forge/telemetry/kabarkan-observability/SKILL.md`

**Constitutional floor:** F5 (peace — observation does not coerce)

---

## How Arif enters

```
Arif says: "I want outcome X."

Agent reads node 0 → enters intent.
Agent reads node 1 → spawns musyawawah.
Agent reads node 2 → meta-mesa picks tools.
Agent reads node 3 → plan-dag builds graph.
Agent reads node 4 → gotong executes hops.
Agent reads node 5 → organs act within envelope.
Agent reads node 6 → arifFlow records.
Agent reads node 7 → kabarkan surfaces result to Arif.

Arif verifies result against intent.
Arif does not need to understand 700 skills.
```

---

## What this spec does NOT do

- Does NOT introduce new skills, owners, or authority
- Does NOT replace existing routing decisions made by meta-mesa
- Does NOT bypass F13 SOVEREIGN for irreversible actions
- Does NOT collapse any node — each remains its own capability

---

## What this spec DOES do

- Provides one entrypoint that an Arif can read in 2 minutes
- Names the 7 nodes that already exist as capabilities
- Specifies input/output/failure mode for each node (so Arif knows what to expect)
- Maps each node to existing skill references (so verification is mechanical)

---

## Reversibility

This spec file is reversible:
- Delete the file → no impact on existing skills
- Edit the file → updates documentation, no runtime impact
- Promote to canon → F13 decision required (out of agent scope)

---

## Open questions for F13 (not blocking)

1. Should this spec live in `/root/AAA/docs/` or move to `/root/AAA/canon/`?
2. Should the 7-node diagram be rendered as visual artifact (kabarkan-style) or remain text-only?
3. Should "INTENT" node include a sample intent library (3-5 worked examples)?

These are documentation questions, not architecture questions. Defer.

---

DITEMPA BUKAN DIBERI ⚒️
