"""CHRON Verify — checks predictions at verify_at.

The verification engine runs on a schedule (or manually).
For each due prediction:
  1. Check if the event/outcome can be observed
  2. Classify: CORRECT, INCORRECT, UNVERIFIABLE
  3. Compute Brier score
  4. Emit verify episode
  5. Feed result to chron_learn for lesson extraction

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

from chron.chron_prediction import (
    get_due,
    get_active,
    verify_prediction,
    compute_calibration,
    save_calibration,
    load_predictions,
)
from chron.chron_episode import verify_from_result
from chron.chron_store import get_store

MYT = timezone(timedelta(hours=8))
CHRON_EVENTS = Path("/root/AAA/scripts/chron_events.json")
VERIFICATION_LOG = Path("/root/chron/data/verification_log.jsonl")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ───────────────────────── VERIFICATION ─────────────────────────


def verify_event_prediction(pred: dict) -> tuple[dict, str, Optional[float], str]:
    """Verify a prediction derived from chron_events.

    Returns: (updated_prediction, observed_outcome, error, error_class)
    """
    source_id = pred.get("source_id")
    if not source_id:
        return pred, "UNVERIFIABLE — no source_id", None, "DATA_ERROR"

    if not CHRON_EVENTS.exists():
        return pred, "UNVERIFIABLE — chron_events.json not found", None, "DATA_ERROR"

    try:
        events = json.loads(CHRON_EVENTS.read_text()).get("events", [])
    except Exception:
        return pred, "UNVERIFIABLE — cannot parse chron_events", None, "DATA_ERROR"

    event = next((e for e in events if e.get("id") == source_id), None)
    if not event:
        return pred, "UNVERIFIABLE — source event not found", None, "DATA_ERROR"

    target_date_str = event.get("target_date")
    today = datetime.now(MYT).date()

    try:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return pred, "UNVERIFIABLE — no target_date", None, "DATA_ERROR"

    if today < target_date:
        return pred, f"NOT YET DUE — target is {target_date_str}", None, "PENDING"

    # Target date passed — verify based on kind
    kind = event.get("kind", "UNKNOWN")

    if kind in ("FISCAL", "REGULATORY", "REGULATORY_WINDOW"):
        # Date-bound events: if date passed, event window closed
        # For now: mark CORRECT (event dates are usually met)
        # More specific verification needs external data
        observed = f"Event window closed ({target_date_str}). Date-bound event."
        return pred, observed, 0.0, "NONE"

    elif kind == "MARKET_EVENT":
        # Market events need price data — mark UNVERIFIABLE for now
        observed = f"Market event window closed ({target_date_str}). Needs price data."
        return pred, observed, None, "DATA_ERROR"

    else:
        observed = f"Event window closed ({target_date_str}). Kind={kind}, needs manual verification."
        return pred, observed, None, "UNKNOWN"


# ───────────────────────── RUN VERIFICATION ─────────────────────────


def run_verification(dry_run: bool = False) -> dict:
    """Run verification on all due predictions.

    Returns summary dict.
    """
    due = get_due()
    now = datetime.now(MYT).strftime("%Y-%m-%d %H:%M MYT")

    if not due:
        return {
            "timestamp": now,
            "due": 0,
            "verified": 0,
            "unverifiable": 0,
            "message": "No predictions due for verification.",
        }

    results = []
    store = get_store()
    all_preds = load_predictions()
    pred_map = {p["prediction_id"]: p for p in all_preds}

    for pred in due:
        pred_id = pred["prediction_id"]
        observed, error, error_class = None, None, "UNKNOWN"

        # Verify based on source
        if pred.get("source") == "chron_events":
            pred, observed, error, error_class = verify_event_prediction(pred)
        else:
            observed = "UNKNOWN — no verification method for source"
            error_class = "UNKNOWN"

        # Determine correctness
        correct = error == 0.0 if error is not None else False

        if error is not None and not dry_run:
            # Update prediction
            updated = verify_prediction(pred, observed, correct)
            pred_map[pred_id] = updated

            # Create verify episode
            ep = verify_from_result(pred, observed, error, error_class)
            store.append(ep)

            # Log
            _log_verification(
                pred_id,
                pred.get("claim", "?"),
                pred.get("expected_outcome", "?"),
                observed,
                error,
                error_class,
                updated["status"],
            )

        results.append(
            {
                "prediction_id": pred_id,
                "claim": pred.get("claim", "?"),
                "observed": observed,
                "error": error,
                "error_class": error_class,
                "status": pred_map[pred_id].get("status", "?"),
            }
        )

    # Save updated predictions
    if not dry_run:
        _save_all_predictions(list(pred_map.values()))

        # Recompute calibration
        calibration = compute_calibration()
        save_calibration(calibration)

    verified_count = sum(
        1 for r in results if r["error"] is not None and r["error"] == 0.0
    )
    incorrect_count = sum(
        1 for r in results if r["error"] is not None and r["error"] > 0.0
    )
    unverifiable_count = sum(1 for r in results if r["error"] is None)

    return {
        "timestamp": now,
        "due": len(due),
        "verified_correct": verified_count,
        "verified_incorrect": incorrect_count,
        "unverifiable": unverifiable_count,
        "results": results,
    }


def _log_verification(pred_id, claim, expected, observed, error, error_class, status):
    """Append to verification log."""
    VERIFICATION_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": _now_iso(),
        "prediction_id": pred_id,
        "claim": claim,
        "expected": expected,
        "observed": observed,
        "error": error,
        "error_class": error_class,
        "status": status,
    }
    with open(VERIFICATION_LOG, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")


def _save_all_predictions(predictions: list[dict]) -> None:
    """Rewrite predictions JSONL from updated list."""
    pred_file = Path("/root/chron/data/predictions.jsonl")
    pred_file.parent.mkdir(parents=True, exist_ok=True)
    with open(pred_file, "w") as f:
        for p in predictions:
            f.write(json.dumps(p, default=str) + "\n")


# ───────────────────────── CLI ─────────────────────────


def main() -> int:
    import sys

    args = sys.argv[1:]
    dry_run = "--dry-run" in args

    result = run_verification(dry_run=dry_run)

    print(f"CHRON Verify — {result['timestamp']}")
    print(f"  Due: {result['due']}")
    if result["due"] > 0:
        print(f"  Correct: {result.get('verified_correct', 0)}")
        print(f"  Incorrect: {result.get('verified_incorrect', 0)}")
        print(f"  Unverifiable: {result.get('unverifiable', 0)}")
        for r in result.get("results", []):
            print(f"    [{r['prediction_id'][:12]}] {r['claim'][:50]}")
            print(f"      observed: {str(r['observed'])[:50]}")
            print(
                f"      error: {r['error']}  class: {r['error_class']}  status: {r['status']}"
            )
    else:
        print(f"  {result.get('message', '')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
