#!/usr/bin/env python3
"""
dream_chron_bridge.py — Wire CHRON calibration data into Dream Candidates.

The missing arrow: p_predictive was null because no one fed prediction
outcomes back into the dream. This module closes that loop.

Flow:
  1. Read CHRON's verified predictions (Brier scores, outcomes)
  2. Read CHRON's calibration snapshot (accuracy, bias, mean_brier)
  3. Read latest dream candidates
  4. For each candidate, compute p_predictive via keyword overlap with predictions
  5. Update candidates, write back

When CHRON has enough resolved predictions matched to a candidate's domain,
p_predictive becomes empirical. When it doesn't, p_predictive stays null
with a note explaining why.

Architecture:
  Dream Engine produces candidates (p_occurrence, p_predictive=null)
  CHRON measures outcomes (Brier, accuracy, calibration)
  This bridge connects them: candidate ← CHRON → p_predictive

DITEMPA BUKAN DIBERI ⚒️
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ── Paths ───────────────────────────────────────────────────────────────────
CHRON_DATA = Path(os.environ.get("CHRON_DATA_DIR", "/root/chron/data"))
PREDICTIONS_FILE = CHRON_DATA / "predictions.jsonl"
CALIBRATION_FILE = CHRON_DATA / "calibration.json"
LESSONS_FILE = CHRON_DATA / "lessons.jsonl"

DREAM_OUTPUT = Path("/root/AAA/knowledge-graph/dream-engine")
CANDIDATES_FILE = DREAM_OUTPUT / "dream_candidates_latest.json"

# Minimum matched predictions needed to compute p_predictive
MIN_MATCHED_FOR_PREDICTIVE = 2

# Keyword domains for semantic matching (simple but effective)
DOMAIN_KEYWORDS = {
    "technical-agent": [
        "agent", "execution", "tool", "code", "deploy", "system",
        "error", "failure", "retry", "probe", "skill", "config",
        "docker", "service", "timer", "cron", "pipeline", "test"
    ],
    "trading-market": [
        "price", "trade", "market", "xauusd", "gold", "commodity",
        "forecast", "prediction", "signal", "chart", "position",
        "brier", "calibration", "accuracy", "verdict"
    ],
    "human-interface": [
        "human", "user", "arif", "telegram", "chat", "message",
        "bridge", "persona", "voice", "register", "tone", "reply"
    ],
    "governance-federation": [
        "governance", "federation", "authority", "seal", "ratify",
        "canon", "constitution", "floor", "boundary", "scope",
        "arifos", "aaa", "vault999", "witness"
    ],
    "memory-architecture": [
        "memory", "qdrant", "redis", "supabase", "graphiti",
        "recall", "store", "embed", "dedup", "consolidate",
        "promotion", "candidate", "wisdom", "lesson"
    ],
    "geoscience-domain": [
        "geology", "basin", "well", "seismic", "petronas",
        "subsurface", "reservoir", "log", "core", "facies"
    ]
}


def load_predictions() -> list[dict]:
    """Load all CHRON predictions."""
    if not PREDICTIONS_FILE.exists():
        return []
    predictions = []
    with open(PREDICTIONS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                predictions.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return predictions


def load_calibration() -> Optional[dict]:
    """Load CHRON calibration snapshot."""
    if not CALIBRATION_FILE.exists():
        return None
    try:
        return json.loads(CALIBRATION_FILE.read_text())
    except Exception:
        return None


def load_lessons() -> list[dict]:
    """Load CHRON lessons."""
    if not LESSONS_FILE.exists():
        return []
    lessons = []
    with open(LESSONS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                lessons.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return lessons


def load_candidates() -> Optional[dict]:
    """Load latest dream candidates snapshot."""
    if not CANDIDATES_FILE.exists():
        return None
    try:
        return json.loads(CANDIDATES_FILE.read_text())
    except Exception:
        return None


def classify_domain(text: str) -> dict[str, int]:
    """Classify text into domains by keyword overlap. Returns {domain: match_count}."""
    text_lower = text.lower()
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > 0:
            scores[domain] = count
    return scores


def match_predictions_to_candidate(
    candidate: dict,
    predictions: list[dict]
) -> list[dict]:
    """Find CHRON predictions that semantically match a dream candidate."""
    statement = candidate.get("claim", {}).get("statement", "")
    scope = candidate.get("claim", {}).get("scope", "")
    match_text = f"{statement} {scope}"

    candidate_domains = classify_domain(match_text)
    if not candidate_domains:
        return []

    primary_domain = max(candidate_domains, key=lambda k: candidate_domains[k])

    matched = []
    for pred in predictions:
        # Only match against verified predictions (have outcomes)
        if pred.get("status") not in ("VERIFIED", "SUPERSEDED"):
            continue

        # Check domain overlap
        pred_text = f"{pred.get('claim', '')} {pred.get('instrument', '')} {pred.get('error_type', '')}"
        pred_domains = classify_domain(pred_text)

        if primary_domain in pred_domains or any(
            d in candidate_domains for d in pred_domains
        ):
            matched.append(pred)

    return matched


def compute_p_predictive(matched: list[dict]) -> tuple[Optional[float], dict]:
    """
    Compute p_predictive from matched CHRON predictions.

    Returns (p_predictive, metadata).
    p_predictive = 1.0 - mean_brier (lower Brier = higher predictive power)
    Only computed if we have enough matched predictions.
    """
    if len(matched) < MIN_MATCHED_FOR_PREDICTIVE:
        return None, {
            "reason": "insufficient_matches",
            "matched_count": len(matched),
            "required": MIN_MATCHED_FOR_PREDICTIVE
        }

    # Compute aggregate Brier from verified predictions
    brier_scores = []
    outcomes = {"HIT": 0, "MISS": 0, "VOID": 0}

    for pred in matched:
        brier = pred.get("brier_score")
        outcome = pred.get("outcome", "VOID")

        if brier is not None:
            brier_scores.append(brier)
        if outcome in outcomes:
            outcomes[outcome] += 1

    if not brier_scores:
        return None, {
            "reason": "no_brier_scores",
            "matched_count": len(matched)
        }

    mean_brier = sum(brier_scores) / len(brier_scores)
    p_predictive = round(1.0 - mean_brier, 4)

    # Compute accuracy (HIT / (HIT + MISS))
    total_decided = outcomes["HIT"] + outcomes["MISS"]
    accuracy = outcomes["HIT"] / total_decided if total_decided > 0 else None

    return p_predictive, {
        "matched_predictions": len(matched),
        "mean_brier": round(mean_brier, 4),
        "p_predictive": p_predictive,
        "outcomes": outcomes,
        "accuracy": round(accuracy, 4) if accuracy is not None else None,
        "prediction_ids": [p.get("prediction_id") for p in matched]
    }


def update_candidates(candidates_data: dict, predictions: list[dict],
                      calibration: Optional[dict], lessons: list[dict]) -> dict:
    """Update dream candidates with CHRON calibration data."""
    candidates = candidates_data.get("candidates", [])
    updated_count = 0

    for candidate in candidates:
        # Skip already-calibrated candidates
        if candidate.get("epistemics", {}).get("p_predictive") is not None:
            continue

        # Match predictions to this candidate
        matched = match_predictions_to_candidate(candidate, predictions)

        # Compute p_predictive
        p_pred, meta = compute_p_predictive(matched)

        # Update candidate
        if "epistemics" not in candidate:
            candidate["epistemics"] = {}

        candidate["epistemics"]["p_predictive"] = p_pred
        candidate["epistemics"]["predictive_metadata"] = meta

        if "temporal" not in candidate:
            candidate["temporal"] = {}
        candidate["temporal"]["prediction_ids"] = meta.get("prediction_ids", [])
        candidate["temporal"]["calibration_n"] = meta.get("matched_predictions", 0)
        candidate["temporal"]["brier_score"] = meta.get("mean_brier")

        # Attach global calibration context
        if calibration:
            candidate["epistemics"]["global_calibration"] = {
                "accuracy": calibration.get("accuracy"),
                "mean_brier": calibration.get("mean_brier"),
                "effective_n": calibration.get("effective_n"),
                "bias": calibration.get("bias"),
            }

        if p_pred is not None:
            updated_count += 1
            print(f"  {candidate['id']}: p_predictive = {p_pred} ({meta['matched_predictions']} predictions, brier={meta['mean_brier']})")
        else:
            print(f"  {candidate['id']}: p_predictive = null ({meta['reason']})")

    # Add CHRON lessons as counterstory material
    active_lessons = [
        l for l in lessons
        if l.get("status") not in ("SUPERSEDED", "RETRACTED")
    ]

    if active_lessons:
        print(f"\n  Active CHRON lessons available for counterstories: {len(active_lessons)}")
        for lesson in active_lessons:
            print(f"    - {lesson.get('lesson_id')}: {lesson.get('lesson', '')[:80]}")

    # Gap analysis: what predictions would enable p_predictive?
    pred_domains_hit = set()
    for pred in predictions:
        pred_text = f"{pred.get('claim', '')} {pred.get('instrument', '')}"
        pred_domains = classify_domain(pred_text)
        pred_domains_hit.update(pred_domains.keys())

    candidate_domains_hit = set()
    for candidate in candidates:
        stmt = candidate.get("claim", {}).get("statement", "")
        cand_domains = classify_domain(stmt)
        candidate_domains_hit.update(cand_domains.keys())

    gap = candidate_domains_hit - pred_domains_hit
    if gap:
        print(f"\n  GAP: No CHRON predictions exist for domains: {', '.join(sorted(gap))}")
        print(f"  To enable p_predictive, CHRON needs predictions in these domains.")
    if pred_domains_hit:
        print(f"  Current CHRON coverage: {', '.join(sorted(pred_domains_hit))}")
    if candidate_domains_hit:
        print(f"  Candidate domains:     {', '.join(sorted(candidate_domains_hit))}")
    overlap = candidate_domains_hit & pred_domains_hit
    if overlap:
        print(f"  Overlap (bridgeable):  {', '.join(sorted(overlap))}")

    # Update metadata
    if "metadata" not in candidates_data:
        candidates_data["metadata"] = {}
    candidates_data["metadata"]["chron_bridge"] = {
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "total_predictions": len(predictions),
        "verified_predictions": len([
            p for p in predictions
            if p.get("status") in ("VERIFIED", "SUPERSEDED")
        ]),
        "candidates_calibrated": updated_count,
        "candidates_total": len(candidates),
        "global_calibration": calibration,
        "active_lessons": len(active_lessons),
    }

    return candidates_data


def main():
    """Bridge CHRON calibration into dream candidates."""
    print("=" * 60)
    print("Dream-CHRON Bridge — Computing p_predictive")
    print("=" * 60)

    # Load data
    print("\n[1/4] Loading CHRON data...")
    predictions = load_predictions()
    calibration = load_calibration()
    lessons = load_lessons()
    print(f"  Predictions: {len(predictions)}")
    print(f"  Calibration: {'loaded' if calibration else 'missing'}")
    print(f"  Lessons: {len(lessons)}")

    # Load candidates
    print("\n[2/4] Loading dream candidates...")
    candidates_data = load_candidates()
    if not candidates_data:
        print("  No candidates found. Run dream_engine.py first.")
        return

    candidates = candidates_data.get("candidates", [])
    print(f"  Candidates: {len(candidates)}")

    # Bridge
    print("\n[3/4] Computing p_predictive for each candidate...")
    updated = update_candidates(candidates_data, predictions, calibration, lessons)

    # Write back
    print("\n[4/4] Writing updated candidates...")
    CANDIDATES_FILE.write_text(json.dumps(updated, indent=2))
    print(f"  Written: {CANDIDATES_FILE}")

    # Also append to JSONL log
    jsonl_path = DREAM_OUTPUT / "chron_bridge_log.jsonl"
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "predictions_used": len(predictions),
        "candidates_updated": updated.get("metadata", {}).get("chron_bridge", {}).get("candidates_calibrated", 0),
    }
    with open(jsonl_path, 'a') as f:
        f.write(json.dumps(log_entry) + "\n")

    print("\n" + "=" * 60)
    print("BRIDGE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
