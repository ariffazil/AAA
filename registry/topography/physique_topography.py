"""
physique_topography — pose-normalized body-relation extraction.

WHY THIS FILE EXISTS
  The federation already has a 1:1 FACE verifier (arifosmcp/biometric, receipts in
  VAULT999, band 0.42/0.25). It has NO body layer. This module is the body layer:
  it turns landmark observations into pose-normalized relation invariants.

CONSTITUTIONAL POSITION (read before using)
  Body topography is a STATE witness, never an identity witness.
  It may CORROBORATE a face match. It may NEVER name a person on its own.
  Rationale: physique changes with cut/bulk, pump, flexion, clothing, lens, and
  viewpoint. Name + history + relations already carry the permanent identity load
  (see /root/AAA/registry/identity_cards/*.yaml — W3/W4/W5/W6 never expire).
  A body is the least permanent thing about a person. Do not build identity on it.

  Every output carries `evidence_class` so a caller cannot silently promote a
  body observation into an identification:
      STATE_OBSERVATION  — posture-dependent, do not compare across sessions naively
      RATIO_INVARIANT    — long-bone relation, stable enough to compare across sessions
      UNUSABLE           — occlusion/foreshortening too severe; must abstain

DEPENDENCY NOTE
  This module uses numpy only. Landmarks must be supplied by a pose estimator
  (none is installed as of 2026-09-16) or by a vision model's structured read.
  It deliberately does NOT bundle a pose model: swapping in a detector changes the
  measurement regime, so that choice belongs to a governed decision, not an import.

Layout assumed (COCO-17 subset). Extra keys are ignored; missing keys degrade to
UNUSABLE rather than raising, because a half-occluded frame is a normal input.
  nose, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist,
  right_wrist, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

import numpy as np

# ── relation catalogue ────────────────────────────────────────────────────────
# Each entry: (name, numerator segments, denominator segments, class, min_vis)
# Segment names are pairs of landmark keys. Ratios of SUMS of bone lengths are far
# more robust than two-point ratios because one bad landmark only perturbs one term.

# Coverage groups: a read is only cross-session-comparable when it has an anchor in
# BOTH groups. Discovered by test 2026-09-16: with the whole lower body occluded the
# module still reported GOOD, because 2 of 4 invariants are upper-body-only and the
# 50%-coverage rule was satisfied by the upper body alone. A torso-and-arms-only read
# cannot re-identify a stance across sessions — it must abstain upward to FAIR.
COVERAGE_GROUPS: dict[str, list[str]] = {
    "UPPER": ["arm_span_to_torso", "upper_to_lower_arm"],
    "LOWER": ["femur_to_tibia", "torso_to_femur"],
}

RATIO_CATALOGUE: dict[str, dict[str, Any]] = {
    # --- long-bone relations: the only cross-session-comparable family ---------
    "arm_span_to_torso": {
        "num": [("left_shoulder", "left_wrist"), ("right_shoulder", "right_wrist")],
        "den": [("left_shoulder", "left_hip"), ("right_shoulder", "right_hip")],
        "class": "RATIO_INVARIANT",
        "note": "requires both arms extended or both flexed symmetrically",
    },
    "upper_to_lower_arm": {
        "num": [("left_shoulder", "left_elbow"), ("right_shoulder", "right_elbow")],
        "den": [("left_elbow", "left_wrist"), ("right_elbow", "right_wrist")],
        "class": "RATIO_INVARIANT",
        "note": "single most clothing-blind limb relation",
    },
    "femur_to_tibia": {
        "num": [("left_hip", "left_knee"), ("right_hip", "right_knee")],
        "den": [("left_knee", "left_ankle"), ("right_knee", "right_ankle")],
        "class": "RATIO_INVARIANT",
        "note": "needs legs in frame; unusable under long shorts crop",
    },
    "torso_to_femur": {
        "num": [("left_shoulder", "left_hip"), ("right_shoulder", "right_hip")],
        "den": [("left_hip", "left_knee"), ("right_hip", "right_knee")],
        "class": "RATIO_INVARIANT",
        "note": "standing-height proxy that does not need a calibration object",
    },
    # --- posture/shape state: recorded, NEVER used to confirm identity ---------
    "shoulder_to_hip": {
        "num": [("left_shoulder", "right_shoulder")],
        "den": [("left_hip", "right_hip")],
        "class": "STATE_OBSERVATION",
        "note": "V-taper proxy. Moves with lat spread, lean, camera height. Do NOT "
                "use as a scale reference — it is the most pose-variable pair.",
    },
    "neck_to_shoulder": {
        "num": [("nose", "left_shoulder"), ("nose", "right_shoulder")],
        "den": [("left_shoulder", "right_shoulder")],
        "class": "STATE_OBSERVATION",
        "note": "head tilt and camera elevation dominate this; measure only when "
                "gaze is level and head is unsupported",
    },
}

# Long bones used for the robust scale. Deliberately EXCLUDES shoulder breadth and
# neck: those are the two most flexion-sensitive pairs on a gym physique.
SCALE_SEGMENTS = [
    ("left_hip", "left_knee"), ("right_hip", "right_knee"),
    ("left_knee", "left_ankle"), ("right_knee", "right_ankle"),
    ("left_shoulder", "left_elbow"), ("right_shoulder", "right_elbow"),
    ("left_elbow", "left_wrist"), ("right_elbow", "right_wrist"),
]

MIN_VIS = 0.30          # below this a landmark is treated as absent
MIN_SCALE_SEGMENTS = 3  # need this many usable bones before normalizing at all


@dataclass
class TopographyResult:
    """A body-relation read. Never an identity. Always carries its own uncertainty."""
    ratios: dict[str, float] = field(default_factory=dict)
    ratios_resolved: list[str] = field(default_factory=list)
    ratio_evidence_class: dict[str, str] = field(default_factory=dict)
    symmetry: dict[str, float] = field(default_factory=dict)
    scale_reference: float = 0.0
    scale_segments_used: int = 0
    coverage_groups: dict[str, bool] = field(default_factory=dict)  # UPPER/LOWER anchors
    frame_quality: str = "UNUSABLE"        # GOOD | FAIR | UNUSABLE
    evidence_class: str = "UNUSABLE"
    abstained: bool = True
    abstain_reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    # provenance — mandatory, because a ratio without its acquisition conditions is
    # not comparable to the same ratio measured another way
    provenance: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict:
        return asdict(self)


def _p(lm: dict, key: str) -> np.ndarray | None:
    """Fetch a landmark's (x, y[, z]) if present and visible enough."""
    v = lm.get(key)
    if v is None:
        return None
    try:
        if isinstance(v, dict):                       # {x, y, visibility}
            if float(v.get("visibility", 1.0)) < MIN_VIS:
                return None
            xy = [float(v["x"]), float(v["y"])]
            if "z" in v:
                xy.append(float(v["z"]))
            return np.asarray(xy, dtype=float)
        arr = np.asarray(v, dtype=float).ravel()
        return arr if arr.size >= 2 else None
    except (TypeError, ValueError, KeyError):
        return None


def _seg_len(lm: dict, a: str, b: str) -> float | None:
    pa, pb = _p(lm, a), _p(lm, b)
    if pa is None or pb is None:
        return None
    n = min(pa.size, pb.size)                 # use shared dims (2D or 3D)
    d = float(np.linalg.norm(pa[:n] - pb[:n]))
    return d if d > 1e-6 else None


def _sum_segments(lm: dict, pairs: list[tuple[str, str]]) -> tuple[float, int]:
    vals = [v for v in (_seg_len(lm, a, b) for a, b in pairs) if v is not None]
    return (float(sum(vals)), len(vals)) if vals else (0.0, 0)


def normalize(lm: dict) -> tuple[dict, float, int, list[str]]:
    """Pose-normalize landmarks about the pelvis and scale by a ROBUST long-bone reference.

    Why not divide by shoulder width (the common recipe): shoulder breadth is the
    landmark pair that moves most with lat spread, flexion and camera elevation, so
    making it the denominator injects pose noise into EVERY derived ratio. Instead
    the scale is the median usable long-bone length — a bad landmark perturbs one
    term and the median absorbs it.

    Returns (normalized_landmarks, scale, segments_used, warnings).
    """
    warnings: list[str] = []

    lh, rh = _p(lm, "left_hip"), _p(lm, "right_hip")
    if lh is not None and rh is not None:
        origin = (lh + rh) / 2.0
    else:
        ls, rs = _p(lm, "left_shoulder"), _p(lm, "right_shoulder")
        if ls is None or rs is None:
            return {}, 0.0, 0, ["no pelvis and no shoulder axis — cannot establish origin"]
        origin = (ls + rs) / 2.0
        warnings.append("origin from shoulder midpoint (hips occluded)")

    bones = [v for v in (_seg_len(lm, a, b) for a, b in SCALE_SEGMENTS) if v is not None]
    if len(bones) < MIN_SCALE_SEGMENTS:
        return {}, 0.0, len(bones), [f"only {len(bones)} usable long bones (need {MIN_SCALE_SEGMENTS})"]
    scale = float(np.median(bones))

    # Rotation: pelvis->shoulder axis vertical, shoulder axis horizontal.
    ls, rs = _p(lm, "left_shoulder"), _p(lm, "right_shoulder")
    rot = None
    if ls is not None and rs is not None:
        sh_axis = rs - ls
        if np.linalg.norm(sh_axis[:2]) > 1e-6:
            th = np.arctan2(sh_axis[1], sh_axis[0])
            c, s = np.cos(-th), np.sin(-th)
            rot = np.array([[c, -s], [s, c]], dtype=float)
    if rot is None:
        warnings.append("no reliable shoulder axis — translation-only normalization")

    out: dict[str, np.ndarray] = {}
    for k in lm:
        p = _p(lm, k)
        if p is None:
            continue
        q = p[:2] - origin[:2]
        if rot is not None:
            q = rot @ q
        out[k] = q / scale
    return out, scale, len(bones), warnings


def symmetry(lm_norm: dict) -> dict[str, float]:
    """Bilateral asymmetry. Recorded at low weight; NOT corrected away.

    A single frame's asymmetry is usually scapular position, unilateral loading or
    perspective. It only becomes evidence when it repeats across independent
    sessions — so this returns raw deltas and lets the caller accumulate them.
    """
    out: dict[str, float] = {}
    for a, b in [("left_shoulder", "right_shoulder"), ("left_elbow", "right_elbow"),
                 ("left_wrist", "right_wrist"), ("left_knee", "right_knee"),
                 ("left_ankle", "right_ankle")]:
        pa, pb = lm_norm.get(a), lm_norm.get(b)
        if pa is None or pb is None:
            continue
        # mirrored x: after rotation the axis is horizontal, so compare |x| and y
        out[f"{a.split('_', 1)[1]}_height_delta"] = float(pa[1] - pb[1])
        out[f"{a.split('_', 1)[1]}_reach_delta"] = float(abs(pa[0]) - abs(pb[0]))
    return out


def read(lm: dict, *, acquisition: dict | None = None) -> TopographyResult:
    """Extract pose-normalized body relations from one frame's landmarks.

    Abstains (rather than guessing) whenever the frame cannot support the claim.
    """
    res = TopographyResult()
    res.provenance = {"acquisition": acquisition or {}, "extractor": "physique_topography/1.0.0"}

    if not lm:
        res.abstain_reasons.append("no landmarks supplied")
        return res

    norm, scale, n_seg, warns = normalize(lm)
    res.scale_reference, res.scale_segments_used, res.warnings = scale, n_seg, warns
    if not norm or scale <= 0:
        res.abstain_reasons.extend(warns or ["normalization failed"])
        return res

    for name, spec in RATIO_CATALOGUE.items():
        num, n_num = _sum_segments(norm, spec["num"])
        den, n_den = _sum_segments(norm, spec["den"])
        if n_num == 0 or n_den == 0 or den <= 1e-9:
            continue
        res.ratios[name] = round(num / den, 6)
        res.ratio_evidence_class[name] = spec["class"]
        if n_num < len(spec["num"]) or n_den < len(spec["den"]):
            res.warnings.append(f"{name}: partial pairs ({n_num}/{n_den}) — one-sided")

    res.symmetry = symmetry(norm)
    res.ratios_resolved = sorted(res.ratios)

    # Frame quality: how much of the catalogue actually resolved, and did the
    # invariant family (the only cross-session-comparable one) survive at all.
    resolvable = {k: v for k, v in res.ratios.items()
                  if res.ratio_evidence_class.get(k) == "RATIO_INVARIANT"}
    total_inv = len([k for k, c in RATIO_CATALOGUE.items() if c["class"] == "RATIO_INVARIANT"])
    ratio_cov = len(resolvable) / max(1, total_inv)
    groups_present = {g: any(k in resolvable for k in keys)
                      for g, keys in COVERAGE_GROUPS.items()}
    res.coverage_groups = dict(groups_present)
    both_groups = all(groups_present.values())

    if ratio_cov >= 0.5 and both_groups and n_seg >= MIN_SCALE_SEGMENTS:
        res.frame_quality = "GOOD"
        res.evidence_class = "RATIO_INVARIANT"
        res.abstained = False
    elif resolvable and n_seg >= MIN_SCALE_SEGMENTS:
        res.frame_quality = "FAIR"
        res.evidence_class = "STATE_OBSERVATION"
        res.abstained = True
        if not both_groups:
            missing = [g for g, ok in groups_present.items() if not ok]
            res.abstain_reasons.append(
                f"no invariant anchor in {'/'.join(missing)} body group — "
                f"half-body read is not cross-session comparable")
        else:
            res.abstain_reasons.append(f"only {ratio_cov:.0%} of invariant catalogue resolved")
    else:
        res.frame_quality = "UNUSABLE"
        res.evidence_class = "UNUSABLE"
        res.abstained = True
        res.abstain_reasons.append("no cross-session-comparable relation resolved")

    return res


def compare(a: TopographyResult, b: TopographyResult,
            *, tolerance: float = 0.12) -> dict:
    """Compare two reads. Returns per-ratio relative delta and a corroboration verdict.

    Corroboration only. The output can never assert identity: `verdict` is one of
    CORROBORATES / DIVERGES / INSUFFICIENT. A caller that wants a NAME must get it
    from the consent-bound face witness plus the permanent name/history witnesses.
    """
    if a.abstained or b.abstained:
        return {"verdict": "INSUFFICIENT",
                "reason": "at least one read abstained",
                "a": a.abstain_reasons, "b": b.abstain_reasons}
    shared = [k for k in a.ratios if k in b.ratios
              and a.ratio_evidence_class.get(k) == "RATIO_INVARIANT"
              and b.ratio_evidence_class.get(k) == "RATIO_INVARIANT"]
    if not shared:
        return {"verdict": "INSUFFICIENT", "reason": "no shared invariant ratio"}
    deltas = {k: round(abs(a.ratios[k] - b.ratios[k]) / max(abs(a.ratios[k]), 1e-9), 6)
              for k in shared}
    within = sum(1 for d in deltas.values() if d <= tolerance)
    frac = within / len(deltas)
    verdict = "CORROBORATES" if frac >= 0.75 else ("DIVERGES" if frac <= 0.25 else "AMBIGUOUS")
    return {"verdict": verdict, "fraction_within_tolerance": round(frac, 3),
            "tolerance": tolerance, "deltas": deltas,
            "note": "corroboration only — NEVER sufficient to assert identity"}
