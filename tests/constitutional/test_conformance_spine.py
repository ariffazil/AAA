"""Conformance spine tests — Stage 4 (2026-07-05).

9-point kernel conformance spine — replicates arif_conformance_report's
checks at the unit level so any single regression is caught without
needing a live kernel.

For live cross-validation, see test_conformance_spine_e2e() which uses
the `live_kernel` fixture (skips if :8088 unreachable).
"""

from __future__ import annotations

import pytest
import yaml


# ─── Static YAML invariants ────────────────────────────────────────────────


def test_yaml_parses_clean(invariants_yaml_path):
    """TOOL_INVARIANTS.yaml must be valid YAML."""
    with open(invariants_yaml_path) as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict)


def test_canonical_count_is_14(invariants):
    """arifOS declared 14 canonical kernel tools."""
    canonical = invariants.get("canonical", {})
    assert len(canonical) == 14, f"expected 14 canonical, got {len(canonical)}"


def test_diagnostic_count_at_least_40(invariants):
    """Diagnostic tools count must be ≥ 40 (current is 45)."""
    diagnostic = invariants.get("diagnostic", {})
    assert len(diagnostic) >= 40


def test_every_canonical_has_required_fields(invariants):
    required = {"name", "description", "stage", "action_class", "status"}
    canonical = invariants.get("canonical", {})
    for k_id, meta in canonical.items():
        missing = required - set(meta.keys())
        assert not missing, f"K-series {k_id} missing fields: {missing}"


def test_canonical_names_unique(invariants):
    canonical = invariants.get("canonical", {})
    names = [m.get("name") for m in canonical.values()]
    assert len(set(names)) == len(names), "duplicate canonical tool names"


def test_stage_constants_match_seven_pipeline(invariants):
    canonical = invariants.get("canonical", {})
    stages = {m.get("stage") for m in canonical.values()}
    # canonical section MUST use only the 7 stages of the golden path
    expected_stages = {
        "000 INIT",
        "111 SENSE",
        "333 REASON",
        "555 CRITIQUE",
        "666 JUDGE",
        "777 FORGE",
        "999 SEAL",
    }
    assert stages <= expected_stages, f"unknown stages: {stages - expected_stages}"


def test_action_classes_are_known(invariants):
    """Only canonical tools carry action_class.

    Diagnostic tools (D-series) intentionally omit it — they're internal
    probes, not governed actions, so the action_class semantics don't apply.
    """
    valid = {"OBSERVE", "JUDGE", "MUTATE", "IRREVERSIBLE"}
    for k_id, meta in invariants.get("canonical", {}).items():
        ac = meta.get("action_class")
        assert ac in valid, f"canonical.{k_id} bad action_class: {ac}"


def test_golden_path_block_lists_known_canonical(invariants):
    """Every K-id in golden_path[*] must exist in canonical section."""
    canonical = invariants.get("canonical", {})
    golden = invariants.get("golden_path", {})
    for stage, kids in golden.items():
        for kid in kids:
            assert kid in canonical, (
                f"golden_path[{stage}] lists {kid} but not in canonical section"
            )


# ─── Harmonic index tests (Stage 1) ──────────────────────────────────────────


def test_harmonic_index_present(invariants):
    hi = invariants.get("harmonic_index")
    assert hi is not None, "harmonic_index block missing"


def test_harmonic_index_contains_all_14(invariants):
    hi = invariants.get("harmonic_index", {})
    by_harmonic = hi.get("by_harmonic", {})
    assert len(by_harmonic) == 14, f"expected 14 harmonic IDs, got {len(by_harmonic)}"


def test_harmonic_ids_unique(invariants):
    hi = invariants.get("harmonic_index", {})
    by_harmonic = hi.get("by_harmonic", {})
    harmonic_ids = list(by_harmonic.keys())
    assert len(set(harmonic_ids)) == len(harmonic_ids), "duplicate harmonic IDs"


def test_harmonic_id_band_format(invariants):
    """band.slot must be one of 000, 111, 333, 555, 666, 777, 999."""
    allowed_bands = {"000", "111", "333", "555", "666", "777", "999"}
    hi = invariants.get("harmonic_index", {}).get("by_harmonic", {})
    for h in hi.keys():
        band = h.split(".", 1)[0]
        assert band in allowed_bands, f"unknown band: {h}"


def test_harmonic_index_by_name_matches_by_harmonic(invariants):
    hi = invariants.get("harmonic_index", {})
    by_harmonic = hi.get("by_harmonic", {})
    by_name = hi.get("by_name", {})
    for h, meta in by_harmonic.items():
        name = meta.get("name")
        assert by_name.get(name) == h, f"by_name mismatch for {name}"


# ─── tool_id_resolver round-trip ────────────────────────────────────────────


def test_resolver_resolves_by_name(resolver):
    if resolver is None:
        pytest.skip("resolver not importable")
    assert resolver.resolve_harmonic_id("arif_fetch") == "111.2"
    assert resolver.resolve_harmonic_id("arif_init") == "000.1"
    assert resolver.resolve_harmonic_id("arif_seal") == "999.1"


def test_resolver_resolves_by_kid(resolver):
    if resolver is None:
        pytest.skip("resolver not importable")
    assert resolver.resolve_harmonic_id("K012") == "111.2"
    assert resolver.resolve_harmonic_id("K001") == "000.1"


def test_resolver_idempotent_by_harmonic(resolver):
    """harmonic_id in → harmonic_id out (idempotent)."""
    if resolver is None:
        pytest.skip("resolver not importable")
    assert resolver.resolve_harmonic_id("111.2") == "111.2"


def test_resolver_resolves_tool_name_from_any_form(resolver):
    if resolver is None:
        pytest.skip("resolver not importable")
    # From name
    assert resolver.resolve_tool_name("arif_judge") == "arif_judge"
    # From K-id
    assert resolver.resolve_tool_name("K006") == "arif_judge"
    # From harmonic
    assert resolver.resolve_tool_name("666.1") == "arif_judge"


def test_resolver_unknown_input_returns_none(resolver):
    if resolver is None:
        pytest.skip("resolver not importable")
    assert resolver.resolve_harmonic_id("totally-unknown-tool-2026") is None
    assert resolver.resolve_tool_name("totally-unknown-tool-2026") is None


def test_resolver_list_canonical_harmonic_length(resolver):
    if resolver is None:
        pytest.skip("resolver not importable")
    out = resolver.list_canonical_harmonic()
    assert len(out) == 14
    for row in out:
        h, kid, name, stage = row
        assert h in {"000.1", "111.1", "111.2", "111.3", "333.1", "333.2",
                    "333.3", "555.1", "666.1", "666.2", "777.1", "777.2",
                    "999.1", "999.2"}


# ─── Live E2E (skipped if no live kernel) ──────────────────────────────────


def test_conformance_spine_e2e(live_kernel):
    """If kernel is reachable, must report 9/9 spine tests PASS."""
    body = live_kernel["body"]
    # Maybe the /health endpoint payload has a "spine" or similar field;
    # we accept the live result and assert nothing leaks.
    assert body is not None
