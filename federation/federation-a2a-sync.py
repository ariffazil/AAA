#!/usr/bin/env python3
"""
federation-a2a-sync.py — Bridge federation.yaml → A2A registry.
Converts federation agent cards to A2A JSON format and places them
in the a2a-server registry directory. Does NOT replace existing rich cards
(charter, species, genome) — supplements with MCP surface data.

Reads: /root/AAA/federation/agents/<name>/agent.yaml
Writes: /root/AAA/a2a-server/agent-cards/federation/<name>.json
"""
import yaml
import json
import sys
from pathlib import Path

FED_AGENTS = Path("/root/AAA/federation/agents")
A2A_TARGET = Path("/root/AAA/a2a-server/agent-cards/federation")

def convert(fed_card):
    """Convert federation YAML card → A2A JSON card."""
    a2a = {
        "$schema": "arifOS/agent-card/v2.2.0",
        "schemaVersion": "2.2.0",
        "protocolVersion": "1.2",
        "agentId": fed_card["name"],
        "name": fed_card["name"],
        "description": fed_card.get("description", ""),
        "version": fed_card.get("version", "1.0.0"),
        "provider": {
            "organization": "arifOS Federation",
            "source": "federation.yaml (generated)"
        },
        "capabilities": fed_card.get("capabilities", {
            "streaming": True,
            "pushNotifications": False,
            "opaqueExecution": True,
        }),
        "defaultInputModes": fed_card.get("defaultInputModes", ["text"]),
        "defaultOutputModes": fed_card.get("defaultOutputModes", ["text"]),
        "securitySchemes": fed_card.get("securitySchemes", {
            "bearer": {
                "type": "http",
                "scheme": "bearer",
                "description": "arifOS SCT token"
            }
        }),
        "skills": [
            {"id": s["id"], "name": s["id"].replace("-", " ").title(), "tags": [s["owner"]]}
            for s in fed_card.get("skill", [])
        ],
        "mcp_surface": {
            sid: {
                "port": sdef.get("port"),
                "tier": sdef.get("tier"),
                "surface": sdef.get("surface"),
                "capability": sdef.get("capability", []),
            }
            for sid, sdef in fed_card.get("server", {}).items()
        },
        "role": fed_card.get("role", "unknown"),
        "grant": fed_card.get("grant", []),
        "federation_metadata": {
            "fi": fed_card.get("fi", ""),
            "runtime": fed_card.get("runtime", "unknown"),
            "note": fed_card.get("note", ""),
            "source": "federation.yaml",
            "generated_by": "federation-a2a-sync.py"
        }
    }
    return a2a

def main():
    A2A_TARGET.mkdir(parents=True, exist_ok=True)
    count = 0

    for agent_dir in sorted(FED_AGENTS.iterdir()):
        card_path = agent_dir / "agent.yaml"
        if not card_path.exists():
            continue

        with open(card_path) as f:
            fed_card = yaml.safe_load(f)

        a2a_card = convert(fed_card)
        out_path = A2A_TARGET / f"{agent_dir.name}.json"
        with open(out_path, "w") as f:
            json.dump(a2a_card, f, indent=2)
        count += 1
        print(f"  synced: {agent_dir.name} → {out_path.name}")

    print(f"\n{count} federation cards synced to A2A registry at {A2A_TARGET}")
    return count

if __name__ == "__main__":
    main()
