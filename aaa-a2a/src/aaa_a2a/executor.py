"""ConstitutionalExecutor — AAA's heart.

Implements a2a-sdk's AgentExecutor interface.
Every A2A request passes through constitutional governance:
  identity → floors → delegation guard → verdict → organ dispatch → audit

This is the 200 lines that replace 3,862 lines of Express.

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


class ConstitutionalExecutor(AgentExecutor):
    """AAA's constitutional overlay on A2A transport.

    Every request goes through:
    1. Identity resolution — who is calling?
    2. Floor check — F1-F13 gate
    3. Delegation guard — cross-organ boundary
    4. Verdict routing — SEAL/HOLD/SABAR/VOID
    5. Organ dispatch — route to correct MCP server
    6. Audit receipt — VAULT999 chain
    """

    def __init__(self, arifos_url: str = "http://localhost:8088"):
        self.arifos_url = arifos_url

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute an A2A request through constitutional governance."""
        message = context.message
        task_id = context.task_id
        text = _extract_text(message)

        # 1. Identity resolution
        agent_id = context.metadata.get("agent_id") if context.metadata else None
        identity = resolve_identity(agent_id=agent_id)
        logger.info(
            f"[AAA] Task {task_id} from {identity.agent_id} (authority: {identity.authority_band.value})"
        )

        # 2. Floor check (F1-F13)
        floor_result = check_all_floors(text)
        if not floor_result.passed:
            verdict = floor_result.verdict
            logger.warning(f"[AAA] Task {task_id} FLOOR VIOLATION: {floor_result.rationale}")

            # Write audit receipt
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

            # Emit status update
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

        # 3. Delegation guard
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

        # 4. Emit working status
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
                                    text=f"[AAA] Routing to {target_organ} ({ORGANS[target_organ]['domain']})..."
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

        # 5. Organ dispatch — route to MCP server
        # Extract tool name from text (simple heuristic)
        tool_name = _detect_tool(text, target_organ)
        result = await call_mcp_tool(
            organ_id=target_organ,
            tool_name=tool_name,
            arguments={"query": text, "session_id": task_id},
        )

        # 6. Build response
        if result.get("ok"):
            response_text = f"[AAA→{target_organ}] {result.get('result', 'OK')}"
            final_state = TaskState.TASK_STATE_COMPLETED
            verdict = Verdict.SEAL
        else:
            response_text = f"[AAA→{target_organ}] Error: {result.get('error', 'unknown')}"
            final_state = TaskState.TASK_STATE_FAILED
            verdict = Verdict.HOLD

        # 7. Audit receipt
        write_receipt(
            AuditRecord(
                event="task_completed",
                agent_id=identity.agent_id,
                task_id=task_id,
                verdict=verdict,
                floors_checked=floor_result.floors_checked,
                evidence={"organ": target_organ, "tool": tool_name, "ok": result.get("ok")},
            )
        )

        # 8. Emit final status
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
        """Cancel a task — write audit receipt."""
        task_id = context.task_id
        write_receipt(
            AuditRecord(
                event="task_cancelled",
                agent_id="system",
                task_id=task_id,
                verdict=Verdict.HOLD,
            )
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
