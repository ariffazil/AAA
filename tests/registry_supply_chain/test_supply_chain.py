#!/usr/bin/env python3
"""
Supply-chain registry test suite — ARIFOS::AAA_MODEL_SUPPLY_CHAIN_REGISTRY::2026-10-30::v1 Phase 7.

Covers: schema validity, broken refs, duplicate IDs, conflation guard, evidence status,
knowledge-cutoff claims, freshness split, route expiry, empty-success FAIL,
mismatch HOLD, known-remap WARN (A), silent-upgrade HOLD (B), floating-alias
ineligibility (D), independence collapse (E), secret scan, deterministic compile,
compatibility projection, append-only probes, incident preservation.

Run: python3 -m pytest tests/registry_supply_chain/test_supply_chain.py -q
"""

from __future__ import annotations

import importlib.util
import io
import json
import shutil
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest
import yaml

AAA = Path(__file__).resolve().parents[2]
REAL_REGISTRY = AAA / "registry"


@pytest.fixture(scope="session")
def reg(tmp_path_factory):
    """Copy of the real registry in tmp, with compile.py imported FROM the copy."""
    regdir = tmp_path_factory.mktemp("reg") / "registry"
    shutil.copytree(REAL_REGISTRY, regdir)
    spec = importlib.util.spec_from_file_location("compile_copy", regdir / "compile.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return regdir, mod


# ── 1. schema validity + 17. compatibility projection ──────────────────────────

def test_real_registry_validates_clean(reg):
    regdir, m = reg
    entities = m.load_entities()
    errors = (
        m.validate_entity_schemas(entities)
        + m.check_duplicate_ids(entities)
        + m.check_references(entities)
        + m.check_conflation(entities)
        + m.check_secrets()
        + m.check_probe_append_only(entities)
    )
    assert errors == [], "real registry must validate clean:\n" + "\n".join(errors)


def test_nine_catalog_profiles_accessible(reg):
    regdir, m = reg
    records = m.load_catalog()
    assert len(records) == 9
    model_records = [r for r in records if isinstance(r.get("identity"), dict) and "id" in r["identity"]]
    provider_projections = [r for r in records if "provider" in r and "identity" not in r]
    assert len(model_records) == 8
    assert len(provider_projections) == 1  # zai.yaml — provider map, not a model record
    assert m.generate_federation_model(records)["record_count"] == 8


# ── 2-6. structural guards (synthetic negatives) ───────────────────────────────

def test_broken_reference_detected(reg):
    _, m = reg
    entities = m.load_entities()
    entities["families"].append({"_source_file": "synthetic", "family_id": "ghost-fam",
                                 "developer_refs": ["nonexistent-org"], "release_refs": []})
    errs = m.check_references(entities)
    assert any("nonexistent-org" in e for e in errs)


def test_duplicate_ids_detected(reg):
    _, m = reg
    entities = m.load_entities()
    entities["routes"].append(dict(entities["routes"][0]))
    errs = m.check_duplicate_ids(entities)
    assert any("duplicate route_id" in e for e in errs)


def test_conflation_guard(reg):
    _, m = reg
    entities = m.load_entities()
    # ytl-ai-cloud is API_provider only — crediting it as a developer must fail
    entities["families"].append({"_source_file": "synthetic", "family_id": "fake-fam",
                                 "developer_refs": ["ytl-ai-cloud"], "release_refs": []})
    errs = m.check_conflation(entities)
    assert any("conflation" in e and "ytl-ai-cloud" in e for e in errs)


def test_missing_evidence_status_rejected_by_schema(reg):
    _, m = reg
    if m.jsonschema is None:
        pytest.skip("jsonschema not installed")
    entities = m.load_entities()
    bad = dict(entities["organizations"][0])
    bad.pop("evidence_status")
    bad["_source_file"] = "synthetic"
    entities["organizations"] = [bad]
    errs = m.validate_entity_schemas(entities)
    assert errs, "entity without evidence_status must fail schema"


def test_knowledge_cutoff_requires_evidence_status(reg):
    _, m = reg
    if m.jsonschema is None:
        pytest.skip("jsonschema not installed")
    entities = m.load_entities()
    bad = dict(entities["releases"][0])
    bad["knowledge_cutoff"] = {"value": "2026-01-01"}  # bare claim, no evidence axis
    bad["_source_file"] = "synthetic"
    entities["releases"] = [bad]
    errs = m.validate_entity_schemas(entities)
    assert errs, "knowledge_cutoff without evidence_status must fail"


# ── 7-8. freshness split + expiry ──────────────────────────────────────────────

def test_freshness_split_family_vs_route(reg):
    regdir, m = reg
    entities = m.load_entities()
    for f in entities["families"]:
        assert "family_freshness" in f, f"family {f.get('family_id')} lost family_freshness"
        assert "route_freshness" not in f
    for r in entities["routes"]:
        assert "route_freshness" in r, f"route {r.get('route_id')} lost route_freshness"
        assert "family_freshness" not in r


def test_route_expiry_reported(reg):
    _, m = reg
    report = m.build_freshness_report(m.load_entities(), "2026-10-30T00:00:00+00:00")
    stale = [r for r in report["route_freshness"] if r["stale"]]
    # groq route carries a stale witness by design — the report must surface it
    assert any(r["route_id"] == "groq-openai" for r in stale)


# ── 9-12 + A/B: verdict grammar regression cases ──────────────────────────────

sys.path.insert(0, str(REAL_REGISTRY))
from update import verdict_for  # noqa: E402

V = lambda ne, sv, fs, mk=True: {"non_empty": ne, "schema_valid": sv, "finish_state_valid": fs, "expected_marker_present": mk}


def test_case_C_empty_success_is_FAIL():
    assert verdict_for("m", "m", 200, V(False, True, True), None, []) == "FAIL"


def test_mismatch_without_remap_is_HOLD():
    assert verdict_for("deepseek-v3.2", "deepseek-v4-pro", 200, V(True, True, True), None, []) == "HOLD"


def test_case_A_known_remap_is_WARN():
    remaps = [{"from": "glm-5.2", "to": "glm-5.3", "severity_on_match": "WARN"}]
    assert verdict_for("glm-5.2", "glm-5.3", 200, V(True, True, True), None, remaps) == "WARN"


def test_case_B_silent_upgrade_is_HOLD():
    # same resolution as A but NOT in known_remaps — must not be smoothed to WARN
    assert verdict_for("deepseek-v3.2", "deepseek-v4-pro", 200, V(True, True, True), None, []) == "HOLD"


def test_exact_echo_is_PASS_and_missing_marker_is_FAIL():
    assert verdict_for("glm-5.3", "glm-5.3", 200, V(True, True, True, True), "PONG", []) == "PASS"
    assert verdict_for("glm-5.3", "glm-5.3", 200, V(True, True, True, False), "PONG", []) == "FAIL"


def test_unresolved_identity_is_HOLD():
    assert verdict_for("x", None, 200, V(True, True, True), None, []) == "HOLD"


def test_non_200_is_FAIL():
    assert verdict_for("x", "x", 402, V(False, False, False), None, []) == "FAIL"


# ── D. frozen-reference eligibility ────────────────────────────────────────────

def frozen_eligible(route: dict, latest_probe: dict | None) -> bool:
    mut = str(route.get("mutability_class", "UNKNOWN"))
    if mut.endswith("FLOATING") or mut == "UNKNOWN":
        return False
    if not latest_probe:
        return False
    return latest_probe.get("requested_model") == latest_probe.get("resolved_model")


def test_case_D_floating_alias_ineligible_pinned_eligible(reg):
    _, m = reg
    entities = m.load_entities()
    routes = {r["route_id"]: r for r in entities["routes"]}
    assert routes["zai-coding-openai"]["mutability_class"] == "PROVIDER_ALIAS_FLOATING"
    assert frozen_eligible(routes["zai-coding-openai"], None) is False
    pinned = dict(routes["zai-coding-openai"], mutability_class="SELF_HOSTED_HASH_PINNED")
    assert frozen_eligible(pinned, {"requested_model": "m", "resolved_model": "m"}) is True
    assert frozen_eligible(pinned, {"requested_model": "m", "resolved_model": "other"}) is False


# ── E. independence collapse ───────────────────────────────────────────────────

def collapse(proposer_fd, verifier_fd, judge_fd):
    def doms(fd):
        return {(fd or {}).get("provider"), (fd or {}).get("endpoint_cluster"), (fd or {}).get("router_ref", (fd or {}).get("provider"))}
    return bool(doms(proposer_fd) & doms(verifier_fd) & doms(judge_fd))


def test_case_E_independence_collapse(reg):
    _, m = reg
    entities = m.load_entities()
    fd = {r["route_id"]: r.get("failure_domain") for r in entities["routes"]}
    # synthetic collapse: all three roles on fed-4000
    assert collapse(fd["fed-4000"], fd["fed-4000"], fd["fed-4000"]) is True
    # current federation: 333=zai, 555=kimi(+fed rung), 888=fed/gemini — no triple collapse
    assert collapse(fd["zai-coding-openai"], fd["kimi-coding-openai"], fd["fed-4000"]) is False


# ── 15. secrets ────────────────────────────────────────────────────────────────

def test_secret_scan_clean_and_catches(reg):
    regdir, m = reg
    assert m.check_secrets() == []
    bad = regdir / "routes" / "zz-secret-trap.yaml"
    bad.write_text("endpoint_ref: https://x\napi_key: sk-abcdefgh1234567890abcdef\n", encoding="utf-8")
    try:
        errs = m.check_secrets()
        assert errs and "secret-like" in errs[0]
    finally:
        bad.unlink()


# ── 16. deterministic compilation ──────────────────────────────────────────────

def test_deterministic_compile(reg):
    regdir, m = reg
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = m.compile_registry()
    assert rc == 0, f"initial compile failed:\n{buf.getvalue()}"
    outs = list((regdir / "generated").glob("*.json")) + list((regdir / "compiled").glob("*"))

    def snapshot():
        return {p.name: p.read_bytes() for p in sorted(outs)}

    first = snapshot()
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = m.compile_registry()
    assert rc == 0, f"second compile failed:\n{buf.getvalue()}"
    assert snapshot() == first, "second compile must be byte-identical"


def test_generated_declares_provenance(reg):
    regdir, m = reg
    buf = io.StringIO()
    with redirect_stdout(buf):
        m.compile_registry()
    doc = json.loads((regdir / "generated" / "provider-map.json").read_text())
    assert doc["generated"] is True
    assert doc["generator_version"].startswith("aaa-supply-chain-compiler/")
    assert doc["source_paths"], "generated output must declare its sources"


# ── 18. append-only probes ─────────────────────────────────────────────────────

def test_probe_append_only_guard(reg):
    _, m = reg
    entities = m.load_entities()
    dup = dict(entities["probes"][0])
    entities["probes"].append(dup)
    errs = m.check_probe_append_only(entities)
    assert any("append-only" in e for e in errs)


def test_probe_receipt_hash_is_verifiable(reg):
    regdir, _ = reg
    for fp in sorted((regdir / "probes").glob("*.yaml")):
        rec = yaml.safe_load(fp.read_text())
        clean = {k: v for k, v in rec.items() if k != "receipt_hash"}
        import hashlib
        want = hashlib.sha256(json.dumps(clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode()).hexdigest()
        assert rec["receipt_hash"] == want, f"{fp.name}: receipt_hash not recomputable"


# ── 19. incident history preserved ─────────────────────────────────────────────

def test_incidents_preserved_with_scar_history(reg):
    _, m = reg
    entities = m.load_entities()
    incs = {i["incident_id"]: i for i in entities["incidents"]}
    assert "INC-001-glm52-silent-remap" in incs
    assert "INC-002-deepseek-v3.2-silent-upgrade-claim" in incs
    assert incs["INC-001-glm52-silent-remap"]["status"] == "classified"
    assert incs["INC-002-deepseek-v3.2-silent-upgrade-claim"]["status"] == "UNVERIFIED"
    # resolved incidents are retained, never deleted
    assert incs["INC-003-deepseek-v4flash-compat-retirement"]["status"] == "resolved"


# ── drift report surfaces open risks ───────────────────────────────────────────

def test_drift_report_flags_unverified_and_floating(reg):
    _, m = reg
    dr = m.build_drift_report(m.load_entities())
    assert any(i["incident_id"].startswith("INC-002") for i in dr["open_unverified_incidents"])
    assert "qwen-tp/deepseek-v3.2" in [a["alias_id"] for a in dr["floating_aliases"]]
    assert "ilmu-nemo" in dr["unknown_developer_families"]
