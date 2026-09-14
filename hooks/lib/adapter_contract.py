#!/usr/bin/env python3
"""
adapter_contract.py — Contract and Base Interface for AAA Harness Hook Adapters
Canonical Path: /root/AAA/hooks/lib/adapter_contract.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 6

Every harness (OpenCode, Claude Code, Antigravity, Hermes, OpenClaw, Kimi, Qwen, WELL)
interacts with the Federation Hook Mesh via an adapter adhering to this contract.
"""

from __future__ import annotations

import abc
from typing import Any, Dict, List, Optional, Tuple

from event_schema import HookEvent, canonical_json
from decision_schema import HookDecision


class HarnessAdapter(abc.ABC):
    """Abstract Base Class defining the contract for all harness adapters."""

    @property
    @abc.abstractmethod
    def harness_name(self) -> str:
        """Returns the canonical harness identifier (e.g. 'opencode', 'claude_code')."""
        pass

    @property
    @abc.abstractmethod
    def supported_events(self) -> List[str]:
        """List of canonical event names supported by this harness."""
        pass

    @abc.abstractmethod
    def to_canonical(self, raw_payload: Dict[str, Any], event_name: str) -> HookEvent:
        """Translates harness-native payload into a canonical HookEvent envelope."""
        pass

    @abc.abstractmethod
    def from_canonical(self, decision: HookDecision) -> Dict[str, Any]:
        """Translates canonical HookDecision envelope into harness-native response format."""
        pass

    def validate_payload(self, raw_payload: Dict[str, Any]) -> bool:
        """Basic validation that payload contains minimum required structure."""
        return isinstance(raw_payload, dict)
