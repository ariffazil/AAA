#!/usr/bin/env python3
"""
arifOS Graphiti Memory Bridge — Session Boot Integration
Forged: 2026-07-31 · Session: SEAL-06ca329779e642e9

Loads temporal knowledge graph context from Graphiti at session start,
merging it with carry_forward.json for comprehensive agent memory.

Usage:
    python3 graphiti_boot_context.py [--session-id SEAL-xxx]
"""

import json
import sys
import os
from datetime import datetime, timezone

GRAPHITI_MCP_URL = os.environ.get("GRAPHITI_MCP_URL", "http://localhost:8000/mcp")
CARRY_FORWARD_PATH = os.path.expanduser("~/.local/share/arifos/carry_forward.json")
BOOT_CONTEXT_PATH = os.path.expanduser("~/.local/share/arifos/graphiti_boot_context.json")


def query_graphiti_nodes(query: str, max_nodes: int = 5) -> dict:
    """Query Graphiti for relevant nodes via MCP."""
    import urllib.request

    payload = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "search_nodes", "arguments": {"query": query, "max_nodes": max_nodes}},
        }
    ).encode()

    req = urllib.request.Request(
        GRAPHITI_MCP_URL,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e), "source": "graphiti_query"}


def query_graphiti_facts(query: str, max_facts: int = 5) -> dict:
    """Query Graphiti for relevant facts."""
    import urllib.request

    payload = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "search_memory_facts", "arguments": {"query": query, "max_facts": max_facts}},
        }
    ).encode()

    req = urllib.request.Request(
        GRAPHITI_MCP_URL,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e), "source": "graphiti_facts"}


def load_carry_forward() -> dict:
    """Load the existing carry_forward.json."""
    try:
        with open(CARRY_FORWARD_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"_note": "no carry_forward.json found"}


def build_boot_context(session_id: str | None = None, task_intent: str | None = None) -> dict:
    """
    Build a comprehensive boot context from Graphiti + carry_forward.json.

    Queries:
    1. Federation topology (organs, agents)
    2. Model routing registry (providers, model status)
    3. Recent security events (permission changes, provider deaths)
    4. Task-specific context (based on intent keywords)
    """
    boot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "sources": {
            "graphiti": GRAPHITI_MCP_URL,
            "carry_forward": CARRY_FORWARD_PATH,
        },
        "graphiti_healthy": False,
    }

    # 1. Federation topology
    topo = query_graphiti_nodes("federation organs arifOS kernel agents trinity", max_nodes=8)
    if "error" not in topo:
        boot["graphiti_healthy"] = True
        boot["federation_topology"] = topo
    else:
        boot["federation_topology"] = {"error": topo.get("error", "unknown")}

    # 2. Model routing
    models = query_graphiti_facts("model routing provider deepseek qwen token plan status", max_facts=5)
    if "error" not in models:
        boot["model_routing"] = models
    else:
        boot["model_routing"] = {"error": models.get("error", "unknown")}

    # 3. Security events
    security = query_graphiti_facts("security event fix permission change provider death", max_facts=5)
    if "error" not in security:
        boot["security_events"] = security
    else:
        boot["security_events"] = {"error": security.get("error", "unknown")}

    # 4. Task-specific context
    if task_intent:
        task_ctx = query_graphiti_nodes(task_intent, max_nodes=5)
        if "error" not in task_ctx:
            boot["task_context"] = task_ctx
        else:
            boot["task_context"] = {"error": task_ctx.get("error", "unknown")}

    # 5. Merge carry_forward
    cf = load_carry_forward()
    boot["carry_forward"] = {
        "session_id": cf.get("session_id"),
        "open_loops": cf.get("open_loops_888_HOLD", []),
        "never_patterns": cf.get("never_patterns", []),
        "completed": cf.get("completed_this_session", []),
    }

    return boot


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Graphiti Boot Context Builder")
    parser.add_argument("--session-id", default=None, help="Current session ID")
    parser.add_argument("--intent", default=None, help="Task intent for targeted context")
    parser.add_argument("--output", default=BOOT_CONTEXT_PATH, help="Output path")
    parser.add_argument("--json", action="store_true", help="Print to stdout as JSON")

    args = parser.parse_args()

    boot_ctx = build_boot_context(session_id=args.session_id, task_intent=args.intent)

    # Write to boot context file
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(boot_ctx, f, indent=2, default=str)

    if args.json:
        print(json.dumps(boot_ctx, indent=2, default=str))
    else:
        print(f"Graphiti boot context written to {args.output}")
        print(f"  Healthy: {boot_ctx['graphiti_healthy']}")
        print(f"  Open loops: {len(boot_ctx.get('carry_forward', {}).get('open_loops', []))}")


if __name__ == "__main__":
    main()
