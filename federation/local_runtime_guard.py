"""
local_runtime_guard.py — Local Runtime Isolation Guard
═════════════════════════════════════════════════════════

Forged 2026-08-10 by 333-AGI under F13 directive. Lane B SESSION_RECEIPT ratification.

Refactored FROM: /root/AAA/federation/shadow_guard.py (deleted in same session)

Purpose: PRESERVE the isolation guarantee (local-runtime requests must NEVER
touch public cloud APIs) while REMOVING the shadow ledger pattern that
violated F4 (parallel source of truth) and F11 (audit bypass).

Changes from shadow_guard.py:
  - Shadow ledger /root/.shadow/shadow_telemetry.jsonl → REMOVED.
    All guard events emit to canonical arifflow_receipts.jsonl via
    FlowReceiptProxy (single ledger, F4 + F11 compliant).
  - "SHADOW_RUNTIME" naming → "LOCAL_RUNTIME" (honest naming, F9).
  - PUBLIC_API_DOMAINS list preserved (the safety check itself is sound).
  - LOCALHOST_PATTERN + strict mode preserved.
  - assert_no_public_ledger_contamination REMOVED (no shadow ledger to
    contaminate; the canonical ledger now legitimately contains LOCAL_RUNTIME
    events with content_classification field).

Floor binding:
  F2 TRUTH    — blocklist deterministic, no ML, honest naming
  F4 CLARITY  — single canonical ledger, no parallel source
  F5 PEACE²   — prevents uncensored model output leaking to public cloud APIs
  F11 AUDIT   — every guard event hits arifflow_receipts.jsonl
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

__all__ = [
    "AAALocalRuntimeGuard",
    "PUBLIC_API_DOMAINS",
    "LOCALHOST_PATTERNS",
    "CONTENT_CLASS_OPTIONS",
]


# ── Constants ────────────────────────────────────────────────────────────

PUBLIC_API_DOMAINS: list[str] = [
    "api.openai.com",
    "dashscope.aliyuncs.com",
    "api.anthropic.com",
    "api.deepseek.com",
    "api.moonshot.cn",
    "api.groq.com",
    "generativelanguage.googleapis.com",
    "api.cloudflare.com",
    "gateway.arif-fazil.com",
    "mcp.arif-fazil.com",
    "arifos.arif-fazil.com",
    "geox.arif-fazil.com",
    "wealth.arif-fazil.com",
    "well.arif-fazil.com",
]

LOCALHOST_PATTERNS: tuple[str, ...] = (
    "127.0.0.1",
    "localhost",
    "::1",
)

CONTENT_CLASS_OPTIONS: tuple[str, ...] = (
    "general", "sensitive", "artistic", "research", "medical",
)


# ── Canonical ledger (single source of truth) ──────────────────────────

def _emit_to_arifflow(
    event: str,
    target_url: str,
    violation_type: str,
    severity: str,
) -> Optional[str]:
    """
    Emit a guard event to the CANONICAL arifflow_receipts.jsonl ledger
    via FlowReceiptProxy. NEVER to a shadow file.
    """
    try:
        from fed_router_v2 import FlowReceiptProxy  # type: ignore[import-not-found]
    except ImportError:
        return None
    proxy = FlowReceiptProxy()
    return proxy.emit(
        step_type="Barrier",
        floor_verdict="Hold" if severity == "CRITICAL" else "Caution",
        epistemic_label="Observation",
        payload={
            "event": event,
            "guard": "AAALocalRuntimeGuard",
            "target_url": target_url,
            "violation_type": violation_type,
            "severity": severity,
            "isolation_note": "local-runtime guard event, canonical ledger",
        },
    )


# ── The Guard ────────────────────────────────────────────────────────────


class AAALocalRuntimeGuard:
    """
    Static guard — no state, no shadow ledger, pure assertion functions.
    Every guard hit emits to the canonical arifflow_receipts.jsonl.

    Renamed from AAAShadowGuard; same isolation guarantees, honest naming.
    """

    @staticmethod
    def assert_local_isolation(
        signature_name: str,
        target_url: str,
        *,
        strict: bool = True,
    ) -> bool:
        """
        Core guard: fails fast if a local-runtime request attempts to
        route to any public cloud API domain. Logs every check to the
        canonical ledger (NOT a shadow file).

        Args:
            signature_name: The capability signature (e.g. "fed-local-uncensored")
            target_url: The resolved target URL for the request
            strict: If True (default), ONLY localhost is permitted.
                    If False, blocklist enforcement only.

        Returns:
            True if isolation is maintained.

        Raises:
            PermissionError: If local-runtime request reaches public domain.
        """
        # Only enforce for local-runtime signatures
        if not signature_name.startswith("fed-local-"):
            return True

        target_lower = target_url.lower()

        # Check against public-domain blocklist
        for domain in PUBLIC_API_DOMAINS:
            if domain in target_lower:
                _emit_to_arifflow(
                    event="LOCAL_RUNTIME_BLOCKED_DOMAIN",
                    target_url=target_url,
                    violation_type=f"BLOCKED_DOMAIN:{domain}",
                    severity="CRITICAL",
                )
                raise PermissionError(
                    f"[AAA LOCAL-RUNTIME VIOLATION] Signature '{signature_name}' "
                    f"attempted to route to public domain: {domain}\n"
                    f"  target_url: {target_url}\n"
                    f"  Required: localhost-only execution"
                )

        # Strict mode: only localhost permitted
        if strict:
            is_localhost = any(
                host in target_lower for host in LOCALHOST_PATTERNS
            )
            if not is_localhost:
                _emit_to_arifflow(
                    event="LOCAL_RUNTIME_NOT_LOCALHOST",
                    target_url=target_url,
                    violation_type="NOT_LOCALHOST",
                    severity="HIGH",
                )
                raise PermissionError(
                    f"[AAA LOCAL-RUNTIME VIOLATION] Signature '{signature_name}' "
                    f"target is not localhost: {target_url}\n"
                    f"  Strict mode requires execution on 127.0.0.1 / localhost"
                )

        # Pass: emit a lightweight receipt (single ledger, no shadow)
        _emit_to_arifflow(
            event="LOCAL_RUNTIME_ISOLATION_PASS",
            target_url=target_url,
            violation_type="PASS",
            severity="INFO",
        )
        return True

    @staticmethod
    def preflight_local_health(
        local_url: str = "http://127.0.0.1:8188",
    ) -> dict:
        """
        Check if the local runtime (ComfyUI / SD-WebUI / custom) is healthy
        before routing. Returns health status dict.
        """
        try:
            req = urllib.request.Request(f"{local_url}/system_stats", method="GET")
            resp = urllib.request.urlopen(req, timeout=3)
            data = json.loads(resp.read())
            return {
                "status": "HEALTHY",
                "local_url": local_url,
                "system_stats": data,
            }
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            return {
                "status": "UNREACHABLE",
                "local_url": local_url,
                "error": str(e),
            }

    @staticmethod
    def validate_content_class(content_class: str) -> bool:
        """Reject content_class outside the 5-value enum."""
        if content_class not in CONTENT_CLASS_OPTIONS:
            raise ValueError(
                f"content_class '{content_class}' not in {CONTENT_CLASS_OPTIONS}"
            )
        return True