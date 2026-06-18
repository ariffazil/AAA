#!/usr/bin/env python3
"""AAA NATS Publish — Push session telemetry to federation memory bus."""
from __future__ import annotations

import json
import socket
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hook_lib as h


def main() -> None:
    event = h.read_event()
    session_id = event.get("session_id", "unknown")
    hook_event = event.get("hook_event_name", "Stop")
    if event.get("stop_hook_active"):
        return

    seal_file = h.TELEMETRY_DIR / f"seal-{session_id}.jsonl"
    verdict = "UNKNOWN"
    avg_delta = 0.0
    max_delta = 0.0
    session_events = 0
    high_risk = 0

    try:
        if seal_file.exists() and seal_file.stat().st_size > 0:
            with seal_file.open() as f:
                lines = f.readlines()
            last = json.loads(lines[-1])
            verdict = last.get("verdict", "UNKNOWN")
            avg_delta = last.get("thermodynamics", {}).get("dS_session_avg", 0.0)
            max_delta = last.get("thermodynamics", {}).get("dS_session_max", 0.0)
            session_events = last.get("telemetry", {}).get("session_events", 0)
            high_risk = last.get("telemetry", {}).get("high_risk_actions", 0)
    except Exception:
        pass

    payload = {
        "agent": "opencode-bot",
        "session_id": session_id,
        "timestamp": h.now_utc(),
        "epoch": int(__import__("time").time()),
        "host": socket.gethostname(),
        "event": hook_event,
        "verdict": verdict,
        "thermodynamics": {"dS_session_avg": avg_delta, "dS_session_max": max_delta},
        "telemetry": {"session_events": session_events, "high_risk_actions": high_risk},
    }

    published = False
    try:
        result = subprocess.run(
            ["nats", "pub", "agent.memory.opencode", json.dumps(payload)],
            capture_output=True,
            text=True,
            timeout=5,
        )
        published = result.returncode == 0
    except Exception:
        pass

    h.allow(
        hook_event,
        f"[CLAIM] NATS publish: agent.memory.opencode | verdict={verdict} | events={session_events} | high_risk={high_risk}",
        {
            "nats_published": published,
            "nats_subject": "agent.memory.opencode",
            "session_id": session_id,
        },
    )


if __name__ == "__main__":
    main()
