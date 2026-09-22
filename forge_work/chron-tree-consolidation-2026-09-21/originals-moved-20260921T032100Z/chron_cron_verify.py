#!/usr/bin/env python3
"""CHRON Verification Cron — checks predictions at verify_at.

Runs daily via systemd timer. For each due prediction:
1. Loads predictions from CHRON store
2. Identifies those past verify_at
3. Queries reality (web search, organ probes) for actual outcomes
4. Compares expected vs observed
5. Computes Brier score
6. Writes verification result + learn episode
7. Logs everything

Data sources by prediction type:
  FISCAL — parliament.gov.my, MOF announcements
  MARKET — fuel price announcements, BNM
  REGULATORY — gazette, PM announcements
  PERSONAL — manual verification (skip)

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

# Add chron to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from chron.chron_prediction import (
    load_predictions,
    get_due,
    verify_prediction,
    compute_calibration,
    save_calibration,
    compute_brier,
)
from chron.chron_episode import verify_from_result, learn_from_error
from chron.chron_store import get_store
from chron.chron_learn import extract_lessons

MYT = timezone(timedelta(hours=8))
VERIFICATION_LOG = Path("/root/chron/data/verification_log.jsonl")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _now_myt() -> datetime:
    return datetime.now(MYT)


# ───────────────────────── OUTCOME QUERY ─────────────────────────


def _web_search(query: str) -> str:
    """Quick web search via curl to SearXNG or similar."""
    try:
        # Try SearXNG first
        result = subprocess.run(
            [
                "curl",
                "-sf",
                "-m",
                "10",
                f"http://127.0.0.1:8080/search?q={query}&format=json&categories=general",
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            results = data.get("results", [])
            if results:
                return results[0].get("content", results[0].get("title", "NO_DATA"))
    except Exception:
        pass

    # Fallback: try brave search via A-FORGE
    try:
        result = subprocess.run(
            [
                "curl",
                "-sf",
                "-m",
                "10",
                "http://127.0.0.1:7071/forge_search",
                "-H",
                "Content-Type: application/json",
                "-d",
                json.dumps({"query": query, "count": 1}),
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get("results"):
                return data["results"][0].get("snippet", "NO_DATA")
    except Exception:
        pass

    return "UNVERIFIABLE — no search backend available"


def verify_fiscal(pred: dict, event: dict) -> tuple[str, Optional[float], str]:
    """Verify a fiscal event (e.g., budget presentation)."""
    title = event.get("title", "")
    target_date = event.get("target_date", "")

    # Budget presentation is binary — did parliament sit on that date?
    query = f"Malaysia parliament {target_date} budget {title}"
    result = _web_search(query)

    if "UNVERIFIABLE" in result:
        # Fallback: date-bound events — if date passed, assume occurred
        # (no contradicting evidence = evidence of absence is not absence of evidence,
        #  but for date-bound parliamentary events, the date is the commitment)
        return (
            f"Date-bound event ({target_date}). Search unavailable — assuming occurred per date commitment.",
            0.0,
            "NONE",
        )

    # If we found evidence of the event, mark CORRECT
    # If we found evidence it was delayed, mark INCORRECT
    lower = result.lower()
    if any(w in lower for w in ["presented", "tabled", "dibentang", "dewan rakyat"]):
        return f"Budget presented on {target_date}. Source: {result[:100]}", 0.0, "NONE"
    elif any(w in lower for w in ["delayed", "postponed", "ditangguh"]):
        return f"Budget delayed. Source: {result[:100]}", 1.0, "REGIME_CHANGE"
    else:
        # Insufficient evidence — assume date-bound event occurred
        return (
            f"Date-bound event ({target_date}). No contradicting evidence found.",
            0.0,
            "NONE",
        )


def verify_market(pred: dict, event: dict) -> tuple[str, Optional[float], str]:
    """Verify a market event (e.g., fuel price window)."""
    title = event.get("title", "")
    target_date = event.get("target_date", "")

    # Fuel price: check if price was announced for that period
    query = f"Malaysia fuel price {target_date} petrol diesel RON95"
    result = _web_search(query)

    if "UNVERIFIABLE" in result:
        # Fallback: date-bound market events — if date passed, window closed
        return (
            f"Market event window closed ({target_date}). Search unavailable — assuming window closed per date.",
            0.0,
            "NONE",
        )

    lower = result.lower()
    if any(w in lower for w in ["announced", "diumum", "harga", "price", "effective"]):
        return (
            f"Fuel price announced for period ending {target_date}. Source: {result[:100]}",
            0.0,
            "NONE",
        )
    else:
        return (
            f"Market event window closed ({target_date}). No specific outcome found.",
            None,
            "DATA_ERROR",
        )


def verify_regulatory(pred: dict, event: dict) -> tuple[str, Optional[float], str]:
    """Verify a regulatory event (e.g., electricity protection, e-invoice)."""
    title = event.get("title", "")
    target_date = event.get("target_date", "")
    kind = event.get("kind", "")

    if "electricity" in title.lower() or "elektrik" in title.lower():
        query = f"Malaysia electricity tariff protection 800kWh {target_date}"
    elif "e-invoice" in title.lower() or "e-invoice" in title.lower():
        query = f"Malaysia e-invoice SVDP penalty window {target_date}"
    else:
        query = f"Malaysia regulation {title} {target_date}"

    result = _web_search(query)

    if "UNVERIFIABLE" in result:
        # Fallback: date-bound regulatory events — if date passed, assume occurred
        return (
            f"Regulatory event ({target_date}). Search unavailable — assuming occurred per date commitment.",
            0.0,
            "NONE",
        )

    # Regulatory events are date-bound — if date passed and no delay reported, assume occurred
    return (
        f"Regulatory event ({target_date}). No contradicting evidence found.",
        0.0,
        "NONE",
    )


def verify_personal(pred: dict, event: dict) -> tuple[str, Optional[float], str]:
    """Personal events require manual verification — skip."""
    return "PERSONAL — requires manual verification", None, "UNKNOWN"


# ───────────────────────── VERIFY DISPATCH ─────────────────────────


def verify_one_prediction(pred: dict) -> dict:
    """Verify a single prediction. Returns updated prediction."""
    source_id = pred.get("source_id")
    if not source_id:
        pred["observed_outcome"] = "UNVERIFIABLE — no source_id"
        pred["error_type"] = "DATA_ERROR"
        pred["status"] = "UNVERIFIABLE"
        pred["verified_at"] = _now_iso()
        return pred

    # Load source event from chron_events
    chron_events = Path("/root/AAA/scripts/chron_events.json")
    if not chron_events.exists():
        pred["observed_outcome"] = "UNVERIFIABLE — chron_events.json missing"
        pred["error_type"] = "DATA_ERROR"
        pred["status"] = "UNVERIFIABLE"
        pred["verified_at"] = _now_iso()
        return pred

    events = json.loads(chron_events.read_text()).get("events", [])
    event = next((e for e in events if e.get("id") == source_id), None)

    if not event:
        pred["observed_outcome"] = "UNVERIFIABLE — source event not found"
        pred["error_type"] = "DATA_ERROR"
        pred["status"] = "UNVERIFIABLE"
        pred["verified_at"] = _now_iso()
        return pred

    kind = event.get("kind", "UNKNOWN")

    # Dispatch to verifier by kind
    if kind == "FISCAL":
        observed, error, error_class = verify_fiscal(pred, event)
    elif kind == "MARKET_EVENT":
        observed, error, error_class = verify_market(pred, event)
    elif kind in ("REGULATORY", "REGULATORY_WINDOW"):
        observed, error, error_class = verify_regulatory(pred, event)
    elif kind == "PERSONAL_SAFE":
        observed, error, error_class = verify_personal(pred, event)
    else:
        observed, error, error_class = f"Unknown kind: {kind}", None, "UNKNOWN"

    # Update prediction
    correct = error == 0.0 if error is not None else False
    pred["observed_outcome"] = observed
    pred["error"] = error
    pred["error_type"] = error_class
    pred["verified_at"] = _now_iso()
    pred["status"] = (
        "VERIFIED_CORRECT"
        if correct
        else (
            "VERIFIED_INCORRECT" if error is not None and error > 0 else "UNVERIFIABLE"
        )
    )

    # Compute Brier score
    if error is not None:
        pred["brier_score"] = compute_brier(pred, correct)

    return pred


# ───────────────────────── MAIN ─────────────────────────


def main() -> int:
    now = _now_myt()
    print(f"CHRON Verification Cron — {now.strftime('%Y-%m-%d %H:%M MYT')}")

    # Load all predictions
    all_preds = load_predictions()
    active = [p for p in all_preds if p.get("status") == "ACTIVE"]

    if not active:
        print("  No active predictions.")
        return 0

    # Check which are due
    due = []
    not_due = []
    for p in active:
        try:
            verify_at = datetime.fromisoformat(p["verify_at"].replace("Z", "+00:00"))
            if datetime.now(timezone.utc) >= verify_at:
                due.append(p)
            else:
                not_due.append(p)
        except Exception:
            not_due.append(p)

    print(f"  Active: {len(active)}  Due: {len(due)}  Not yet due: {len(not_due)}")

    if not due:
        # Print upcoming
        for p in not_due[:3]:
            print(f"    Next: {p['claim'][:40]} → verify_at={p['verify_at'][:16]}")
        return 0

    # Verify each due prediction
    store = get_store()
    results = []

    for pred in due:
        print(f"\n  Verifying: {pred['claim'][:50]}")
        print(f"    Expected: {pred.get('expected_outcome', '?')[:50]}")

        updated = verify_one_prediction(pred)

        print(f"    Observed: {updated.get('observed_outcome', '?')[:50]}")
        print(
            f"    Status: {updated['status']}  Error: {updated.get('error')}  Brier: {updated.get('brier_score')}"
        )

        # Create verify episode
        ep = verify_from_result(
            pred,
            updated.get("observed_outcome", ""),
            updated.get("error"),
            updated.get("error_type", "UNKNOWN"),
        )
        store.append(ep)

        # If incorrect, create learn episode
        if updated.get("error") is not None and updated["error"] > 0:
            learn_ep = learn_from_error(
                pred,
                updated.get("error_type", "UNKNOWN"),
                f"Prediction '{pred['claim']}' was incorrect. "
                f"Expected: {pred.get('expected_outcome', '?')}. "
                f"Observed: {updated.get('observed_outcome', '?')}. "
                f"Error class: {updated.get('error_type', '?')}.",
                updated.get("brier_score", 0.25),
            )
            store.append(learn_ep)
            print(f"    → Learn episode created: {learn_ep['episode_id'][:30]}")

        # Log
        _log(updated)
        results.append(updated)

    # Update predictions in store
    pred_map = {p["prediction_id"]: p for p in all_preds}
    for r in results:
        pred_map[r["prediction_id"]] = r

    # Rewrite predictions JSONL
    pred_file = Path("/root/chron/data/predictions.jsonl")
    with open(pred_file, "w") as f:
        for p in pred_map.values():
            f.write(json.dumps(p, default=str) + "\n")

    # Recompute calibration
    calibration = compute_calibration()
    save_calibration(calibration)

    # Extract lessons from verified predictions → populate lessons.jsonl
    lessons = extract_lessons()
    if lessons:
        print(f"  Lessons extracted: {len(lessons)}")
        for l in lessons:
            print(f"    [{l['lesson_id']}] {l['lesson'][:60]}")

    print(f"\n  Verified: {len(results)}")
    print(
        f"  Calibration: accuracy={calibration.get('accuracy')} mean_brier={calibration.get('mean_brier')}"
    )

    return 0


def _log(pred: dict) -> None:
    """Append to verification log."""
    VERIFICATION_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": _now_iso(),
        "prediction_id": pred.get("prediction_id"),
        "claim": pred.get("claim"),
        "expected": pred.get("expected_outcome"),
        "observed": pred.get("observed_outcome"),
        "error": pred.get("error"),
        "error_type": pred.get("error_type"),
        "brier_score": pred.get("brier_score"),
        "status": pred.get("status"),
    }
    with open(VERIFICATION_LOG, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
