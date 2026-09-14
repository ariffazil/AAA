#!/usr/bin/env python3
"""
capability.py — Harness Capability Registry and Discovery for AAA Hook Mesh
Canonical Path: /root/AAA/hooks/lib/capability.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 5, 6

Maintains discovery state, blocking capability, fidelity levels,
and supported event vectors across all 7 federation harnesses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass(frozen=True)
class HarnessCapability:
    harness_id: str
    fidelity: str  # L1, L2, L3, L4
    can_block_pre_tool: bool
    can_post_tool: bool
    can_session_lifecycle: bool
    supported_canonical_events: List[str]
    description: str


HARNESS_REGISTRY: Dict[str, HarnessCapability] = {
    "opencode": HarnessCapability(
        harness_id="opencode",
        fidelity="L4",
        can_block_pre_tool=True,
        can_post_tool=True,
        can_session_lifecycle=True,
        supported_canonical_events=[
            "aaa.session.opened",
            "aaa.turn.received",
            "aaa.action.proposed",
            "aaa.action.completed",
            "aaa.turn.idle",
            "aaa.session.sealing",
            "aaa.policy.violation",
        ],
        description="Full native TypeScript plugin architecture via Node hooks",
    ),
    "claude_code": HarnessCapability(
        harness_id="claude_code",
        fidelity="L3",
        can_block_pre_tool=True,
        can_post_tool=True,
        can_session_lifecycle=True,
        supported_canonical_events=[
            "aaa.session.opened",
            "aaa.turn.received",
            "aaa.action.proposed",
            "aaa.action.completed",
            "aaa.session.sealing",
        ],
        description="Native hooks.json with PreToolUse and PostToolUse blocking gates",
    ),
    "antigravity": HarnessCapability(
        harness_id="antigravity",
        fidelity="L3",
        can_block_pre_tool=True,
        can_post_tool=True,
        can_session_lifecycle=True,
        supported_canonical_events=[
            "aaa.session.opened",
            "aaa.turn.received",
            "aaa.action.proposed",
            "aaa.action.completed",
            "aaa.action.failed",
            "aaa.session.sealing",
        ],
        description="Native hooks.json calling Python CLI hook scripts",
    ),
    "hermes": HarnessCapability(
        harness_id="hermes",
        fidelity="L2",
        can_block_pre_tool=False,
        can_post_tool=True,
        can_session_lifecycle=True,
        supported_canonical_events=[
            "aaa.session.opened",
            "aaa.turn.received",
            "aaa.action.completed",
            "aaa.session.sealing",
        ],
        description="CLI gateway / Telegram surface; async hook logging via arifflow",
    ),
    "openclaw": HarnessCapability(
        harness_id="openclaw",
        fidelity="L2",
        can_block_pre_tool=False,
        can_post_tool=True,
        can_session_lifecycle=True,
        supported_canonical_events=[
            "aaa.session.opened",
            "aaa.action.completed",
            "aaa.action.failed",
            "aaa.session.sealing",
        ],
        description="Edge agent on KVM4; telemetry and notification bridge",
    ),
    "kimi": HarnessCapability(
        harness_id="kimi",
        fidelity="L1",
        can_block_pre_tool=False,
        can_post_tool=False,
        can_session_lifecycle=True,
        supported_canonical_events=[
            "aaa.session.opened",
            "aaa.session.sealing",
        ],
        description="CLI session wrapper; entry/exit lifecycle checks",
    ),
    "qwen": HarnessCapability(
        harness_id="qwen",
        fidelity="L1",
        can_block_pre_tool=False,
        can_post_tool=False,
        can_session_lifecycle=True,
        supported_canonical_events=[
            "aaa.session.opened",
            "aaa.session.sealing",
        ],
        description="CLI session wrapper; entry/exit lifecycle checks",
    ),
    "well": HarnessCapability(
        harness_id="well",
        fidelity="L3",
        can_block_pre_tool=True,
        can_post_tool=True,
        can_session_lifecycle=True,
        supported_canonical_events=[
            "aaa.session.opened",
            "aaa.action.proposed",
            "aaa.action.completed",
            "aaa.policy.violation",
        ],
        description="WELL organ biometric and dignity boundary guard",
    ),
}

# Aliases
HARNESS_REGISTRY["claude"] = HARNESS_REGISTRY["claude_code"]
HARNESS_REGISTRY["agy"] = HARNESS_REGISTRY["antigravity"]


def get_harness_capability(harness_id: str) -> Optional[HarnessCapability]:
    """Retrieves capability record for a given harness identifier."""
    return HARNESS_REGISTRY.get(harness_id.lower())


def list_supported_harnesses() -> List[str]:
    """Returns list of registered harness identifiers."""
    return sorted(list(HARNESS_REGISTRY.keys()))
