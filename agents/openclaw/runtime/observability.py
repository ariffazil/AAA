#!/usr/bin/env python3
"""
OpenClaw Observability Layer v1.0.0

Lightweight observability for OpenClaw orchestrator:
  - Trace ID generation and propagation
  - Token budget tracking per conversation
  - FQ correlation with routing decisions
  - Latency tracking per agent/operation
  - Structured event logging (JSONL)

No OTel dependency — pure Python, zero external deps.
Can be upgraded to OTel later.

Forged: 2026-09-12 by 333-AGI under F13 directive
DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import json
import os
import time
import uuid
import threading
from typing import Any, Optional
from dataclasses import dataclass, field, asdict
from collections import defaultdict


# ─── Constants ───────────────────────────────────────────────────────────
TRACE_LOG_DIR = os.environ.get("OPENCLAW_TRACE_DIR", "/root/AAA/agents/openclaw/runtime/traces")
TOKEN_BUDGET_DEFAULT = int(os.environ.get("OPENCLAW_TOKEN_BUDGET", "100000"))  # tokens per conversation
BUDGET_WARNING_THRESHOLD = float(os.environ.get("OPENCLAW_BUDGET_WARN", "0.8"))  # 80%
BUDGET_HARD_LIMIT = float(os.environ.get("OPENCLAW_BUDGET_HARD", "0.95"))  # 95%
ARIFLOW_HEALTH_URL = "http://127.0.0.1:7073/health"


@dataclass
class TraceSpan:
    """A single trace span."""

    span_id: str
    trace_id: str
    parent_id: str | None
    operation: str
    agent: str
    started_at: float
    completed_at: float = 0
    status: str = "running"  # running | completed | failed
    attributes: dict = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)


@dataclass
class TokenBudget:
    """Token budget tracker for a conversation."""

    conversation_id: str
    budget: int = TOKEN_BUDGET_DEFAULT
    used: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    warnings_issued: int = 0
    hard_limit_hit: bool = False


@dataclass
class FQSnapshot:
    """FQ state at a point in time."""

    fq: float
    source: str  # live | cache | unreachable
    timestamp: float
    verdict: str  # FLOWING | STUCK | BURNING


class ObservabilityLayer:
    """
    Lightweight observability for OpenClaw orchestrator.
    """

    def __init__(self):
        os.makedirs(TRACE_LOG_DIR, exist_ok=True)
        self._active_traces: dict[str, list[TraceSpan]] = {}
        self._token_budgets: dict[str, TokenBudget] = {}
        self._fq_history: list[FQSnapshot] = []
        self._latency_stats: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()
        self._event_log_path = os.path.join(TRACE_LOG_DIR, "events.jsonl")

    # ─── Tracing ─────────────────────────────────────────────────────

    def start_trace(
        self,
        operation: str,
        agent: str = "openclaw",
        attributes: dict | None = None,
    ) -> tuple[str, str]:
        """
        Start a new trace. Returns (trace_id, span_id).
        """
        trace_id = f"tr-{uuid.uuid4().hex[:16]}"
        span_id = f"sp-{uuid.uuid4().hex[:8]}"

        span = TraceSpan(
            span_id=span_id,
            trace_id=trace_id,
            parent_id=None,
            operation=operation,
            agent=agent,
            started_at=time.time(),
            attributes=attributes or {},
        )

        with self._lock:
            self._active_traces[trace_id] = [span]

        self._log_event(
            "trace_start",
            {
                "trace_id": trace_id,
                "span_id": span_id,
                "operation": operation,
                "agent": agent,
            },
        )

        return trace_id, span_id

    def start_span(
        self,
        trace_id: str,
        operation: str,
        agent: str = "openclaw",
        parent_span_id: str | None = None,
        attributes: dict | None = None,
    ) -> str:
        """Start a child span within a trace. Returns span_id."""
        span_id = f"sp-{uuid.uuid4().hex[:8]}"

        span = TraceSpan(
            span_id=span_id,
            trace_id=trace_id,
            parent_id=parent_span_id,
            operation=operation,
            agent=agent,
            started_at=time.time(),
            attributes=attributes or {},
        )

        with self._lock:
            if trace_id in self._active_traces:
                self._active_traces[trace_id].append(span)

        return span_id

    def end_span(
        self,
        trace_id: str,
        span_id: str,
        status: str = "completed",
        attributes: dict | None = None,
    ) -> None:
        """End a span."""
        with self._lock:
            if trace_id in self._active_traces:
                for span in self._active_traces[trace_id]:
                    if span.span_id == span_id:
                        span.completed_at = time.time()
                        span.status = status
                        if attributes:
                            span.attributes.update(attributes)

                        # Track latency
                        latency_ms = (span.completed_at - span.started_at) * 1000
                        self._latency_stats[span.agent].append(latency_ms)
                        break

    def end_trace(self, trace_id: str, status: str = "completed") -> dict:
        """End a trace and return summary."""
        with self._lock:
            spans = self._active_traces.pop(trace_id, [])

        for span in spans:
            if span.completed_at == 0:
                span.completed_at = time.time()
                span.status = status

        summary = {
            "trace_id": trace_id,
            "status": status,
            "span_count": len(spans),
            "total_duration_ms": round(
                (max(s.completed_at for s in spans) - min(s.started_at for s in spans)) * 1000, 2
            )
            if spans
            else 0,
            "agents_involved": list(set(s.agent for s in spans)),
            "operations": [
                {
                    "operation": s.operation,
                    "agent": s.agent,
                    "duration_ms": round((s.completed_at - s.started_at) * 1000, 2),
                    "status": s.status,
                }
                for s in spans
            ],
        }

        # Write to trace file
        trace_path = os.path.join(TRACE_LOG_DIR, f"{trace_id}.json")
        with open(trace_path, "w") as f:
            json.dump(summary, f, indent=2)

        self._log_event("trace_end", summary)
        return summary

    # ─── Token Budget ────────────────────────────────────────────────

    def get_budget(self, conversation_id: str) -> TokenBudget:
        """Get or create token budget for a conversation."""
        if conversation_id not in self._token_budgets:
            self._token_budgets[conversation_id] = TokenBudget(
                conversation_id=conversation_id,
            )
        return self._token_budgets[conversation_id]

    def record_tokens(
        self,
        conversation_id: str,
        input_tokens: int,
        output_tokens: int,
    ) -> dict:
        """Record token usage. Returns budget status."""
        budget = self.get_budget(conversation_id)
        total = input_tokens + output_tokens
        budget.used += total
        budget.input_tokens += input_tokens
        budget.output_tokens += output_tokens

        usage_ratio = budget.used / budget.budget

        result = {
            "conversation_id": conversation_id,
            "used": budget.used,
            "budget": budget.budget,
            "remaining": budget.budget - budget.used,
            "usage_ratio": round(usage_ratio, 3),
            "status": "ok",
        }

        if usage_ratio >= BUDGET_HARD_LIMIT:
            budget.hard_limit_hit = True
            result["status"] = "hard_limit"
            result["warning"] = f"Token budget {usage_ratio:.0%} used. Hard limit reached."
            self._log_event("token_hard_limit", result)
        elif usage_ratio >= BUDGET_WARNING_THRESHOLD:
            budget.warnings_issued += 1
            result["status"] = "warning"
            result["warning"] = f"Token budget {usage_ratio:.0%} used."
            self._log_event("token_warning", result)

        return result

    def can_proceed(self, conversation_id: str) -> bool:
        """Check if conversation can proceed (not at hard limit)."""
        budget = self.get_budget(conversation_id)
        return not budget.hard_limit_hit

    def get_budget_summary(self, conversation_id: str) -> dict:
        """Get budget summary."""
        budget = self.get_budget(conversation_id)
        return {
            "conversation_id": conversation_id,
            "used": budget.used,
            "budget": budget.budget,
            "remaining": budget.budget - budget.used,
            "usage_ratio": round(budget.used / budget.budget, 3) if budget.budget else 0,
            "input_tokens": budget.input_tokens,
            "output_tokens": budget.output_tokens,
            "warnings": budget.warnings_issued,
            "hard_limit_hit": budget.hard_limit_hit,
        }

    # ─── FQ Correlation ──────────────────────────────────────────────

    def record_fq(self, fq: float, source: str = "live") -> FQSnapshot:
        """Record FQ snapshot for correlation."""
        if fq < 0.5:
            verdict = "STUCK"
        elif fq > 2.0:
            verdict = "BURNING"
        else:
            verdict = "FLOWING"

        snapshot = FQSnapshot(
            fq=fq,
            source=source,
            timestamp=time.time(),
            verdict=verdict,
        )

        with self._lock:
            self._fq_history.append(snapshot)
            # Keep last 1000
            if len(self._fq_history) > 1000:
                self._fq_history = self._fq_history[-1000:]

        return snapshot

    def get_fq_advice(self) -> dict:
        """Get routing advice based on FQ history."""
        if not self._fq_history:
            return {"advice": "unknown", "reason": "no FQ data"}

        recent = self._fq_history[-10:]
        avg_fq = sum(s.fq for s in recent) / len(recent)
        latest = recent[-1]

        if avg_fq < 0.5:
            return {
                "advice": "simplify",
                "reason": f"FQ avg {avg_fq:.2f} — system is stuck. Simplify responses, don't escalate.",
                "avg_fq": avg_fq,
                "latest": latest.fq,
            }
        elif avg_fq > 2.0:
            return {
                "advice": "slow_down",
                "reason": f"FQ avg {avg_fq:.2f} — system is burning. Execution outrunning verification.",
                "avg_fq": avg_fq,
                "latest": latest.fq,
            }
        else:
            return {
                "advice": "normal",
                "reason": f"FQ avg {avg_fq:.2f} — healthy flow.",
                "avg_fq": avg_fq,
                "latest": latest.fq,
            }

    # ─── Latency Stats ───────────────────────────────────────────────

    def get_latency_stats(self, agent: str | None = None) -> dict:
        """Get latency statistics per agent."""
        if agent:
            latencies = self._latency_stats.get(agent, [])
            return self._compute_latency(agent, latencies)

        return {agent_name: self._compute_latency(agent_name, lats) for agent_name, lats in self._latency_stats.items()}

    def _compute_latency(self, agent: str, latencies: list[float]) -> dict:
        """Compute latency stats for an agent."""
        if not latencies:
            return {"agent": agent, "count": 0}
        return {
            "agent": agent,
            "count": len(latencies),
            "avg_ms": round(sum(latencies) / len(latencies), 2),
            "min_ms": round(min(latencies), 2),
            "max_ms": round(max(latencies), 2),
            "p50_ms": round(sorted(latencies)[len(latencies) // 2], 2),
            "p95_ms": round(sorted(latencies)[int(len(latencies) * 0.95)], 2) if len(latencies) >= 20 else None,
        }

    # ─── Event Logging ───────────────────────────────────────────────

    def _log_event(self, event_type: str, data: dict) -> None:
        """Append structured event to JSONL log."""
        event = {
            "type": event_type,
            "timestamp": time.time(),
            "iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            **data,
        }
        try:
            with open(self._event_log_path, "a") as f:
                f.write(json.dumps(event, default=str) + "\n")
        except Exception:
            pass

    def log_routing_decision(
        self,
        trace_id: str,
        query: str,
        rule_id: str,
        target_agent: str,
        confidence: float,
        source: str,  # regex | semantic | fallback
    ) -> None:
        """Log a routing decision."""
        self._log_event(
            "routing_decision",
            {
                "trace_id": trace_id,
                "query_preview": query[:100],
                "rule_id": rule_id,
                "target_agent": target_agent,
                "confidence": confidence,
                "source": source,
            },
        )

    def log_workflow_event(self, flow_id: str, event: str, details: dict | None = None) -> None:
        """Log a workflow lifecycle event."""
        self._log_event(
            "workflow_event",
            {
                "flow_id": flow_id,
                "event": event,
                "details": details or {},
            },
        )


# ─── Module-level singleton ─────────────────────────────────────────────
_obs: ObservabilityLayer | None = None


def get_observability() -> ObservabilityLayer:
    """Get or create the singleton ObservabilityLayer."""
    global _obs
    if _obs is None:
        _obs = ObservabilityLayer()
    return _obs
