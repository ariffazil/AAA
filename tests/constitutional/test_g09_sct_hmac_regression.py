"""G-09 regression — the SCT recovery branch must verify the HMAC.

WHY THIS FILE EXISTS
--------------------
G-09 (reality-graph/FLOW_GAPS.md): the sovereign-ignition recovery branch in
federation_act.py decoded the token payload and trusted the `auth` claim because
the signature region was only SHAPE-valid. No HMAC was ever checked. Proven
2026-09-14: 4 of 6 attempts ALLOWED a garbage signature
(act_v1.<b64({"auth":"SOVEREIGN"})>.deadbeefdeadbeef) into GEOX, WELL and WEALTH.

The fix shipped on main; this file keeps it from silently regressing.

WHY NOT test_federation_act.py
------------------------------
That file (41 tests) has been UNCOLLECTABLE since the "SCT -> ACT rename" commit:
it imports `_extract_sct_from_meta` and `_validate_format`, neither of which exists
any more. So the module's own tests have not run in a long time, and the security
fix would have landed with ZERO coverage. This file is deliberately self-contained
and imports only symbols that exist, so it runs today.

THE PATH UNDER TEST
-------------------
The stub kernel answers 200 with valid=false — the recovery branch's own trigger.
An unreachable kernel is NOT a valid substitute: that hits the ARIFOS_UNREACHABLE
branch, which was already fail-closed, and is why the original probe's 2 rejections
were called "not structural".
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from governance.federation_act import (  # noqa: E402
    _resolve_local_signing_secret,
    _verify_local_hmac,
    verify_federation_sct,
)


# ── fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture
def pending_kernel():
    """A REACHABLE kernel that declines to confirm the token (valid=false)."""

    class _H(BaseHTTPRequestHandler):
        def do_POST(self):  # noqa: N802
            n = int(self.headers.get("Content-Length") or 0)
            self.rfile.read(n)
            body = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "result": {"valid": False, "error": "session pending", "claims": {}},
                }
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):  # silence
            return

    srv = HTTPServer(("127.0.0.1", 0), _H)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()
    srv.server_close()


def _b64(payload: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")


def _forged(auth: str = "SOVEREIGN") -> str:
    """A structurally valid token whose signature is meaningless."""
    return f"act_v1.{_b64({'auth': auth, 'actor': 'ARIF', 'act_v': 1})}.deadbeefdeadbeef"


def _genuine(secret: bytes, auth: str = "SOVEREIGN") -> str:
    """The same payload, correctly signed with the verifier's own key."""
    b = _b64({"auth": auth, "actor": "ARIF", "act_v": 1})
    sig = hmac.new(secret, b.encode("ascii"), hashlib.sha256).hexdigest()
    return f"act_v1.{b}.{sig}"


# ── the regression ────────────────────────────────────────────────────────


def test_forged_signature_is_refused_on_the_recovery_path(pending_kernel, monkeypatch):
    """G-09: a token with a garbage signature must NOT resolve as authority."""
    import governance.federation_act as fa

    monkeypatch.setattr(fa, "ARIFOS_BASE", pending_kernel)
    v = verify_federation_sct(
        _forged(), expected_actor="ARIF", required_authority="SOVEREIGN"
    )
    assert v.ok is False, (
        "FORGED TOKEN ACCEPTED — G-09 has regressed. A token whose signature was "
        "never verified must never resolve to SOVEREIGN."
    )
    assert v.error_code in {"SCT_HMAC_MISMATCH", "SCT_HMAC_UNCOMPUTABLE"}, v.error_code


def test_genuine_signature_still_passes(pending_kernel, monkeypatch):
    """The fix must not break the sovereign-ignition path it exists to serve."""
    import governance.federation_act as fa

    secret = _resolve_local_signing_secret()
    if secret is None:
        pytest.skip("SCT signing secret unavailable in this environment")

    monkeypatch.setattr(fa, "ARIFOS_BASE", pending_kernel)
    v = verify_federation_sct(
        _genuine(secret), expected_actor="ARIF", required_authority="SOVEREIGN"
    )
    assert v.ok is True, f"genuine token rejected: {v.error_code} {v.error_message}"
    assert v.authority == "SOVEREIGN"


def test_hmac_verifier_rejects_a_tampered_payload():
    """Flipping one payload byte must invalidate the signature."""
    secret = _resolve_local_signing_secret()
    if secret is None:
        pytest.skip("SCT signing secret unavailable in this environment")

    token = _genuine(secret)
    _, payload_b64, sig = token.split(".", 2)
    assert _verify_local_hmac(payload_b64, sig)[0] is True

    tampered = base64.urlsafe_b64encode(
        json.dumps({"auth": "SOVEREIGN", "actor": "ARIF", "act_v": 1, "extra": 1}).encode()
    ).decode().rstrip("=")
    ok, reason = _verify_local_hmac(tampered, sig)
    assert ok is False, "tampered payload accepted — signature does not cover the payload"
    assert reason == "SCT_HMAC_MISMATCH"


def test_hmac_verifier_fails_closed_without_a_key(monkeypatch):
    """No key => no authority. Never a permissive default."""
    import governance.federation_act as fa

    monkeypatch.setattr(fa, "_resolve_local_signing_secret", lambda: None)
    ok, reason = _verify_local_hmac("anything", "a" * 64)
    assert ok is False
    assert reason == "SCT_HMAC_SECRET_UNAVAILABLE"
