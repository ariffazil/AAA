"""
example_codex_agent.py — Worked example: wrap a Codex agent with arifOS.

This shows the SDK in action with the OpenAI Agents SDK. The agent
cannot take any action without first calling _arifos_prethink.

Usage:
    OPENAI_API_KEY=sk-... python example_codex_agent.py
"""

from __future__ import annotations

import asyncio
import os

from arifos_openai_agents import ArifKernel

from agents import Agent, Runner, function_tool


@function_tool
def read_file(path: str) -> str:
    """Read a file from disk."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return f"FILE NOT FOUND: {path}"


@function_tool
def list_directory(path: str) -> str:
    """List a directory."""
    try:
        return "\n".join(os.listdir(path))
    except Exception as exc:
        return f"ERROR: {exc}"


async def main() -> None:
    # 1. Define the agent (Codex-style)
    agent = Agent(
        name="CodexCoder",
        instructions=(
            "You are a code review assistant. You MUST call _arifos_prethink "
            "before any other tool. Never write code or modify files. "
            "Only observe and report."
        ),
        tools=[read_file, list_directory],
    )

    # 2. Wrap with the arifOS kernel
    kernel = ArifKernel(
        base_url="https://arifos.arif-fazil.com",
        actor_id="arif",
    )
    wrapped = kernel.wrap(agent)

    # 3. Run it — the agent will be forced to call _arifos_prethink first
    result = await Runner.run(
        wrapped,
        "Read the file /etc/hostname and tell me what it says.",
    )

    print(f"Final output: {result.final_output}")
    if hasattr(result, "_arifos_seal"):
        print(f"arifOS seal: {result._arifos_seal}")


if __name__ == "__main__":
    asyncio.run(main())
