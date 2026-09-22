"""CHRON Prediction — lifecycle management.

Wraps the existing prediction_store.py with CHRON-native operations.
Adds Brier score computation and calibration tracking.

Prediction lifecycle:
  CREATED → ACTIVE → VERIFIED_CORRECT | VERIFIED_INCORRECT | EXPIRED_UNVERIFIED

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

PREDICTIONS_FILE = Path("/root/chron/data/predictions.jsonl")
CALIBRATION_FILE = Path("/root/chron/data/calibration.json")

MYT = timezone(timedelta(hours=8))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ───────────────────────── PREDICTION STORE ─────────────────────────


def load_predictions() -> list[dict]:
    """Load all predictions from JSONL store."""
    if not PREDICTIONS_FILE.exists():
        return []
    predictions = []
    with open(PREDICTIONS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    predictions.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return predictions


def save_prediction(prediction: dict) -> None:
    """Append a single prediction to JSONL store."""
    PREDICTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PREDICTIONS_FILE, "a") as f:
        f.write(json.dumps(prediction, default=str) + "\n")


def create_prediction(
    claim: str,
    expected_outcome: str,
    confidence: float,
    verify_at: str,
    assumptions: Optional[list[str]] = None,
    source: str = "chron_events",
    source_id: Optional[str] = None,
    principal: str = "arif",
    horizon: str = "?",
) -> dict:
    """Create a new prediction object."""
    pred = {
        "prediction_id": f"pred-{uuid.uuid4().hex[:12]}",
        "claim": claim,
        "expected_outcome": expected_outcome,
        "confidence": confidence,
        "verify_at": verify_at,
        "horizon": horizon,
        "assumptions": assumptions or [],
        "evidence": [],
        "source": source,
        "source_id": source_id,
        "principal": principal,
        "status": "ACTIVE",
        "created_at": _now_iso(),
        "observed_outcome": None,
        "error": None,
        "error_type": None,
        "verified_at": None,
        "brier_score": None,
        "supersedes": None,
    }
    save_prediction(pred)
    return pred


def get_active() -> list[dict]:
    """Get all active (unverified) predictions."""
    return [p for p in load_predictions() if p["status"] == "ACTIVE"]


def get_due() -> list[dict]:
    """Get predictions whose verify_at has arrived."""
    now = datetime.now(timezone.utc)
    due = []
    for p in load_predictions():
        if p["status"] != "ACTIVE":
            continue
        try:
            verify_at = datetime.fromisoformat(p["verify_at"].replace("Z", "+00:00"))
            if now >= verify_at:
                due.append(p)
        except Exception:
            pass
    return due


def get_verified(limit: int = 50) -> list[dict]:
    """Get verified predictions for calibration."""
    verified = [
        p
        for p in load_predictions()
        if p["status"] in ("VERIFIED_CORRECT", "VERIFIED_INCORRECT")
    ]
    verified.sort(key=lambda p: p.get("verified_at", ""), reverse=True)
    return verified[:limit]


# ───────────────────────── BRIER SCORE ─────────────────────────


def compute_brier(prediction: dict, outcome: bool) -> float:
    """Compute Brier score for a binary prediction.

    Brier = (confidence - outcome)^2
    where outcome = 1 if correct, 0 if incorrect.

    Lower is better. Perfect prediction = 0.0.
    Always predicting 0.5 = 0.25.
    """
    confidence = prediction.get("confidence", 0.5)
    return (confidence - (1.0 if outcome else 0.0)) ** 2


def verify_prediction(prediction: dict, observed_outcome: str, correct: bool) -> dict:
    """Verify a prediction and compute Brier score."""
    prediction["observed_outcome"] = observed_outcome
    prediction["verified_at"] = _now_iso()
    prediction["status"] = "VERIFIED_CORRECT" if correct else "VERIFIED_INCORRECT"
    prediction["error"] = 0.0 if correct else 1.0
    prediction["error_type"] = "NONE" if correct else _classify_error(prediction)
    prediction["brier_score"] = compute_brier(prediction, correct)
    return prediction


def _classify_error(prediction: dict) -> str:
    """Classify why a prediction was wrong."""
    if not prediction.get("assumptions"):
        return "UNKNOWN"
    # Default — more specific classification needs domain context
    return "ASSUMPTION_ERROR"


# ───────────────────────── CALIBRATION ─────────────────────────


def compute_calibration() -> dict:
    """Compute calibration statistics from all verified predictions."""
    verified = get_verified()
    if not verified:
        return {
            "total": 0,
            "correct": 0,
            "incorrect": 0,
            "accuracy": None,
            "mean_brier": None,
            "by_error_type": {},
        }

    correct = sum(1 for p in verified if p.get("status") == "VERIFIED_CORRECT")
    incorrect = len(verified) - correct
    brier_scores = [
        p.get("brier_score", 0.25) for p in verified if p.get("brier_score") is not None
    ]

    by_error_type: dict[str, int] = {}
    for p in verified:
        et = p.get("error_type", "UNKNOWN")
        by_error_type[et] = by_error_type.get(et, 0) + 1

    return {
        "total": len(verified),
        "correct": correct,
        "incorrect": incorrect,
        "accuracy": correct / len(verified) if verified else None,
        "mean_brier": sum(brier_scores) / len(brier_scores) if brier_scores else None,
        "by_error_type": by_error_type,
    }


def save_calibration(calibration: dict) -> None:
    """Save calibration stats."""
    CALIBRATION_FILE.parent.mkdir(parents=True, exist_ok=True)
    calibration["updated_at"] = _now_iso()
    CALIBRATION_FILE.write_text(json.dumps(calibration, indent=2, default=str))


def load_calibration() -> Optional[dict]:
    """Load calibration stats."""
    if not CALIBRATION_FILE.exists():
        return None
    try:
        return json.loads(CALIBRATION_FILE.read_text())
    except Exception:
        return None


# ───────────────────────── GENERATE FROM EVENTS ─────────────────────────


def generate_from_chron_events() -> list[dict]:
    """Generate predictions from chron_events.json."""
    chron_events = Path("/root/AAA/scripts/chron_events.json")
    if not chron_events.exists():
        return []

    data = json.loads(chron_events.read_text())
    events = data.get("events", [])
    today = datetime.now(MYT).date()

    # Track existing source_ids to avoid duplicates
    existing = {
        p.get("source_id")
        for p in load_predictions()
        if p.get("source") == "chron_events"
    }

    predictions = []
    for event in events:
        event_id = event.get("id", "")
        if event_id in existing:
            continue

        target_date_str = event.get("target_date")
        if not target_date_str:
            continue

        try:
            target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
        except ValueError:
            continue

        days_until = (target_date - today).days
        if days_until < 0:
            continue

        confidence_map = {
            "CONFIRMED": 0.9,
            "LIKELY": 0.7,
            "ANNOUNCED": 0.8,
            "TENTATIVE": 0.6,
        }
        confidence = confidence_map.get(event.get("confidence", ""), 0.5)

        verify_at = f"{target_date_str}T23:59:59+08:00"

        kind = event.get("kind", "")
        title = event.get("title", "?")

        if kind == "FISCAL":
            claim = f"Budget event: {title}"
            expected = f"{title} will occur on {target_date_str}"
            assumptions = ["No parliamentary delay", "No emergency recess"]
        elif kind == "MARKET_EVENT":
            claim = f"Market event: {title}"
            expected = f"Market condition '{title}' will resolve by {target_date_str}"
            assumptions = ["No regime change in oil markets", "No supply shock"]
        elif kind in ("REGULATORY_WINDOW", "REGULATORY"):
            claim = f"Regulatory event: {title}"
            expected = (
                f"Regulatory change '{title}' will take effect on {target_date_str}"
            )
            assumptions = ["No regulatory delay", "No enforcement exception"]
        else:
            claim = f"Event: {title}"
            expected = f"{title} will occur by {target_date_str}"
            assumptions = []

        horizon_days = days_until
        if horizon_days <= 7:
            horizon = f"{horizon_days}d"
        elif horizon_days <= 30:
            horizon = f"{horizon_days // 7}w"
        else:
            horizon = f"{horizon_days // 30}m"

        pred = create_prediction(
            claim=claim,
            expected_outcome=expected,
            confidence=confidence,
            verify_at=verify_at,
            assumptions=assumptions,
            source="chron_events",
            source_id=event_id,
            horizon=horizon,
        )
        predictions.append(pred)

    return predictions
