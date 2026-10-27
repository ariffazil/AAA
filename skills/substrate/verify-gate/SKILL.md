---
# verify-gate — Six Gates Before Commitment
# UPDATED: 2026-08-12 — Added Gate 5: REALITY (C4 + E20 enforcement)
# UPDATED: 2026-10-28 — Added Gate 0: REFUSAL (E4/E15 Consequence-Bearer Refusal Enforcement)

id: verify-gate
name: verify-gate
risk_tier: low
floor_scope: [F1, F2, F4, F6, F7, F11, F13]
version: 2.1.0
layer: substrate
description: 'Six gates before commitment: REFUSAL + authority + evidence + reversibility + lineage + REALITY. All must open. One refusal or missing check = HOLD.'
owner: F13 SOVEREIGN
status: active
three_axis: true
axis_version: 2.1.0
autonomy_tier: T1
capability_tier: fed-agent-subagent
ecology_state: WARM
owned_by: F13 SOVEREIGN
authority_of: F13 SOVEREIGN
---

# verify-gate

> **Purpose:** Six gates before commitment. All must open. One refusal or missing check = HOLD.
>
> **v2.1.0 CHANGE (2026-10-28):** Added Gate 0 — REFUSAL. Per E4/E15 and 2026-10-28 live probe.
> Even if authority, evidence, reversibility, lineage, and reality pass, an active refusal from a named consequence-bearer halts execution unconditionally.
> Refusal can block execution; it can NEVER authorize execution.
>
> **v2.0.0 CHANGE:** Added Gate 5 — REALITY. Per Gödel Eureka #4 and Reality-First RULE 1.

## The Six Gates

### Gate 0: REFUSAL (NEW — v2.1.0)
- Is there a named consequence-bearer for this action?
- Is there an active Signed Refusal Object in scope (`status: ACTIVE`, `position: NO`)?
- Does silence exist? (Absence of response is NOT consent).
- **Fail / Active Refusal → HOLD (EXECUTION_BLOCKED)** — human bearer said NO.

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

### Gate 5: REALITY (v2.0.0)
- Does the claimed state match live reality?
- C4 Reality Drift Gate: probe live endpoints
- E20 Truth Metabolism: are supporting claims still FRESH?
- **Fail → HOLD** — reality contact broken or stale
- **Implementation:** `c4_reality_drift_gate.py` + `truth_metabolism.py`
- **Doctrine:** "Reality before judgment" (Reality-First RULE 1)

## Gate Logic

```python
# All six gates must pass for execution or a SEAL
gates = {
    "refusal": check_refusal(action, consequence_bearer),     # Gate 0 (Must not have active NO)
    "authority": check_authority(session, action),
    "evidence": check_evidence(claims, labels),
    "reversibility": check_reversibility(action, auth_band),
    "lineage": check_lineage(session, constitutional_chain),
    "reality": assess_reality_drift(claimed_state, session),
}

if gates["refusal"].active_refusal:
    verdict = "HOLD"  # Consequence-bearer veto is absolute
elif all(g.passed for g in gates.values()):
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
- **evidence_schema**: 6-gate checklist: refusal|authority|evidence|reversibility|lineage|reality
- **reversibility**: gate itself is reversible; gated action may not be
- **lineage**: verification receipt includes all 6 gate results
- **reality**: C4 probe + E20 metabolism check — LIVE, not cached
- **trigger_semantics**: irreversible_action OR high_blast_radius OR claim_to_seal OR mutation_request
- **failure_contract**: HOLD — surface which gate failed, do not proceed
- **resource_budget**: {'cpu': 'moderate', 'time_ms': 15000, 'entropy': 'neutral'}
- **audit_surface**: ['gates_passed', 'gates_failed', 'verdict', 'evidence_count', 'reality_verdict', 'refusal_status']

## Axis 2: Bridge Connections

- **kernel_verbs**: ['arif_verify', 'arif_critique', 'arif_judge']
- **skills**: ['kernel-bind', 'observe-ground', 'audit-seal', 'know-physics']
- **knowledge**: ['know-math', 'know-physics']
- **protocol**: synchronous_rpc
- **inputs**: {'action': 'string', 'evidence': 'list', 'reversibility': 'enum[reversible,irreversible]', 'blast_radius': 'enum[low,medium,high]', 'claimed_state': 'dict', 'consequence_bearer': 'string'}

## Axis 3: Contrasts

- **vs audit-seal**: verify-gate runs BEFORE action. audit-seal runs AFTER.
- **vs kernel-bind**: verify-gate checks action admissibility. kernel-bind checks session identity.
- **vs observe-ground**: verify-gate checks internal consistency. observe-ground checks external evidence.
