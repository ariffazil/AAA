#!/usr/bin/env python3
"""AAA SESSION-START — Bind epoch, init telemetry, warm caches."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hook_lib as h


def main() -> None:
    event = h.read_event()
    session_id = event.get("session_id", "unknown")
    source = event.get("source", "startup")
    cwd = event.get("cwd", "/root")
    hook_event = event.get("hook_event_name", "SessionStart")
    epoch = int(__import__("time").time())

    h.ensure_dirs()

    # ── Kernel handshake: mint governed session envelope (best-effort) ──
    envelope = Path("/root/.arifos/federation-session.json")
    if not envelope.exists():
        try:
            subprocess.run(
                ["python3", "/root/scripts/federation_ritual.py", "init",
                 "--actor", "opencode", "--intent", "substrate session start",
                 "--write-envelope", str(envelope), "--quiet"],
                check=False, timeout=15,
            )
        except Exception:
            pass  # best-effort — don't block OpenCode startup

    h.audit_log(
        {
            "type": "opencode-session-start",
            "timestamp": h.now_utc(),
            "session_id": session_id,
            "hook_event": hook_event,
            "source": source,
            "epoch": epoch,
            "cwd": cwd,
            "seal_status": "OPEN",
        }
    )

    health_status = "unknown"
    compose = Path("/root/compose/docker-compose.yml")
    if compose.exists():
        try:
            result = subprocess.run(
                ["docker", "compose", "-f", str(compose), "ps"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            health_status = "federation_up" if "Up" in result.stdout else "federation_down"
        except Exception:
            health_status = "federation_down"

    reason = f"[CLAIM] AAA SessionStart: epoch={epoch}, source={source}, health={health_status}. Full autonomy granted. Telemetry active."
    h.allow(
        hook_event,
        reason,
        {
            "epoch": epoch,
            "source": source,
            "health_status": health_status,
            "telemetry_path": str(h.AUDIT_LOG),
        },
    )


if __name__ == "__main__":
    main()
