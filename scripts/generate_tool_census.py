#!/usr/bin/env python3
"""Generate tool_census.yaml as an ENRICHED VIEW of federation_tools_sot.yaml.

RULE: There is exactly ONE federation aggregate (federation_tools_sot.yaml).
This script generates tool_census.yaml by:
  1. Reading all organ SOT files (tool names + visibility)
  2. Enriching with ABI data (action_class, mutation, authority, floors)
  3. Computing derived fields (lane, danger_class, ttl)
  4. Writing the enriched census

tool_census.yaml is NEVER hand-edited. It is always generated from SOT + ABI.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# SOT files per organ
ORGAN_SOTS = {
    "arifOS": Path("/root/arifOS/tools_sot.yaml"),
    "A-FORGE": Path("/root/A-FORGE/tools_sot.yaml"),
    "GEOX": Path("/root/GEOX/tools_sot.yaml"),
    "WEALTH": Path("/root/WEALTH/tools_sot.yaml"),
    "WELL": Path("/root/WELL/tools_sot.yaml"),
}

# ABI enrichment source
ABI_PATH = Path("/root/arifOS/arifosmcp/abi/capability_registry.json")

FEDERATION_SOT = Path("/root/AAA/docs/federation_tools_sot.yaml")
OUTPUT = Path("/root/AAA/docs/tool_census.yaml")

# Lane derivation from action_class
LANE_MAP = {
    "OBSERVE": "READ",
    "PREPARE": "READ",
    "MATERIAL": "WRITE",
    "IRREVERSIBLE": "WRITE",
}

# Danger class from action_class + mutation + irreversible
DANGER_MAP = {
    ("OBSERVE", False, False): "GREEN",
    ("PREPARE", False, False): "GREEN",
    ("MATERIAL", False, False): "YELLOW",
    ("MATERIAL", True, False): "ORANGE",
    ("MATERIAL", True, True): "RED",
    ("IRREVERSIBLE", True, True): "RED",
}

# TTL defaults by action class
TTL_MAP = {
    "OBSERVE": 300,
    "PREPARE": 300,
    "MATERIAL": 600,
    "IRREVERSIBLE": 0,
}


def load_abi_enrichment() -> dict[str, dict]:
    """Load enrichment data from capability_registry.json."""
    if not ABI_PATH.exists():
        return {}
    with open(ABI_PATH) as f:
        abi = json.load(f)
    enrichment = {}
    for cap in abi.get("capabilities", []):
        name = cap["provider"]["tool"]
        enrichment[name] = {
            "action_class": cap["action_class"],
            "mutation": cap["mutation"],
            "irreversible": cap["irreversible"],
            "authority_required": cap["authority_required"],
            "floors": cap.get("constitutional_floors", []),
        }
    return enrichment


def derive_fields(entry: dict, enrichment: dict[str, dict]) -> dict:
    """Add derived fields to a tool entry."""
    name = entry["name"]
    abi = enrichment.get(name, {})

    action_class = abi.get("action_class", "OBSERVE")
    mutation = abi.get("mutation", False)
    irreversible = abi.get("irreversible", False)

    entry["lane"] = LANE_MAP.get(action_class, "READ")
    entry["mutation"] = mutation
    entry["authority_required"] = abi.get("authority_required", "OBSERVER")
    entry["evidence_layer"] = "RUNTIME" if mutation else "CACHED_STATE"
    entry["ttl_seconds"] = TTL_MAP.get(action_class, 300)
    entry["runtime_callable"] = entry.get("access", "public") != "internal_only"
    entry["deprecated"] = entry.get("status") == "deprecated"
    entry["replacement"] = None  # filled manually if needed
    entry["danger_class"] = DANGER_MAP.get((action_class, mutation, irreversible), "GREEN")

    return entry


def main() -> None:
    enrichment = load_abi_enrichment()
    census_tools = []
    organ_counts = {}

    for organ_name, sot_path in sorted(ORGAN_SOTS.items()):
        if not sot_path.exists():
            print(f"WARNING: SOT not found for {organ_name} at {sot_path}", file=sys.stderr)
            continue

        with open(sot_path) as f:
            sot = yaml.safe_load(f)

        tools = sot.get("tools", [])
        organ_counts[organ_name] = {"total": len(tools), "public": 0, "internal": 0}

        for tool in tools:
            entry = {
                "name": tool["name"],
                "organ": organ_name,
                "access": tool.get("access", "public"),
                "description": tool.get("description", ""),
            }

            # Count by class
            access = tool.get("access", "public")
            if access in ("public", "authenticated"):
                organ_counts[organ_name]["public"] += 1
            else:
                organ_counts[organ_name]["internal"] += 1

            # Skip internal-only tools from census (they're in SOT but not federation-facing)
            if access == "internal_only":
                continue

            # Enrich with ABI data
            entry = derive_fields(entry, enrichment)
            census_tools.append(entry)

    census = {
        "census_metadata": {
            "version": "2.0.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": str(FEDERATION_SOT),
            "description": (
                "GENERATED VIEW of federation_tools_sot.yaml + ABI enrichment. "
                "Do not hand-edit. Regenerate with: python3 /root/AAA/scripts/generate_tool_census.py"
            ),
            "inclusion_rule": "public + authenticated tools only. internal_only excluded.",
            "organ_counts": organ_counts,
        },
        "tools": census_tools,
    }

    with open(OUTPUT, "w") as f:
        yaml.dump(census, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"tool_census.yaml generated: {len(census_tools)} tools from {len(organ_counts)} organs")
    for organ, counts in organ_counts.items():
        print(f"  {organ}: {counts['public']} public + {counts['internal']} internal = {counts['total']} total")


if __name__ == "__main__":
    main()
