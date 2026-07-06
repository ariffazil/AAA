#!/usr/bin/env python3
"""Validate explorer civilization dispatch packets against minimal schema floors."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"ERROR: PyYAML is required: {exc}", file=sys.stderr)
    sys.exit(2)


REQUIRED_BY_PACKET = {
    "dispatch_envelope": ["packet_type", "handoff_id", "query_id", "from_agent", "to_agent", "phase", "packet_ref", "validated", "timestamps"],
    "observation_packet": ["packet_type", "packet_id", "query", "observations", "domain_hints", "owning_organs", "next_route", "receipts"],
    "hypothesis_packet": ["packet_type", "packet_id", "query", "observation_refs", "hypotheses", "next_route", "receipts"],
    "falsification_packet": ["packet_type", "packet_id", "query", "hypothesis_refs", "falsifiers", "tests", "next_route", "owning_organs", "receipts"],
    "verification_packet": ["packet_type", "packet_id", "query", "survivor_refs", "falsification_summary", "uncertainty_band", "verdict_candidate", "next_route", "receipts"],
    "eureka_packet": ["packet_type", "packet_id", "contradiction_refs", "domains_touched", "compression_failure", "constitutional_review_required", "next_route", "receipts"],
    "verdict_envelope": ["packet_type", "packet_id", "verdict", "source_packet", "graph_updates", "next_route", "receipts"],
    "scar_packet": ["packet_type", "packet_id", "falsified_assumption", "permanent_constraint", "scope", "next_route", "receipts"],
}

VALID_PACKET_TYPES = set(REQUIRED_BY_PACKET)
VALID_VERDICTS = {"SEAL", "SABAR", "HOLD", "VOID", None}


def load_doc(path: Path):
    raw = path.read_text()
    if path.suffix.lower() == ".json":
        return json.loads(raw)
    return yaml.safe_load(raw)


def validate_packet_obj(name: str, obj: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return [f"{name} must be an object"]

    packet_type = obj.get("packet_type", name)
    if packet_type != name:
        errors.append(f"{name}.packet_type must equal {name}")

    for field in REQUIRED_BY_PACKET[name]:
        if field not in obj:
            errors.append(f"{name} missing {field}")

    if name == "verification_packet":
        verdict = obj.get("verdict_candidate")
        if verdict not in VALID_VERDICTS:
            errors.append("verification_packet.verdict_candidate invalid")

    if name == "dispatch_envelope" and "validated" in obj and not isinstance(obj["validated"], bool):
        errors.append("dispatch_envelope.validated must be boolean")

    return errors


def validate_doc(doc: object) -> list[str]:
    errors: list[str] = []
    if isinstance(doc, dict) and "packet_type" in doc:
        packet_type = doc["packet_type"]
        if packet_type not in VALID_PACKET_TYPES:
            return [f"unknown packet_type: {packet_type}"]
        return validate_packet_obj(packet_type, doc)

    if not isinstance(doc, dict):
        return ["document root must be an object"]

    for packet_name in doc:
        if packet_name not in VALID_PACKET_TYPES:
            errors.append(f"unknown top-level packet block: {packet_name}")
            continue
        errors.extend(validate_packet_obj(packet_name, doc[packet_name]))
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_dispatch_packet.py <packet.yaml|packet.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    try:
        doc = load_doc(path)
        errors = validate_doc(doc)
    except Exception as exc:
        print(f"ERROR: failed to load packet: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("INVALID dispatch packet")
        for err in errors:
            print(f"- {err}")
        return 1

    print("VALID dispatch packet")
    if isinstance(doc, dict) and "packet_type" in doc:
        print(f"- packet_type: {doc['packet_type']}")
    else:
        print(f"- packet_blocks: {', '.join(doc.keys())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
