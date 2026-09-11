#!/usr/bin/env python3
"""
P2.9 — MCP Auto-Discovery Watcher
===================================
Endpoint poller that discovers new MCP servers, extracts their tool surface,
and auto-indexes the capability descriptions into federation memory.

Architecture:
  1. Poll known MCP endpoints (:8088, :7072, :8081, :18082, :18083, )
  2. Fetch tools/list from each
  3. Store tool affordances via FederationMemory adapter
     (collection_class=skill_mesh → arifOS_skill_mesh; the kernel
     owns embedding — agents never touch the vector store directly)
  4. Detect new/removed tools since last scan

Forged: 2026-08-10 by 333-AGI under F13 directive.
Migrated 2026-09-12 to federation_memory_adapter (F13 SOVEREIGN
directive — /root/AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md).
"""

import json
import os
import urllib.request
import sys
from pathlib import Path
from datetime import datetime, timezone

_FEDERATION_DIR = Path(__file__).resolve().parents[1] / "federation"
if str(_FEDERATION_DIR) not in sys.path:
    sys.path.insert(0, str(_FEDERATION_DIR))

from federation_memory_adapter import FederationMemory

# ── Config ────────────────────────────────────────────────────────
MCP_ENDPOINTS = {
    "arifos": "http://127.0.0.1:8088",
    "aforge": "http://127.0.0.1:7072",
    "geox": "http://127.0.0.1:8081",
    "wealth": "http://127.0.0.1:18082",
    "well": "http://127.0.0.1:18083",
    # flame RETIRED 2026-09-04 -> FED flash lane
    "fed": "http://127.0.0.1:7074",
}

COLLECTION_CLASS = "skill_mesh"  # → arifOS_skill_mesh (memory_classes.yaml)
MEMORY_TIER = "canon"
STATE_FILE = Path("/root/.local/share/arifos/mcp_discovery_state.json")


def fetch_tools(endpoint: str) -> list[dict]:
    """Fetch tools/list from an MCP server."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
    }
    try:
        req = urllib.request.Request(
            f"{endpoint}/mcp",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        tools = data.get("result", {}).get("tools", [])
        return tools
    except Exception as e:
        return []


def main():
    print("🔍 MCP Auto-Discovery Watcher — P2.9 (FederationMemory)")
    fm = FederationMemory(
        actor_id="aaa-mcp-discovery",
        session_id=os.getenv("ARIFOS_SESSION_ID", "system"),
    )

    # Load previous state
    previous_state = {}
    if STATE_FILE.exists():
        previous_state = json.loads(STATE_FILE.read_text())

    discovered = {}
    indexed = 0
    new_tools = 0

    for organ, endpoint in MCP_ENDPOINTS.items():
        try:
            tools = fetch_tools(endpoint)
        except Exception:
            tools = []

        discovered[organ] = {"endpoint": endpoint, "tool_count": len(tools), "tools": []}

        for tool in tools:
            tool_name = tool.get("name", "unknown")
            tool_desc = tool.get("description", "")
            discovered[organ]["tools"].append(tool_name)

            skill_id = f"{organ}/{tool_name}"
            if skill_id in previous_state.get("indexed_tools", {}):
                continue  # Already indexed

            # Classify capability tier
            tier = "fed-agent-subagent"  # Default
            desc_lower = (tool_name + " " + tool_desc).lower()
            if any(k in desc_lower for k in ["seismic", "geology", "basin", "petrophysic"]):
                tier = "fed-reasoning-heavy"
            elif any(k in desc_lower for k in ["image", "vision", "screenshot"]):
                tier = "fed-multimodal-vision"
            elif any(k in desc_lower for k in ["ingest", "document", "pdf"]):
                tier = "fed-long-context"

            # Store tool affordance via adapter (kernel owns embedding)
            fm.store(
                content={
                    "skill_id": skill_id,
                    "name": tool_name,
                    "description": tool_desc[:500],
                    "capability_tier": tier,
                    "ecology_state": "WARM",
                    "total_invocations": 0,
                    "success_count": 0,
                    "avg_latency_ms": 0.0,
                    "source": f"mcp-discovery/{organ}",
                },
                tier=MEMORY_TIER,
                collection_class=COLLECTION_CLASS,
                tags=["skill-mesh", "mcp-discovery", f"organ:{organ}", f"capability-tier:{tier}"],
                source_type="mcp_tool_discovery",
                source_uri=f"{endpoint}/mcp",
            )
            indexed += 1
            new_tools += 1

    # Save state
    state = {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "endpoints": len(MCP_ENDPOINTS),
        "total_tools": sum(d["tool_count"] for d in discovered.values()),
        "indexed_tools": {
            **previous_state.get("indexed_tools", {}),
            **{f"{org}/{t}": True for org, d in discovered.items() for t in d.get("tools", [])},
        },
        "new_indexed": new_tools,
        "organs": discovered,
    }
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

    for organ, d in discovered.items():
        print(f"   {organ}: {d['tool_count']} tools at {d['endpoint']}")
    print(f"   Newly indexed: {new_tools} tools")
    print(f"   State file: {STATE_FILE}")
    return state


if __name__ == "__main__":
    result = main()
    print(f"\n📊 DISCOVERY: {result['total_tools']} tools across {result['endpoints']} organs")
