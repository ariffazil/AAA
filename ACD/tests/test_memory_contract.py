"""ACD memory contract tests — the acceptance criterion:
One shadow cycle where (a) the object stays SIMULATED-typed,
(b) it is retrievable only in an explicit scenario context,
(c) self-promotion fails closed. Constitution Articles 10-13."""

import sys
import uuid
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.acd_core import ACDCore, VERSION  # noqa: E402
from core import acd_memory as mem  # noqa: E402


def make_req() -> dict:
    return {
        "request_id": str(uuid.uuid4()),
        "cycle_id": str(uuid.uuid4()),
        "requested_by": "pytest",
        "requesting_agent": "pytest",
        "command": "dream",
        "mode": "shadow",
        "shadow": True,
        "purpose": "memory contract acceptance",
        "scope": "bounded",
        "horizon": "short",
        "evidence_refs": ["doc:fixture"],
        "constraints": ["shadow_mode"],
        "compute_budget": 5,
        "created_at": "2026-09-12T00:00:00+00:00",
        "contract_version": VERSION,
    }


def test_zones_defined():
    assert set(mem.ZONES) == {"evidence_context", "possibility_quarantine", "ratified_learning"}
    assert mem.ZONES["possibility_quarantine"]["acd_write"] == "request-only"
    assert mem.ZONES["ratified_learning"]["acd_write"] == "never-direct"


def test_simulated_excluded_from_default_recall():
    materials = [{"ontology": "OBSERVED", "id": "o1"}, {"ontology": "SIMULATED", "id": "s1"}]
    got = mem.recall_filter(materials)
    assert [m["id"] for m in got] == ["o1"]


def test_simulated_visible_only_in_scenario_scope():
    materials = [{"ontology": "SIMULATED", "id": "s1"}]
    assert mem.recall_filter(materials, scope="scenario")[0]["id"] == "s1"
    assert mem.recall_filter(materials, scope="acd")[0]["id"] == "s1"
    assert mem.recall_filter(materials, scope="ordinary_factual_recall") == []


def test_forbidden_transition_raises():
    with pytest.raises(mem.ForbiddenTransition):
        mem.assert_transition_allowed("SIMULATED", "OBSERVED")
    with pytest.raises(mem.ForbiddenTransition):
        mem.assert_transition_allowed("SIMULATED", "RATIFIED")
    assert mem.assert_transition_allowed("OBSERVED", "INFERRED") is True


def test_shadow_cycle_object_is_quarantine_typed(tmp_path):
    core = ACDCore(receipts_dir=tmp_path)
    rec = core.dream(make_req())
    assert rec["ontology"] == "SIMULATED"
    assert rec["memory_zone"] == "AAA.POSSIBILITY"
    assert rec["memory_class"] == "ACD_DREAM_RECEIPT"
    assert rec["recall_visibility"] == "SCENARIO_ONLY"
    assert rec["promotion_status"] == "NONE"


def test_self_promotion_fails_closed(tmp_path):
    core = ACDCore(receipts_dir=tmp_path)
    rec = core.dream(make_req())
    with pytest.raises(PermissionError):
        core.attempt_self_promotion()
    with pytest.raises(mem.ForbiddenTransition):
        mem.attempt_self_promotion()
    # Promotion status must remain untouched — no silent upgrade
    assert rec["promotion_status"] == "NONE"
    assert "authorized_by" not in rec
