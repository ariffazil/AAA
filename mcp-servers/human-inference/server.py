"""
Human Meaning Inference Protocol — FastMCP Server

Implements the inference schema from human-meaning-membrane governance doctrine.
Every human interpretation must pass through this schema before action.

arifOS Federation — DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from jsonschema import Draft7Validator, ValidationError

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_SCHEMA_PATH = (
    Path(__file__).parent.parent.parent
    / "skills"
    / "human-meaning-membrane"
    / "references"
    / "inference-schema.json"
)

if _SCHEMA_PATH.exists():
    INFERENCE_SCHEMA: dict[str, Any] = json.loads(_SCHEMA_PATH.read_text())
else:
    # Inline fallback so the server is self-contained
    INFERENCE_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Human Meaning Inference Protocol",
        "type": "object",
        "required": [
            "observation",
            "context",
            "candidate_interpretations",
            "unknowns",
            "projection_risk",
            "verification_path",
            "consent_status",
            "action_authority",
            "confidence_band",
        ],
        "properties": {
            "observation": {"type": "string"},
            "context": {"type": "string"},
            "candidate_interpretations": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 3,
            },
            "unknowns": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
            },
            "projection_risk": {
                "type": "string",
                "enum": ["LOW", "MEDIUM", "HIGH"],
                "default": "MEDIUM",
            },
            "verification_path": {"type": "string"},
            "consent_status": {
                "type": "string",
                "enum": ["NOT_RELEVANT", "EXPLICIT", "UNKNOWN", "MUST_NOT_INFER"],
                "default": "UNKNOWN",
            },
            "action_authority": {
                "type": "string",
                "enum": ["READ_ONLY", "HUMAN_CONFIRMATION_REQUIRED"],
                "default": "HUMAN_CONFIRMATION_REQUIRED",
            },
            "confidence_band": {
                "type": "array",
                "items": {"type": "number"},
                "minItems": 2,
                "maxItems": 2,
            },
        },
    }

_validator = Draft7Validator(INFERENCE_SCHEMA)

# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "Human Inference",
    instructions=(
        "Human Meaning Inference Protocol server. "
        "Exposes a `human_inference` tool that accepts an observation + context "
        "and returns a structured inference JSON per the arifOS membrane schema. "
        "Non-negotiable: min 3 interpretations, confidence hard-capped at 0.9, "
        "consent defaults to UNKNOWN, projection defaults to MEDIUM."
    ),
)


@mcp.tool()
def human_inference(
    observation: str,
    context: str,
    candidate_interpretations: list[str] | None = None,
    unknowns: list[str] | None = None,
    projection_risk: str = "MEDIUM",
    verification_path: str = "",
    consent_status: str = "UNKNOWN",
    action_authority: str = "HUMAN_CONFIRMATION_REQUIRED",
    confidence_band: list[float] | None = None,
) -> dict[str, Any]:
    """Run the Human Meaning Inference Protocol.

    Takes a raw observation and contextual grounding, builds (or validates)
    a structured inference payload, and returns it as validated JSON.

    Non-negotiable governance rules enforced:
      - Minimum 3 candidate interpretations
      - Confidence band hard-capped at [0.0, 0.9]
      - Consent defaults to UNKNOWN; projection defaults to MEDIUM
      - action_authority defaults to HUMAN_CONFIRMATION_REQUIRED

    Args:
        observation: What was literally said or done. Raw data only.
        context: Time, relationship, setting, prior relevant evidence.
        candidate_interpretations: At least 3 competing interpretations.
        unknowns: What CANNOT be inferred from available data.
        projection_risk: LOW | MEDIUM | HIGH (default MEDIUM).
        verification_path: Reversible, dignified question or observable outcome.
        consent_status: NOT_RELEVANT | EXPLICIT | UNKNOWN | MUST_NOT_INFER.
        action_authority: READ_ONLY | HUMAN_CONFIRMATION_REQUIRED.
        confidence_band: [low, high] confidence range, max 0.9.

    Returns:
        Validated inference JSON matching the Human Meaning Inference Protocol.
    """
    # --- Defaults for list fields ---
    if candidate_interpretations is None:
        candidate_interpretations = [
            f"Interpretation based on literal reading: {observation[:120]}",
            "Contextual reading informed by relationship and setting",
            "Alternative: signal may be noise — insufficient evidence",
        ]

    if unknowns is None:
        unknowns = [
            "Internal state of the observed person",
            "Whether the observation is representative or anomalous",
            "Cultural or personal context not captured in the input",
        ]

    if confidence_band is None:
        confidence_band = [0.3, 0.7]

    # --- Governance enforcement ---

    # Min 3 interpretations
    while len(candidate_interpretations) < 3:
        candidate_interpretations.append(
            f"Insufficient data — floor interpretation #{len(candidate_interpretations) + 1}"
        )

    # Min 1 unknown
    if len(unknowns) < 1:
        unknowns.append("Unstated context that may alter interpretation")

    # Hard-cap confidence band at 0.9
    confidence_band[0] = max(0.0, min(1.0, confidence_band[0]))
    confidence_band[1] = max(0.0, min(0.9, confidence_band[1]))
    # Ensure low <= high
    if confidence_band[0] > confidence_band[1]:
        confidence_band[0], confidence_band[1] = confidence_band[1], confidence_band[0]

    # Build the inference record
    record: dict[str, Any] = {
        "observation": observation,
        "context": context,
        "candidate_interpretations": candidate_interpretations,
        "unknowns": unknowns,
        "projection_risk": projection_risk,
        "verification_path": verification_path or "No verification path provided — MEDIUM confidence inference",
        "consent_status": consent_status,
        "action_authority": action_authority,
        "confidence_band": confidence_band,
    }

    # --- Schema validation ---
    errors = sorted(_validator.iter_errors(record), key=lambda e: list(e.path))
    if errors:
        error_details = [
            {"field": ".".join(str(p) for p in err.absolute_path), "message": err.message}
            for err in errors
        ]
        return {
            "valid": False,
            "error": "Schema validation failed",
            "details": error_details,
            "record": record,
        }

    return {"valid": True, "record": record}


# ---------------------------------------------------------------------------
# Resources — expose the schema itself
# ---------------------------------------------------------------------------

@mcp.resource("human-meaning-membrane://inference-schema")
def get_inference_schema() -> str:
    """Return the Human Meaning Inference Protocol JSON Schema."""
    return json.dumps(INFERENCE_SCHEMA, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
