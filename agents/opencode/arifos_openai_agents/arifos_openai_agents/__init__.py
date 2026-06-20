"""
arifos_openai_agents — cognition firewall wrapper for OpenAI Agents SDK.

DITEMPA BUKAN DIBERI — Forged, not given.

This package wraps any OpenAI Agent with the arifOS constitutional kernel.
The 4 guards (prethink, pretool, posttool, seal) implement the Band 1
cognition-firewall pattern over OpenAI's existing primitives (guardrails,
human-in-the-loop, tools, tracing, MCP).

Usage:
    from agents import Agent
    from arifos_openai_agents import ArifKernel, CognitionLane

    kernel = ArifKernel(
        base_url="https://arifos.arif-fazil.com",
        actor_id="arif",
        session_id="...",
    )

    agent = Agent(
        name="CodexCoder",
        instructions="...",
        tools=[read_file, write_file, run_command],
    )

    wrapped = kernel.wrap(agent)
    result = await Runner.run(wrapped, "Fix the F2 bug in envelope.py")
"""

from arifos_openai_agents.decision import (
    ActionClass,
    CognitionLane,
    Decision,
    FloorVerdict,
    RiskEnvelope,
)
from arifos_openai_agents.exceptions import (
    ArifDenied,
    ArifHold,
    ArifSealMissing,
)
from arifos_openai_agents.guards import (
    arifos_posttool,
    arifos_prethink,
    arifos_pretool,
    arifos_seal,
)
from arifos_openai_agents.kernel import ArifKernel
from arifos_openai_agents.tools import ARIFOS_PRETHINK_TOOL

__all__ = [
    "ArifKernel",
    "ARIFOS_PRETHINK_TOOL",
    "ActionClass",
    "ArifDenied",
    "ArifHold",
    "ArifSealMissing",
    "CognitionLane",
    "Decision",
    "FloorVerdict",
    "RiskEnvelope",
    "arifos_posttool",
    "arifos_prethink",
    "arifos_pretool",
    "arifos_seal",
]
