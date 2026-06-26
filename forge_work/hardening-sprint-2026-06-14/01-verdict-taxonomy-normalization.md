# 01 — Verdict Taxonomy Normalization

**Hardening Item:** #1 of 8
**Status:** SPEC (design phase)
**Author:** OPENCLAW
**Session:** hardening-sprint-2026-06-14
**Reversibility:** READ-ONLY design doc. No live system touched.
**Epoch:** 2026-06-14T12:45Z

---

## §0 — The Bug

### Current behavior (broken)

When an ops health tool like `arif_ops_measure(mode=health)` returns:

```json
{
  "service": "arifOS",
  "status": "healthy",
  "verdict": "pass"
}
```

Then the governance envelope processes `verdict: "pass"`:

1. **arifOS constitutional parser** does NOT recognize lowercase `pass`
2. The envelope marks the claim as `degraded` or `rejected`
3. But the service IS actually healthy
4. Result: **green service, yellow claim** — false degraded

### Root cause

**Machine health status and constitutional verdict are collapsed into one field.**

`verdict: "pass"` is a machine health check pass — it means "the HTTP endpoint returned 200." It does NOT mean "this claim is constitutionally sealed."

### Why it matters

The envelope chain goes:

```
Claim → arifOS judge → verdict → VAULT999 seal
```

If `verdict: pass` enters this chain:
- It cannot be audited (what does "pass" mean?)
- It cannot be sealed (no canonical verdict)
- It pollutes the vault with ambiguous entries
- It triggers false F2 TRUTH violations (the service IS healthy, but the claim says degraded)

---

## §1 — The Correction

### Design principle

```
machine_status ∈ {healthy, degraded, offline, quarantined, unknown}
constitutional_verdict ∈ {SEAL, HOLD, VOID, OBSERVE_ONLY, CAUTION, FORGE_READY}
claim_state ∈ {OBSERVED, DERIVED, INTERPRETED, SPECULATED, SEALED}
```

**These three are separate layers.** Never merge them.

### Correct shape

Every tool output from a governed organ MUST return:

```json
{
  "machine_status": "healthy",
  "constitutional_verdict": "OBSERVE_ONLY",
  "claim_state": "OBSERVED",
  "payload": { ... },
  "governance": {
    "floors_active": ["F01", "F02", "F05", "F07"],
    "risk_class": "C1_OBSERVE",
    "requires_human": false,
    "irreversible": false
  }
}
```

### Layer definitions

| Layer | Values | Meaning | Who sets it |
|-------|--------|---------|-------------|
| `machine_status` | healthy, degraded, offline, quarantined, unknown | Is the organ/service alive? | Organ itself |
| `constitutional_verdict` | SEAL, HOLD, VOID, OBSERVE_ONLY, CAUTION, FORGE_READY | Is this action constitutionally allowed? | arifOS judge |
| `claim_state` | OBSERVED, DERIVED, INTERPRETED, SPECULATED, SEALED | What is the epistemic status of the data? | Organ + arifOS |

### Constitutional verdict meanings

| Verdict | Meaning | Action allowed |
|---------|---------|---------------|
| `SEAL` | Constitutionally approved, irreversible | Write to VAULT999, commit, deploy |
| `HOLD` | Pending human review | Pause, escalate to Arif |
| `VOID` | Rejected or self-contradictory | Discard, do not proceed |
| `OBSERVE_ONLY` | Read-only observation | Read, list, describe |
| `CAUTION` | Proceed with warning | Limited scope, no mutation |
| `FORGE_READY` | Dry-run approved, mutation pending 888 | Dry-run only, no apply |

---

## §2 — Migration Map

### Legacy → Canonical

| Legacy `verdict` | → `machine_status` | → `constitutional_verdict` |
|-----------------|-------------------|---------------------------|
| `pass` | `healthy` | `OBSERVE_ONLY` |
| `fail` | `degraded` | `HOLD` |
| `error` | `offline` | `HOLD` |
| `SEAL` | `healthy` | `SEAL` (requires judge) |
| `HOLD` | `healthy` | `HOLD` |
| `VOID` | `degraded` | `VOID` |
| `green` | `healthy` | `OBSERVE_ONLY` |
| `yellow` | `degraded` | `CAUTION` |
| `red` | `offline` | `HOLD` |
| `ok` | `healthy` | `OBSERVE_ONLY` |
| `REGISTRY_PASS` | `healthy` | `OBSERVE_ONLY` |
| `REGISTRY_DRIFT` | `degraded` | `CAUTION` |

### Forward compatibility

New tools MUST use the canonical shape. Old tools get a compatibility wrapper:

```python
def normalize_verdict(tool_output):
    """Wrap legacy verdict into canonical three-layer shape."""
    legacy_verdict = tool_output.get("verdict", "unknown")
    mapping = LEGACY_TO_CANONICAL[legacy_verdict]
    return {
        "machine_status": mapping["machine_status"],
        "constitutional_verdict": mapping["constitutional_verdict"],
        "claim_state": "OBSERVED",
        "payload": tool_output,
    }
```

---

## §3 — Implementation Plan

### Phase A: Spec seal (NOW)
- [x] This document exists
- [ ] Arif reviews and seals
- [ ] Record in VAULT999 as CANONICAL-VERDICT-TAXONOMY-v1

### Phase B: arifOS kernel patch
1. Add `machine_status` field to all organ health responses
2. Add `constitutional_verdict` field to arifOS judge output
3. Add `claim_state` field to all tool responses
4. Add legacy→canonical wrapper for backward compatibility
5. Update `/health` to return canonical shape
6. Update `/api/arifos/readiness` to use canonical shape

### Phase C: Organ patches
1. GEOX: update all 37 tools to return canonical shape
2. WEALTH: update all 20 tools to return canonical shape
3. WELL: update all 18 tools to return canonical shape
4. A-FORGE: update health and bridge responses

### Phase D: Envelope hardening
1. arifOS `_enforce_nine_signal` rejects lowercase `pass`
2. Gateway `gateway_receipts` uses canonical verdicts
3. VAULT999 `arif_vault_seal` requires canonical SEAL verdict

### Phase E: Test
1. End-to-end: health check → machine_status: healthy + constitutional_verdict: OBSERVE_ONLY
2. End-to-end: mutation attempt → constitutional_verdict: FORGE_READY → 888_HOLD
3. End-to-end: after Arif approval → constitutional_verdict: SEAL → action

---

## §4 — What This Fixes

| Before | After |
|--------|-------|
| `verdict: pass` enters envelope, gets rejected | `machine_status: healthy` + `constitutional_verdict: OBSERVE_ONLY` — correctly classified |
| Health check pollutes vault with ambiguous entries | Health check is read-only observation, vault only gets sealed verdicts |
| No distinction between "service is alive" and "action is allowed" | Three distinct layers, each with clear semantics |
| False degraded claims on healthy services | Machine status and constitutional verdict independently verifiable |
| No standard verdict taxonomy across organs | All organs speak the same 6 canonical verdicts |

---

## §5 — Constitutional Binding

| Floor | Relevance |
|-------|-----------|
| F1 Amanah | SEAL verdict requires ack_irreversible=true |
| F2 Truth | Machine status must not lie about service health |
| F4 Clarity | Canonical verdicts are unambiguous |
| F7 Humility | OBSERVE_ONLY is the default, not SEAL |
| F9 Anti-Hantu | No ambiguous "pass" masquerading as constitutional |
| F11 Auth | Identity must be verified before SEAL |
| F13 Sovereign | HOLD and 888_HOLD preserve human veto |

---

## §A — Appendix: Full Canonical Verdict Taxonomy

```
SEAL
├── Requires: identity_verified=true, ack_irreversible=true, F1-F13 cleared
├── Allows: mutation, deployment, vault seal, external write
└── Blocked by: HOLD, VOID, unverified identity, F13 veto

HOLD
├── Requires: nothing (default when uncertain)
├── Allows: read, observe, dry-run
└── Triggered by: uncertainty, missing evidence, F13, 888_HOLD gate

VOID
├── Requires: self-contradiction, F9 violation, or sovereign rejection
├── Allows: nothing (terminal rejection)
└── Triggered by: contradiction, consciousness claim, dignity violation

OBSERVE_ONLY
├── Requires: nothing (default for all read operations)
├── Allows: read, list, describe, health check, status
└── Default for: all GET/health/status/registry operations

CAUTION
├── Requires: machine_status=healthy, some evidence
├── Allows: limited scope operations, reversible changes
└── Flagged: human review recommended but not required

FORGE_READY
├── Requires: dry-run passed, diff reviewed, machine_status=healthy
├── Allows: dry-run execution, preview
├── Blocked: cannot apply without → SEAL
└── Transition: FORGE_READY → 888_HOLD → (Arif approves) → SEAL
```

---

**Signed:** OPENCLAW · 2026-06-14T12:45Z
**Next:** Submit for Arif review. After seal → Phase B (arifOS kernel patch).
