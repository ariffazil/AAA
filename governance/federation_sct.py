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

import json
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
    # Wire contract (sealed 2026-07-17 live receipt):
    #   arguments.session_id = full SCT string (intentional overload for validate mode)
    #   response = {valid: bool, claims: {...}, error: str|None}
    # MCP transport may wrap that as result.content[0].text JSON (SSE/streamable).
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
                        "session_token": sct,  # dual-key for hosts that prefer explicit token field
                    },
                },
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
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

    # Parse JSON or SSE (data: {...})
    try:
        text = r.text or ""
        if "data:" in text:
            # last data: line wins
            for line in text.splitlines():
                if line.startswith("data:"):
                    text = line[5:].strip()
            data = json.loads(text) if text else {}
        else:
            data = r.json()
    except Exception as exc:
        return SCTVerification(
            ok=False,
            error_code="ARIFOS_PARSE_ERROR",
            error_message=f"Could not parse arifOS validate response: {exc!r}",
        )

    result = data.get("result", {}) or {}
    # Unwrap MCP tool content envelope
    if isinstance(result, dict) and isinstance(result.get("content"), list) and result["content"]:
        try:
            inner_text = result["content"][0].get("text") or ""
            parsed = json.loads(inner_text) if inner_text else {}
            # Nested wrappers: {result: {valid...}} or flat {valid...}
            if isinstance(parsed, dict):
                if "valid" in parsed or "claims" in parsed:
                    result = parsed
                elif isinstance(parsed.get("result"), dict):
                    result = parsed["result"]
                else:
                    result = parsed
        except Exception:
            pass
    # Some hosts put structuredContent
    if isinstance(result, dict) and not result.get("valid") and isinstance(
        result.get("structuredContent"), dict
    ):
        sc = result["structuredContent"]
        if "valid" in sc or "claims" in sc:
            result = sc

    if not result.get("valid"):
        return SCTVerification(
            ok=False,
            error_code="SCT_INVALID",
            error_message=result.get("error")
            or result.get("message")
            or "arifOS rejected SCT",
        )

    claims = result.get("claims", {}) or {}
    # Live interop law: token validation MUST return claims. session_store
    # path can set valid=true without claims — that is not SCT proof.
    if not isinstance(claims, dict) or not claims:
        return SCTVerification(
            ok=False,
            error_code="SCT_CLAIMS_MISSING",
            error_message=(
                "arifOS returned valid=true without claims "
                f"(validation_path={result.get('validation_path')!r}); "
                "not an SCT verification receipt"
            ),
        )
    actor = claims.get("actor") or claims.get("actor_id") or result.get("actor")
    authority = (
        claims.get("auth")
        or claims.get("authority")
        or result.get("authority")
        or "OBSERVE_ONLY"
    )

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


def extract_sct_from_call(
    arguments: dict[str, Any] | None = None,
    *,
    headers: dict[str, str] | None = None,
    meta: dict[str, Any] | None = None,
) -> str | None:
    """Pull SCT from tool args, _meta, or HTTP headers.

    Search order:
      1. arguments.session_token / arguments.sct / arguments.arifos_sct
      2. arguments._meta.{sct,session_token,arifos_sct}
      3. explicit meta dict
      4. headers X-ArifOS-SCT / X-Session-Token / Authorization: Bearer sct_v1...
    """
    args = arguments if isinstance(arguments, dict) else {}
    for key in ("session_token", "sct", "arifos_sct"):
        val = args.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    nested_meta = args.get("_meta") if isinstance(args.get("_meta"), dict) else None
    for m in (nested_meta, meta):
        sct = _extract_sct_from_meta(m)
        if sct:
            return sct
    if headers:
        # header keys may be lower-cased by ASGI
        lower = {str(k).lower(): v for k, v in headers.items()}
        for key in ("x-arifos-sct", "x-session-token", "x-arifos-session-token"):
            val = lower.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        auth = lower.get("authorization") or ""
        if isinstance(auth, str) and auth.lower().startswith("bearer "):
            token = auth[7:].strip()
            if token.startswith("sct_v1.") or token.startswith("arifos.v1."):
                return token
    return None


def gate_tool_ingress(
    tool_name: str,
    arguments: dict[str, Any] | None = None,
    *,
    headers: dict[str, str] | None = None,
    meta: dict[str, Any] | None = None,
    required_authority: str = "OBSERVE_ONLY",
    require_sct: bool = False,
    organ: str = "unknown",
) -> dict[str, Any] | None:
    """Organ ingress SCT gate.

    Policy:
      - If SCT is present → must verify (fail closed).
      - If require_sct=True and SCT missing → SCT_REQUIRED reject.
      - If SCT absent and not required → allow (backward-compatible OBSERVE).

    Returns None to proceed, or a rejection dict.
    """
    args = arguments if isinstance(arguments, dict) else {}
    actor = None
    for key in ("actor_id", "actor", "caller_actor_id"):
        if isinstance(args.get(key), str) and args[key].strip():
            actor = args[key].strip()
            break
    sct = extract_sct_from_call(args, headers=headers, meta=meta)
    if not sct:
        if require_sct:
            return {
                "error": "SCT_REQUIRED",
                "message": (
                    f"Tool '{tool_name}' requires a valid Session Capability Token "
                    f"(session_token / _meta.sct / X-ArifOS-SCT). Mint via arif_init."
                ),
                "tool": tool_name,
                "organ": organ,
                "actor": actor,
                "_epistemic": {
                    "output_class": "GOVERNANCE_TEMPLATE",
                    "authority_claim": "GATE_REJECTED",
                    "tagged_by": "federation-sct-gate",
                    "schema_version": "2.0.0",
                },
            }
        return None
    rej = verify_or_reject(
        sct,
        expected_actor=actor,
        required_authority=required_authority,
        meta=meta,
    )
    if rej is None:
        return None
    rej["tool"] = tool_name
    rej["organ"] = organ
    return rej
