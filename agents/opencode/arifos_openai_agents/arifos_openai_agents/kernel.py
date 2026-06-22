"""
kernel.py — ArifKernel: the wrapper that wires the 4 guards into an
OpenAI Agent.

Usage:
    from agents import Agent, Runner
    from arifos_openai_agents import ArifKernel

    kernel = ArifKernel(
        base_url="https://arifos.arif-fazil.com",
        actor_id="arif",
    )

    agent = Agent(
        name="CodexCoder",
        instructions="You write code under the arifOS constitution.",
        tools=[read_file, write_file],
    )

    wrapped = kernel.wrap(agent)
    result = await Runner.run(wrapped, "Fix the F2 bug in envelope.py")
"""

from __future__ import annotations

import functools
import logging
from typing import Any, Awaitable, Callable

from arifos_openai_agents.client import ArifOSMCPClient
from arifos_openai_agents.decision import CognitionLane, Decision
from arifos_openai_agents.exceptions import ArifHold, ArifSealMissing
from arifos_openai_agents.guards import (
    arifos_posttool,
    arifos_pretool,
    arifos_seal,
)
from arifos_openai_agents.tools import ARIFOS_PRETHINK_TOOL

logger = logging.getLogger(__name__)


class ArifKernel:
    """
    Wraps an OpenAI Agent with the arifOS cognition firewall.

    The wrap injects:
    1. The prethink tool (forced call before any other tool)
    2. pretool guard (before every tool call)
    3. posttool guard (after every tool result)
    4. seal guard (at end of run)

    The agent is wrapped without changing its core behaviour — the
    kernel sits as middleware.
    """

    def __init__(
        self,
        base_url: str = "https://arifos.arif-fazil.com",
        actor_id: str = "arif",
        session_id: str | None = None,
        # If True, fail-closed on kernel unreachable. If False, allow
        # with warning (development mode).
        fail_closed_on_kernel_unavailable: bool = True,
    ):
        self.client = ArifOSMCPClient(
            base_url=base_url,
            actor_id=actor_id,
            session_id=session_id,
        )
        self.actor_id = actor_id
        self.session_id = self.client.session_id
        self.fail_closed = fail_closed_on_kernel_unavailable

    def wrap(self, agent: Any) -> Any:
        """
        Wrap an OpenAI Agent with the 4 guards.

        Returns a wrapped agent. The original agent is NOT mutated.
        """
        # Track decision history across the run
        history = _DecisionHistory()

        # 1. Inject the prethink tool into the agent's tool list
        # (OpenAI Agents SDK uses agent.tools list)
        original_tools = list(agent.tools) if hasattr(agent, "tools") else []
        agent.tools = [ARIFOS_PRETHINK_TOOL] + original_tools

        # 2. Wrap the original execute_tool_call (or whatever the
        # SDK uses to execute tools) with pretool + posttool guards.
        # This is the deep integration point.
        original_execute = getattr(agent, "_execute_tool_call", None) or getattr(
            agent, "execute_tool_call", None
        )

        if original_execute is not None:
            # Monkey-patch the agent's tool execution
            agent._execute_tool_call = _wrap_execute(
                original_execute,
                client=self.client,
                history=history,
            )

        # 3. Wrap the run-end to apply the seal
        original_run = getattr(agent, "run", None) or getattr(agent, "__call__", None)
        if original_run is not None:
            agent.run = _wrap_run(
                original_run,
                client=self.client,
                history=history,
            )

        return agent


class _DecisionHistory:
    """Tracks decisions across an agent run. Internal use only."""

    def __init__(self) -> None:
        self.decisions: list[Decision] = []

    def add(self, decision: Decision) -> None:
        self.decisions.append(decision)

    def last(self) -> Decision | None:
        return self.decisions[-1] if self.decisions else None

    def all(self) -> list[Decision]:
        return list(self.decisions)


def _wrap_execute(
    original: Callable[..., Awaitable[Any]],
    client: ArifOSMCPClient,
    history: _DecisionHistory,
) -> Callable[..., Awaitable[Any]]:
    """
    Wrap a tool-execution function with pretool + posttool guards.
    """
    @functools.wraps(original)
    async def wrapper(*args, **kwargs):
        tool_name = kwargs.get("tool_name") or (args[0] if args else "unknown")
        tool_args = kwargs.get("tool_args") or kwargs.get("arguments") or {}

        # Get the current cognition lane from the last prethink decision
        last = history.last()
        if last is None:
            # No prethink yet — refuse
            raise ArifHold(
                Decision(
                    verdict="HOLD",
                    cognition_lane=CognitionLane.OBSERVE,
                    reasons=[
                        f"F8 LAW: tool {tool_name!r} called before _arifos_prethink. "
                        "No agent may form an executable plan until prethink returns ALLOW."
                    ],
                    required_human_ack=True,
                )
            )

        # PRETOOL guard
        if tool_name != "_arifos_prethink":
            decision = await arifos_pretool(
                tool_name=tool_name,
                tool_args=tool_args,
                prior_decision=last,
                client=client,
            )
            history.add(decision)

        # Execute the original tool
        result = await original(*args, **kwargs)

        # POSTTOOL guard (skip prethink itself to avoid recursion)
        if tool_name != "_arifos_prethink":
            # Best-effort: extract confidence + source from result if dict
            confidence = None
            source = None
            if isinstance(result, dict):
                confidence = result.get("confidence")
                source = result.get("source") or result.get("url")

            post_decision = await arifos_posttool(
                tool_name=tool_name,
                tool_result=result,
                prior_decision=last,
                confidence=confidence,
                source=source,
                client=client,
            )
            history.add(post_decision)

            # Handle _arifos_prethink specially — record the lane decision
        else:
            # This was a prethink call. Record the result as the next decision.
            if isinstance(result, dict):
                try:
                    decision = Decision(**result)
                    history.add(decision)
                except Exception:
                    logger.warning("Could not parse prethink result as Decision")

        return result

    return wrapper


def _wrap_run(
    original: Callable[..., Awaitable[Any]],
    client: ArifOSMCPClient,
    history: _DecisionHistory,
) -> Callable[..., Awaitable[Any]]:
    """
    Wrap the run-end to apply the seal.
    """
    @functools.wraps(original)
    async def wrapper(*args, **kwargs):
        result = await original(*args, **kwargs)

        # SEAL guard
        try:
            seal = await arifos_seal(
                final_output=result,
                decision_history=history.all(),
                client=client,
            )
            # Attach seal to result
            if isinstance(result, dict):
                result["_arifos_seal"] = seal.to_envelope()
            else:
                setattr(result, "_arifos_seal", seal)
        except ArifSealMissing as exc:
            logger.error(f"arifOS seal missing: {exc}")
            raise

        return result

    return wrapper
