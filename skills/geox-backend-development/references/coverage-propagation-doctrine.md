# Coverage Propagation Across GEOX Tools — Doctrine Component #36

Forged 2026-08-13 alongside the Bekok Deep-1 root cause analysis.

## Why coverage must travel with confidence

`Confidence` is the model's certainty about a value it has computed.
`Coverage` is whether the data was actually looked at.

A model can be confident and blind. `confidence=0.81` in an unsampled interval is
epistemic garbage — engineering-shaped noise. The Bekok Deep-1 blowout (4 Apr 2023)
is the canonical institutional example: sensing PASS on 3D seismic / historical well,
but recognition/interpretation/memory FAIL. The report said "well collide" — that
narrative compressed the actual cause (no shallow gas seismic coverage) into the
institutional lie.

Per Component #36 (`/root/GEOX/resources/ontology/pressure_states.yaml`), every
prediction MUST report `coverage_score` alongside `confidence`.

## The 5-tier coverage taxonomy

| Score | Label | Meaning | Default epistemic |
|-------|-------|---------|-------------------|
| 1.0 | OBSERVED | Direct measurement (RFT/MDT/DST/LOT/FIT) | OBS |
| 0.8 | CALIBRATED | Model fitted to nearby observations | DER |
| 0.4 | EXTRAPOLATED | Borrowed from adjacent interval | INT |
| 0.25 | ANALOG | Offset well / analog field (>5km) | INT |
| 0.0 | UNKNOWN | No observation AND no applicable analog | HYPOTHESIS |

## Fail-closed rules (binding)

- `coverage_score = 0.0` → `confidence_cap = 0.50` regardless of model output
  → `epistemic_label = HYPOTHESIS`
- `no_seismic AND coverage=0.0 AND target_interval` → `epistemic = UNKNOWN`
  (bright spot cannot exist without seismic)
- `platform_slot AND shallow_interval AND no_site_survey` → `coverage = 0.0` for shallow
- `confidence_reported AND coverage_NOT_reported` → F9 ANTIHANTU flag

## Where coverage fields go in a tool result

Every GEOX tool result that emits `confidence` must emit BOTH:

```python
{
    "confidence": 0.85,                    # existing
    "coverage_score": 0.80,                # NEW — observation density
    "epistemic_label": "CALIBRATED",       # NEW — OBS/DER/INT/HYPOTHESIS/UNKNOWN
    "evidence_refs": [..., "ontology/pressure_states.yaml"],  # NEW — cite engine
    # ... existing fields unchanged ...
}
```

Default for uncalibrated tools: `coverage_score=0.0`, `epistemic_label="HYPOTHESIS"`.

## Harden recipe (verified 2026-08-13)

### 1. Tool return dict — add new top-level keys

```python
# prospect_unified.py falsify mode
coverage_score = 0.0   # default: UNKNOWN
epistemic_label = "HYPOTHESIS"
return {
    "coverage_score": coverage_score,
    "epistemic_label": epistemic_label,
    "apex_score": {"G": gals_check, "C_dark": 0.50 if falsified else 0.15},
    "witness_chain": {...},
    # ... existing fields preserved ...
}
```

### 2. evidence_refs — append ontology citation

```python
# basin.py
evidence_refs=[f"basins/{normalized}/{f}" for f in evidence_loaded] +
    ["ontology/pressure_states.yaml"],
```

### 3. Claim candidates — add `coverage_model` per claim

```python
claim_candidates = [
    {
        "claim_id": "clm_xxx",
        "type": "structure",
        "claim": "...",
        "evidence_ref": lit_ref,
        "confidence": "HIGH",
        "coverage_model": "OBSERVED",  # OBSERVED/CALIBRATED/EXTRAPOLATED/ANALOG
    },
    ...
]
```

## Verification commands

```bash
# 1. Functional smoke test
cd /root/GEOX && .venv/bin/python3 -c "
import sys, asyncio; sys.path.insert(0, 'src')
from geox_mcp.tools.prospect_unified import geox_prospect
r = asyncio.run(geox_prospect('TEST', mode='falsify', evidence_refs=['r1']))
assert 'coverage_score' in r and 'epistemic_label' in r
assert all(k in r for k in ['apex_score','witness_chain','results','falsified','ac_risk'])
print('PASS')
"

# 2. Targeted unit tests
cd /root/GEOX && .venv/bin/python3 -m pytest \
  tests/test_prospect_falsify.py tests/test_prospect_falsify_mode.py \
  tests/test_prospect_stratum.py tests/test_tool_contracts.py \
  tests/test_basin_synthesis_pipeline.py -q --tb=short
# Expect: 58 passed (verified 2026-08-13)

# 3. Compile check after every patch
python3 -m py_compile src/geox_mcp/tools/basin.py src/geox_mcp/tools/prospect_unified.py
```

## Remaining hardening (after 2026-08-13 session)

DONE:
- `prospect_unified.py` — `coverage_score`, `epistemic_label` added
- `basin.py` — `evidence_refs` cites ontology; claim candidates carry `coverage_model`

PENDING:
- `geox_geological_cognition.py` (line 700+ — fault confidence)
- `vision.py` (overall_confidence output)
- `collision_zone.py` (`_meta.confidence_cap`)
- `dde_reason.py` (composite `confidence`)
- `geomechanics_unified.py` (`f7_humility.confidence_cap`)
- `seismic_onnx_adapter.py` (`confidence_by_segment`)

When hardening any of these, the same 3-step pattern applies: (1) add coverage_score
+ epistemic_label to return, (2) cite ontology in evidence_refs, (3) optionally
annotate internal claim candidates with coverage_model.

## Architectural-lie detection rule

> **Confidence without coverage provenance is narrative, not engineering.**

If a tool returns `confidence` but omits `coverage_score`, downstream consumers must
raise F9 ANTIHANTU before accepting the claim. This is not a soft warning — it is
a binding tie signature check at the 888 gate.
