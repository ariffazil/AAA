---
name: handoff-contract
id: handoff-contract
version: 2.0.0-wave2-merged
description: "Cross-agent handoff contract — input/output schema, capability requested, authority classification, evidence requirement, return contract, receipt."
owner: A-FORGE
risk_tier: medium
floor_scope: [F1, F2, F4, F11, F13]
doctrine: /root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md
merged_from:
  - FORGE-cross-agent-handoff (sha256: dad5a1f7d6c55b00b201dd51f5027c461d995d2bb92ae2f757eafc5e51f2086f)
wave: 2
ts: 2026-09-16T22:46:00Z
audit: /root/.hermes/reports/hermes-skill-entropy-audit-2026-09-16.md
tombstones: /root/.hermes/.archive_skills_wave2/federation-handoff/TOMBSTONE-FORGE-cross-agent-handoff.json
triggers:
  - "handoff to OpenCode"
  - "delegate to another agent"
  - "cross-agent task"
  - "A2A handoff"
  - "task delegation"
attention:
  load_class: medium
  default_load: false
  prerequisite_skills: [FORGE-call-map]
  mutually_exclusive_with: []
  activation_signals:
    - "handoff"
    - "delegate"
    - "A2A"
  output_contract:
    - "handoff_envelope"
    - "trace_context"
    - "receipt"
    - "return_contract"
tags: [federation, handoff, A2A, delegation, F11, F13]
---

# core/federation/handoff-contract

Cross-agent task handoff envelope. Owner of the *delegation* contract: what may be asked of another
agent, under what authority, and what must come back. It does **not** own the transport (that is
`agent-to-agent-enablement`), the wire verbs (`a2a-task-delegator`), or the agent card
(`a2a-agent-card-registration`).

A handoff contract binds: sender organ · recipient organ · intent · capability requested · authority classification · trace context · evidence requirement · data minimization · return contract · receipt.

**Load the recovered envelope before composing one:** `references/absorbed-FORGE-cross-agent-handoff.md`
carries the handoff artifact schema, the four handoff rules (F1 reversibility, F4 entropy, F11
provenance, receiver-ACK), the context-manifest artifact classes, and the context-capture governance
rules. Recovered 2026-09-17 — the Wave-2 merge had recorded the move without carrying the body.

## The binding layers this contract stands on (do not restate them here)

| Layer | Canonical owner | What it already fixes |
|---|---|---|
| Transition states | `/root/AAA/instructions/state-transition-discipline.md` (AGENTS.md) | `PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ ACKNOWLEDGED`; timeout = `SYNCHRONIZATION_FAULT`, never silence; every handoff records `expected_event` + `owner` + `deadline`; consequential receipts carry `trace_id` |
| Authority | `/root/AAA/instructions/authority-envelope.md` (AGENTS.md) | the 10-field tuple ⟨Actor, Session, Host, Objective, Operation, Scope, Target, Issuer, Expiry, ExpectedPostcondition⟩; the executor may never issue its own envelope; `RESOLVED ≠ AUTHORIZED` |
| Claim states | `/root/AAA/instructions/state-transition-discipline.md` §Claim States | `ESTIMATED → MEASURED → CROSS_VALIDATED → RETRACTED`; never serve a superseded number as live |

**Reconciliation note (2026-09-17).** The recovered envelope says *"receiving agent must ACK within
10s or escalate."* That rule is now generalized by the transition law above: a fixed 10 s is one
instance of a deadline, and a missed deadline reclassifies the blocker as `SYNCHRONIZATION_FAULT`
with the owner of the next action named — it is not an incident and it must not resolve disagreement
by silence. Keep the deadline; take the fault classification from the law.

## The one invariant

```
Delegation transfers a task scope, never sovereign authority.
```

A receiving agent may refuse any delegated task that violates its own local invariants. Acceptance is
explicit — silence is not acceptance. A result is not completion until it carries a receipt and
passes the acceptance tests declared in the envelope.

## Usage

```text
"handoff X to OpenCode with capability Y"
→ produces handoff envelope + trace + receipt
```

## Rollback

```bash
git checkout entropy-wave2-pre-act-20260916T144144Z -- skills/FORGE-cross-agent-handoff/
rm -rf skills/core/federation/handoff-contract/
```

## Provenance
- **Wave:** 2, item 5
- **Deprecation window:** 90 days (cross-agent routing — safety-critical)

**DITEMPA BUKAN DIBERI ⚒️**
## Absorbed references (Wave-2 merge completion)
- `references/absorbed-FORGE-cross-agent-handoff.md` — content absorbed from the retired `FORGE-cross-agent-handoff` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
