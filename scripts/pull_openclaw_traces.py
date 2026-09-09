#!/usr/bin/env python3
"""
pull_openclaw_traces.py — Pull experience traces from KVM4 OpenClaw
====================================================================
Pulls traces from OpenClaw's trace store on KVM4 and appends to
/root/VAULT999/experience/traces.jsonl (shared federation store).

Run via cron every 30 minutes or on-demand.

KVM4 OpenClaw stores traces at: /root/.local/share/arifos/world-model/experience_traces.jsonl
Access via: ssh or direct file read over Tailscale.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

KVM4_HOST = "100.64.0.5"
KVM4_TRACE_PATH = "/root/.local/share/arifos/world-model/experience_traces.jsonl"
SHARED_STORE = Path("/root/VAULT999/experience/traces.jsonl")
PULL_STATE = Path("/root/.local/share/arifos/openclaw_trace_pull_state.json")
KVM4_SSH = "ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no root@100.64.0.5"


def load_pull_state() -> dict:
    if PULL_STATE.exists():
        return json.loads(PULL_STATE.read_text())
    return {"last_line_count": 0, "last_pull_utc": None}


def save_pull_state(state: dict):
    PULL_STATE.parent.mkdir(parents=True, exist_ok=True)
    PULL_STATE.write_text(json.dumps(state, indent=2))


def pull_traces() -> int:
    """Pull new traces from KVM4. Returns count of new traces added."""
    state = load_pull_state()
    last_count = state.get("last_line_count", 0)

    try:
        # Get trace count on KVM4
        result = subprocess.run(
            f"{KVM4_SSH} 'wc -l < {KVM4_TRACE_PATH} 2>/dev/null || echo 0'",
            shell=True, capture_output=True, text=True, timeout=10
        )
        remote_count = int(result.stdout.strip())

        if remote_count <= last_count:
            return 0  # No new traces

        # Pull new lines (skip already-pulled lines)
        result = subprocess.run(
            f"{KVM4_SSH} 'tail -n +{last_count + 1} {KVM4_TRACE_PATH}'",
            shell=True, capture_output=True, text=True, timeout=15
        )

        if result.returncode != 0 or not result.stdout.strip():
            return 0

        new_lines = result.stdout.strip().split("\n")
        new_traces = [l for l in new_lines if l.strip()]

        if not new_traces:
            return 0

        # Tag each trace with source agent
        tagged = []
        for line in new_traces:
            try:
                trace = json.loads(line)
                # Add source tag if not present
                if "source_host" not in trace:
                    trace["source_host"] = "KVM4"
                if "source_agent" not in trace:
                    trace["source_agent"] = trace.get("agent_id", "openclaw")
                tagged.append(json.dumps(trace, ensure_ascii=False))
            except json.JSONDecodeError:
                tagged.append(line)  # Append raw if parse fails

        # Append to shared store
        SHARED_STORE.parent.mkdir(parents=True, exist_ok=True)
        with open(SHARED_STORE, "a") as f:
            for t in tagged:
                f.write(t + "\n")

        # Update state
        state["last_line_count"] = remote_count
        state["last_pull_utc"] = datetime.now(timezone.utc).isoformat()
        state["last_pull_count"] = len(tagged)
        save_pull_state(state)

        return len(tagged)

    except subprocess.TimeoutExpired:
        print(f"ERROR: KVM4 SSH timeout")
        return 0
    except Exception as e:
        print(f"ERROR: {e}")
        return 0


def main():
    count = pull_traces()
    if count > 0:
        print(f"Pulled {count} new traces from KVM4 OpenClaw → {SHARED_STORE}")
    else:
        print("No new traces from KVM4")


if __name__ == "__main__":
    main()
