"""Tests for physique_topography — synthetic landmarks, no ML dependency.

Run:  /opt/arifos/venv/bin/python -m pytest registry/topography/test_physique_topography.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from physique_topography import (  # noqa: E402
    RATIO_CATALOGUE, compare, read, symmetry,
)


def L(x, y, vis=0.95):
    return {"x": float(x), "y": float(y), "visibility": vis}


def standing_subject(scale=1.0, shoulder_w=100.0, hip_w=80.0, arm_len=140.0,
                     leg_len=190.0, upper_frac=0.45):
    """A crude upright figure. Coordinates roughly anatomical, y grows downward.

    shoulder_w and hip_w are INDEPENDENT: anatomically hip width does not follow
    shoulder width, and coupling them in the fixture made the shoulder-breadth test
    fail for the wrong reason (it moved the femurs, not the scale).
    """
    s = scale
    return {
        "nose": L(300, 100),
        "left_shoulder": L(300 - shoulder_w / 2, 160),
        "right_shoulder": L(300 + shoulder_w / 2, 160),
        "left_elbow": L(300 - shoulder_w / 2, 160 + arm_len * upper_frac * s),
        "right_elbow": L(300 + shoulder_w / 2, 160 + arm_len * upper_frac * s),
        "left_wrist": L(300 - shoulder_w / 2, 160 + arm_len * s),
        "right_wrist": L(300 + shoulder_w / 2, 160 + arm_len * s),
        "left_hip": L(300 - hip_w / 2, 300),
        "right_hip": L(300 + hip_w / 2, 300),
        "left_knee": L(300 - hip_w / 2 * 0.75, 300 + leg_len * 0.55 * s),
        "right_knee": L(300 + hip_w / 2 * 0.75, 300 + leg_len * 0.55 * s),
        "left_ankle": L(300 - hip_w / 2 * 0.75, 300 + leg_len * s),
        "right_ankle": L(300 + hip_w / 2 * 0.75, 300 + leg_len * s),
    }


def test_full_frame_resolves_invariants():
    r = read(standing_subject())
    assert r.frame_quality == "GOOD", r.abstain_reasons
    assert not r.abstained
    assert r.evidence_class == "RATIO_INVARIANT"
    inv = [k for k, v in r.ratio_evidence_class.items() if v == "RATIO_INVARIANT"]
    assert len(inv) >= 3, r.ratios
    assert r.scale_segments_used >= 3


def test_scale_ignores_shoulder_breadth():
    """Shoulder breadth must NOT change the invariant ratios: it is excluded from scale."""
    a = read(standing_subject(shoulder_w=100.0))
    b = read(standing_subject(shoulder_w=150.0))   # broader 'V-taper' subject
    for k in ("upper_to_lower_arm", "femur_to_tibia"):
        if k in a.ratios and k in b.ratios:
            rel = abs(a.ratios[k] - b.ratios[k]) / max(a.ratios[k], 1e-9)
            assert rel < 0.02, f"{k} drifted {rel} with shoulder width -> scale is contaminated"
    # while the STATE ratio is allowed (and expected) to move
    if "shoulder_to_hip" in a.ratios and "shoulder_to_hip" in b.ratios:
        assert b.ratios["shoulder_to_hip"] > a.ratios["shoulder_to_hip"]


def test_same_body_two_frames_corroborates():
    a = read(standing_subject())
    b = read(standing_subject(scale=1.0))      # same anatomy, same framing
    c = compare(a, b)
    assert c["verdict"] == "CORROBORATES", c


def test_different_body_diverges():
    a = read(standing_subject(arm_len=140.0, leg_len=190.0))
    b = read(standing_subject(arm_len=175.0, leg_len=165.0))  # long-armed, short-legged
    c = compare(a, b)
    assert c["verdict"] in ("DIVERGES", "AMBIGUOUS"), c


def test_occluded_lower_body_abstains():
    lm = standing_subject()
    for k in ("left_knee", "right_knee", "left_ankle", "right_ankle"):
        lm.pop(k)
    r = read(lm)
    assert r.abstained, r.ratios
    assert r.frame_quality in ("FAIR", "UNUSABLE")
    assert r.coverage_groups.get("LOWER") is False
    assert any("half-body" in x for x in r.abstain_reasons), r.abstain_reasons


def test_no_landmarks_abstains():
    r = read({})
    assert r.abstained and r.evidence_class == "UNUSABLE"
    assert r.abstain_reasons


def test_missing_landmark_does_not_raise():
    lm = standing_subject()
    lm.pop("nose")
    lm.pop("left_wrist")
    r = read(lm)
    assert isinstance(r.ratios, dict)


def test_low_visibility_landmark_dropped():
    lm = standing_subject()
    for k in ("left_ankle", "right_ankle"):
        lm[k] = L(300, 500, vis=0.05)
    r = read(lm)
    assert r.scale_segments_used >= 3          # still normalized on remaining bones


def test_compare_never_asserts_identity():
    c = compare(read(standing_subject()), read(standing_subject()))
    assert c["verdict"] in ("CORROBORATES", "DIVERGES", "AMBIGUOUS", "INSUFFICIENT")
    assert "never sufficient" in c["note"].lower()


def test_evidence_classes_are_declared_for_every_ratio():
    for name, spec in RATIO_CATALOGUE.items():
        assert spec["class"] in ("RATIO_INVARIANT", "STATE_OBSERVATION"), name
        assert spec["num"] and spec["den"], name


def test_symmetry_reports_both_axes():
    s = symmetry(read(standing_subject()).ratios and {})
    # empty input -> empty output, no crash
    assert isinstance(s, dict)


def test_long_bone_proportion_swap_is_caught():
    """A different body PLAN (long-armed, short-legged) must diverge on bone ratios,
    not just on the state ratios that a pump or a cut can move."""
    a = read(standing_subject(arm_len=140.0, leg_len=190.0, upper_frac=0.45))
    b = read(standing_subject(arm_len=200.0, leg_len=150.0, upper_frac=0.60))
    c = compare(a, b)
    assert c["verdict"] == "DIVERGES", c


def test_coverage_groups_reported():
    r = read(standing_subject())
    assert r.coverage_groups == {"UPPER": True, "LOWER": True}, r.coverage_groups


def test_upper_only_read_is_not_good():
    """Arms and torso only (legs cropped, the normal gym framing) must be FAIR, not GOOD."""
    lm = standing_subject()
    for k in ("left_hip", "right_hip", "left_knee", "right_knee",
              "left_ankle", "right_ankle"):
        lm.pop(k)
    r = read(lm)
    assert r.abstained and r.coverage_groups.get("LOWER") is False
