# SKILL INVARIANT SCHEMA — The Frozen Header Spec

> **DITEMPA BUKAN DIBERI** — Forged 2026-08-04 by 333-AGI Δ MIND
> **Owner:** Muhammad Arif bin Fazil (F13 SOVEREIGN)
> **Domain:** AAA Control Plane — skill governance
> **Status:** SPEC — canonical schema for all 129 skills
> **Enforcement:** skill-linter validates against this schema

---

## 0. The Principle

A skill is a static, signed, orthogonal contract with a dynamic distilled memory —
it owns one axis, refuses the rest, and collaborates by exposing its promise, not its mind.

---

## 1. INVARIANT HEADER (frozen, human-signed)

The header NEVER auto-changes. It changes only via approved RSI with F1 AMANAH.

```yaml
# ============================================
# SKILL INVARIANT HEADER — frozen, signed
# ============================================

id: FORGE-fastmcp                          # unique, namespaced, never reused
version: 1.0.0                             # semver, changes only on approved edit
purpose: "Build MCP servers with FastMCP"  # ONE sentence. Two = two skills.

# BOUNDARIES — what this skill OWNS and REFUSES
owns:
  - "MCP server creation and deployment"
  - "FastMCP library usage"
  - "MCP protocol compliance"
refuses:
  - "MCP server hosting (A-FORGE territory)"
  - "MCP client connections (agent responsibility)"
  - "MCP protocol design (arifOS territory)"

# FAILURE OWNERSHIP — what failures this skill can legitimately own
cause_class:
  - SKILL_DEFECT       # instruction was wrong/missing/unclear
  # NOT: MODEL_ERROR, HARNESS_FAULT, DATA_FAULT, TASK_IMPOSSIBLE, UPSTREAM_FAULT, AMBIGUOUS_INTENT

# COST — context + risk weight
cost_class: C1         # C0=substrate(free) C1=low C2=medium C3=high C4=sovereign
context_tokens: 2000   # estimated context consumption when loaded
risk_level: LOW        # LOW/MEDIUM/HIGH/CRITICAL

# GOVERNANCE — who may load, when, where
tier: forge_on_demand  # substrate_always | constitutional | forge_on_demand | github_on_demand | knowledge_on_demand | agi_on_demand | asi_sensory | a2a_handoff
permissions:
  agents: ["*"]        # which agents may load this skill
  stages: ["ACT"]      # which institutional stages this skill may fire in
  max_concurrent: 1    # max simultaneous loads (1 = exclusive)

# DEPENDENCIES — what must be true before this skill loads
dependencies:
  skills: []           # other skills that must be loaded first
  tools: ["forge_fastmcp"]  # MCP tools required
  organs: []           # federation organs that must be alive
  preconditions: []    # runtime conditions that must hold

# COLLISION — who wins on conflict
precedence: 0          # higher = wins on collision. 0 = defer to other.
conflicts_with: []     # skills that cannot be loaded simultaneously

# CONTRACT — inputs → outputs → side_effects (explicit)
contract:
  inputs:
    - name: "intent"
      type: "string"
      description: "Natural language description of MCP server to build"
      required: true
  outputs:
    - name: "server_code"
      type: "file"
      description: "Python MCP server using FastMCP"
      required: true
  side_effects:
    - "Creates files on disk"
    - "May run pip install"
  reversible: true     # all side effects can be undone

# REVERSIBILITY — the F1 AMANAH binding
reversibility: REVERSIBLE  # REVERSIBLE | GATED | IRREVERSIBLE
rollback_procedure: "Delete generated files, revert pip changes"

# OWNERSHIP — accountable human/organ
owner: "333-AGI"
owner_organ: "A-FORGE"
accountability: "F13 SOVEREIGN"

# SEAL — VAULT999 hash of this header
seal: null             # filled by arif_seal on first promotion
seal_date: null
sealed_by: null
```

---

## 2. MUTABLE BODY (grows, distilled, capped)

The body is where learning happens. It changes through the Skill Evolution Protocol.

```yaml
# ============================================
# MUTABLE BODY — learning layer
# ============================================

# PROCEDURE — the actual how-to (edits = approval)
procedure: |
  1. Parse intent for MCP server requirements
  2. Generate FastMCP server scaffold
  3. Add tools based on intent
  4. Run tests
  5. Deploy to A-FORGE

# MEMORY — distilled lessons (capped at 7 hot)
memory:
  hot_cap: 7
  lessons: []          # auto-populated by Skill Evolution Protocol
  last_distilled: null

# SCARS — failure patterns → regression tests
scars:
  count: 0
  recurrence_rate: 0.0
  last_scar: null
  regression_tests: [] # auto-generated from confirmed scars

# EUREKAS — confirmed insights that changed a decision
eurekas:
  count: 0
  last_eureka: null
  verified: []         # eurekas that passed the 3-gate discriminator

# METRICS — convergence tracking
metrics:
  last_used: null
  use_count: 0
  edit_count: 0
  convergence_status: CONVERGED  # CONVERGED | STABLE | UNSTABLE | DIVERGENT
  last_stable_version: "1.0.0"
  days_since_last_edit: 0
```

---

## 3. FIELD SPECIFICATION

### 3.1 Required Fields (header)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | YES | Unique, namespaced (FORGE-fastmcp). Never reused. |
| `version` | string | YES | Semver (1.0.0). Changes only on approved edit. |
| `purpose` | string | YES | ONE sentence. Two = two skills. |
| `owns` | list[string] | YES | What this skill OWNS. Min 1. |
| `refuses` | list[string] | YES | What this skill REFUSES. Min 1. |
| `cause_class` | list[enum] | YES | What failures this skill can own. Must include at least one. |
| `cost_class` | enum | YES | C0/C1/C2/C3/C4. |
| `tier` | enum | YES | One of the 8 canonical tiers. |
| `permissions` | object | YES | agents, stages, max_concurrent. |
| `dependencies` | object | YES | skills, tools, organs, preconditions. |
| `precedence` | integer | YES | Higher = wins on collision. 0 = defer. |
| `conflicts_with` | list[string] | YES | Skills that cannot coexist. |
| `contract` | object | YES | inputs, outputs, side_effects, reversible. |
| `reversibility` | enum | YES | REVERSIBLE/GATED/IRREVERSIBLE. |
| `owner` | string | YES | Accountable human/organ. |
| `owner_organ` | string | YES | Federation organ. |
| `accountability` | string | YES | Who answers for this skill. |
| `seal` | string\|null | AUTO | VAULT999 hash. Filled on promotion. |

### 3.2 Required Fields (body)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `procedure` | string | YES | The actual how-to. Free text. |
| `memory.hot_cap` | integer | YES | Max distilled lessons. Default 7. |
| `memory.lessons` | list | AUTO | Populated by Skill Evolution Protocol. |
| `scars.count` | integer | AUTO | Total scars observed. |
| `scars.recurrence_rate` | float | AUTO | 0.0-1.0. Lower = better. |
| `metrics.last_used` | datetime\|null | AUTO | Last time skill was loaded. |
| `metrics.convergence_status` | enum | AUTO | CONVERGED/STABLE/UNSTABLE/DIVERGENT. |

### 3.3 Enumerations

```
cost_class:     C0 | C1 | C2 | C3 | C4
tier:           substrate_always | constitutional | forge_on_demand | github_on_demand | knowledge_on_demand | agi_on_demand | asi_sensory | a2a_handoff
reversibility:  REVERSIBLE | GATED | IRREVERSIBLE
risk_level:     LOW | MEDIUM | HIGH | CRITICAL
convergence:    CONVERGED | STABLE | UNSTABLE | DIVERGENT
cause_class:    SKILL_DEFECT | MODEL_ERROR | HARNESS_FAULT | DATA_FAULT | TASK_IMPOSSIBLE | UPSTREAM_FAULT | AMBIGUOUS_INTENT
institutional_stage: SENSE | DECIDE | GATE | ACT | ATTEST | REVIEW
```

---

## 4. VALIDATION RULES

### 4.1 Header Validation (linter enforced)

```python
HEADER_VALIDATION = {
    'id': {
        'type': 'string',
        'pattern': r'^[A-Z][A-Z0-9-]+$',  # uppercase, alphanumeric, hyphens
        'unique': True,  # must not collide with other skills
        'required': True
    },
    'version': {
        'type': 'string',
        'pattern': r'^\d+\.\d+\.\d+$',  # semver
        'required': True
    },
    'purpose': {
        'type': 'string',
        'max_length': 200,  # ONE sentence
        'required': True
    },
    'owns': {
        'type': 'list',
        'min_items': 1,
        'items': {'type': 'string'},
        'required': True
    },
    'refuses': {
        'type': 'list',
        'min_items': 1,
        'items': {'type': 'string'},
        'required': True
    },
    'cause_class': {
        'type': 'list',
        'min_items': 1,
        'items': {'enum': ['SKILL_DEFECT', 'MODEL_ERROR', 'HARNESS_FAULT', 'DATA_FAULT', 'TASK_IMPOSSIBLE', 'UPSTREAM_FAULT', 'AMBIGUOUS_INTENT']},
        'required': True
    },
    'cost_class': {
        'type': 'enum',
        'values': ['C0', 'C1', 'C2', 'C3', 'C4'],
        'required': True
    },
    'tier': {
        'type': 'enum',
        'values': ['substrate_always', 'constitutional', 'forge_on_demand', 'github_on_demand', 'knowledge_on_demand', 'agi_on_demand', 'asi_sensory', 'a2a_handoff'],
        'required': True
    },
    'permissions': {
        'type': 'object',
        'required': True,
        'fields': {
            'agents': {'type': 'list', 'items': {'type': 'string'}},
            'stages': {'type': 'list', 'items': {'enum': ['SENSE', 'DECIDE', 'GATE', 'ACT', 'ATTEST', 'REVIEW']}},
            'max_concurrent': {'type': 'integer', 'min': 1}
        }
    },
    'dependencies': {
        'type': 'object',
        'required': True,
        'fields': {
            'skills': {'type': 'list', 'items': {'type': 'string'}},
            'tools': {'type': 'list', 'items': {'type': 'string'}},
            'organs': {'type': 'list', 'items': {'type': 'string'}},
            'preconditions': {'type': 'list', 'items': {'type': 'string'}}
        }
    },
    'precedence': {
        'type': 'integer',
        'min': 0,
        'required': True
    },
    'conflicts_with': {
        'type': 'list',
        'items': {'type': 'string'},
        'required': True
    },
    'contract': {
        'type': 'object',
        'required': True,
        'fields': {
            'inputs': {'type': 'list', 'min_items': 1},
            'outputs': {'type': 'list', 'min_items': 1},
            'side_effects': {'type': 'list'},
            'reversible': {'type': 'boolean'}
        }
    },
    'reversibility': {
        'type': 'enum',
        'values': ['REVERSIBLE', 'GATED', 'IRREVERSIBLE'],
        'required': True
    },
    'owner': {
        'type': 'string',
        'required': True
    },
    'owner_organ': {
        'type': 'string',
        'required': True
    },
    'accountability': {
        'type': 'string',
        'required': True
    }
}
```

### 4.2 Invariant Checks

```python
INVARIANT_CHECKS = {
    'orthogonality': {
        'description': 'Skill must not overlap with another skill in the same tier',
        'check': lambda skill, all_skills: not any(
            set(skill['owns']) & set(other['owns'])
            for other in all_skills
            if other['id'] != skill['id'] and other['tier'] == skill['tier']
        ),
        'message': 'Skill owns territory already claimed by another skill in same tier'
    },
    'refusal_boundary': {
        'description': 'Skill must refuse at least as many things as it owns',
        'check': lambda skill: len(skill['refuses']) >= len(skill['owns']),
        'message': 'Skill refuses fewer things than it owns — insufficient boundary'
    },
    'purpose_singularity': {
        'description': 'Purpose must be ONE sentence',
        'check': lambda skill: skill['purpose'].count('.') <= 1,
        'message': 'Purpose has multiple sentences — split into two skills'
    },
    'cause_class_specificity': {
        'description': 'Skill must own at least one cause_class',
        'check': lambda skill: len(skill['cause_class']) >= 1,
        'message': 'Skill has no cause_class — cannot own any failures'
    },
    'dependency_acyclic': {
        'description': 'Skill dependencies must not form a cycle',
        'check': lambda skill, all_skills: not _has_cycle(skill, all_skills),
        'message': 'Skill has circular dependency'
    }
}
```

---

## 5. THE 13 BASIS SKILLS (spanning set)

These are the minimal orthogonal basis. Everything else is composition.

### 5.1 Substrate (always-on kernel — C0)

| Skill | Purpose | Owns | Refuses | Stage |
|-------|---------|------|---------|-------|
| **GROUND** | Attach to reality, evidence tagging | Evidence labeling (OBS/DER/INT/SPEC) | Interpretation, judgment | SENSE |
| **ROUTE** | Pick least-power path that works | Intent classification, organ routing | Execution, judgment | SENSE |
| **REFUSE** | Know what NOT to do | Refusal boundaries, sovereignty checks | Execution, approval | GATE |
| **OBSERVE** | Sense state before acting | State observation, health probes | Mutation, judgment | SENSE |

### 5.2 Cognition (reasoning organs)

| Skill | Purpose | Owns | Refuses | Stage |
|-------|---------|------|---------|-------|
| **DECOMPOSE** | Turn a goal into a DAG of steps | Task decomposition, dependency analysis | Execution, judgment | DECIDE |
| **VERIFY** | Check a claim against evidence | Claim verification, evidence comparison | Judgment, execution | REVIEW |
| **CONTRAST** | Hold two models, find the tension | Contradiction detection, tension analysis | Resolution, judgment | DECIDE |
| **METABOLIZE** | Turn scar/eureka into a lesson | Failure metabolization, insight distillation | Execution, judgment | ATTEST |

### 5.3 Governance (sovereign, not just smart)

| Skill | Purpose | Owns | Refuses | Stage |
|-------|---------|------|---------|-------|
| **GATE** | Permission + reversibility check before action | Permission checking, reversibility assessment | Execution, judgment | GATE |
| **ATTEST** | Seal what happened to an audit chain | Audit sealing, provenance recording | Judgment, execution | ATTEST |
| **DEPRECATE** | Kill your own stale skills | Skill retirement, double-loop verdicts | Skill creation, execution | REVIEW |

### 5.4 Collaboration (mesh layer)

| Skill | Purpose | Owns | Refuses | Stage |
|-------|---------|------|---------|-------|
| **HANDOFF** | Pass a bounded task to another agent | Task packaging, context minimization | Execution, judgment | ACT |
| **DELEGATE** | Request capability you don't own | Capability discovery, delegation | Execution, judgment | ACT |
| **RECONCILE** | Merge results, resolve conflicting claims | Result merging, conflict resolution | Execution, judgment | REVIEW |

---

## 6. INSTITUTIONAL FLOW

Skills don't just exist — they occupy a stage. Stage order is the institution's constitution.

```
SENSE     (OBSERVE, GROUND, ROUTE)        → what is true?
           ↓
DECIDE    (DECOMPOSE, CONTRAST)            → what should happen?
           ↓
GATE      (GATE, REFUSE)                   → am I allowed?
           ↓
ACT       (domain + forge skills)          → do it
           ↓
ATTEST    (ATTEST, METABOLIZE)             → record + learn
           ↓
REVIEW    (VERIFY, DEPRECATE)              → was it right? keep or kill?
```

**Institutional invariant:** No skill in a later stage may fire until earlier stages sealed.

---

## 7. COLLABORATION MODEL

Agents collaborate through contracts, not intimacy.

```
Agent A needs capability it doesn't have
  ↓
A reads B's ADVERTISED contract (purpose, inputs, outputs, cost, permissions)
  ↓
A sends a BOUNDED task via HANDOFF (minimal context, no leakage)
  ↓
B executes under ITS OWN governance (A cannot override B's gates)
  ↓
B returns a TAGGED result (EVIDENCE/INTERPRET/UNKNOWN + seal)
  ↓
A RECONCILES it with its own claims (RECONCILE resolves conflict)
```

**Four collaboration invariants:**
1. **OPACITY** — agents share contracts, never internals
2. **SOVEREIGNTY** — each agent keeps its own veto; no remote override
3. **BOUNDED** — handoff carries minimum context (least-privilege)
4. **TAGGED** — every returned claim carries its epistemic label + seal

---

## 8. THE FIVE LAWS

1. A skill declares what it OWNS and REFUSES. (boundary)
2. Contract is static; memory is dynamic; keep a membrane. (trust + learning)
3. Skills should be ORTHOGONAL — a basis, not a pile. (composability)
4. Intelligence needs ~13 basis skills; the rest compose. (spanning set)
5. Agents collaborate through contracts, never internals. (sovereign mesh)

---

*DITEMPA BUKAN DIBERI — skills are contracts, not conversations.*
*SKILL INVARIANT SCHEMA v1.0 — 2026-08-04 — 333-AGI Δ MIND*
