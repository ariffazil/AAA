"""ConstitutionalExecutor — AAA's heart.

Implements a2a-sdk's AgentExecutor interface.
Every A2A request passes through constitutional governance:

  identity → floors → delegation guard
  → ART (admission) → FQ (metabolism) → ACT (execution readiness)
  → organ dispatch → audit receipt → flow_ingest

The Gate Runtime (ART/FQ/ACT) wraps the Wisdom Runtime (333/555/888).
Three gates, three scales:
  ART  = Call Scale     — "May this call enter?"
  FQ   = System Scale   — "Is the federation healthy enough to act?"
  ACT  = Mutation Scale — "May reality now change?"

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import logging
from typing import Any

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    Message,
    Part,
    Role,
    Task,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    TextPart,
)

from aaa_a2a.middleware.audit import AuditRecord, write_receipt
from aaa_a2a.middleware.floors import check_all_floors
from aaa_a2a.middleware.identity import resolve_identity
from aaa_a2a.middleware.verdicts import verdict_to_a2a_state, verdict_requires_human
from aaa_a2a.guard import check_delegation
from aaa_a2a.models import Verdict
from aaa_a2a.gate import (
    GateVerdict,
    run_gate_chain,
    ingest_flow,
)
from .routing.organ_router import route_intent, call_mcp_tool, ORGANS

logger = logging.getLogger("aaa.constitutional")


def _extract_text(message: Message | None) -> str:
    """Extract text from A2A message parts."""
    if not message or not message.parts:
        return ""
    texts = []
    for part in message.parts:
        if isinstance(part.root, TextPart):
            texts.append(part.root.text)
    return " ".join(texts)


def _extract_session_token(context: RequestContext) -> str | None:
    """Extract session_token (ACT/SCT) from request context metadata."""
    if not context.metadata:
        return None
    # Check common keys
    for key in ("session_token", "act", "sct", "sessionToken"):
        token = context.metadata.get(key)
        if token:
            return str(token)
    return None


class ConstitutionalExecutor(AgentExecutor):
    """AAA's constitutional overlay on A2A transport.

    Pipeline (2026-08-08 — ART/AUTH/ACT wired):
    1.  Identity resolution  — who is calling?
    2.  Floor check          — F1-F13 gate
    3.  Delegation guard     — cross-organ boundary
    4.  Gate chain runtime:
        a. FQ Gate            — federation metabolism healthy?
        b. ART Gate           — may this call enter?
        c. ACT Gate           — may reality change?
    5.  Organ dispatch       — route to correct MCP server
    6.  Audit receipt        — VAULT999 chain
    7.  arifFLOW ingest      — metabolic ledger
    """

    def __init__(self, arifos_url: str = "http://localhost:8088"):
        self.arifos_url = arifos_url

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute an A2A request through constitutional governance."""
        message = context.message
        task_id = context.task_id
        text = _extract_text(message)

        # ── Extract session token ──────────────────────────────────────
        session_token = _extract_session_token(context)

        # ── 1. Identity resolution ─────────────────────────────────────
        agent_id = context.metadata.get("agent_id") if context.metadata else None
        identity = resolve_identity(agent_id=agent_id)
        logger.info(
            f"[AAA] Task {task_id} from {identity.agent_id}"
            f" (authority: {identity.authority_band.value})"
            f" {'[SCT]' if session_token else '[NO-SCT]'}"
        )

        # ── 2. Floor check (F1-F13) ────────────────────────────────────
        floor_result = check_all_floors(text)
        if not floor_result.passed:
            verdict = floor_result.verdict
            logger.warning(f"[AAA] Task {task_id} FLOOR VIOLATION: {floor_result.rationale}")

            write_receipt(
                AuditRecord(
                    event="floor_violation",
                    agent_id=identity.agent_id,
                    task_id=task_id,
                    verdict=verdict,
                    floors_checked=floor_result.floors_checked,
                    floors_violated=floor_result.floors_violated,
                    evidence={"rationale": floor_result.rationale},
                )
            )

            event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    task_id=task_id,
                    context_id=context.context_id,
                    status=TaskStatus(
                        state=TaskState(verdict_to_a2a_state(verdict)),
                        message=Message(
                            role=Role.agent,
                            parts=[
                                Part(
                                    root=TextPart(
                                        text=f"[AAA] Constitutional floor violation: {floor_result.rationale}"
                                    )
                                )
                            ],
                            message_id=f"aaa-{task_id}",
                            task_id=task_id,
                            context_id=context.context_id,
                        ),
                    ),
                    final=True,
                )
            )
            return

        # ── 3. Delegation guard ────────────────────────────────────────
        target_organ = route_intent(text)
        delegation = check_delegation(
            source_agent=identity.agent_id,
            target_skill=target_organ,
            message_text=text,
        )
        if delegation.blocked:
            logger.warning(f"[AAA] Task {task_id} DELEGATION BLOCKED: {delegation.reason}")

            write_receipt(
                AuditRecord(
                    event="delegation_blocked",
                    agent_id=identity.agent_id,
                    task_id=task_id,
                    verdict=Verdict.VOID,
                    evidence={"reason": delegation.reason, "floor": delegation.floor},
                )
            )

            event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    task_id=task_id,
                    context_id=context.context_id,
                    status=TaskStatus(
                        state=TaskState.TASK_STATE_REJECTED,
                        message=Message(
                            role=Role.agent,
                            parts=[
                                Part(
                                    root=TextPart(
                                        text=f"[AAA] Delegation blocked: {delegation.reason}"
                                    )
                                )
                            ],
                            message_id=f"aaa-{task_id}",
                            task_id=task_id,
                            context_id=context.context_id,
                        ),
                    ),
                    final=True,
                )
            )
            return

        # ── 4. Gate Chain Runtime — ART → FQ → ACT ────────────────────
        tool_name = _detect_tool(text, target_organ)
        gate_chain = await run_gate_chain(
            intent_text=text,
            agent_id=identity.agent_id,
            target_organ=target_organ,
            session_token=session_token,
            tool_name=tool_name,
        )

        if gate_chain.blocked:
            logger.warning(
                f"[AAA] Task {task_id} GATE BLOCKED at {gate_chain.blocked_by}:"
                f" verdict={gate_chain.final_verdict.value}"
            )

            blocked_reason = ""
            if gate_chain.blocked_by == "FQ" and gate_chain.fq:
                blocked_reason = gate_chain.fq.reason
            elif gate_chain.blocked_by == "ART" and gate_chain.art:
                blocked_reason = gate_chain.art.reason
            elif gate_chain.blocked_by == "ACT" and gate_chain.act:
                blocked_reason = gate_chain.act.reason

            write_receipt(
                AuditRecord(
                    event=f"gate_blocked_{gate_chain.blocked_by.lower()}",
                    agent_id=identity.agent_id,
                    task_id=task_id,
                    verdict=Verdict.HOLD,
                    evidence={
                        "gate": gate_chain.blocked_by,
                        "verdict": gate_chain.final_verdict.value,
                        "reason": blocked_reason,
                    },
                )
            )

            event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    task_id=task_id,
                    context_id=context.context_id,
                    status=TaskStatus(
                        state=TaskState.TASK_STATE_REJECTED,
                        message=Message(
                            role=Role.agent,
                            parts=[
                                Part(
                                    root=TextPart(
                                        text=f"[AAA] Gate {gate_chain.blocked_by} HOLD: {blocked_reason}"
                                    )
                                )
                            ],
                            message_id=f"aaa-{task_id}",
                            task_id=task_id,
                            context_id=context.context_id,
                        ),
                    ),
                    final=True,
                )
            )
            return

        # ── 5. Emit working status ─────────────────────────────────────
        gate_summary = ""
        if gate_chain.fq and gate_chain.fq.verdict == GateVerdict.SABAR:
            gate_summary = f" [FQ:SABAR]"
        event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context.context_id,
                status=TaskStatus(
                    state=TaskState.TASK_STATE_WORKING,
                    message=Message(
                        role=Role.agent,
                        parts=[
                            Part(
                                root=TextPart(
                                    text=f"[AAA] Routing to {target_organ}"
                                    f" ({ORGANS[target_organ]['domain']}){gate_summary}..."
                                )
                            )
                        ],
                        message_id=f"aaa-{task_id}",
                        task_id=task_id,
                        context_id=context.context_id,
                    ),
                ),
                final=False,
            )
        )

        # ── 6. Organ dispatch — with session_token forwarding ──────────
        target_info = ORGANS.get(target_organ, {})
        if target_info.get("domain") == "cognition":
            tool_name = "hermes_system_status"
            arguments: dict[str, Any] = {"query": text, "session_id": task_id}
            if session_token:
                arguments["session_token"] = session_token
            result = await call_mcp_tool(
                organ_id=target_organ,
                tool_name=tool_name,
                arguments=arguments,
                session_token=session_token,
            )
        else:
            if tool_name in ("arif_init", "arif_seal"):
                arguments = {
                    "actor_id": identity.agent_id,
                    "intent": text[:200],
                    "session_id": task_id,
                }
                if tool_name == "arif_init":
                    arguments["mode"] = "light"
                else:
                    arguments["mode"] = "seal"
                    arguments["content"] = text[:500]
                if session_token:
                    arguments["session_token"] = session_token
            else:
                arguments = {"query": text, "session_id": task_id}
                if session_token:
                    arguments["session_token"] = session_token

            result = await call_mcp_tool(
                organ_id=target_organ,
                tool_name=tool_name,
                arguments=arguments,
                session_token=session_token,
            )

        # ── 7. Build response ──────────────────────────────────────────
        if result.get("ok"):
            response_text = f"[AAA→{target_organ}] {result.get('result', 'OK')}"
            final_state = TaskState.TASK_STATE_COMPLETED
            verdict = Verdict.SEAL
            flow_step = "Execute"
            flow_verdict = "Pass"
        else:
            response_text = f"[AAA→{target_organ}] Error: {result.get('error', 'unknown')}"
            final_state = TaskState.TASK_STATE_FAILED
            verdict = Verdict.HOLD
            flow_step = "Execute"
            flow_verdict = "Caution"

        # ── 8. Audit receipt ───────────────────────────────────────────
        write_receipt(
            AuditRecord(
                event="task_completed",
                agent_id=identity.agent_id,
                task_id=task_id,
                verdict=verdict,
                floors_checked=floor_result.floors_checked,
                evidence={
                    "organ": target_organ,
                    "tool": tool_name,
                    "ok": result.get("ok"),
                    "gate_fq": gate_chain.fq.details if gate_chain.fq else {},
                    "gate_art": gate_chain.art.details if gate_chain.art else {},
                    "gate_act": gate_chain.act.details if gate_chain.act else {},
                },
            )
        )

        # ── 9. arifFLOW ingest — metabolic ledger ──────────────────────
        await ingest_flow(
            actor_id=identity.agent_id,
            session_id=task_id,
            step_type=flow_step,
            epistemic_label="Observation" if result.get("ok") else "Derivation",
            floor_verdict=flow_verdict,
            payload={
                "organ": target_organ,
                "tool": tool_name,
                "ok": result.get("ok"),
            },
        )

        # ── 10. Emit final status ──────────────────────────────────────
        event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context.context_id,
                status=TaskStatus(
                    state=final_state,
                    message=Message(
                        role=Role.agent,
                        parts=[Part(root=TextPart(text=response_text))],
                        message_id=f"aaa-{task_id}",
                        task_id=task_id,
                        context_id=context.context_id,
                    ),
                ),
                final=True,
            )
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel a task — write audit receipt + flow ingest."""
        task_id = context.task_id
        write_receipt(
            AuditRecord(
                event="task_cancelled",
                agent_id="system",
                task_id=task_id,
                verdict=Verdict.HOLD,
            )
        )
        await ingest_flow(
            actor_id="system",
            session_id=task_id,
            step_type="Cool",
            epistemic_label="Derivation",
            floor_verdict="Hold",
        )
        event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context.context_id,
                status=TaskStatus(state=TaskState.TASK_STATE_CANCELED),
                final=True,
            )
        )


def _detect_tool(text: str, organ: str) -> str:
    """Simple heuristic to detect MCP tool from text."""
    lower = text.lower()
    if lower.startswith("init ") or lower.startswith("agent-init"):
        return "arif_init"
    if lower.startswith("seal ") or lower.startswith("agent-seal"):
        return "arif_seal"
    if organ == "geox":
        if "seismic" in lower:
            return "geox_seismic_compute"
        if "basin" in lower:
            return "geox_basin"
        if "petro" in lower:
            return "geox_petrophysics"
        return "geox_evidence"
    if organ == "wealth":
        if "npv" in lower:
            return "wealth_compute_npv"
        if "stock" in lower:
            return "wealth_stock_analysis"
        if "emv" in lower:
            return "wealth_compute_emv"
        return "wealth_omni_wisdom"
    if organ == "well":
        if "sleep" in lower or "fatigue" in lower:
            return "well_assess_homeostasis"
        if "vitality" in lower or "readiness" in lower:
            return "well_validate_vitality"
        return "well_readiness"
    if organ == "aforge":
        return "forge_execute"
    return "arif_think"
