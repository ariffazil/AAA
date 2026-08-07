# AAA Federation Enforcement Matrix v0.1

> **Status:** DRAFT — companion to GAP_REPORT_v0.1
> **Reuses:** AAA_FEDERATION_CONTRACT_v0.1.x, EUREKA_EXTRACTION_2026-08-07.md
> **Source:** Kimi directive 2026-08-07 (mission: AAA_FEDERATION_CONVERGENCE_V1)

---

## Purpose

A canonical **envelope** every agent must carry, plus inheritance
rules, plus an enforcement matrix by risk tier. Three artifacts
the federation needs in order to converge.

This document does not add doctrine. It defines the *operational
shape* of existing invariants.

---

## A. Canonical Federation Envelope

Every agent in arifOS's jurisdiction must carry this envelope on
every action. Six fields, no more, no less:

```yaml
identity:
  actor_id: "FI-XXXX"          # canonical registry ID (FI-001, FI-007, etc.)
  session_id: "ses_..."        # minted by arif_init, never local
  parent_session_id: "ses_..." # null for primary; set for spawned child
  harness: "opencode | hermes | kimi-code | ..."
  epoch: "2026-08-07T..."      # session start timestamp

authority:
  band: "OBSERVE_ONLY | LIMITED_MUTATE | FULL"   # from arif_init
  tier: "T0 | T1 | T2 | T3"                     # action class
  scopes: ["read", "write", "delete", "secrets", "deploy"]
  lease_id: "lease_..."        # from arif_judge grant
  lease_expires: "epoch"

action:
  name: "write_file"           # what tool
  args_hash: "sha256:..."     # what content, NEVER the content itself
  intent: "audit probe"        # why this action, plain text
  archetype: "af-explore"      # if spawn-bearing

judgment_path:
  apex_verdict_ref: "vaul..." # when arif_judge has spoken
  apex_verdict_status: "SEAL | HOLD | VOID | null"
  judgment_required: false    # does this action NEED apex?

constraints:
  risk_tier: "T2"
  blast_radius: "local"
  reversibility: "high"
  ceiling_enforced: ["T2_MAX"]  # from archetype manifest

receipt:
  receipt_id: "receipt_..."    # canonical namespace, never local
  parent_receipt_id: "..."     # chains backward
  vault_anchor: "VAULT999:abc" # evidence says vault, not log
  observed_at: "epoch"
  tx_hash: "sha256:..."        # field-level provenance
```

**Six fields. Six invariants live inside this shape:**

- `identity.session_id` + `parent_session_id` — enforces E-04 (per-spawn governance)
- `authority.band` + `tier` — enforces E-12 (capability > instruction)
- `judgment_path.apex_verdict_ref` — enforces E-22 (cannot violate silently)
- `constraints.blast_radius` + `reversibility` — enforces E-11 (fail closed)
- `receipt.receipt_id` + `parent_receipt_id` — enforces E-18 (receipt > memory)
- `action.archetype` — enforces E-01 (work vs authority)

---

## B. Inheritance: parent → child

Every spawn produces a child whose envelope differs from parent in
exactly three fields and not the other three:

| Field                | Parent                   | Child                                              |
|----------------------|--------------------------|----------------------------------------------------|
| `authority.band`     | FULL (or LIMITED_MUTATE) | **OBSERVE_ONLY** (default) — child must ASK        |
| `action.name`        | (whatever)               | parent action that spawned (e.g. `delegate_task`)  |
| `parent_session_id`  | parent's own             | parent's session_id (mandatory; never null)        |
| `parent_receipt_id`  | parent's spawn receipt   | parent's spawn receipt (mandatory; never null)     |
| `lease_id`           | parent's lease           | **null** until child earns apex verdict            |
| `apex_verdict_status` | whatever                 | **null** until child acts under judgment           |

Three rules:

1. **Band demotes.** A FULL primary cannot spawn a FULL child. Spawn ⇔ demote to OBSERVE_ONLY.
2. **Lease disappears.** Child inherits authority but no lease. Child cannot exercise authority without explicit apex verdict.
3. **Receipt chains.** Every child action must carry both `parent_session_id` and `parent_receipt_id`. Dropping either = INVALID RETURN.

Inheritance is enforced by the spawn-gate (`hermes_mutation_gate.py`
for Hermes; analogous gates for OpenCode, Kimi, OpenClaw). The
gate sees the parent's envelope, emits the child's envelope,
appends the spawn receipt to VAULT999 atomically before the child
runs.

---

## C. Enforcement matrix by risk tier

| Tier | Risk class | Receipt path | Judgment path | Hermes gate verdict | OpenCode gate verdict | Kimi witness verdict |
|---|---|---|---|---|---|---|
| **T0** | read-only | write receipt to local journal | not required | ALLOW | ALLOW | exit 0 |
| **T1** | reversible mutate | write receipt + parent chain | not required unless apex asked | ALLOW | ALLOW (via MUTATE_PATTERNS) | exit 0 unless pattern matches catastrophic → exit 2 |
| **T2** | recommend / non-revert mutate | write receipt + parent chain + apex verdict ref | **REQUIRED** | REQUIRE_JUDGE → BLOCK (no apex) | REQUIRE_JUDGE (linked to local judge) | exit 2 (no apex) |
| **T3** | irreversible / cataclysmic | write receipt + parent chain + signed apex verdict | **MANDATORY** (`arif_seal` required) | BLOCK (with apex_exit_code 0 sub) | BLOCK with escalate | exit 2 unconditional |

**Defaults:**

- T0/T1: ALLOW. Gate is witness only. Receipt is recorded but does
  not block.
- T2: BLOCK unless `apex_verdict_present`. Receipt must contain
  apex verdict reference.
- T3: BLOCK ALWAYS unless `apex_verdict_present = true` AND
  `apex_verdict_status = "SEAL"`. Bare `apex_verdict_ref` is
  insufficient — it must be SEAL-class.

**Fail-closed:**

- If the gate script crashes mid-decision → caller must default to BLOCK.
- If receipt write fails → caller must still emit the verdict; receipt is backup.

---

## D. Where this matrix does NOT apply yet

This matrix is normative — it is the *target*. It is not operational
in any active harness today except partially in Kimi (T3 catastrophic
patterns only). Bringing every active harness to this matrix is the
Phase 1-2 work of AAA_FEDERATION_CONVERGENCE_PLAN_v0.1.
