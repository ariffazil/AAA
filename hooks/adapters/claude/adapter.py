#!/usr/bin/env python3
"""
claude/adapter.py — Claude Code Native Hooks Adapter for AAA Hook Mesh
Canonical Path: /root/AAA/hooks/adapters/claude/adapter.py
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

CLAUDE_EVENT_MAP = {
    "SessionStart": "aaa.session.opened",
    "PreToolUse": "aaa.action.proposed",
    "PostToolUse": "aaa.action.completed",
    "SessionEnd": "aaa.session.sealing",
}


class ClaudeCodeAdapter(HarnessAdapter):
    """Adapter for Claude Code hook events."""

    @property
    def harness_name(self) -> str:
        return "claude_code"

    @property
    def supported_events(self) -> List[str]:
        return [
            "aaa.session.opened",
            "aaa.turn.received",
            "aaa.action.proposed",
            "aaa.action.completed",
            "aaa.session.sealing",
        ]

    def to_canonical(self, raw_payload: Dict[str, Any], event_name: str) -> HookEvent:
        canonical_event = CLAUDE_EVENT_MAP.get(event_name, event_name)
        tool_name = raw_payload.get("tool_name") or raw_payload.get("tool", "")
        args = raw_payload.get("tool_input") or raw_payload.get("arguments", {})
        session_id = raw_payload.get("session_id", "claude-default")

        target_path = None
        if isinstance(args, dict):
            target_path = (
                args.get("path")
                or args.get("file_path")
                or args.get("file")
                or args.get("command")
            )

        action = None
        if tool_name:
            action = ActionPayload(
                tool_name=tool_name,
                arguments=args,
                target_path=str(target_path) if target_path else None,
            )

        risk_class = raw_payload.get("risk_class", "R1")
        if tool_name in ("Bash", "Edit", "Write", "Replace"):
            risk_class = "R2"

        return HookEvent(
            event_name=canonical_event,
            harness_id="claude_code",
            session_id=session_id,
            action=action,
            risk_class=risk_class,
            metadata={"raw_claude_event": event_name},
        )

    def from_canonical(self, decision: HookDecision) -> Dict[str, Any]:
        is_allowed = decision.verdict in ("ALLOW", "ALLOW_WITH_CONSTRAINTS")
        return {
            "continue": is_allowed,
            "verdict": decision.verdict,
            "message": decision.message,
            "reason_codes": decision.reason_codes,
            "event_id": decision.event_id,
        }
