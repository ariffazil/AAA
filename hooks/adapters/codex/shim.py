#!/usr/bin/env python3
"""
codex/shim.py — stdin/stdout sensor shim: Codex hook → AAA Hook Mesh
Canonical Path: /root/AAA/hooks/adapters/codex/shim.py

Law (FP-02, ratified): HOOKS ARE SENSORS, NOT JUDGES.
This shim converts a Codex-native hook payload into a canonical
aaa.hook-event.v1 envelope, validates it, appends it to the mesh evidence
spool, and returns an advisory JSON supplement. It NEVER returns a blocking
verdict and NEVER exits non-zero for policy reasons — enforcement lives in
the kernel (forge_shell / ArifJudge / mcp_guard), which this shim cannot
and must not replicate.

Usage (from hooks.json):
  python3 /root/AAA/hooks/adapters/codex/shim.py <NativeEventName>
Payload: harness JSON on stdin (missing/malformed payload degrades to {}).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from adapter import CODEX_EVENT_MAP, CodexAdapter  # noqa: E402
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

    adapter = CodexAdapter()
    canonical = CODEX_EVENT_MAP.get(native_event)

    if canonical is None:
        # Unknown native event: record as turn.received with metadata — an
        # unmapped event must not vanish (void guard: no data ≠ all clear).
        canonical = "aaa.turn.received"
        unmapped = True
    else:
        unmapped = False

    try:
        hook_event = adapter.to_canonical(raw, native_event) if not unmapped else None
    except Exception:
        hook_event = None

    tool_name = raw.get("tool_name") or raw.get("toolName")
    envelope = scaffold_event(
        canonical,
        agent_id=str(raw.get("agent_id") or "codex-agent"),
        harness="codex",
        session_id=str(raw.get("session_id") or raw.get("sessionId") or "codex-session"),
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
        with open(spool / "codex.jsonl", "a") as f:
            f.write(line + "\n")
    except Exception:
        pass  # sensor must never take the session down — evidence loss recorded below

    # Advisory supplement only. No blocking fields, no authority fields.
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
