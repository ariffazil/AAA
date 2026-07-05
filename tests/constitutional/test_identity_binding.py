"""Identity binding tests — Stage 4 (2026-07-05).

Covers:
  - ActorVerified default state (verified=False, no bridge, no auth)
  - BridgingSeal dataclass constraints (TTL bounds, required fields)
  - Stub bodies raise NotImplementedError (no fake crypto)
  - JWT stub bodies raise (encode/decode)
  - DPoP stub bodies raise (mint/verify)
  - actor_verified never returns True without real crypto (F2 TRUTH)
"""

from __future__ import annotations

import pytest


# ─── actor_verified ───────────────────────────────────────────────────────────


def test_actor_verified_default_state_denies(identity_pkgs):
    """F2 TRUTH: actor_verified default-returns-False without bridge seal."""
    av = identity_pkgs.ActorVerified()
    assert av.verified is False, "must default-verify=False"
    assert av.state.value == "UNVERIFIED", "must default-state=UNVERIFIED"
    assert av.is_authorized() is False, "must default-deny"


def test_actor_verified_with_expired_bridge_denies(identity_pkgs):
    """F13 SOVEREIGN — TTL bounded; expired seal must deny."""
    from datetime import datetime, timezone, timedelta

    av = identity_pkgs.ActorVerified(actor_id="arif")
    past = datetime(2020, 1, 1, tzinfo=timezone.utc)
    av_expired = identity_pkgs.ActorVerified(
        actor_id="arif",
        bridge_seal_id="SEAL-fake",
        expires_at_epoch=past,
    )
    assert av_expired.is_authorized(current_epoch=datetime.now(timezone.utc)) is False


def test_actor_verified_bridge_does_not_set_verified_true(identity_pkgs):
    """F2 TRUTH — bridge toggles `state`, never toggles `verified`."""
    av = identity_pkgs.ActorVerified(actor_id="arif")
    # Touch bridge path
    av_bridged = identity_pkgs.ActorVerified(
        actor_id="arif",
        state=identity_pkgs.ActorVerifiedState.BRIDGED,
        bridge_seal_id="SEAL-pending-real-impl",
    )
    assert av_bridged.verified is False, "F2: bridge must NOT set verified=True"
    assert av_bridged.state.value == "BRIDGED"


def test_actor_verified_serialisable_snapshot(identity_pkgs):
    av = identity_pkgs.ActorVerified(actor_id="arif")
    snap = av.to_dict()
    assert "actor_id" in snap
    assert "state" in snap
    assert "verified" in snap
    assert snap["verified"] is False
    assert "F2" in snap["note_if_unverified"] or "TRUTH" in snap["note_if_unverified"]


# ─── BridgingSeal constraints ────────────────────────────────────────────────


def test_bridging_seal_rejects_zero_ttl(identity_pkgs):
    with pytest.raises(ValueError, match="ttl_seconds"):
        identity_pkgs.BridgingSealRequest(
            sovereign_authorization="test",
            intent="x",
            ttl_seconds=0,
        )


def test_bridging_seal_rejects_oversized_ttl(identity_pkgs):
    with pytest.raises(ValueError, match="ttl_seconds"):
        identity_pkgs.BridgingSealRequest(
            sovereign_authorization="test",
            intent="x",
            ttl_seconds=3601,
        )


def test_bridging_seal_rejects_empty_sovereign_authorization(identity_pkgs):
    with pytest.raises(ValueError, match="sovereign_authorization"):
        identity_pkgs.BridgingSealRequest(
            sovereign_authorization="   ",
            intent="x",
        )


def test_bridging_seal_rejects_empty_intent(identity_pkgs):
    with pytest.raises(ValueError, match="intent"):
        identity_pkgs.BridgingSealRequest(
            sovereign_authorization="test",
            intent="",
        )


def test_bridging_seal_default_ttl_is_fifteen_minutes(identity_pkgs):
    """F13 SOVEREIGN — bounded; 900 sec is the constitutional default."""
    assert identity_pkgs.request_bridging_seal.__doc__ is not None
    # Use the proxy attributes — direct `from arifosmcp.runtime.identity.bridging_seal import`
    # would chain-load runtime/__init__.py and trip the broken core.shared chain.
    bs = identity_pkgs.bridge_seal_module
    assert bs.ttl_default_seconds() == 900
    assert bs.max_ttl_seconds() == 3600


def test_bridging_seal_stub_body_raises(identity_pkgs):
    """F1 AMANAH — stubs raise, never fall-through to fake crypto."""
    req = identity_pkgs.BridgingSealRequest(
        sovereign_authorization="yes seal",
        intent="test",
    )
    with pytest.raises(NotImplementedError):
        identity_pkgs.request_bridging_seal(req)
    with pytest.raises(NotImplementedError):
        identity_pkgs.verify_bridging_seal(
            identity_pkgs.BridgingSealReceipt(
                seal_id="SEAL-x",
                epoch=__import__("datetime").datetime(2026, 7, 5),
                expires_at=__import__("datetime").datetime(2026, 7, 5),
                actor_override=True,
                sovereign_signature="STUB",
            )
        )


# ─── JWT + DPoP stubs ────────────────────────────────────────────────────────


def test_jwt_encode_stub_raises(identity_pkgs):
    with pytest.raises(NotImplementedError):
        identity_pkgs.encode_jwt({"iss": "test"}, b"key")


def test_jwt_decode_stub_raises(identity_pkgs):
    with pytest.raises(NotImplementedError):
        identity_pkgs.decode_jwt("a.b.c", b"key")


def test_dpop_mint_stub_raises(identity_pkgs):
    with pytest.raises(NotImplementedError):
        identity_pkgs.make_dpop_proof("GET", "https://x.test", "tok", b"key")


def test_dpop_verify_stub_raises(identity_pkgs):
    with pytest.raises(NotImplementedError):
        identity_pkgs.verify_dpop_proof("a.b.c", "GET", "https://x.test", b"key")


def test_stub_algorithm_constant(identity_pkgs):
    sentinel = identity_pkgs.stub_algorithm()
    assert "PLACEHOLDER" in sentinel.upper()
    assert "REPLACE" in sentinel.upper()
    assert "BEFORE_PROD" in sentinel.upper()
