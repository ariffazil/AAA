#!/usr/bin/env python3
"""
hermes/adapter.py — Hermes ASI Hooks Adapter for AAA Hook Mesh
Canonical Path: /root/AAA/hooks/adapters/hermes/adapter.py
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

HERMES_EVENT_MAP = {
    "session_boot": "aaa.session.opened",
    "message_received": "aaa.turn.received",
    "tool_executed": "aaa.action.completed",
    "session_close": "aaa.session.sealing",
}


class HermesAdapter(HarnessAdapter):
    """Adapter for Hermes telemetry and lifecycle events."""

    @property
    def harness_name(self) -> str:
        return "hermes"

    @property
    def supported_events(self) -> List[str]:
        return [
            "aaa.session.opened",
            "aaa.turn.received",
            "aaa.action.completed",
            "aaa.session.sealing",
        ]

    def to_canonical(self, raw_payload: Dict[str, Any], event_name: str) -> HookEvent:
        canonical_event = HERMES_EVENT_MAP.get(event_name, event_name)
        session_id = raw_payload.get("session_id", "hermes-default")
        tool_name = raw_payload.get("skill") or raw_payload.get("tool", "")

        action = None
        if tool_name:
            action = ActionPayload(
                tool_name=tool_name,
                arguments=raw_payload.get("args", {}),
                target_path=raw_payload.get("target"),
            )

        return HookEvent(
            event_name=canonical_event,
            harness_id="hermes",
            session_id=session_id,
            action=action,
            risk_class=raw_payload.get("risk_class", "R1"),
            metadata={"raw_hermes_event": event_name},
        )

    def from_canonical(self, decision: HookDecision) -> Dict[str, Any]:
        return {
            "hermes_status": "PROCEED" if decision.verdict in ("ALLOW", "ALLOW_WITH_CONSTRAINTS") else "HOLD",
            "verdict": decision.verdict,
            "message": decision.message,
            "event_id": decision.event_id,
        }
