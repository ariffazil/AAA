"""Tests for the IdentityVerifier.

Phase 2 stub. These tests verify:
    1. Importable + constructible.
    2. F9 SOVEREIGNTY guard rejects F13 impersonation.
    3. Expected protocolVersion constant is '1.0.0'.
    4. Stub methods raise NotImplementedError.
"""

from __future__ import annotations

import pytest

from aaa_a2a.middleware.identity import IdentityReceipt, IdentityVerifier


def test_identity_verifier_instantiation() -> None:
    """IdentityVerifier constructs with default registry URL."""
    v = IdentityVerifier()
    assert v.registry_url == "http://localhost:3001"
    assert v.identity_anchor_path is None


def test_expected_protocol_version() -> None:
    """A2A v1.0 protocolVersion is enforced."""
    assert IdentityVerifier.EXPECTED_PROTOCOL_VERSION == "1.0.0"


@pytest.mark.parametrize(
    "actor_id",
    ["F13", "f13", "  f13  ", "sovereign-bot", "SOVEREIGN_AGENT"],
)
def test_f13_impersonation_guard(actor_id: str) -> None:
    """F9 SOVEREIGNTY: no agent may claim F13 authority."""
    v = IdentityVerifier()
    assert v._check_f13_impersonation(actor_id) is True


@pytest.mark.parametrize("actor_id", ["kimi-code", "openclaw-anon", "hermes", "arifos"])
def test_non_f13_actors_pass_sovereignty_guard(actor_id: str) -> None:
    """F9 guard does not falsely flag normal agents."""
    v = IdentityVerifier()
    assert v._check_f13_impersonation(actor_id) is False


@pytest.mark.asyncio
async def test_verify_is_stub() -> None:
    """verify raises NotImplementedError in Phase 2."""
    v = IdentityVerifier()
    with pytest.raises(NotImplementedError, match="Phase 2 stub"):
        await v.verify(task=None)


def test_identity_receipt_is_frozen() -> None:
    """IdentityReceipt is immutable."""
    receipt = IdentityReceipt(
        agent_id="aaa-cockpit",
        actor_id="kimi-code",
        agent_card_id="sha256:abc",
        verified=True,
        verified_at="2026-07-04T09:00:00Z",
        floor_scope=("F1", "F2", "F11"),
    )
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        receipt.verified = False  # type: ignore[misc]