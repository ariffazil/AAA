"""
arifOS Kernel Wiring — Tool Dispatch with Governance Pre-Filter.

Integrates governance enforcement (from kernel_abi) BEFORE OPA policy
evaluation in the tool dispatch pipeline.

Flow:
  1. Governance check (kernel_abi.evaluate_governance)
     → BLOCKED: deny immediately, write audit, return
     → REQUIRES_HOLD: write audit, return SABAR
     → APPROVED: proceed to step 2
  2. OPA policy evaluation (existing bridge.evaluate)
     → DENY / SABAR / PERMIT

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .abi.kernel_abi import (
    evaluate_governance,
    filter_tools_for_role,
    get_governance,
    capability_registry,
    _write_audit_event,
    _init_audit_chain,
)


@dataclass
class PolicyVerdict:
    """Unified verdict from governance + OPA evaluation."""

    recommendation: str  # DENY | SABAR | PERMIT
    reason: str
    override: bool = False
    governance: dict[str, Any] | None = None
    opa_verdict: str | None = None


async def evaluate_tool_dispatch(
    tool: str,
    actor_id: str,
    session_id: str | None = None,
    is_write_operation: bool = False,
    policy_path: str | None = None,
    opa_bridge: Any = None,
) -> PolicyVerdict:
    """Evaluate a tool dispatch through governance + OPA pipeline.

    Args:
        tool: Capability ID to evaluate (e.g. "memory.govern").
        actor_id: Invoking agent/role (e.g. "333-AGI").
        session_id: Session context (optional).
        is_write_operation: Whether this is a write/mutation.
        policy_path: OPA policy file path (optional).
        opa_bridge: OPA bridge instance for policy evaluation.

    Returns:
        PolicyVerdict with recommendation (DENY/SABAR/PERMIT).
    """
    # ── Step 1: Governance pre-filter ──
    gov_verdict = evaluate_governance(
        capability_id=tool,
        invoking_role=actor_id,
        is_write_operation=is_write_operation,
    )

    if gov_verdict["verdict"] == "BLOCKED":
        _write_audit_event(
            event="TOOL_CALL_BLOCKED",
            agent_id=actor_id,
            tool=tool,
            capability_id=tool,
            governance=gov_verdict["governance"],
            verdict="BLOCKED",
            reason=gov_verdict["reason"],
            session_id=session_id,
        )
        return PolicyVerdict(
            recommendation="DENY",
            reason=gov_verdict["reason"],
            governance=gov_verdict["governance"],
        )

    if gov_verdict["verdict"] == "REQUIRES_HOLD":
        _write_audit_event(
            event="TOOL_CALL_REQUIRES_HOLD",
            agent_id=actor_id,
            tool=tool,
            capability_id=tool,
            governance=gov_verdict["governance"],
            verdict="REQUIRES_HOLD",
            reason=gov_verdict["reason"],
            session_id=session_id,
        )
        return PolicyVerdict(
            recommendation="SABAR",
            reason=gov_verdict["reason"],
            governance=gov_verdict["governance"],
        )

    # ── Governance APPROVED → proceed to OPA ──
    _write_audit_event(
        event="TOOL_CALL_APPROVED",
        agent_id=actor_id,
        tool=tool,
        capability_id=tool,
        governance=gov_verdict["governance"],
        verdict="APPROVED",
        reason=gov_verdict["reason"],
        session_id=session_id,
    )

    # ── Step 2: OPA policy evaluation ──
    if opa_bridge is not None:
        try:
            inp = {
                "tool": tool,
                "actor_id": actor_id,
                "session_id": session_id,
                "is_write": is_write_operation,
            }
            opa_result = await opa_bridge.evaluate(
                policy_path or "default", inp
            )
            opa_verdict = getattr(opa_result, "recommendation", None) or str(opa_result)

            if opa_verdict in ("DENY", "REJECT"):
                return PolicyVerdict(
                    recommendation="DENY",
                    reason=f"OPA denied: {opa_verdict}",
                    governance=gov_verdict["governance"],
                    opa_verdict=opa_verdict,
                )
            if opa_verdict in ("HOLD", "SABAR"):
                return PolicyVerdict(
                    recommendation="SABAR",
                    reason=f"OPA hold: {opa_verdict}",
                    governance=gov_verdict["governance"],
                    opa_verdict=opa_verdict,
                )
            # PERMIT or similar → approved
            return PolicyVerdict(
                recommendation="PERMIT",
                reason="Governance + OPA approved.",
                governance=gov_verdict["governance"],
                opa_verdict=opa_verdict,
            )
        except Exception as e:
            return PolicyVerdict(
                recommendation="SABAR",
                reason=f"OPA evaluation failed: {e}",
                governance=gov_verdict["governance"],
                opa_verdict=f"ERROR: {e}",
            )

    # No OPA bridge → governance-only approval
    return PolicyVerdict(
        recommendation="PERMIT",
        reason="Governance approved (no OPA bridge configured).",
        governance=gov_verdict["governance"],
    )
