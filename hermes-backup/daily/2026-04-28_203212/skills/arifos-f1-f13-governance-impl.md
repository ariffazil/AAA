# arifOS F1–F13 Data Governance Implementation

## Context
arifOS F1–F13 floors have two enforcement layers:

1. **`FloorEvaluator.evaluate()`** (`arifosmcp/core/floor_evaluator.py`) — called per-tool-invocation, deep analysis with `ThreatAssessment`
2. **`DataGovernanceEnforcer.ingest_asset()`** (`arifosmcp/runtime/data_governance.py`) — called per-data-asset-ingestion, comprehensive F1–F13 pipeline

Both layers must pass for a full governance verdict.

## FloorEvaluator Wire-Up Pattern

To add a new floor class to `FloorEvaluator.evaluate()`:

```python
def _floor_context(self, ctx: ActionContext, threat: ThreatAssessment) -> dict[str, Any]:
    """Pre-compute shared context used by all floor evaluations."""
    # Always compute all values, even if unused
    irreversibility = threat.irreversibility.value  # 0.0–1.0
    confidence = threat.confidence  # 0.0–1.0

    # Derive security_risk from actual ThreatCategory values
    security_risk = 1.0 if threat.threats & {
        ThreatCategory.FEDERATION_IMPERSONATION,
        ThreatCategory.SESSION_IMPERSONATION,
    } else 0.0

    return {
        "irreversibility": irreversibility,
        "confidence": confidence,
        "security_risk": security_risk,
        # Add floor-specific computed values here
    }

def evaluate(self, ctx: ActionContext, threat: ThreatAssessment) -> ConstitutionalVerdict:
    results: dict[str, FloorResult] = {}
    ctx_dict = self._floor_context(ctx, threat)

    # Wire new floors here (was bypassed by `floor_level <= 4` gate)
    # Call each floor's enforcement method
    results["F02"] = self._f02_truth(ctx, threat, ctx_dict)
    results["F03"] = self._f03_witness(ctx, threat, ctx_dict)
    # ...
```

## DataGovernanceEnforcer Pipeline Order

The `ingest_asset()` method evaluates floors in this fixed order:

1. **F12 INJECTION** — terminal gate, returns VOID immediately if triggered
2. **F1 AMANAH** — custodian check
3. **F2 TRUTH** — source verification
4. **F3 WITNESS** — multi-source bundle
5. **F4 CLARITY** — schema contract
6. **F5 PEACE** — field masking
7. **F6 EMPATHY** — downstream consumers
8. **F7 HUMILITY** — confidence envelope
9. **F8 GENIUS** — schema edge cases
10. **F10 ONTOLOGY** — taxonomy
11. **F11 AUTH** — role-based access
12. **F13 SOVEREIGN** — human veto record

**Critical**: F12 short-circuits before F01/F10/F11 are evaluated. Test assertions must account for this.

## Verdict Derivation

```python
if "F12" in failed_floors or "F01" in failed_floors or "F10" in failed_floors or "F11" in failed_floors:
    verdict = GovernanceVerdict.VOID      # Terminal floors — never proceed
elif failed_floors:
    verdict = GovernanceVerdict.HOLD       # Non-terminal failures — require human review
else:
    verdict = GovernanceVerdict.SEAL      # All floors pass
```

## Test Design Principles

### 1. Always provide full context to isolate the floor under test
```python
# To test F03 (WITNESS), avoid F02 (TRUTH) failures by providing verified source
verified = SourceVerificationRecord(
    source_name="trusted",
    verification_method="cryptographic",
    trust_score=0.95,
)
bundle = WitnessBundle(sources=[...], witness_count=2, consensus_score=0.89)
decision = enforcer.ingest_asset(..., source_verification=verified, witness_bundle=bundle)
```

### 2. F13 (SOVEREIGN) — high_impact without floor failures → pending
If `high_impact=True` but no other floor fails, `veto_record.status == "pending"`:
```python
# Must pass F01–F12 to reach pending status
verified = SourceVerificationRecord(...)
bundle = WitnessBundle(witness_count=2, consensus_score=0.89, ...)
decision = enforcer.ingest_asset(..., source_verification=verified, witness_bundle=bundle, high_impact=True)
assert decision.veto_record.status == "pending"  # not "vetoed"
```

### 3. F12 (INJECTION) short-circuit — assert VOID + failed_floors only
```python
# F12 fires first and returns VOID immediately
decision = enforcer.ingest_asset(asset_data={"query": "'; DROP TABLE..."})
assert decision.verdict == GovernanceVerdict.VOID
assert "F12" in decision.failed_floors
# F01/F10/F11 NOT in failed_floors — not evaluated in same pass
```

### 4. Audit log is written before returning early-void
The F12 gate calls `_write_audit()` with all required fields before `return decision`:
```python
self._write_audit(
    decision_id=decision_id,
    action="ingest",
    asset_id=asset_id,
    actor_id=actor_id,
    session_id=session_id,
    fields_affected=list(asset_data.keys()),
    verdict=GovernanceVerdict.VOID,
    reason="F12 INJECTION: blocked at sanitization gate",
)
return decision
```

## Confidence Envelope (F7)

```python
def compute_confidence_envelope(source_scores: list[float]) -> ConfidenceEnvelope:
    if not source_scores:
        score = 0.0
        omega_0 = 0.04
    else:
        import math
        score = math.prod(source_scores) ** (1.0 / len(source_scores))
        omega_0 = 1.0 - score
        omega_0 = max(0.03, min(0.05, omega_0))  # Clamp to F7 band
    return ConfidenceEnvelope(score=score, band=(0.03, 0.05), sources=source_scores, omega_0=omega_0)
```

## Taxonomy Categories (F10)

```python
ARIFOS_TAXONOMY_CATEGORIES: set[str] = {
    "telemetry", "verdict", "session", "vault_record", "tool_manifest",
    "governance_decision", "constitutional_floor", "threat_assessment",
    "audit_log", "geox_data", "wealth_data", "configuration", "unknown",
}
```

## Key Files

| File | Role |
|-------|------|
| `arifosmcp/core/floor_evaluator.py` | Per-tool invocation, deep threat analysis |
| `arifosmcp/runtime/data_governance.py` | Per-asset ingestion, full F1–F13 pipeline |
| `arifosmcp/runtime/tools.py:_runtime_selftest()` | `/ready` endpoint, includes `governance_check` |
| `tests/test_data_governance.py` | 36 tests covering all 13 floors |
