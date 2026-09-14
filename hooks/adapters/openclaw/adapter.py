#!/usr/bin/env python3
"""
openclaw/adapter.py — OpenClaw Edge Hooks Adapter for AAA Hook Mesh
Canonical Path: /root/AAA/hooks/adapters/openclaw/adapter.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 6
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))

from adapter_contract import HarnessAdapter
from event_schema import ActionPayload, HookEvent, utc_now_iso
from decision_schema import HookDecision

OPENCLAW_EVENT_MAP = {
    "edge_init": "aaa.session.opened",
    "edge_tool_done": "aaa.action.completed",
    "edge_tool_error": "aaa.action.failed",
    "edge_shutdown": "aaa.session.sealing",
}


class OpenClawAdapter(HarnessAdapter):
    """Adapter for OpenClaw edge agent hook events."""

    @property
    def harness_name(self) -> str:
        return "openclaw"

    @property
    def supported_events(self) -> List[str]:
        return [
            "aaa.session.opened",
            "aaa.action.completed",
            "aaa.action.failed",
            "aaa.session.sealing",
        ]

    def to_canonical(self, raw_payload: Dict[str, Any], event_name: str) -> HookEvent:
        canonical_event = OPENCLAW_EVENT_MAP.get(event_name, event_name)
        session_id = raw_payload.get("session_id", "openclaw-edge")
        tool_name = raw_payload.get("command") or raw_payload.get("action", "")

        action = None
        if tool_name:
            action = ActionPayload(
                tool_name=tool_name,
                arguments=raw_payload.get("payload", {}),
            )

        return HookEvent(
            event_name=canonical_event,
            harness_id="openclaw",
            session_id=session_id,
            action=action,
            risk_class=raw_payload.get("risk_class", "R1"),
            metadata={"raw_openclaw_event": event_name},
        )

    def from_canonical(self, decision: HookDecision) -> Dict[str, Any]:
        return {
            "edge_allowed": decision.verdict in ("ALLOW", "ALLOW_WITH_CONSTRAINTS"),
            "verdict": decision.verdict,
            "reason": decision.message,
            "event_id": decision.event_id,
        }
