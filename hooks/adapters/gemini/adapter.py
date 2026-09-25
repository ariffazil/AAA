#!/usr/bin/env python3
"""
gemini/adapter.py — Google Gemini CLI Adapter for AAA Hook Mesh
Canonical Path: /root/AAA/hooks/adapters/gemini/adapter.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 6 · built 2026-09-25 (F13 "buat adapter grok/gemini")

HONEST ABSENT DECLARATION (FP-04): as of 2026-09-25 no lifecycle-hook
mechanism is documented or configured for gemini-cli on this host —
/root/.gemini/hooks/ exists but is empty (created 2026-08-13, never
populated), and settings.json carries only mcpServers. This adapter
therefore declares ZERO native events rather than faking a map.

The gemini plugin VIEW (dist/gemini/) wires what IS real: the compiled
mcpServers parity fragment (6 organs from organs.yaml). If gemini-cli
ships a hook surface later, extend GEMINI_EVENT_MAP here and re-run
build.sh — the compile pipeline picks it up with zero view hand-edits (FP-01).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))

from adapter_contract import HarnessAdapter
from decision_schema import HookDecision

# Verified-absent surface. Populate ONLY with events documented by gemini-cli.
GEMINI_EVENT_MAP: Dict[str, str] = {}


class GeminiAdapter(HarnessAdapter):
    """Adapter for Google Gemini CLI — declared-absent hook surface (2026-09-25)."""

    @property
    def harness_name(self) -> str:
        return "gemini"

    @property
    def supported_events(self) -> List[str]:
        return []

    @property
    def native_events(self) -> List[str]:
        return []

    def is_degraded(self, native_event: str) -> bool:
        return True  # everything is absent-class until the surface exists

    def to_canonical(self, raw_payload: Dict[str, Any], event_name: str):
        raise ValueError(
            f"Gemini hook surface ABSENT (verified 2026-09-25): event {event_name!r} has no native source"
        )

    def from_canonical(self, decision: HookDecision) -> Dict[str, Any]:
        return {
            "verdict": decision.verdict,
            "event_id": decision.event_id,
            "advisory": True,
            "absent_surface": True,
        }
