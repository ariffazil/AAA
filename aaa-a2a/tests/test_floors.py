"""Tests for the ConstitutionalMiddleware floor gate.

Phase 2 stubs raise NotImplementedError on real methods. These tests verify
that:
    1. The class is importable and constructible.
    2. The floor inventory is exactly F1..F13 (no missing, no extras).
    3. Stub methods raise NotImplementedError with a useful message.
    4. Dry-run mode does not crash on construction.
"""

from __future__ import annotations

import pytest

from aaa_a2a.middleware.floors import ConstitutionalMiddleware


def test_constitutional_middleware_instantiation() -> None:
    """The middleware can be constructed with default arifOS URL."""
    mw = ConstitutionalMiddleware()
    assert mw.judge_url == "http://localhost:8088"
    assert mw.dry_run is False
    assert mw.actor_id == "unknown"


def test_constitutional_middleware_custom_config() -> None:
    """Custom judge URL, session_id, and actor_id are honored."""
    mw = ConstitutionalMiddleware(
        judge_url="http://arifos.local:9999",
        session_id="sess-123",
        actor_id="kimi-code",
        dry_run=True,
    )
    assert mw.judge_url == "http://arifos.local:9999"
    assert mw.session_id == "sess-123"
    assert mw.actor_id == "kimi-code"
    assert mw.dry_run is True


def test_floor_inventory_is_complete() -> None:
    """All 13 floors F1..F13 are declared."""
    expected = tuple(f"F{i}" for i in range(1, 14))
    assert ConstitutionalMiddleware.FLOORS == expected
    assert len(ConstitutionalMiddleware.FLOORS) == 13


@pytest.mark.asyncio
async def test_before_task_is_stub() -> None:
    """before_task raises NotImplementedError in Phase 2."""
    mw = ConstitutionalMiddleware(dry_run=True)
    with pytest.raises(NotImplementedError, match="Phase 2 stub"):
        await mw.before_task(task=None)


@pytest.mark.asyncio
async def test_after_task_is_stub() -> None:
    """after_task raises NotImplementedError in Phase 2."""
    mw = ConstitutionalMiddleware(dry_run=True)
    with pytest.raises(NotImplementedError, match="Phase 2 stub"):
        await mw.after_task(task=None)


def test_reversibility_check_default_conservative() -> None:
    """_check_reversibility defaults to False (F1 safe default)."""
    mw = ConstitutionalMiddleware()
    assert mw._check_reversibility(task=None) is False


def test_repr_does_not_leak_secrets() -> None:
    """__repr__ contains identifying fields but no secrets."""
    mw = ConstitutionalMiddleware(actor_id="kimi-code")
    r = repr(mw)
    assert "kimi-code" in r
    assert "localhost:8088" in r