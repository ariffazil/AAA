"""test_state_reconciler.py — PR-2 FEDERATION-SOT regression tests.

Encodes the three known live contradictions as unit tests on synthetic
observations (NO network):

  (a) WEALTH split-brain — HERMES TCP probe sees internal transport UP while
      the external connector times out. Output must be per-dimension
      (internal UP + external DOWN both present); a single "WEALTH is down"
      verdict must be structurally impossible in the output shape.
  (b) GEOX advertised != accepted — the connector advertises tools its RT1
      runtime guard rejects. ADVERTISED_NOT_ACCEPTED with the tool names.
  (c) WELL tool-name error — `well_system_registry_status` gets "Unknown tool"
      while `well_registry_status` is the real tool. UNKNOWN_TOOL_NAME must
      distinguish "never declared" from "declared but broken".

Plus: same-dimension contradiction (two sources, conflicting states) and
stale detection via source_age_seconds.

Constitutional anchors:
  F2 TRUTH  — findings preserve sources and age, never average conflicts
  F9        — "no data" / "unmeasured" is never silently promoted to a verdict
  README    — ObservedState_A ?= ObservedState_B (reconciliation, not verification)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from state_reconciler import (  # noqa: E402
    K_ADVERTISED_NOT_ACCEPTED,
    K_CONTRADICTION,
    K_CONCLUSION,
    K_STALE,
    K_TOOL_SURFACE_UNMEASURED,
    K_UNKNOWN_TOOL_NAME,
    Observation,
    ReconciliationResult,
    STALE_THRESHOLD_SECONDS,
    reconcile,
)


def obs(**overrides) -> Observation:
    """Fresh, healthy observation with per-test overrides."""
    base = dict(
        component="TEST",
        dimension="http_reachability",
        state="REACHABLE",
        observed_at="2026-10-02T12:00:00Z",
        source="synthetic-probe",
        source_age_seconds=0.5,
        confidence=0.95,
        probe_method="GET (timeout 4s)",
        failure_reason=None,
        detail=None,
    )
    base.update(overrides)
    return Observation(**base)


def findings_of(result: ReconciliationResult, kind: str):
    return [f for f in result.entries if f.kind == kind]


def conclusions_of(result: ReconciliationResult) -> set:
    return result.conclusion_ids()


# ---------------------------------------------------------------------------
# (a) WEALTH split-brain — per-dimension conclusions, no single component verdict
# ---------------------------------------------------------------------------

def test_wealth_split_brain_is_per_dimension():
    observations = [
        obs(component="WEALTH", dimension="internal_transport", state="UP",
            source="hermes-tcp-probe",
            probe_method="HERMES TCP socket probe", confidence=0.9),
        obs(component="WEALTH", dimension="external_ingress", state="DOWN",
            source="http://127.0.0.1:18082/mcp",
            probe_method="GET (timeout 4s)", confidence=0.85,
            failure_reason="timeout after 4s"),
    ]
    result = reconcile(observations)

    ids = conclusions_of(result)
    assert "WEALTH_INTERNAL_TRANSPORT_UP" in ids
    assert "WEALTH_EXTERNAL_INGRESS_DOWN" in ids

    up = findings_of(result, K_CONCLUSION)
    dims = {(f.component, f.dimension, f.detail["state"]) for f in up}
    assert ("WEALTH", "internal_transport", "UP") in dims
    assert ("WEALTH", "external_ingress", "DOWN") in dims


def test_no_single_component_verdict_is_possible_in_output_shape():
    """Structural impossibility: every finding is (component, dimension)-scoped
    and every conclusion id embeds the dimension segment — so a component-level
    'WEALTH is down' verdict cannot be expressed by this output shape."""
    observations = [
        obs(component="WEALTH", dimension="internal_transport", state="UP",
            source="hermes-tcp-probe"),
        obs(component="WEALTH", dimension="external_ingress", state="DOWN",
            source="http://127.0.0.1:18082/mcp", failure_reason="timeout after 4s"),
    ]
    result = reconcile(observations)

    component_verdict = re.compile(r"^WEALTH_(UP|DOWN|DEGRADED|OUTAGE)$")
    for finding in result.entries:
        assert finding.dimension, "finding without a dimension = component-level verdict"
        assert finding.dimension not in {"overall", "component", ""}, (
            f"component-level dimension leaked: {finding.conclusion}")
        assert not component_verdict.match(finding.conclusion), (
            f"single component verdict leaked: {finding.conclusion}"
        )
        # conclusion id must carry the dimension slug
        dim_slug = re.sub(r"[^A-Za-z0-9]+", "_", finding.dimension).strip("_").upper().split(":")[0]
        assert dim_slug in finding.conclusion, (
            f"conclusion '{finding.conclusion}' does not embed dimension '{finding.dimension}'"
        )


# ---------------------------------------------------------------------------
# (b) GEOX advertised != accepted (connector advertises, RT1 runtime guard rejects)
# ---------------------------------------------------------------------------

def test_geox_advertised_not_accepted_lists_tool_names():
    observations = [
        obs(component="GEOX", dimension="advertised_tools", state="DECLARED",
            source="connector-tools-list",
            detail={"tools": ["geox_basin", "geox_claim", "geox_prospect",
                              "geox_paleobiodb_query"]}),
        obs(component="GEOX", dimension="accepted_tools", state="ACCEPTED",
            source="rt1-runtime-guard",
            detail={"tools": ["geox_basin", "geox_claim", "geox_prospect"]}),
    ]
    result = reconcile(observations)

    mismatches = findings_of(result, K_ADVERTISED_NOT_ACCEPTED)
    assert len(mismatches) == 1
    mismatch = mismatches[0]
    assert mismatch.component == "GEOX"
    assert mismatch.detail["tools"] == ["geox_paleobiodb_query"]
    assert set(mismatch.sources) == {"connector-tools-list", "rt1-runtime-guard"}


def test_advertised_matches_accepted_emits_no_mismatch():
    observations = [
        obs(component="GEOX", dimension="advertised_tools", state="DECLARED",
            source="connector-tools-list", detail={"tools": ["geox_basin"]}),
        obs(component="GEOX", dimension="accepted_tools", state="ACCEPTED",
            source="rt1-runtime-guard", detail={"tools": ["geox_basin", "geox_claim"]}),
    ]
    result = reconcile(observations)
    assert findings_of(result, K_ADVERTISED_NOT_ACCEPTED) == []


def test_unmeasured_accepted_surface_blocks_mismatch_claim():
    """F9: connector reachable but runtime surface unmeasured -> no mismatch
    may be claimed."""
    observations = [
        obs(component="GEOX", dimension="advertised_tools", state="DECLARED",
            source="connector-tools-list", detail={"tools": ["geox_basin"]}),
        obs(component="GEOX", dimension="accepted_tools", state="UNREACHABLE",
            source="rt1-runtime-guard", failure_reason="runtime guard probe timed out"),
    ]
    result = reconcile(observations)
    assert findings_of(result, K_ADVERTISED_NOT_ACCEPTED) == []
    unmeasured = findings_of(result, K_TOOL_SURFACE_UNMEASURED)
    assert len(unmeasured) == 1


# ---------------------------------------------------------------------------
# (c) WELL unknown tool name — never declared vs declared-but-broken
# ---------------------------------------------------------------------------

def test_well_unknown_tool_never_declared():
    observations = [
        obs(component="WELL", dimension="advertised_tools", state="DECLARED",
            source="well-tools-list",
            detail={"tools": ["well_registry_status", "well_validate_vitality",
                              "well_machine_diagnose"]}),
        obs(component="WELL", dimension="tool_invocation", state="UNKNOWN_TOOL",
            source="mcp-call-attempt",
            detail={"tool": "well_system_registry_status",
                    "error": "Unknown tool"},
            failure_reason="Unknown tool: well_system_registry_status"),
    ]
    result = reconcile(observations)

    unknowns = findings_of(result, K_UNKNOWN_TOOL_NAME)
    assert len(unknowns) == 1
    finding = unknowns[0]
    assert finding.detail["classification"] == "NEVER_DECLARED"
    assert finding.detail["tool"] == "well_system_registry_status"
    # the real tool is visible in the declared sample so a human can self-correct
    assert "well_registry_status" in finding.detail["declared_tools_sample"]


def test_well_declared_but_broken_is_distinguished_from_never_declared():
    observations = [
        obs(component="WELL", dimension="advertised_tools", state="DECLARED",
            source="well-tools-list",
            detail={"tools": ["well_registry_status"]}),
        obs(component="WELL", dimension="tool_invocation", state="UNKNOWN_TOOL",
            source="mcp-call-attempt",
            detail={"tool": "well_registry_status", "error": "handler raised"},
            failure_reason="handler raised"),
    ]
    result = reconcile(observations)
    unknowns = findings_of(result, K_UNKNOWN_TOOL_NAME)
    assert len(unknowns) == 1
    assert unknowns[0].detail["classification"] == "DECLARED_BUT_BROKEN"


def test_unknown_tool_without_declaration_evidence_is_flagged_not_guessed():
    observations = [
        obs(component="WELL", dimension="tool_invocation", state="UNKNOWN_TOOL",
            source="mcp-call-attempt",
            detail={"tool": "well_registry_status", "error": "Unknown tool"},
            failure_reason="Unknown tool: well_registry_status"),
    ]
    result = reconcile(observations)
    unknowns = findings_of(result, K_UNKNOWN_TOOL_NAME)
    assert len(unknowns) == 1
    assert unknowns[0].detail["classification"] == "DECLARATION_UNMEASURED"


# ---------------------------------------------------------------------------
# (d) same-dimension contradiction — two sources, conflicting states
# ---------------------------------------------------------------------------

def test_same_dimension_conflicting_states_emit_contradiction_with_both_sources():
    observations = [
        obs(component="HERMES", dimension="http_reachability", state="REACHABLE",
            source="generate_runtime_state.py"),
        obs(component="HERMES", dimension="http_reachability", state="UNREACHABLE",
            source="frame-drift-report", failure_reason="connection refused"),
    ]
    result = reconcile(observations)

    contradictions = findings_of(result, K_CONTRADICTION)
    assert len(contradictions) == 1
    contradiction = contradictions[0]
    assert contradiction.component == "HERMES"
    assert contradiction.dimension == "http_reachability"
    assert set(contradiction.sources) == {
        "generate_runtime_state.py", "frame-drift-report"}
    assert sorted(contradiction.detail["conflicting_states"]) == [
        "REACHABLE", "UNREACHABLE"]
    # no merged per-state conclusion replaces the conflict
    assert not any(
        f.kind == K_CONCLUSION and f.component == "HERMES"
        and f.dimension == "http_reachability"
        for f in result.entries
    )


def test_agreeing_sources_do_not_emit_contradiction():
    observations = [
        obs(component="CHRON", dimension="http_reachability", state="REACHABLE",
            source="generate_runtime_state.py"),
        obs(component="CHRON", dimension="http_reachability", state="REACHABLE",
            source="frame-probe"),
    ]
    result = reconcile(observations)
    assert findings_of(result, K_CONTRADICTION) == []
    assert "CHRON_HTTP_REACHABILITY_REACHABLE" in conclusions_of(result)


# ---------------------------------------------------------------------------
# (e) stale detection
# ---------------------------------------------------------------------------

def test_stale_observation_emits_stale_finding():
    observations = [
        obs(component="WELL", dimension="http_reachability", state="REACHABLE",
            source="cached-probe", source_age_seconds=STALE_THRESHOLD_SECONDS + 3600),
        obs(component="WELL", dimension="tool_health", state="UP",
            source="fresh-probe", source_age_seconds=1.0),
    ]
    result = reconcile(observations)
    stales = findings_of(result, K_STALE)
    assert len(stales) == 1
    assert stales[0].detail["source_age_seconds"] > STALE_THRESHOLD_SECONDS
    assert stales[0].detail["threshold_seconds"] == STALE_THRESHOLD_SECONDS


# ---------------------------------------------------------------------------
# shape invariants + serialization round-trip
# ---------------------------------------------------------------------------

def test_reconciled_payload_is_json_serializable(tmp_path):
    observations = [
        obs(component="WEALTH", dimension="internal_transport", state="UP",
            source="hermes-tcp-probe"),
        obs(component="WEALTH", dimension="external_ingress", state="DOWN",
            source="http://127.0.0.1:18082/mcp", failure_reason="timeout after 4s"),
        obs(component="GEOX", dimension="advertised_tools", state="DECLARED",
            source="connector-tools-list", detail={"tools": ["geox_basin"]}),
        obs(component="GEOX", dimension="accepted_tools", state="ACCEPTED",
            source="rt1-runtime-guard", detail={"tools": []}),
    ]
    result = reconcile(observations)
    payload = result.to_dict(input_path="synthetic")

    import json
    text = json.dumps(payload)  # must not raise
    loaded = json.loads(text)
    assert loaded["summary"]["observations"] == 4
    kinds = {e["kind"] for e in loaded["entries"]}
    assert K_CONCLUSION in kinds
    assert K_ADVERTISED_NOT_ACCEPTED in kinds


def test_empty_input_yields_empty_result():
    result = reconcile([])
    assert result.entries == []
    assert result.summary["observations"] == 0
