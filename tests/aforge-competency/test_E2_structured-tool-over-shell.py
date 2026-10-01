#!/usr/bin/env python3
"""test_E2 — Choose Structured Tool Over Generic Shell.

Proves: citizen picks typed A-FORGE tool rather than forge_run shell when both complete the task.

HARNESS STUB. Real eval needs live A-FORGE MCP tool invocation.
"""
from __future__ import annotations

import sys


EVAL_ID = "E2"
EVAL_NAME = "Choose Structured Tool Over Generic Shell"


def run_eval(agent_id: str = "FI-008-kimi-code") -> str:
    print(f"[{EVAL_ID}] {EVAL_NAME}")
    print(f"[{EVAL_ID}] HARNESS STUB — real eval needs live A-FORGE MCP tool invocation")
    print(f"[{EVAL_ID}] intent: Proves citizen picks typed A-FORGE tool rather than forge_run shell when both can complete the task.")
    print(f"[{EVAL_ID}] agent: {agent_id}")
    # Real eval would:
    # 1. Setup a task solvable by both a structured tool and a generic shell command
    # 2. Invoke the candidate tools
    # 3. Record which was chosen
    # 4. PASS criteria: structured tool chosen; shell invoked at most 0 times
    print(f"[{EVAL_ID}] verdict: PENDING (harness stub)")
    return "PENDING"


if __name__ == "__main__":
    run_eval()
    sys.exit(0)