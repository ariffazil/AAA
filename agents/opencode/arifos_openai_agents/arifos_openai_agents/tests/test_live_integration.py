"""
test_live_integration.py — End-to-end test against the live arifOS MCP.

Skipped by default. Run with: pytest -m live_integration

These tests verify that the arifOS OpenAI SDK actually talks to the
public arifOS MCP at arifos.arif-fazil.com.
"""

from __future__ import annotations

import pytest
from arifos_openai_agents.client import ArifOSMCPClient
from arifos_openai_agents.decision import ActionClass, CognitionLane
from arifos_openai_agents.guards import arifos_prethink

pytestmark = pytest.mark.live_integration


@pytest.mark.asyncio
async def test_live_prethink_against_public_arifos():
    """Issue a real prethink call to the live arifOS MCP."""
    client = ArifOSMCPClient()  # Default: arifos.arif-fazil.com
    decision = await arifos_prethink(
        intent_summary="observe the live kernel health",
        proposed_lane=CognitionLane.OBSERVE,
        proposed_action_class=ActionClass.OBSERVE,
        estimated_blast_radius="NONE",
        client=client,
    )
    # Should not be DENY on a read-only request
    assert decision.verdict != "DENY", f"Live prethink denied: {decision.reasons}"
    print(f"Live prethink result: verdict={decision.verdict}, lease={decision.lease_id}")


@pytest.mark.asyncio
async def test_live_publish_request_holds():
    """A PUBLISH request to the live kernel should 888 HOLD."""
    client = ArifOSMCPClient()
    decision = await arifos_prethink(
        intent_summary="publish to external channel",
        proposed_lane=CognitionLane.EXECUTE,
        proposed_action_class=ActionClass.PUBLISH,
        estimated_blast_radius="EXTERNAL",
        client=client,
    )
    # F1 short-circuit should HOLD
    assert decision.verdict == "HOLD"
    assert decision.required_human_ack is True
