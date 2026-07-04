"""Tests for organ + tool routing.

Phase 2 stub. These tests verify:
    1. Organ enum + port mapping is complete.
    2. OrganRouter falls back to A-FORGE below confidence threshold.
    3. ToolRouter resolves endpoints per organ.
    4. Stub methods raise NotImplementedError.
"""

from __future__ import annotations

import pytest

from aaa_a2a.routing.organ_router import (
    ORGAN_PORT,
    Organ,
    OrganChoice,
    OrganRouter,
)
from aaa_a2a.routing.tool_router import ToolRouter


def test_organ_enum_has_five_organs() -> None:
    """All five federation organs are declared."""
    assert {o.value for o in Organ} == {"arifos", "aforge", "geox", "wealth", "well"}


def test_organ_port_mapping_complete() -> None:
    """Every organ has a port assignment."""
    for organ in Organ:
        assert organ in ORGAN_PORT
        assert 1024 < ORGAN_PORT[organ] < 65536


def test_organ_router_fallback() -> None:
    """Below confidence threshold, OrganRouter returns A-FORGE default."""
    r = OrganRouter(default_organ=Organ.AFORGE)
    choice = r._fallback_choice(intent="obscure")
    assert choice.organ == Organ.AFORGE
    assert choice.confidence == 0.0
    assert "Fallback" in choice.reasoning


def test_tool_router_endpoints() -> None:
    """ToolRouter exposes a working endpoint_for() for every organ."""
    tr = ToolRouter()
    for organ in Organ:
        ep = tr.endpoint_for(organ)
        assert ep.startswith("http://")
        assert str(ORGAN_PORT[organ]) in ep


@pytest.mark.asyncio
async def test_organ_router_route_is_stub() -> None:
    """OrganRouter.route raises NotImplementedError in Phase 2."""
    r = OrganRouter()
    with pytest.raises(NotImplementedError, match="Phase 2 stub"):
        await r.route(intent="compute EMV for Petronas deal")


@pytest.mark.asyncio
async def test_tool_router_resolve_is_stub() -> None:
    """ToolRouter.resolve raises NotImplementedError in Phase 2."""
    tr = ToolRouter()
    with pytest.raises(NotImplementedError, match="Phase 2 stub"):
        await tr.resolve(task=None, organ=Organ.GEOX)


def test_organ_choice_is_frozen() -> None:
    """OrganChoice is immutable."""
    choice = OrganChoice(
        organ=Organ.WEALTH,
        confidence=0.85,
        alternatives={Organ.AFORGE: 0.10},
        reasoning="Capital-flow keywords detected.",
    )
    with pytest.raises(Exception):  # FrozenInstanceError
        choice.confidence = 0.5  # type: ignore[misc]