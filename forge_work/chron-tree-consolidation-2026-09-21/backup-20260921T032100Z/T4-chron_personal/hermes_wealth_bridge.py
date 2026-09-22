#!/usr/bin/env python3
"""HERMES → WEALTH Bridge: PLAUSIBLE/CLAIM signals → MacroObservation injection.

Per CHRON × WEALTH × HERMES synthesis 2026-09-18:
- HERMES classifies social posts via signal_schema.py (EvidenceStatus)
- Only PLAUSIBLE/CLAIM signals enter the macro diagnosis pipeline
- Topic→channel mapping routes signals to the right transmission channel
- Each signal adjusts DiagnosisStatement confidence ±0.10 based on alignment
  (aligned → +0.10 confidence; contrary → -0.10)

This module is the CONSUMER. It does not classify HERMES signals.
HERMES classifies; WEALTH consumes.

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

MYT = timezone(timedelta(hours=8))

# Default locations
SIGNALS_JSONL = Path("/root/hermes-social/data/signals.jsonl")
SIGNALS_CLASSIFIED_JSONL = Path("/root/hermes-social/data/signals.classified.jsonl")
OBSERVATIONS_JSONL = Path(
    "/root/.hermes/cron/state/chron_personal/hermes_observations.jsonl"
)
ADJUSTMENTS_JSONL = Path(
    "/root/.hermes/cron/state/chron_personal/diagnosis_adjustments.jsonl"
)

# Acceptable evidence statuses — the constitutional gate
ACCEPTABLE_STATUSES = {"PLAUSIBLE", "CLAIM"}

# ── Topic → Channel mapping (deterministic, rule-based) ──────

TOPIC_CHANNEL_RULES: list[tuple[str, str]] = [
    # Order matters: first match wins
    ("opec", "fiscal_energy"),
    ("brent", "fiscal_energy"),
    ("wti", "fiscal_energy"),
    ("crude", "fiscal_energy"),
    ("lng", "fiscal_energy"),
    ("jcc", "fiscal_energy"),
    ("petronas", "fiscal_energy"),
    ("oil", "fiscal_energy"),
    ("gold", "fiscal_energy"),
    ("xauusd", "fiscal_energy"),
    ("iran", "fiscal_energy"),
    ("saudi", "fiscal_energy"),
    ("hormuz", "fiscal_energy"),
    ("war", "fiscal_energy"),
    ("geopol", "fiscal_energy"),
    ("fed", "currency"),
    ("fomc", "currency"),
    ("dxy", "currency"),
    ("usd", "currency"),
    ("dollar", "currency"),
    ("bnm", "currency"),
    ("opr", "currency"),
    ("myr", "currency"),
    ("ringgit", "currency"),
    ("asean", "currency"),
    ("sgd", "currency"),
    ("idr", "currency"),
    ("php", "currency"),
    ("regional", "currency"),
    ("fx", "currency"),
    ("klci", "growth"),
    ("fbm", "growth"),
    ("bursa", "growth"),
    ("equity", "growth"),
    ("china", "growth"),
    ("pmi", "growth"),
    ("exports", "growth"),
    ("cpi", "inflation"),
    ("ppi", "inflation"),
    ("inflation", "inflation"),
    ("subsidy", "inflation"),
    ("fuel", "inflation"),
]

DEFAULT_CHANNEL = "currency"  # most market signals route through currency


def map_topics_to_channel(topics: list[str], excerpt: str = "") -> str:
    """Map signal topics to a WEALTH transmission channel.

    Returns one of: fiscal_energy, currency, growth, inflation, unknown.
    """
    hay = " ".join([*topics, excerpt or ""]).lower()
    for kw, channel in TOPIC_CHANNEL_RULES:
        if kw in hay:
            return channel
    return "unknown"


# ── Sentiment alignment (supportive vs contrary) ──────────────

# Words that signal "supporting the diagnosis" (rising, hawkish, tight, etc.)
SUPPORTIVE_KEYWORDS = {
    "rising",
    "rally",
    "surge",
    "gain",
    "strengthen",
    "up",
    "hike",
    "hike",
    "increases",
    "expanded",
    "expansion",
    "boost",
    "strong",
    "tight",
    "elevated",
    "above",
    "firm",
    "bid",
    "demand",
    "increase",
}
# Words that signal "contrary to the diagnosis" (falling, dovish, loose, etc.)
CONTRARY_KEYWORDS = {
    "falling",
    "drop",
    "plunge",
    "weaken",
    "weakening",
    "down",
    "cut",
    "decrease",
    "decline",
    "loose",
    "easing",
    "below",
    "weak",
    "low",
    "soft",
    "reversal",
    "loss",
    "shrinking",
    "shrink",
    "fear",
    "risk-off",
    "sell-off",
    "selloff",
    "fears",
}


def detect_signal_direction(signal: dict) -> str:
    """Return 'supportive' | 'contrary' | 'neutral' based on signal text."""
    text = " ".join(
        [
            signal.get("content_excerpt", "") or "",
            signal.get("summary_bm_en", "") or "",
        ]
    ).lower()

    supportive = sum(1 for w in SUPPORTIVE_KEYWORDS if w in text)
    contrary = sum(1 for w in CONTRARY_KEYWORDS if w in text)

    if supportive > contrary:
        return "supportive"
    if contrary > supportive:
        return "contrary"
    return "neutral"


def detect_diagnosis_direction(diagnosis: dict) -> str:
    """Best-effort: extract direction of a WEALTH DiagnosisStatement."""
    text = (diagnosis.get("statement", "") or "").lower()
    # "may strengthen", "may weaken", "supports", "favourable"
    supportive = sum(1 for w in SUPPORTIVE_KEYWORDS if w in text)
    contrary = sum(1 for w in CONTRARY_KEYWORDS if w in text)
    if supportive > contrary:
        return "supportive"
    if contrary > supportive:
        return "contrary"
    return "neutral"


def compute_confidence_delta(signal_direction: str, diagnosis_direction: str) -> float:
    """Compute confidence adjustment for a diagnosis based on signal alignment.

    Per synthesis: PLAUSIBLE signal aligned WITH diagnosis → +0.10.
    PLAUSIBLE signal aligned AGAINST diagnosis → -0.10.
    Neutral / unknown → 0.0.
    """
    if signal_direction == "neutral" or diagnosis_direction == "neutral":
        return 0.0
    if signal_direction == diagnosis_direction:
        return +0.10
    return -0.10


# ── Bridge: Signal → MacroObservation ──────────────────────────


def load_signals(
    path: Path = SIGNALS_JSONL,
    since: Optional[datetime] = None,
    prefer_classified: bool = True,
) -> list[dict]:
    """Load signals from jsonl store.

    If `prefer_classified` and signals.classified.jsonl exists, read it instead
    (it carries classification verdicts in `_classification` and may have
    elevated evidence_status). Falls back to raw signals.jsonl otherwise.

    Filters to those newer than `since` if provided.
    """
    # Prefer classified if available
    if (
        prefer_classified
        and SIGNALS_CLASSIFIED_JSONL.exists()
        and path == SIGNALS_JSONL
    ):
        path = SIGNALS_CLASSIFIED_JSONL

    if not path.exists():
        return []
    signals = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                s = json.loads(line)
            except json.JSONDecodeError:
                continue
            if since is not None:
                try:
                    obs = datetime.fromisoformat(
                        s.get("observed_at", "").replace("Z", "+00:00")
                    )
                    if obs < since:
                        continue
                except Exception:
                    pass
            signals.append(s)
    return signals


def filter_actionable(signals: list[dict]) -> list:
    """Filter signals to PLAUSIBLE/CLAIM only."""
    return [s for s in signals if s.get("evidence_status") in ACCEPTABLE_STATUSES]


def signal_to_macro_observation(signal: dict) -> dict:
    """Convert a HERMES Signal into a WEALTH MacroObservation dict.

    Preserves provenance, topic→channel mapping, excerpt as the "value".
    """
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    topics = signal.get("topics", []) or []
    excerpt = signal.get("content_excerpt", "") or ""
    summary = signal.get("summary_bm_en", "") or ""

    channel = map_topics_to_channel(topics, f"{excerpt} {summary}")
    direction = detect_signal_direction(signal)

    # Extract a numeric "value" where possible (price quotes in excerpt)
    # Otherwise treat the excerpt as qualitative evidence
    value: str | float | None = None
    price_match = re.search(r"\$?\s*(\d{3,5}(?:[.,]\d{1,3})?)", excerpt)
    if price_match:
        try:
            value = float(price_match.group(1).replace(",", ""))
        except ValueError:
            value = excerpt[:200]

    if value is None:
        value = excerpt[:200]

    return {
        "value": value,
        "observation_period": signal.get("observed_at", "")[:10],  # YYYY-MM-DD
        "published_at": signal.get("observed_at", ""),
        "fetched_at": now,
        "source": f"hermes:{signal.get('platform', 'unknown')}:{signal.get('signal_id', '')}",
        "freshness": "CURRENT",
        "revision_status": "preliminary",
        "_class": "OBSERVED",
        "_meta": {
            "signal_id": signal.get("signal_id"),
            "author_handle": signal.get("author_handle", ""),
            "platform": signal.get("platform", ""),
            "source_url": signal.get("source_url", ""),
            "evidence_status": signal.get("evidence_status", "UNKNOWN"),
            "channel": channel,
            "direction": direction,
            "relevance_score": signal.get("relevance_score"),
            "novelty_score": signal.get("novelty_score"),
            "language": signal.get("language", ""),
            "topics": topics,
        },
    }


def apply_signal_to_diagnoses(
    signal: dict, diagnoses: list[dict], observation: dict
) -> list[dict]:
    """Apply a signal's confidence adjustment to matching diagnoses.

    A diagnosis is "matching" if:
    - Same transmission channel (or one of them is 'unknown'), AND
    - Diagnosis direction aligns (or is 'neutral')

    Returns the list of diagnoses with adjusted confidence + audit trail.
    """
    sig_channel = observation["_meta"]["channel"]
    sig_dir = observation["_meta"]["direction"]

    adjusted = []
    for diag in diagnoses:
        d_channel = diag.get("channel", "unknown")
        d_dir = detect_diagnosis_direction(diag)

        # Channel match: both must be known and equal.
        # If signal channel is unknown (no topic matched), do NOT route it anywhere — fail-closed.
        # If diagnosis channel is unknown, do NOT adjust it — fail-closed.
        channel_match = (
            sig_channel != "unknown"
            and d_channel != "unknown"
            and sig_channel == d_channel
        )

        if channel_match:
            delta = compute_confidence_delta(sig_dir, d_dir)
            if delta != 0.0:
                new_d = dict(diag)
                new_d["confidence"] = round(
                    min(1.0, max(0.0, diag.get("confidence", 0.5) + delta)), 2
                )
                new_d["_adjustment"] = {
                    "delta": delta,
                    "reason": f"hermes:{sig_channel}:{sig_dir} vs diag:{d_channel}:{d_dir}",
                    "signal_id": observation["_meta"]["signal_id"],
                    "applied_at": datetime.now(timezone.utc)
                    .isoformat()
                    .replace("+00:00", "Z"),
                }
                adjusted.append(new_d)
                continue
        adjusted.append(diag)
    return adjusted


# ── Audit trail writers ────────────────────────────────────────


def append_observation(observation: dict, path: Path = OBSERVATIONS_JSONL) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(observation, default=str) + "\n")


def append_adjustment(adjustment: dict, path: Path = ADJUSTMENTS_JSONL) -> None:
    """Append a single adjustment record: signal_id, diagnosis_id, channel, delta, applied."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(adjustment, default=str) + "\n")


# ── Main bridge run ────────────────────────────────────────────


def bridge_run(
    signals_path: Path = SIGNALS_JSONL,
    diagnoses: Optional[list[dict]] = None,
    since: Optional[datetime] = None,
    output_observations: Path = OBSERVATIONS_JSONL,
    output_adjustments: Path = ADJUSTMENTS_JSONL,
    write_outputs: bool = True,
) -> dict:
    """One-shot HERMES → WEALTH bridge run.

    Returns:
      {
        "signals_total": int,
        "signals_filtered": int,
        "signals_filtered_out": int,
        "observations_emitted": int,
        "adjustments_applied": int,
        "observations": [list of MacroObservation dicts],
        "adjustments": [list of adjustment dicts]
      }
    """
    all_signals = load_signals(signals_path, since=since)
    actionable = filter_actionable(all_signals)

    observations = []
    adjustments = []

    for signal in actionable:
        obs = signal_to_macro_observation(signal)
        observations.append(obs)

        if write_outputs:
            append_observation(obs, output_observations)

        # Apply to diagnoses if provided
        if diagnoses:
            channel = obs["_meta"]["channel"]
            direction = obs["_meta"]["direction"]
            for diag in diagnoses:
                d_channel = diag.get("channel", "unknown")
                d_dir = detect_diagnosis_direction(diag)
                # Fail-closed: both channels must be known and equal.
                if (
                    channel != "unknown"
                    and d_channel != "unknown"
                    and channel == d_channel
                ):
                    delta = compute_confidence_delta(direction, d_dir)
                    if delta != 0.0:
                        diag_id = diag.get("statement", "")[:60]
                        adjustments.append(
                            {
                                "signal_id": obs["_meta"]["signal_id"],
                                "diagnosis_id": diag_id,
                                "channel": channel,
                                "signal_direction": direction,
                                "diagnosis_direction": d_dir,
                                "delta": delta,
                                "applied_at": obs["fetched_at"],
                            }
                        )
                        if write_outputs:
                            append_adjustment(adjustments[-1], output_adjustments)

    return {
        "signals_total": len(all_signals),
        "signals_filtered": len(actionable),
        "signals_filtered_out": len(all_signals) - len(actionable),
        "observations_emitted": len(observations),
        "adjustments_applied": len(adjustments),
        "observations": observations,
        "adjustments": adjustments,
    }


# ── CLI ────────────────────────────────────────────────────────


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        description="HERMES → WEALTH bridge (PLAUSIBLE/CLAIM → MacroObservation)"
    )
    ap.add_argument(
        "--signals",
        type=str,
        default=str(SIGNALS_JSONL),
        help="Path to HERMES signals.jsonl",
    )
    ap.add_argument(
        "--since-hours",
        type=int,
        default=24,
        help="Only process signals newer than N hours",
    )
    ap.add_argument(
        "--diagnoses",
        type=str,
        default=None,
        help="Path to JSON file with WEALTH diagnoses list (optional)",
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="Compute but don't write outputs"
    )
    ap.add_argument("--quiet", action="store_true", help="Less output")
    args = ap.parse_args()

    since = datetime.now(timezone.utc) - timedelta(hours=args.since_hours)
    diagnoses = None
    if args.diagnoses:
        with open(args.diagnoses) as f:
            d = json.load(f)
            diagnoses = d.get("interpretations", d) if isinstance(d, dict) else d

    result = bridge_run(
        signals_path=Path(args.signals),
        diagnoses=diagnoses,
        since=since,
        write_outputs=not args.dry_run,
    )

    if not args.quiet:
        print(
            f"HERMES → WEALTH bridge — {datetime.now(MYT).strftime('%Y-%m-%d %H:%M MYT')}"
        )
        print(f"  Signals total: {result['signals_total']}")
        print(
            f"  Filtered to actionable (PLAUSIBLE/CLAIM): {result['signals_filtered']}"
        )
        print(
            f"  Filtered out (UNKNOWN/HYPOTHESIS/ESTIMATE): {result['signals_filtered_out']}"
        )
        print(f"  MacroObservations emitted: {result['observations_emitted']}")
        print(f"  Diagnosis adjustments applied: {result['adjustments_applied']}")
        if result["signals_total"] == 0:
            print(
                f"  NOTE: No signals found. If HERMES is operational, check {SIGNALS_JSONL}."
            )
            print(
                f"  Operational gap: signals require classification to PLAUSIBLE/CLAIM before injection."
            )
        if args.dry_run:
            print(f"  [dry-run] no files written")
        else:
            print(f"  Output: {OBSERVATIONS_JSONL}")
            if result["adjustments_applied"] > 0:
                print(f"  Output: {ADJUSTMENTS_JSONL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
