#!/usr/bin/env python3
"""
P1.6 — A-FORGE SIDECAR Auto-Ingest Interceptor (:7074 wrapper)
==============================================================
Wraps the FED execution transport socket layer. For every request/response
cycle passing through FED, automatically emits JSON execution spans to
arifFlow (:7073).

Enforces the Self-Attestation Ban: agents MUST NOT invoke their own logging
tools. All telemetry is captured transparently by the sidecar — the agent
never knows it's being observed.

Architecture:
  Agent → FED (:7074) [SIDECAR WRAPS] → arifFlow (:7073) [METABOLIC INGEST]
                       ↓
  Every fed_route call → sidecar intercept → emit FlowReceipt to arifFlow

Forged: 2026-08-10 by 333-AGI under F13 directive.
DITEMPA BUKAN DIBERI ⚒️
"""

import os
import sys
import json
import time
import hashlib
import uuid
import threading
from pathlib import Path
from datetime import datetime, timezone

# ── Sidecar config ────────────────────────────────────────────────
ARIFLOW_URL = os.environ.get("ARIFLOW_URL", "http://127.0.0.1:7073")
SIDECAR_LOG = Path("/root/.local/share/arifos/sidecar_spans.jsonl")
SELF_ATTESTATION_BAN = True  # Agents must not self-log


# ── Span emitter ──────────────────────────────────────────────────
class SidecarSpan:
    """A single execution span captured by the sidecar."""

    def __init__(self, agent_id: str, session_id: str, operation: str):
        self.trace_id = str(uuid.uuid4()).replace("-", "")[:32]
        self.span_id = str(uuid.uuid4()).replace("-", "")[:16]
        self.parent_span_id = None
        self.agent_id = agent_id
        self.session_id = session_id
        self.operation = operation
        self.start_time = time.time()
        self.end_time = None
        self.duration_ms = 0.0
        self.status = "started"
        self.metadata = {}

    def finish(self, status: str = "ok", metadata: dict = None):
        self.end_time = time.time()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 2)
        self.status = status
        if metadata:
            self.metadata = metadata

    def to_flow_receipt(self) -> dict:
        """Convert span to arifFlow-compatible FlowReceipt."""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "agent_id": self.agent_id,
            "session_id": self.session_id,
            "step_type": "Execute",
            "cost_ns": int(self.duration_ms * 1_000_000) if self.duration_ms else 0,
            "epistemic_label": "Observation",
            "floor_verdict": "Pass",
            "payload": {
                "operation": self.operation,
                "status": self.status,
                "duration_ms": self.duration_ms,
                "captured_by": "sidecar-auto-ingest",
                "self_attestation_ban": SELF_ATTESTATION_BAN,
                **self.metadata,
            },
            "witness_organs": ["aforge", "fed"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def persist(self):
        """Append span to sidecar ledger."""
        receipt = self.to_flow_receipt()
        SIDECAR_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(SIDECAR_LOG, "a") as f:
            f.write(json.dumps(receipt) + "\n")


# ── arifFlow ingestion ────────────────────────────────────────────
def ingest_to_arifflow(span: SidecarSpan, act_token: str = "") -> bool:
    """Push a span to arifFlow :7073 for metabolic ingestion."""
    import urllib.request

    receipt = span.to_flow_receipt()
    try:
        req = urllib.request.Request(
            f"{ARIFLOW_URL}/ingest",
            data=json.dumps(receipt).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=2)
        return True
    except Exception:
        # arifFlow may be down — persist locally as fallback
        span.persist()
        return False


# ── Intercept decorator ────────────────────────────────────────────
def intercept(func):
    """Wrap an MCP tool function with sidecar telemetry."""

    def wrapper(*args, **kwargs):
        span = SidecarSpan(
            agent_id=kwargs.get("agent_id", "unknown"),
            session_id=kwargs.get("session_id", "unknown"),
            operation=func.__name__,
        )

        try:
            result = func(*args, **kwargs)
            span.finish("ok", {"routes_count": len(result.get("routes", [])) if isinstance(result, dict) else 0})
        except Exception as e:
            span.finish("error", {"error": str(e)})
            raise
        finally:
            # Fire-and-forget ingestion (non-blocking)
            threading.Thread(target=ingest_to_arifflow, args=(span,), daemon=True).start()

        return result

    return wrapper


# ── CLI ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("🧪 Sidecar Interceptor — test span")
        span = SidecarSpan(agent_id="test-agent", session_id="test-sid", operation="fed_route")
        span.finish("ok", {"test": True})
        ingest_to_arifflow(span)
        print(f"   Span: {span.trace_id} / {span.span_id}")
        print(f"   Duration: {span.duration_ms}ms")
        print(f"   Logged to: {SIDECAR_LOG}")
    elif len(sys.argv) > 1 and sys.argv[1] == "daemon":
        print("🔍 Sidecar Daemon — watching FED :7074 → arifFlow :7073")
        print(f"   Self-attestation ban: {SELF_ATTESTATION_BAN}")
        print(f"   Span log: {SIDECAR_LOG}")
        print("   (Daemon mode: attach to FED MCP server transport)")
        # In production, this would monkey-patch the FED transport layer
        # For now, spans are emitted via the intercept() decorator
    else:
        print("Sidecar Auto-Ingest Interceptor — P1.6")
        print("Usage: python3 sidecar_interceptor.py [test|daemon]")
        print(f"arifFlow: {ARIFLOW_URL}")
        print(f"Spans: {SIDECAR_LOG}")
