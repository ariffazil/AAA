"""G-09 regression — the cross-organ SCT recovery path must never grant
authority on an unverified or non-current token.

Background. The sovereign-ignition recovery branch in
`governance/federation_act.py` runs whenever the kernel's `validate` verb
returns not-valid, which is its normal answer for live sessions. Until
2026-09-20 that branch decoded the payload and trusted the `auth` claim
after only SHAPE-CHECKING the signature, so a forged token bearing any
signature reached GEOX, WELL and WEALTH ingress (recorded as G-09 in
AAA/reality-graph/FLOW_GAPS.md; FI-008 measured 4 of 6 attempts allowed).

FI-008 closed the core defect with a local HMAC check. FI-003 then found
the residual: the branch verified the signature but never checked `exp`,
`act_v`, or actor binding, so a validly-signed but EXPIRED token — or
another actor's token — still authorised.

This file exists because the older suite in `test_federation_act.py` can
no longer be collected at all (it imports helpers that have since been
renamed), which is precisely how the defect survived unnoticed. These
tests depend on nothing but the module's public verify entry point.

Run:  python3 -m pytest tests/constitutional/test_federation_act_g09.py -q
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from governance.federation_act import verify_federation_sct

LIVE = {"act_v": 1, "auth": "SOVEREIGN", "actor": "ARIF"}


class _KernelRejects:
    """Kernel `validate` answers not-valid — this forces the recovery branch."""

    status_code = 200
    text = ""

    def json(self) -> dict[str, Any]:
        return {"result": {"valid": False, "error": "kernel pending"}}


@pytest.fixture()
def kernel_rejects(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "governance.federation_act.httpx.post", lambda *a, **k: _KernelRejects()
    )


@pytest.fixture()
def secret() -> bytes:
    key = os.getenv("ARIFOS_SESSION_SECRET", "").strip()
    if not key:
        pytest.skip("ARIFOS_SESSION_SECRET unavailable — signing tests need the ACT key")
    return key.encode()


def _token(payload: dict[str, Any], key: bytes, sig: str | None = None) -> str:
    b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    if sig is None:
        sig = hmac.new(key, b64.encode(), hashlib.sha256).hexdigest()
    return f"act_v1.{b64}.{sig}"


def test_valid_signed_token_is_accepted(kernel_rejects: None, secret: bytes) -> None:
    """The recovery path must still work — a live signed token authorises."""
    v = verify_federation_sct(_token(LIVE, secret), expected_actor="ARIF")
    assert v.ok is True
    assert v.authority == "SOVEREIGN"


def test_unsigned_token_is_rejected(kernel_rejects: None, secret: bytes) -> None:
    """G-09 core: forged token, shape-valid signature, no HMAC."""
    v = verify_federation_sct(
        _token(LIVE, secret, sig="de" * 32), expected_actor="ARIF"
    )
    assert v.ok is False
    assert v.error_code == "SCT_HMAC_MISMATCH"


def test_token_signed_with_wrong_key_is_rejected(
    kernel_rejects: None, secret: bytes
) -> None:
    v = verify_federation_sct(
        _token(LIVE, b"not-the-kernel-key"), expected_actor="ARIF"
    )
    assert v.ok is False
    assert v.error_code == "SCT_HMAC_MISMATCH"


def test_expired_signed_token_is_rejected(kernel_rejects: None, secret: bytes) -> None:
    """G-09 residual: the signature proves provenance, not currency."""
    v = verify_federation_sct(
        _token({**LIVE, "exp": time.time() - 60}, secret), expected_actor="ARIF"
    )
    assert v.ok is False
    assert v.error_code == "SCT_EXPIRED"


def test_unsupported_version_is_rejected(kernel_rejects: None, secret: bytes) -> None:
    v = verify_federation_sct(
        _token({**LIVE, "act_v": 2}, secret), expected_actor="ARIF"
    )
    assert v.ok is False
    assert v.error_code == "SCT_VERSION_UNSUPPORTED"


def test_actor_mismatch_is_rejected(kernel_rejects: None, secret: bytes) -> None:
    """A token minted for one actor must not authorise another organ."""
    v = verify_federation_sct(_token(LIVE, secret), expected_actor="GEOX")
    assert v.ok is False
    assert v.error_code == "SCT_ACTOR_MISMATCH"
