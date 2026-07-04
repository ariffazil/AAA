# PR 3 SPEC — Truth-Bound Cockpit (deliverable for OpenCode)

> **Forged 2026-06-02 18:41 UTC under F13 SOVEREIGN ratification.**
> Implements PR 3 of the seven-repo forge order. See `/root/CONTEXT.md` ## RATIFIED: The Refusal-and-Authority Kernel.
> Consumed artifacts: PR 1 sealed at `cc77d077` — `arifOS/schemas/{receipt,mission,authority-state}.schema.json`, `arifOS/docs/{CORE_INVARIANTS,AUTHORITY_MODEL,VERDICT_SEMANTICS}.md`.

## Purpose

Make the AAA cockpit **truth-bound**: every badge, button, and verdict the operator sees is bound to a receipt from the kernel. No narrative. No overclaim. No bare "SEAL." This is the in-UI enforcement of the doctrine we just ratified.

## Scope (in / out)

**In scope:**
1. Consume the three PR 1 schemas as the AAA state model.
2. Implement the HOLD approval queue.
3. Bind every cockpit badge to a receipt.
4. Disable the in-UI "SEAL" affordance until `JUDGE_SEAL_AUTHORIZATION` is active.
5. Migrate the bare `SEAL` verdict in `deliberation.ts` to the namespaced seal grammar.
6. Add a truth-bound test.

**Out of scope:**
- Modifying arifOS's `888_JUDGE` (kernel logic stays in kernel).
- A-FORGE forge gate changes (PR 4 territory).
- arif-sites public surface (PR 2 territory).
- Domain organ advisory boundaries (PR 5/6/7 territory).

## F13 touchpoints (require sovereign ratification before code lands)

These changes touch constitutional logic. The spec author flags them; the operator ratifies them before OpenCode applies them:

| Change | File | F13 trigger? |
|---|---|---|
| Replace `'SEAL' \| 'HOLD_888' \| 'VOID'` with namespaced seal grammar | `src/gateway/deliberation.ts:14` | **YES** — modifies constitutional verdict type |
| Add `mission.schema.json` import as AAA state model | `src/gateway/server.ts` | **YES** — affects how AAA reads mission state |
| Disable "SEAL" button in cockpit UI | `src/Cockpit.tsx` | **YES** — modifies operator affordance |
| New approval queue component | `src/components/ApprovalQueue.tsx` (new) | no — additive |
| Truth-bound test | `tests/invariants/test_truth_bound_cockpit.py` (new) | no — test only |

OpenCode should **stage** the F13-flagged changes locally and surface them to the operator for ratification before commit. The non-F13 work (additive components, tests) may proceed.

---

## 1. Schema consumption (the data layer)

AAA's gateway server (`src/gateway/server.ts`) should import and use the three PR 1 schemas as the **canonical state model**:

```typescript
// src/gateway/state.ts (new file — extracts state types from the three PR 1 schemas)
import missionSchema from 'arifOS/schemas/mission.schema.json';
import receiptSchema from 'arifOS/schemas/receipt.schema.json';
import authorityStateSchema from 'arifOS/schemas/authority-state.schema.json';
import Ajv from 'ajv';

const ajv = new Ajv({ allErrors: true, strict: false });
const validateMission = ajv.compile(missionSchema);
const validateReceipt = ajv.compile(receiptSchema);
const validateAuthorityState = ajv.compile(authorityStateSchema);

export { validateMission, validateReceipt, validateAuthorityState, missionSchema, receiptSchema, authorityStateSchema };
```

**Why:** AAA should not invent its own state shape. The federation has one mission object, one receipt shape, one authority-state shape. The schemas are the contract.

**Where it goes:** `src/gateway/state.ts` is new. The path makes the federation state explicit and importable from anywhere in AAA.

---

## 2. Migration of the bare-SEAL bug

`src/gateway/deliberation.ts:14` currently declares:

```typescript
export type VerdictType = 'SEAL' | 'HOLD_888' | 'VOID';
```

This is a **doctrine violation** under the ratified `VERDICT_SEMANTICS.md`. The bare word `SEAL` is forbidden everywhere. Replace with namespaced seals:

```typescript
// After migration
export type VerdictType =
  | 'JUDGE_SEAL_AUTHORIZATION'  // F1-F13 cleared, APEX approved
  | 'KERNEL_SEAL_AWARENESS'     // kernel has seen the candidate
  | 'DOMAIN_SEAL_VALIDITY'      // domain calculation valid
  | 'HOLD_888'                  // constitutional hold (preserved)
  | 'VOID';                     // refused
```

**Migration map** for the rest of `deliberation.ts`:

| Old return value | New return value | Why |
|---|---|---|
| `verdict: 'SEAL'` after F1-F13 clear | `verdict: 'JUDGE_SEAL_AUTHORIZATION'` | The deliberation pattern scan cannot issue execution authority; it can only request it from the kernel |
| `verdict: 'HOLD_888'` | `verdict: 'HOLD_888'` (unchanged) | HOLD is a federated concept; keep its name |
| `verdict: 'VOID'` on F9 Anti-Hantu | `verdict: 'VOID'` (unchanged) | VOID is a federated concept |

**Critical insight:** the deliberation pattern scan in `deliberation.ts` cannot itself authorize execution. It can only *request* a `JUDGE_SEAL_AUTHORIZATION` from the kernel. The verdict it emits should be either a request or a refusal — never an authority claim.

Cleaner design:

```typescript
export type DeliberationVerdict =
  | { kind: 'JUDGE_SEAL_REQUEST'; rationale: string; confidence: number; evidence_chain: string[] }
  | { kind: 'HOLD_888'; rationale: string; confidence: number }
  | { kind: 'VOID'; rationale: string; confidence: number };
```

Discriminated union. The cockpit knows at the type level that deliberation never *grants* authority — it only *requests* it from the kernel.

---

## 3. Mission object integration

The AAA gateway should treat any incoming mission shape as a `mission.schema.json`-validated object. The `TaskStore` in `src/gateway/store.ts` should be typed against the schema:

```typescript
import type { Mission } from './state';  // generated from mission.schema.json

export class TaskStore {
  private tasks: Map<string, Mission> = new Map();

  create(mission: Mission): void { /* ... */ }
  get(missionId: string): Mission | undefined { /* ... */ }
  attachReceipt(missionId: string, receipt: Receipt): void { /* ... */ }
  hold(missionId: string, reason: string): void { /* ... */ }
  seal(missionId: string, seal_type: SealType, evidence_chain: string[]): void { /* ... */ }
}
```

Every `create()` validates against `missionSchema`. Every `attachReceipt()` validates against `receiptSchema`. Every `seal()` validates that the seal_type is one of the five namespaced seals.

**Why:** prevents drift. AAA can never accept a mission shape the kernel wouldn't accept.

---

## 4. HOLD approval queue

A new component: `src/components/ApprovalQueue.tsx`.

Contract:
- Subscribes to the gateway's `pending_holds` event stream.
- Renders a list of missions currently in `HOLD` state.
- For each HOLD, shows: `mission_id`, `objective`, `raised_at`, `raised_by`, `stage`, `reason`, and the **receipts attached** (linked, not narrated).
- Provides two operator actions per HOLD:
  - **APPROVE** — sends an APEX approval to the kernel. Triggers a re-judge. If APEX is bound (per session), the kernel may re-issue `JUDGE_SEAL_AUTHORIZATION`.
  - **REJECT** — sends a rejection. Mission transitions to `VOID`. The rejection is itself sealed to VAULT999 with `evidence_type = "apex_reject"`.

**UI rules (per `CORE_INVARIANTS.md` and the federation voice):**
- No HOLD is ever silent. If the queue is empty, the UI shows *"No missions currently held. Federation posture: see bottom bar."* — never an empty box that looks like "all clear."
- The "APPROVE" button is disabled unless `actor_verified = true` for the current session.
- The "APPROVE" button is disabled unless the kernel's `authority_state.actor.verified = true` is reflected in the operator session (per the 888_APEX identity flow).
- Every action shows a **receipt preview** before commit. The operator sees what evidence backs the action they're about to take.

**State shape:** consume `authority_state.schema.json`'s `active_holds[]` and `active_missions[]` fields.

---

## 5. Truth-bound cockpit badges

The current `Cockpit.tsx` already has `FLOORS_META` with floor IDs and names. Per the F2 comment in that file ("Initial state is UNKNOWN per F2"), the floor status is already derived from `/health`.

**Extend the truth-binding:**

| Current badge | New truth-bound behavior |
|---|---|
| Service health (green/yellow/red) | Render from `authority_state.public_posture.service_health`. Never show "green" if the gate is closed — see below. |
| Floor status (F1-F13) | Render from `/health` per existing F2 path. Add a **receipt preview** on click: which evidence backs this floor's status. |
| Mission state badge | Render from `mission.stages` of the current mission. The badge must include the **seal type** (one of 5), never a bare "SEAL." |
| Execution readiness | Render from `authority_state.public_posture.execution_readiness` (separate field from service_health). |
| Forge gate state | Render from `authority_state.forge_gate.enabled` and `authority_state.forge_gate.blockers[]`. The blockers list is the receipt. |

**The golden rule:** every badge derives from a field in `authority_state.schema.json`. No badge is computed locally without a receipt.

**Anti-pattern to remove:** if the cockpit currently has a "Mission SEALED" badge that fires on any `JUDGE_SEAL_AUTHORIZATION` regardless of evidence chain length, replace it with a receipts-count badge: *"JUDGE_SEAL_AUTHORIZATION — 3 receipts"* (linked, not narrated).

---

## 6. Disable the in-UI "SEAL" button

The cockpit must not have a button that *grants* a seal. The only button that *approves* a HOLD is the queue's "APPROVE" — and that button is **gated**:

```typescript
// src/components/ApprovalQueue.tsx (pseudocode)
const canApprove = (
  session.actor_verified === true
  && session.verification_method !== 'none'
  && pendingHold.evidence_chain.length > 0
  && pendingHold.context_verdict !== 'DEGRADED_CONTEXT'
);

<Button disabled={!canApprove} onClick={onApprove}>
  {canApprove ? 'APPROVE (APEX)' : 'Approval requires verified actor + non-degraded context'}
</Button>
```

If a previous version of the cockpit had a generic "Seal mission" or "Mark complete" button, **delete it**. That affordance is doctrine-forbidden.

---

## 7. Truth-bound test (the deliverable proof)

New file: `tests/invariants/test_truth_bound_cockpit.py` (or `.ts` — match AAA's test runner).

Cases to cover (minimum):

| Test | Asserts |
|---|---|
| `test_cockpit_no_bare_seal_badge` | The cockpit component, given a mission with `JUDGE_SEAL_AUTHORIZATION`, renders "JUDGE_SEAL_AUTHORIZATION" — not "SEAL" or "Sealed." |
| `test_cockpit_health_and_readiness_separate` | The cockpit renders `service_health` and `execution_readiness` as two independent fields. Setting one to "green" does not change the other. |
| `test_cockpit_approve_button_disabled_when_actor_unverified` | With `actor_verified = false`, the APPROVE button is disabled and the tooltip explains why. |
| `test_cockpit_approve_button_disabled_when_context_degraded` | With `context_verdict = DEGRADED_CONTEXT`, the APPROVE button is disabled and the tooltip explains why. |
| `test_cockpit_hold_never_silent` | When `active_holds[]` is empty, the UI shows the empty-state message — not a blank panel. |
| `test_cockpit_badge_derived_from_authority_state` | Every badge in the rendered DOM traces back to a field in `authority_state.schema.json`. (Implementation: render with a fake state, assert each badge text contains the source field name.) |
| `test_deliberation_does_not_emit_bare_seal` | The deliberation module never returns the string `"SEAL"` — only namespaced seals or HOLD/VOID. |
| `test_mission_create_validates_against_schema` | `TaskStore.create()` rejects any object that does not validate against `mission.schema.json`. |

Run the AAA test suite after these land. All must pass.

---

## Handoff

This spec is the **what**. The **how** is OpenCode's to choose. Constraints:

- Keep the F13-flagged changes in a separate commit so the operator can review them in isolation.
- The additive work (approval queue component, test file, state module) may land in any order.
- Do **not** push to HF until the operator has ratified the F13-flagged changes and the AAA test suite is green.

When complete, surface:
- AAA PR link (or local commit SHA)
- Test output (test count, pass count, names of F13-flagged commits)
- The 11-file staging list for the next HF push, if any of the changes belong in the HF dataset

---

**DITEMPA BUKAN DIBERI — Forged, Not Given.**
