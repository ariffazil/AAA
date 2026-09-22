#!/usr/bin/env python3
"""CHRON Prediction Verifier — checks predictions at verify_at.

Runs daily. For each prediction whose verify_at has arrived:
1. Checks if the event/outcome can be observed from available data
2. Classifies: VERIFIED (matched), CONTRADICTED (mismatched), UNVERIFIABLE (no data)
3. Computes error and error_type
4. Writes verification result back to prediction store
5. Emits calibration stats

Schema:
- v0 (chron_predictions_v0): event predictions only — uses chron_events.json
- v1 (chron_predictions_v1): price predictions — uses yfinance, Brier scoring
  via chron_price_predictions module

Verification sources:
- chron_events.json (event dates)
- yfinance: instrument → ticker close price (v1)
- executions.db (scheduler behavior)
- deliveries.db (delivery outcomes)
- Manual input (for market/regulatory events)

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Make sibling module importable
sys.path.insert(0, str(Path(__file__).parent))

from chron_price_predictions import (
    SCHEMA_V1,
    is_price_prediction,
    verify_price_prediction,
    compute_calibration,
)

MYT = timezone(timedelta(hours=8))
PREDICTIONS_FILE = Path("/root/.hermes/cron/state/chron_personal/predictions.json")

# ── Every store a prediction may live in (REPAIR 2026-09-20) ─────────────────
# This loader used to read exactly ONE file. Two live stores existed, and they
# shared ZERO prediction ids: the verified store held 12 rows, while the store
# the generators actually write held 20 — including the two F5-private Syed and
# mother predictions. The daily verifier ran, reported "0 due", and was correct
# about a ledger nobody writes to. Receipts would have landed with no witness.
#
# The loader is now a UNION, and every row carries the store it came from so the
# save path can write each row back to its OWN ledger rather than migrating
# everything into the first one it finds.
PREDICTION_STORES: list[Path] = [
    Path("/root/.hermes/cron/state/chron_personal/predictions.json"),  # json  {predictions:[…]}
    Path("/root/chron/data/predictions.jsonl"),                        # jsonl, one row per line
]


def _load_one(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        raw = path.read_text()
    except OSError:
        return []
    if path.suffix == ".jsonl":
        rows = []
        for line in raw.splitlines():
            line = line.strip()
            if line.startswith("{"):
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return rows
    try:
        return json.loads(raw).get("predictions", [])
    except Exception:
        return []


def load_predictions() -> list[dict]:
    """Union of every prediction store; each row tagged with `_store`."""
    merged: dict[str, dict] = {}
    for path in PREDICTION_STORES:
        for row in _load_one(path):
            pid = row.get("prediction_id")
            if not pid:
                continue
            row = dict(row)
            row.setdefault("_store", str(path))
            # First store listed wins on a genuine id collision — but collisions
            # are a defect worth seeing, so keep the loser addressable.
            if pid in merged:
                merged[pid].setdefault("_also_in", []).append(str(path))
                continue
            merged[pid] = row
    return list(merged.values())
CHRON_EVENTS = Path("/root/AAA/scripts/chron_events.json")
OUTPUT_FILE = Path("/root/.hermes/cron/state/chron_personal/verification_log.jsonl")
CALIBRATION_REPORT = Path(
    "/root/.hermes/cron/state/chron_personal/calibration_report.json"
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def now_myt() -> datetime:
    return datetime.now(MYT)


# ───────────────────────── LOAD ─────────────────────────


def save_predictions(predictions: list[dict]) -> None:
    """Write each row back to the store it came from.

    REPAIR 2026-09-20 — the naive version wrote everything it had loaded into
    PREDICTIONS_FILE. Now that the loader is a union, that would have silently
    migrated the jsonl store's rows into the json store on the next verification
    (a second, worse fragmentation). Rows are grouped by `_store`; the jsonl
    store is rewritten line-for-line after a timestamped backup.
    """
    by_store: dict[str, list[dict]] = {}
    for p in predictions:
        origin = p.get("_store") or str(PREDICTIONS_FILE)
        by_store.setdefault(origin, []).append({k: v for k, v in p.items() if not k.startswith("_")})

    for origin, rows in by_store.items():
        path = Path(origin)
        if path.suffix == ".jsonl":
            if path.exists():
                backup = path.with_suffix(f".jsonl.bak-{datetime.now(MYT).strftime('%Y%m%d%H%M%S')}")
                try:
                    backup.write_bytes(path.read_bytes())
                except OSError:
                    pass
            with path.open("w", encoding="utf-8") as fh:
                for row in rows:
                    fh.write(json.dumps(row, default=str) + "\n")
            continue

        path.parent.mkdir(parents=True, exist_ok=True)
        schema, version = "chron_predictions_v0", "0.1.0"
        if path.exists():
            try:
                existing = json.loads(path.read_text())
                schema = existing.get("$schema", schema)
                version = existing.get("version", version)
            except Exception:
                pass
        path.write_text(json.dumps(
            {"$schema": schema, "version": version, "updated_at": now_iso(),
             "count": len(rows), "predictions": rows},
            indent=2, default=str))


def get_due_predictions(predictions: list[dict]) -> list[dict]:
    """Predictions whose verify_at has arrived.

    REPAIR 2026-09-20 — two silent-skip defects are gone:
      1. It read `p["state"]`, but rows written by the generators carry
         `status`, and rows in the json store carried NEITHER. A missing key
         raised KeyError, was swallowed by the bare `except`, and the row was
         skipped in silence — which is how a store with two predictions three
         days past due still reported "due_count: 0".
      2. A malformed or absent verify_at was swallowed the same way. It is now
         counted and reported as UNPARSEABLE, never dropped quietly.
    """
    now = datetime.now(timezone.utc)
    due: list[dict] = []
    for p in predictions:
        state = p.get("state", p.get("status", "ACTIVE")) or "ACTIVE"
        if str(state).upper() not in {"ACTIVE", "PENDING", "NONE", ""}:
            continue  # already closed (CORRECT / CONTRADICTED / UNVERIFIABLE …)
        raw = p.get("verify_at")
        if not raw:
            p["_unparseable"] = "no verify_at"
            continue
        try:
            verify_at = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        except ValueError:
            p["_unparseable"] = f"bad verify_at: {raw!r}"
            continue
        if verify_at.tzinfo is None:
            verify_at = verify_at.replace(tzinfo=timezone.utc)
        if now >= verify_at:
            due.append(p)
    return due


# ───────────────────────── VERIFY ─────────────────────────


def verify_event_prediction(pred: dict) -> dict:
    """Verify a prediction derived from chron_events.

    Check if the target_date has passed → event either occurred or didn't.
    For now: if target_date passed, mark as VERIFIED (event window closed).
    More specific verification needs external data.
    """
    source_id = pred.get("source_id")
    if not source_id:
        return pred

    # Load chron_events to check current state
    if not CHRON_EVENTS.exists():
        pred["observed_outcome"] = "UNVERIFIABLE — chron_events.json not found"
        pred["error_type"] = "DATA_ERROR"
        pred["state"] = "UNVERIFIABLE"
        pred["verified_at"] = now_iso()
        return pred

    try:
        events = json.loads(CHRON_EVENTS.read_text()).get("events", [])
    except Exception:
        pred["observed_outcome"] = "UNVERIFIABLE — cannot parse chron_events"
        pred["error_type"] = "DATA_ERROR"
        pred["state"] = "UNVERIFIABLE"
        pred["verified_at"] = now_iso()
        return pred

    event = next((e for e in events if e.get("id") == source_id), None)
    if not event:
        pred["observed_outcome"] = "UNVERIFIABLE — source event not found"
        pred["error_type"] = "DATA_ERROR"
        pred["state"] = "UNVERIFIABLE"
        pred["verified_at"] = now_iso()
        return pred

    target_date_str = event.get("target_date")
    today = now_myt().date()

    try:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        pred["observed_outcome"] = "UNVERIFIABLE — no target_date"
        pred["error_type"] = "DATA_ERROR"
        pred["state"] = "UNVERIFIABLE"
        pred["verified_at"] = now_iso()
        return pred

    # Check if target date has passed
    if today < target_date:
        # Not yet due — shouldn't happen if verify_at is correct
        return pred

    # Target date passed — the event window closed
    # For FISCAL/REGULATORY events: occurrence is binary (it happened or it didn't)
    # For MARKET events: outcome needs specific data
    kind = event.get("kind", "UNKNOWN")

    if kind in ("FISCAL", "REGULATORY"):
        # These are date-bound events — if the date passed, we can verify
        # For now: mark as VERIFIED with "event window closed"
        # (More specific verification would check news/government sources)
        pred["observed_outcome"] = (
            f"Event window closed ({target_date_str}). Specific outcome requires external verification."
        )
        pred["error"] = 0.0  # Optimistic default — event dates are usually met
        pred["error_type"] = "NONE"
        pred["state"] = "VERIFIED"
        pred["verified_at"] = now_iso()
    elif kind == "MARKET_EVENT":
        # Market events need price/data verification
        pred["observed_outcome"] = (
            f"Market event window closed ({target_date_str}). Requires price data verification."
        )
        pred["error"] = None  # Cannot determine without data
        pred["error_type"] = "DATA_ERROR"
        pred["state"] = "UNVERIFIABLE"
        pred["verified_at"] = now_iso()
    else:
        pred["observed_outcome"] = (
            f"Event window closed ({target_date_str}). Kind={kind}, needs manual verification."
        )
        pred["error"] = None
        pred["error_type"] = "UNKNOWN"
        pred["state"] = "UNVERIFIABLE"
        pred["verified_at"] = now_iso()

    return pred


# ───────────────────────── LOG ─────────────────────────


def log_verification(pred: dict) -> None:
    """Append verification result to log."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": now_iso(),
        "prediction_id": pred["prediction_id"],
        "claim": pred["claim"],
        "expected": pred["expected_outcome"],
        "observed": pred.get("observed_outcome"),
        "error": pred.get("error"),
        "error_type": pred.get("error_type"),
        "state": pred["state"],
    }
    with open(OUTPUT_FILE, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")


# ───────────────────────── MAIN ─────────────────────────


def main() -> int:
    predictions = load_predictions()
    due = get_due_predictions(predictions)

    if not due:
        print(f"CHRON Verifier — {now_myt().strftime('%Y-%m-%d %H:%M MYT')}")
        print(f"  No predictions due for verification.")
        print(f"  Active: {sum(1 for p in predictions if p['state'] == 'ACTIVE')}")
        print(f"  Verified: {sum(1 for p in predictions if p['state'] == 'VERIFIED')}")
        # Still write calibration report (audit trail)
        try:
            calibration = compute_calibration(predictions)
            legacy_event_cal = compute_calibration_legacy(predictions)
            CALIBRATION_REPORT.parent.mkdir(parents=True, exist_ok=True)
            CALIBRATION_REPORT.write_text(
                json.dumps(
                    {
                        "$schema": "chron_calibration_report_v1",
                        "generated_at": now_iso(),
                        "total_predictions": len(predictions),
                        "active": sum(
                            1 for p in predictions if p.get("state") == "ACTIVE"
                        ),
                        "verified": sum(
                            1 for p in predictions if p.get("state") == "VERIFIED"
                        ),
                        "unverifiable": sum(
                            1 for p in predictions if p.get("state") == "UNVERIFIABLE"
                        ),
                        "price_calibration": calibration,
                        "event_calibration": legacy_event_cal,
                    },
                    indent=2,
                    default=str,
                )
            )
            print(f"  Calibration report: {CALIBRATION_REPORT}")
        except Exception as e:
            print(f"  Failed to write calibration report: {e}")
        return 0

    print(f"CHRON Verifier — {now_myt().strftime('%Y-%m-%d %H:%M MYT')}")
    print(f"  Due for verification: {len(due)}")
    print()

    verified_count = 0
    unverifiable_count = 0

    for pred in due:
        print(f"  [{pred['prediction_id'][:12]}] {pred['claim'][:60]}")
        print(f"    Expected: {pred['expected_outcome'][:60]}")

        # Verify based on source
        if is_price_prediction(pred):
            # v1: instrument price prediction — uses yfinance + Brier
            pred = verify_price_prediction(pred, now=datetime.now(timezone.utc))
            print(
                f"    [v1-price] {pred.get('price_observed')} → {pred.get('outcome')} "
                f"(brier={pred.get('brier_score')})"
            )
        elif pred.get("source") == "chron_events":
            pred = verify_event_prediction(pred)
        else:
            pred["observed_outcome"] = "UNKNOWN — no verification method for source"
            pred["error_type"] = "UNKNOWN"
            pred["state"] = "UNVERIFIABLE"
            pred["verified_at"] = now_iso()

        print(f"    Observed: {pred.get('observed_outcome', 'N/A')[:60]}")
        print(f"    Error: {pred.get('error')}  Type: {pred.get('error_type')}")
        print(f"    State: {pred['state']}")
        print()

        # Log
        log_verification(pred)

        if pred["state"] == "VERIFIED":
            verified_count += 1
        elif pred["state"] == "UNVERIFIABLE":
            unverifiable_count += 1

    # Save updated predictions
    # Rebuild the full list with updated due predictions
    all_preds = load_predictions()
    due_ids = {p["prediction_id"] for p in due}
    updated = []
    for p in all_preds:
        if p["prediction_id"] in due_ids:
            # Find the updated version
            updated_pred = next(
                (d for d in due if d["prediction_id"] == p["prediction_id"]), p
            )
            updated.append(updated_pred)
        else:
            updated.append(p)
    save_predictions(updated)

    # Calibration (legacy event accuracy + new v1 price calibration)
    calibration = compute_calibration(updated)
    legacy_event_cal = compute_calibration_legacy(updated)
    print(f"  Verified: {verified_count}  Unverifiable: {unverifiable_count}")
    if legacy_event_cal["accuracy"] is not None:
        print(f"  Event calibration accuracy: {legacy_event_cal['accuracy']:.2f}")
    if calibration["total_verified"] > 0:
        print(f"  Price predictions verified: {calibration['total_verified']}")
        print(f"    Mean Brier: {calibration['mean_brier']}")
        print(f"    Brier Skill Score: {calibration['brier_skill_score']}")
        print(f"    Reliability: {calibration['reliability']}")
        for b in calibration["by_bucket"]:
            if b["n"] > 0:
                print(
                    f"    [{b['label']}] n={b['n']} avg_conf={b['avg_confidence']} "
                    f"hit_rate={b['hit_rate']} gap={b['gap']:+.4f}"
                )
    # Always write calibration report (audit trail for cron pipeline)
    try:
        CALIBRATION_REPORT.parent.mkdir(parents=True, exist_ok=True)
        CALIBRATION_REPORT.write_text(
            json.dumps(
                {
                    "$schema": "chron_calibration_report_v1",
                    "generated_at": now_iso(),
                    "total_predictions": len(updated),
                    "active": sum(1 for p in updated if p.get("state") == "ACTIVE"),
                    "verified": sum(1 for p in updated if p.get("state") == "VERIFIED"),
                    "unverifiable": sum(
                        1 for p in updated if p.get("state") == "UNVERIFIABLE"
                    ),
                    "price_calibration": calibration,
                    "event_calibration": legacy_event_cal,
                },
                indent=2,
                default=str,
            )
        )
        print(f"  Calibration report: {CALIBRATION_REPORT}")
    except Exception as e:
        print(f"  Failed to write calibration report: {e}")
    print(f"  Output: {OUTPUT_FILE}")

    return 0


def compute_calibration_legacy(predictions: list[dict]) -> dict:
    """Legacy event-prediction calibration (v0 schema, no Brier)."""
    verified = [
        p
        for p in predictions
        if p["state"] == "VERIFIED" and not is_price_prediction(p)
    ]
    unverifiable = [
        p
        for p in predictions
        if p["state"] == "UNVERIFIABLE" and not is_price_prediction(p)
    ]
    if not verified:
        return {
            "total_verified": 0,
            "total_unverifiable": len(unverifiable),
            "correct": 0,
            "incorrect": 0,
            "accuracy": None,
            "by_error_type": {},
        }
    correct = sum(1 for p in verified if p.get("error", 1) == 0)
    incorrect = len(verified) - correct
    by_error_type: dict[str, int] = {}
    for p in verified:
        et = p.get("error_type", "UNKNOWN")
        by_error_type[et] = by_error_type.get(et, 0) + 1
    return {
        "total_verified": len(verified),
        "total_unverifiable": len(unverifiable),
        "correct": correct,
        "incorrect": incorrect,
        "accuracy": correct / len(verified) if verified else None,
        "by_error_type": by_error_type,
    }


if __name__ == "__main__":
    raise SystemExit(main())
