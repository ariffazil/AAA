"""
Tests for the Latent-Aware Router (fed_router_v2).

Forged 2026-08-10. Lane B SESSION_RECEIPT ratification.

Coverage:
  - Modality inference (text / pixel / mixed / audio)
  - Task class inference (generate / inspect / repair / plan)
  - Capability signature resolution (registry hits + misses)
  - Closed-loop repair dispatch (PERSIST / REPAIR / ESCALATE)
  - Edge cases (empty payload, low fidelity no defect, attempt exhaustion)
  - Determinism (same payload → same classification, no IO)

All tests are pure logic — no GPU, no torch, no CUDA, no network.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure AAA root on sys.path with priority.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Latent-Aware Router lives at /root/AAA/federation/fed_router_v2.py
FEDERATION_ROOT = PROJECT_ROOT / "federation"
if str(FEDERATION_ROOT) not in sys.path:
    sys.path.insert(0, str(FEDERATION_ROOT))

from fed_router_v2 import (  # noqa: E402
    DEFAULT_FIDELITY_THRESHOLD,
    BoundingBox,
    LatentAwareRouter,
    Modality,
    RepairDecision,
    TaskClass,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture
def router() -> LatentAwareRouter:
    return LatentAwareRouter()


# ─────────────────────────────────────────────────────────────────────────────
# Modality inference
# ─────────────────────────────────────────────────────────────────────────────


class TestModalityInference:
    def test_text_only(self, router: LatentAwareRouter) -> None:
        m, _ = router.classify({"prompt": "plan my day"})
        assert m == Modality.TEXT

    def test_pixel_only(self, router: LatentAwareRouter) -> None:
        m, _ = router.classify({"image_uri": "s3://x.png"})
        assert m == Modality.PIXEL

    def test_mixed(self, router: LatentAwareRouter) -> None:
        m, _ = router.classify(
            {"image_uri": "s3://x.png", "prompt": "describe this"}
        )
        assert m == Modality.MIXED

    def test_audio(self, router: LatentAwareRouter) -> None:
        m, _ = router.classify({"audio": "voice.wav"})
        assert m == Modality.AUDIO

    def test_empty_defaults_to_text(self, router: LatentAwareRouter) -> None:
        m, _ = router.classify({})
        assert m == Modality.TEXT

    def test_latent_key_triggers_pixel(self, router: LatentAwareRouter) -> None:
        m, _ = router.classify({"latent": "tensor", "prompt": "denoise"})
        assert m == Modality.MIXED


# ─────────────────────────────────────────────────────────────────────────────
# Task class inference (intent + heuristic)
# ─────────────────────────────────────────────────────────────────────────────


class TestTaskClassInference:
    def test_explicit_intent_wins(self, router: LatentAwareRouter) -> None:
        _, tc = router.classify(
            {"prompt": "plan a thing", "intent": "generate"}
        )
        assert tc == TaskClass.GENERATE

    def test_invalid_explicit_intent_falls_back_to_heuristic(
        self, router: LatentAwareRouter
    ) -> None:
        _, tc = router.classify(
            {"prompt": "fix the broken image", "intent": "frobnicate"}
        )
        assert tc == TaskClass.REPAIR

    def test_generate_hint(self, router: LatentAwareRouter) -> None:
        _, tc = router.classify({"prompt": "render a sunset"})
        assert tc == TaskClass.GENERATE

    def test_inspect_hint(self, router: LatentAwareRouter) -> None:
        _, tc = router.classify({"prompt": "describe what's in this image"})
        assert tc == TaskClass.INSPECT

    def test_repair_hint(self, router: LatentAwareRouter) -> None:
        _, tc = router.classify({"prompt": "fix the distorted hand"})
        assert tc == TaskClass.REPAIR

    def test_plan_hint(self, router: LatentAwareRouter) -> None:
        _, tc = router.classify({"prompt": "design a microservice"})
        assert tc == TaskClass.PLAN

    def test_no_prompt_defaults_to_plan(self, router: LatentAwareRouter) -> None:
        # Per fed_router.py default: most general capability wins
        _, tc = router.classify({"image_uri": "x.png"})
        assert tc == TaskClass.PLAN

    def test_repair_beats_inspect_in_heuristic_order(
        self, router: LatentAwareRouter
    ) -> None:
        # "repair" check should win over "inspect" because REPAIR_HINTS
        # is checked first in _infer_task_class — this is a stated
        # design choice (defects matter more than descriptions).
        _, tc = router.classify({"prompt": "inspect and repair this image"})
        assert tc == TaskClass.REPAIR


# ─────────────────────────────────────────────────────────────────────────────
# Capability signature resolution
# ─────────────────────────────────────────────────────────────────────────────


class TestResolve:
    def test_pixel_generate_maps_to_diffusion(self, router: LatentAwareRouter) -> None:
        sig = router.resolve(Modality.PIXEL, TaskClass.GENERATE)
        assert sig == "fed-image-generation"

    def test_pixel_inspect_maps_to_grounded_vlm(self, router: LatentAwareRouter) -> None:
        sig = router.resolve(Modality.PIXEL, TaskClass.INSPECT)
        assert sig == "fed-grounded-vision"

    def test_pixel_repair_maps_to_inpainting(self, router: LatentAwareRouter) -> None:
        sig = router.resolve(Modality.PIXEL, TaskClass.REPAIR)
        assert sig == "fed-inpainting"

    def test_text_plan_maps_to_reasoning(self, router: LatentAwareRouter) -> None:
        sig = router.resolve(Modality.TEXT, TaskClass.PLAN)
        assert sig == "fed-reasoning-heavy"

    def test_audio_maps_to_voice(self, router: LatentAwareRouter) -> None:
        sig = router.resolve(Modality.AUDIO, TaskClass.PLAN)
        assert sig == "fed-realtime-voice"

    def test_missing_combination_returns_none(
        self, router: LatentAwareRouter
    ) -> None:
        # TEXT + REPAIR has no entry in registry
        sig = router.resolve(Modality.TEXT, TaskClass.REPAIR)
        assert sig is None


class TestResolvePayload:
    def test_full_pipeline_returns_metadata(
        self, router: LatentAwareRouter
    ) -> None:
        # image_uri + prompt together → MIXED (correct per classifier)
        result = router.resolve_payload(
            {"image_uri": "x.png", "prompt": "generate a sunset"}
        )
        assert result == {
            "modality": "mixed",
            "task_class": "generate",
            "signature": "fed-image-generation",
            "registry_hit": True,
        }

    def test_registry_miss_flagged(self, router: LatentAwareRouter) -> None:
        result = router.resolve_payload(
            {"prompt": "repair the text", "intent": "repair"}
        )
        assert result["signature"] is None
        assert result["registry_hit"] is False


# ─────────────────────────────────────────────────────────────────────────────
# Closed-loop repair dispatch
# ─────────────────────────────────────────────────────────────────────────────


class TestEvaluateAndRepair:
    def test_high_fidelity_persists(self, router: LatentAwareRouter) -> None:
        decision = router.evaluate_and_repair(fidelity_score=0.95)
        assert decision.action == "PERSIST"
        assert decision.signature == "fed-grounded-vision"

    def test_low_fidelity_with_defect_repairs(self, router: LatentAwareRouter) -> None:
        defect = BoundingBox(0.2, 0.3, 0.1, 0.1, label="hand")
        decision = router.evaluate_and_repair(
            fidelity_score=0.75, defects=[defect], attempt=1
        )
        assert decision.action == "REPAIR"
        assert decision.signature == "fed-inpainting"
        assert decision.defect is defect
        assert decision.attempt == 1

    def test_low_fidelity_no_defect_persists(self, router: LatentAwareRouter) -> None:
        # P_quality low but VLM found no localized defect — re-roll not useful
        decision = router.evaluate_and_repair(fidelity_score=0.70, defects=[])
        assert decision.action == "PERSIST"

    def test_exhausted_attempts_escalate(self, router: LatentAwareRouter) -> None:
        defect = BoundingBox(0.1, 0.1, 0.05, 0.05, label="face")
        decision = router.evaluate_and_repair(
            fidelity_score=0.50, defects=[defect], attempt=3
        )
        assert decision.action == "ESCALATE"
        assert decision.signature == "fed-judge-deputy"
        assert decision.attempt == 3

    def test_at_threshold_persists(self, router: LatentAwareRouter) -> None:
        # Exactly at threshold (0.88) → persist
        decision = router.evaluate_and_repair(
            fidelity_score=DEFAULT_FIDELITY_THRESHOLD, defects=[]
        )
        assert decision.action == "PERSIST"

    def test_just_below_threshold_repairs(self, router: LatentAwareRouter) -> None:
        defect = BoundingBox(0.5, 0.5, 0.1, 0.1, label="eye")
        decision = router.evaluate_and_repair(
            fidelity_score=DEFAULT_FIDELITY_THRESHOLD - 0.001,
            defects=[defect],
        )
        assert decision.action == "REPAIR"

    def test_custom_threshold_respected(self) -> None:
        custom = LatentAwareRouter(fidelity_threshold=0.95)
        decision = custom.evaluate_and_repair(
            fidelity_score=0.90, defects=[BoundingBox(0, 0, 0.1, 0.1)]
        )
        assert decision.action == "REPAIR"

    def test_custom_max_attempts(self) -> None:
        router = LatentAwareRouter(max_repair_attempts=2)
        defect = BoundingBox(0.5, 0.5, 0.1, 0.1, label="x")
        # attempt=2 with max=2 → ESCALATE
        decision = router.evaluate_and_repair(
            fidelity_score=0.50, defects=[defect], attempt=2
        )
        assert decision.action == "ESCALATE"

    def test_repair_attempt_increments_correctly(
        self, router: LatentAwareRouter
    ) -> None:
        defect = BoundingBox(0.5, 0.5, 0.1, 0.1, label="leg")
        d1 = router.evaluate_and_repair(
            fidelity_score=0.75, defects=[defect], attempt=1
        )
        d2 = router.evaluate_and_repair(
            fidelity_score=0.80, defects=[defect], attempt=2
        )
        assert d1.attempt == 1
        assert d2.attempt == 2


# ─────────────────────────────────────────────────────────────────────────────
# Determinism — same input always → same classification
# ─────────────────────────────────────────────────────────────────────────────


class TestDeterminism:
    def test_repeated_classification_is_stable(
        self, router: LatentAwareRouter
    ) -> None:
        payload = {"image_uri": "x.png", "prompt": "render a sunset"}
        results = [router.resolve_payload(payload) for _ in range(20)]
        assert all(r == results[0] for r in results)


# ─────────────────────────────────────────────────────────────────────────────
# BoundingBox serialization
# ─────────────────────────────────────────────────────────────────────────────


class TestBoundingBox:
    def test_as_dict_roundtrip(self) -> None:
        bb = BoundingBox(0.1, 0.2, 0.3, 0.4, label="hand", confidence=0.88)
        d = bb.as_dict()
        assert d == {
            "x": 0.1,
            "y": 0.2,
            "w": 0.3,
            "h": 0.4,
            "label": "hand",
            "confidence": 0.88,
        }
        assert isinstance(d["label"], str)
        assert isinstance(d["confidence"], float)


# ─────────────────────────────────────────────────────────────────────────────
# Composition: full loop classify → resolve → evaluate
# ─────────────────────────────────────────────────────────────────────────────


class TestEndToEndLoop:
    def test_generate_then_low_fidelity_repairs(
        self, router: LatentAwareRouter
    ) -> None:
        # 1. Planner receives user intent
        plan_payload = {
            "image_uri": "sketch.png",
            "prompt": "generate a portrait of arif",
        }
        meta = router.resolve_payload(plan_payload)
        assert meta["signature"] == "fed-image-generation"

        # 2. Renderer runs DiT, returns image bytes
        # (caller does the actual diffusion; we just simulate scoring)
        fidelity_score = 0.72  # below threshold
        defects = [BoundingBox(0.4, 0.3, 0.1, 0.15, label="hand")]

        # 3. Inspector feeds into router's repair loop
        decision = router.evaluate_and_repair(
            fidelity_score=fidelity_score, defects=defects, attempt=1
        )
        assert decision.action == "REPAIR"
        assert decision.signature == "fed-inpainting"

        # 4. Repair succeeds, second evaluation
        decision2 = router.evaluate_and_repair(
            fidelity_score=0.95, defects=[], attempt=1
        )
        assert decision2.action == "PERSIST"

    def test_generate_then_persistent_failure_escalates(
        self, router: LatentAwareRouter
    ) -> None:
        defect = BoundingBox(0.4, 0.3, 0.1, 0.15, label="face")
        # attempt 1: REPAIR
        d1 = router.evaluate_and_repair(0.72, [defect], attempt=1)
        # attempt 2: still REPAIR
        d2 = router.evaluate_and_repair(0.78, [defect], attempt=2)
        # attempt 3: ESCALATE (max attempts reached)
        d3 = router.evaluate_and_repair(0.65, [defect], attempt=3)
        assert d1.action == "REPAIR"
        assert d2.action == "REPAIR"
        assert d3.action == "ESCALATE"