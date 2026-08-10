"""
Tests for fed_local_runtime.LocalRuntimeRouter + fed_local_runtime_guard.

Forged 2026-08-10. Lane B SESSION_RECEIPT ratification.

Coverage:
  - LocalRuntimeRouter: route() decisions + guard failures
  - ContentClass enum validation
  - LocalRuntimeGuard: public-API blocklist + localhost enforcement
  - Determinism + edge cases (empty, malformed)
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Ensure AAA root + federation on sys.path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEDERATION_ROOT = PROJECT_ROOT / "federation"
for p in (str(PROJECT_ROOT), str(FEDERATION_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

from fed_local_runtime import (  # noqa: E402
    CONTENT_CLASS_OPTIONS,
    DEFAULT_OPERATOR_CLEARANCE,
    LOCAL_ENDPOINTS,
    SOVEREIGN_CLEARANCE,
    ContentClass,
    LedgerViewDecision,
    LedgerViewFilter,
    LocalRouteDecision,
    LocalRuntimeRouter,
    RingSample,
    TelemetryRing,
)
from local_runtime_guard import (  # noqa: E402
    AAALocalRuntimeGuard,
    LOCALHOST_PATTERNS,
    PUBLIC_API_DOMAINS,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture
def router() -> LocalRuntimeRouter:
    return LocalRuntimeRouter(pre_check_service=False)


# ─────────────────────────────────────────────────────────────────────────────
# LocalRuntimeRouter.route() — happy path
# ─────────────────────────────────────────────────────────────────────────────


class TestLocalRuntimeHappyPath:
    def test_default_endpoint_comfyui(
        self, router: LocalRuntimeRouter
    ) -> None:
        d = router.route(
            {"checkpoint": "sdxl-base", "prompt": "..."}
        )
        assert d.preflight_passed is True
        assert d.target_endpoint == "http://127.0.0.1:8188"
        assert d.checkpoint == "sdxl-base"
        # classifier (Path A+ integration) auto-tags; sdxl-base has no
        # shadow keyword so default = general
        assert d.content_class == ContentClass.GENERAL.value
        assert d.receipt_payload["ledger"] == (
            "/root/.local/share/arifos/arifflow_receipts.jsonl"
        )

    def test_explicit_endpoint_accepted(
        self, router: LocalRuntimeRouter
    ) -> None:
        d = router.route(
            {
                "endpoint": "http://127.0.0.1:7860",
                "checkpoint": "realvisxl-v4",
                "content_class": "artistic",
            }
        )
        assert d.preflight_passed is True
        assert d.target_endpoint == "http://127.0.0.1:7860"
        assert d.content_class == "artistic"

    def test_all_content_classes_accepted(
        self, router: LocalRuntimeRouter
    ) -> None:
        for cc in CONTENT_CLASS_OPTIONS:
            d = router.route(
                {"endpoint": "http://127.0.0.1:8188",
                 "checkpoint": "flux-1-schnell",
                 "content_class": cc}
            )
            assert d.preflight_passed is True, f"rejected {cc}"
            assert d.content_class == cc

    def test_receipt_payload_contains_content_classification(
        self, router: LocalRuntimeRouter
    ) -> None:
        d = router.route(
            {"checkpoint": "pony-v6-xl", "content_class": "sensitive"}
        )
        # Per F11: content_classification MUST be in payload (transparency, not concealment)
        assert d.receipt_payload["content_classification"] == "sensitive"
        assert "ledger" in d.receipt_payload
        assert "isolation_note" in d.receipt_payload

    def test_prompt_hashed_not_stored(
        self, router: LocalRuntimeRouter
    ) -> None:
        d = router.route(
            {"checkpoint": "pony-v6-xl", "prompt": "secret prompt text"}
        )
        # Prompt must NOT appear in payload verbatim — only hash
        assert "secret prompt text" not in str(d.receipt_payload)
        # But a hash field is present
        assert "prompt_hash" in d.receipt_payload
        assert len(d.receipt_payload["prompt_hash"]) == 16


# ─────────────────────────────────────────────────────────────────────────────
# LocalRuntimeRouter.route() — guard failures (F4 + F11 isolation)
# ─────────────────────────────────────────────────────────────────────────────


class TestLocalRuntimeGuards:
    def test_unknown_endpoint_blocked(
        self, router: LocalRuntimeRouter
    ) -> None:
        d = router.route(
            {"endpoint": "http://192.168.1.42:8188",
             "checkpoint": "pony-v6-xl"}
        )
        assert d.preflight_passed is False
        assert "not in allowed local-runtime" in d.blocked_reason

    @pytest.mark.parametrize("public_url", [
        "https://api.openai.com/v1/images/generations",
        "https://dashscope.aliyuncs.com/v1/services/aigc/text2image",
        "https://api.anthropic.com/v1/messages",
        "https://generativelanguage.googleapis.com/v1/models",
        "https://api.deepseek.com/v1/chat/completions",
        "https://openrouter.ai/api/v1/chat",
    ])
    def test_public_cloud_api_blocked(
        self, router: LocalRuntimeRouter, public_url: str
    ) -> None:
        """F4 + F11 isolation guard — local runtime MUST NOT hit public APIs."""
        d = router.route(
            {"endpoint": public_url, "checkpoint": "pony-v6-xl"}
        )
        assert d.preflight_passed is False
        assert "LOCAL-RUNTIME ISOLATION VIOLATION" in d.blocked_reason
        assert "public cloud" in d.blocked_reason

    def test_empty_checkpoint_blocked(
        self, router: LocalRuntimeRouter
    ) -> None:
        d = router.route({"endpoint": "http://127.0.0.1:8188"})
        assert d.preflight_passed is False
        assert "checkpoint" in d.blocked_reason

    def test_path_traversal_checkpoint_blocked(
        self, router: LocalRuntimeRouter
    ) -> None:
        d = router.route(
            {"endpoint": "http://127.0.0.1:8188",
             "checkpoint": "../../etc/passwd"}
        )
        assert d.preflight_passed is False
        assert "path traversal" in d.blocked_reason

    def test_invalid_content_class_blocked(
        self, router: LocalRuntimeRouter
    ) -> None:
        d = router.route(
            {"endpoint": "http://127.0.0.1:8188",
             "checkpoint": "pony-v6-xl",
             "content_class": "literally_nsfw_unmoderated"}
        )
        assert d.preflight_passed is False
        assert "content_class" in d.blocked_reason


# ─────────────────────────────────────────────────────────────────────────────
# Determinism
# ─────────────────────────────────────────────────────────────────────────────


class TestDeterminism:
    def test_repeated_route_is_stable(
        self, router: LocalRuntimeRouter
    ) -> None:
        payload = {"checkpoint": "pony-v6-xl", "content_class": "artistic"}
        decisions = [router.route(payload) for _ in range(10)]
        # Same checkpoint name, same class → same endpoint + class
        assert all(d.target_endpoint == decisions[0].target_endpoint for d in decisions)
        assert all(d.content_class == decisions[0].content_class for d in decisions)


# ─────────────────────────────────────────────────────────────────────────────
# LocalRuntimeGuard (the refactored isolation guard)
# ─────────────────────────────────────────────────────────────────────────────


class TestLocalRuntimeGuard:
    def test_non_local_signature_passes(self) -> None:
        # Guard does NOT apply to non-local signatures
        assert AAALocalRuntimeGuard.assert_local_isolation(
            "fed-reasoning-heavy", "https://api.openai.com/v1/chat"
        ) is True

    def test_local_signature_with_public_api_raises(self) -> None:
        with pytest.raises(PermissionError) as exc:
            AAALocalRuntimeGuard.assert_local_isolation(
                "fed-local-uncensored",
                "https://api.openai.com/v1/images/generations",
            )
        assert "LOCAL-RUNTIME VIOLATION" in str(exc.value)

    def test_local_signature_with_non_localhost_raises(self) -> None:
        with pytest.raises(PermissionError) as exc:
            AAALocalRuntimeGuard.assert_local_isolation(
                "fed-local-uncensored",
                "http://192.168.1.50:8188",
            )
        assert "not localhost" in str(exc.value)

    def test_local_signature_with_localhost_passes(self) -> None:
        # All LOCALHOST_PATTERNS should pass strict mode
        for pattern in ["127.0.0.1:8188", "localhost:5000", "::1:7860"]:
            assert AAALocalRuntimeGuard.assert_local_isolation(
                "fed-local-uncensored", f"http://{pattern}/api"
            ) is True

    def test_strict_false_relaxes_localhost_requirement(self) -> None:
        # With strict=False, non-localhost host passes (only blocklist enforced)
        assert AAALocalRuntimeGuard.assert_local_isolation(
            "fed-local-uncensored",
            "http://192.168.1.50:8188",
            strict=False,
        ) is True

    def test_validate_content_class_accepts_enum(self) -> None:
        for cc in CONTENT_CLASS_OPTIONS:
            assert AAALocalRuntimeGuard.validate_content_class(cc) is True

    def test_validate_content_class_rejects_garbage(self) -> None:
        with pytest.raises(ValueError):
            AAALocalRuntimeGuard.validate_content_class("lol_nsfw_unleashed")

    def test_public_api_blocklist_covers_major_providers(self) -> None:
        # Per F4 isolation, these MUST be in the blocklist
        required = [
            "api.openai.com",
            "dashscope.aliyuncs.com",
            "api.anthropic.com",
            "api.deepseek.com",
            "generativelanguage.googleapis.com",
        ]
        for domain in required:
            assert domain in PUBLIC_API_DOMAINS, f"missing {domain}"


# ─────────────────────────────────────────────────────────────────────────────
# Composition — LocalRuntimeRouter + LocalRuntimeGuard agree
# ─────────────────────────────────────────────────────────────────────────────


class TestComposition:
    def test_router_blocks_same_urls_as_guard(self) -> None:
        # LocalRuntimeRouter's URL check (the per-call endpoint blocklist)
        # and AAALocalRuntimeGuard's signature-based blocklist should
        # both reject the same public API endpoints.
        public_urls = [
            "https://api.openai.com/v1/images/generations",
            "https://dashscope.aliyuncs.com/v1/services/aigc",
        ]
        for url in public_urls:
            r = LocalRuntimeRouter(pre_check_service=False)
            d = r.route({"endpoint": url, "checkpoint": "pony-v6-xl"})
            assert d.preflight_passed is False
            # And the guard would also raise
            with pytest.raises(PermissionError):
                AAALocalRuntimeGuard.assert_local_isolation(
                    "fed-local-uncensored", url
                )

# ─────────────────────────────────────────────────────────────────────────────
# Path A+ — LedgerViewFilter (per-operator ACL)
# ─────────────────────────────────────────────────────────────────────────────


class TestLedgerViewFilter:
    def test_default_operator_sees_only_general(self) -> None:
        f = LedgerViewFilter()  # default = {general}
        assert f.show({"payload": {"content_classification": "general"}}).visible
        assert not f.show({"payload": {"content_classification": "sensitive"}}).visible
        assert not f.show({"payload": {"content_classification": "artistic"}}).visible

    def test_sovereign_sees_everything(self) -> None:
        f = LedgerViewFilter(SOVEREIGN_CLEARANCE)
        for cc in CONTENT_CLASS_OPTIONS:
            decision = f.show({"payload": {"content_classification": cc}})
            assert decision.visible, f"sovereign should see {cc}"

    def test_missing_content_class_defaults_to_general(self) -> None:
        f = LedgerViewFilter()
        # No content_classification field — defaults to "general", visible
        decision = f.show({"payload": {}})
        assert decision.visible
        assert decision.content_class == "general"

    def test_redaction_marks_payload(self) -> None:
        f = LedgerViewFilter()  # default {general}
        sensitive_receipt = {
            "ts": "2026-08-10T07:00:00Z",
            "payload": {
                "content_classification": "sensitive",
                "checkpoint": "pony-v6-xl",
                "prompt_hash": "abc123",
            },
        }
        redacted = f.redaction_view(sensitive_receipt)
        assert redacted["_redacted"] is True
        assert all(
            v == "[REDACTED_NEEDS_SOVEREIGN_CLEARANCE]"
            for v in redacted["payload"].values()
        )

    def test_filter_stream_omits_hidden(self) -> None:
        f = LedgerViewFilter()  # default {general}
        stream = [
            {"payload": {"content_classification": "general"}},
            {"payload": {"content_classification": "sensitive"}},
            {"payload": {"content_classification": "artistic"}},
            {"payload": {"content_classification": "general"}},
        ]
        visible = f.filter_stream(stream)
        # Only 2 "general" entries should be visible
        assert len(visible) == 2

    def test_redaction_preserves_metadata(self) -> None:
        f = LedgerViewFilter()
        receipt = {
            "ts": "2026-08-10T07:00:00Z",
            "actor_id": "333-AGI",
            "session_id": "abc",
            "payload": {"content_classification": "sensitive"},
        }
        redacted = f.redaction_view(receipt)
        # Metadata fields stay (so operators know sensitive work happened)
        assert redacted["ts"] == "2026-08-10T07:00:00Z"
        assert redacted["actor_id"] == "333-AGI"
        assert redacted["payload"]["content_classification"] == "[REDACTED_NEEDS_SOVEREIGN_CLEARANCE]"

    def test_filter_decision_is_frozen_dataclass(self) -> None:
        f = LedgerViewFilter()
        d = f.show({"payload": {"content_classification": "general"}})
        # Should be immutable
        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            d.visible = False  # type: ignore[misc]


# ─────────────────────────────────────────────────────────────────────────────
# Path A+ — TelemetryRing (TTL-bounded, sampled)
# ─────────────────────────────────────────────────────────────────────────────


class TestTelemetryRing:
    def test_empty_ring_drain(self) -> None:
        ring = TelemetryRing(maxlen=10, ttl_seconds=1.0, sample_rate=1.0)
        assert ring.drain_summary() == {"count": 0, "ttl_seconds": 1.0}
        assert ring.drain_expired() == []

    def test_sampling_rate_holds(self) -> None:
        # 1% sampling: with 1000 offers, expect ~10 accepted (allow 3-30)
        ring = TelemetryRing(maxlen=100_000, ttl_seconds=300.0, sample_rate=0.01)
        accepted = sum(
            1 for _ in range(1000)
            if ring.offer({"latency_ms": 100.0, "vram_gb": 12.0})
        )
        # Statistical: 1000 * 0.01 = 10, with high variance. Allow 1-50.
        assert 1 <= accepted <= 50

    def test_maxlen_caps_ring(self) -> None:
        # Sample rate 1.0, maxlen 5 — ring should hold at most 5
        ring = TelemetryRing(maxlen=5, ttl_seconds=300.0, sample_rate=1.0)
        for i in range(20):
            ring.offer({"latency_ms": float(i)})
        assert ring.drain_summary()["count"] == 5

    def test_drain_summary_returns_aggregates_not_raw(self) -> None:
        ring = TelemetryRing(maxlen=10, ttl_seconds=300.0, sample_rate=1.0)
        for ms in [100, 200, 300, 400, 500]:
            ring.offer({"latency_ms": float(ms), "vram_gb": 10.0})
        summary = ring.drain_summary()
        # No raw payload fields leak
        assert "samples" not in summary
        assert "raw" not in summary
        # Aggregate stats present
        assert summary["count"] == 5
        assert summary["latency_ms"]["max"] == 500.0
        # p50 should be ~300 (sorted: [100, 200, 300, 400, 500], middle = 300)
        assert summary["latency_ms"]["p50"] == 300.0

    def test_drain_expired_drops_old_samples(self) -> None:
        import time as _t
        ring = TelemetryRing(maxlen=100, ttl_seconds=0.05, sample_rate=1.0)
        ring.offer({"latency_ms": 100.0})
        # Wait > TTL
        _t.sleep(0.1)
        ring.offer({"latency_ms": 200.0})
        expired = ring.drain_expired()
        assert len(expired) == 1
        # The fresh sample is preserved
        assert ring.drain_summary()["count"] == 1

    def test_promote_expired_returns_aggregate(self) -> None:
        import time as _t
        ring = TelemetryRing(maxlen=100, ttl_seconds=0.05, sample_rate=1.0)
        ring.offer({"latency_ms": 100.0, "vram_gb": 8.0})
        _t.sleep(0.1)
        promoted = ring.promote_expired_to_canonical()
        assert "samples_in_window" in promoted
        assert promoted["samples_in_window"] == 1

    def test_promote_expired_empty_when_nothing_expired(self) -> None:
        ring = TelemetryRing(maxlen=100, ttl_seconds=300.0, sample_rate=1.0)
        ring.offer({"latency_ms": 100.0})
        promoted = ring.promote_expired_to_canonical()
        assert promoted == {}

    def test_ring_offer_returns_bool(self) -> None:
        ring = TelemetryRing(maxlen=10, ttl_seconds=300.0, sample_rate=0.0)
        # 0% sample rate: should always return False
        assert ring.offer({"latency_ms": 100.0}) is False
        ring2 = TelemetryRing(maxlen=10, ttl_seconds=300.0, sample_rate=1.0)
        assert ring2.offer({"latency_ms": 100.0}) is True


# ─────────────────────────────────────────────────────────────────────────────
# Path A+ — Composition: filter + ring work together
# ─────────────────────────────────────────────────────────────────────────────


class TestFilterRingComposition:
    def test_sovereign_sees_promoted_aggregates(self) -> None:
        """Sovereign uses both: view filter (sees sensitive) + ring (sees perf)."""
        view = LedgerViewFilter(SOVEREIGN_CLEARANCE)
        ring = TelemetryRing(maxlen=100, ttl_seconds=300.0, sample_rate=1.0)

        # Simulate: sensitive call + ring sample
        sensitive_receipt = {
            "payload": {"content_classification": "sensitive", "checkpoint": "pony"},
        }
        ring.offer({"latency_ms": 200.0, "vram_gb": 14.0})

        # Sovereign sees the sensitive receipt
        d = view.show(sensitive_receipt)
        assert d.visible

        # And the ring has a performance sample
        assert ring.drain_summary()["count"] == 1

    def test_default_operator_sees_summary_but_not_payload(self) -> None:
        """Default operator: sensitive payload hidden, aggregate stats visible."""
        view = LedgerViewFilter()  # default {general}
        ring = TelemetryRing(maxlen=100, ttl_seconds=300.0, sample_rate=1.0)

        ring.offer({"latency_ms": 200.0, "vram_gb": 14.0})

        sensitive_receipt = {
            "payload": {"content_classification": "sensitive"},
        }

        # Sensitive payload hidden
        d = view.show(sensitive_receipt)
        assert not d.visible
        redacted = view.redaction_view(sensitive_receipt)
        assert redacted["_redacted"] is True

        # Aggregate stats (no content) still visible
        summary = ring.drain_summary()
        assert summary["count"] == 1
        assert summary["latency_ms"]["p50"] == 200.0
