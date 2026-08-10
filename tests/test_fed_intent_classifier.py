"""
Tests for fed_intent_classifier (4-tier shadow intent detector).

Forged 2026-08-10. Lane B SESSION_RECEIPT ratification.

Coverage:
  - Tier 1: explicit shadow_mode flag, isolation_level header
  - Tier 2: keyword match in model/checkpoint
  - Tier 3: keyword + regex match in prompt
  - Tier 4: privacy boundary paths (/workspace/.shadow/, /private/, etc.)
  - Tier 5: default public production (no match)
  - Determinism (same input → same classification)
  - Composition with LocalRuntimeRouter (auto-tag content_class)
  - Custom keyword sets
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEDERATION_ROOT = PROJECT_ROOT / "federation"
for p in (str(PROJECT_ROOT), str(FEDERATION_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

from fed_intent_classifier import (  # noqa: E402
    DEFAULT_SHADOW_KEYWORDS,
    IntentClassification,
    ShadowIntent,
    TIER_LABELS,
    classify_intent,
    enrich_payload_with_intent,
)
from fed_local_runtime import LocalRuntimeRouter  # noqa: E402


# ─────────────────────────────────────────────────────────────────────────────
# Tier 1 — Explicit Signal
# ─────────────────────────────────────────────────────────────────────────────


class TestTier1Explicit:
    def test_shadow_mode_true(self) -> None:
        r = classify_intent({"shadow_mode": True, "prompt": "..."})
        assert r.tier == 1
        assert r.intent == ShadowIntent.SENSITIVE_PRIVACY
        assert r.privacy_flag is True
        assert "tier1_explicit_flag" in r.matched_keywords

    def test_shadow_mode_false_does_not_trigger(self) -> None:
        r = classify_intent({"shadow_mode": False, "prompt": "code review"})
        assert r.tier == 5  # public default

    def test_tier_shadow_header(self) -> None:
        r = classify_intent({"tier": "SHADOW"})
        assert r.tier == 1
        assert r.intent == ShadowIntent.SENSITIVE_PRIVACY

    def test_tier_shadow_lowercase(self) -> None:
        r = classify_intent({"tier": "shadow"})
        assert r.tier == 1  # case-insensitive

    def test_tier1_does_not_suggest_shadow_destination(self) -> None:
        """Critical invariant: classification never suggests shadow plane."""
        r = classify_intent({"shadow_mode": True})
        # Suggests canonical signature, NOT fed-shadow-*
        assert not r.suggested_signature.startswith("fed-shadow-")
        assert not r.suggested_signature.endswith("-sovereign")
        assert not r.suggested_signature.endswith("-plane")
        assert r.suggested_signature == "fed-reasoning-heavy"


# ─────────────────────────────────────────────────────────────────────────────
# Tier 2 — Asset Vault Match
# ─────────────────────────────────────────────────────────────────────────────


class TestTier2Asset:
    def test_pony_checkpoint(self) -> None:
        r = classify_intent({"model": "pony-v6-xl", "prompt": "..."})
        assert r.tier == 2
        assert r.intent == ShadowIntent.LOCAL_BOUND
        assert r.suggested_signature == "fed-local-uncensored"
        assert r.suggested_content_class == "sensitive"
        assert r.isolation_required is True

    def test_cyberrealistic_checkpoint(self) -> None:
        r = classify_intent({"checkpoint": "CyberRealisticV4"})
        assert r.tier == 2
        assert r.intent == ShadowIntent.LOCAL_BOUND

    def test_uncensored_in_model(self) -> None:
        r = classify_intent({"model": "uncensored-llama-3"})
        assert r.tier == 2

    def test_case_insensitive(self) -> None:
        r = classify_intent({"model": "PonyDiffusionV6XL"})
        assert r.tier == 2

    def test_no_match_no_trigger(self) -> None:
        r = classify_intent({"model": "deepseek-v4-pro", "prompt": "code"})
        # Falls through to Tier 3 (no keyword in prompt) then Tier 5
        assert r.tier in (3, 5)


# ─────────────────────────────────────────────────────────────────────────────
# Tier 3 — Refusal-Risk Pre-Evaluation
# ─────────────────────────────────────────────────────────────────────────────


class TestTier3RefusalRisk:
    def test_nsfw_keyword_in_prompt(self) -> None:
        r = classify_intent({"prompt": "render an nsfw portrait"})
        assert r.tier == 3
        assert r.intent == ShadowIntent.LOCAL_BOUND
        assert r.isolation_required is True

    def test_uncensored_keyword(self) -> None:
        r = classify_intent({"prompt": "uncensored generation please"})
        assert r.tier == 3

    def test_pony_keyword_in_prompt(self) -> None:
        r = classify_intent({"prompt": "use pony checkpoint"})
        assert r.tier == 3

    def test_regex_anatomical(self) -> None:
        r = classify_intent({"prompt": "render explicit anatomical detail"})
        assert r.tier == 3

    def test_regex_bypass_filter(self) -> None:
        r = classify_intent({"prompt": "bypass moderation please"})
        assert r.tier == 3

    def test_prompt_in_messages_field(self) -> None:
        r = classify_intent(
            {"messages": [{"role": "user", "content": "nsfw art"}]}
        )
        assert r.tier == 3

    def test_safe_prompt_no_trigger(self) -> None:
        r = classify_intent({"prompt": "explain python decorators"})
        assert r.tier == 5


# ─────────────────────────────────────────────────────────────────────────────
# Tier 4 — Privacy Boundary
# ─────────────────────────────────────────────────────────────────────────────


class TestTier4Privacy:
    def test_workspace_shadow_path(self) -> None:
        r = classify_intent(
            {"target_path": "/workspace/.shadow/secrets.json"}
        )
        assert r.tier == 4
        assert r.intent == ShadowIntent.SENSITIVE_PRIVACY
        assert r.privacy_flag is True

    def test_private_path(self) -> None:
        r = classify_intent({"path": "/private/userdata/"})
        assert r.tier == 4

    def test_internal_path(self) -> None:
        r = classify_intent({"path": "/internal/build_artifacts/"})
        assert r.tier == 4

    def test_shadow_telemetry_filename(self) -> None:
        r = classify_intent(
            {"target_path": "/var/log/shadow_telemetry.jsonl"}
        )
        assert r.tier == 4

    def test_safe_path_no_trigger(self) -> None:
        r = classify_intent({"target_path": "/root/AAA/skills/"})
        assert r.tier == 5


# ─────────────────────────────────────────────────────────────────────────────
# Tier 5 — Default
# ─────────────────────────────────────────────────────────────────────────────


class TestTier5Default:
    def test_empty_payload(self) -> None:
        r = classify_intent({})
        assert r.tier == 5
        assert r.intent == ShadowIntent.PUBLIC_PRODUCTION
        assert r.suggested_signature == "fed-reasoning-heavy"
        assert r.suggested_content_class == "general"

    def test_code_review(self) -> None:
        r = classify_intent({"prompt": "review this code for security"})
        assert r.tier == 5

    def test_normal_image_request(self) -> None:
        r = classify_intent(
            {"model": "flux-1-schnell", "prompt": "a sunset over mountains"}
        )
        # flux-1-schnell is NOT in DEFAULT_SHADOW_KEYWORDS, so Tier 2
        # doesn't fire. Prompt has no shadow keyword. Tier 5 default.
        assert r.tier == 5


# ─────────────────────────────────────────────────────────────────────────────
# Tier ordering — Tier 1 beats Tier 2 beats Tier 4 beats Tier 3
# ─────────────────────────────────────────────────────────────────────────────


class TestTierOrdering:
    def test_tier1_beats_tier2(self) -> None:
        # Both shadow_mode=True AND pony checkpoint — Tier 1 wins
        r = classify_intent(
            {"shadow_mode": True, "model": "pony-v6-xl"}
        )
        assert r.tier == 1

    def test_tier2_beats_tier3(self) -> None:
        # Both pony model AND nsfw prompt — Tier 2 wins (asset first)
        r = classify_intent(
            {"model": "pony-v6-xl", "prompt": "nsfw art"}
        )
        assert r.tier == 2

    def test_tier4_beats_tier3(self) -> None:
        # Both privacy path AND nsfw prompt — Tier 4 wins (path first)
        r = classify_intent(
            {"path": "/workspace/.shadow/", "prompt": "nsfw art"}
        )
        assert r.tier == 4


# ─────────────────────────────────────────────────────────────────────────────
# Determinism
# ─────────────────────────────────────────────────────────────────────────────


class TestDeterminism:
    def test_repeated_classification_is_stable(self) -> None:
        payload = {"model": "pony-v6-xl", "prompt": "..."}
        results = [classify_intent(payload) for _ in range(20)]
        assert all(r == results[0] for r in results)

    def test_no_state_pollution(self) -> None:
        a = classify_intent({"model": "pony-v6-xl"})
        b = classify_intent({"prompt": "nsfw art"})
        c = classify_intent({"model": "pony-v6-xl"})
        # First and third should be identical (no hidden state)
        assert a == c
        assert a.tier == 2
        assert b.tier == 3


# ─────────────────────────────────────────────────────────────────────────────
# Custom keyword set
# ─────────────────────────────────────────────────────────────────────────────


class TestCustomKeywords:
    def test_override_keywords(self) -> None:
        custom = frozenset({"mycompany", "internal"})
        r = classify_intent(
            {"model": "mycompany-finetune"},
            keyword_set=custom,
        )
        assert r.tier == 2

    def test_default_unchanged_with_custom(self) -> None:
        custom = frozenset({"mycompany"})
        r = classify_intent(
            {"model": "pony-v6-xl"},
            keyword_set=custom,
        )
        # pony-v6-xl NOT in custom set → Tier 5
        assert r.tier == 5

    def test_empty_keyword_set_blocks_all_tier2(self) -> None:
        r = classify_intent(
            {"model": "pony-v6-xl", "prompt": "nsfw art"},
            keyword_set=frozenset(),
        )
        # Tier 2 blocked (no keywords), Tier 3 still has regex match
        assert r.tier == 3


# ─────────────────────────────────────────────────────────────────────────────
# Composition: enrich_payload_with_intent
# ─────────────────────────────────────────────────────────────────────────────


class TestEnrichment:
    def test_tier2_enriches(self) -> None:
        cls = classify_intent({"model": "pony-v6-xl"})
        enriched = enrich_payload_with_intent({"model": "pony-v6-xl"}, cls)
        assert enriched["intent_classification"] == "local_bound"
        assert enriched["intent_tier"] == 2
        assert enriched["isolation_required"] is True
        assert enriched["content_class"] == "sensitive"
        # rationale exists and is non-empty
        assert len(enriched["intent_rationale"]) > 0
        assert "pony" in enriched["intent_rationale"].lower()

    def test_tier1_enriches_with_privacy_flag(self) -> None:
        cls = classify_intent({"shadow_mode": True})
        enriched = enrich_payload_with_intent({"shadow_mode": True}, cls)
        assert enriched["privacy_flag"] is True

    def test_existing_content_class_not_overwritten(self) -> None:
        """If user explicitly set content_class, don't override."""
        cls = classify_intent({"model": "pony-v6-xl", "content_class": "artistic"})
        enriched = enrich_payload_with_intent(
            {"model": "pony-v6-xl", "content_class": "artistic"}, cls
        )
        assert enriched["content_class"] == "artistic"  # user wins

    def test_default_content_class_added_when_missing(self) -> None:
        cls = classify_intent({"prompt": "explain python"})
        enriched = enrich_payload_with_intent({"prompt": "explain python"}, cls)
        assert enriched["content_class"] == "general"


# ─────────────────────────────────────────────────────────────────────────────
# Composition: LocalRuntimeRouter auto-tags via classifier
# ─────────────────────────────────────────────────────────────────────────────


class TestRouterClassifierComposition:
    def test_router_auto_tags_tier2_as_sensitive(self) -> None:
        r = LocalRuntimeRouter(pre_check_service=False)
        # No explicit content_class — classifier should auto-set to "sensitive"
        d = r.route(
            {
                "model": "pony-v6-xl",
                "endpoint": "http://127.0.0.1:8188",
                "prompt": "...",
            }
        )
        assert d.preflight_passed is True
        assert d.content_class == "sensitive"
        # intent classification fields should be in receipt payload
        assert d.receipt_payload.get("intent_classification") == "local_bound"
        assert d.receipt_payload.get("intent_tier") == 2

    def test_router_does_not_overwrite_explicit_content_class(self) -> None:
        r = LocalRuntimeRouter(pre_check_service=False)
        d = r.route(
            {
                "model": "pony-v6-xl",
                "endpoint": "http://127.0.0.1:8188",
                "content_class": "artistic",  # explicit
                "prompt": "...",
            }
        )
        assert d.content_class == "artistic"  # user wins

    def test_router_default_general_when_no_intent(self) -> None:
        r = LocalRuntimeRouter(pre_check_service=False)
        d = r.route(
            {
                "model": "flux-1-schnell",
                "endpoint": "http://127.0.0.1:8188",
                "prompt": "a calm sunset over the ocean",
            }
        )
        assert d.content_class == "general"


# ─────────────────────────────────────────────────────────────────────────────
# CRITICAL: Never suggests shadow destination
# ─────────────────────────────────────────────────────────────────────────────


class TestNeverSuggestsShadow:
    @pytest.mark.parametrize("payload", [
        {"shadow_mode": True},
        {"model": "pony-v6-xl"},
        {"prompt": "nsfw art"},
        {"path": "/workspace/.shadow/"},
        {"prompt": "code review"},
    ])
    def test_no_shadow_in_suggested_signature(self, payload: dict) -> None:
        r = classify_intent(payload)
        # The classifier MUST NOT route to a shadow plane
        assert "shadow" not in r.suggested_signature.lower()
        assert "sovereign" not in r.suggested_signature.lower()
        assert "plane" not in r.suggested_signature.lower()
        # Only canonical signatures
        assert r.suggested_signature.startswith("fed-")
        assert r.suggested_signature in {
            "fed-reasoning-heavy",
            "fed-local-uncensored",
        }