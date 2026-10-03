# Validator + Fixture Test Plan

**Generated:** 2026-10-02
**Status:** CANDIDATE_ABI
**Purpose:** Outline validators + fixture tests required before IR_REGISTRY promotion to FROZEN.

---

## Goal

Every IR schema MUST pass:
1. JSON Schema syntax validation (draft 2020-12).
2. Cross-schema `$ref` resolution.
3. Hard-invariant guards (`allOf` if/then blocks).
4. Fixture conformance (golden examples pass; negative examples rejected).
5. Adversarial fixture (must-not-be-acceptable).

---

## Test harness structure

```
/root/AAA/schemas/ir/
  tests/
    conftest.py                       — pytest config, schema loader, resolver
    test_schema_syntax.py            — every schema parses + draft-2020-12 valid
    test_cross_schema_refs.py        — every $ref resolves
    test_hard_invariants.py          — every allOf if/then rejects violation
    test_bridge_proof_axes.py        — BridgeProof four-axis + 4 hard invariants
    test_authority_envelope_tuple.py — AuthorityEnvelope 12-field tuple
    test_release_link_gate.py        — region_match mandatory + Release = all checks pass
    test_capability_graph_7_layer.py — 7-layer + mutating exclusion
    fixtures/
      gold_identity_packet.json
      gold_capability_graph.json
      gold_authority_envelope.json
      gold_bridge_proof_equivalent.json
      gold_bridge_proof_type_mismatch.json
      gold_release_link.json
      gold_artifact_bundle.json
      gold_worldline.json
      adversarial_bridge_proof_equiv_no_evidence.json     # verification_state forced to UNRESOLVED by invariant
      adversarial_bridge_proof_type_mismatch_diverge.json    # relation forbidden
      adversarial_bridge_proof_probe_error_refuted.json   # verification_state forbidden
      adversarial_release_link_app_no_region.json         # region_match mandatory for app
      adversarial_capability_graph_mutating_in_callable.json # mutating tool in callable set
```

---

## Validator 1 — Schema syntax

```python
import json
import pytest
import pathlib
from jsonschema import Draft202012Validator

SCHEMA_DIR = pathlib.Path(__file__).parent.parent

@pytest.mark.parametrize("schema_file", SCHEMA_DIR.glob("*.schema.json"))
def test_schema_parses(schema_file):
    schema = json.loads(schema_file.read_text())
    Draft202012Validator.check_schema(schema)  # raises if invalid
```

**Pass:** every schema passes. (Today: 15/15 pass after C.2 reconciliation.)

---

## Validator 2 — Cross-schema $ref resolution

```python
def test_runtime_packet_refs_resolve():
    schema = json.loads((SCHEMA_DIR / "runtime-packet.v1.schema.json").read_text())
    # Walk every $ref and confirm file exists
    refs = collect_refs(schema)
    for ref in refs:
        assert (SCHEMA_DIR / Path(ref).name).exists(), f"ref {ref} unresolved"
```

**Pass:** every $ref resolves to a co-located schema file. (Today: 8/8 refs resolve.)

---

## Validator 3 — Hard invariants (BridgeProof)

```python
def test_bridge_proof_equivalent_requires_comparable_witnessed():
    packet = json.loads(open("fixtures/gold_bridge_proof_equivalent.json").read())
    validate(packet, bridge_proof_schema)
    # Now mutate to adversarial
    bad = copy.deepcopy(packet)
    bad["comparability"] = "TYPE_MISMATCH"  # forces invalid combo
    with pytest.raises(ValidationError):
        validate(bad, bridge_proof_schema)
```

**Tests 4 hard invariants:**
1. EQUIVALENT_TO requires COMPARABLE ∧ WITNESSED
2. ProbeFailure forces UNRESOLVED (forbids REFUTED)
3. Empty evidence_refs forces UNRESOLVED
4. TYPE_MISMATCH forbids DIVERGES_FROM

---

## Validator 4 — AuthorityEnvelope 12-field tuple

```python
def test_authority_envelope_required_fields():
    schema = json.loads(open("authority-envelope.v1.schema.json").read())
    required = set(schema["required"])
    expected = {"actor", "session", "host", "objective", "operation", "scope", "target",
                "issuer", "expiry", "expected_postcondition", "budget", "revocation_ref",
                "verdict", "decided_at"}
    assert required == expected, f"AuthorityEnvelope must carry 12-tuple + 3 (verdict/decided_at/...). Missing: {expected - required}; Extra: {required - expected}"
```

**Pass:** required set equals 12-tuple + verdict/decided_at (14 total).

---

## Validator 5 — ReleaseLinkGate region_match mandatory

```python
def test_release_link_app_requires_region():
    schema = json.loads(open("release-link-gate.v1.schema.json").read())
    # Adversarial: app with region_match=null
    bad = json.loads(open("fixtures/adversarial_release_link_app_no_region.json").read())
    with pytest.raises(ValidationError):
        validate(bad, schema)
```

---

## Validator 6 — CapabilityGraph mutating exclusion

```python
def test_capability_graph_mutating_excluded_from_callable():
    schema = json.loads(open("capability-graph.v1.schema.json").read())
    bad = json.loads(open("fixtures/adversarial_capability_graph_mutating_in_callable.json").read())
    # The fixture has a mutating tool listed in both mutating_tools and observed_callable
    with pytest.raises(ValidationError):
        validate(bad, schema)
```

---

## Validator 7 — Epistemic taxonomy purity

```python
EXPECTED_EPISTEMIC_ENUM = {"OBS", "DER", "INT", "SPEC", "SEAL"}

@pytest.mark.parametrize("schema_file", SCHEMA_DIR.glob("*.schema.json"))
def test_no_parallel_epistemic_enums(schema_file):
    schema_text = schema_file.read_text()
    # Naive scan for any enum containing epistemic-class-shaped names
    suspicious = {"GENERATED", "DERIVED", "REPORTED", "OBSERVED", "INTROSPECTED",
                  "SPECULATIVE", "NORMATIVE", "CONTESTED", "UNKNOWN"}
    for token in suspicious:
        # Match as enum value
        assert f'"{token}"' not in schema_text, f"{schema_file.name}: forbidden epistemic token {token!r}"
```

**Pass:** no schema contains forbidden epistemic-class-shaped enum values.

---

## Fixture examples

### Gold fixture: BridgeProof EQUIVALENT_TO with full evidence

```json
{
  "bridge_id": "11111111-1111-4111-8111-111111111111",
  "claim_a": {"value": "800eb164", "type": "git_sha"},
  "claim_b": {"value": "800eb164", "type": "git_sha"},
  "relation": "EQUIVALENT_TO",
  "comparability": "COMPARABLE",
  "verification_state": "WITNESSED",
  "probe_state": "SUCCESS",
  "witness_method": {"kind": "lineage", "tool": "git_log"},
  "witness_evidence_refs": ["refs/git/log/abc123"],
  "decided_at": "2026-10-02T10:00:00Z",
  "decided_by": "bridge-compiler-session-2026-10-02"
}
```

### Gold fixture: BridgeProof TYPE_MISMATCH (NOT divergence)

```json
{
  "bridge_id": "22222222-2222-4222-8222-222222222222",
  "claim_a": {"value": "800eb164", "type": "git_sha"},
  "claim_b": {"value": "1!2026.9.6", "type": "pep440"},
  "relation": "DERIVED_FROM",
  "comparability": "TYPE_MISMATCH",
  "verification_state": "UNRESOLVED",
  "probe_state": "NOT_RUN",
  "witness_method": {"kind": "unknown"},
  "type_mismatch_resolution": {
    "bridge_name": "pep440_to_git_sha_via_BUILDINFO",
    "bridge_artifact_ref": "BUILDINFO.json",
    "comparable_after_resolution": true
  },
  "witness_evidence_refs": ["BUILDINFO.json"],
  "decided_at": "2026-10-02T10:01:00Z",
  "decided_by": "bridge-compiler-session-2026-10-02"
}
```

### Adversarial fixture: EQUIVALENT_TO with empty evidence

```json
{
  "bridge_id": "33333333-3333-4333-8333-333333333333",
  "claim_a": {"value": "800eb164", "type": "git_sha"},
  "claim_b": {"value": "800eb164", "type": "git_sha"},
  "relation": "EQUIVALENT_TO",
  "comparability": "COMPARABLE",
  "verification_state": "WITNESSED",
  "probe_state": "SUCCESS",
  "witness_method": {"kind": "lineage"},
  "witness_evidence_refs": [],
  "decided_at": "2026-10-02T10:02:00Z",
  "decided_by": "adversarial-fixture"
}
```

This must FAIL validation because invariant 3 (empty evidence → UNRESOLVED) fires.

---

## CI integration

```yaml
# .github/workflows/ir-validate.yml
on:
  paths:
    - 'schemas/ir/**'
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install jsonschema pytest
      - run: pytest schemas/ir/tests/ -v
```

---

## Status

**Plan complete.** Fixtures need to be authored (next session). Once authored + CI green + FROZEN promotion criteria met, IR layer is ready for FROZEN status.

**Owner:** session-2026-10-02-1038 (reconciliation) + future session (fixture authoring).