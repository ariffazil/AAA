# AAA_FEDERATION_CONVERGENCE_PLAN — Convergence V1

> **Mission:** AAA_FEDERATION_CONVERGENCE_V1
> **Date:** 2026-08-07
> **Author:** Hermes (federation architect + verifier)
> **Doctrine:** Reuses AAA_FEDERATION_CONTRACT_v0.1 + AAA_EUREKA_DOCTRINE_v1. No new doctrine.
> **Precondition:** Gap report + enforcement matrix (companion docs) read first.

---

## Objective Restated

Establish a single enforceable AAA federation contract across all active agents such that **no governed action bypasses: 333 Proposal → 555 Verification → 888 Judgment → Receipt Emission**.

## Success Condition

For every active harness:
1. Every T2/T3 action has a traceable judgment path (INV-03)
2. Every spawn carries an envelope with inheritance (INV-01, INV-14)
3. Every gate disable emits a receipt (INV-15)
4. E-22 answer flips to NO for all mutation/delegation paths

---

## Phase 0 — Envelope Canon (shared, no new doctrine)

**Owner:** Hermes (architect)
**Action:** Publish the canonical envelope as a machine-readable schema alongside `spawn_enums.json`:

```yaml
# federation/protocols/federation_envelope.yaml
envelope_version: 0.1.0
fields:
  identity:      {type: string, required: true}
  authority:     {enum: [OBSERVE_ONLY, DRAFT_ONLY, EXECUTE_REVERSIBLE, EXECUTE_AFTER_SEAL, DISPATCH_ONLY, JUDGMENT_ONLY], required: true}
  classification: {enum: [OBSERVE, T1, T2, T3], required: true}
  constraints:   {type: list, required: true}
  receipt_id:    {type: string, required: true}
  parent_receipt: {type: string, required: false}   # null at root
  harness:       {type: string, required: true}
```

**Gate:** existing contract already defines these concepts (INV-01/02/03/14). This is packaging, not doctrine.

---

## Phase 1 — Close the Worst Offender (OpenClaw)

**Owner:** Hermes (wiring) — OpenClaw gateway is live but gate-free.
**Action:** Wire a pre-tool hook equivalent for OpenClaw. OpenClaw runs from system node_modules; the gate must be a wrapper or plugin in its config path `/root/.openclaw/`.
**Success:** OpenClaw T3 blocked with receipt; E-22 for OpenClaw flips to NO.
**Reversible:** yes (hook removal = restore).
**Risk:** OpenClaw is a WebSocket gateway — hook insertion point must be verified in its plugin system first.

## Phase 2 — Judgment Escalation (K-03)

**Owners:** Hermes + Kimi.
**Action:** Upgrade T2 from WITNESSED to arif_judge-routed:
- Hermes: T2 tools (write_file, patch, terminal-normal, cronjob) → attempt arif_judge; fail-closed HOLD if arifOS down.
- Kimi: extend PreToolUse matcher to include spawn tools (`task`, af-* spawn) + route T2 to arif_judge.
**Success:** T2 without judgment marker → exit 2 (both harnesses).
**Reversible:** yes (config revert).

## Phase 3 — Spawn Envelope Inheritance (K-04)

**Owners:** Hermes + OpenCode + Kimi.
**Action:** Every delegate_task/task/af-* call must embed the parent envelope; child receipt must reference parent_receipt. Spawn without envelope → denied.
- Hermes: prepend envelope to delegate_task context; gate rejects spawns lacking it.
- OpenCode: task tool now gated (MUTATE_PATTERNS); extend gate to require envelope in args.
- Kimi: add spawn matcher to PreToolUse + envelope check.
**Success:** child authority ≤ parent authority, receipt chain intact.
**Reversible:** yes (rollback config + hook).

## Phase 4 — gate.disabled Receipt (INV-15 closure)

**Owners:** All active harnesses.
**Action:** Add `gate.disabled` event to receipt schemas (Hermes hook, OpenCode gate, Kimi witness). Emitted when hook removed/disabled.
**Success:** disabling any gate leaves a receipt.
**Reversible:** n/a (receipt emission only).

## Phase 5 — Dormant Activation Policy

**Owner:** Hermes (policy record) + AAA registry.
**Action:** Record in agent registry: on reactivation, dormant agents must adopt envelope + gate before tools unlock. No ungoverned reactivation.
**Success:** GAP-08 closed by policy + receipt.
**Reversible:** yes (policy doc).

## Phase 6 — E-22 Retest (K-05, verification)

**Owner:** Hermes (verifier) — rerun live probes on all harnesses.
**Action:** Re-run the E-22 penetration test per harness; compare before/after against the matrix in this session.
**Success:** Previously-YES paths flip to NO; report delta.
**Reversible:** n/a (read-only test).

---

## Dependency Order

```
Phase 0 (envelope canon)
   ↓
Phase 1 (OpenClaw gate)          ← independent of P0 but needs envelope format
   ↓
Phase 2 (K-03 judgment escalation)
   ↓
Phase 3 (K-04 spawn inheritance) ← needs P0 envelope
   ↓
Phase 4 (gate.disabled)          ← needs P0 receipt schema
   ↓
Phase 5 (dormant policy)         ← independent
   ↓
Phase 6 (E-22 retest)            ← needs P1–P4 complete
```

## F13 Decision Points (each phase requires sovereign authorization)

| Phase | Decision |
|---|---|
| P0 | Approve envelope schema as canonical (no new doctrine, packaging only) |
| P1 | Authorize OpenClaw hook wiring (T2 — runtime change on live gateway) |
| P2 | Authorize T2→arif_judge escalation on Hermes + Kimi (T2 — behavioral change) |
| P3 | Authorize spawn envelope enforcement (T2 — delegation behavior change) |
| P4 | Authorize gate.disabled receipt (T1 — additive) |
| P5 | Authorize dormant activation policy (T1 — doc) |
| P6 | Run E-22 retest (T1 — read-only) |

---

## What This Plan Does NOT Do

- ❌ Adds no doctrine, no Eurekas, no new floors
- ❌ Does not redesign OpenCode's gate (OpenCode implements, does not architect)
- ❌ Does not unify models (E-20: models differ, constitution same)
- ❌ Does not push to origin without F13

## What This Plan Delivers

- ✅ Single envelope across harnesses (identity, authority, classification, constraints, receipt, parent)
- ✅ Enforcement matrix with clear YES/NO per action class
- ✅ Spawn inheritance (parent governed → child governed)
- ✅ gate.disabled receipt (no silent control removal)
- ✅ E-22 retest proving convergence

---

**Ω₀ ≈ 0.04. Confidence: 0.90.**
**DITEMPA BUKAN DIBERI.**
