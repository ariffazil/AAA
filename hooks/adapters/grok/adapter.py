#!/usr/bin/env python3
"""
grok/adapter.py — xAI Grok CLI Adapter for AAA Hook Mesh
Canonical Path: /root/AAA/hooks/adapters/grok/adapter.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 6 · built 2026-09-25 (F13 "buat adapter grok/gemini")

Maps Grok-native lifecycle events onto the canonical aaa.hook-event.v1
envelope. Surface verified against /root/.grok/README.md (bundled CLI docs,
2026-09-23 metadata): hooks run on "tool and session lifecycle events
(pre/post-tool-use, session start/end)". Only those four events are wired;
anything else arrives via shim as unmapped aaa.turn.received (void guard).

Coverage DECLARED, not assumed (FP-04): UserPromptSubmit / Stop / Compact /
Subagent events are NOT documented for Grok — absent here, never faked.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))

from adapter_contract import HarnessAdapter
from event_schema import ActionPayload, HookEvent
from decision_schema import HookDecision

# Grok native event → canonical aaa.hook-event.v1 event (documented surface only).
GROK_EVENT_MAP: Dict[str, str] = {
    "SessionStart": "aaa.session.opened",
    "PreToolUse":    "aaa.action.proposed",
    "PostToolUse":   "aaa.action.completed",
    "SessionEnd":    "aaa.session.sealing",
}

SHELL_TOOLS = frozenset({"Bash", "Shell", "shell"})
WRITE_TOOLS = frozenset({"Write", "Edit", "MultiEdit", "ApplyPatch"})


def _risk_class(tool_name: Optional[str]) -> str:
    if tool_name in SHELL_TOOLS:
        return "R3"
    if tool_name in WRITE_TOOLS:
        return "R2"
    return "R1"


def _action_kind(native_event: str, tool_name: Optional[str]) -> str:
    if native_event == "PostToolUse":
        return "execute" if tool_name in SHELL_TOOLS else "write" if tool_name in WRITE_TOOLS else "read"
    if native_event == "PreToolUse":
        return "execute" if tool_name in SHELL_TOOLS else "write" if tool_name in WRITE_TOOLS else "read"
    if native_event == "SessionEnd":
        return "seal"
    return "unknown"


class GrokAdapter(HarnessAdapter):
    """Adapter for xAI Grok CLI lifecycle events (hook surface per bundled README)."""

    @property
    def harness_name(self) -> str:
        return "grok"

    @property
    def supported_events(self) -> List[str]:
        return sorted(set(GROK_EVENT_MAP.values()))

    @property
    def native_events(self) -> List[str]:
        return sorted(GROK_EVENT_MAP.keys())

    def is_degraded(self, native_event: str) -> bool:
        return False  # no lossy mappings on the documented four

    def to_canonical(self, raw_payload: Dict[str, Any], event_name: str) -> HookEvent:
        canonical = GROK_EVENT_MAP.get(event_name)
        if canonical is None:
            raise ValueError(f"Unknown Grok event: {event_name!r}")

        tool_name = raw_payload.get("tool_name") or raw_payload.get("toolName")
        session_id = raw_payload.get("session_id") or raw_payload.get("sessionId") or "grok-session"

        action = None
        if canonical in ("aaa.action.proposed", "aaa.action.completed"):
            action = ActionPayload(
                tool_name=str(tool_name) if tool_name else "unknown",
                arguments={},
                kind=_action_kind(event_name, tool_name),
                risk_class=_risk_class(tool_name),
                resource_class="unknown",
            )

        metadata: Dict[str, Any] = {
            "native_event": event_name,
            "harness_version": raw_payload.get("version") or "unknown",
        }
        if raw_payload.get("tool_input") is not None:
            metadata["has_tool_input"] = True  # digest-flag only, never raw args

        return HookEvent(
            event_name=canonical,
            harness_id=self.harness_name,
            session_id=str(session_id),
            action=action,
            risk_class=action.risk_class if action else "R0",
            metadata=metadata,
        )

    def from_canonical(self, decision: HookDecision) -> Dict[str, Any]:
        # Grok hook response schema is undocumented for decision semantics; the
        # shim is advisory-only (FP-02) so this shape is telemetry, not a wire.
        return {
            "verdict": decision.verdict,
            "event_id": decision.event_id,
            "advisory": True,
        }
