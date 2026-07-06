#!/usr/bin/env python3
"""Append a compact handoff receipt for explorer dispatch."""

from __future__ import annotations

import json
import sys
from datetime import datetime, UTC
from pathlib import Path

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"ERROR: PyYAML is required: {exc}", file=sys.stderr)
    sys.exit(2)


DEFAULT_LOG = Path(__file__).resolve().parent.parent / "assets" / "handoff_log.jsonl"


def load_doc(path: Path):
    raw = path.read_text()
    if path.suffix.lower() == ".json":
        return json.loads(raw)
    return yaml.safe_load(raw)


def infer_packet_type(packet: dict) -> str | None:
    if packet.get("packet_type"):
        return packet["packet_type"]
    if "falsifiers" in packet and "tests" in packet:
        return "falsification_packet"
    if "hypotheses" in packet and "observation_refs" in packet:
        return "hypothesis_packet"
    if "observations" in packet and "domain_hints" in packet:
        return "observation_packet"
    if "verdict" in packet and "graph_updates" in packet:
        return "verdict_envelope"
    return None


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print("Usage: log_handoff.py <packet.yaml|packet.json> [log.jsonl]", file=sys.stderr)
        return 2

    packet_path = Path(argv[1])
    log_path = Path(argv[2]) if len(argv) == 3 else DEFAULT_LOG
    if not packet_path.exists():
        print(f"ERROR: file not found: {packet_path}", file=sys.stderr)
        return 2

    packet = load_doc(packet_path)
    entry = {
        "ts_utc": datetime.now(UTC).isoformat(),
        "packet_type": infer_packet_type(packet),
        "packet_id": packet.get("packet_id", packet.get("handoff_id")),
        "query": packet.get("query", packet.get("query_id")),
        "from_agent": packet.get("from_agent", packet.get("source_agent")),
        "to_agent": packet.get("to_agent"),
        "next_route": packet.get("next_route"),
    }

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")

    print(json.dumps({"logged": True, "path": str(log_path), "entry": entry}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
