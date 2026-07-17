"""PR 2 — registry-owned action class / authority.

Callers cannot self-declare OBSERVE to bypass SCT on MUTATE tools.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from governance.tool_authority_registry import (
    ACTION_MUTATE,
    ACTION_OBSERVE,
    ACTION_UNKNOWN,
    AUTH_LIMITED,
    AUTH_OBSERVE,
    effective_gate_params,
    reload_registry,
    resolve_tool_authority,
    strip_caller_action_class,
)
from governance.federation_sct import gate_tool_ingress


@pytest.fixture(autouse=True)
def _reload():
    reload_registry()
    yield
    reload_registry()


class TestResolveFromToolsYaml:
    def test_read_tool_is_observe(self):
        a = resolve_tool_authority("forge_status")
        assert a.action_class == ACTION_OBSERVE
        assert a.require_sct is False
        assert a.required_authority == AUTH_OBSERVE
        assert a.known is True
        assert a.source == "tools.yaml"

    def test_execute_tool_requires_sct(self):
        a = resolve_tool_authority("forge_execute")
        assert a.action_class == ACTION_MUTATE
        assert a.require_sct is True
        assert a.required_authority == AUTH_LIMITED
        assert a.known is True

    def test_dash_underscore_aliases(self):
        a1 = resolve_tool_authority("arifos-init")
        a2 = resolve_tool_authority("arifos_init")
        assert a1.action_class == ACTION_OBSERVE
        assert a2.action_class == ACTION_OBSERVE

    def test_geox_query_observe(self):
        a = resolve_tool_authority("geox-query")
        assert a.action_class == ACTION_OBSERVE
        assert a.require_sct is False


class TestOrganDefaults:
    def test_unknown_geox_tool_defaults_observe(self):
        a = resolve_tool_authority("geox_basin_synthesis_xyz", organ="geox")
        assert a.action_class == ACTION_OBSERVE
        assert a.require_sct is False
        assert a.known is False
        assert a.source == "organ_default"

    def test_unknown_forge_mutate_name_requires_sct(self):
        a = resolve_tool_authority("forge_deploy_nuclear", organ="a-forge")
        assert a.action_class == ACTION_MUTATE
        assert a.require_sct is True

    def test_strict_unknown_holds(self):
        a = resolve_tool_authority("totally_unknown_tool_xyz", organ="mystery", strict_unknown=True)
        assert a.action_class == ACTION_UNKNOWN
        assert a.require_sct is True


class TestCallerCannotWeaken:
    def test_strip_action_class(self):
        cleaned = strip_caller_action_class(
            {"action_class": "OBSERVE", "session_token": "sct_v1.x", "actor_id": "a"}
        )
        assert "action_class" not in cleaned
        assert cleaned["session_token"] == "sct_v1.x"
        assert cleaned["actor_id"] == "a"

    def test_caller_cannot_disable_sct_on_mutate(self):
        rec, require_sct, auth, rej = effective_gate_params(
            "forge_execute",
            organ="a-forge",
            caller_require_sct=False,  # caller tries to skip SCT
            caller_required_authority=AUTH_OBSERVE,
        )
        assert rej is None
        assert require_sct is True  # registry wins
        assert rec.action_class == ACTION_MUTATE

    def test_caller_can_tighten(self):
        rec, require_sct, auth, rej = effective_gate_params(
            "forge_status",
            organ="a-forge",
            caller_require_sct=True,  # tighter than registry
        )
        assert require_sct is True
        assert rec.action_class == ACTION_OBSERVE


class TestGateToolIngressRegistry:
    def test_mutate_without_sct_rejected(self):
        rej = gate_tool_ingress(
            "forge_execute",
            {"actor_id": "agent", "action_class": "OBSERVE"},  # lie
            organ="a-forge",
            require_sct=False,  # organ forgot to set require
        )
        assert rej is not None
        assert rej["error"] == "SCT_REQUIRED"
        assert rej["registry"]["action_class"] == ACTION_MUTATE

    def test_observe_without_sct_allowed(self):
        rej = gate_tool_ingress(
            "forge_status",
            {"actor_id": "agent"},
            organ="a-forge",
        )
        assert rej is None

    def test_geox_unknown_observe_without_sct_allowed(self):
        rej = gate_tool_ingress(
            "geox_some_read_tool",
            {},
            organ="geox",
        )
        assert rej is None

    def test_strict_unknown_holds(self):
        rej = gate_tool_ingress(
            "no_such_tool_ever",
            {},
            organ="mystery",
            strict_unknown=True,
        )
        assert rej is not None
        assert rej["error"] == "CAPABILITY_UNKNOWN"
