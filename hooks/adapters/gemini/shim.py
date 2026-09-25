#!/usr/bin/env python3
"""
gemini/shim.py — sensor shim for the declared-absent Gemini hook surface.
Canonical Path: /root/AAA/hooks/adapters/gemini/shim.py

FP-02: sensors, never judges. FP-04: absent declared, never faked.
This shim exists so that IF a gemini hook ever fires (future CLI version,
experimental flag), the event still reaches the mesh spool as an honestly
unmapped aaa.turn.received instead of vanishing. It maps nothing today.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))

from event_schema import scaffold_event, validate_event  # noqa: E402

SPOOL_DIR = Path("/var/spool/arifos/hook-events")
FALLBACK_SPOOL_DIR = Path("/tmp/arifos-hook-events")


def main() -> int:
    native_event = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    try:
        if sys.stdin.isatty():
            raw = {}
        else:
            data = sys.stdin.read()
            raw = json.loads(data) if data.strip() else {}
    except Exception:
        raw = {}

    envelope = scaffold_event(
        "aaa.turn.received",
        agent_id=str(raw.get("agent_id") or "gemini-agent"),
        harness="gemini",
        session_id=str(raw.get("session_id") or raw.get("sessionId") or "gemini-session"),
        kind="unknown",
        tool_id=str(raw.get("tool_name") or raw.get("toolName") or "") or None,
        risk_class="R0",
        source_trust="internal",
        payload={
            "native_event": native_event,
            "mapped": False,
            "absent_surface": True,  # every gemini event today is unmapped-class
            "degraded": True,
        },
    )
    ok, errs = validate_event(envelope)

    try:
        SPOOL_DIR.mkdir(parents=True, exist_ok=True)
        spool = SPOOL_DIR
    except Exception:
        FALLBACK_SPOOL_DIR.mkdir(parents=True, exist_ok=True)
        spool = FALLBACK_SPOOL_DIR

    line = json.dumps({"valid": ok, "errors": errs, "event": envelope}, separators=(",", ":"))
    try:
        with open(spool / "gemini.jsonl", "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

    print(json.dumps({
        "supplemental": {
            "mesh_event_id": envelope["event_id"],
            "mesh_trace_id": envelope["trace_id"],
            "canonical_event": "aaa.turn.received",
            "validated": ok,
            "unmapped_native": True,
            "absent_surface": True,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
