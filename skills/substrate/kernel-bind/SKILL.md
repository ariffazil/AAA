---
id: kernel-bind
name: kernel-bind
version: 1.0.0
layer: substrate
description: Bind governance before action. Every session must initialize constitutional
  floors, recognize sovereign signals, and classify autonomy tier before any other
  verb.
owner: F13 SOVEREIGN
status: active
three_axis: true
axis_version: 1.0.0
---

# kernel-bind

> **Purpose:** Bind governance before action. Every session must initialize constitutional floors, recognize sovereign signals, and classify autonomy tier before any other verb.

## Axis 1: Invariants

- **authority**: arif_init returns session_id + authority_band
- **evidence_schema**: F1-F13 floors loaded as constitutional truth
- **reversibility**: True
- **lineage**: session_id bound to all subsequent actions
- **trigger_semantics**: session_start OR new_conversation OR resume_after_idle
- **failure_contract**: HOLD — do not proceed without session_id
- **resource_budget**: {'cpu': 'minimal', 'time_ms': 5000, 'entropy': 'low'}
- **audit_surface**: ['session_id', 'authority_band', 'floors_loaded', 'sovereign_id']

## Axis 2: Bridge Connections

- **kernel_verbs**: ['arif_init', 'arif_judge']
- **skills**: ['observe-ground', 'verify-gate']
- **knowledge**: ['know-language']
- **protocol**: synchronous_rpc
- **inputs**: {'actor_id': 'string', 'intent': 'string', 'context': 'object'}
- **outputs**: {'session_id': 'string', 'authority_band': 'enum[T1,T2,T3]', 'allowed_verbs': 'list[string]'}

## Axis 3: Contrast

- **Not**: kernel-floors, kernel-act, kernel-sovereign
- **Distinction**: BINDING ACTION at session start. kernel-floors is floor KNOWLEDGE. kernel-act is POST-verdict execution. kernel-sovereign is signal RECOGNITION.
- **Trigger conflicts**: fires ONLY at session init or resume, never mid-session

## Replaces

- `kernel-invariants`
- `kernel-floors`
- `kernel-f1-gate`
- `kernel-sovereign`
- `kernel-escalation`
- `kernel-init`
- `kernel-membrane`
- `kernel-nusantara`
- `kernel-authority-detect`
- `CONSTITUTIONAL_REFLEX`
- `HOST_MEMBRANE_AWARENESS`
- `aaa-agent-invariants`
- `aaa-agentic-governance`
- `arifos-governance`
- `constitutional-reasoning`
- `f1-gate`
- `sovereign-recognize`
- `phase-escalation-discipline`
- `000-init-intent-classify`

---
*Forged: 2026-07-11 under F13 SOVEREIGN.*
*DITEMPA BUKAN DIBERI*
