"""PR 3 — SCT decision event + trace_id (no raw token in logs)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from governance.sct_decision_event import (
    DECISION_EVENT_JSON_SCHEMA,
    append_decision_event,
    build_decision_event,
    emit_decision,
    extract_trace_id,
    new_trace_id,
)
from governance.federation_sct import gate_tool_ingress


@pytest.fixture
def event_dir(tmp_path, monkeypatch):
    d = tmp_path / "events"
    monkeypatch.setenv("SCT_DECISION_EVENT_DIR", str(d))
    # force module to re-read default — append uses env at call time via Path in module
    import governance.sct_decision_event as m

    monkeypatch.setattr(m, "_DEFAULT_EVENT_DIR", d)
    return d


class TestTraceId:
    def test_mint_format(self):
        t = new_trace_id()
        assert t.startswith("trc-")
        assert len(t) > 8

    def test_from_arguments(self):
        assert extract_trace_id({"trace_id": "trc-abc"}) == "trc-abc"

    def test_from_header(self):
        assert (
            extract_trace_id({}, headers={"X-Trace-Id": "trc-hdr-1"}) == "trc-hdr-1"
        )

    def test_mint_when_absent(self):
        t = extract_trace_id({})
        assert t.startswith("trc-")


class TestDecisionEvent:
    def test_no_raw_token_fields(self):
        ev = build_decision_event(
            tool="forge_execute",
            organ="a-forge",
            decision="REJECT",
            reason_code="SCT_REQUIRED",
            sct_fingerprint="sha256:deadbeef",
            actor_id="agent",
        )
        blob = ev.to_jsonl()
        assert "sct_v1." not in blob
        assert "Bearer" not in blob
        assert "sha256:deadbeef" in blob
        d = json.loads(blob)
        assert d["decision"] == "REJECT"
        assert d["schema"] == "sct_decision_event.v1"

    def test_append_jsonl(self, event_dir):
        ev = build_decision_event(
            tool="forge_status",
            organ="a-forge",
            decision="ALLOW",
            reason_code="OK_OBSERVE_NO_SCT",
            trace_id="trc-test-1",
        )
        path = append_decision_event(ev, directory=event_dir)
        assert path is not None
        lines = path.read_text().strip().splitlines()
        assert len(lines) == 1
        assert json.loads(lines[0])["trace_id"] == "trc-test-1"

    def test_schema_required_keys(self):
        req = set(DECISION_EVENT_JSON_SCHEMA["required"])
        assert "trace_id" in req
        assert "decision" in req


class TestGateEmitsDecision:
    def test_reject_emits_trace_id(self, event_dir):
        rej = gate_tool_ingress(
            "forge_execute",
            {"actor_id": "agent", "trace_id": "trc-shared-65"},
            organ="a-forge",
        )
        assert rej is not None
        assert rej.get("error") == "SCT_REQUIRED"
        assert rej.get("trace_id") == "trc-shared-65"
        # file written
        files = list(event_dir.glob("sct_decisions_*.jsonl"))
        assert files
        raw = files[0].read_text()
        assert "trc-shared-65" in raw
        assert "sct_v1." not in raw
        assert "REJECT" in raw

    def test_allow_observe_emits(self, event_dir):
        args = {"actor_id": "agent", "trace_id": "trc-obs-1"}
        rej = gate_tool_ingress("forge_status", args, organ="a-forge")
        assert rej is None
        files = list(event_dir.glob("sct_decisions_*.jsonl"))
        assert files
        assert "OK_OBSERVE_NO_SCT" in files[0].read_text()
        assert "ALLOW" in files[0].read_text()
