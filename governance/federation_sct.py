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

import hashlib
import json
import logging
import os
import re
from dataclasses import dataclass, field
from typing import Any

import httpx

logger = logging.getLogger("federation.sct")

ARIFOS_BASE = os.getenv("ARIFOS_BASE_URL", "http://localhost:8088")
ARIFOS_TIMEOUT_S = float(os.getenv("ARIFOS_SCT_TIMEOUT_S", "2.0"))

# Token shape: sct_v1.<base64url>.<hmac>
SCT_RE = re.compile(r"^sct_v1\.[A-Za-z0-9_\-]+(?:\.[A-Za-z0-9_\-]+)?$")


def _fingerprint(token: str) -> str:
    """Cryptographic fingerprint of a token — NEVER log the raw token."""
    return "sha256:" + hashlib.sha256(token.encode()).hexdigest()[:12]


@dataclass
class TokenSource:
    """One location where a token was found."""
    location: str       # e.g. "arguments.sct", "header.x-arifos-sct"
    fingerprint: str    # sha256 prefix
    length: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "location": self.location,
            "fingerprint": self.fingerprint,
            "length": self.length,
        }


@dataclass
class TokenExtraction:
    """Result of collecting all SCT sources and detecting conflicts."""
    status: str                     # "PRESENT" | "ABSENT" | "AMBIGUOUS"
    token: str | None = None        # Set only when PRESENT (one unique token)
    sources: list[TokenSource] = field(default_factory=list)
    source_count: int = 0
    unique_fingerprints: int = 0
    conflict_detected: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "token_present": self.status == "PRESENT",
            "source_count": self.source_count,
            "unique_fingerprints": self.unique_fingerprints,
            "conflict_detected": self.conflict_detected,
            "sources": [s.to_dict() for s in self.sources],
        }


@dataclass
class SCTVerification:
    ok: bool
    error_code: str | None = None
    error_message: str | None = None
    claims: dict[str, Any] | None = None
    actor: str | None = None
    authority: str | None = None
    extraction: TokenExtraction | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "ok": self.ok,
            "error_code": self.error_code,
            "error_message": self.error_message,
            "actor": self.actor,
            "authority": self.authority,
        }
        if self.extraction:
            d["extraction"] = self.extraction.to_dict()
        return d


def _collect_sct_from_meta(
    meta: dict[str, Any] | None, location: str
) -> list[tuple[str, str]]:
    """Collect SCT candidates from an _meta envelope. Returns [(token, location), ...]."""
    if not meta or not isinstance(meta, dict):
        return []
    results: list[tuple[str, str]] = []
    for key in ("sct", "session_token", "arifos_sct"):
        val = meta.get(key)
        if isinstance(val, str) and val.strip():
            results.append((val.strip(), f"{location}.{key}"))
    return results


def extract_sct_from_call(
    arguments: dict[str, Any] | None = None,
    *,
    headers: dict[str, str] | None = None,
    meta: dict[str, Any] | None = None,
) -> TokenExtraction:
    """Collect ALL SCT candidate tokens from every source and detect conflicts.

    Sources (all checked, none skipped):
      1. arguments.session_token / arguments.sct / arguments.arifos_sct
      2. arguments._meta.{sct, session_token, arifos_sct}
      3. explicit meta dict
      4. headers X-ArifOS-SCT / X-Session-Token / X-ArifOS-Session-Token
      5. headers Authorization: Bearer <sct_v1.*|arifos.v1.*>

    Returns TokenExtraction with:
      - ABSENT: zero tokens found
      - PRESENT: exactly one unique token (may appear in multiple sources)
      - AMBIGUOUS: multiple DISTINCT tokens — REJECT
    """
    sources: list[TokenSource] = []
    seen_fingerprints: set[str] = set()
    unique_tokens: list[str] = []

    args = arguments if isinstance(arguments, dict) else {}

    # 1. Direct argument keys
    for key in ("session_token", "sct", "arifos_sct"):
        val = args.get(key)
        if isinstance(val, str) and val.strip():
            token = val.strip()
            fp = _fingerprint(token)
            sources.append(TokenSource(
                location=f"arguments.{key}",
                fingerprint=fp,
                length=len(token),
            ))
            if fp not in seen_fingerprints:
                seen_fingerprints.add(fp)
                unique_tokens.append(token)

    # 2. Nested _meta in arguments
    nested_meta = args.get("_meta") if isinstance(args.get("_meta"), dict) else None
    if nested_meta:
        for token_val, loc in _collect_sct_from_meta(nested_meta, "arguments._meta"):
            fp = _fingerprint(token_val)
            sources.append(TokenSource(
                location=loc,
                fingerprint=fp,
                length=len(token_val),
            ))
            if fp not in seen_fingerprints:
                seen_fingerprints.add(fp)
                unique_tokens.append(token_val)

    # 3. Explicit meta dict
    if meta:
        for token_val, loc in _collect_sct_from_meta(meta, "_meta"):
            fp = _fingerprint(token_val)
            sources.append(TokenSource(
                location=loc,
                fingerprint=fp,
                length=len(token_val),
            ))
            if fp not in seen_fingerprints:
                seen_fingerprints.add(fp)
                unique_tokens.append(token_val)

    # 4. HTTP headers
    if headers:
        lower = {str(k).lower(): v for k, v in headers.items()}
        for key in ("x-arifos-sct", "x-session-token", "x-arifos-session-token"):
            val = lower.get(key)
            if isinstance(val, str) and val.strip():
                token = val.strip()
                fp = _fingerprint(token)
                sources.append(TokenSource(
                    location=f"header.{key}",
                    fingerprint=fp,
                    length=len(token),
                ))
                if fp not in seen_fingerprints:
                    seen_fingerprints.add(fp)
                    unique_tokens.append(token)

        # 5. Authorization: Bearer
        auth = lower.get("authorization") or ""
        if isinstance(auth, str) and auth.lower().startswith("bearer "):
            token = auth[7:].strip()
            if token.startswith("sct_v1.") or token.startswith("arifos.v1."):
                fp = _fingerprint(token)
                sources.append(TokenSource(
                    location="header.authorization",
                    fingerprint=fp,
                    length=len(token),
                ))
                if fp not in seen_fingerprints:
                    seen_fingerprints.add(fp)
                    unique_tokens.append(token)

    # Determine status
    source_count = len(sources)
    unique_count = len(unique_tokens)

    if unique_count == 0:
        return TokenExtraction(
            status="ABSENT",
            sources=sources,
            source_count=source_count,
            unique_fingerprints=0,
        )

    if unique_count == 1:
        return TokenExtraction(
            status="PRESENT",
            token=unique_tokens[0],
            sources=sources,
            source_count=source_count,
            unique_fingerprints=1,
        )

    # Multiple distinct tokens → AMBIGUOUS
    logger.warning(
        "SCT_AMBIGUOUS: %d distinct tokens from %d sources. "
        "Fingerprints: %s. This call MUST be rejected.",
        unique_count, source_count,
        ", ".join(s.fingerprint for s in sources),
    )
    return TokenExtraction(
        status="AMBIGUOUS",
        sources=sources,
        source_count=source_count,
        unique_fingerprints=unique_count,
        conflict_detected=True,
    )


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
    if sct is None and meta:
        # Collect from meta envelope using new collect-all approach
        candidates = _collect_sct_from_meta(meta, "_meta")
        if candidates:
            sct = candidates[0][0]  # token from first candidate

    if not sct:
        return SCTVerification(
            ok=False,
            error_code="SCT_MISSING",
            error_message="No SCT provided in call or _meta envelope",
        )
    # Format validation — sct_v1.<base64url>.<hmac> or arifos.v1.*
    if not (sct.startswith("sct_v1.") or sct.startswith("arifos.v1.")):
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



def _emit_gate_decision(
    *,
    tool_name: str,
    organ: str,
    decision: str,
    reason_code: str,
    arguments: dict[str, Any] | None,
    headers: dict[str, str] | None,
    meta: dict[str, Any] | None,
    actor: str | None,
    auth: Any,
    extraction: TokenExtraction | None,
    eff_require_sct: bool,
    eff_authority: str,
) -> str:
    """PR3: emit decision event; return trace_id. Never raises into gate path."""
    try:
        from governance.sct_decision_event import emit_decision
    except ImportError:  # pragma: no cover
        try:
            from sct_decision_event import emit_decision  # type: ignore
        except ImportError:
            return ""

    fp = ""
    source_count = 0
    unique_tokens = 0
    locations: list[str] = []
    if extraction is not None:
        source_count = extraction.source_count
        unique_tokens = extraction.unique_fingerprints
        locations = [s.location for s in extraction.sources]
        if extraction.status == "PRESENT" and extraction.token:
            fp = _fingerprint(extraction.token)
        elif extraction.sources:
            # AMBIGUOUS: log first fingerprint only (already hashed)
            fp = extraction.sources[0].fingerprint

    reg = auth.to_dict() if auth is not None and hasattr(auth, "to_dict") else {}
    event = emit_decision(
        tool=tool_name,
        organ=organ,
        decision=decision,
        reason_code=reason_code,
        arguments=arguments,
        headers=headers,
        meta=meta,
        actor_id=actor or "",
        action_class=str(reg.get("action_class") or ""),
        required_authority=eff_authority,
        require_sct=eff_require_sct,
        sct_fingerprint=fp,
        sct_source_count=source_count,
        sct_unique_tokens=unique_tokens,
        registry_source="tools.yaml" if reg.get("tool_id") else "unknown",
        registry_known=bool(reg.get("tool_id")) and reg.get("action_class") != "UNKNOWN",
        extraction_locations=locations,
    )
    return event.trace_id


def gate_tool_ingress(
    tool_name: str,
    arguments: dict[str, Any] | None = None,
    *,
    headers: dict[str, str] | None = None,
    meta: dict[str, Any] | None = None,
    required_authority: str | None = None,
    require_sct: bool | None = None,
    organ: str = "unknown",
) -> dict[str, Any] | None:
    """Organ ingress SCT gate — registry-owned authority + SCT conflict check.

    Policy (PR 2):
      - action_class / require_sct / required_authority are resolved from
        governance/tool_authority_registry.py (tools.yaml + organ defaults).
        Caller-supplied action_class is STRIPPED. Caller may only tighten
        require_sct / authority, never loosen.
      - AMBIGUOUS (multiple distinct tokens) → REJECT immediately
      - UNKNOWN tool (strict) → CAPABILITY_UNKNOWN HOLD
      - Domain organs (geox/wealth/well): unlisted tools default OBSERVE
      - If SCT is present → must verify (fail closed)
      - If require_sct=True and SCT missing → SCT_REQUIRED reject
      - If SCT absent and not required → allow (backward-compatible OBSERVE)

    PR 3: every ALLOW/REJECT emits a decision event with trace_id +
    token fingerprint (never raw SCT).

    Returns None to proceed, or a rejection dict with extraction + registry evidence.
    """
    # Canonical PR2 resolver: tools.yaml + dash/underscore aliases + organ defaults.
    # DO NOT use registries/tool_authority.py (exact-id only → total lockdown).
    from governance.tool_authority_registry import (  # type: ignore
        ACTION_UNKNOWN,
        resolve_tool_authority,
        strip_caller_action_class,
    )

    auth = resolve_tool_authority(tool_name, organ=organ, strict_unknown=False)
    args = strip_caller_action_class(arguments if isinstance(arguments, dict) else {})

    # Strict UNKNOWN only (no organ default) → HOLD. Domain organ defaults
    # return OBSERVE with known=False and never hit this path.
    if auth.action_class == ACTION_UNKNOWN:
        rej = {
            "error": "CAPABILITY_UNKNOWN",
            "message": (
                f"Tool '{tool_name}' has no registry entry and no safe organ "
                f"default for organ='{organ}'. HOLD until registered in tools.yaml "
                f"with execution_kind + risk_tier."
            ),
            "tool": tool_name,
            "organ": organ,
            "registry": auth.to_dict(),
            "_epistemic": {
                "output_class": "GOVERNANCE_TEMPLATE",
                "authority_claim": "GATE_REJECTED",
                "tagged_by": "federation-sct-gate",
                "schema_version": "2.0.0",
            },
        }
        tid = _emit_gate_decision(
            tool_name=tool_name,
            organ=organ,
            decision="REJECT",
            reason_code="CAPABILITY_UNKNOWN",
            arguments=args,
            headers=headers,
            meta=meta,
            actor=None,
            auth=auth,
            extraction=None,
            eff_require_sct=True,
            eff_authority=auth.required_authority,
        )
        if tid:
            rej["trace_id"] = tid
        return rej

    # Registry is the floor. Caller may only tighten (never loosen).
    # If caller requires stricter auth than registry, use caller's value.
    eff_require_sct = auth.require_sct
    if require_sct is not None:
        eff_require_sct = auth.require_sct or require_sct

    eff_authority = auth.required_authority
    # caller_required_authority tightening: if caller demands MUTATE but
    # registry says OBSERVE_ONLY, the stricter (MUTATE) wins.
    _AUTHORITY_RANK = {
        "OBSERVE_ONLY": 0,
        "AUTHENTICATED_OBSERVE": 1,
        "MUTATE": 2,
        "MUTATE_PRIVILEGED": 3,
        "LIMITED_MUTATE": 2,
        "FULL": 3,
        "SOVEREIGN": 4,
        "OPERATOR": 1,
    }
    if required_authority is not None and required_authority in _AUTHORITY_RANK:
        reg_rank = _AUTHORITY_RANK.get(eff_authority, 0)
        cal_rank = _AUTHORITY_RANK[required_authority]
        if cal_rank > reg_rank:
            eff_authority = required_authority

    actor = None
    for key in ("actor_id", "actor", "caller_actor_id"):
        if isinstance(args.get(key), str) and args[key].strip():
            actor = args[key].strip()
            break
    extraction = extract_sct_from_call(args, headers=headers, meta=meta)

    def _reject(error: str, message: str, **extra: Any) -> dict[str, Any]:
        body: dict[str, Any] = {
            "error": error,
            "message": message,
            "tool": tool_name,
            "organ": organ,
            "actor": actor,
            "registry": auth.to_dict(),
            "extraction": extraction.to_dict(),
            "_epistemic": {
                "output_class": "GOVERNANCE_TEMPLATE",
                "authority_claim": "GATE_REJECTED",
                "tagged_by": "federation-sct-gate",
                "schema_version": "2.0.0",
            },
        }
        body.update(extra)
        tid = _emit_gate_decision(
            tool_name=tool_name,
            organ=organ,
            decision="REJECT",
            reason_code=error,
            arguments=args,
            headers=headers,
            meta=meta,
            actor=actor,
            auth=auth,
            extraction=extraction,
            eff_require_sct=eff_require_sct,
            eff_authority=eff_authority,
        )
        if tid:
            body["trace_id"] = tid
        return body

    # AMBIGUOUS — conflicting tokens → REJECT immediately
    if extraction.status == "AMBIGUOUS":
        return _reject(
            "SCT_AMBIGUOUS",
            (
                f"Tool '{tool_name}' received {extraction.unique_fingerprints} distinct "
                f"SCT tokens from {extraction.source_count} sources. "
                f"All sources must carry the same token."
            ),
        )

    # ABSENT — no token found
    if extraction.status == "ABSENT":
        if eff_require_sct:
            return _reject(
                "SCT_REQUIRED",
                (
                    f"Tool '{tool_name}' requires a valid Session Capability Token "
                    f"(session_token / _meta.sct / X-ArifOS-SCT). Mint via arif_init. "
                    f"Registry: action_class={auth.action_class} "
                    f"required_authority={eff_authority}."
                ),
            )
        # ALLOW observe path — still emit decision for black box
        _emit_gate_decision(
            tool_name=tool_name,
            organ=organ,
            decision="ALLOW",
            reason_code="OK_OBSERVE_NO_SCT",
            arguments=args,
            headers=headers,
            meta=meta,
            actor=actor,
            auth=auth,
            extraction=extraction,
            eff_require_sct=eff_require_sct,
            eff_authority=eff_authority,
        )
        # Do NOT inject _sct_trace_id into arguments — breaks Pydantic tool schemas.
        # Trace lives in decision-event log only (PR3).
        return None

    # PRESENT — verify the single unique token against registry floor
    rej = verify_or_reject(
        extraction.token,
        expected_actor=actor,
        required_authority=eff_authority,
        meta=meta,
    )
    if rej is None:
        _emit_gate_decision(
            tool_name=tool_name,
            organ=organ,
            decision="ALLOW",
            reason_code="OK_SCT_VALID",
            arguments=args,
            headers=headers,
            meta=meta,
            actor=actor,
            auth=auth,
            extraction=extraction,
            eff_require_sct=eff_require_sct,
            eff_authority=eff_authority,
        )
        # Do NOT inject _sct_trace_id into arguments (schema-safe).
        return None

    rej["tool"] = tool_name
    rej["organ"] = organ
    rej["registry"] = auth.to_dict()
    rej["extraction"] = extraction.to_dict()
    tid = _emit_gate_decision(
        tool_name=tool_name,
        organ=organ,
        decision="REJECT",
        reason_code=str(rej.get("error") or "SCT_INVALID"),
        arguments=args,
        headers=headers,
        meta=meta,
        actor=actor,
        auth=auth,
        extraction=extraction,
        eff_require_sct=eff_require_sct,
        eff_authority=eff_authority,
    )
    if tid:
        rej["trace_id"] = tid
    return rej
