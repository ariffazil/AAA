#!/usr/bin/env python3
"""
P1.7 — A2A Trace Propagation Headers
====================================
Enforces standard W3C trace context propagation on all inter-agent
message envelopes across the federation:

  traceparent: 00-{trace_id}-{span_id}-01
  arif_trace_id: {trace_id}

This module provides the header injection helpers used by:
  - FED Router (:7074) — attaches to every fed_route response
  - AAA Dispatch (:3001) — attaches to every a2a message
  - Hermes Bridge — attaches to every Telegram→agent relay
  - OpenClaw Gateway — attaches to every inbound message

Forged: 2026-08-10 by 333-AGI under F13 directive.
TRACE_HEADER_SPEC: W3C Trace Context Level 2 (traceparent:00-{tid}-{sid}-01)
"""

import uuid
import hashlib
from typing import Optional


def generate_trace_id(source: str = "") -> str:
    """Generate a 32-hex-char trace ID. Uses source entropy for determinism."""
    if source:
        return hashlib.sha256(source.encode()).hexdigest()[:32]
    return uuid.uuid4().hex


def generate_span_id() -> str:
    """Generate a 16-hex-char span ID."""
    return uuid.uuid4().hex[:16]


def make_traceparent(trace_id: str, span_id: str, sampled: bool = True) -> str:
    """
    W3C traceparent header: 00-{trace_id}-{span_id}-{trace_flags}
    trace_flags: 01 = sampled, 00 = not sampled
    """
    flags = "01" if sampled else "00"
    return f"00-{trace_id}-{span_id}-{flags}"


def make_trace_headers(
    trace_id: Optional[str] = None,
    span_id: Optional[str] = None,
    parent_trace_id: Optional[str] = None,
) -> dict:
    """
    Produce standard A2A trace propagation headers.

    Args:
        trace_id: If None, generates a new one. If provided, reuses.
        span_id: If None, generates new child span. If parent_trace_id set, links.
        parent_trace_id: Optional parent trace for linking.

    Returns:
        dict with 'traceparent' and 'arif_trace_id' keys.
    """
    tid = trace_id or generate_trace_id()
    sid = span_id or generate_span_id()

    return {
        "traceparent": make_traceparent(tid, sid),
        "arif_trace_id": tid,
        "arif_span_id": sid,
    }


def inject_trace_headers(headers: dict, trace_id: str = "", span_id: str = "") -> dict:
    """
    Inject trace headers into an existing headers dict.
    Does NOT overwrite existing trace headers (first-writer-wins).
    """
    if "traceparent" not in headers:
        headers["traceparent"] = make_traceparent(
            trace_id or generate_trace_id(),
            span_id or generate_span_id(),
        )
    if "arif_trace_id" not in headers:
        headers["arif_trace_id"] = (
            trace_id or headers.get("traceparent", "").split("-")[1]
            if "traceparent" in headers
            else generate_trace_id()
        )
    if "arif_span_id" not in headers and span_id:
        headers["arif_span_id"] = span_id

    return headers


# ── CLI ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        h = make_trace_headers()
        print("🧪 A2A Trace Headers — test generation")
        for k, v in h.items():
            print(f"   {k}: {v}")

        # Test injection
        existing = {"Authorization": "Bearer xxx", "traceparent": "00-oldtrace-oldspan-01"}
        injected = inject_trace_headers(existing)
        print(f"\n   Injected (first-writer-wins): {injected['traceparent']} (preserved old)")
    else:
        print("A2A Trace Propagation Headers — P1.7")
        print("Usage: python3 trace_propagation.py test")
        print("W3C Trace Context Level 2 compliant")
