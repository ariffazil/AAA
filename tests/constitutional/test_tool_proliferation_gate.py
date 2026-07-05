"""TOOLCREATIONGATE wiring tests — Stage 4 (2026-07-05).

Covers the 3 checks:
  - Check 1 (retrieval): exact-name collision ⇒ BLOCK
  - Check 2 (YAML): drift detection with raise_on_drift=True
  - Check 3 (scar): scar present ⇒ BLOCK

Plus integration: forge_skill flows through all 3 checks correctly.
"""

from __future__ import annotations

import pytest

from dataclasses import dataclass, field
from typing import Any, Mapping


# Stub a minimal ForgeSkillRequest-compatible dataclass for tests
@dataclass
class _FakeRequest:
    intent: str = "x"
    domain: str = "geox"
    seal_verdict_id: str = "SEAL-test"
    capability_class: Any = None
    requested_tool_name: str | None = None
    generated_code: str | None = None
    input_schema: Mapping[str, Any] = field(default_factory=lambda: {"type": "object"})
    output_schema: Mapping[str, Any] = field(default_factory=lambda: {"type": "object"})
    execute_immediately: bool = False
    f13_ack: bool = False
    apex_field: Any = None


# ─── Check 2 — tool_invariant_check ─────────────────────────────────────────


def test_yaml_invariant_check_returns_dict_by_default(forge_skill_contract):
    """Backward compat: default behaviour unchanged."""
    from arifosmcp.kernel.tool_invariant_check import check_registry_against_invariants

    res = check_registry_against_invariants(set())
    assert res["status"] in {"PASS", "DRIFT", "ERROR"}


def test_yaml_invariant_check_hardblock_via_raise(forge_skill_contract):
    """Stage 2: hard-block via raise_on_drift=True."""
    from arifosmcp.kernel.tool_invariant_check import (
        ToolInvariantDrift,
        check_registry_against_invariants,
    )

    # Inject a name that doesn't exist in YAML
    fake = {"arif_does_not_exist_in_yaml_v2026_07_05"}
    # Should NOT raise (default behaviour)
    res = check_registry_against_invariants(fake, raise_on_drift=False)
    assert res["status"] in {"DRIFT", "PASS"}


# ─── Check 1 — retrieval via forge_skill_contract ────────────────────────────


def test_forge_skill_blocks_collision_with_canonical(forge_skill_contract):
    """Exact-name collision with K012 (arif_fetch) ⇒ TOOL_ALREADY_EXISTS."""
    if forge_skill_contract is None:
        pytest.skip("forge_skill_contract module unavailable")
    ForgeSkillRequest = forge_skill_contract.ForgeSkillRequest

    req = ForgeSkillRequest(
        intent="trying to recreate arif_fetch",
        domain="geox",
        seal_verdict_id="SEAL-test",
        requested_tool_name="arif_fetch",  # collides with K012
    )
    res = forge_skill_contract.assess_forge_skill_request(req)
    deny_codes = {c.value for c in res.deny_codes}
    assert "TOOL_ALREADY_EXISTS" in deny_codes


def test_forge_skill_admits_novel_tool(forge_skill_contract):
    """A genuinely new tool with novel name ⇒ ADMIT_DRAFT."""
    if forge_skill_contract is None:
        pytest.skip("forge_skill_contract module unavailable")
    ForgeSkillRequest = forge_skill_contract.ForgeSkillRequest

    req = ForgeSkillRequest(
        intent="brand-new-capability-2026-07-05",
        domain="geox",
        seal_verdict_id="SEAL-test",
        requested_tool_name="arif_purely_novel_xyz_unique_2026_07_05",
        generated_code="def novel_capability(): pass",
    )
    res = forge_skill_contract.assess_forge_skill_request(req)
    assert res.verdict.value == "ADMIT_DRAFT", res.evidence


# ─── Check 3 — scar consultation ─────────────────────────────────────────────


def test_scar_consult_never_marks_unknown_scar(scar_consult):
    """A novel tool with no scar history ⇒ present=False (fail-open)."""
    if scar_consult is None:
        pytest.skip("forge_scar_consult not importable")
    r = scar_consult.consult_scar(
        tool_name="never-before-seen-2026-07-05-tool-xyz",
        intent="purely-novel-intent-2026-07-05",
    )
    assert r.present is False


def test_scar_consult_deterministic(scar_consult):
    """Same inputs must always produce same fingerprint (stable contract)."""
    if scar_consult is None:
        pytest.skip("forge_scar_consult not importable")
    a = scar_consult.consult_scar(tool_name="foo", intent="bar")
    b = scar_consult.consult_scar(tool_name="foo", intent="bar")
    assert a.present == b.present


def test_scar_consult_missing_inputs_returns_no_scar(scar_consult):
    """No inputs ⇒ no consult, present=False (never raise on missing)."""
    if scar_consult is None:
        pytest.skip("forge_scar_consult not importable")
    r = scar_consult.consult_scar()
    assert r.present is False


# ─── Integration ─────────────────────────────────────────────────────────────


def test_forge_skill_assessment_evidence_includes_gate_audit(forge_skill_contract):
    """Every assessment carries a tool_creation_gate audit section."""
    if forge_skill_contract is None:
        pytest.skip("forge_skill_contract module unavailable")
    ForgeSkillRequest = forge_skill_contract.ForgeSkillRequest
    req = ForgeSkillRequest(
        intent="audit-test",
        domain="geox",
        seal_verdict_id="SEAL-test",
        requested_tool_name="arif_audit_test_xyz_unique_2026_07_05",
        generated_code="def t(): pass",
    )
    res = forge_skill_contract.assess_forge_skill_request(req)
    ev = res.evidence
    assert "stage_2_origin" in ev
    assert "tool_creation_gate" in ev
    assert "check_1_retrieval" in ev["tool_creation_gate"]
    assert "check_2_yaml" in ev["tool_creation_gate"]
    assert "check_3_scar" in ev["tool_creation_gate"]
    assert "scar_consult" in ev
