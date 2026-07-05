# Constitutional Test Suite

**Forged:** 2026-07-05 by Kimi Code (FI-008) under F13 SOVEREIGN directive.
**Stage:** 4 (constitutional repair — test infrastructure).
**Location:** `/root/AAA/tests/constitutional/`
**Runner:** `python /root/AAA/tests/constitutional/constitutional_runner.py`

## Quick start

```bash
# Show what's in the suite
python /root/AAA/tests/constitutional/constitutional_runner.py list

# Dry-run (collect-only)
python /root/AAA/tests/constitutional/constitutional_runner.py dry-run

# Run everything
python /root/AAA/tests/constitutional/constitutional_runner.py all

# Run one stage
python /root/AAA/tests/constitutional/constitutional_runner.py stage 3
```

Or use pytest directly:
```bash
python -m pytest /root/AAA/tests/constitutional/ -v
python -m pytest /root/AAA/tests/constitutional/test_identity_binding.py -v
```

## Stage map

| Stage | File | Covers |
|---|---|---|
| 0.2 | `test_drift_detection.py` | VAULT999 chain integrity, identity anchor materialization, hash drift detection |
| 1 | `test_conformance_spine.py` | 9-point kernel conformance spine + harmonic ID resolution + invarian counts |
| 2 | `test_tool_proliferation_gate.py` | TOOLCREATIONGATE 3-check enforcement (retrieval / YAML / scar) |
| 3 | `test_identity_binding.py` + `test_bridging_seal_overrides.py` | actor_verified, BRIDGING_SEAL constraints, JWT/DPoP stub raise behaviour |
| e2e | `test_conformance_spine.py::test_conformance_spine_e2e` + `test_well_freshness.py` | Live kernel/health probes (skip if not reachable) |

## Test count (approximate)

| File | Tests |
|---|---|
| test_identity_binding.py | ~14 |
| test_tool_proliferation_gate.py | ~8 |
| test_conformance_spine.py | ~16 |
| test_well_freshness.py | ~4 |
| test_drift_detection.py | ~7 |
| test_bridging_seal_overrides.py | ~3 |
| **Total** | **~52** |

## Conventions

- All tests skip cleanly if a dependency is missing (e.g., live kernel :8088 down).
- Tests do NOT mutate state by default.
- Tests that need mutation require `ARIFOS_SOVEREIGN_MODE=1` env var.
- Stage 3 (identity) tests verify stubs RAISE — that IS the contract.

## Adding new tests

When Stage 5 lands (whatever that is), add tests here. Use pytest style:

```python
def test_<stage>_<invariant>_<scenario>(<fixtures>):
    """Docstring says which F-numbered floor this enforces."""
    ...

@pytest.fixture
def new_fixture():
    ...
```

## Cross-references

- AGENTS.md §"Autonomy Tiers" — T1 read-only tests run without sovereign ack.
- KEY_ROTATION_POLICY.md — keys never enter test contexts.
- /root/forge_work/2026-07-05/constitutional-repair/receipts/FINAL_RECEIPT.md — full receipt.

## Author / license

Forged by Kimi Code (FI-008) under F13 SOVEREIGN directive "i approve. at the end muat delete the chaos" (2026-07-05).

DITEMPA BUKAN DIBERI — tested, not assumed.
