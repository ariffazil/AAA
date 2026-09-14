#!/usr/bin/env python3
"""
opencode/adapter.py — OpenCode Native Plugin Adapter for AAA Hook Mesh
Canonical Path: /root/AAA/hooks/adapters/opencode/adapter.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 6
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add lib to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))

from adapter_contract import HarnessAdapter
from event_schema import ActionPayload, HookEvent, utc_now_iso
from decision_schema import HookDecision

OPENCODE_EVENT_MAP = {
    "session.start": "aaa.session.opened",
    "tool.execute.before": "aaa.action.proposed",
    "tool.execute.after": "aaa.action.completed",
    "session.end": "aaa.session.sealing",
    "permission.ask": "aaa.action.proposed",
    "session.idle": "aaa.turn.idle",
}


class OpenCodeAdapter(HarnessAdapter):
    """Adapter for OpenCode plugin hook events."""

    @property
    def harness_name(self) -> str:
        return "opencode"

    @property
    def supported_events(self) -> List[str]:
        return [
            "aaa.session.opened",
            "aaa.turn.received",
            "aaa.action.proposed",
            "aaa.action.completed",
            "aaa.turn.idle",
            "aaa.session.sealing",
            "aaa.policy.violation",
        ]

    def to_canonical(self, raw_payload: Dict[str, Any], event_name: str) -> HookEvent:
        canonical_event = OPENCODE_EVENT_MAP.get(event_name, event_name)
        tool_name = raw_payload.get("tool") or raw_payload.get("tool_name", "")
        args = raw_payload.get("parameters") or raw_payload.get("args", {})
        session_id = raw_payload.get("session_id", "opencode-default")

        # Extract target path if present in parameters
        target_path = None
        if isinstance(args, dict):
            target_path = (
                args.get("path")
                or args.get("file_path")
                or args.get("target_file")
                or args.get("cwd")
            )

        action = None
        if tool_name:
            action = ActionPayload(
                tool_name=tool_name,
                arguments=args,
                target_path=target_path,
            )

        # Infer risk class
        risk_class = raw_payload.get("risk_class", "R1")
        if tool_name in ("bash", "write", "edit"):
            risk_class = "R2"

        return HookEvent(
            event_name=canonical_event,
            harness_id="opencode",
            session_id=session_id,
            action=action,
            risk_class=risk_class,
            metadata={"raw_opencode_event": event_name},
        )

    def from_canonical(self, decision: HookDecision) -> Dict[str, Any]:
        is_allowed = decision.verdict in ("ALLOW", "ALLOW_WITH_CONSTRAINTS")
        return {
            "allow": is_allowed,
            "verdict": decision.verdict,
            "reason": decision.message,
            "reason_codes": decision.reason_codes,
            "risk_class": decision.risk_class,
            "event_id": decision.event_id,
        }
