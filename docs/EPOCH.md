# EPOCH

> CANON: TRUE · INDEX: 333 · INVARIANT: EPOCH_ARCHITECTURE
> SCOPE: Federation-wide temporal continuity and audit
> WIRED: Epoch wraps Plan → EpochEvent log → VAULT999 seal
> IMPL: `/root/A-FORGE/src/domain/types/epoch.ts` (W3 schema, canonical)
> DEPENDS: PLAN (INDEX 222)
> FORGED: 2026-07-17 · DITEMPA BUKAN DIBERI

---

## 🔥 WHY

```
Session = stateless interaction. Cannot carry continuity.
Epoch   = governed continuity unit. Carries state, events, lineage.
```

Without Epochs:
- Sessions are isolated moments — no temporal binding
- Audit trails exist per-action but not per-mission
- Restarts lose context
- Drift between sessions is invisible
- Memory is untethered from time

With Epochs:
- Every mission is a governed continuity unit
- Epoch receipts carry start→end lineage
- Restarts resume from checkpoints (W11 Temporal)
- Drift between epochs is detected and recorded
- Memory is time-bound and auditable

---

## 🧬 SCHEMA

### Epoch (the lifecycle wrapper)

| Field | Type | Rule |
|-------|------|------|
| `epoch_id` | UUID | Identity. Stable across the epoch's lifecycle. |
| `plan_id` | UUID | Reference to W2 Plan. Plan = static intent; Epoch = runtime lifecycle. |
| `mission_id` | UUID | Reference to parent Mission. |
| `state` | EpochState | State machine position. |
| `created_at` | ISO 8601 | Epoch birth. |
| `started_at` | ISO 8601? | Last CREATED→ACTIVE or SUSPENDED→ACTIVE transition. |
| `completed_at` | ISO 8601? | Last transition to COMPLETED. |
| `max_wall_clock_seconds` | number | Budget from RunConfig. Default 3600. |
| `remaining_seconds` | number | Computed: max − elapsed. |
| `events` | EpochEvent[] | Append-only, hash-chained event log. NEVER mutated after append. |
| `checkpoints` | EpochCheckpoint[] | Durable snapshots for resume (W11 Temporal). |
| `f13_halt_active` | boolean | F13 SOVEREIGN halt. If true, no further transitions. |
| `genesis_event_hash` | string | Hash of first event in the log. |
| `latest_event_hash` | string | Hash of latest event — the chain head. |

### EpochState (the state machine)

```
CREATED ──start()──→ ACTIVE ──complete()──→ COMPLETED  (terminal)
               │         │
               │         ├─fail()───────→ FAILED       (terminal)
               │         ├─abort()──────→ ABORTED      (terminal, F13)
               │         └─suspend()───→ SUSPENDED
               │                              │
               │                              └─resume()─→ ACTIVE
               │
               └─F13 halt (any state)──→ F13_HALTED  (terminal, F13)
```

| State | Meaning | Terminal? |
|-------|---------|-----------|
| CREATED | Fresh, not yet started | No |
| ACTIVE | Executor running tasks | No |
| SUSPENDED | Paused (budget, F13 pre-resolution) | No |
| COMPLETED | All tasks completed, result sealed | Yes |
| FAILED | Unrecoverable error | Yes |
| ABORTED | F13 human aborted | Yes (F13 only) |
| F13_HALTED | F13 halt active | Yes (F13 only) |

### EpochEvent (a single append-only entry)

| Field | Type | Rule |
|-------|------|------|
| `event_id` | UUID | Stable id. |
| `epoch_id` | UUID | Parent epoch. |
| `event_type` | EpochEventType | What happened (14 types). |
| `ts` | ISO 8601 | When it happened. |
| `task_id` | string? | Linked task (for task events). |
| `actor_id` | string? | Who acted (for F13 events). |
| `verdict` | SEAL\|HOLD\|VOID\|SABAR | Verdict on this event. |
| `state_hash` | string? | Hash of state at event time (checkpoint linkage). |
| `payload` | Record | Free-form, JSON-serializable. |
| `vauld_seal_id` | string? | Pointer to VAULT999 sealed entry. |
| `prev_event_hash` | string | Hash of previous event (tamper-evident chain). |
| `event_hash` | string | SHA-256 of this event's canonical form. |

**Hash chain rule:** `event_hash[N] = SHA-256(event_hash[N-1] || canonical(event[N]))`. Altering any event breaks the chain downstream. This is F2 TRUTH for time.

### EpochCheckpoint (durable snapshot)

| Field | Type | Rule |
|-------|------|------|
| `checkpoint_id` | UUID | Stable id. |
| `epoch_id` | UUID | Parent epoch. |
| `ts` | ISO 8601 | Snapshot time. |
| `state_hash` | string | SHA-256 of serialized epoch state. |
| `last_event_id` | string | Last event before this checkpoint. |
| `reason` | enum | Why: PERIODIC, ON_SUSPEND, ON_F13_HALT, ON_ABORT, ON_COMPLETE, MANUAL. |
| `storage_ref` | string? | L1/L2/L3/L4/L5 storage location. |
| `event_count` | number | Events at checkpoint time. |

### Event Types (14 canonical)

| Event | Trigger | Sets state to |
|-------|---------|---------------|
| EPOCH_CREATED | Epoch object created | CREATED |
| EPOCH_STARTED | start() called | ACTIVE |
| EPOCH_TASK_STARTED | Task begins execution | (no state change) |
| EPOCH_TASK_COMPLETED | Task verdict = SEAL | (no state change) |
| EPOCH_TASK_FAILED | Task verdict = VOID | (no state change) |
| EPOCH_VETO_TRIGGERED | Veto point fired | (no state change) |
| EPOCH_VETO_RESOLVED | F13 resolves veto | (no state change) |
| EPOCH_SUSPENDED | suspend() called | SUSPENDED |
| EPOCH_RESUMED | resume() called | ACTIVE |
| EPOCH_CHECKPOINT | Snapshot saved | (no state change) |
| EPOCH_COMPLETED | All tasks done | COMPLETED |
| EPOCH_FAILED | Unrecoverable error | FAILED |
| EPOCH_ABORTED | F13 abort | ABORTED |
| EPOCH_F13_HALTED | F13 halt | F13_HALTED |

---

## 🔗 WIRING (what already exists)

### Epoch wraps Plan
- `Plan` = static intent (DAG of tasks, veto points).
- `Epoch` = runtime lifecycle of that plan.
- One Epoch per Plan. One Plan per Mission.

### EpochEvent log → VAULT999
- Every event is hash-chained (tamper-evident).
- `vauld_seal_id` links events to VAULT999 sealed records.
- On EPOCH_COMPLETED: the full event log can be sealed as a single VAULT999 receipt.

### Checkpoints → W11 Temporal
- `EpochCheckpoint` stores a durable snapshot at checkpoints.
- W11 Temporal executor uses checkpoints to resume after crash/restart.
- `state_hash` links checkpoint to the event chain.

### Session → Epoch binding
- A session is a stateless interaction window.
- Sessions inherit their epoch from the mission context.
- Session start = check for active epoch, resume if checkpoint exists.
- Session end = append EPOCH_CHECKPOINT or epoch close event.

---

## 📜 RECEIPT LINEAGE

```
Epoch created (CREATED)
    → EPOCH_CREATED event (genesis_event_hash set)
    → EPOCH_STARTED event (ACTIVE)
    → Task events... (EPOCH_TASK_STARTED, COMPLETED, FAILED)
    → Veto events... (EPOCH_VETO_TRIGGERED, RESOLVED)
    → Checkpoints... (EPOCH_CHECKPOINT)
    → EPOCH_COMPLETED event (COMPLETED)
    → arif_seal → VAULT999 (full epoch receipt sealed, immutable)
```

---

## 🧪 WORKED EXAMPLE: Stabilization Epoch (today)

### Epoch: `stabilization-2026-07-17`

```
EPOCH_CREATED    → { plan_id: "zen-md-stabilize", mission_id: "federation-stabilize" }
EPOCH_STARTED    → { actor: "copilot-cli" }
EPOCH_TASK_STARTED   → { task: "verify-refs" }
EPOCH_TASK_COMPLETED → { task: "verify-refs", verdict: SEAL, files_scanned: 22 }
EPOCH_TASK_STARTED   → { task: "handle-dirty-repos" }
EPOCH_TASK_COMPLETED → { task: "handle-dirty-repos", verdict: SEAL, repos: "AAA, WEALTH" }
EPOCH_TASK_STARTED   → { task: "update-context" }
EPOCH_TASK_COMPLETED → { task: "update-context", verdict: SEAL }
EPOCH_COMPLETED  → { total_tasks: 3, all_sealed: true }
→ arif_seal → VAULT999
```

---

## 🔒 CONSTITUTIONAL BINDING

| Floor | How it binds Epoch |
|-------|--------------------|
| F1 AMANAH | Epoch state transitions are reversible until terminal. Terminal states are permanent. |
| F2 TRUTH | Every event is hash-chained. Altering any event breaks the chain. The event log IS the truth. |
| F3 WITNESS | Epoch completion requires tri-witness before SEAL. |
| F4 CLARITY | Epoch must emit an event for every transition. No silent state changes. |
| F7 HUMILITY | Epoch confidence ≤ 0.90. Drift between epochs must be explicitly declared. |
| F11 AUDIT | Every event is an auditable entry. The event log is the audit trail. |
| F13 SOVEREIGN | ABORTED and F13_HALTED are F13-only transitions. Agents cannot issue them. |

---

## 🔗 RELATIONSHIP TO OTHER ORGANS

| Organ | Relationship |
|-------|-------------|
| **PLAN** (222) | Epoch wraps a Plan. Plan = static; Epoch = temporal. |
| **VAULT999** | Sealed epoch receipts live here. Immutable, append-only. |
| **W11 Temporal** | Executor that resumes epochs from checkpoints across restarts. (Spec: this forge.) |
| **SESSION** | Stateless interaction window within an epoch. Inherits epoch context. |
| **CONTEXT** | Reflects the current epoch's live state. |

---

## 📍 CANONICAL PATHS

| What | Where |
|------|-------|
| TypeScript schema (W3, canonical) | `/root/A-FORGE/src/domain/types/epoch.ts` |
| Plan schema (W2, dependency) | `/root/A-FORGE/src/domain/types/plan.ts` |
| This canon file | `/root/AAA/docs/EPOCH.md` |
| Planning Organ canon | `/root/AAA/docs/PLAN.md` |
| VAULT999 | `/root/arifOS/VAULT999/outcomes.jsonl` |

---

*CANON: TRUE · INDEX: 333 · FORGED 2026-07-17 · DITEMPA BUKAN DIBERI*
