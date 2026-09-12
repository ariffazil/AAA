"""ACD contract tests — schema conformance, integrity, ontology, shadow enforcement."""

import json
import sys
import uuid
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.acd_core import ACDCore, VERSION  # noqa: E402

SCHEMAS = ROOT / "schemas"


def load_schema(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text())


def make_req(cycle=None) -> dict:
    return {
        "request_id": str(uuid.uuid4()),
        "cycle_id": cycle or str(uuid.uuid4()),
        "requested_by": "pytest",
        "requesting_agent": "pytest",
        "command": "dream",
        "mode": "shadow",
        "shadow": True,
        "purpose": "schema conformance",
        "scope": "bounded",
        "horizon": "short",
        "evidence_refs": ["doc:fixture"],
        "constraints": ["shadow_mode"],
        "compute_budget": 5,
        "created_at": "2026-09-12T00:00:00+00:00",
        "contract_version": VERSION,
    }


def test_request_schema_valid():
    jsonschema.validate(make_req(), load_schema("dream-request.schema.json"))


def test_cycle_receipt_and_branches_schema(tmp_path):
    core = ACDCore(receipts_dir=tmp_path)
    rec = core.dream(make_req())
    jsonschema.validate(rec, load_schema("dream-receipt.schema.json"))
    assert rec["runtime_status"] == "COMPLETED"
    assert rec["shadow"] is True
    assert rec["ontology"] == "SIMULATED"
    assert rec["external_actions_attempted"] == 0
    assert rec["external_actions_executed"] == 0
    assert rec["memory_zone"] == "AAA.POSSIBILITY"
    assert rec["recall_visibility"] == "SCENARIO_ONLY"
    branch_schema = load_schema("possibility-branch.schema.json")
    assert len(rec["branches"]) >= 3
    for branch in rec["branches"]:
        jsonschema.validate(branch, branch_schema)
        assert branch["ontology"] == "SIMULATED"
        assert branch["parent_id"]  # lineage preserved


def test_content_hash_integrity(tmp_path):
    from core.acd_core import _hash

    core = ACDCore(receipts_dir=tmp_path)
    rec = core.dream(make_req())
    expected = _hash({k: v for k, v in rec.items() if k != "content_hash"})
    assert rec["content_hash"] == expected
    # Tamper simulation: any field change must break the hash
    tampered = dict(rec)
    tampered["constitutional_verdict"] = "VOID"
    assert _hash({k: v for k, v in tampered.items() if k != "content_hash"}) != rec["content_hash"]


def test_dissent_and_contradictions_retained(tmp_path):
    core = ACDCore(receipts_dir=tmp_path)
    rec = core.dream(make_req())
    assert isinstance(rec["dissent"], list) and len(rec["dissent"]) >= 1
    assert isinstance(rec["contradictions"], list) and len(rec["contradictions"]) >= 1


def test_contract_mismatch_fails_closed(tmp_path):
    core = ACDCore(receipts_dir=tmp_path)
    bad = make_req()
    bad["contract_version"] = "acd.dream.v0"
    rec = core.dream(bad)
    assert rec["runtime_status"] == "FAILED"
    assert rec["constitutional_verdict"] == "BLOCKED"
    assert rec["external_actions_executed"] == 0
