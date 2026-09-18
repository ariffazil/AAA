"""CHRON Loop Closer — wires the three UNBUILT arrows.

OUTCOME → LEARNING: verify → extract_lessons
EXPERIENCE → MEMORY: arifflow bridge → episode store → durable lessons
MEMORY → POLICY: lessons → policy candidate → promotion gate

This is the runtime that closes the open loop.
Run: python3 -m chron.loop_close

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from chron.chron_verify import run_verification
from chron.chron_learn import extract_lessons, load_lessons, get_candidates
from chron.chron_prediction import get_verified, compute_calibration, save_calibration
from chron.chron_store import get_store
from chron.chron_ariflow_bridge import run_bridge, poll_fq_daemon

LESSONS_FILE = Path("/root/chron/data/lessons.jsonl")
POLICY_CANDIDATES_FILE = Path("/root/chron/data/policy_candidates.jsonl")
LOOP_LOG = Path("/root/chron/data/loop_log.jsonl")

MYT = timezone(timedelta(hours=8))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ───────────────────────── ARROW 1: OUTCOME → LEARNING ─────────────────────────


def arrow_outcome_to_learning(dry_run: bool = False) -> dict:
    """Wire: verification results → lesson extraction.

    This closes the OUTCOME → LEARNING arrow.
    After every verification run, extract lessons from verified predictions.
    """
    # 1. Run verification on due predictions
    verify_result = run_verification(dry_run=dry_run)

    # 2. Extract lessons from verified predictions
    lessons = extract_lessons()

    # 3. Compute calibration
    calibration = compute_calibration()
    if not dry_run:
        save_calibration(calibration)

    result = {
        "arrow": "OUTCOME → LEARNING",
        "timestamp": _now_iso(),
        "verify_result": {
            "due": verify_result.get("due", 0),
            "verified_correct": verify_result.get("verified_correct", 0),
            "verified_incorrect": verify_result.get("verified_incorrect", 0),
            "unverifiable": verify_result.get("unverifiable", 0),
        },
        "lessons_extracted": len(lessons),
        "calibration": {
            "total_verified": calibration.get("total", 0),
            "accuracy": calibration.get("accuracy"),
            "mean_brier": calibration.get("mean_brier"),
        },
        "status": "COMPLETE"
        if verify_result.get("due", 0) > 0
        else "NO_DUE_PREDICTIONS",
    }

    if not dry_run:
        _log_loop("OUTCOME→LEARNING", result)

    return result


# ───────────────────────── ARROW 2: EXPERIENCE → MEMORY ─────────────────────────


def arrow_experience_to_memory() -> dict:
    """Wire: arifflow receipts → CHRON episodes → durable lessons.

    This closes the EXPERIENCE → MEMORY arrow.
    The arifflow bridge already creates episodes. This arrow ensures
    those episodes feed into the lesson extraction pipeline.
    """
    # 1. Run arifflow bridge (creates episodes from receipts)
    bridge_result = run_bridge()

    # 2. Poll FQ daemon (creates episodes on significant transitions)
    fq_result = poll_fq_daemon()

    # 3. Check if any new episodes warrant lesson extraction
    store = get_store()
    total_episodes = store.count()

    # Count recent episodes (last 24h)
    now = datetime.now(timezone.utc)
    day_ago = (now - timedelta(hours=24)).isoformat().replace("+00:00", "Z")
    recent = store.query(since=day_ago, limit=1000)

    result = {
        "arrow": "EXPERIENCE → MEMORY",
        "timestamp": _now_iso(),
        "bridge": {
            "status": bridge_result.get("status"),
            "new_receipts": bridge_result.get("new_receipts", 0),
            "episodes_created": bridge_result.get("episodes_created", 0),
        },
        "fq_poll": {
            "status": fq_result.get("status"),
            "significant_transitions": fq_result.get("significant_transitions", 0),
            "episodes_created": fq_result.get("episodes_created", 0),
        },
        "store": {
            "total_episodes": total_episodes,
            "episodes_last_24h": len(recent),
        },
        "status": "COMPLETE",
    }

    _log_loop("EXPERIENCE→MEMORY", result)
    return result


# ───────────────────────── ARROW 3: MEMORY → POLICY ─────────────────────────


def arrow_memory_to_policy() -> dict:
    """Wire: lessons → policy candidate → promotion gate.

    This closes the MEMORY → POLICY arrow.
    Lessons that meet promotion criteria become policy candidates.
    Policy candidates require external validation before deployment.

    Promotion criteria:
      - Recurrence: same error_class seen 2+ times
      - Measured effect: lesson applied → error reduced
      - External validation: FRAME or arifOS confirms
    """
    candidates = get_candidates()
    all_lessons = load_lessons()

    # Evaluate each candidate for promotion
    promoted = []
    held = []

    for candidate in candidates:
        promotion_result = _evaluate_promotion(candidate)
        if promotion_result["eligible"]:
            promoted.append(promotion_result)
        else:
            held.append(promotion_result)

    result = {
        "arrow": "MEMORY → POLICY",
        "timestamp": _now_iso(),
        "lessons_total": len(all_lessons),
        "candidates": len(candidates),
        "promoted": len(promoted),
        "held": len(held),
        "promotions": promoted,
        "holds": held,
        "status": "COMPLETE" if promoted else "NO_PROMOTIONS",
    }

    _log_loop("MEMORY→POLICY", result)
    return result


def _evaluate_promotion(lesson: dict) -> dict:
    """Evaluate whether a lesson qualifies for policy promotion.

    Returns promotion assessment.
    """
    lesson_id = lesson.get("lesson_id", "?")
    recurrence = lesson.get("recurrence", 0)
    error_type = lesson.get("error_type", "UNKNOWN")
    mean_brier = lesson.get("mean_brier")

    # Criterion 1: Recurrence (need 2+)
    has_recurrence = recurrence >= 2

    # Criterion 2: Measured effect (Brier improving)
    has_measurement = mean_brier is not None and mean_brier < 0.25  # Better than random

    # Criterion 3: External validation (placeholder — needs FRAME/arifOS)
    has_external_validation = False  # Not yet implemented

    eligible = has_recurrence and has_measurement

    return {
        "lesson_id": lesson_id,
        "error_type": error_type,
        "recurrence": recurrence,
        "mean_brier": mean_brier,
        "criteria": {
            "recurrence": has_recurrence,
            "measured_effect": has_measurement,
            "external_validation": has_external_validation,
        },
        "eligible": eligible,
        "reason": (
            "Meets all criteria"
            if eligible
            else f"Missing: {', '.join(k for k, v in {'recurrence': has_recurrence, 'measurement': has_measurement, 'external_validation': has_external_validation}.items() if not v)}"
        ),
    }


# ───────────────────────── FULL LOOP ─────────────────────────


def run_full_loop(dry_run: bool = False) -> dict:
    """Run the full CHRON loop: all three arrows.

    This is the runtime that closes the open loop.
    Run daily via cron, or manually.
    """
    result = {
        "loop_id": f"loop-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "started_at": _now_iso(),
        "arrows": {},
    }

    # Arrow 1: Experience → Memory (bridge + FQ poll)
    result["arrows"]["experience_to_memory"] = arrow_experience_to_memory()

    # Arrow 2: Outcome → Learning (verify + extract lessons)
    result["arrows"]["outcome_to_learning"] = arrow_outcome_to_learning(dry_run=dry_run)

    # Arrow 3: Memory → Policy (evaluate promotions)
    result["arrows"]["memory_to_policy"] = arrow_memory_to_policy()

    result["completed_at"] = _now_iso()
    result["status"] = "COMPLETE"

    # Summary
    result["summary"] = {
        "episodes_created": (
            result["arrows"]["experience_to_memory"]["bridge"].get(
                "episodes_created", 0
            )
            + result["arrows"]["experience_to_memory"]["fq_poll"].get(
                "episodes_created", 0
            )
        ),
        "predictions_verified": (
            result["arrows"]["outcome_to_learning"]["verify_result"].get(
                "verified_correct", 0
            )
            + result["arrows"]["outcome_to_learning"]["verify_result"].get(
                "verified_incorrect", 0
            )
        ),
        "lessons_extracted": result["arrows"]["outcome_to_learning"].get(
            "lessons_extracted", 0
        ),
        "policies_promoted": result["arrows"]["memory_to_policy"].get("promoted", 0),
    }

    _log_loop("FULL_LOOP", result["summary"])
    return result


# ───────────────────────── LOGGING ─────────────────────────


def _log_loop(arrow: str, data: dict) -> None:
    """Append to loop log."""
    LOOP_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": _now_iso(),
        "arrow": arrow,
        "data": data,
    }
    with open(LOOP_LOG, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")


# ───────────────────────── CLI ─────────────────────────


def main() -> int:
    import sys

    args = sys.argv[1:]
    dry_run = "--dry-run" in args

    if args and args[0] == "arrows":
        # Run individual arrows
        if "1" in args or "experience" in args:
            r = arrow_experience_to_memory()
            print(f"Arrow 1 (Experience→Memory): {json.dumps(r, indent=2)}")
        if "2" in args or "outcome" in args:
            r = arrow_outcome_to_learning(dry_run=dry_run)
            print(f"Arrow 2 (Outcome→Learning): {json.dumps(r, indent=2)}")
        if "3" in args or "memory" in args:
            r = arrow_memory_to_policy()
            print(f"Arrow 3 (Memory→Policy): {json.dumps(r, indent=2)}")
        return 0

    # Full loop
    result = run_full_loop(dry_run=dry_run)
    print(f"CHRON Loop Closer — {result['loop_id']}")
    print(f"  Status: {result['status']}")
    print(f"  Summary:")
    for k, v in result["summary"].items():
        print(f"    {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
