#!/usr/bin/env python3
"""
qwen/adapter.py — Qwen CLI Hooks Adapter for AAA Hook Mesh
Canonical Path: /root/AAA/hooks/adapters/qwen/adapter.py
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


class QwenAdapter(HarnessAdapter):
    """Adapter for Qwen CLI session lifecycle events."""

    @property
    def harness_name(self) -> str:
        return "qwen"

    @property
    def supported_events(self) -> List[str]:
        return [
            "aaa.session.opened",
            "aaa.session.sealing",
        ]

    def to_canonical(self, raw_payload: Dict[str, Any], event_name: str) -> HookEvent:
        canonical_event = "aaa.session.opened" if "start" in event_name or "open" in event_name else "aaa.session.sealing"
        return HookEvent(
            event_name=canonical_event,
            harness_id="qwen",
            session_id=raw_payload.get("session_id", "qwen-session"),
            risk_class="R1",
            metadata={"raw_qwen_event": event_name},
        )

    def from_canonical(self, decision: HookDecision) -> Dict[str, Any]:
        return {
            "verdict": decision.verdict,
            "event_id": decision.event_id,
        }
