#!/usr/bin/env python3
"""
codex/adapter.py — OpenAI Codex CLI Adapter for AAA Hook Mesh
Canonical Path: /root/AAA/hooks/adapters/codex/adapter.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 6

Maps Codex native lifecycle events (protocol.rs HookEventName — 12 events)
onto the canonical aaa.hook-event.v1 envelope.

Coverage is DECLARED, not assumed: events with no clean canonical pair are
mapped DEGRADED and the original native name is preserved in metadata so
downstream consumers never mistake a lossy mapping for a lossless one.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))

from adapter_contract import HarnessAdapter
from event_schema import ActionPayload, HookEvent, utc_now_iso
from decision_schema import HookDecision

# Codex native event → canonical aaa.hook-event.v1 event.
# "DEGRADED:" comment marks lossy mappings (phase information kept in metadata).
CODEX_EVENT_MAP: Dict[str, str] = {
    "SessionStart":       "aaa.session.opened",
    "UserPromptSubmit":   "aaa.turn.received",
    "PreToolUse":         "aaa.action.proposed",
    "PermissionRequest":  "aaa.action.proposed",   # sub-kind: permission
    "PostToolUse":        "aaa.action.completed",
    "SubagentStart":      "aaa.action.proposed",   # action.kind = delegate
    "SubagentStop":       "aaa.action.completed",  # action.kind = delegate
    "Stop":               "aaa.turn.idle",
    "Interrupt":          "aaa.action.failed",
    "PreCompact":         "aaa.context.compacting",
    "PostCompact":        "aaa.context.compacting",  # DEGRADED: post-phase only
    "SessionEnd":         "aaa.session.sealing",
}

# Codex-native completion status → canonical action state metadata.
COMPLETE_EVENTS = frozenset({"PostToolUse", "SubagentStop"})
FAILED_EVENTS = frozenset({"Interrupt"})

SHELL_TOOLS = frozenset({"Bash", "Shell", "LocalShell", "shell"})
WRITE_TOOLS = frozenset({"Write", "Edit", "ApplyPatch", "apply_patch", "MultiEdit"})


def _risk_class(tool_name: Optional[str]) -> str:
    """Conservative R-ladder guess from the tool identity (advisory only)."""
    if tool_name in SHELL_TOOLS:
        return "R3"          # live/elevated — shell can reach anything
    if tool_name in WRITE_TOOLS:
        return "R2"          # bounded-reversible repo mutation
    return "R1"              # local-reversible default


def _action_kind(native_event: str, tool_name: Optional[str]) -> str:
    if native_event in {"SubagentStart", "SubagentStop"}:
        return "delegate"
    if native_event == "PermissionRequest":
        return "policy_change"
    if native_event in COMPLETE_EVENTS:
        return "execute" if tool_name in SHELL_TOOLS else "write" if tool_name in WRITE_TOOLS else "read"
    if native_event == "PreToolUse":
        return "execute" if tool_name in SHELL_TOOLS else "write" if tool_name in WRITE_TOOLS else "read"
    if native_event == "SessionEnd":
        return "seal"
    return "unknown"


class CodexAdapter(HarnessAdapter):
    """Adapter for OpenAI Codex CLI session lifecycle events (v0.156.x)."""

    @property
    def harness_name(self) -> str:
        return "codex"

    @property
    def supported_events(self) -> List[str]:
        return sorted(set(CODEX_EVENT_MAP.values()))

    @property
    def native_events(self) -> List[str]:
        return sorted(CODEX_EVENT_MAP.keys())

    def is_degraded(self, native_event: str) -> bool:
        return native_event == "PostCompact"

    def to_canonical(self, raw_payload: Dict[str, Any], event_name: str) -> HookEvent:
        canonical = CODEX_EVENT_MAP.get(event_name)
        if canonical is None:
            raise ValueError(f"Unknown Codex event: {event_name!r}")

        tool_name = raw_payload.get("tool_name") or raw_payload.get("toolName")
        session_id = raw_payload.get("session_id") or raw_payload.get("sessionId") or "codex-session"

        action = None
        if canonical in ("aaa.action.proposed", "aaa.action.completed", "aaa.action.failed"):
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
        if self.is_degraded(event_name):
            metadata["degraded"] = True
            metadata["reason"] = "no dedicated canonical post-compact event; phase kept here"
        if event_name == "PermissionRequest":
            metadata["sub_kind"] = "permission"
        if raw_payload.get("tool_input") is not None:
            # Never carry raw arguments across the boundary — digest only.
            metadata["has_tool_input"] = True

        return HookEvent(
            event_name=canonical,
            harness_id=self.harness_name,
            session_id=str(session_id),
            action=action,
            risk_class=action.risk_class if action else "R0",
            metadata=metadata,
        )

    def from_canonical(self, decision: HookDecision) -> Dict[str, Any]:
        # NOTE (VERIFY lane): Codex hook decision-response wire schema is not yet
        # cross-verified against codex-rs hooks/src. Emitted shape is minimal and
        # non-authoritative; the shim is advisory and never blocks regardless.
        return {
            "verdict": decision.verdict,
            "event_id": decision.event_id,
            "advisory": True,
        }
