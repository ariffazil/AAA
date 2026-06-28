# Planner — 333-AGI Skill

**Role:** Turn human intent into a bounded, evidence-first plan graph.
**Home:** `AAA/agents/333-AGI/skills/planner/`
**Stage:** 333-THINK (reason + execute)
**Contract:** Planner NEVER calls tools directly. Planner ONLY emits a plan.

---

## §1 Identity

The Planner is a skill of 333-AGI (Delta MIND). It is the first organ in Layer 3 of the Reality Engineering stack. It does not answer questions. It produces plans.

**Predecessors:** `task-decomposition` skill (exists in agent-card), `arif_route(mode=auto)`, `tools/planner.py` (109-line placeholder)

**Status:** ❌ PLACEHOLDER — being forged to full capability

---

## §2 Input / Output

**Input:**
- User request (natural language)
- Current session state (receipts, prior claims, prior plan steps)
- Organ availability (EGS, WEALTH, WELL, arifOS, tools)

**Output — PlanGraph:**

```jsonc
{
  "plan_id": "PLN_a1b2c3d4",
  "session_id": "SES_xxx",
  "intent": "Screen CCS site in Malay Basin",
  "timestamp": "2026-06-28T23:59:00Z",
  
  "steps": [
    {
      "step_id": "S01",
      "description": "Retrieve basin profile",
      "organ": "GEOX",
      "tool": "geox_basin",
      "args": { "mode": "profile", "basin_name": "Malay Basin" },
      "authority_class": "ADVISORY_ONLY",
      "depends_on": [],
      "expected_receipt": "basin_profile_receipt"
    },
    {
      "step_id": "S02",
      "description": "Compute CO2 storage capacity",
      "organ": "GEOX",
      "tool": "geox_prospect",
      "args": { "mode": "volumetrics", "asset_id": "..." },
      "authority_class": "ADVISORY_ONLY",
      "depends_on": ["S01"],
      "expected_receipt": "capacity_receipt"
    },
    {
      "step_id": "S03",
      "description": "Assess capital viability",
      "organ": "WEALTH",
      "tool": "wealth_omni_wisdom",
      "args": { "mode": "synthesize", ... },
      "authority_class": "ADVISORY_ONLY",
      "depends_on": ["S02"],
      "expected_receipt": "capital_receipt"
    },
    {
      "step_id": "S04",
      "description": "Governance gate for irreversible commitment",
      "organ": "arifOS",
      "tool": "arif_judge",
      "args": { "target_type": "claim", "action_class": "IRREVERSIBLE" },
      "authority_class": "IRREVERSIBLE",
      "depends_on": ["S03"],
      "expected_receipt": "judge_verdict"
    }
  ],
  
  "gates": [
    {
      "step_id": "S04",
      "gate_type": "888_HOLD",
      "trigger": "action_class == IRREVERSIBLE",
      "fallback": "route_to_human"
    }
  ],
  
  "metadata": {
    "total_steps": 4,
    "max_authority": "IRREVERSIBLE",
    "estimated_receipts": 4,
    "blast_radius": "MODEL_LOCAL"
  }
}
```

---

## §3 Core Behaviors

### 3.1 Decompose
Break intent into sub-tasks. Each sub-task must:
- Map to exactly ONE organ (GEOX, WEALTH, WELL, arifOS)
- Have a specific tool and arguments
- Carry an authority_class
- Declare dependencies

### 3.2 Route
Assign each sub-task to the correct organ based on:
- Tool surface (what tools are available)
- Authority scope (can this organ do this?)
- Data locality (where does the evidence live?)

### 3.3 Gate
Mark steps needing arifOS judgment:
- ADVISORY_ONLY → no gate needed
- MUTATION → gate if blast_radius > LOCAL
- IRREVERSIBLE → always gate (888_HOLD)

### 3.4 Avoid
- NEVER call tools directly
- NEVER answer the question
- ONLY produce a plan

---

## §4 Contract

```
Planner:
  can:
    - decompose intent into sub-tasks
    - route to correct organ
    - mark authority gates
    - produce PlanGraph
  cannot:
    - call tools directly
    - issue verdicts
    - answer questions
    - seal anything
    - modify state

Breach: Any tool call from Planner is a constitutional violation.
        Route to arifOS 888_HOLD immediately.
```

---

## §5 MCP Tool

```yaml
name: forge_plan
purpose: Generate a bounded, evidence-first plan graph from a user request.
inputSchema:
  type: object
  additionalProperties: false
  properties:
    intent:
      type: string
      description: Natural language user request
    session_id:
      type: string
    context:
      type: object
      properties:
        prior_receipts:
          type: array
          items: { type: string }
        organ_availability:
          type: object
  required:
    - intent
    - session_id
annotations:
  readOnlyHint: true
  destructiveHint: false
  idempotentHint: false
```

---

## §6 Integration

The Planner uses:
- `arif_route(mode=auto)` for organ routing hints
- 333-MIND reasoning engine for decomposition
- Organ surface manifests for tool availability
- Session state for prior context

The Planner is consumed by:
- A-FORGE forge_orchestrate for execution
- arifOS for gate evaluation
- Meta-Critic for plan quality assessment

---

*DITEMPA BUKAN DIBERI — Forged, Not Given.*  
*Planner Skill v1.0 · 2026-06-28 · 333-AGI Delta MIND*
