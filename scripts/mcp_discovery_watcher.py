#!/usr/bin/env python3
"""
P2.9 — MCP Auto-Discovery Watcher
===================================
Endpoint poller that discovers new MCP servers, extracts their tool surface,
embeds the capability descriptions, and auto-indexes into Qdrant.

Architecture:
  1. Poll known MCP endpoints (:8088, :7072, :8081, :18082, :18083, :18901)
  2. Fetch tools/list from each
  3. Embed tool descriptions using all-MiniLM-L6-v2
  4. Upsert into Qdrant arifOS_skill_mesh (skill_id = tool name)
  5. Detect new/removed tools since last scan

Forged: 2026-08-10 by 333-AGI under F13 directive.
"""

import json
import time
import urllib.request
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# ── Config ────────────────────────────────────────────────────────
MCP_ENDPOINTS = {
    "arifos": "http://127.0.0.1:8088",
    "aforge": "http://127.0.0.1:7072",
    "geox": "http://127.0.0.1:8081",
    "wealth": "http://127.0.0.1:18082",
    "well": "http://127.0.0.1:18083",
    "flame": "http://127.0.0.1:18901",
    "fed": "http://127.0.0.1:7074",
}

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION = "arifOS_skill_mesh"
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
    print("🔍 MCP Auto-Discovery Watcher — P2.9")
    encoder = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

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

            # Embed tool description
            text = f"{tool_name}: {tool_desc}" if tool_desc else tool_name
            vector = encoder.encode(text).tolist()

            # Classify capability tier
            tier = "fed-agent-subagent"  # Default
            desc_lower = (tool_name + " " + tool_desc).lower()
            if any(k in desc_lower for k in ["seismic", "geology", "basin", "petrophysic"]):
                tier = "fed-reasoning-heavy"
            elif any(k in desc_lower for k in ["image", "vision", "screenshot"]):
                tier = "fed-multimodal-vision"
            elif any(k in desc_lower for k in ["ingest", "document", "pdf"]):
                tier = "fed-long-context"

            point_id = abs(hash(skill_id)) % (2**63)
            client.upsert(
                collection_name=COLLECTION,
                points=[
                    {
                        "id": point_id,
                        "vector": vector,
                        "payload": {
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
                    }
                ],
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
