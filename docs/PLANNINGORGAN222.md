# 🧠 PLANNINGORGAN222

> **CANON: TRUE · INDEX: 222 · INVARIANT: PLANNING_ORGAN**
> **EPOCH_INTRODUCED: v2026.07.17**
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## 0. WHAT THIS IS

PLANNINGORGAN222 is the **constitutional planning organ** of the arifOS Federation.
It sits at index 222 in the metabolic pipeline — between OBSERVE (111) and THINK (333) —
transforming raw intent into governed execution graphs.

Every plan emitted through `arif_think(mode=plan)` MUST conform to this schema.
A-FORGE `PlanValidator` enforces this schema before any multi-step execution.

**Planning is not behavior. Planning is an organ.**

---

## 1. SCHEMA

Every plan object MUST contain these six sections. Unknown fields are REJECTED.

### 1.1 TASK_GRAPH

```yaml
TASK_GRAPH:
  nodes:
    - id: string           # unique within plan, kebab-case
      description: string   # what this node does
      organ: string         # arifOS | A-FORGE | AAA | GEOX | WEALTH | WELL
      tool: string          # canonical tool name (arif_*, forge_*, geox_*, etc.)
      reversibility_class:  # REVERSIBLE | REVERSIBLE_WITH_ROLLBACK | IRREVERSIBLE
      blast_radius:         # LOW | MEDIUM | HIGH | FEDERATION
  edges:
    - from: string          # node id
      to: string            # node id
      type:                 # depends_on | triggers | vetoes
      condition: string     # human-readable condition for edge traversal
```

### 1.2 PRECONDITIONS

```yaml
PRECONDITIONS:
  required_state:
    memory: string          # "clean" | "dirty_ok" — what memory state is required
    registry: string        # "pinned" — registry must match live surface
    git: string             # "clean" | "dirty_ok" — git working tree state
    floors_active: list     # ["F1","F2","F11"] — which floors must be active
  evidence_required: list   # evidence IDs from arif_observe that must exist
  authority_required: string # OBSERVE_ONLY | SUGGEST | EXECUTE_REVERSIBLE | 888_HOLD
```

### 1.3 POSTCONDITIONS

```yaml
POSTCONDITIONS:
  expected_state:
    files_changed: list     # glob patterns of files expected to change
    receipts_written: list  # expected VAULT999 receipt types
    tags_applied: list      # expected git tags
    services_restarted: list # systemd units expected to restart
  verification:
    health_probe: list      # organs to probe after execution
    test_command: string    # verification command to run
```

### 1.4 VETO_POINTS

```yaml
VETO_POINTS:
  - trigger: string         # what triggers the veto
    authority: string       # who can override (sovereign | AAA_floor | PlanValidator | constitutional_gate)
    fallback: string        # what happens if veto is not overridden (HALT | SKIP_NODE | ROLLBACK)
```

### 1.5 REVERSIBILITY

```yaml
REVERSIBILITY:
  reversible: boolean       # true if entire plan is reversible
  rollback_plan_id: string  # reference to rollback plan (if exists)
  rollback_requires: string # what is needed to roll back (e.g., "prior_commit_sha", "db_snapshot")
  irreversible_nodes: list  # node IDs that cannot be undone
```

### 1.6 RECEIPT_LINEAGE

```yaml
RECEIPT_LINEAGE:
  plan_id: string           # unique plan identifier
  epoch_tag: string         # git tag at plan creation (e.g., "v2026.07.17")
  parent_plan_id: string    # plan that spawned this one (if any)
  vault_candidate: boolean  # true if this plan should be sealed to VAULT999
  constitutional_chain_id: string  # from arif_judge SEAL (if pre-judged)
```

---

## 2. GOVERNED LIFECYCLE

```
INTENT (human or agent)
    │
    ▼
arif_think(mode=plan) ─── emits PLANNINGORGAN222 object
    │
    ▼
PlanValidator (A-FORGE) ─── validates schema + preconditions
    │
    ▼
arif_judge ─── SEAL | HOLD | SABAR | VOID
    │
    ▼
arif_forge ─── dry_run → execute (node by node)
    │
    ▼
arif_seal ─── VAULT999 receipt (if vault_candidate=true)
```

**No plan may bypass PlanValidator. No plan may execute without arif_judge clearance on IRREVERSIBLE nodes.**

---

## 3. WORKED EXAMPLE — Multi-Organ Doc Rename

**Intent:** Rename 5 docs across arifOS and AAA to single-term names, aligning with ZEN naming doctrine.

```yaml
TASK_GRAPH:
  nodes:
    - id: verify-dirty-state
      description: "Confirm all organs have clean git state"
      organ: A-FORGE
      tool: forge_worktree
      reversibility_class: REVERSIBLE
      blast_radius: LOW

    - id: rename-arifos-docs
      description: "Rename 3 docs in arifOS to single-term canon names"
      organ: arifOS
      tool: arif_forge
      reversibility_class: REVERSIBLE_WITH_ROLLBACK
      blast_radius: MEDIUM

    - id: rename-aaa-docs
      description: "Rename 2 docs in AAA to single-term canon names"
      organ: AAA
      tool: forge_filesystem
      reversibility_class: REVERSIBLE_WITH_ROLLBACK
      blast_radius: MEDIUM

    - id: update-references
      description: "Update all internal references to renamed docs across federation"
      organ: A-FORGE
      tool: forge_filesystem
      reversibility_class: REVERSIBLE_WITH_ROLLBACK
      blast_radius: HIGH

    - id: verify-health
      description: "Probe all 6 organs after rename"
      organ: A-FORGE
      tool: forge_probe
      reversibility_class: REVERSIBLE
      blast_radius: LOW

    - id: tag-epoch
      description: "Tag all organs with new date stamp"
      organ: A-FORGE
      tool: forge_git
      reversibility_class: REVERSIBLE
      blast_radius: LOW

  edges:
    - from: verify-dirty-state
      to: rename-arifos-docs
      type: depends_on
      condition: "All organs clean"

    - from: verify-dirty-state
      to: rename-aaa-docs
      type: depends_on
      condition: "All organs clean"

    - from: rename-arifos-docs
      to: update-references
      type: depends_on
      condition: "arifOS renames committed"

    - from: rename-aaa-docs
      to: update-references
      type: depends_on
      condition: "AAA renames committed"

    - from: update-references
      to: verify-health
      type: depends_on
      condition: "All references updated"

    - from: verify-health
      to: tag-epoch
      type: depends_on
      condition: "All 6 organs healthy"

    - from: verify-dirty-state
      to: tag-epoch
      type: vetoes
      condition: "Any organ dirty → VETO entire plan"

PRECONDITIONS:
  required_state:
    memory: clean
    registry: pinned
    git: clean
    floors_active: ["F1","F2","F4","F11"]
  evidence_required: ["git-status-all-organs"]
  authority_required: EXECUTE_REVERSIBLE

POSTCONDITIONS:
  expected_state:
    files_changed: ["arifOS/docs/*.md", "AAA/docs/*.md"]
    receipts_written: ["plan-executed", "docs-renamed"]
    tags_applied: ["v2026.07.17"]
    services_restarted: []
  verification:
    health_probe: ["arifos","aforge","aaa","geox","wealth","well"]
    test_command: "cd /root && make health"

VETO_POINTS:
  - trigger: "Any organ dirty at verify-dirty-state"
    authority: PlanValidator
    fallback: HALT

  - trigger: "Reference update fails"
    authority: constitutional_gate
    fallback: ROLLBACK

  - trigger: "Health probe fails after rename"
    authority: sovereign
    fallback: ROLLBACK

REVERSIBILITY:
  reversible: true
  rollback_plan_id: "rollback-doc-rename-v2026.07.17"
  rollback_requires: "prior_commit_sha per organ"
  irreversible_nodes: []

RECEIPT_LINEAGE:
  plan_id: "doc-rename-zen-v2026.07.17"
  epoch_tag: "v2026.07.17"
  parent_plan_id: null
  vault_candidate: true
  constitutional_chain_id: null
```

---

## 4. INTEGRATION POINTS

### 4.1 arif_think(mode=plan)

When `arif_think` is called with `mode=plan`, the response MUST include a
`plan_object` field conforming to this schema. The kernel validates:

- All required sections present
- All node IDs unique within TASK_GRAPH
- All edge targets reference existing nodes
- PRECONDITIONS match current federation state
- No IRREVERSIBLE node without a VETO_POINT

### 4.2 A-FORGE PlanValidator

`PlanValidator` (at `/root/A-FORGE/src/domain/PlanValidator.ts`) reads the plan
object and enforces:

- Schema compliance (Zod validation against this spec)
- Precondition satisfaction (live state probe vs required_state)
- Veto chain integrity (every IRREVERSIBLE node has a veto path)
- Reversibility coherence (rollback_plan_id references a valid plan)

### 4.3 VAULT999 Receipt

If `vault_candidate=true`, the plan object is sealed to VAULT999 after completion
via `arif_seal`. The receipt includes plan_id, epoch_tag, node execution order,
veto events (if any), and final state.

---

## 5. CONSTITUTIONAL BOUNDARIES

- **F1 AMANAH:** Every plan must declare reversibility per node. IRREVERSIBLE nodes require explicit VETO_POINTS.
- **F2 TRUTH:** Every node's `description` and `expected_state` must use epistemic labels (OBS/DER/INT/SPEC).
- **F4 CLARITY:** ΔS ≤ 0 — plan must reduce federation entropy, never increase it.
- **F11 AUDIT:** Every executed plan leaves a receipt. Veto events are recorded as audit scars.
- **F13 SOVEREIGN:** Sovereign veto overrides all. Any node can be VETOED by F13.

---

## 6. EVOLUTION

This is a LIVING organ. As the federation matures, PLANNINGORGAN222 may gain:

- **Parallel execution groups** (fan-out nodes with bounded concurrency)
- **Conditional branches** (if-then-else node routing)
- **Time-bounded leases** (plan expires after N hours)
- **Cross-plan dependencies** (plan B depends on plan A's completion)

Each extension must pass the same gates: schema validation, PlanValidator, arif_judge, F13 ack.

---

*DITEMPA BUKAN DIBERI — Planning is forged, not given.*
*Epoch v2026.07.17 — Federation clean, gated, ready.*
