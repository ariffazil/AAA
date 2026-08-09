<!-- SATELLITE | tier:satellite | sot:STATE.md | 2026-08-09 -->
> **Satellite** — historical elaboration / design note / prior draft.  
> **Canonical SOT:** [`STATE.md`](./STATE.md) (§1–16).  
> If this file conflicts with STATE.md, **STATE wins**. Do not fork law here.  
> *One truth · Many projections · 0 contradictions* · DITEMPA BUKAN DIBERI.

# PLAN

> CANON: TRUE · INDEX: 222 · INVARIANT: PLANNING_ORGAN
> SCOPE: Federation-wide planning and refactor governance
> WIRED: `arif_think(mode=plan)` → A-FORGE `PlanValidator` → VAULT999
> IMPL: `/root/A-FORGE/src/domain/types/plan.ts` (W2 schema, canonical)
> FORGED: 2026-07-17 · DITEMPA BUKAN DIBERI

---

## 🔥 WHY

```
BEFORE:  INTENT → EXECUTION          (trust prompts)
AFTER:   INTENT → PLAN → AUDIT → EXECUTION → RECEIPT   (trust schema)
```

Without a Planning Organ, the federation has smart agents but not governed architecture. Every refactor, rename, or cross-organ operation is a prompt-exercise, not a constitutional pipeline.

---

## 🧬 SCHEMA

### Plan (the organ object)

| Field | Type | Rule |
|-------|------|------|
| `plan_id` | ULID | Identity. Stable across the plan's lifecycle. |
| `mission_id` | ULID | Parent mission this plan fulfills. |
| `tasks` | Task[] | Ordered DAG nodes. Declaration order ≠ execution order. |
| `edges` | Edge[] | `from_task_id → to_task_id`. Derived from `depends_on`. |
| `reversibility_class` | `reversible \| irreversible \| mixed` | Computed from tasks. `mixed` = at least one irreversible task. |
| `risk_tier` | `LOW \| MEDIUM \| HIGH \| CRITICAL` | `max(task.risk_tier)`. |
| `plan_state` | `DRAFT → REVIEW → APPROVED → RUNNING → COMPLETED \| ABORTED` | Lifecycle state machine. F13 gate at `APPROVED`. |
| `veto_points` | VetoPoint[] | Materialized from tasks. Each must clear before its task runs. |
| `judge_verdict` | `SEAL \| HOLD \| VOID \| SABAR` | arifOS 888 verdict. Only `SEAL` permits execution. |
| `judge_state_hash` | string \| null | Hash of judge state at verdict time. Set by arifOS, not factory. |

### Task (a single node)

| Field | Type | Rule |
|-------|------|------|
| `task_id` | ULID | Unique within the plan. |
| `tool` | string | MCP tool name to invoke. |
| `args` | Record | JSON-serializable arguments. |
| `depends_on` | string[] | task_ids that must complete before this one. |
| `reversibility_class` | `reversible \| irreversible` | Per-task reversibility. |
| `risk_tier` | `LOW \| MEDIUM \| HIGH \| CRITICAL` | Per-task risk. |
| `floor_context` | string[] | Most relevant floors to gate this task. |
| `veto_point` | VetoPoint? | Optional gate before execution. |
| `timeout_s` | number | Wall-clock timeout. Default 60. |
| `receipt` | TaskReceipt? | Populated post-execution. |

### VetoPoint

| Field | Type | Rule |
|-------|------|------|
| `veto_id` | ULID | Stable id. |
| `before_task_id` | string | Task that requires this veto to pass. |
| `floor` | string | Which floor's gate must clear (F1, F13, etc.). |
| `reason` | string | Human-readable. |
| `human_required` | boolean | True = F13 SOVEREIGN must explicitly ratify. |

### TaskReceipt

| Field | Type | Rule |
|-------|------|------|
| `verdict` | `SEAL \| HOLD \| VOID \| SABAR` | Execution verdict. |
| `started_at` | ISO 8601 | Execution start. |
| `ended_at` | ISO 8601 | Execution end. |
| `duration_ms` | number | Wall-clock duration. |
| `args_digest` | string | SHA-256 hex prefix of args. |
| `result_digest` | string | SHA-256 hex prefix of result. |

---

## 🔗 WIRING (what already exists)

### arif_think(mode=plan)
- Emits candidate plans conforming to this schema.
- Every plan = a candidate plan receipt.
- F2 TRUTH: uncertainties tagged. F7 HUMILITY: confidence ≤ 0.90.

### A-FORGE PlanValidator (`/root/A-FORGE/src/domain/planner/PlanValidator.ts`)
- Pre-execution gate: validates DAG acyclicity, root integrity, dependency closure, reachability, complexity.
- **Before**: post-hoc sanity check.
- **After this organ**: pre-execution constitutional gate. Enforces preconditions, veto points, reversibility rules.

### Session plan.md
- Becomes a **view** over the Planning Organ, not an ad-hoc scratchpad.
- Every session plan derives from this schema.

---

## 📋 PRECONDITIONS (before any task executes)

1. `plan_state ∈ {APPROVED, RUNNING}` — plan must be judged and approved.
2. `judge_verdict === SEAL` — arifOS 888 must have sealed the plan.
3. All `depends_on` tasks must have `receipt.verdict === SEAL`.
4. All `veto_points` for this task must be cleared (if `human_required`, F13 must ratify).
5. `plan.risk_tier` must not exceed the executor's authority band.

## 📋 POSTCONDITIONS (after each task executes)

1. `task.receipt` is populated with verdict, timestamps, digests.
2. If `receipt.verdict === VOID`: halt plan, signal to arifOS, do not proceed to dependent tasks.
3. If `receipt.verdict === SABAR`: pause plan, await human resolution.
4. Plan-level `plan_state` transitions per the state machine.
5. Every task receipt is auditable (F11).

---

## 🛑 VETO FLOW

```
Task with veto_point
    │
    ├─ human_required = false → FloorEnforcer clears gate → proceed
    │
    └─ human_required = true → 888_HOLD → notifier_channel → await F13
            │
            ├─ F13 SEAL → proceed
            └─ F13 HOLD/VOID → abort plan
```

---

## 🔄 REVERSIBILITY RULES

| Class | Rule |
|-------|------|
| `reversible` | Auto-rollback on failure. No F13 required. |
| `irreversible` | Blocked unless `plan.judge_verdict === SEAL`. Veto point required. |
| `mixed` | Plan contains both. Irreversible tasks individually gated. |

---

## 📜 RECEIPT LINEAGE

```
Plan created (plan_id, DRAFT)
    → arif_judge → SEAL (plan_state = APPROVED, judge_state_hash set)
    → Executor runs tasks in DAG order
    → Each task emits TaskReceipt
    → Final task completes → plan_state = COMPLETED
    → arif_seal → VAULT999 (plan receipt sealed, immutable)
```

---

## 🧪 WORKED EXAMPLE: 20-File Zen-MD Rename

### Plan: `zen-md-rename-2026-07-17`

**Tasks (simplified subset):**

```
T1: audit_multiword_files    tool=forge_filesystem_search  reversible  risk=LOW
T2: check_collisions         tool=forge_filesystem_stat     reversible  risk=LOW
T3: rename_files             tool=forge_filesystem_move     irreversible  risk=MEDIUM
    └─ veto_point: F1 AMANAH, human_required=false
T4: update_references        tool=forge_filesystem_patch    irreversible  risk=HIGH
    └─ veto_point: F13 SOVEREIGN, human_required=true
T5: verify_consistency       tool=forge_filesystem_search   reversible  risk=LOW
T6: seal_audit               tool=arif_seal                 irreversible  risk=CRITICAL
    └─ veto_point: F13 SOVEREIGN, human_required=true

Edges: T1→T3, T2→T3, T3→T4, T4→T5, T5→T6
```

**Gates:**
- T3 (rename): FloorEnforcer clears F1 gate (files are backed up, reversible via git).
- T4 (update refs): 888_HOLD fires. Arif must ratify before mass reference update.
- T6 (seal): 888_HOLD fires. Arif must ratify before VAULT999 append.

---

## 🔒 CONSTITUTIONAL BINDING

| Floor | How it binds Planning |
|-------|----------------------|
| F1 AMANAH | Plan must declare reversibility per task. Irreversible tasks require veto points. |
| F2 TRUTH | Every task declares epistemic state. Unknowns must be explicit. |
| F3 WITNESS | High-risk plans require tri-witness before SEAL. |
| F4 CLARITY | Plan must reduce entropy (ΔS ≤ 0). No dead tasks, no orphan edges. |
| F7 HUMILITY | Plan confidence ≤ 0.90. Unknowns declared. |
| F11 AUDIT | Every task emits a receipt. Plan lifecycle is traceable. |
| F13 SOVEREIGN | `human_required` veto points routed to Arif. Only Arif seals CRITICAL plans. |

---

## 📍 CANONICAL PATHS

| What | Where |
|------|-------|
| TypeScript schema (W2, canonical) | `/root/A-FORGE/src/domain/types/plan.ts` |
| PlanValidator (pre-execution gate) | `/root/A-FORGE/src/domain/planner/PlanValidator.ts` |
| Plan DAG skill (agent-facing) | `/root/AAA/registries/antigravity/skills/arifos-plan-dag/SKILL.md` |
| This canon file | `/root/AAA/docs/PLAN.md` |
| Epoch Architecture (333) | `/root/AAA/docs/EPOCH.md` |
| Memory Routing (444) | `/root/AAA/docs/MEMORY.md` |

---

*CANON: TRUE · INDEX: 222 · FORGED 2026-07-17 · DITEMPA BUKAN DIBERI*
