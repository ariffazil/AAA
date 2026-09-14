#!/usr/bin/env python3
"""
well/adapter.py — WELL Organ Dignity & Biometric Hooks Adapter for AAA Hook Mesh
Canonical Path: /root/AAA/hooks/adapters/well/adapter.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 6 & F6 MARUAH
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))

from adapter_contract import HarnessAdapter
from event_schema import ActionPayload, HookEvent, utc_now_iso
from decision_schema import HookDecision

WELL_EVENT_MAP = {
    "well.session.init": "aaa.session.opened",
    "well.boundary.check": "aaa.action.proposed",
    "well.biometric.log": "aaa.action.completed",
    "well.dignity.violation": "aaa.policy.violation",
}


class WellAdapter(HarnessAdapter):
    """Adapter for WELL organ dignity, biometric, and substrate events."""

    @property
    def harness_name(self) -> str:
        return "well"

    @property
    def supported_events(self) -> List[str]:
        return [
            "aaa.session.opened",
            "aaa.action.proposed",
            "aaa.action.completed",
            "aaa.policy.violation",
        ]

    def to_canonical(self, raw_payload: Dict[str, Any], event_name: str) -> HookEvent:
        canonical_event = WELL_EVENT_MAP.get(event_name, event_name)
        session_id = raw_payload.get("session_id", "well-stream")
        tool_name = raw_payload.get("metric") or raw_payload.get("tool", "")

        action = None
        if tool_name:
            action = ActionPayload(
                tool_name=tool_name,
                arguments=raw_payload.get("data", {}),
            )

        return HookEvent(
            event_name=canonical_event,
            harness_id="well",
            session_id=session_id,
            action=action,
            risk_class="R1",
            metadata={"raw_well_event": event_name},
        )

    def from_canonical(self, decision: HookDecision) -> Dict[str, Any]:
        return {
            "dignity_passed": decision.verdict in ("ALLOW", "ALLOW_WITH_CONSTRAINTS"),
            "verdict": decision.verdict,
            "constitutional_floors": decision.constitutional_floors,
            "message": decision.message,
            "event_id": decision.event_id,
        }
