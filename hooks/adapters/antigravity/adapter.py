#!/usr/bin/env python3
"""
antigravity/adapter.py — Antigravity CLI Hooks Adapter for AAA Hook Mesh
Canonical Path: /root/AAA/hooks/adapters/antigravity/adapter.py
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

ANTIGRAVITY_EVENT_MAP = {
    "session_start": "aaa.session.opened",
    "pre_tool_call": "aaa.action.proposed",
    "post_tool_call": "aaa.action.completed",
    "post_tool_failure": "aaa.action.failed",
    "session_end": "aaa.session.sealing",
    "context_compact": "aaa.context.compacting",
}


class AntigravityAdapter(HarnessAdapter):
    """Adapter for Google Antigravity (AGY) CLI hook events."""

    @property
    def harness_name(self) -> str:
        return "antigravity"

    @property
    def supported_events(self) -> List[str]:
        return [
            "aaa.session.opened",
            "aaa.turn.received",
            "aaa.action.proposed",
            "aaa.action.completed",
            "aaa.action.failed",
            "aaa.session.sealing",
        ]

    def to_canonical(self, raw_payload: Dict[str, Any], event_name: str) -> HookEvent:
        canonical_event = ANTIGRAVITY_EVENT_MAP.get(event_name, event_name)
        tool_name = raw_payload.get("tool_name") or raw_payload.get("tool", "")
        args = raw_payload.get("tool_arguments") or raw_payload.get("arguments", {})
        session_id = raw_payload.get("session_id", "agy-default")

        target_path = None
        if isinstance(args, dict):
            target_path = (
                args.get("TargetFile")
                or args.get("AbsolutePath")
                or args.get("DirectoryPath")
                or args.get("CommandLine")
            )

        action = None
        if tool_name:
            action = ActionPayload(
                tool_name=tool_name,
                arguments=args,
                target_path=str(target_path) if target_path else None,
            )

        risk_class = raw_payload.get("risk_class", "R1")
        if tool_name in ("run_command", "write_to_file", "replace_file_content"):
            risk_class = "R2"

        return HookEvent(
            event_name=canonical_event,
            harness_id="antigravity",
            session_id=session_id,
            action=action,
            risk_class=risk_class,
            metadata={"raw_agy_event": event_name},
        )

    def from_canonical(self, decision: HookDecision) -> Dict[str, Any]:
        is_allowed = decision.verdict in ("ALLOW", "ALLOW_WITH_CONSTRAINTS")
        return {
            "status": "APPROVED" if is_allowed else "BLOCKED",
            "verdict": decision.verdict,
            "message": decision.message,
            "reason_codes": decision.reason_codes,
            "risk_class": decision.risk_class,
            "event_id": decision.event_id,
        }
