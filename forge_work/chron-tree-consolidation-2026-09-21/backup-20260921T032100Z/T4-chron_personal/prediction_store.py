#!/usr/bin/env python3
"""CHRON Prediction Store — closes Claim → Prediction arrow.

Prediction lifecycle:
  CREATED → ACTIVE → VERIFIED | EXPIRED | SUPERSEDED

At verify_at: verifier computes expected vs observed → error → error_type.

Prediction object carries:
  - claim (what we believe)
  - expected_outcome (what we predict)
  - confidence (0-1)
  - verify_at (appointment with reality)
  - assumptions[] (what must hold)
  - observed_outcome (filled at verification)
  - error (filled at verification)
  - error_type (DATA_ERROR | ASSUMPTION_ERROR | MODEL_ERROR | REGIME_CHANGE | UNKNOWN)

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path

MYT = timezone(timedelta(hours=8))
PREDICTIONS_FILE = Path("/root/.hermes/cron/state/chron_personal/predictions.json")
CHRON_EVENTS = Path("/root/AAA/scripts/chron_events.json")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def now_myt() -> datetime:
    return datetime.now(MYT)


# ───────────────────────── PREDICTION STORE ─────────────────────────

def load_predictions() -> list[dict]:
    """Load all predictions from store."""
    if not PREDICTIONS_FILE.exists():
        return []
    try:
        return json.loads(PREDICTIONS_FILE.read_text()).get("predictions", [])
    except Exception:
        return []


def save_predictions(predictions: list[dict]) -> None:
    """Save predictions to store."""
    PREDICTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "$schema": "chron_predictions_v0",
        "version": "0.1.0",
        "updated_at": now_iso(),
        "count": len(predictions),
        "predictions": predictions,
    }
    PREDICTIONS_FILE.write_text(json.dumps(payload, indent=2, default=str))


def create_prediction(
    claim: str,
    expected_outcome: str,
    confidence: float,
    verify_at: str,
    assumptions: list[str] | None = None,
    source: str = "chron_events",
    source_id: str | None = None,
    principal: str = "arif",
) -> dict:
    """Create a new prediction object."""
    return {
        "prediction_id": f"pred-{uuid.uuid4().hex[:12]}",
        "claim": claim,
        "expected_outcome": expected_outcome,
        "confidence": confidence,
        "verify_at": verify_at,
        "assumptions": assumptions or [],
        "source": source,
        "source_id": source_id,
        "principal": principal,
        "state": "ACTIVE",
        "created_at": now_iso(),
        "observed_outcome": None,
        "error": None,
        "error_type": None,
        "verified_at": None,
        "supersedes": None,
    }


def verify_prediction(prediction: dict, observed_outcome: str) -> dict:
    """Verify a prediction against observed reality. Returns updated prediction."""
    prediction["observed_outcome"] = observed_outcome
    prediction["verified_at"] = now_iso()
    prediction["state"] = "VERIFIED"

    # Error classification
    expected = prediction.get("expected_outcome", "")
    if expected.lower() == observed_outcome.lower():
        prediction["error"] = 0.0
        prediction["error_type"] = "NONE"
    else:
        prediction["error"] = 1.0  # Binary for now; real calibration needs numeric
        # Classify error type based on assumptions
        if not prediction.get("assumptions"):
            prediction["error_type"] = "UNKNOWN"
        else:
            # Default to ASSUMPTION_ERROR — more specific classification needs context
            prediction["error_type"] = "ASSUMPTION_ERROR"

    return prediction


def expire_stale(predictions: list[dict]) -> tuple[list[dict], list[str]]:
    """Expire predictions past their verify_at without verification."""
    now = datetime.now(timezone.utc)
    expired = []
    active = []
    for p in predictions:
        if p["state"] == "ACTIVE":
            try:
                verify_at = datetime.fromisoformat(p["verify_at"].replace("Z", "+00:00"))
                if now > verify_at + timedelta(hours=24):  # 24h grace period
                    p["state"] = "EXPIRED"
                    expired.append(p["prediction_id"])
            except Exception:
                pass
        active.append(p)
    return active, expired


# ───────────────────────── GENERATE FROM CHRON EVENTS ─────────────────────────

def generate_from_chron_events() -> list[dict]:
    """Generate predictions from chron_events.json claims."""
    if not CHRON_EVENTS.exists():
        return []

    try:
        data = json.loads(CHRON_EVENTS.read_text())
        events = data.get("events", [])
    except Exception:
        return []

    predictions = []
    today = now_myt().date()

    for event in events:
        target_date_str = event.get("target_date")
        if not target_date_str:
            continue

        try:
            target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
        except ValueError:
            continue

        # Only predict for events within the next 90 days
        days_until = (target_date - today).days
        if days_until < 0 or days_until > 90:
            continue

        # Generate prediction based on event type
        event_id = event.get("id", "?")
        title = event.get("title", "?")
        kind = event.get("kind", "UNKNOWN")
        consequence = event.get("consequence", "MEDIUM")
        confidence_str = event.get("confidence", "INTERPRETATION")

        # Map confidence string to numeric
        confidence_map = {
            "CONFIRMED": 0.9,
            "LIKELY": 0.7,
            "INTERPRETATION": 0.5,
            "SPECULATIVE": 0.3,
        }
        confidence = confidence_map.get(confidence_str, 0.5)

        # Verify_at = target_date (when the event should resolve)
        verify_at = f"{target_date_str}T23:59:59+08:00"

        # Build prediction
        if kind == "FISCAL":
            claim = f"Budget event: {title}"
            expected = f"{title} will occur on {target_date_str}"
            assumptions = ["No parliamentary delay", "No emergency recess"]
        elif kind == "MARKET_EVENT":
            claim = f"Market event: {title}"
            expected = f"Market condition {title} will resolve by {target_date_str}"
            assumptions = ["No regime change in oil markets", "No supply shock"]
        elif kind == "REGULATORY":
            claim = f"Regulatory event: {title}"
            expected = f"Regulatory change {title} will take effect {target_date_str}"
            assumptions = ["No regulatory delay", "No enforcement exception"]
        else:
            claim = f"Event: {title}"
            expected = f"{title} will occur by {target_date_str}"
            assumptions = []

        pred = create_prediction(
            claim=claim,
            expected_outcome=expected,
            confidence=confidence,
            verify_at=verify_at,
            assumptions=assumptions,
            source="chron_events",
            source_id=event_id,
        )
        predictions.append(pred)

    return predictions


# ───────────────────────── ACTIVE PREDICTIONS ─────────────────────────

def get_active_predictions() -> list[dict]:
    """Get all active (unverified) predictions."""
    return [p for p in load_predictions() if p["state"] == "ACTIVE"]


def get_predictions_due() -> list[dict]:
    """Get predictions whose verify_at has arrived."""
    now = datetime.now(timezone.utc)
    due = []
    for p in load_predictions():
        if p["state"] != "ACTIVE":
            continue
        try:
            verify_at = datetime.fromisoformat(p["verify_at"].replace("Z", "+00:00"))
            if now >= verify_at:
                due.append(p)
        except Exception:
            pass
    return due


def get_verified_predictions(limit: int = 20) -> list[dict]:
    """Get recent verified predictions for calibration."""
    verified = [p for p in load_predictions() if p["state"] == "VERIFIED"]
    verified.sort(key=lambda p: p.get("verified_at", ""), reverse=True)
    return verified[:limit]


# ───────────────────────── CALIBRATION ─────────────────────────

def compute_calibration_stats(verified: list[dict]) -> dict:
    """Compute basic calibration statistics from verified predictions."""
    if not verified:
        return {"total": 0, "correct": 0, "incorrect": 0, "accuracy": None, "by_error_type": {}}

    correct = sum(1 for p in verified if p.get("error", 1) == 0)
    incorrect = len(verified) - correct

    by_error_type: dict[str, int] = {}
    for p in verified:
        et = p.get("error_type", "UNKNOWN")
        by_error_type[et] = by_error_type.get(et, 0) + 1

    return {
        "total": len(verified),
        "correct": correct,
        "incorrect": incorrect,
        "accuracy": correct / len(verified) if verified else None,
        "by_error_type": by_error_type,
    }


# ───────────────────────── CLI ─────────────────────────

def main() -> int:
    """CLI: generate, list, or status."""
    import sys

    args = sys.argv[1:]
    command = args[0] if args else "status"

    if command == "generate":
        # Generate predictions from chron_events
        existing = load_predictions()
        existing_ids = {p.get("source_id") for p in existing if p.get("source") == "chron_events"}
        new_preds = generate_from_chron_events()
        added = 0
        for p in new_preds:
            if p["source_id"] not in existing_ids:
                existing.append(p)
                added += 1
        save_predictions(existing)
        print(f"Generated {added} new predictions ({len(existing)} total)")

    elif command == "active":
        active = get_active_predictions()
        print(f"Active predictions: {len(active)}")
        for p in active:
            print(f"  [{p['prediction_id'][:12]}] {p['claim'][:60]}")
            print(f"    verify_at: {p['verify_at'][:16]}  confidence: {p['confidence']}")

    elif command == "due":
        due = get_predictions_due()
        print(f"Predictions due for verification: {len(due)}")
        for p in due:
            print(f"  [{p['prediction_id'][:12]}] {p['claim'][:60]}")
            print(f"    expected: {p['expected_outcome'][:60]}")

    elif command == "verified":
        verified = get_verified_predictions()
        stats = compute_calibration_stats(verified)
        print(f"Verified: {stats['total']}  Correct: {stats['correct']}  Accuracy: {stats['accuracy']}")
        for p in verified[:5]:
            print(f"  [{p['prediction_id'][:12]}] error_type={p.get('error_type')}")

    else:  # status
        all_preds = load_predictions()
        active = [p for p in all_preds if p["state"] == "ACTIVE"]
        verified = [p for p in all_preds if p["state"] == "VERIFIED"]
        expired = [p for p in all_preds if p["state"] == "EXPIRED"]
        due = get_predictions_due()
        print(f"Predictions: {len(all_preds)} total")
        print(f"  Active: {len(active)}")
        print(f"  Verified: {len(verified)}")
        print(f"  Expired: {len(expired)}")
        print(f"  Due now: {len(due)}")
        if verified:
            stats = compute_calibration_stats(verified)
            print(f"  Accuracy: {stats['accuracy']:.2f}" if stats['accuracy'] else "  Accuracy: N/A")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
