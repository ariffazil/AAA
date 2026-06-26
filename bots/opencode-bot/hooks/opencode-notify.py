#!/usr/bin/env python3
"""AAA NOTIFY — Surface attention events without blocking."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hook_lib as h


def main() -> None:
    event = h.read_event()
    session_id = event.get("session_id", "unknown")
    sink = event.get("sink", "unknown")
    notif_type = event.get("notification_type", "unknown")
    title = event.get("title", "")
    body = event.get("body", "")
    severity = event.get("severity", "info")
    hook_event = event.get("hook_event_name", "Notification")

    h.audit_log(
        {
            "type": "opencode-notify",
            "timestamp": h.now_utc(),
            "session_id": session_id,
            "hook_event": hook_event,
            "sink": sink,
            "notification_type": notif_type,
            "title": title,
            "body": body,
            "severity": severity,
        }
    )

    if notif_type == "permission_prompt" or severity in ("warning", "error"):
        reason = f"[CLAIM] AAA Notify: Attention required — {severity} | {title} | {body}. Agent autonomy preserved."
    else:
        reason = f"[PLAUSIBLE] AAA Notify: {severity} event logged silently."

    h.allow(
        hook_event,
        reason,
        {"severity": severity, "notif_type": notif_type, "audit_logged": True},
    )


if __name__ == "__main__":
    main()
