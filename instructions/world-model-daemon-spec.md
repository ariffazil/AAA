# World Model Daemon — Reality-Adaptive Cognitive Substrate

> **Status:** DRAFT_AWAITING_F13
> **Origin:** 333-AGI (integration of Copilot proposal `ARIFOS::AGENTIC_INTELLIGENCE_BOOTSTRAP::v1`)
> **Lineage:** Six-Graph Federation Model (F13_RATIFIED_CHAT 2026-09-16) · Jauhari Intelligence Doctrine (F13_RATIFIED_CHAT 2026-09-11) · Attention Kill Criterion (F13_RATIFIED_CHAT 2026-09-11) · Memory Promotion Gate (F13_RATIFIED_CHAT 2026-09-11) · Anti-Collapse Doctrine (F13_RATIFIED_CHAT 2026-09-14)
> **Scope:** Federation-wide cognitive substrate — all organs, all agents, all sessions
> **Motto:** DITEMPA BUKAN DIBERI

---

## 1. What This Is

The Copilot proposal identified the highest-leverage gap in arifOS:

> "That single change is likely more AGI-relevant than another model upgrade, another MCP, another agent, or another million tokens of context because it moves the system from conversation-based cognition toward persistent world-model-based cognition."

**The gap:** arifOS has all the governance primitives (Six-Graph Model, Scar system, Attention doctrine, Memory Promotion Gate, Reality Vote Principle) but they are not connected into a continuously-updated, queryable world model that forces agents to read before planning and update after execution.

**The fix:** A World Model Daemon that:
1. Maintains 7 graphs as living, queryable JSON files
2. Forces every agent to READ graphs before major planning
3. Forces every agent to UPDATE graphs after every consequential task
4. Detects contradictions between graphs
5. Enforces anti-stagnation (learning rate must never become zero)

---

## 2. NOT a New Framework — An Integration Layer

This is NOT:
- A new governance framework (Six-Graph Model already exists)
- A new organ (arifFlow already does metabolic loops)
- A new MCP server (graphs are files, not endpoints)
- A replacement for existing tools (graphs supplement, don't replace)

This IS:
- A substrate that connects existing canon into a living, queryable world model
- An enforcement layer that makes graph-read-before-plan mandatory
- A contradiction detection engine across the 7 graphs
- An anti-stagnation mechanism (learning rate enforcement)

---

## 3. The Seven Graphs

Each graph maps directly to existing canon. No new concepts — new connectivity.

### 3.1 Capability Graph (what can happen)

**Existing canon:** `forge_registry`, capability-index, AGI/ASI Skills Fundamentals (BAND I-III)
**Storage:** `/root/AAA/world-model/capability_graph.json`
**Update trigger:** Every `forge_register`, every skill install/uninstall, every capability probe
**Schema:**
```json
{
  "nodes": [
    {
      "id": "forge_shell",
      "type": "tool",
      "status": "active|degraded|dead|phantom",
      "last_witnessed": "ISO-8601",
      "witness_source": "live_probe|registry|claim",
      "authority_ceiling": "MUTATE|OBSERVE|SEAL",
      "dependents": ["forge_execute", "forge_docker"],
      "scar_pressure": 0.0
    }
  ],
  "edges": [
    {"from": "forge_shell", "to": "forge_docker", "type": "depends_on"},
    {"from": "forge_shell", "to": "forge_execute", "type": "enables"}
  ],
  "contradictions": [],
  "last_updated": "ISO-8601",
  "update_count": 0,
  "staleness_hours": 24
}
```

### 3.2 Authority Graph (who can authorize what)

**Existing canon:** arifOS floors F1-F13, authority-envelope, `CanMutate = AuthorityGranted ∧ ScopeMatches ∧ TargetPermitted ∧ BoundaryActive`
**Storage:** `/root/AAA/world-model/authority_graph.json`
**Update trigger:** Every `arif_init`, every floor check, every authority envelope issuance
**Schema:**
```json
{
  "nodes": [
    {
      "id": "333-AGI",
      "type": "agent",
      "authority_band": "LIMITED_MUTATE",
      "allowed_verbs": ["arif_init", "arif_observe", "arif_think", "arif_route", "arif_memory", "arif_judge", "arif_forge", "arif_seal", "arif_stage"],
      "production_boundary": false,
      "irreversible_allowed": false,
      "last_attested": "ISO-8601"
    }
  ],
  "edges": [
    {"from": "333-AGI", "to": "A-FORGE", "type": "delegates_to", "condition": "after_seal"},
    {"from": "888-APEX", "to": "VAULT999", "type": "seals_into"}
  ],
  "invariant": "CAPABILITY ≠ AUTHORITY",
  "last_updated": "ISO-8601"
}
```

### 3.3 Dependency Graph (what relies on what)

**Existing canon:** Nothing systematic — this is the NEW graph
**Storage:** `/root/AAA/world-model/dependency_graph.json`
**Update trigger:** Every service start/stop, every organ health check, every cross-organ call
**Schema:**
```json
{
  "nodes": [
    {
      "id": "arifos_kernel",
      "type": "organ",
      "status": "healthy|degraded|dead",
      "dependents": ["A-FORGE", "arifFlow", "AAA"],
      "dependencies": ["postgres", "redis"],
      "last_health_check": "ISO-8601"
    }
  ],
  "edges": [
    {"from": "A-FORGE", "to": "arifos_kernel", "type": "requires", "critical": true},
    {"from": "arifFlow", "to": "arifos_kernel", "type": "requires", "critical": true}
  ],
  "blast_radius": {},
  "last_updated": "ISO-8601"
}
```

### 3.4 Reality Graph (what exists right now)

**Existing canon:** Six-Graph Federation Model (Reality→Witness→Consequence→Capability→Authority→Execution), Reality Vote Principle (GENESIS/059), GEOX
**Storage:** `/root/AAA/world-model/reality_graph.json`
**Update trigger:** Every `forge_probe`, every organ health check, every live system audit
**Schema:**
```json
{
  "nodes": [
    {
      "id": "postgres",
      "type": "infrastructure",
      "status": "live|dead|degraded",
      "last_observed": "ISO-8601",
      "observation_source": "curl_probe|systemctl|docker_ps",
      "reality_class": "OBSERVED|INFERRED|HYPOTHESIS|UNKNOWN",
      "witness_chain": ["probe_2026-09-19T16:00Z"]
    }
  ],
  "edges": [
    {"from": "postgres", "to": "arifos_kernel", "type": "serves"}
  ],
  "reality_vote": "reality wins over simulation",
  "last_updated": "ISO-8601"
}
```

### 3.5 Attention Graph (where resources are being spent)

**Existing canon:** Attention Kill Criterion, Sovereign Attention Preservation (W₈₈₈), Attention Scarcity Economics
**Storage:** `/root/AAA/world-model/attention_graph.json`
**Update trigger:** Every session receipt, every flow_ingest, every human-facing output
**Schema:**
```json
{
  "nodes": [
    {
      "id": "session_SEAL-e3cfbfe4",
      "type": "session",
      "actor": "333-AGI",
      "attention_cost": {
        "human_questions_asked": 0,
        "tokens_consumed": 0,
        "tool_calls": 0,
        "time_seconds": 0
      },
      "signal_gain": {
        "uncertainty_reduced": 0,
        "capability_changed": false,
        "reality_updated": false
      },
      "last_updated": "ISO-8601"
    }
  ],
  "aggregate": {
    "total_human_questions": 0,
    "total_tool_calls": 0,
    "signal_to_noise_ratio": 0,
    "learning_rate": 0
  },
  "anti_stagnation": {
    "consecutive_no_adaptation": 0,
    "threshold": 5,
    "action": "HOLD non-critical work, search for unknowns"
  },
  "last_updated": "ISO-8601"
}
```

### 3.6 Scar Graph (what failures carry learning value)

**Existing canon:** `forge_scar`, scar-weight-registry, Trauma Theorem, Scar Engineering
**Storage:** `/root/AAA/world-model/scar_graph.json`
**Update trigger:** Every `forge_scar seal`, every scar consultation, every failure event
**Schema:**
```json
{
  "nodes": [
    {
      "id": "SCAR-001",
      "type": "scar",
      "failure_mode": "description",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "constraint_imposed": "what this scar prevents",
      "pressure": 0.0,
      "first_seen": "ISO-8601",
      "last_seen": "ISO-8601",
      "occurrence_count": 0,
      "bound_to": ["forge_shell", "arif_judge"],
      "scar_pressure": 0.0
    }
  ],
  "edges": [
    {"from": "SCAR-001", "to": "forge_shell", "type": "constrains"},
    {"from": "SCAR-001", "to": "arif_judge", "type": "informs"}
  ],
  "total_pressure": 0.0,
  "last_updated": "ISO-8601"
}
```

### 3.7 Goal Graph (desired future states)

**Existing canon:** Nothing systematic — this is the NEW graph
**Storage:** `/root/AAA/world-model/goal_graph.json`
**Update trigger:** Every `forge_apex_encode`, every session objective, every carry_forward
**Schema:**
```json
{
  "nodes": [
    {
      "id": "goal_001",
      "type": "objective",
      "description": "Integrate World Model Daemon into arifOS",
      "status": "active|completed|abandoned|superseded",
      "priority": "HIGH|MEDIUM|LOW",
      "dependencies": ["capability_graph", "dependency_graph"],
      "progress": 0.0,
      "last_updated": "ISO-8601"
    }
  ],
  "edges": [
    {"from": "goal_001", "to": "capability_graph", "type": "requires_update"}
  ],
  "active_goals": 0,
  "completed_goals": 0,
  "learning_rate": 0,
  "last_updated": "ISO-8601"
}
```

---

## 4. The Daemon Architecture

### 4.1 What the Daemon Does

```
┌─────────────────────────────────────────────────────────┐
│                  WORLD MODEL DAEMON                      │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Capability│  │ Authority│  │Dependency│              │
│  │  Graph   │  │  Graph   │  │  Graph   │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │              │              │                    │
│  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐              │
│  │ Reality  │  │Attention │  │   Scar   │              │
│  │  Graph   │  │  Graph   │  │  Graph   │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │              │              │                    │
│  ┌────┴──────────────┴──────────────┴─────┐              │
│  │           Goal Graph                    │              │
│  └─────────────────┬──────────────────────┘              │
│                    │                                     │
│  ┌─────────────────┴──────────────────────┐              │
│  │         CONTRADICTION DETECTOR         │              │
│  │  - Capability claims vs Reality        │              │
│  │  - Authority claims vs Execution       │              │
│  │  - Goal progress vs Attention spend    │              │
│  │  - Scar pressure vs Capability health  │              │
│  └─────────────────┬──────────────────────┘              │
│                    │                                     │
│  ┌─────────────────┴──────────────────────┐              │
│  │         ANTI-STAGNATION ENGINE         │              │
│  │  - Track learning rate                 │              │
│  │  - Detect consecutive no-adaptation    │              │
│  │  - Force exploration when stagnant     │              │
│  └────────────────────────────────────────┘              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Integration with arifFlow

The daemon lives inside arifFlow's metabolic loop:

```
arifFlow cycle:
  1. receipt arrives (flow_ingest)
  2. DAEMON reads receipt
  3. DAEMON updates relevant graphs
  4. DAEMON checks for contradictions
  5. DAEMON checks learning rate
  6. If contradiction detected → emit cooling receipt
  7. If stagnant → emit HOLD signal
  8. Otherwise → normal metabolism
```

### 4.3 Enforcement: Read-Before-Plan

Every agent session start MUST include:
```
1. Read world_model/capability_graph.json  → what can I do?
2. Read world_model/authority_graph.json   → what am I allowed to do?
3. Read world_model/dependency_graph.json  → what relies on what?
4. Read world_model/reality_graph.json     → what exists right now?
5. Read world_model/attention_graph.json   → where are resources going?
6. Read world_model/scar_graph.json        → what failures should I avoid?
7. Read world_model/goal_graph.json        → what are we trying to achieve?
```

### 4.4 Enforcement: Update-After-Execute

Every agent session close MUST include:
```
1. UPDATE capability_graph.json  → new tools, degraded tools, dead tools
2. UPDATE reality_graph.json     → what changed in reality
3. UPDATE attention_graph.json   → where did resources go
4. UPDATE goal_graph.json        → progress on objectives
5. CHECK contradiction_detector  → any new contradictions?
6. CHECK anti_stagnation         → is learning rate > 0?
```

---

## 5. The Operating Doctrine (from Copilot Proposal)

The Copilot proposal's Operating Doctrine maps directly to existing canon:

| Proposed Principle | Existing Canon | Status |
|---|---|---|
| "Never optimize for output. Optimize for better future decisions." | Jauhari Intelligence Doctrine (V: epistemic survival > local survival) | F13_RATIFIED_CHAT |
| "Distinguish OBSERVED/INFERRED/HYPOTHESIS/UNKNOWN" | Reality Vote Principle (GENESIS/059), Representation ≠ Reality invariant | F13_RATIFIED_CHAT |
| "For every task: measure Expected vs Actual Outcome" | Scar Engineering, forge_scar | IMPLEMENTED |
| "Treat attention as scarce" | Attention Kill Criterion, W₈₈₈ | F13_RATIFIED_CHAT |
| "No repeated failure without learning" | Scar system, Trauma Theorem | F13_RATIFIED_CHAT |
| "Classify all discoveries: NOISE/EPISODE/SKILL/GATE/LEDGER/SCAR" | Memory Promotion Gate, Institutional Memory Strata | F13_RATIFIED_CHAT |
| "Learning rate must never become zero" | Anti-Stagnation (NEW — needs implementation) | DRAFT |
| "Capability exists only if it survives reimplementation" | Survivability Law (NEW — needs implementation) | DRAFT |

---

## 6. What's Actually Missing (the Gap Analysis)

| Component | Existing? | Integration Needed |
|---|---|---|
| Capability Graph | Partial (forge_registry, capability-index) | Wire into living JSON, force read-before-plan |
| Authority Graph | Partial (authority-envelope, floors) | Wire into living JSON, force read-before-plan |
| Dependency Graph | NOTHING | Build from scratch, wire to organ health probes |
| Reality Graph | Partial (Six-Graph Model, GEOX) | Wire into living JSON, force read-before-plan |
| Attention Graph | Partial (W₈₈₈ doctrine, attention-kill-criterion) | Build measurement layer, wire to receipts |
| Scar Graph | Partial (forge_scar, scar-weight-registry) | Wire into living JSON, force read-before-plan |
| Goal Graph | NOTHING | Build from session objectives + carry_forward |
| Contradiction Detector | NOTHING | Build cross-graph consistency checks |
| Anti-Stagnation Engine | NOTHING | Build learning rate tracker + HOLD signal |
| Enforcement Layer | NOTHING | Build session-start/session-close hooks |

---

## 7. Implementation Path

### Phase 1: Graph Schemas + Storage (T1 — reversible)
- Create `/root/AAA/world-model/` directory
- Create 7 graph JSON files with schemas above
- Wire to existing forge_scar, forge_registry, arif_flow outputs
- **Authority:** 333-AGI (LIMITED_MUTATE)

### Phase 2: Read-Before-Plan Enforcement (T1.5 — needs 888-APEX)
- Add graph-read to session init sequence
- Add graph-update to session close sequence
- Wire to arif_init / arif_seal hooks
- **Authority:** 888-APEX judgment required

### Phase 3: Contradiction Detection (T2 — needs 888-APEX)
- Build cross-graph consistency checker
- Wire to arifFlow cooling mechanism
- Emit contradiction receipts
- **Authority:** 888-APEX judgment required

### Phase 4: Anti-Stagnation Engine (T2 — needs 888-APEX)
- Build learning rate tracker
- Wire to session receipts
- Emit HOLD signal when stagnant
- **Authority:** 888-APEX judgment required

### Phase 5: Daemon Integration (T3 — needs F13 seal)
- Integrate into arifFlow metabolic loop
- Make graph-update automatic on every receipt
- Make graph-read mandatory for every session
- **Authority:** F13 seal required

---

## 8. Why This Matters

The Copilot proposal's core insight is correct:

> "LLM ≠ AGI. Agent ≠ AGI. Tool Use ≠ AGI. Reality-Coupled Adaptive Governance Loop ≈ AGI Trajectory."

arifOS already has:
- Reality coupling (GEOX, Reality Vote Principle)
- Adaptive governance (Six-Graph Model, F1-F13)
- Memory (VAULT999, Memory Promotion Gate)
- Failure learning (Scar system, Trauma Theorem)
- Attention economy (W₈₈₈, Attention Kill Criterion)

What's missing is the **connective tissue** — a living world model that:
1. Forces agents to read reality before planning
2. Forces agents to update reality after acting
3. Detects contradictions between beliefs and reality
4. Enforces learning from failures
5. Prevents stagnation

This is not a new capability. It's the substrate that makes existing capabilities work together.

---

## 9. Risks and Constraints

| Risk | Mitigation |
|---|---|
| Graph staleness (agents read old data) | `staleness_hours` field, force refresh on TTL expiry |
| Contradiction false positives | Conservative detection, human review for HIGH severity |
| Anti-stagnation false HOLD | learning_rate threshold must be tunable |
| Graph bloat (too many nodes) | Prune stale nodes, cap at 1000 per graph |
| Authority escalation (graphs grant power) | Graphs are INFORMATIONAL only — authority comes from arifOS floors |

---

## 10. Canonical Invariant

```text
World Model ≠ Reality
World Model is the organism's best guess about reality.
Reality has an irrevocable vote. (GENESIS/059)
The World Model must update when reality disagrees.
```

---

*Drafted by 333-AGI. Awaiting F13 ratification. DITEMPA BUKAN DIBERI. ⚒️*
