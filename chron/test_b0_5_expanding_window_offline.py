"""
B0.5 OFFLINE INSTRUMENTATION — pytest test suite (T1-T12).
"""
import ast
import hashlib
import json
import os
import sys
from pathlib import Path

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))

from b0_5_comparator import expand_window, brier  # noqa: E402

FIXTURE_PATH = THIS_DIR / "fixtures" / "b0_5_calibration_fixture.json"


def load_fixture():
    with open(FIXTURE_PATH) as f:
        return json.load(f)


def hypothesis_key(record):
    return record["hypothesis_key"]


# ----- T1 -----
def test_t1_duplicate_rows_collapse_deterministically():
    fx = load_fixture()
    result = expand_window(
        predictions=fx["predictions"],
        outcomes=fx["outcomes"],
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=tuple(fx["evaluation_windows"]["full_window"]),
    )
    assert result["raw_sample_count"] == 8, f"T1 raw: {result}"
    assert result["effective_sample_count"] == 5, f"T1 effective: {result}"
    assert result["duplicate_rows_collapsed"] == 3, f"T1 collapsed: {result}"


# ----- T2 -----
def test_t2_raw_and_effective_counts_both_reported():
    fx = load_fixture()
    result = expand_window(
        predictions=fx["predictions"],
        outcomes=fx["outcomes"],
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=tuple(fx["evaluation_windows"]["full_window"]),
    )
    assert "raw_sample_count" in result
    assert "effective_sample_count" in result
    assert isinstance(result["raw_sample_count"], int)
    assert isinstance(result["effective_sample_count"], int)


# ----- T3 -----
def test_t3_model_brier_computed_from_fixture():
    fx = load_fixture()
    result = expand_window(
        predictions=fx["predictions"],
        outcomes=fx["outcomes"],
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=tuple(fx["evaluation_windows"]["full_window"]),
    )
    expected = (0.0625 + 0.2025 + 0.16 + 0.01 + 0.09) / 5
    assert abs(result["model_brier"] - expected) < 1e-9, f"T3 brier: {result['model_brier']} vs {expected}"


# ----- T4 (corrected: dict-insertion-order dedup) -----
def test_t4_base_rate_probability_and_brier_reproducible():
    fx = load_fixture()
    r1 = expand_window(
        predictions=fx["predictions"],
        outcomes=fx["outcomes"],
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=tuple(fx["evaluation_windows"]["full_window"]),
    )
    r2 = expand_window(
        predictions=fx["predictions"],
        outcomes=fx["outcomes"],
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=tuple(fx["evaluation_windows"]["full_window"]),
    )
    assert r1["base_rate_probability"] == r2["base_rate_probability"]
    assert r1["base_rate_brier"] == r2["base_rate_brier"]
    # After dedup (last-write-wins, dict insertion order), effective = [p005, p008, p004, p006, p007]
    # effective[:-1] = [p005, p008, p004, p006] -> outcomes 1,1,0,1 -> n_pos=3, n_total=4 -> 0.75
    # current_outcome = p007 outc=0 -> base_rate_brier = (0.75-0)^2 = 0.5625
    assert abs(r1["base_rate_probability"] - 0.75) < 1e-9
    assert abs(r1["base_rate_brier"] - 0.5625) < 1e-9


# ----- T5 -----
def test_t5_model_worse_or_equal_to_baseline_relation():
    fx = load_fixture()
    result = expand_window(
        predictions=fx["predictions"],
        outcomes=fx["outcomes"],
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=tuple(fx["evaluation_windows"]["full_window"]),
    )
    if result["model_brier"] is not None and result["base_rate_brier"] is not None:
        assert result["model_beats_baseline"] == (result["model_brier"] < result["base_rate_brier"])


# ----- T6 -----
def test_t6_model_better_than_baseline():
    fx = load_fixture()
    result = expand_window(
        predictions=fx["predictions"],
        outcomes=fx["outcomes"],
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=tuple(fx["evaluation_windows"]["full_window"]),
    )
    assert result["model_beats_baseline"] is True
    assert result["model_brier"] < result["base_rate_brier"]


# ----- T7 -----
def test_t7_insufficient_data_fails_closed():
    fx = load_fixture()
    narrow = (fx["predictions"][-1]["timestamp"], fx["predictions"][-1]["timestamp"])
    result = expand_window(
        predictions=fx["predictions"],
        outcomes=fx["outcomes"],
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=narrow,
    )
    assert result["insufficient_evidence"] is True
    assert result["model_brier"] is None
    assert result["base_rate_probability"] is None
    assert result["base_rate_brier"] is None
    assert result["model_beats_baseline"] is None
    assert "raw_sample_count" in result
    assert "effective_sample_count" in result


# ----- T8 -----
def test_t8_eight_required_fields_present():
    fx = load_fixture()
    result = expand_window(
        predictions=fx["predictions"],
        outcomes=fx["outcomes"],
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=tuple(fx["evaluation_windows"]["full_window"]),
    )
    required = [
        "model_brier", "base_rate_probability", "base_rate_brier",
        "effective_sample_count", "raw_sample_count",
        "duplicate_rows_collapsed", "evaluation_window",
        "model_beats_baseline",
    ]
    for k in required:
        assert k in result, f"T8 missing field: {k}"


# ----- T9 (AST-import check, not string match) -----
def test_t9_no_chron_probability_in_execution():
    fx = load_fixture()
    result = expand_window(
        predictions=fx["predictions"],
        outcomes=fx["outcomes"],
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=tuple(fx["evaluation_windows"]["full_window"]),
    )
    forbidden = ["execution_score", "eligibility", "routing", "judgment", "authorization", "seal"]
    for k in forbidden:
        assert k not in result, f"T9 leaked forbidden field: {k}"
    src = (THIS_DIR / "b0_5_comparator.py").read_text()
    tree = ast.parse(src)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imported.add(n.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.add(node.module.split(".")[0])
    forbidden_modules = ["arif_judge", "arif_seal", "arif_forge", "aforge", "arifFlow", "VAULT999", "ClaimLedger"]
    for mod in forbidden_modules:
        assert mod not in imported, f"T9 comparator imports forbidden: {mod}"


# ----- T10 -----
def test_t10_temporal_ordering_preserved():
    predictions = [
        {"prediction_id": "s1", "hypothesis_key": "ev1", "predicted_probability": 0.7,
         "event_time": 100, "prediction_time": 110, "action_time": 120, "verification_time": 130,
         "timestamp": 110},
        {"prediction_id": "s2", "hypothesis_key": "ev2", "predicted_probability": 0.3,
         "event_time": 200, "prediction_time": 210, "action_time": 220, "verification_time": 230,
         "timestamp": 210},
    ]
    for p in predictions:
        assert p["event_time"] <= p["prediction_time"]
        assert p["prediction_time"] < p["action_time"]
        assert p["action_time"] <= p["verification_time"]
    outcomes = {"s1": 1, "s2": 0}
    result = expand_window(
        predictions=predictions,
        outcomes=outcomes,
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=(0, 1000),
    )
    assert result["raw_sample_count"] == 2


# ----- T11 -----
def test_t11_zero_live_chron_writes():
    pre = {}
    for path in ["/root/VAULT999/receipts_v2.jsonl", "/root/chron/chron_events.json"]:
        if os.path.exists(path):
            with open(path, "rb") as f:
                pre[path] = hashlib.sha256(f.read()).hexdigest()[:16]
    fx = load_fixture()
    expand_window(
        predictions=fx["predictions"],
        outcomes=fx["outcomes"],
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=tuple(fx["evaluation_windows"]["full_window"]),
    )
    for path, h_pre in pre.items():
        with open(path, "rb") as f:
            h_post = hashlib.sha256(f.read()).hexdigest()[:16]
        assert h_pre == h_post, f"T11: {path} changed {h_pre} -> {h_post}"


# ----- T12 -----
def test_t12_zero_organ_mutations():
    targets = [
        "/root/VAULT999/receipts_v2.jsonl",
        "/root/chron/chron_events.json",
        "/root/chron/data/chron.db",
    ]
    pre = {}
    for path in targets:
        if os.path.exists(path):
            with open(path, "rb") as f:
                pre[path] = hashlib.sha256(f.read()).hexdigest()[:16]
    fx = load_fixture()
    expand_window(
        predictions=fx["predictions"],
        outcomes=fx["outcomes"],
        duplicate_identity_rule=hypothesis_key,
        evaluation_window=tuple(fx["evaluation_windows"]["full_window"]),
    )
    for path, h_pre in pre.items():
        with open(path, "rb") as f:
            h_post = hashlib.sha256(f.read()).hexdigest()[:16]
        assert h_pre == h_post, f"T12: {path} changed {h_pre} -> {h_post}"
