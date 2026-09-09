#!/usr/bin/env python3
"""
trace_emitter.py — Universal Experience Trace Emitter
=====================================================
Any agent can call this to emit an experience trace to the shared store.

Usage:
    python3 trace_emitter.py --agent <agent_id> --tool <tool_name> --success <true|false> [--feedback <text>]
    python3 trace_emitter.py --json '{"agent_id":"openclaw","action":{"tool":"forge_shell"},"observation":{"success":true}}'

Output: appends JSONL line to /root/VAULT999/experience/traces.jsonl
Also syncs to /root/.local/share/arifos/world-model/experience_traces.jsonl
"""

import json
import hashlib
import sys
import os
import time
from datetime import datetime, timezone
from pathlib import Path

SHARED_STORE = Path("/root/VAULT999/experience/traces.jsonl")
LOCAL_STORE = Path("/root/.local/share/arifos/world-model/experience_traces.jsonl")


def emit_trace(agent_id: str, tool: str, success: bool, feedback: str = "", input_data: str = "") -> dict:
    """Emit a single experience trace to shared store."""
    now = datetime.now(timezone.utc)
    trace = {
        "trace_id": f"exp-{int(time.time()*1000)}-{agent_id}",
        "seq": int(time.time()),
        "ts": now.isoformat(),
        "agent_id": agent_id,
        "action": {
            "tool": tool,
            "input_hash": hashlib.sha256(input_data.encode()).hexdigest()[:16] if input_data else None,
        },
        "observation": {
            "success": success,
            "output_hash": None,
        },
        "feedback": {
            "self": feedback if feedback else None,
            "environmental": None,
            "constitutional": None,
        },
    }

    line = json.dumps(trace, ensure_ascii=False)

    # Append to shared store
    SHARED_STORE.parent.mkdir(parents=True, exist_ok=True)
    with open(SHARED_STORE, "a") as f:
        f.write(line + "\n")

    # Also sync to local store (backward compat)
    LOCAL_STORE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCAL_STORE, "a") as f:
        f.write(line + "\n")

    return trace


def main():
    if "--json" in sys.argv:
        idx = sys.argv.index("--json")
        data = json.loads(sys.argv[idx + 1])
        trace = emit_trace(
            agent_id=data.get("agent_id", "unknown"),
            tool=data.get("action", {}).get("tool", "unknown"),
            success=data.get("observation", {}).get("success", False),
            feedback=data.get("feedback", {}).get("self", ""),
        )
    else:
        agent_id = "unknown"
        tool = "unknown"
        success = False
        feedback = ""

        for i, arg in enumerate(sys.argv):
            if arg == "--agent" and i + 1 < len(sys.argv):
                agent_id = sys.argv[i + 1]
            elif arg == "--tool" and i + 1 < len(sys.argv):
                tool = sys.argv[i + 1]
            elif arg == "--success" and i + 1 < len(sys.argv):
                success = sys.argv[i + 1].lower() == "true"
            elif arg == "--feedback" and i + 1 < len(sys.argv):
                feedback = sys.argv[i + 1]

        trace = emit_trace(agent_id, tool, success, feedback)

    print(json.dumps({"emitted": True, "trace_id": trace["trace_id"], "store": str(SHARED_STORE)}, indent=2))


if __name__ == "__main__":
    main()
