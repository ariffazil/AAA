"""Constitutional middleware for A2A request handling.

Each module in this package is a single constitutional concern. They compose
on top of the official a2a-sdk transport and run on every A2A task.

Layers (in execution order):
    1. floors        — F1-F13 gate before the task is allowed to execute.
    2. identity      — verify the calling actor is who they claim to be.
    3. verdicts      — typed result: SEAL | HOLD | SABAR | VOID.
    4. audit         — append the outcome to VAULT999 hash-chained ledger.
"""

from aaa_a2a.middleware.floors import check_all_floors
from aaa_a2a.middleware.identity import resolve_identity, register_agent
from aaa_a2a.middleware.verdicts import (
    verdict_to_a2a_state,
    verdict_requires_human,
    verdict_is_terminal,
)
from aaa_a2a.middleware.audit import write_receipt, verify_chain, get_chain

__all__ = [
    "check_all_floors",
    "resolve_identity",
    "register_agent",
    "verdict_to_a2a_state",
    "verdict_requires_human",
    "verdict_is_terminal",
    "write_receipt",
    "verify_chain",
    "get_chain",
]
