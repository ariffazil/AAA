"""
federation_sct.py — Cross-organ SCT verification helper
═══════════════════════════════════════════════════════════════════════
Forged 2026-07-14 · SCT v1 wiring steps 4-7 closure

This module is the FFI for any organ (A-FORGE, GEOX, WEALTH, WELL) to
verify a Session Capability Token issued by arifOS.

The contract is simple:
  1. arif_init() mints an SCT and returns it in session_token
  2. The agent puts the SCT in every cross-organ call's _meta envelope
  3. Each organ's ingress middleware calls verify_federation_sct(sct, actor)
  4. If verify returns ok=False, the organ REJECTS the call
  5. If verify returns ok=True, the organ proceeds (with claims for audit)

DITEMPA BUKAN DIBERI — Tokens are forged, not assumed.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from typing import Any

import httpx

logger = logging.getLogger("federation.sct")

ARIFOS_BASE = os.getenv("ARIFOS_BASE_URL", "http://localhost:8088")
ARIFOS_TIMEOUT_S = float(os.getenv("ARIFOS_SCT_TIMEOUT_S", "2.0"))

# Token shape: sct_v1.<base64url>.<hmac>
SCT_RE = re.compile(r"^sct_v1\.[A-Za-z0-9_\-]+(?:\.[A-Za-z0-9_\-]+)?$")


@dataclass
class SCTVerification:
    ok: bool
    error_code: str | None = None
    error_message: str | None = None
    claims: dict[str, Any] | None = None
    actor: str | None = None
    authority: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "error_code": self.error_code,
            "error_message": self.error_message,
            "actor": self.actor,
            "authority": self.authority,
        }


def _extract_sct_from_meta(meta: dict[str, Any] | None) -> str | None:
    """Pull sct out of an MCP _meta envelope."""
    if not meta or not isinstance(meta, dict):
        return None
    sct = meta.get("sct") or meta.get("session_token") or meta.get("arifos_sct")
    if not sct or not isinstance(sct, str):
        return None
    return sct


def _validate_format(sct: str) -> bool:
    """Format check before calling arifOS (saves a round-trip on obvious garbage)."""
    if not sct or len(sct) < 16:
        return False
    return bool(SCT_RE.match(sct))


def verify_federation_sct(
    sct: str | None,
    *,
    expected_actor: str | None = None,
    required_authority: str = "OBSERVE_ONLY",
    meta: dict[str, Any] | None = None,
) -> SCTVerification:
    """Verify an SCT and (optionally) enforce actor binding + authority floor.

    Args:
        sct: The token string, OR None (will try to extract from meta).
        expected_actor: If set, the caller's actor must match this.
        required_authority: Minimum authority band required for this call.
        meta: Optional MCP _meta envelope (will be searched for sct if sct is None).

    Returns:
        SCTVerification with .ok=True if valid; .error_code set otherwise.
    """
    if sct is None:
        sct = _extract_sct_from_meta(meta)

    if not sct:
        return SCTVerification(
            ok=False,
            error_code="SCT_MISSING",
            error_message="No SCT provided in call or _meta envelope",
        )
    if not _validate_format(sct):
        return SCTVerification(
            ok=False,
            error_code="SCT_MALFORMED",
            error_message=f"SCT does not match sct_v1.<b64>.<hmac> shape: {sct[:24]}...",
        )

    # Ask arifOS kernel to verify via arif_init(mode=validate).
    # arif_session_validate does not exist on the live arifOS MCP surface;
    # arif_init with mode="validate" is the canonical validation verb.
    try:
        r = httpx.post(
            f"{ARIFOS_BASE}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "arif_init",
                    "arguments": {
                        "mode": "validate",
                        "session_id": sct,
                    },
                },
            },
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=ARIFOS_TIMEOUT_S,
        )
    except httpx.RequestError as exc:
        # FAIL-CLOSED: arifOS unreachable means we cannot verify the SCT.
        # Accepting unaudited cross-organ calls during kernel outage is an
        # authorization bypass (F1 AMANAH, F8 LAW).
        logger.error("arifOS unreachable for SCT verify — FAIL CLOSED: %s", exc)
        return SCTVerification(
            ok=False,
            error_code="ARIFOS_UNREACHABLE",
            error_message=f"arifOS unreachable ({exc!r}); SCT rejected (fail-closed)",
        )

    if r.status_code != 200:
        return SCTVerification(
            ok=False,
            error_code="ARIFOS_HTTP_ERROR",
            error_message=f"arifOS returned HTTP {r.status_code}",
        )

    data = r.json()
    result = data.get("result", {}) or {}
    if not result.get("valid"):
        return SCTVerification(
            ok=False,
            error_code="SCT_INVALID",
            error_message=result.get("error", "arifOS rejected SCT"),
        )

    claims = result.get("claims", {}) or {}
    actor = claims.get("actor") or claims.get("actor_id")
    authority = claims.get("auth") or claims.get("authority", "OBSERVE_ONLY")

    # Actor binding check
    if expected_actor and actor and actor != expected_actor:
        return SCTVerification(
            ok=False,
            error_code="ACTOR_MISMATCH",
            error_message=f"SCT actor {actor!r} does not match caller {expected_actor!r}",
        )

    # Authority floor check (lowest acceptable).
    # Unknown authority names are REJECTED, not silently mapped to OBSERVE_ONLY.
    # Repo-specific strings like JUDGE_SEAL_AUTHORIZATION or 888_HOLD must be
    # canonicalised before reaching this gate; raw unknowns are a policy breach.
    AUTHORITY_RANK = ("OBSERVE_ONLY", "OPERATOR", "LIMITED_MUTATE", "FULL", "SOVEREIGN")
    if required_authority not in AUTHORITY_RANK:
        return SCTVerification(
            ok=False,
            error_code="UNKNOWN_REQUIRED_AUTHORITY",
            error_message=f"required_authority {required_authority!r} is not a recognised band; "
            f"canonical bands: {AUTHORITY_RANK}",
        )
    if authority not in AUTHORITY_RANK:
        return SCTVerification(
            ok=False,
            error_code="UNKNOWN_AUTHORITY",
            error_message=f"SCT authority {authority!r} is not a recognised band; canonical bands: {AUTHORITY_RANK}",
        )
    rank_required = AUTHORITY_RANK.index(required_authority)
    rank_actual = AUTHORITY_RANK.index(authority)
    if rank_actual < rank_required:
        return SCTVerification(
            ok=False,
            error_code="INSUFFICIENT_AUTHORITY",
            error_message=f"SCT authority {authority!r} < required {required_authority!r}",
        )

    return SCTVerification(
        ok=True,
        claims=claims,
        actor=actor or expected_actor,
        authority=authority,
    )


def verify_or_reject(
    sct: str | None,
    *,
    expected_actor: str | None = None,
    required_authority: str = "OBSERVE_ONLY",
    meta: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Convenience wrapper for ingress middleware.

    Returns None if verification passes, or a dict error if it fails.
    """
    result = verify_federation_sct(
        sct,
        expected_actor=expected_actor,
        required_authority=required_authority,
        meta=meta,
    )
    if result.ok:
        return None
    return {
        "error": result.error_code,
        "message": result.error_message,
        "actor": expected_actor,
        "required_authority": required_authority,
        "_epistemic": {
            "output_class": "GOVERNANCE_TEMPLATE",
            "authority_claim": "GATE_REJECTED",
            "tagged_by": "federation-sct-gate",
            "schema_version": "2.0.0",
        },
    }
