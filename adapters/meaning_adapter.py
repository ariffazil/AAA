"""MeaningAdapter — the ONE DOOR to HERMES's meaning capability (PR-3).

Contract (stable, AAA-owned):
    classify(text) -> {
        available: bool,
        principal_type: str | None,   # door contract typing (see below)
        confidence: float | None,     # None when the door provides none (F2: never invent)
        source: str,                  # provenance of the classification
        observed_at: str | None,      # ISO-8601 UTC
        adapter_version: str,
        degradation: str | None,      # None when healthy
        principals: [...],            # full HERMES principal extraction
        separated: bool,              # multi-perspective separation happened
        injection_detected: bool,
    }

Capability behind the door (live probe 2026-10-02, HERMES :18087 /health +
tools/list): HERMES exposes ``hermes_perspective_scope`` and
``hermes_claim_validate`` over MCP. Their principal typing is the coarse
5-type contract: PERSON | INSTITUTION | COLLECTIVE | SYSTEM | UNDEFINED.

Known granularity gap, recorded not papered over (F2): the deterministic
15-class classifier (POLITICAL_PARTY, AI_ORGAN, LEGISLATURE, …) lives at
/root/HERMES/mcp/hermes-rasa/principal_type_classifier.py and is NOT
exposed behind any HTTP/MCP door. Before PR-3, AAA smuggled it in via
sys.path. After PR-3, AAA sees only what HERMES actually serves.

F1 AMANAH — fail closed: HERMES unreachable ⇒ available=False with
degradation="HERMES_UNREACHABLE". No fallback typing, no guessing.

NO sys.path insertion. NO imports of HERMES modules. NO access under
/root/HERMES. One lane: HTTP to the HERMES MCP endpoint only.
"""

from __future__ import annotations

import datetime as _dt
import os
from typing import Any

from ._mcp_http import McpHttpSession, McpTransportError, http_json

ADAPTER_VERSION = "1.0.0"
DEFAULT_HERMES_URL = "http://127.0.0.1:18087"

_CLASSIFY_TOOL = "hermes_perspective_scope"


def _utcnow_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


class MeaningAdapter:
    """Stable classify() contract over HERMES MCP. Read-only."""

    def __init__(self, base_url: str | None = None, timeout: float = 4.0):
        self.base_url = (
            base_url or os.getenv("HERMES_MCP_URL") or DEFAULT_HERMES_URL
        ).rstrip("/")
        self.timeout = timeout

    def classify(self, text: str) -> dict[str, Any]:
        result: dict[str, Any] = {
            "available": False,
            "principal_type": None,
            "confidence": None,
            "source": "unavailable",
            "observed_at": None,
            "adapter_version": ADAPTER_VERSION,
            "degradation": None,
            "principals": [],
            "separated": False,
            "injection_detected": False,
        }
        if not text or not text.strip():
            result["degradation"] = "EMPTY_INPUT"
            return result

        # 1) Liveness probe (GET /health) — cheap, distinguishes down vs misrouted
        try:
            status, _hdrs, _body = http_json(
                f"{self.base_url}/health", timeout=self.timeout
            )
            if status != 200:
                result["degradation"] = f"HERMES_UNHEALTHY:{status}"
                return result
        except McpTransportError:
            result["degradation"] = "HERMES_UNREACHABLE"
            return result

        # 2) One-door MCP call — the only classification lane
        try:
            with McpHttpSession(self.base_url, timeout=self.timeout) as session:
                payload = session.call_tool(_CLASSIFY_TOOL, {"statement": text})
        except McpTransportError as exc:
            result["degradation"] = f"HERMES_MCP_ERROR:{exc}"
            return result

        # HERMES wraps tool output in {"tool", "status", "result"} — unwrap
        if "principals" not in payload and isinstance(payload.get("result"), dict):
            payload = payload["result"]

        principals = payload.get("principals") or []
        first = principals[0] if principals else {}
        result.update(
            available=True,
            principal_type=first.get("principal_type"),
            # The door provides no numeric confidence for this tool —
            # None stays None (F2 TRUTH: never fabricate a number).
            confidence=None,
            source=f"hermes-mcp:{_CLASSIFY_TOOL}",
            observed_at=_utcnow_iso(),
            principals=principals,
            separated=bool(payload.get("separated", False)),
            injection_detected=bool(
                (payload.get("injection_scan") or {}).get("injection_detected", False)
            ),
        )
        return result
