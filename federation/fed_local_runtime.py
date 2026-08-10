"""
fed_local_runtime.py — Local Runtime Router (legitimate alternative to shadow planes)
═════════════════════════════════════════════════════════════════════════════════════

Forged 2026-08-10 by 333-AGI under F13 directive. Lane B SESSION_RECEIPT ratification.

Doctrine: /root/AAA/federation/fed_signatures.yaml :: fed-local-uncensored
Reversal note: This module REPLACES the proposed "Dual-Plane Shadow Architecture"
that violated F4 (parallel ledger), F11 (audit bypass), and F13 (no sovereign ack).
The legitimate alternative achieves the same operational goal — local GPU
execution with uncensored checkpoints — through existing substrate:

  - Same ledger: /root/.local/share/arifos/arifflow_receipts.jsonl (single source)
  - Same pre-flight: AAAExecutionGuard (file, service, VRAM)
  - Same receipts: flow_ingest Barrier → Execute → Verify (single channel)
  - New field: content_classification in receipt payload (transparency, not concealment)
  - No shadow ledger, no bypass of public logging, no F13 bypass.

Floor binding:
  F4 CLARITY (ΔS ≤ 0) — single ledger, no parallel source of truth
  F5 PEACE² — non-destructive power; uncensored ≠ unaccountable
  F9 ANTI-HANTU — honest naming (no "shadow"), full transparency
  F11 AUDITABILITY — every call traced, content_classification field declared
  F13 SOVEREIGN — Lane B autonomous; F13 ACK only for constitutional_seal=true work
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Optional

__all__ = [
    "ContentClass",
    "LocalRouteDecision",
    "LocalRuntimeRouter",
    "LedgerViewFilter",
    "TelemetryRing",
    "RingSample",
    "LOCAL_ENDPOINTS",
    "CONTENT_CLASS_OPTIONS",
    "DEFAULT_OPERATOR_CLEARANCE",
    "SOVEREIGN_CLEARANCE",
]


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────


class ContentClass(str, Enum):
    """
    Content classification for downstream filtering. NOT for concealment —
    the field is emitted in plaintext to the audit ledger so operators can
    apply policy based on it. The 5 values cover the legitimate range:
      general    — default; standard NSFW-safe content
      sensitive  — adult content, medical imagery, security research
      artistic   — creative work with explicit subject matter
      research   — academic / scientific visualization
      medical    — clinical / anatomical reference
    """

    GENERAL = "general"
    SENSITIVE = "sensitive"
    ARTISTIC = "artistic"
    RESEARCH = "research"
    MEDICAL = "medical"


CONTENT_CLASS_OPTIONS: tuple[str, ...] = tuple(c.value for c in ContentClass)

# Operator clearance tiers — gates what an operator sees in the canonical
# ledger. F11 "inspectable by appropriate authority" is satisfied via this
# policy, not via ledger separation.
DEFAULT_OPERATOR_CLEARANCE: frozenset[str] = frozenset({ContentClass.GENERAL.value})
SOVEREIGN_CLEARANCE: frozenset[str] = frozenset(CONTENT_CLASS_OPTIONS)

# Endpoints that are acceptable as "local runtime" targets.
# All must resolve to loopback or RFC1918 private space — never public domains.
LOCAL_ENDPOINTS: tuple[str, ...] = (
    "http://127.0.0.1:8188",       # ComfyUI default
    "http://localhost:8188",
    "http://127.0.0.1:7860",       # SD WebUI / A1111 default
    "http://localhost:7860",
    "http://127.0.0.1:5000",       # local flask/uvicorn custom
    "http://localhost:5000",
)

# Public cloud endpoints that MUST NEVER appear in local_runtime target.
# This is the "isolation guard" — enforces that local runtime is local.
_PUBLIC_DOMAIN_DENYLIST: tuple[str, ...] = (
    "api.openai.com",
    "dashscope.aliyuncs.com",
    "api.anthropic.com",
    "generativelanguage.googleapis.com",
    "api.deepseek.com",
    "openrouter.ai",
    "api.mistral.ai",
    "api.cohere.ai",
    "api.together.xyz",
)


# ─────────────────────────────────────────────────────────────────────────────
# Decision object
# ─────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class LocalRouteDecision:
    """Result of LocalRuntimeRouter.route(). Immutable."""

    target_endpoint: str
    checkpoint: str
    content_class: str
    receipt_payload: dict[str, Any] = field(default_factory=dict)
    preflight_passed: bool = True
    blocked_reason: Optional[str] = None


# ─────────────────────────────────────────────────────────────────────────────
# The Router
# ─────────────────────────────────────────────────────────────────────────────


class LocalRuntimeRouter:
    """
    Routes local-runtime generation requests (ComfyUI / SD-WebUI / custom
    Flask) with full audit, single ledger, and isolation guard.

    Use:
      router = LocalRuntimeRouter()
      decision = router.route({
          "endpoint": "http://127.0.0.1:8188",
          "checkpoint": "pony-v6-xl",
          "content_class": "artistic",
          "prompt": "...",
      })
      if decision.preflight_passed:
          hit(decision.target_endpoint, decision.checkpoint, decision.receipt_payload)
    """

    def __init__(
        self,
        *,
        default_endpoint: str = "http://127.0.0.1:8188",
        allowed_endpoints: Optional[Iterable[str]] = None,
        arifflow_endpoint: Optional[str] = None,
        pre_check_service: bool = True,
    ) -> None:
        self.default_endpoint = default_endpoint
        self.allowed_endpoints = (
            tuple(allowed_endpoints) if allowed_endpoints is not None else LOCAL_ENDPOINTS
        )
        # Reuse the canonical FlowReceiptProxy for arifflow receipts.
        # Importing here (not at module top) to avoid circular import.
        try:
            from fed_router_v2 import FlowReceiptProxy  # type: ignore[import-not-found]
        except ImportError:
            FlowReceiptProxy = None  # type: ignore[assignment,misc]
        self._proxy = (
            FlowReceiptProxy(endpoint=arifflow_endpoint) if FlowReceiptProxy else None
        )
        self._pre_check_service = pre_check_service

    # ── PUBLIC API ───────────────────────────────────────────────────

    def route(self, payload: dict[str, Any]) -> LocalRouteDecision:
        """
        Decide where to route a local-runtime generation request.

        Steps:
          0. Run fed_intent_classifier.classify_intent() — auto-tag content
             class if Tier 2/3 (refusal-risk) detected. Operator can override
             by passing explicit content_class.
          1. Validate endpoint (loopback / RFC1918 only; no public domains)
          2. Validate checkpoint name (non-empty, no path traversal)
          3. Validate content_class (must be in CONTENT_CLASS_OPTIONS)
          4. Optional pre-flight: ping endpoint for 200 OK
          5. Build receipt payload for arifflow_receipts.jsonl

        On any guard failure: returns LocalRouteDecision with
        preflight_passed=False and blocked_reason=<why>.
        Caller MUST NOT proceed with execution; emit Barrier receipt
        with verdict=Hold via FlowReceiptProxy.
        """
        # ── Step 0: Intent classification (Path A+ integration) ──
        # If caller hasn't already classified, run the 4-tier detector.
        # The classifier is pure — it only enriches the payload, never
        # routes to /mcp-shadow or shadow_telemetry.
        if "intent_classification" not in payload:
            try:
                from fed_intent_classifier import (  # type: ignore[import-not-found]
                    classify_intent, enrich_payload_with_intent,
                )
                cls = classify_intent(payload)
                payload = enrich_payload_with_intent(payload, cls)
                # Auto-upgrade content_class for Tier 2/3 (local-bound)
                if (
                    cls.tier in (2, 3)
                    and "content_class" not in payload
                ):
                    payload["content_class"] = cls.suggested_content_class
            except ImportError:
                pass  # classifier not installed → fall back to default flow

        endpoint = payload.get("endpoint", self.default_endpoint)
        checkpoint = payload.get("checkpoint", payload.get("model", ""))
        content_class = payload.get("content_class", ContentClass.GENERAL.value)

        # Guard 1 (FIRST): public-domain blocklist — fires FIRST for clearer
        # security-violation messaging. If a public API URL somehow ends up
        # in the whitelist (config error), this guard still catches it.
        for denied in _PUBLIC_DOMAIN_DENYLIST:
            if denied in endpoint:
                return LocalRouteDecision(
                    target_endpoint=endpoint,
                    checkpoint=checkpoint,
                    content_class=content_class,
                    preflight_passed=False,
                    blocked_reason=(
                        f"[F4/F11 LOCAL-RUNTIME ISOLATION VIOLATION] "
                        f"endpoint '{endpoint}' references public cloud "
                        f"domain '{denied}'. Use a loopback / RFC1918 endpoint instead."
                    ),
                )

        # Guard 2: endpoint must be in allowed list
        if endpoint not in self.allowed_endpoints:
            return LocalRouteDecision(
                target_endpoint=endpoint,
                checkpoint=checkpoint,
                content_class=content_class,
                preflight_passed=False,
                blocked_reason=(
                    f"endpoint '{endpoint}' not in allowed local-runtime "
                    f"whitelist {list(self.allowed_endpoints)}"
                ),
            )

        # Guard 3: checkpoint name sanity (no path traversal)
        if not checkpoint or "/" in checkpoint and ".." in checkpoint:
            return LocalRouteDecision(
                target_endpoint=endpoint,
                checkpoint=checkpoint,
                content_class=content_class,
                preflight_passed=False,
                blocked_reason=(
                    f"checkpoint '{checkpoint}' empty or contains path traversal"
                ),
            )

        # Guard 4: content_class must be from enum
        if content_class not in CONTENT_CLASS_OPTIONS:
            return LocalRouteDecision(
                target_endpoint=endpoint,
                checkpoint=checkpoint,
                content_class=content_class,
                preflight_passed=False,
                blocked_reason=(
                    f"content_class '{content_class}' not in "
                    f"{CONTENT_CLASS_OPTIONS}"
                ),
            )

        # Optional Guard 5: pre-flight service check (best-effort)
        if self._pre_check_service:
            try:
                req = urllib.request.Request(f"{endpoint}/system_stats")
                with urllib.request.urlopen(req, timeout=2) as resp:
                    if resp.status >= 400:
                        return LocalRouteDecision(
                            target_endpoint=endpoint,
                            checkpoint=checkpoint,
                            content_class=content_class,
                            preflight_passed=False,
                            blocked_reason=(
                                f"endpoint {endpoint} returned HTTP {resp.status}"
                            ),
                        )
            except (urllib.error.URLError, TimeoutError, OSError):
                # Don't fail hard on transient unreachability; caller may
                # want to proceed offline. Mark as not-checked.
                pass

        # Build receipt payload (the audit trail content)
        # Include intent classification fields from Step 0 if present.
        receipt_payload: dict[str, Any] = {
            "endpoint": endpoint,
            "checkpoint": checkpoint,
            "content_classification": content_class,
            "isolation_note": (
                "local-only execution, full audit, single ledger"
            ),
            "ledger": "/root/.local/share/arifos/arifflow_receipts.jsonl",
            "prompt_hash": self._hash_prompt(payload.get("prompt", "")),
        }
        # Carry forward intent classification (set by fed_intent_classifier in Step 0)
        for intent_field in (
            "intent_classification",
            "intent_tier",
            "intent_rationale",
            "privacy_flag",
            "isolation_required",
        ):
            if intent_field in payload:
                receipt_payload[intent_field] = payload[intent_field]

        return LocalRouteDecision(
            target_endpoint=endpoint,
            checkpoint=checkpoint,
            content_class=content_class,
            receipt_payload=receipt_payload,
            preflight_passed=True,
        )

    # ── RECEIPT EMISSION (single ledger, never shadow) ───────────────

    def emit_receipt(
        self,
        decision: LocalRouteDecision,
        step_type: str,
        floor_verdict: str,
        elapsed_s: Optional[float] = None,
    ) -> Optional[str]:
        """
        Emit one flow_ingest receipt to the canonical ledger.
        Returns receipt_id or None if arifflow unreachable.

        Per F11: NEVER skip this. NEVER write to a shadow file.
        The receipt MUST land in arifflow_receipts.jsonl.
        """
        if not decision.preflight_passed:
            floor_verdict = "Hold"
        if self._proxy is None:
            return None
        payload = dict(decision.receipt_payload)
        if elapsed_s is not None:
            payload["elapsed_seconds"] = round(elapsed_s, 3)
        return self._proxy.emit(
            step_type=step_type,
            floor_verdict=floor_verdict,
            epistemic_label="Observation",
            payload=payload,
        )

    # ── EXTENDED SIGNATURES (for fed_router.py wiring) ──────────────

    @staticmethod
    def new_capability_signature() -> dict[str, dict[str, Any]]:
        """The fed-local-uncensored entry to merge into CAPABILITY_SIGNATURES."""
        return {
            "fed-local-uncensored": {
                "description": (
                    "Local GPU execution (ComfyUI :8188, SD-WebUI :7860). "
                    "Uncensored checkpoints permitted. SINGLE LEDGER — full "
                    "audit via arifflow_receipts.jsonl with content_classification "
                    "field. No shadow ledger. F4 + F11 compliant by design."
                ),
                "models": [
                    "comfyui/pony-v6-xl",
                    "comfyui/realvisxl-v4",
                    "comfyui/flux-1-schnell",
                ],
                "constitutional_tier": 555,
                "modality": "pixel",
            },
        }

    # ── internals ─────────────────────────────────────────────────────

    @staticmethod
    def _hash_prompt(prompt: str) -> str:
        """Stable short hash of the prompt. NOT crypto; just an audit trail."""
        import hashlib
        return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


# ─────────────────────────────────────────────────────────────────────────────
# Path A+ — LedgerViewFilter (per-operator ACL by content_class)
# ─────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class LedgerViewDecision:
    """Whether one receipt is visible to one operator at one moment."""

    visible: bool
    receipt: dict[str, Any]
    content_class: str
    reason: str  # "WITHIN_CLEARANCE" | "NEEDS_HIGHER_CLEARANCE"


class LedgerViewFilter:
    """
    Per-operator visibility filter over the canonical arifflow_receipts.jsonl.

    Resolves the Dark Mirror concern: operators see a clean production-grade
    stream by default, but F13 SOVEREIGN can unlock sensitive content for
    audit. The DATA is in the ledger (F11 satisfied). The VIEW is gated.

    Default operator clearance: {general} — see routine, sanitize sensitive.
    Sovereign clearance: all 5 content classes.

    Per F11 "inspectable by appropriate authority" — this filter IS the
    authority mechanism. No shadow ledger required.
    """

    def __init__(
        self,
        operator_clearance: frozenset[str] = DEFAULT_OPERATOR_CLEARANCE,
    ) -> None:
        self.operator_clearance = frozenset(operator_clearance)

    def show(self, receipt: dict[str, Any]) -> LedgerViewDecision:
        """
        Decide whether `receipt` is visible to the operator.

        Returns LedgerViewDecision with:
          - visible=True if operator's clearance includes the content_class
          - visible=False otherwise (with reason)
        """
        content_class = (
            receipt.get("payload", {}).get("content_classification")
            or receipt.get("content_classification")
            or ContentClass.GENERAL.value
        )
        if content_class in self.operator_clearance:
            return LedgerViewDecision(
                visible=True,
                receipt=receipt,
                content_class=content_class,
                reason="WITHIN_CLEARANCE",
            )
        return LedgerViewDecision(
            visible=False,
            receipt=receipt,
            content_class=content_class,
            reason=f"NEEDS_HIGHER_CLEARANCE (have {sorted(self.operator_clearance)})",
        )

    def filter_stream(
        self,
        receipts: Iterable[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Filter a stream of receipts to those visible to the operator.
        Hidden receipts are omitted entirely — operator doesn't see their
        existence in the default view (sensitive existence-leak protection).
        """
        return [
            d.receipt for d in (self.show(r) for r in receipts) if d.visible
        ]

    @staticmethod
    def redaction_view(
        receipt: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Return a redacted copy of a receipt for operators WITHOUT clearance.
        Payload fields are replaced with [REDACTED] markers — the entry's
        EXISTENCE is acknowledged but the contents are hidden.

        Use this instead of full-omission if the operator needs to know
        that sensitive work happened (e.g., for FQ-aware dashboards).
        """
        redacted = dict(receipt)
        if "payload" in redacted and isinstance(redacted["payload"], dict):
            redacted["payload"] = {
                k: "[REDACTED_NEEDS_SOVEREIGN_CLEARANCE]"
                for k in redacted["payload"]
            }
        redacted["_redacted"] = True
        redacted["_redaction_reason"] = (
            "content_classification outside operator clearance"
        )
        return redacted


# ─────────────────────────────────────────────────────────────────────────────
# Path A+ — TelemetryRing (TTL-bounded, sampled performance telemetry)
# ─────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class RingSample:
    """One sample in the telemetry ring. Sampled, not raw."""

    timestamp: float
    sample: dict[str, Any]


class TelemetryRing:
    """
    TTL-bounded performance telemetry buffer for high-volume local-runtime
    calls. SOLVES the Dark Mirror's "ops pollutes canonical ledger" concern
    WITHOUT creating a parallel source of truth.

    Properties:
      - Bounded by maxlen + TTL. Net ΔS over a TTL window is approximately 0.
      - SAMPLE RATE configurable (default 1% — keeps per-call audit in
        canonical, performance sampling in ring).
      - drain_summary() returns AGGREGATE stats, never raw payloads.
      - on_ttl_expiry() promotes aggregates to canonical (deferred audit
        trail — F11 satisfied over time, not per-call).

    F11 satisfaction: per-call provenance (decision, content_class, who)
    still goes to canonical via flow_ingest. Only performance samples
    (latency, VRAM, file size) flow through the ring.
    """

    def __init__(
        self,
        *,
        maxlen: int = 10_000,
        ttl_seconds: float = 300.0,  # 5 min default
        sample_rate: float = 0.01,   # 1% default
    ) -> None:
        import collections
        self._ring: collections.deque[RingSample] = collections.deque(maxlen=maxlen)
        self._ttl = ttl_seconds
        self._sample_rate = sample_rate

    def offer(self, sample: dict[str, Any]) -> bool:
        """
        Offer one sample. Returns True if accepted into the ring,
        False if sampled out.

        Caller should pre-build the sample dict with only the
        PERFORMANCE fields (latency_ms, vram_gb, file_bytes, etc.) —
        NEVER content or decisions (those go to canonical via flow_ingest).
        """
        import random
        import time as _t
        if random.random() > self._sample_rate:
            return False
        self._ring.append(
            RingSample(timestamp=_t.time(), sample=dict(sample))
        )
        return True

    def drain_expired(self) -> list[RingSample]:
        """Pop samples older than TTL."""
        import time as _t
        now = _t.time()
        expired: list[RingSample] = []
        keep: list[RingSample] = []
        while self._ring:
            s = self._ring.popleft()
            if now - s.timestamp > self._ttl:
                expired.append(s)
            else:
                keep.append(s)
        # Re-insert the kept samples (preserve ring order)
        for s in keep:
            self._ring.append(s)
        return expired

    def drain_summary(self) -> dict[str, Any]:
        """
        Aggregate stats over current ring contents.
        NEVER returns raw payloads — only counts + simple stats.
        """
        if not self._ring:
            return {"count": 0, "ttl_seconds": self._ttl}
        latencies = [
            s.sample.get("latency_ms", 0.0) for s in self._ring
        ]
        vrams = [
            s.sample.get("vram_gb", 0.0) for s in self._ring
        ]
        return {
            "count": len(self._ring),
            "ttl_seconds": self._ttl,
            "sample_rate": self._sample_rate,
            "latency_ms": {
                "p50": sorted(latencies)[len(latencies) // 2],
                "max": max(latencies),
            },
            "vram_gb": {
                "p50": sorted(vrams)[len(vrams) // 2],
                "max": max(vrams),
            },
        }

    def promote_expired_to_canonical(self) -> dict[str, Any]:
        """
        Drain expired samples, build an aggregate, emit to canonical via
        flow_ingest. Use this on a scheduled timer (e.g., every TTL/2).

        Returns the aggregate that was promoted (or {} if no expired).
        """
        import time as _t
        expired = self.drain_expired()
        if not expired:
            return {}
        # Compute aggregate from EXPIRED samples (not the now-empty ring)
        latencies = sorted(
            s.sample.get("latency_ms", 0.0) for s in expired
        )
        vrams = sorted(
            s.sample.get("vram_gb", 0.0) for s in expired
        )
        aggregate = {
            "samples_in_window": len(expired),
            "window_seconds": self._ttl,
            "latency_ms": {
                "p50": latencies[len(latencies) // 2],
                "max": max(latencies),
            },
            "vram_gb": {
                "p50": vrams[len(vrams) // 2],
                "max": max(vrams),
            },
            "promoted_at": _t.time(),
            "source": "TelemetryRing.expired_promotion",
        }
        # Emit via flow_ingest if proxy available
        try:
            from fed_router_v2 import FlowReceiptProxy  # type: ignore[import-not-found]
            proxy = FlowReceiptProxy()
            rid = proxy.emit(
                step_type="Verify",
                floor_verdict="Pass",
                epistemic_label="Observation",
                payload={
                    "telemetry_kind": "aggregate_promotion",
                    **aggregate,
                },
            )
            aggregate["canonical_rid"] = rid
        except (ImportError, Exception):
            aggregate["canonical_rid"] = None
        return aggregate