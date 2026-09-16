---
# verify-gate — Five Gates Before Commitment
# UPDATED: 2026-08-12 — Added Gate 5: REALITY (C4 + E20 enforcement)

id: verify-gate
name: verify-gate
risk_tier: low
floor_scope: [F1, F2, F4, F7, F11]
version: 2.0.0
layer: substrate
description: 'Five gates before commitment: authority + evidence + reversibility + lineage + REALITY. All five must open. One missing = HOLD.'
owner: F13 SOVEREIGN
status: active
three_axis: true
axis_version: 2.0.0
autonomy_tier: T1
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# verify-gate

> **Purpose:** Five gates before commitment. All five must open. One missing = HOLD.
>
> **v2.0.0 CHANGE:** Added Gate 5 — REALITY. Per Gödel Eureka #4 and Reality-First RULE 1.
> The previous 4 gates verified the SYSTEM's internal consistency.
> Gate 5 verifies the system's CONTACT WITH REALITY.

## The Five Gates

### Gate 1: AUTHORITY
- Who is authorizing this action?
- Does the actor have a valid session?
- Is the authority band sufficient for this action class?
- **Fail → HOLD** — authority insufficient

### Gate 2: EVIDENCE
- Is there evidence supporting this action?
- Does evidence carry OBS/DER/INT/SPEC labels?
- Is confidence ≤ 0.90 (F7 HUMILITY cap)?
- **Fail → HOLD** — evidence insufficient

### Gate 3: REVERSIBILITY
- Can this action be undone?
- If irreversible → is there 888_HOLD authorization?
- F1 AMANAH: reversible-first
- **Fail → HOLD** — irreversibility not authorized

### Gate 4: LINEAGE
- Is there a constitutional chain back to F13?
- Is there a session trace?
- Is there a prior verb in the Golden Path?
- **Fail → HOLD** — lineage broken

### Gate 5: REALITY (NEW — v2.0.0)
- Does the claimed state match live reality?
- C4 Reality Drift Gate: probe live endpoints
- E20 Truth Metabolism: are supporting claims still FRESH?
- **Fail → HOLD** — reality contact broken or stale
- **Implementation:** `c4_reality_drift_gate.py` + `truth_metabolism.py`
- **Doctrine:** "Reality before judgment" (Reality-First RULE 1)

## Gate Logic

```python
# All five gates must pass for a SEAL
gates = {
    "authority": check_authority(session, action),
    "evidence": check_evidence(claims, labels),
    "reversibility": check_reversibility(action, auth_band),
    "lineage": check_lineage(session, constitutional_chain),
    "reality": assess_reality_drift(claimed_state, session),  # NEW
}

if all(g.passed for g in gates.values()):
    verdict = "PROCEED"
elif gates["reality"].verdict == "UNKNOWN":
    verdict = "HOLD"  # can't verify reality → can't verify safety
elif gates["reality"].verdict == "DRIFT":
    verdict = "SABAR"  # reality diverges → re-probe before proceeding
else:
    verdict = "HOLD"  # some other gate failed
```

## Axis 1: Invariants

- **authority**: arif_verify checks token + command_hash + actor
- **evidence_schema**: 5-gate checklist: authority|evidence|reversibility|lineage|reality
- **reversibility**: gate itself is reversible; gated action may not be
- **lineage**: verification receipt includes all 5 gate results
- **reality**: C4 probe + E20 metabolism check — LIVE, not cached
- **trigger_semantics**: irreversible_action OR high_blast_radius OR claim_to_seal OR mutation_request
- **failure_contract**: HOLD — surface which gate failed, do not proceed
- **resource_budget**: {'cpu': 'moderate', 'time_ms': 15000, 'entropy': 'neutral'}
- **audit_surface**: ['gates_passed', 'gates_failed', 'verdict', 'evidence_count', 'reality_verdict']

## Axis 2: Bridge Connections

- **kernel_verbs**: ['arif_verify', 'arif_critique', 'arif_judge']
- **skills**: ['kernel-bind', 'observe-ground', 'audit-seal', 'know-physics']
- **knowledge**: ['know-math', 'know-physics']
- **protocol**: synchronous_rpc
- **inputs**: {'action': 'string', 'evidence': 'list', 'reversibility': 'enum[reversible,irreversible]', 'blast_radius': 'enum[low,medium,high]', 'claimed_state': 'dict'}

## Axis 3: Contrasts

- **vs audit-seal**: verify-gate runs BEFORE action. audit-seal runs AFTER.
- **vs kernel-bind**: verify-gate checks action admissibility. kernel-bind checks session identity.
- **vs observe-ground**: verify-gate checks internal consistency. observe-ground checks external evidence.
