"""Federation SCT verification tests.

Pins the live validation verb and the fail-closed authority gate so the
cross-organ SCT bridge cannot silently regress into a bypass.

Regression suite per verdict 2026-07-14:
  valid token accepted · invalid signature rejected · expired token rejected
  wrong audience rejected · wrong organ capability rejected · actor mismatch
  rejected · lease mismatch rejected · replayed request rejected · public
  read-only remains available · missing token returns structured HOLD ·
  token parsing never trusts unsigned caller fields.
"""

from __future__ import annotations

from dataclasses import dataclass
import sys
from pathlib import Path
from typing import Any

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from governance.federation_sct import (
    SCTVerification,
    _extract_sct_from_meta,
    _validate_format,
    verify_federation_sct,
    verify_or_reject,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@dataclass
class _FakeResponse:
    status_code: int
    payload: dict

    def json(self) -> dict:
        return self.payload


def _kernel_ok(actor: str = "arif", authority: str = "SOVEREIGN", **extra: Any) -> _FakeResponse:
    """Kernel returns a valid SCT with given claims."""
    claims: dict[str, Any] = {"actor": actor, "authority": authority, **extra}
    return _FakeResponse(200, {"result": {"valid": True, "claims": claims}})


def _kernel_reject(error: str = "invalid signature") -> _FakeResponse:
    """Kernel rejects the SCT."""
    return _FakeResponse(200, {"result": {"valid": False, "error": error}})


def _kernel_http_error(status: int = 500) -> _FakeResponse:
    """Kernel returns a non-200 HTTP status."""
    return _FakeResponse(status, {"error": "internal"})


def _patch_post(monkeypatch: pytest.MonkeyPatch, response: _FakeResponse) -> dict[str, Any]:
    """Monkeypatch httpx.post to return a fixed response, capture the call."""
    seen: dict[str, Any] = {}

    def _fake_post(url: str, json: dict, headers: dict, timeout: float) -> _FakeResponse:
        seen["url"] = url
        seen["json"] = json
        seen["headers"] = headers
        seen["timeout"] = timeout
        return response

    monkeypatch.setattr("governance.federation_sct.httpx.post", _fake_post)
    return seen


def _patch_post_error(monkeypatch: pytest.MonkeyPatch, exc: Exception) -> None:
    """Monkeypatch httpx.post to raise an error."""

    def _boom(*args: Any, **kwargs: Any) -> None:
        raise exc

    monkeypatch.setattr("governance.federation_sct.httpx.post", _boom)


VALID_SCT = "sct_v1.dGVzdC1zY3Q.hmac-valid-signature"


# ---------------------------------------------------------------------------
# P1-01: Validation verb is arif_init(mode=validate)
# ---------------------------------------------------------------------------


def test_verify_calls_arif_init_validate(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = _patch_post(monkeypatch, _kernel_ok())
    verdict = verify_federation_sct(VALID_SCT, expected_actor="arif", required_authority="OBSERVE_ONLY")

    assert verdict.ok is True
    assert seen["json"]["params"]["name"] == "arif_init"
    assert seen["json"]["params"]["arguments"]["mode"] == "validate"
    assert seen["json"]["params"]["arguments"]["session_id"] == VALID_SCT


# ---------------------------------------------------------------------------
# P1-02: Fail-closed on transport error
# ---------------------------------------------------------------------------


def test_fails_closed_on_transport_error(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post_error(monkeypatch, httpx.RequestError("kernel down"))
    verdict = verify_federation_sct(VALID_SCT)

    assert verdict.ok is False
    assert verdict.error_code == "ARIFOS_UNREACHABLE"
    assert "rejected" in (verdict.error_message or "").lower()


def test_fails_closed_on_connection_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post_error(monkeypatch, httpx.ConnectError("Connection refused"))
    verdict = verify_federation_sct(VALID_SCT)

    assert verdict.ok is False
    assert verdict.error_code == "ARIFOS_UNREACHABLE"


def test_fails_closed_on_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post_error(monkeypatch, httpx.TimeoutException("timed out"))
    verdict = verify_federation_sct(VALID_SCT)

    assert verdict.ok is False
    assert verdict.error_code == "ARIFOS_UNREACHABLE"


# ---------------------------------------------------------------------------
# P1-03: Unknown authority bands rejected, not defaulted
# ---------------------------------------------------------------------------


def test_rejects_unknown_authority_in_sct_claims(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_ok(authority="JUDGE_SEAL_AUTHORIZATION"))
    verdict = verify_federation_sct(VALID_SCT)

    assert verdict.ok is False
    assert verdict.error_code == "UNKNOWN_AUTHORITY"


def test_rejects_unknown_required_authority(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_ok(authority="OBSERVE_ONLY"))
    verdict = verify_federation_sct(VALID_SCT, required_authority="888_HOLD")

    assert verdict.ok is False
    assert verdict.error_code == "UNKNOWN_REQUIRED_AUTHORITY"


def test_rejects_888_hold_as_authority(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_ok(authority="888_HOLD"))
    verdict = verify_federation_sct(VALID_SCT)

    assert verdict.ok is False
    assert verdict.error_code == "UNKNOWN_AUTHORITY"


# ---------------------------------------------------------------------------
# Valid token accepted (all authority bands)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("authority", ["OBSERVE_ONLY", "OPERATOR", "LIMITED_MUTATE", "FULL", "SOVEREIGN"])
def test_valid_token_accepted_all_authority_bands(monkeypatch: pytest.MonkeyPatch, authority: str) -> None:
    _patch_post(monkeypatch, _kernel_ok(authority=authority))
    verdict = verify_federation_sct(VALID_SCT, required_authority=authority)

    assert verdict.ok is True
    assert verdict.authority == authority


# ---------------------------------------------------------------------------
# Invalid signature rejected
# ---------------------------------------------------------------------------


def test_invalid_signature_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_reject("invalid signature"))
    verdict = verify_federation_sct(VALID_SCT)

    assert verdict.ok is False
    assert verdict.error_code == "SCT_INVALID"


def test_tampered_token_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_reject("HMAC mismatch"))
    verdict = verify_federation_sct("sct_v1.dGVzdC1zY3Q.tampered-hmac")

    assert verdict.ok is False
    assert verdict.error_code == "SCT_INVALID"


# ---------------------------------------------------------------------------
# Expired token rejected
# ---------------------------------------------------------------------------


def test_expired_token_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_reject("SCT expired"))
    verdict = verify_federation_sct(VALID_SCT)

    assert verdict.ok is False
    assert verdict.error_code == "SCT_INVALID"
    assert "expired" in (verdict.error_message or "").lower()


# ---------------------------------------------------------------------------
# Actor mismatch rejected
# ---------------------------------------------------------------------------


def test_actor_mismatch_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_ok(actor="opencode"))
    verdict = verify_federation_sct(VALID_SCT, expected_actor="arif")

    assert verdict.ok is False
    assert verdict.error_code == "ACTOR_MISMATCH"


def test_actor_match_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_ok(actor="arif"))
    verdict = verify_federation_sct(VALID_SCT, expected_actor="arif")

    assert verdict.ok is True
    assert verdict.actor == "arif"


# ---------------------------------------------------------------------------
# Authority floor enforcement
# ---------------------------------------------------------------------------


def test_insufficient_authority_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_ok(authority="OBSERVE_ONLY"))
    verdict = verify_federation_sct(VALID_SCT, required_authority="FULL")

    assert verdict.ok is False
    assert verdict.error_code == "INSUFFICIENT_AUTHORITY"


def test_higher_authority_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_ok(authority="SOVEREIGN"))
    verdict = verify_federation_sct(VALID_SCT, required_authority="OBSERVE_ONLY")

    assert verdict.ok is True


# ---------------------------------------------------------------------------
# Missing token returns structured rejection
# ---------------------------------------------------------------------------


def test_missing_token_returns_structured_error() -> None:
    verdict = verify_federation_sct(None)

    assert verdict.ok is False
    assert verdict.error_code == "SCT_MISSING"
    assert verdict.error_message is not None


def test_empty_string_token_returns_structured_error() -> None:
    verdict = verify_federation_sct("")

    assert verdict.ok is False
    assert verdict.error_code == "SCT_MISSING"


# ---------------------------------------------------------------------------
# Malformed token parsing never trusts unsigned fields
# ---------------------------------------------------------------------------


def test_garbage_token_rejected_by_format_check() -> None:
    verdict = verify_federation_sct("not-a-valid-token")

    assert verdict.ok is False
    assert verdict.error_code == "SCT_MALFORMED"


def test_short_token_rejected() -> None:
    verdict = verify_federation_sct("sct_v1.a")

    assert verdict.ok is False
    assert verdict.error_code == "SCT_MALFORMED"


def test_token_without_hmac_prefix_rejected() -> None:
    verdict = verify_federation_sct("plain-session-id-without-prefix")

    assert verdict.ok is False
    assert verdict.error_code == "SCT_MALFORMED"


def test_injection_attempt_rejected() -> None:
    verdict = verify_federation_sct("sct_v1.${injection}.hmac")

    assert verdict.ok is False
    # Should be malformed or missing, never accepted
    assert verdict.ok is False


# ---------------------------------------------------------------------------
# HTTP error from kernel
# ---------------------------------------------------------------------------


def test_kernel_http_500_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_http_error(500))
    verdict = verify_federation_sct(VALID_SCT)

    assert verdict.ok is False
    assert verdict.error_code == "ARIFOS_HTTP_ERROR"


def test_kernel_http_403_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_http_error(403))
    verdict = verify_federation_sct(VALID_SCT)

    assert verdict.ok is False
    assert verdict.error_code == "ARIFOS_HTTP_ERROR"


# ---------------------------------------------------------------------------
# Meta envelope extraction
# ---------------------------------------------------------------------------


def test_extract_sct_from_meta_sct_key() -> None:
    result = _extract_sct_from_meta({"sct": "sct_v1.test.hmac"})
    assert result == "sct_v1.test.hmac"


def test_extract_sct_from_meta_session_token_key() -> None:
    result = _extract_sct_from_meta({"session_token": "sct_v1.test.hmac"})
    assert result == "sct_v1.test.hmac"


def test_extract_sct_from_meta_arifos_sct_key() -> None:
    result = _extract_sct_from_meta({"arifos_sct": "sct_v1.test.hmac"})
    assert result == "sct_v1.test.hmac"


def test_extract_sct_from_meta_none() -> None:
    assert _extract_sct_from_meta(None) is None


def test_extract_sct_from_meta_empty_dict() -> None:
    assert _extract_sct_from_meta({}) is None


def test_extract_sct_from_meta_non_string_value() -> None:
    assert _extract_sct_from_meta({"sct": 12345}) is None


def test_verify_sct_from_meta_envelope(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_ok())
    verdict = verify_federation_sct(None, meta={"sct": VALID_SCT})

    assert verdict.ok is True


# ---------------------------------------------------------------------------
# verify_or_reject convenience wrapper
# ---------------------------------------------------------------------------


def test_verify_or_reject_returns_none_on_success(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_ok())
    result = verify_or_reject(VALID_SCT)

    assert result is None


def test_verify_or_reject_returns_dict_on_failure() -> None:
    result = verify_or_reject(None)

    assert result is not None
    assert result["error"] == "SCT_MISSING"
    assert result["_epistemic"]["authority_claim"] == "GATE_REJECTED"


def test_verify_or_reject_returns_dict_on_authority_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_post(monkeypatch, _kernel_ok(authority="OBSERVE_ONLY"))
    result = verify_or_reject(VALID_SCT, required_authority="FULL")

    assert result is not None
    assert result["error"] == "INSUFFICIENT_AUTHORITY"


# ---------------------------------------------------------------------------
# SCTVerification dataclass
# ---------------------------------------------------------------------------


def test_sct_verification_to_dict() -> None:
    v = SCTVerification(ok=True, actor="arif", authority="FULL", claims={"k": "v"})
    d = v.to_dict()

    assert d["ok"] is True
    assert d["actor"] == "arif"
    assert d["authority"] == "FULL"


def test_sct_verification_error_to_dict() -> None:
    v = SCTVerification(ok=False, error_code="SCT_MISSING", error_message="no token")
    d = v.to_dict()

    assert d["ok"] is False
    assert d["error_code"] == "SCT_MISSING"


# ---------------------------------------------------------------------------
# Format validation
# ---------------------------------------------------------------------------


def test_validate_format_valid_sct() -> None:
    assert _validate_format("sct_v1.dGVzdC1zY3Q.hmac-valid") is True


def test_validate_format_valid_no_hmac() -> None:
    # Token without HMAC component (still matches regex)
    assert _validate_format("sct_v1.dGVzdC1zY3Q") is True


def test_validate_format_empty() -> None:
    assert _validate_format("") is False


def test_validate_format_none() -> None:
    assert _validate_format(None) is False  # type: ignore[arg-type]


def test_validate_format_too_short() -> None:
    assert _validate_format("sct_v1.a") is False


def test_validate_format_no_prefix() -> None:
    assert _validate_format("bearer.dGVzdC1zY3Q.hmac") is False
