#!/usr/bin/env python3
"""CHRON Price Predictions — schema v1 + price verifier + Brier scoring.

Adds per-instrument price predictions to CHRON's prediction store. Additive
extension to chron_predictions_v0 (event predictions). v0 records remain valid;
v1 records add instrument/prediction_type/direction/threshold/horizon_sessions
and resolve with real prices via yfinance, producing Brier scores.

Brier score = (confidence - outcome)² for binary outcomes (HIT=1, MISS=0).
- Perfect calibration → 0.0 (predicted 0.7 hits 70% of the time)
- Always wrong with confidence=1 → 1.0
- Climatology (0.5 baseline) → 0.25

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import json
import math
import statistics
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

MYT = timezone(timedelta(hours=8))

# ── Instrument registry ─────────────────────────────────────────
# Canonical instrument → yfinance ticker. Single SOT for price lookup.
INSTRUMENT_TICKERS: dict[str, dict] = {
    "XAUUSD": {
        "ticker": "GC=F",
        "name": "Gold Futures (USD/oz)",
        "category": "metal",
        "decimal_places": 2,
        "source": "yfinance:GC=F",
    },
    "OIL": {
        "ticker": "CL=F",
        "name": "WTI Crude Futures (USD/bbl)",
        "category": "energy",
        "decimal_places": 2,
        "source": "yfinance:CL=F",
    },
    "GAS": {
        "ticker": "NG=F",
        "name": "Natural Gas Futures (USD/MMBtu)",
        "category": "energy",
        "decimal_places": 3,
        "source": "yfinance:NG=F",
    },
    "KLCI": {
        "ticker": "^KLSE",
        "name": "FTSE Bursa Malaysia KLCI",
        "category": "equity_index",
        "decimal_places": 2,
        "source": "yfinance:^KLSE",
    },
    "USMYR": {
        "ticker": "MYR=X",
        "name": "USD/MYR",
        "category": "fx",
        "decimal_places": 4,
        "source": "yfinance:MYR=X",
    },
}


def is_valid_instrument(instrument: str) -> bool:
    return instrument in INSTRUMENT_TICKERS


def ticker_for(instrument: str) -> str:
    if not is_valid_instrument(instrument):
        raise ValueError(
            f"Unknown instrument: {instrument}. Valid: {list(INSTRUMENT_TICKERS.keys())}"
        )
    return INSTRUMENT_TICKERS[instrument]["ticker"]


# ── Schema v1 ──────────────────────────────────────────────────

SCHEMA_V1 = "chron_predictions_v1"

# Calibration buckets (lower-inclusive, upper-exclusive except final)
CALIBRATION_BUCKETS = [
    (0.0, 0.2, "very_low"),
    (0.2, 0.4, "low"),
    (0.4, 0.6, "medium"),
    (0.6, 0.8, "high"),
    (0.8, 1.01, "very_high"),  # 1.01 to include 1.0
]


def calibration_bucket(confidence: float) -> tuple[float, float, str]:
    """Return (lo, hi, label) bucket for a confidence value."""
    for lo, hi, label in CALIBRATION_BUCKETS:
        if lo <= confidence < hi:
            return lo, hi, label
    return 0.8, 1.01, "very_high"


@dataclass
class PricePredictionFields:
    """Schema v1 additions for price predictions.

    All fields optional on the record; presence implies prediction_type=='price'.
    """

    instrument: str = ""
    prediction_type: str = "price"  # 'event' | 'price'
    direction: str = "up"  # 'up' | 'down' | 'range'
    threshold: float = 0.0
    horizon_sessions: int = 5
    baseline_price: Optional[float] = None
    baseline_date: str = ""
    regime_context: str = "UNKNOWN"  # UPTREND | DOWNTREND | SIDEWAYS | UNKNOWN
    macro_context: dict = field(default_factory=dict)
    check_window_max: bool = False  # if True, check max/min within horizon
    # Resolved by verifier:
    price_observed: Optional[float] = None
    price_observed_at: str = ""
    price_source: str = ""
    price_data_quality: str = "UNKNOWN"  # CURRENT | STALE | UNAVAILABLE
    outcome: str = "PENDING"  # HIT | MISS | PENDING
    brier_score: Optional[float] = None


def is_price_prediction(pred: dict) -> bool:
    """Return True if record is a v1 price prediction (or has price fields)."""
    if pred.get("prediction_type") == "price":
        return True
    return bool(pred.get("instrument")) and is_valid_instrument(
        pred.get("instrument", "")
    )


# ── Price fetching ─────────────────────────────────────────────


def fetch_price_at_or_after(instrument: str, target_date: str) -> Optional[dict]:
    """Fetch price for instrument at or after target_date (ISO date or datetime).

    Returns dict with price, observed_at, source, or None if unavailable.
    Uses yfinance with a 7-day look-forward to handle weekends/holidays.
    """
    try:
        import yfinance as yf
    except ImportError:
        return None

    ticker = ticker_for(instrument)
    info = INSTRUMENT_TICKERS[instrument]

    # Parse target_date
    try:
        if "T" in target_date:
            dt = datetime.fromisoformat(target_date.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(target_date).replace(tzinfo=timezone.utc)
    except Exception:
        return None

    # Look-forward 7 calendar days to handle weekends
    start = dt.date()
    end_date = (dt + timedelta(days=7)).date()
    end_inclusive = (end_date + timedelta(days=1)).isoformat()

    try:
        df = yf.download(
            ticker,
            start=start.isoformat(),
            end=end_inclusive,
            progress=False,
            auto_adjust=True,
        )
    except Exception:
        return None

    if df is None or df.empty:
        return None

    # Get first available close after target_date
    # yfinance may return MultiIndex columns (Price, Ticker) on some versions
    row = df.iloc[0]
    if isinstance(df.columns, __import__("pandas").MultiIndex):
        close = float(row[("Close", ticker)])
    else:
        close = float(row["Close"])
    idx = df.index[0]
    observed_at = (
        idx.to_pydatetime() if hasattr(idx, "to_pydatetime") else idx
    ).replace(tzinfo=timezone.utc)

    return {
        "instrument": instrument,
        "ticker": ticker,
        "price": round(close, info["decimal_places"]),
        "observed_at": observed_at.isoformat().replace("+00:00", "Z"),
        "source": info["source"],
        "currency": "USD",
    }


def fetch_price_history(instrument: str, start: str, end: str) -> list[dict]:
    """Fetch daily closes between start and end (inclusive). For window checks."""
    try:
        import yfinance as yf
    except ImportError:
        return []

    ticker = ticker_for(instrument)
    info = INSTRUMENT_TICKERS[instrument]

    try:
        df = yf.download(
            ticker,
            start=start,
            end=(datetime.fromisoformat(end) + timedelta(days=1)).date().isoformat(),
            progress=False,
            auto_adjust=True,
        )
    except Exception:
        return []

    if df is None or df.empty:
        return []

    return [
        {
            "date": (idx.to_pydatetime() if hasattr(idx, "to_pydatetime") else idx)
            .date()
            .isoformat(),
            "close": round(
                float(
                    row[("Close", ticker)]
                    if isinstance(df.columns, __import__("pandas").MultiIndex)
                    else row["Close"]
                ),
                info["decimal_places"],
            ),
        }
        for idx, row in df.iterrows()
    ]


# ── Outcome evaluation ──────────────────────────────────────────


def evaluate_outcome(direction: str, threshold: float, prices: list[float]) -> bool:
    """Evaluate whether a price prediction hits.

    direction='up': HIT if any price >= threshold (or max price >= threshold for window)
    direction='down': HIT if any price <= threshold
    direction='range': HIT if min >= lower AND max <= upper (threshold = upper, lower derived?)

    Returns True for HIT.
    """
    if not prices:
        return False

    if direction == "up":
        return max(prices) >= threshold
    if direction == "down":
        return min(prices) <= threshold
    if direction == "range":
        # threshold interpreted as upper bound; lower = baseline * 0.99 (1% band)
        # Better: store band_low and band_high separately. For MVP, range not seeded.
        return min(prices) >= threshold * 0.99 and max(prices) <= threshold
    return False


# ── Brier scoring ──────────────────────────────────────────────


def brier_score(confidence: float, outcome: int) -> float:
    """Brier score for a single binary prediction.

    Brier = (confidence - outcome)² where outcome ∈ {0, 1}.
    """
    if not 0.0 <= confidence <= 1.0:
        raise ValueError(f"confidence must be in [0,1], got {confidence}")
    if outcome not in (0, 1):
        raise ValueError(f"outcome must be 0 or 1, got {outcome}")
    return (confidence - outcome) ** 2


def brier_skill_score(mean_brier: float, climatology: float = 0.5) -> Optional[float]:
    """Brier Skill Score vs climatology baseline.

    BSS = 1 - brier / brier_climatology
    > 0: better than baseline, < 0: worse. None if brier_climatology is 0.
    """
    brier_clim = climatology * (1 - climatology)  # variance of base rate
    if brier_clim == 0:
        return None
    return 1.0 - mean_brier / brier_clim


# ── Calibration aggregation ────────────────────────────────────


def compute_calibration(predictions: list[dict]) -> dict:
    """Compute calibration stats over verified price predictions.

    Returns:
      {
        "total_verified": int,
        "by_bucket": [{lo, hi, label, n, avg_confidence, hit_rate, gap}, ...],
        "mean_brier": float | None,
        "brier_skill_score": float | None,
        "reliability": "WELL_CALIBRATED" | "OVERCONFIDENT" | "UNDERCONFIDENT" | "INSUFFICIENT_DATA"
      }
    """
    verified_price = [
        p
        for p in predictions
        if is_price_prediction(p)
        and p.get("outcome") in ("HIT", "MISS")
        and p.get("brier_score") is not None
    ]

    if not verified_price:
        return {
            "total_verified": 0,
            "by_bucket": [],
            "mean_brier": None,
            "brier_skill_score": None,
            "reliability": "INSUFFICIENT_DATA",
        }

    # Bucket
    by_bucket: dict[str, dict] = {}
    for lo, hi, label in CALIBRATION_BUCKETS:
        by_bucket[label] = {
            "lo": lo,
            "hi": hi,
            "label": label,
            "predictions": [],
        }

    for p in verified_price:
        conf = float(p["confidence"])
        hit = 1 if p["outcome"] == "HIT" else 0
        lo, hi, label = calibration_bucket(conf)
        by_bucket[label]["predictions"].append({"conf": conf, "hit": hit})

    # Aggregate per bucket
    bucket_summary = []
    for label, b in by_bucket.items():
        n = len(b["predictions"])
        if n == 0:
            bucket_summary.append(
                {
                    "lo": b["lo"],
                    "hi": b["hi"],
                    "label": label,
                    "n": 0,
                    "avg_confidence": None,
                    "hit_rate": None,
                    "gap": None,
                }
            )
        else:
            avg_conf = sum(x["conf"] for x in b["predictions"]) / n
            hit_rate = sum(x["hit"] for x in b["predictions"]) / n
            gap = avg_conf - hit_rate  # positive = overconfident
            bucket_summary.append(
                {
                    "lo": b["lo"],
                    "hi": b["hi"],
                    "label": label,
                    "n": n,
                    "avg_confidence": round(avg_conf, 4),
                    "hit_rate": round(hit_rate, 4),
                    "gap": round(gap, 4),
                }
            )

    # Mean Brier
    brier_vals = [float(p["brier_score"]) for p in verified_price]
    mean_b = statistics.mean(brier_vals) if brier_vals else None

    # Hit rate as climatology proxy
    hit_count = sum(1 for p in verified_price if p["outcome"] == "HIT")
    clim = hit_count / len(verified_price) if verified_price else 0.5
    # Guard: avoid division by zero
    clim = min(max(clim, 0.01), 0.99)

    bss = brier_skill_score(mean_b, clim) if mean_b is not None else None

    # Reliability verdict: well-calibrated if |mean gap| < 0.10
    nonzero_buckets = [b for b in bucket_summary if b["n"] > 0]
    if nonzero_buckets:
        mean_gap = statistics.mean(abs(b["gap"]) for b in nonzero_buckets)
        if mean_gap < 0.10:
            reliability = "WELL_CALIBRATED"
        elif mean_gap > 0:
            # Sign matters: if positive, overconfident; negative, underconfident
            sign = statistics.mean(b["gap"] for b in nonzero_buckets)
            reliability = "OVERCONFIDENT" if sign > 0 else "UNDERCONFIDENT"
        else:
            reliability = "INSUFFICIENT_DATA"
    else:
        reliability = "INSUFFICIENT_DATA"

    return {
        "total_verified": len(verified_price),
        "total_hits": hit_count,
        "total_misses": len(verified_price) - hit_count,
        "by_bucket": bucket_summary,
        "mean_brier": round(mean_b, 4) if mean_b is not None else None,
        "brier_skill_score": round(bss, 4) if bss is not None else None,
        "climatology_estimate": round(clim, 4),
        "reliability": reliability,
    }


# ── Price verification ────────────────────────────────────────


def verify_price_prediction(pred: dict, now: Optional[datetime] = None) -> dict:
    """Resolve a v1 price prediction against current/marked price data.

    Returns the updated prediction dict with outcome/brier/price fields set.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    instrument = pred.get("instrument", "")
    if not is_valid_instrument(instrument):
        pred["state"] = "UNVERIFIABLE"
        pred["observed_outcome"] = f"Unknown instrument: {instrument}"
        pred["error_type"] = "DATA_ERROR"
        pred["verified_at"] = now.isoformat().replace("+00:00", "Z")
        pred["outcome"] = "PENDING"
        return pred

    direction = pred.get("direction", "up")
    threshold = float(pred.get("threshold", 0))
    check_max = bool(pred.get("check_window_max", False))
    verify_at = pred.get("verify_at", "")

    if check_max and pred.get("created_at"):
        # Window check: created_at to verify_at (or now)
        try:
            start_dt = datetime.fromisoformat(pred["created_at"].replace("Z", "+00:00"))
            end_dt = (
                now
                if not verify_at
                else datetime.fromisoformat(verify_at.replace("Z", "+00:00"))
            )
            if end_dt < start_dt:
                end_dt = now
            start_s = start_dt.date().isoformat()
            end_s = end_dt.date().isoformat()
            history = fetch_price_history(instrument, start_s, end_s)
            if not history:
                pred["state"] = "UNVERIFIABLE"
                pred["observed_outcome"] = (
                    f"No price data between {start_s} and {end_s}"
                )
                pred["error_type"] = "DATA_ERROR"
                pred["price_data_quality"] = "UNAVAILABLE"
                pred["verified_at"] = now.isoformat().replace("+00:00", "Z")
                return pred
            prices = [h["close"] for h in history]
            observed_price = prices[-1]  # last close = reference for reporting
            observed_at = end_s + "T00:00:00Z"
            pred["price_data_quality"] = "CURRENT"
        except Exception as e:
            pred["state"] = "UNVERIFIABLE"
            pred["observed_outcome"] = f"Window fetch error: {e}"
            pred["error_type"] = "DATA_ERROR"
            pred["verified_at"] = now.isoformat().replace("+00:00", "Z")
            return pred
    else:
        # Single-point check at verify_at (or now if verify_at is past)
        target = verify_at if verify_at else now.isoformat()
        result = fetch_price_at_or_after(instrument, target)
        if result is None:
            pred["state"] = "UNVERIFIABLE"
            pred["observed_outcome"] = f"No price data at or after {target}"
            pred["error_type"] = "DATA_ERROR"
            pred["price_data_quality"] = "UNAVAILABLE"
            pred["verified_at"] = now.isoformat().replace("+00:00", "Z")
            return pred
        prices = [result["price"]]
        observed_price = result["price"]
        observed_at = result["observed_at"]
        pred["price_data_quality"] = "CURRENT"
        pred["price_source"] = result["source"]

    # Set resolved
    pred["price_observed"] = observed_price
    pred["price_observed_at"] = observed_at
    if not pred.get("price_source"):
        pred["price_source"] = INSTRUMENT_TICKERS[instrument]["source"]

    # Evaluate outcome
    hit = evaluate_outcome(direction, threshold, prices)
    pred["outcome"] = "HIT" if hit else "MISS"

    # Brier
    conf = float(pred["confidence"])
    outcome_int = 1 if hit else 0
    pred["brier_score"] = round(brier_score(conf, outcome_int), 4)

    pred["observed_outcome"] = (
        f"{instrument} {direction} {threshold} → "
        f"observed={observed_price} → {pred['outcome']} (brier={pred['brier_score']})"
    )
    pred["error"] = 0.0 if hit else 1.0
    pred["error_type"] = "NONE"
    pred["state"] = "VERIFIED"
    pred["verified_at"] = now.isoformat().replace("+00:00", "Z")
    return pred


def is_due_price_prediction(pred: dict, now: Optional[datetime] = None) -> bool:
    """Return True if a price prediction's verify_at has arrived and is ACTIVE."""
    if pred.get("state") != "ACTIVE":
        return False
    if not is_price_prediction(pred):
        return False
    verify_at = pred.get("verify_at", "")
    if not verify_at:
        return False
    if now is None:
        now = datetime.now(timezone.utc)
    try:
        va = datetime.fromisoformat(verify_at.replace("Z", "+00:00"))
        return now >= va
    except Exception:
        return False
