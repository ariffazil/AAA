#!/usr/bin/env python3
"""Model Governance Card tests — runtime wiring Phase 1 (F13-sealed 2026-10-30).

REALITY > EVERYTHING: resolved identity only from probe receipts; floating lanes
render UNKNOWN; cards may lower confidence, never raise authority.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

AAA = Path(__file__).resolve().parents[2]
REGISTRY = AAA / "registry"


@pytest.fixture(scope="session")
def gc():
    spec = importlib.util.spec_from_file_location("gc_mod", REGISTRY / "governance_cards.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def cards(gc):
    spec = importlib.util.spec_from_file_location("compile_mod", REGISTRY / "compile.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    entities = m.load_entities()
    meta = {"source_commit": "testrev", "source_manifest_hash": "0" * 64}
    return gc.build_cards(entities, meta)


def test_six_lane_cards_built(cards):
    assert set(cards) == {"333", "555", "888", "999", "forge", "hermes"}


def test_333_card_bound_by_probe_receipt(cards):
    c = cards["333"]
    assert c["requested_model"] == "glm-5.3"
    assert c["resolved_model"] == "glm-5.3"          # from live probe receipt only
    assert c["identity_state"] == "matched"
    assert c["verdict"] == "BOUND"
    assert c["registry_revision"] == "testrev"
    assert c["resolution_evidence_ref"] and c["resolution_evidence_ref"].startswith("probe-")


def test_floating_lane_renders_UNKNOWN(cards):
    for lane in ("forge", "hermes", "999", "555", "888"):
        c = cards[lane]
        assert c["resolved_model"] == "UNKNOWN", lane
        assert c["identity_state"] == "UNRESOLVED", lane
        assert c["verdict"] == "HOLD", lane


def test_card_never_grants_authority(cards):
    for lane, c in cards.items():
        assert c["authority_ceiling"]["authorize"] is False, lane


def test_card_budget_and_hash(gc, cards):
    for lane, c in cards.items():
        raw = json.dumps(c, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        assert len(raw) <= gc.CARD_HARD_MAX_BYTES, f"{lane} card {len(raw)}B exceeds hard max"
        clean = {k: v for k, v in c.items() if k != "card_hash"}
        want = hashlib.sha256(json.dumps(clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode()).hexdigest()
        assert c["card_hash"] == want, lane


def test_cards_deterministic(gc, cards):
    spec = importlib.util.spec_from_file_location("compile_mod2", REGISTRY / "compile.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    again = gc.build_cards(m.load_entities(), {"source_commit": "testrev", "source_manifest_hash": "0" * 64})
    assert again == cards


def test_compiled_card_files_present_and_consistent():
    d = REGISTRY / "generated" / "model-governance-cards"
    assert d.exists() and len(list(d.glob("*.json"))) == 6
    c333 = json.loads((d / "333.json").read_text())
    assert c333["identity_state"] == "matched"
    assert c333["registry_revision"] != "UNKNOWN"


def test_unknown_lane_card_fails_closed(gc):
    c = gc.unknown_lane_card("zzz", "no assignment")
    assert c["identity_state"] == "UNRESOLVED" and c["verdict"] == "HOLD"
    assert not any(c["authority_ceiling"].values())
    assert c["note"]


def test_cards_carry_no_secrets(cards):
    import re
    pat = re.compile(r"(?<![A-Za-z0-9_-])(?:sk|tp|gho|ghp|ghs)-[A-Za-z0-9]{20,}")
    for lane, c in cards.items():
        assert not pat.search(json.dumps(c)), lane


def test_card_session_binding_is_not_in_compiled_card(cards):
    # session binding lives at INIT (arifOS), never in the compiled projection
    for lane, c in cards.items():
        assert "session_binding" not in c and "session_id" not in c, lane
