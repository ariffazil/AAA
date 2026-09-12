#!/usr/bin/env python3
"""
OpenClaw AGI Orchestrator v1.0.0

The brain that ties everything together:
  - Receives inbound messages from any channel
  - Classifies intent (regex → semantic fallback)
  - Manages cross-session state per person
  - Executes workflows (DAG engine) for complex tasks
  - Tracks observability (traces, tokens, FQ)
  - Routes to federation organs via A2A
  - Returns formatted responses to the originating channel

Architecture:
  Channel → Orchestrator → [Semantic Router | DAG Engine | State Manager]
         → A2A Bridge → Federation Organs
         ← Response ← Channel

This is the AGI-level upgrade to OpenClaw's deterministic intent router.

Forged: 2026-09-12 by 333-AGI under F13 directive
DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import json
import os
import time
import uuid
import urllib.request
import urllib.error
from typing import Any, Optional
from dataclasses import dataclass, field, asdict

from .semantic_router import (
    SemanticRouter,
    SemanticResult,
    classify_intent,
    classify_multi_intents,
    CONFIDENCE_THRESHOLD,
    get_semantic_router,
)
from .dag_engine import (
    DAGEngine,
    FlowDef,
    TaskDef,
    define_workflow,
    execute_workflow,
    create_from_template,
    get_dag_engine,
    TEMPLATES,
)
from .state_manager import (
    StateManager,
    PersonState,
    get_state_manager,
    get_person_state,
    add_conversation_turn,
)
from .observability import (
    ObservabilityLayer,
    get_observability,
)
from .channel_manager import (
    ChannelManager,
    ChannelType,
    InboundMessage,
    OutboundMessage,
    ResponseFormatter,
    get_channel_manager,
)
from ..a2a_bridge import resolve_target, build_task, emit, ROUTER_TO_AGENT


# ─── Constants ───────────────────────────────────────────────────────────
AAA_A2A_URL = "http://127.0.0.1:3001/a2a"
FORGE_HEALTH_URL = "http://127.0.0.1:7071/health"
ARIFLOW_HEALTH_URL = "http://127.0.0.1:7073/health"

# Multi-intent thresholds
MULTI_INTENT_CONFIDENCE_THRESHOLD = 0.65
FAN_OUT_THRESHOLD = 3  # 3+ intents → use forge_parallel


@dataclass
class OrchestratorResult:
    """Result from the orchestrator processing a message."""

    trace_id: str
    person_id: str
    rule_id: str
    target_agent: str
    confidence: float
    source: str  # regex | semantic | dag | fallback
    is_multi_intent: bool
    sub_intents: list[dict] = field(default_factory=list)
    workflow_id: str = ""
    response: str = ""
    latency_ms: int = 0
    token_budget: dict = field(default_factory=dict)
    fq_advice: dict = field(default_factory=dict)
    error: str = ""


class Orchestrator:
    """
    AGI-level orchestrator for OpenClaw.

    Flow:
    1. Receive inbound message
    2. Load person state (cross-session memory)
    3. Check FQ (metabolism gate)
    4. Check token budget
    5. Classify intent (regex → semantic fallback)
    6. If multi-intent → fan-out via DAG or forge_parallel
    7. Route to federation organ via A2A
    8. Track observability
    9. Return formatted response
    """

    def __init__(self):
        self.semantic = get_semantic_router()
        self.dag = get_dag_engine()
        self.state = get_state_manager()
        self.obs = get_observability()
        self.channels = get_channel_manager()
        self.formatter = ResponseFormatter()

    # ─── Main Processing Loop ────────────────────────────────────────

    def process(
        self,
        message: InboundMessage,
        *,
        regex_result: dict | None = None,
        dry_run: bool = False,
    ) -> OrchestratorResult:
        """
        Process an inbound message through the full orchestrator pipeline.

        Args:
            message: Normalized inbound message
            regex_result: Result from deterministic regex router (if available)
            dry_run: If true, show routing decision without executing
        """
        start_ms = int(time.time() * 1000)

        # 1. Start trace
        trace_id, root_span = self.obs.start_trace(
            "orchestrator_process",
            agent="openclaw",
            attributes={"person_id": message.person_id, "channel": message.channel.value},
        )

        try:
            # 2. Load person state
            person = self.state.get_state(message.person_id)
            self.state.add_turn(
                message.person_id,
                "user",
                message.content,
                channel=message.channel.value,
            )

            # 3. Check FQ
            fq_advice = self.obs.get_fq_advice()

            # 4. Check token budget
            budget = self.obs.get_budget(message.person_id)
            if budget.hard_limit_hit:
                return OrchestratorResult(
                    trace_id=trace_id,
                    person_id=message.person_id,
                    rule_id="BUDGET_EXCEEDED",
                    target_agent="none",
                    confidence=1.0,
                    source="budget_gate",
                    is_multi_intent=False,
                    response="Token budget exceeded for this conversation. Please start a new session.",
                    latency_ms=int(time.time() * 1000) - start_ms,
                    error="hard_limit",
                )

            # 5. Classify intent
            classification = self._classify(message, regex_result, person)

            # 6. Check for multi-intent
            if classification.is_multi_intent and len(classification.sub_intents) >= FAN_OUT_THRESHOLD:
                # Fan-out via forge_parallel
                result = self._fan_out_parallel(message, classification, trace_id)
            elif classification.is_multi_intent:
                # Multi-intent: create DAG workflow
                result = self._create_multi_workflow(message, classification, trace_id)
            else:
                # Single intent: route directly
                result = self._route_single(message, classification, trace_id, dry_run)

            # 7. Record observability
            result.latency_ms = int(time.time() * 1000) - start_ms
            result.fq_advice = fq_advice

            self.obs.log_routing_decision(
                trace_id,
                message.content,
                result.rule_id,
                result.target_agent,
                result.confidence,
                result.source,
            )

            self.obs.end_span(trace_id, root_span, "completed")

            # 8. Record response in state
            if result.response:
                self.state.add_turn(
                    message.person_id,
                    "assistant",
                    result.response,
                    channel=message.channel.value,
                    rule_id=result.rule_id,
                    target_agent=result.target_agent,
                )

            return result

        except Exception as e:
            self.obs.end_span(trace_id, root_span, "failed", {"error": str(e)})
            return OrchestratorResult(
                trace_id=trace_id,
                person_id=message.person_id,
                rule_id="ERROR",
                target_agent="none",
                confidence=0.0,
                source="error",
                is_multi_intent=False,
                error=str(e),
                latency_ms=int(time.time() * 1000) - start_ms,
            )
        finally:
            self.obs.end_trace(trace_id)

    # ─── Intent Classification ───────────────────────────────────────

    def _classify(
        self,
        message: InboundMessage,
        regex_result: dict | None,
        person: PersonState,
    ) -> SemanticResult:
        """Classify intent using regex → semantic fallback."""

        # If regex result provided and confident, use it
        if regex_result:
            regex_confidence = regex_result.get("confidence", 0)
            if regex_confidence >= CONFIDENCE_THRESHOLD:
                return SemanticResult(
                    rule_id=regex_result.get("rule_id", "R10_DEFAULT_TRIAGE"),
                    confidence=regex_confidence,
                    source="regex",
                )

        # Build context from person state
        context = {
            "person_class": person.person_class,
            "language": person.language_preference,
            "recent_routes": [t.rule_id for t in person.conversation_history[-5:] if t.rule_id],
            "active_workflows": person.active_workflows,
        }

        # Check for multi-intent first
        multi_results = classify_multi_intents(
            message.content,
            person_id=message.person_id,
            context=context,
        )

        if len(multi_results) > 1:
            # Multi-intent detected
            primary = multi_results[0]
            primary.is_multi_intent = True
            primary.sub_intents = [
                {"rule_id": r.rule_id, "confidence": r.confidence, "source": r.source} for r in multi_results
            ]
            return primary

        # Single intent — semantic classification
        return classify_intent(
            message.content,
            regex_candidates=[regex_result] if regex_result else None,
            person_id=message.person_id,
            context=context,
        )

    # ─── Single Intent Routing ───────────────────────────────────────

    def _route_single(
        self,
        message: InboundMessage,
        classification: SemanticResult,
        trace_id: str,
        dry_run: bool,
    ) -> OrchestratorResult:
        """Route a single-intent message to the appropriate organ."""
        rule_id = classification.rule_id

        # Build A2A task
        target = resolve_target(rule_id, query=message.content)
        if target.get("local"):
            return OrchestratorResult(
                trace_id=trace_id,
                person_id=message.person_id,
                rule_id=rule_id,
                target_agent="local",
                confidence=classification.confidence,
                source=classification.source,
                is_multi_intent=False,
                response=target.get("response", ""),
            )

        if dry_run:
            return OrchestratorResult(
                trace_id=trace_id,
                person_id=message.person_id,
                rule_id=rule_id,
                target_agent=target.get("target_agent", "unknown"),
                confidence=classification.confidence,
                source=classification.source,
                is_multi_intent=False,
                response=f"[DRY RUN] Would route to {target.get('target_agent')} via {target.get('target_skill')}",
            )

        # Execute A2A dispatch
        task = build_task(
            query=message.content,
            target_agent=target["target_agent"],
            target_skill=target.get("target_skill", "agent-dispatch"),
            context={
                "person_id": message.person_id,
                "person_class": message.person_class,
                "channel": message.channel.value,
                "trace_id": trace_id,
            },
        )

        result = emit(task)

        return OrchestratorResult(
            trace_id=trace_id,
            person_id=message.person_id,
            rule_id=rule_id,
            target_agent=target.get("target_agent", "unknown"),
            confidence=classification.confidence,
            source=classification.source,
            is_multi_intent=False,
            response=result.get("status", "dispatched"),
        )

    # ─── Multi-Intent: DAG Workflow ──────────────────────────────────

    def _create_multi_workflow(
        self,
        message: InboundMessage,
        classification: SemanticResult,
        trace_id: str,
    ) -> OrchestratorResult:
        """Create and execute a DAG workflow for multi-intent messages."""
        sub_intents = classification.sub_intents
        if not sub_intents:
            return self._route_single(message, classification, trace_id, False)

        # Build DAG from sub-intents
        tasks = []
        for i, intent in enumerate(sub_intents):
            rule_id = intent.get("rule_id", "R10_DEFAULT_TRIAGE")
            target = resolve_target(rule_id, query=message.content)

            task_id = f"t{i + 1}_{rule_id}"
            depends_on = [f"t{i}_{sub_intents[i - 1].get('rule_id', 'unknown')}"] if i > 0 else []

            tasks.append(
                {
                    "id": task_id,
                    "agent": target.get("target_agent", "hermes-asi"),
                    "skill": target.get("target_skill", "agent-dispatch"),
                    "query": f"[Multi-intent {i + 1}/{len(sub_intents)}] {message.content}",
                    "depends_on": depends_on,
                }
            )

        flow_json = {
            "id": f"multi-{uuid.uuid4().hex[:8]}",
            "name": f"Multi-intent: {message.content[:50]}",
            "context": {"person_id": message.person_id, "trace_id": trace_id},
            "tasks": tasks,
        }

        flow = self.dag.define_flow(flow_json)
        self.obs.log_workflow_event(flow.id, "created", {"task_count": len(tasks)})

        # Execute
        result = self.dag.execute(flow.id)
        self.obs.log_workflow_event(flow.id, "completed", {"state": result.get("state")})

        # Track workflow
        self.state.add_workflow(message.person_id, flow.id)

        return OrchestratorResult(
            trace_id=trace_id,
            person_id=message.person_id,
            rule_id="MULTI_INTENT_DAG",
            target_agent="dag",
            confidence=classification.confidence,
            source="dag",
            is_multi_intent=True,
            sub_intents=sub_intents,
            workflow_id=flow.id,
            response=self.formatter.format_workflow_result(result),
        )

    # ─── Multi-Intent: Parallel Fan-Out ──────────────────────────────

    def _fan_out_parallel(
        self,
        message: InboundMessage,
        classification: SemanticResult,
        trace_id: str,
    ) -> OrchestratorResult:
        """Fan-out to multiple agents in parallel using forge_parallel."""
        sub_intents = classification.sub_intents
        if not sub_intents:
            return self._route_single(message, classification, trace_id, False)

        # Build parallel tasks
        parallel_tasks = []
        for i, intent in enumerate(sub_intents):
            rule_id = intent.get("rule_id", "R10_DEFAULT_TRIAGE")
            target = resolve_target(rule_id, query=message.content)

            parallel_tasks.append(
                {
                    "agent": target.get("target_agent", "hermes-asi"),
                    "prompt": f"[Fan-out {i + 1}/{len(sub_intents)}] {message.content}",
                    "skill": target.get("target_skill", "agent-dispatch"),
                }
            )

        # Call forge_parallel on A-FORGE
        payload = {
            "jsonrpc": "2.0",
            "id": f"fanout-{uuid.uuid4().hex[:8]}",
            "method": "tools/call",
            "params": {
                "name": "forge_parallel",
                "arguments": {
                    "mode": "parallel",
                    "tasks": parallel_tasks,
                    "max_concurrency": min(len(parallel_tasks), 8),
                    "failure_policy": "collect_all",
                    "timeout_ms": 120000,
                },
            },
        }

        try:
            result = self._emit_a2a(payload)
            self.obs.log_workflow_event(
                trace_id,
                "fan_out_completed",
                {
                    "task_count": len(parallel_tasks),
                    "result": str(result)[:200],
                },
            )

            return OrchestratorResult(
                trace_id=trace_id,
                person_id=message.person_id,
                rule_id="FAN_OUT_PARALLEL",
                target_agent="forge_parallel",
                confidence=classification.confidence,
                source="parallel",
                is_multi_intent=True,
                sub_intents=sub_intents,
                response=f"Dispatched {len(parallel_tasks)} tasks in parallel via forge_parallel.",
            )
        except Exception as e:
            return OrchestratorResult(
                trace_id=trace_id,
                person_id=message.person_id,
                rule_id="FAN_OUT_FAILED",
                target_agent="forge_parallel",
                confidence=0.0,
                source="parallel",
                is_multi_intent=True,
                error=str(e),
            )

    # ─── A2A Communication ───────────────────────────────────────────

    def _emit_a2a(self, payload: dict, timeout: int = 30) -> dict:
        """POST A2A task to AAA gateway."""
        payload_bytes = json.dumps(payload).encode()

        req = urllib.request.Request(
            AAA_A2A_URL,
            data=payload_bytes,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "A2A-Version": "1.0",
                "X-Actor-Id": "openclaw-orchestrator",
            },
        )

        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
            return data.get("result", data)

    # ─── Health Check ────────────────────────────────────────────────

    def health(self) -> dict:
        """Check orchestrator health."""
        return {
            "status": "healthy",
            "components": {
                "semantic_router": "ready",
                "dag_engine": "ready",
                "state_manager": "ready",
                "observability": "ready",
                "channels": self.channels.health(),
            },
            "templates": list(TEMPLATES.keys()),
        }


# ─── Module-level singleton ─────────────────────────────────────────────
_orchestrator: Orchestrator | None = None


def get_orchestrator() -> Orchestrator:
    """Get or create the singleton Orchestrator."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = Orchestrator()
    return _orchestrator


def process_message(
    message: InboundMessage,
    *,
    regex_result: dict | None = None,
    dry_run: bool = False,
) -> OrchestratorResult:
    """Convenience: process a message through the orchestrator."""
    return get_orchestrator().process(message, regex_result=regex_result, dry_run=dry_run)
