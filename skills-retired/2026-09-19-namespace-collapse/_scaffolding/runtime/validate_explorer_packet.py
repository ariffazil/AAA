#!/usr/bin/env python3
"""Validate explorer packet YAML/JSON against the protocol floor."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except Exception as exc:  # pragma: no cover - dependency failure path
    print(f"ERROR: PyYAML is required to validate YAML packets: {exc}", file=sys.stderr)
    sys.exit(2)


EXPECTED_MODE_SEQUENCE = ["observe", "hypothesize", "falsify", "verify"]
ALLOWED_VERDICTS = {"SEAL", "SABAR", "HOLD", "VOID", None}
REQUIRED_TOP_LEVEL = [
    "packet_id",
    "query",
    "mode_sequence",
    "observations",
    "hypotheses",
    "tests",
    "contradictions",
    "survivors",
    "uncertainty_band",
    "owning_organs",
    "next_route",
    "verdict_candidate",
    "memory_update",
    "receipts",
    "timestamps",
]


def _load_packet(path: Path) -> dict:
    raw = path.read_text()
    if path.suffix.lower() == ".json":
        return json.loads(raw)
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError("packet root must be a mapping/object")
    return data


def _require_mapping(name: str, value: object, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{name} must be a mapping/object")


def validate_packet(packet: dict) -> list[str]:
    errors: list[str] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in packet:
            errors.append(f"missing top-level field: {key}")

    if errors:
        return errors

    if packet["mode_sequence"] != EXPECTED_MODE_SEQUENCE:
        errors.append(
            "mode_sequence must be exactly "
            + " -> ".join(EXPECTED_MODE_SEQUENCE)
        )

    if not isinstance(packet["observations"], list) or not packet["observations"]:
        errors.append("observations must be a non-empty list")

    if not isinstance(packet["hypotheses"], list) or not packet["hypotheses"]:
        errors.append("hypotheses must be a non-empty list")

    if not isinstance(packet["tests"], list):
        errors.append("tests must be a list")

    if packet["survivors"] and not packet["tests"]:
        errors.append("survivors cannot exist without tests")

    if packet["verdict_candidate"] not in ALLOWED_VERDICTS:
        errors.append("verdict_candidate must be one of SEAL/SABAR/HOLD/VOID/null")

    try:
        uncertainty = float(packet["uncertainty_band"])
    except Exception:
        errors.append("uncertainty_band must be numeric")
    else:
        if uncertainty < 0 or uncertainty > 1:
            errors.append("uncertainty_band must be between 0.0 and 1.0")
        if packet["verdict_candidate"] == "SEAL" and uncertainty > 0.20:
            errors.append("SEAL verdict_candidate requires uncertainty_band <= 0.20")

    _require_mapping("memory_update", packet["memory_update"], errors)
    _require_mapping("timestamps", packet["timestamps"], errors)

    next_route = packet["next_route"]
    if next_route is not None and not isinstance(next_route, dict):
        errors.append("next_route must be null or a mapping/object")

    for idx, obs in enumerate(packet["observations"]):
        if not isinstance(obs, dict):
            errors.append(f"observations[{idx}] must be an object")
            continue
        for field in ("observation_id", "source", "domain", "epistemic_rung", "summary", "confidence"):
            if field not in obs:
                errors.append(f"observations[{idx}] missing {field}")

    for idx, hyp in enumerate(packet["hypotheses"]):
        if not isinstance(hyp, dict):
            errors.append(f"hypotheses[{idx}] must be an object")
            continue
        for field in ("hypothesis_id", "rank", "claim", "owning_domain", "falsifiers", "confidence"):
            if field not in hyp:
                errors.append(f"hypotheses[{idx}] missing {field}")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_explorer_packet.py <packet.yaml|packet.json>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    try:
        packet = _load_packet(path)
        errors = validate_packet(packet)
    except Exception as exc:
        print(f"ERROR: failed to load packet: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("INVALID explorer packet")
        for err in errors:
            print(f"- {err}")
        return 1

    print("VALID explorer packet")
    print(f"- packet_id: {packet['packet_id']}")
    print(f"- verdict_candidate: {packet['verdict_candidate']}")
    print(f"- observations: {len(packet['observations'])}")
    print(f"- hypotheses: {len(packet['hypotheses'])}")
    print(f"- tests: {len(packet['tests'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
