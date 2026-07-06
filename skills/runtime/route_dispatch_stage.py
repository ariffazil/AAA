#!/usr/bin/env python3
"""Route explorer dispatch packets using the machine-readable stage map."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"ERROR: PyYAML is required: {exc}", file=sys.stderr)
    sys.exit(2)


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STAGE_MAP = SKILL_ROOT / "assets" / "agent-stage-map.yaml"


def load_doc(path: Path):
    raw = path.read_text()
    if path.suffix.lower() == ".json":
        return json.loads(raw)
    return yaml.safe_load(raw)


def route_falsification(packet: dict) -> dict:
    falsifiers = packet.get("falsifiers", [])
    physical = []
    cognitive = []
    for falsifier in falsifiers:
        if any([
            falsifier.get("requires_runtime"),
            falsifier.get("requires_code_execution"),
            falsifier.get("requires_build_or_deploy"),
        ]):
            physical.append(falsifier)
        else:
            cognitive.append(falsifier)

    if physical and cognitive:
        return {
            "route_owner": "openclaw",
            "route_mode": "mixed",
            "next_agents": ["openclaw", "aforge"],
            "counts": {"cognitive": len(cognitive), "physical": len(physical)},
        }
    if physical:
        return {
            "route_owner": "aforge",
            "route_mode": "aforge",
            "next_agents": ["aforge"],
            "counts": {"cognitive": 0, "physical": len(physical)},
        }
    return {
        "route_owner": "openclaw",
        "route_mode": "local",
        "next_agents": ["openclaw"],
        "counts": {"cognitive": len(cognitive), "physical": 0},
    }


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
        print("Usage: route_dispatch_stage.py <packet.yaml|packet.json> [stage-map.yaml]", file=sys.stderr)
        return 2

    packet_path = Path(argv[1])
    stage_map_path = Path(argv[2]) if len(argv) == 3 else DEFAULT_STAGE_MAP
    if not packet_path.exists():
        print(f"ERROR: file not found: {packet_path}", file=sys.stderr)
        return 2
    if not stage_map_path.exists():
        print(f"ERROR: file not found: {stage_map_path}", file=sys.stderr)
        return 2

    packet = load_doc(packet_path)
    stage_map = load_doc(stage_map_path)
    packet_type = infer_packet_type(packet)

    if packet_type == "falsification_packet":
        route = route_falsification(packet)
    else:
        dispatch = stage_map.get("packet_dispatch", {}).get(packet_type)
        if not dispatch:
            print(f"ERROR: unsupported packet_type for routing: {packet_type}", file=sys.stderr)
            return 2
        route = {
            "route_owner": dispatch.get("next_agent"),
            "route_mode": "single",
            "next_agents": [dispatch.get("next_agent")],
            "counts": {},
        }

    print(json.dumps({
        "packet_type": packet_type,
        "packet_id": packet.get("packet_id"),
        "route": route,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
