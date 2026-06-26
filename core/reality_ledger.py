"""
Reality Ledger — prediction vs outcome comparison layer.

VAULT999 answers: "What did we decide and seal?"
Reality Ledger answers: "Did reality agree later?"

This creates the AGI-like loop:
    Hypothesis → action → observation → correction

Without this, the system is governed automation.
With this, it becomes a reality-learning substrate.
"""

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Default storage path
DEFAULT_STORE_PATH = Path("/root/AAA/data/reality_ledger")
SCHEMA_PATH = Path("/root/AAA/schemas/reality_ledger.schema.json")


class RealityLedgerError(Exception):
    """Base exception for Reality Ledger operations."""
    pass


class EventNotFoundError(RealityLedgerError):
    """Raised when an event ID is not found."""
    pass


class ValidationError(RealityLedgerError):
    """Raised when event data fails validation."""
    pass


def _ensure_store(store_path: Path = DEFAULT_STORE_PATH):
    """Ensure the store directory exists."""
    store_path.mkdir(parents=True, exist_ok=True)
    events_dir = store_path / "events"
    events_dir.mkdir(exist_ok=True)
    return store_path


def _event_path(event_id: str, store_path: Path = DEFAULT_STORE_PATH) -> Path:
    return store_path / "events" / f"{event_id}.json"


def _index_path(store_path: Path = DEFAULT_STORE_PATH) -> Path:
    return store_path / "index.jsonl"


def create_event(
    actor: str,
    intent: str,
    action_class: str,
    expected_outcome: str,
    confidence: float,
    uncertainty: str = "medium",
    failure_modes: Optional[list] = None,
    organs_consulted: Optional[list] = None,
    evidence_refs: Optional[list] = None,
    vault999_receipt: str = "",
    quantitative_bounds: Optional[dict] = None,
    tags: Optional[list] = None,
    store_path: Path = DEFAULT_STORE_PATH,
) -> dict:
    """
    Create a new Reality Ledger event with a prediction.

    This is called BEFORE execution. The observed_outcome and lesson
    fields are populated later via record_outcome().

    Args:
        actor: Who proposed the action.
        intent: What was the goal.
        action_class: observe | propose | mutate | deploy | communicate | allocate.
        expected_outcome: What we predict will happen.
        confidence: 0.0–1.0 (will be capped at 0.90 per F7).
        uncertainty: low | medium | high.
        failure_modes: What could go wrong.
        organs_consulted: Which witnesses were called.
        evidence_refs: Evidence grounding the decision.
        vault999_receipt: Link to sealed VAULT999 record.
        quantitative_bounds: Optional p10/p50/p90 bounds.
        tags: Free-form tags.

    Returns:
        The created event dict with generated id and timestamp.

    Raises:
        ValidationError: If required fields are missing or invalid.
    """
    logger.info("create_event called", extra={"actor": actor, "action_class": action_class})
    _ensure_store(store_path)
    confidence = min(confidence, 0.90)

    # Validation
    if not actor or not actor.strip():
        raise ValidationError("actor is required")
    if not intent or not intent.strip():
        raise ValidationError("intent is required")
    if action_class not in ["observe", "propose", "mutate", "deploy", "communicate", "allocate"]:
        raise ValidationError(f"Invalid action_class: {action_class}")
    if not expected_outcome or not expected_outcome.strip():
        raise ValidationError("expected_outcome is required")
    if uncertainty not in ["low", "medium", "high"]:
        raise ValidationError(f"Invalid uncertainty: {uncertainty}")

    event = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor": actor,
        "intent": intent,
        "action_class": action_class,
        "organs_consulted": organs_consulted or [],
        "evidence_refs": evidence_refs or [],
        "prediction": {
            "expected_outcome": expected_outcome,
            "confidence": confidence,
            "uncertainty": uncertainty,
            "failure_modes": failure_modes or [],
        },
        "arifos_verdict": {
            "verdict": "SEAL",
            "floors_triggered": [],
            "lease_id": "",
        },
        "execution": {},
        "observed_outcome": {},
        "lesson": {},
        "vault999_receipt": vault999_receipt,
        "supersedes": None,
        "tags": tags or [],
    }

    if quantitative_bounds:
        event["prediction"]["quantitative_bounds"] = quantitative_bounds

    # Write event file
    filepath = _event_path(event["id"], store_path)
    with open(filepath, "w") as f:
        json.dump(event, f, indent=2, default=str)

    # Append to index
    with open(_index_path(store_path), "a") as f:
        f.write(json.dumps({
            "id": event["id"],
            "timestamp": event["timestamp"],
            "actor": event["actor"],
            "action_class": event["action_class"],
            "confidence": event["prediction"]["confidence"],
            "outcome_recorded": False,
        }) + "\n")

    return event


def record_outcome(
    event_id: str,
    result: str,
    delta_from_prediction: str = "",
    actual_value: Optional[float] = None,
    predicted_value: Optional[float] = None,
    evidence_urls: Optional[list] = None,
    what_changed: str = "",
    memory_update: str = "",
    future_rule: str = "",
    store_path: Path = DEFAULT_STORE_PATH,
) -> dict:
    """
    Record the observed outcome for a Reality Ledger event.

    This is called AFTER reality catches up to the prediction.

    Args:
        event_id: The event ID from create_event().
        result: What actually happened.
        delta_from_prediction: How reality differed.
        actual_value: Quantitative actual value (optional).
        predicted_value: Quantitative predicted value (optional).
        evidence_urls: Sources confirming the outcome.
        what_changed: What the system should learn.
        memory_update: What to update in memory.
        future_rule: New invariant if applicable.

    Returns:
        The updated event dict.

    Raises:
        EventNotFoundError: If event_id does not exist.
    """
    filepath = _event_path(event_id, store_path)
    if not filepath.exists():
        logger.error("Event not found: %s", event_id)
        raise EventNotFoundError(f"Event {event_id} not found at {filepath}")

    with open(filepath, "r") as f:
        event = json.load(f)

    # Compute accuracy
    accuracy_score = None
    if actual_value is not None and predicted_value is not None and predicted_value != 0:
        error_pct = abs((actual_value - predicted_value) / predicted_value) * 100
        within_bounds = error_pct < 20.0  # within 20% = acceptable
        accuracy_score = max(0.0, 1.0 - (error_pct / 100.0))
        event["observed_outcome"]["quantitative_delta"] = {
            "actual_value": actual_value,
            "predicted_value": predicted_value,
            "error_pct": round(error_pct, 2),
            "within_bounds": within_bounds,
        }

    event["observed_outcome"] = {
        "result": result,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "delta_from_prediction": delta_from_prediction,
        "evidence_urls": evidence_urls or [],
    }

    event["lesson"] = {
        "what_changed": what_changed,
        "memory_update": memory_update,
        "future_rule": future_rule,
    }
    if accuracy_score is not None:
        event["lesson"]["accuracy_score"] = round(accuracy_score, 4)

    # Write updated event
    with open(filepath, "w") as f:
        json.dump(event, f, indent=2, default=str)

    # Update index
    index_path = _index_path(store_path)
    if index_path.exists():
        lines = index_path.read_text().splitlines()
        new_lines = []
        for line in lines:
            entry = json.loads(line)
            if entry["id"] == event_id:
                entry["outcome_recorded"] = True
            new_lines.append(json.dumps(entry))
        index_path.write_text("\n".join(new_lines) + "\n")

    return event


def get_event(event_id: str, store_path: Path = DEFAULT_STORE_PATH) -> dict:
    """Retrieve a single Reality Ledger event."""
    filepath = _event_path(event_id, store_path)
    if not filepath.exists():
        raise EventNotFoundError(f"Event {event_id} not found")
    with open(filepath, "r") as f:
        return json.load(f)


def list_events(
    limit: int = 50,
    actor: Optional[str] = None,
    action_class: Optional[str] = None,
    only_with_outcome: bool = False,
    store_path: Path = DEFAULT_STORE_PATH,
) -> list:
    """List Reality Ledger events with optional filtering."""
    index_path = _index_path(store_path)
    if not index_path.exists():
        return []

    events = []
    with open(index_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if actor and entry.get("actor") != actor:
                continue
            if action_class and entry.get("action_class") != action_class:
                continue
            if only_with_outcome and not entry.get("outcome_recorded"):
                continue
            events.append(entry)

    events.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
    return events[:limit]


def compute_accuracy_stats(store_path: Path = DEFAULT_STORE_PATH) -> dict:
    """Compute aggregate accuracy statistics across all events with outcomes."""
    stats = {
        "total_events": 0,
        "with_outcome": 0,
        "without_outcome": 0,
        "accuracy_scores": [],
        "mean_accuracy": None,
        "by_action_class": {},
        "by_actor": {},
    }

    events_dir = store_path / "events"
    if not events_dir.exists():
        return stats

    for fpath in events_dir.glob("*.json"):
        with open(fpath) as f:
            event = json.load(f)

        stats["total_events"] += 1

        if event.get("observed_outcome", {}).get("result"):
            stats["with_outcome"] += 1
            lesson = event.get("lesson", {})
            if lesson.get("accuracy_score") is not None:
                stats["accuracy_scores"].append(lesson["accuracy_score"])

            ac = event.get("action_class", "unknown")
            if ac not in stats["by_action_class"]:
                stats["by_action_class"][ac] = {"count": 0, "scores": []}
            stats["by_action_class"][ac]["count"] += 1
            if lesson.get("accuracy_score") is not None:
                stats["by_action_class"][ac]["scores"].append(lesson["accuracy_score"])

            act = event.get("actor", "unknown")
            if act not in stats["by_actor"]:
                stats["by_actor"][act] = {"count": 0, "scores": []}
            stats["by_actor"][act]["count"] += 1
            if lesson.get("accuracy_score") is not None:
                stats["by_actor"][act]["scores"].append(lesson["accuracy_score"])
        else:
            stats["without_outcome"] += 1

    if stats["accuracy_scores"]:
        stats["mean_accuracy"] = round(
            sum(stats["accuracy_scores"]) / len(stats["accuracy_scores"]), 4
        )

    # Compute per-class means
    for ac in stats["by_action_class"]:
        scores = stats["by_action_class"][ac]["scores"]
        stats["by_action_class"][ac]["mean_accuracy"] = (
            round(sum(scores) / len(scores), 4) if scores else None
        )

    for act in stats["by_actor"]:
        scores = stats["by_actor"][act]["scores"]
        stats["by_actor"][act]["mean_accuracy"] = (
            round(sum(scores) / len(scores), 4) if scores else None
        )

    return stats


def validate_schema(event: dict) -> tuple[bool, list]:
    """
    Basic schema validation without external library dependency.
    Returns (is_valid, errors).
    """
    errors = []
    required = ["id", "timestamp", "actor", "intent", "action_class", "prediction", "arifos_verdict"]

    for field in required:
        if field not in event:
            errors.append(f"Missing required field: {field}")

    if "prediction" in event:
        pred = event["prediction"]
        if "expected_outcome" not in pred:
            errors.append("prediction.expected_outcome is required")
        if "confidence" not in pred:
            errors.append("prediction.confidence is required")
        elif not isinstance(pred["confidence"], (int, float)):
            errors.append("prediction.confidence must be a number")
        elif pred["confidence"] < 0 or pred["confidence"] > 1:
            errors.append("prediction.confidence must be between 0 and 1")

    if event.get("action_class") not in [
        "observe", "propose", "mutate", "deploy", "communicate", "allocate"
    ]:
        errors.append(f"Invalid action_class: {event.get('action_class')}")

    return len(errors) == 0, errors


def replay_ledger(store_path: Path = DEFAULT_STORE_PATH) -> dict:
    """
    Full ledger replay: compute accuracy, identify failure patterns,
    and generate recommendations.

    Returns a comprehensive replay report.
    """
    stats = compute_accuracy_stats(store_path)

    replay = {
        "replayed_at": datetime.now(timezone.utc).isoformat(),
        "total_events": stats["total_events"],
        "with_outcome": stats["with_outcome"],
        "without_outcome": stats["without_outcome"],
        "mean_accuracy": stats["mean_accuracy"],
        "by_action_class": stats["by_action_class"],
        "by_actor": stats["by_actor"],
        "improvement_recommendations": [],
    }

    # Generate recommendations
    if stats["without_outcome"] > stats["with_outcome"]:
        replay["improvement_recommendations"].append(
            f"More outcomes needed: {stats['without_outcome']} events pending observation"
        )

    if stats["mean_accuracy"] is not None and stats["mean_accuracy"] < 0.7:
        replay["improvement_recommendations"].append(
            f"Low mean accuracy ({stats['mean_accuracy']:.2f}): consider revising prediction methodology"
        )

    for ac, data in stats.get("by_action_class", {}).items():
        if data.get("mean_accuracy") is not None and data["mean_accuracy"] < 0.6:
            replay["improvement_recommendations"].append(
                f"Action class '{ac}' has low accuracy ({data['mean_accuracy']:.2f}): needs investigation"
            )

    return replay


if __name__ == "__main__":
    # Quick self-test

    print("=== Reality Ledger Self-Test ===")

    # Test with temp store
    test_store = DEFAULT_STORE_PATH / "test"
    if test_store.exists():
        import shutil
        shutil.rmtree(test_store)

    # Create event
    event = create_event(
        actor="FORGE-000Ω",
        intent="Test prediction: file rename should succeed",
        action_class="mutate",
        expected_outcome="File renamed successfully with rollback available",
        confidence=0.85,
        uncertainty="low",
        failure_modes=["File not found", "Permission denied"],
        store_path=test_store,
    )
    print(f"Created event: {event['id']}")
    print(f"  Confidence capped at: {event['prediction']['confidence']}")

    # Record outcome
    updated = record_outcome(
        event_id=event["id"],
        result="File renamed successfully",
        delta_from_prediction="Match: exactly as predicted",
        actual_value=100.0,
        predicted_value=95.0,
        evidence_urls=["file:///tmp/test_rename.log"],
        what_changed="Prediction framework confirmed valid",
        memory_update="Update L3 semantic memory: rename ops are reliable",
        future_rule="Allow file rename with rollback",
        store_path=test_store,
    )
    print(f"Recorded outcome: accuracy = {updated['lesson'].get('accuracy_score')}")

    # Stats
    stats = compute_accuracy_stats(test_store)
    print(f"Stats: {stats['total_events']} events, mean accuracy = {stats['mean_accuracy']}")

    # Replay
    replay = replay_ledger(test_store)
    print(f"Replay recommendations: {replay['improvement_recommendations']}")

    # Cleanup test
    import shutil
    shutil.rmtree(test_store)

    print("\n=== Reality Ledger Self-Test PASSED ===")
