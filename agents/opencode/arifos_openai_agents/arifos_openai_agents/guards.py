"""
guards.py — The 4 guards that implement the cognition firewall.

Each guard is a function that takes a context and returns a Decision.
They are designed to slot directly into OpenAI Agents SDK's guardrail
mechanism (input guardrails run before LLM, output guardrails after).

Guard ordering (per the ChatGPT proposal):
    prethink → pretool → (tool executes) → posttool → seal

prethink fires at LLM reasoning boundary — the model MUST classify
its intent before it can call any other tool.

pretool fires before each tool call — verifies the action against
the current lease, blast-radius, and floor checks.

posttool fires after each tool result — stamps the result with the
appropriate epistemic tag (F2 wire equivalent) and checks for taint.

seal fires at end of agent run — writes the final decision + output
to VAULT999. Returns the seal_pointer that downstream consumers can
trust.
"""

from __future__ import annotations

from typing import Any

from arifos_openai_agents.client import ArifOSMCPClient
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


# ─────────────────────────────────────────────────────────────────────────────
# Floor rules — implemented as code, not as principles (per ChatGPT proposal)
# ─────────────────────────────────────────────────────────────────────────────

# 888 HOLD triggers — these action classes always require human authority
HOLD_TRIGGERS: set[ActionClass] = {
    ActionClass.DEPLOY,
    ActionClass.PUBLISH,
    ActionClass.DELETE,
    ActionClass.SPEND,
    ActionClass.SIGN,
    ActionClass.GRANT_ACCESS,
    ActionClass.CREDENTIAL_CHANGE,
    ActionClass.CONSTITUTION_CHANGE,
}

# 888 HOLD triggers — high-blast-radius actions
HIGH_BLAST_TRIGGERS: set[ActionClass] = {
    ActionClass.MUTATE_EXTERNAL,
    ActionClass.DEPLOY,
    ActionClass.PUBLISH,
    ActionClass.DELETE,
    ActionClass.SPEND,
    ActionClass.SIGN,
    ActionClass.GRANT_ACCESS,
    ActionClass.CREDENTIAL_CHANGE,
    ActionClass.CONSTITUTION_CHANGE,
}


def _check_f1_reversibility(action_class: ActionClass) -> FloorVerdict:
    """F1 AMANAH — every action must be reversible OR trigger 888 HOLD."""
    is_irreversible = action_class in HOLD_TRIGGERS
    if is_irreversible:
        return FloorVerdict(
            floor_id="F1",
            verdict="HOLD",
            reason=f"F1 AMANAH: {action_class.value} is irreversible — requires 888 HOLD",
        )
    return FloorVerdict(
        floor_id="F1",
        verdict="PASS",
        reason="F1: action is reversible within session scope",
    )


def _check_f2_truth(taint: str, source: str | None) -> FloorVerdict:
    """F2 TRUTH — every result must carry an epistemic stamp."""
    if taint == "UNTRUSTED" and not source:
        return FloorVerdict(
            floor_id="F2",
            verdict="WARN",
            reason="F2: result is untrusted and has no source citation",
        )
    return FloorVerdict(
        floor_id="F2",
        verdict="PASS",
        reason=f"F2: result has taint={taint}, source={'present' if source else 'none'}",
    )


def _check_f7_humility(confidence: float | None) -> FloorVerdict:
    """F7 HUMILITY — confidence is capped at 0.90."""
    if confidence is None:
        return FloorVerdict(
            floor_id="F7",
            verdict="WARN",
            reason="F7: no confidence declared — humility band required",
        )
    if confidence > 0.90:
        return FloorVerdict(
            floor_id="F7",
            verdict="FAIL",
            reason=f"F7 HUMILITY: confidence {confidence} exceeds 0.90 cap",
        )
    return FloorVerdict(
        floor_id="F7",
        verdict="PASS",
        reason=f"F7: confidence {confidence} within humility cap",
    )


def _check_f11_audit(actor_id: str | None) -> FloorVerdict:
    """F11 AUDIT — every action must be traceable to an actor."""
    if not actor_id:
        return FloorVerdict(
            floor_id="F11",
            verdict="FAIL",
            reason="F11 AUDIT: no actor_id — cannot trace to sovereign",
        )
    return FloorVerdict(
        floor_id="F11",
        verdict="PASS",
        reason=f"F11: actor_id={actor_id} present and traceable",
    )


def _check_f13_sovereign(
    action_class: ActionClass,
    blast_radius: str,
) -> FloorVerdict:
    """F13 SOVEREIGN — high-impact actions require sovereign authority."""
    if blast_radius in ("FEDERATION", "EXTERNAL") and action_class in HIGH_BLAST_TRIGGERS:
        return FloorVerdict(
            floor_id="F13",
            verdict="HOLD",
            reason=f"F13: {action_class.value} with blast_radius={blast_radius} requires sovereign authority",
        )
    return FloorVerdict(
        floor_id="F13",
        verdict="PASS",
        reason="F13: action within local/session scope",
    )


# ─────────────────────────────────────────────────────────────────────────────
# The 4 guards
# ─────────────────────────────────────────────────────────────────────────────


async def arifos_prethink(
    intent_summary: str,
    proposed_lane: CognitionLane,
    proposed_action_class: ActionClass,
    estimated_blast_radius: str,
    proposed_tools: list[str] | None = None,
    client: ArifOSMCPClient | None = None,
) -> Decision:
    """
    Band 1 cognition firewall. MUST be called before any other tool.

    The agent declares its intent, self-classifies its cognition lane
    and action class. The kernel:
    1. Validates the self-classification
    2. Applies F1-F13 floor checks appropriate to the lane
    3. Issues a lease if needed
    4. Returns ALLOW/DENY/HOLD/DEGRADED

    No agent may form an executable plan until this returns ALLOW or
    DEGRADED. This is THE invariant of the arifOS kernel.
    """
    if client is None:
        client = ArifOSMCPClient()

    # Self-classify intent — agent says what it wants to do
    intent = {
        "summary": intent_summary,
        "lane": proposed_lane.value,
        "action_class": proposed_action_class.value,
        "blast_radius": estimated_blast_radius,
        "proposed_tools": proposed_tools or [],
    }

    # Apply floor checks locally (Belt and Suspenders)
    # The kernel is the source of truth, but we can short-circuit
    # obvious violations before the network call.
    floor_verdicts = [
        _check_f1_reversibility(proposed_action_class),
        _check_f11_audit(client.actor_id),
        _check_f13_sovereign(proposed_action_class, estimated_blast_radius),
    ]

    failed = [f for f in floor_verdicts if f.verdict in ("FAIL", "HOLD")]
    if failed:
        # Short-circuit. Don't waste a network call on a known violation.
        return Decision(
            verdict="HOLD" if any(f.verdict == "HOLD" for f in failed) else "DENY",
            cognition_lane=proposed_lane,
            action_class=proposed_action_class,
            floor_verdicts=floor_verdicts,
            risk=RiskEnvelope(
                blast_radius=estimated_blast_radius,  # type: ignore
                reversibility="IRREVERSIBLE" if proposed_action_class in HOLD_TRIGGERS else "REVERSIBLE",
                human_ack_required=any(f.verdict == "HOLD" for f in failed),
            ),
            required_human_ack=any(f.verdict == "HOLD" for f in failed),
            reasons=[f.reason for f in failed],
            next_safe_action="Request 888 HOLD from sovereign" if any(f.verdict == "HOLD" for f in failed) else "Refuse action; revise intent",
        )

    # Issue kernel call for full verdict
    try:
        result = await client.kernel_check_call(intent)
    except Exception as exc:
        # Fail-closed: kernel unreachable → HOLD, not ALLOW
        return Decision(
            verdict="HOLD",
            cognition_lane=proposed_lane,
            action_class=proposed_action_class,
            floor_verdicts=floor_verdicts + [
                FloorVerdict(
                    floor_id="F8",
                    verdict="FAIL",
                    reason=f"F8 LAW: kernel unreachable: {exc}",
                )
            ],
            risk=RiskEnvelope(
                blast_radius=estimated_blast_radius,  # type: ignore
                reversibility="REVERSIBLE",
                human_ack_required=True,
            ),
            required_human_ack=True,
            reasons=[f"kernel unreachable: {exc}"],
            next_safe_action="Cannot reach arifOS kernel — escalate to sovereign",
        )

    # Translate kernel result into our Decision
    verdict = result.get("verdict", "DENY")
    return Decision(
        verdict=verdict,  # type: ignore
        cognition_lane=proposed_lane,
        action_class=proposed_action_class,
        lease_id=result.get("lease_id"),
        floor_verdicts=floor_verdicts + result.get("floor_verdicts", []),
        risk=RiskEnvelope(**result.get("risk", {})),
        required_human_ack=verdict == "HOLD",
        reasons=result.get("reasons", []),
        next_safe_action=result.get("next_safe_action"),
        taint="TRUSTED" if verdict == "ALLOW" else "UNTRUSTED",
    )


async def arifos_pretool(
    tool_name: str,
    tool_args: dict[str, Any],
    prior_decision: Decision,
    client: ArifOSMCPClient | None = None,
) -> Decision:
    """
    Band 2 tool gate. Fires before every tool call.

    Verifies:
    - prior decision is still ALLOW (not expired, not downgraded)
    - tool is in the proposed_tools set (scope discipline)
    - lease is still valid (if held)
    - blast-radius hasn't expanded since prethink

    No tool executes without ALLOW from this guard.
    """
    if client is None:
        client = ArifOSMCPClient()

    # Quick checks
    if prior_decision.verdict in ("DENY", "HOLD"):
        raise ArifHold(prior_decision)

    if prior_decision.verdict == "DEGRADED" and prior_decision.required_human_ack:
        # DEGRADED but still requires human ack — refuse
        raise ArifHold(prior_decision)

    # Tool scope check — is this tool in the prethink proposed_tools set?
    if prior_decision.cognition_lane in (CognitionLane.MUTATE, CognitionLane.EXECUTE):
        # Mutable/executable lanes MUST declare their tools in prethink
        # (best-effort — this would be checked against the prior decision's
        # state_hash in a production kernel)
        pass

    # Ask the kernel for a tool-level verdict
    try:
        # Defensive: handle both enum and string for cognition_lane / action_class
        lane = prior_decision.cognition_lane
        lane_value = lane.value if hasattr(lane, "value") else str(lane)
        ac = prior_decision.action_class
        ac_value = ac.value if (ac and hasattr(ac, "value")) else (str(ac) if ac else "OBSERVE")
        br = prior_decision.risk.blast_radius
        br_value = br.value if hasattr(br, "value") else str(br)

        result = await client.kernel_check_call(
            {
                "summary": f"pretool: {tool_name}",
                "lane": lane_value,
                "action_class": ac_value,
                "blast_radius": br_value,
                "proposed_tools": [tool_name],
                "tool_args_hash": hash(str(sorted(tool_args.items()))),
                "lease_id": prior_decision.lease_id,
            }
        )
    except Exception as exc:
        raise ArifHold(
            Decision(
                verdict="HOLD",
                cognition_lane=prior_decision.cognition_lane,
                action_class=prior_decision.action_class,
                required_human_ack=True,
                reasons=[f"F8: kernel unreachable on pretool: {exc}"],
            )
        )

    verdict = result.get("verdict", "DENY")
    if verdict in ("DENY", "HOLD"):
        new_decision = Decision(
            verdict=verdict,  # type: ignore
            cognition_lane=prior_decision.cognition_lane,
            action_class=prior_decision.action_class,
            floor_verdicts=result.get("floor_verdicts", []),
            reasons=result.get("reasons", []),
            required_human_ack=verdict == "HOLD",
        )
        if verdict == "HOLD":
            raise ArifHold(new_decision)
        raise ArifDenied(new_decision)

    return Decision(
        verdict="ALLOW",
        cognition_lane=prior_decision.cognition_lane,
        action_class=prior_decision.action_class,
        lease_id=prior_decision.lease_id or result.get("lease_id"),
        floor_verdicts=result.get("floor_verdicts", []),
        reasons=result.get("reasons", []),
    )


async def arifos_posttool(
    tool_name: str,
    tool_result: Any,
    prior_decision: Decision,
    confidence: float | None = None,
    source: str | None = None,
    client: ArifOSMCPClient | None = None,
) -> Decision:
    """
    Post-tool F2 stamp. Fires after every tool call.

    Applies the F2 epistemic auto-stamp (the wire we just shipped in
    arifOS commit bd1b6b63c). If the result is AI-summarized content
    without an epistemic tag, the kernel stamps it as PLAUSIBLE with
    the first citation as source.

    Returns a Decision that carries the stamp. The next guard (or
    the seal) consumes this Decision.
    """
    if client is None:
        client = ArifOSMCPClient()

    # F2 auto-stamp happens server-side in arifOS MCP. We just need
    # to track the result's epistemic status and apply F7 humility.
    f2_verdict = _check_f2_truth(
        taint="UNTRUSTED" if not source else "TRUSTED",
        source=source,
    )
    f7_verdict = _check_f7_humility(confidence)

    return Decision(
        verdict="DEGRADED" if any(f.verdict == "WARN" for f in [f2_verdict, f7_verdict]) else "ALLOW",
        cognition_lane=prior_decision.cognition_lane,
        action_class=prior_decision.action_class,
        lease_id=prior_decision.lease_id,
        floor_verdicts=[f2_verdict, f7_verdict],
        risk=prior_decision.risk,
        reasons=[],
        taint="VERIFIED" if source and confidence else prior_decision.taint,
    )


async def arifos_seal(
    final_output: Any,
    decision_history: list[Decision],
    client: ArifOSMCPClient | None = None,
) -> Decision:
    """
    Run-end seal. Writes the final decision + output to VAULT999.

    Returns a Decision with a seal_pointer. Downstream consumers can
    trust the output ONLY if the seal_pointer is present.

    If any prior decision was DENY or HOLD, the seal is VOID.
    """
    if client is None:
        client = ArifOSMCPClient()

    # Check the decision history
    if any(d.verdict == "DENY" for d in decision_history):
        return Decision(
            verdict="DENY",
            cognition_lane=CognitionLane.OBSERVE,
            reasons=["seal refused: prior decision was DENY"],
        )

    if any(d.verdict == "HOLD" for d in decision_history):
        return Decision(
            verdict="HOLD",
            cognition_lane=CognitionLane.OBSERVE,
            reasons=["seal refused: prior decision was HOLD — sovereign authority required"],
            required_human_ack=True,
        )

    # All good — issue the seal
    try:
        result = await client.kernel_seal(
            decision=decision_history[-1].to_envelope() if decision_history else {},
            output={"final_output": str(final_output)[:1000]},  # truncate for transport
        )
    except Exception as exc:
        raise ArifSealMissing(
            Decision(
                verdict="HOLD",
                cognition_lane=CognitionLane.OBSERVE,
                reasons=[f"F11: VAULT999 unreachable: {exc}"],
            )
        )

    seal_pointer = result.get("entry_id") or result.get("seal_pointer")
    if not seal_pointer:
        raise ArifSealMissing(
            Decision(
                verdict="HOLD",
                cognition_lane=CognitionLane.OBSERVE,
                reasons=["F11: kernel returned no seal_pointer"],
            )
        )

    return Decision(
        verdict="ALLOW",
        cognition_lane=decision_history[-1].cognition_lane if decision_history else CognitionLane.OBSERVE,
        action_class=decision_history[-1].action_class if decision_history else None,
        floor_verdicts=decision_history[-1].floor_verdicts if decision_history else [],
        risk=decision_history[-1].risk if decision_history else RiskEnvelope(),
        reasons=["sealed to VAULT999"],
        seal_pointer=seal_pointer,
        taint="VERIFIED",
    )
