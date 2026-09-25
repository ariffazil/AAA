#!/usr/bin/env python3
"""
grok/shim.py — stdin/stdout sensor shim: Grok hook → AAA Hook Mesh
Canonical Path: /root/AAA/hooks/adapters/grok/shim.py

Law (FP-02, ratified): HOOKS ARE SENSORS, NOT JUDGES.
Converts a Grok-native hook payload into a canonical aaa.hook-event.v1
envelope, validates it, appends it to the mesh evidence spool, and prints an
advisory JSON supplement. NEVER blocks, never exits non-zero for policy
reasons — enforcement lives in the kernel.

Usage (from hooks.json / [[hooks.<Event>]] command):
  python3 /root/AAA/hooks/adapters/grok/shim.py <NativeEventName>
Payload: harness JSON on stdin (missing/malformed degrades to {}).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from adapter import GROK_EVENT_MAP, GrokAdapter  # noqa: E402
from event_schema import scaffold_event, validate_event  # noqa: E402

SPOOL_DIR = Path("/var/spool/arifos/hook-events")
FALLBACK_SPOOL_DIR = Path("/tmp/arifos-hook-events")


def _read_payload() -> dict:
    try:
        if sys.stdin.isatty():
            return {}
        data = sys.stdin.read()
        return json.loads(data) if data.strip() else {}
    except Exception:
        return {}


def _spool_dir() -> Path:
    try:
        SPOOL_DIR.mkdir(parents=True, exist_ok=True)
        return SPOOL_DIR
    except Exception:
        FALLBACK_SPOOL_DIR.mkdir(parents=True, exist_ok=True)
        return FALLBACK_SPOOL_DIR


def main() -> int:
    native_event = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    raw = _read_payload()

    adapter = GrokAdapter()
    canonical = GROK_EVENT_MAP.get(native_event)
    unmapped = canonical is None
    if canonical is None:
        canonical = "aaa.turn.received"  # unmapped events must not vanish

    try:
        hook_event = adapter.to_canonical(raw, native_event) if not unmapped else None
    except Exception:
        hook_event = None

    tool_name = raw.get("tool_name") or raw.get("toolName")
    envelope = scaffold_event(
        canonical,
        agent_id=str(raw.get("agent_id") or "grok-agent"),
        harness="grok",
        session_id=str(raw.get("session_id") or raw.get("sessionId") or "grok-session"),
        kind=hook_event.action.kind if hook_event and hook_event.action else "unknown",
        tool_id=str(tool_name) if tool_name else None,
        risk_class=hook_event.risk_class if hook_event else "R0",
        source_trust="internal",
        payload={
            "native_event": native_event,
            "mapped": not unmapped,
            "degraded": adapter.is_degraded(native_event) if not unmapped else True,
        },
    )
    ok, errs = validate_event(envelope)

    spool = _spool_dir()
    line = json.dumps({"valid": ok, "errors": errs, "event": envelope}, separators=(",", ":"))
    try:
        with open(spool / "grok.jsonl", "a") as f:
            f.write(line + "\n")
    except Exception:
        pass  # sensor must never take the session down

    print(json.dumps({
        "supplemental": {
            "mesh_event_id": envelope["event_id"],
            "mesh_trace_id": envelope["trace_id"],
            "canonical_event": canonical,
            "validated": ok,
            "unmapped_native": unmapped,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
