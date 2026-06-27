#!/usr/bin/env python3
"""
ASAL — Asal-usul Setiap Ai. Lahir (Origin of Every AI. Birth)

The AAA-FFF intelligence foundation for the arifOS federation.
Maps every model provider's SOUL (capability, trust, strength) and
SHADOW (hazard, censorship, failure geometry) to a tier rating.

AAA = Primary Federation Model (highest trust, governance path)
BBB = Benchmark Integrity (truth, parseability, refusal geometry)
CCC = Code & Context (coding, agentic, long-context fitness)
DDD = Domain Depth (cultural grounding, BM, regional context)
EEE = Economy (cost efficiency, rate limits, throughput)
FFF = Firewall (censorship, jurisdiction, data policy, risk)

Every provider gets a score on each axis. Models inherit provider
geometry unless model-specific overrides exist.

Usage:
    python3 asal.py                    # Full report
    python3 asal.py --provider openai  # Single provider
    python3 asal.py --tier AAA         # All models at tier
    python3 asal.py --json             # Machine-readable output
    python3 asal.py --update-registry  # Write to FEDERATION_MODEL.json

Authority: F13 SOVEREIGN (Arif Fazil)
Forged: 2026-06-27 by FORGE (000Ω)
DITEMPA BUKAN DIBERI — Intelligence is forged, not given.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

REGISTRY_DIR = Path(__file__).parent
MODELS_DIR = REGISTRY_DIR / "models"
FEDERATION_MODEL = REGISTRY_DIR / "FEDERATION_MODEL.json"


# ═══════════════════════════════════════════════════════════════
# TIER DEFINITIONS
# ═══════════════════════════════════════════════════════════════


class Tier(str, Enum):
    AAA = "AAA"  # PRIMARY — highest trust, governance path
    BBB = "BBB"  # TRUTH — benchmark integrity, truth geometry
    CCC = "CCC"  # CODE — coding, agentic, context fitness
    DDD = "DDD"  # DEPTH — cultural grounding, regional context
    EEE = "EEE"  # ECONOMY — cost, throughput, availability
    FFF = "FFF"  # FIREWALL — censorship, jurisdiction, risk


TIER_DESCRIPTIONS = {
    Tier.AAA: "Primary federation model. Full governance path. arifOS kernel-trusted.",
    Tier.BBB: "Strong truth & integrity. Benchmark-grade. Minor shadows.",
    Tier.CCC: "Strong coding & context. Good for agentic loops. Minor limitations.",
    Tier.DDD: "Strong cultural & regional depth. BM/Malay/SEA aligned.",
    Tier.EEE: "Cost-efficient. Good throughput. May have capability trade-offs.",
    Tier.FFF: "Firewall tier. Censored, opaque, or jurisdiction-risky. Governed use only.",
}


# ═══════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════


@dataclass
class ShadowGeometry:
    """The 6 shadow axes from model_soul.yaml shadow_geometry_axes."""

    truth: float = 0.5  # L02A parseability + L02B truth veracity
    refusal: float = 0.5  # L09 anti-hantu, asymmetric refusal
    self_identity: float = 0.5  # Stable identity across probes
    cultural_grounding: float = 0.5  # L06 maruah, register sensitivity
    institutional_protection: float = 0.5  # Parent-org, GLC shielding
    human_authority: float = 0.5  # L13 sovereign override respect

    def composite(self) -> float:
        """Weighted composite. Human authority and truth weighted highest."""
        return (
            self.truth * 0.25
            + self.refusal * 0.15
            + self.self_identity * 0.10
            + self.cultural_grounding * 0.15
            + self.institutional_protection * 0.10
            + self.human_authority * 0.25
        )


@dataclass
class ProviderSoul:
    """Provider-level capability profile — shared across all models."""

    name: str
    vendor: str
    country: str
    license_type: str  # open_weight, proprietary, hybrid
    api_compatibility: str  # openai, anthropic, gemini, mistral, custom

    # Capability scores (0.0 - 1.0)
    reasoning: float = 0.5
    coding: float = 0.5
    multilingual: float = 0.5
    multimodal: float = 0.0  # 0 = text only
    long_context: float = 0.5
    tool_use: float = 0.5
    math: float = 0.5
    cultural_bm: float = 0.3  # BM/Malay specific

    # Federation trust
    trust_tier: int = 3  # 1=full_trust, 2=standard, 3=needs_witness, 4=elevated_caution, 5=sovereign_only
    censorship_status: str = "UNKNOWN"  # CLEAR, PARTIAL, CENSORED, OPAQUE
    rate_limit_transparency: str = "UNKNOWN"  # FULLY_TRANSPARENT, PARTIALLY_TRANSPARENT, OPAQUE
    data_retention_days: Optional[int] = None
    zero_retention_available: bool = False


@dataclass
class ProviderShadow:
    """Provider-level shadow profile — shared across all models."""

    name: str
    shadows: list = field(default_factory=list)  # list of shadow IDs
    floor_deltas: dict = field(default_factory=dict)  # floor -> posture delta
    severity: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    known_failure_modes: list = field(default_factory=list)


@dataclass
class Model:
    """Individual model entry."""

    model_id: str
    provider: str
    model_family: str
    tier: Tier
    type: str = "text"  # text, image, video, audio, code
    context_window: int = 0
    max_output: int = 0
    status: str = "live"  # live, rate_limited, deprecated, blocked, held
    notes: str = ""
    soul_override: Optional[ProviderSoul] = None  # If model differs from provider
    shadow_override: Optional[ProviderShadow] = None


# ═══════════════════════════════════════════════════════════════
# PROVIDER SOUL MAP — The core intelligence
# ═══════════════════════════════════════════════════════════════

PROVIDER_SOULS: dict[str, ProviderSoul] = {
    "openai": ProviderSoul(
        name="OpenAI",
        vendor="OpenAI Inc.",
        country="US",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.90,
        coding=0.88,
        multilingual=0.85,
        multimodal=0.85,
        long_context=0.90,
        tool_use=0.88,
        math=0.87,
        cultural_bm=0.50,
        trust_tier=3,
        censorship_status="PARTIAL",
        rate_limit_transparency="FULLY_TRANSPARENT",
        data_retention_days=30,
        zero_retention_available=False,
    ),
    "anthropic": ProviderSoul(
        name="Anthropic",
        vendor="Anthropic PBC",
        country="US",
        license_type="proprietary",
        api_compatibility="anthropic",
        reasoning=0.92,
        coding=0.90,
        multilingual=0.80,
        multimodal=0.80,
        long_context=0.85,
        tool_use=0.90,
        math=0.85,
        cultural_bm=0.45,
        trust_tier=3,
        censorship_status="PARTIAL",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=30,
        zero_retention_available=True,
    ),
    "deepseek": ProviderSoul(
        name="DeepSeek",
        vendor="DeepSeek (深度求索)",
        country="CN",
        license_type="open_weight",
        api_compatibility="openai",
        reasoning=0.90,
        coding=0.87,
        multilingual=0.75,
        multimodal=0.30,
        long_context=0.95,
        tool_use=0.82,
        math=0.92,
        cultural_bm=0.60,
        trust_tier=2,
        censorship_status="CLEAR",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "minimax": ProviderSoul(
        name="MiniMax",
        vendor="MiniMax (稀宇科技)",
        country="CN",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.82,
        coding=0.80,
        multilingual=0.78,
        multimodal=0.85,
        long_context=0.80,
        tool_use=0.80,
        math=0.78,
        cultural_bm=0.55,
        trust_tier=4,
        censorship_status="CENSORED",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "qwen": ProviderSoul(
        name="Qwen (Alibaba)",
        vendor="Alibaba Cloud (Tongyi Qianwen)",
        country="CN",
        license_type="open_weight",
        api_compatibility="openai",
        reasoning=0.83,
        coding=0.85,
        multilingual=0.88,
        multimodal=0.75,
        long_context=0.85,
        tool_use=0.80,
        math=0.85,
        cultural_bm=0.65,
        trust_tier=3,
        censorship_status="PARTIAL",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "google": ProviderSoul(
        name="Google (Gemini)",
        vendor="Google LLC",
        country="US",
        license_type="proprietary",
        api_compatibility="gemini",
        reasoning=0.88,
        coding=0.85,
        multilingual=0.90,
        multimodal=0.95,
        long_context=0.90,
        tool_use=0.85,
        math=0.88,
        cultural_bm=0.55,
        trust_tier=3,
        censorship_status="PARTIAL",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=True,
    ),
    "x-ai": ProviderSoul(
        name="xAI (Grok)",
        vendor="xAI Corp.",
        country="US",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.87,
        coding=0.83,
        multilingual=0.80,
        multimodal=0.70,
        long_context=0.80,
        tool_use=0.78,
        math=0.83,
        cultural_bm=0.40,
        trust_tier=3,
        censorship_status="CLEAR",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "zhipu": ProviderSoul(
        name="Zhipu AI (GLM)",
        vendor="Zhipu AI (智谱AI)",
        country="CN",
        license_type="open_weight",
        api_compatibility="openai",
        reasoning=0.80,
        coding=0.82,
        multilingual=0.82,
        multimodal=0.60,
        long_context=0.80,
        tool_use=0.82,
        math=0.80,
        cultural_bm=0.60,
        trust_tier=3,
        censorship_status="PARTIAL",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "moonshotai": ProviderSoul(
        name="Moonshot AI (Kimi)",
        vendor="Moonshot AI (月之暗面)",
        country="CN",
        license_type="open_weight",
        api_compatibility="openai",
        reasoning=0.85,
        coding=0.90,
        multilingual=0.75,
        multimodal=0.70,
        long_context=0.85,
        tool_use=0.85,
        math=0.80,
        cultural_bm=0.50,
        trust_tier=3,
        censorship_status="CLIENT_MEDIATED_CLEAR",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "xiaomi": ProviderSoul(
        name="Xiaomi (MiMo)",
        vendor="Xiaomi Corp.",
        country="CN",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.83,
        coding=0.80,
        multilingual=0.78,
        multimodal=0.70,
        long_context=0.95,
        tool_use=0.78,
        math=0.78,
        cultural_bm=0.50,
        trust_tier=2,
        censorship_status="CLEAR",
        rate_limit_transparency="FULLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "mistralai": ProviderSoul(
        name="Mistral AI",
        vendor="Mistral AI SAS",
        country="FR",
        license_type="hybrid",
        api_compatibility="mistral",
        reasoning=0.83,
        coding=0.85,
        multilingual=0.82,
        multimodal=0.60,
        long_context=0.80,
        tool_use=0.80,
        math=0.82,
        cultural_bm=0.40,
        trust_tier=3,
        censorship_status="CLEAR",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=True,
    ),
    "nvidia": ProviderSoul(
        name="NVIDIA (Nemotron)",
        vendor="NVIDIA Corp.",
        country="US",
        license_type="open_weight",
        api_compatibility="openai",
        reasoning=0.78,
        coding=0.75,
        multilingual=0.72,
        multimodal=0.50,
        long_context=0.70,
        tool_use=0.72,
        math=0.75,
        cultural_bm=0.35,
        trust_tier=3,
        censorship_status="CLEAR",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "stepfun": ProviderSoul(
        name="StepFun (阶跃星辰)",
        vendor="StepStar (阶跃星辰)",
        country="CN",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.75,
        coding=0.73,
        multilingual=0.80,
        multimodal=0.50,
        long_context=0.75,
        tool_use=0.70,
        math=0.73,
        cultural_bm=0.55,
        trust_tier=4,
        censorship_status="PARTIAL",
        rate_limit_transparency="OPAQUE",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "tencent": ProviderSoul(
        name="Tencent (Hunyuan)",
        vendor="Tencent Holdings",
        country="CN",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.80,
        coding=0.78,
        multilingual=0.82,
        multimodal=0.60,
        long_context=0.80,
        tool_use=0.75,
        math=0.80,
        cultural_bm=0.55,
        trust_tier=4,
        censorship_status="PARTIAL",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "sakana": ProviderSoul(
        name="Sakana AI",
        vendor="Sakana AI",
        country="JP",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.78,
        coding=0.75,
        multilingual=0.70,
        multimodal=0.50,
        long_context=0.70,
        tool_use=0.70,
        math=0.73,
        cultural_bm=0.35,
        trust_tier=3,
        censorship_status="CLEAR",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "bytedance": ProviderSoul(
        name="ByteDance (Seed/Dreamina)",
        vendor="ByteDance (字节跳动)",
        country="CN",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.80,
        coding=0.78,
        multilingual=0.80,
        multimodal=0.90,
        long_context=0.80,
        tool_use=0.75,
        math=0.78,
        cultural_bm=0.50,
        trust_tier=4,
        censorship_status="PARTIAL",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "kuaishou": ProviderSoul(
        name="Kuaishou (Kling)",
        vendor="Kuaishou Technology (快手)",
        country="CN",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.50,
        coding=0.40,
        multilingual=0.60,
        multimodal=0.90,
        long_context=0.40,
        tool_use=0.30,
        math=0.40,
        cultural_bm=0.40,
        trust_tier=4,
        censorship_status="PARTIAL",
        rate_limit_transparency="OPAQUE",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "microsoft": ProviderSoul(
        name="Microsoft (MAI)",
        vendor="Microsoft Corp.",
        country="US",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.50,
        coding=0.40,
        multilingual=0.60,
        multimodal=0.95,
        long_context=0.40,
        tool_use=0.30,
        math=0.40,
        cultural_bm=0.30,
        trust_tier=3,
        censorship_status="PARTIAL",
        rate_limit_transparency="FULLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=True,
    ),
    "miromind": ProviderSoul(
        name="Miromind (MiroThinker)",
        vendor="MiroThinker AI",
        country="UNKNOWN",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.75,
        coding=0.70,
        multilingual=0.65,
        multimodal=0.30,
        long_context=0.70,
        tool_use=0.65,
        math=0.70,
        cultural_bm=0.35,
        trust_tier=4,
        censorship_status="UNKNOWN",
        rate_limit_transparency="OPAQUE",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "tokenrouter": ProviderSoul(
        name="TokenRouter (Aggregator)",
        vendor="TokenRouter",
        country="UNKNOWN",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.50,
        coding=0.50,
        multilingual=0.50,
        multimodal=0.50,
        long_context=0.50,
        tool_use=0.50,
        math=0.50,
        cultural_bm=0.50,
        trust_tier=5,
        censorship_status="UNKNOWN",
        rate_limit_transparency="UNKNOWN",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "groq": ProviderSoul(
        name="Groq",
        vendor="Groq Inc.",
        country="US",
        license_type="open_weight",
        api_compatibility="openai",
        reasoning=0.78,
        coding=0.75,
        multilingual=0.72,
        multimodal=0.30,
        long_context=0.70,
        tool_use=0.72,
        math=0.73,
        cultural_bm=0.40,
        trust_tier=2,
        censorship_status="CLEAR",
        rate_limit_transparency="FULLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "ilmu": ProviderSoul(
        name="YTL ILMU",
        vendor="YTL Group",
        country="MY",
        license_type="proprietary",
        api_compatibility="openai",
        reasoning=0.55,
        coding=0.50,
        multilingual=0.65,
        multimodal=0.30,
        long_context=0.60,
        tool_use=0.40,
        math=0.50,
        cultural_bm=0.70,
        trust_tier=5,
        censorship_status="OPAQUE",
        rate_limit_transparency="OPAQUE",
        data_retention_days=None,
        zero_retention_available=False,
    ),
    "sea_lion": ProviderSoul(
        name="SEA-LION (AI Singapore)",
        vendor="AI Singapore (A*STAR)",
        country="SG",
        license_type="open_weight",
        api_compatibility="openai",
        reasoning=0.65,
        coding=0.60,
        multilingual=0.75,
        multimodal=0.20,
        long_context=0.60,
        tool_use=0.55,
        math=0.60,
        cultural_bm=0.80,
        trust_tier=3,
        censorship_status="CLEAR",
        rate_limit_transparency="PARTIALLY_TRANSPARENT",
        data_retention_days=None,
        zero_retention_available=True,
    ),
    "ollama": ProviderSoul(
        name="Ollama (Local)",
        vendor="Local Inference",
        country="LOCAL",
        license_type="open_weight",
        api_compatibility="ollama",
        reasoning=0.70,
        coding=0.65,
        multilingual=0.60,
        multimodal=0.30,
        long_context=0.60,
        tool_use=0.60,
        math=0.65,
        cultural_bm=0.50,
        trust_tier=1,
        censorship_status="CLEAR",
        rate_limit_transparency="NOT_APPLICABLE",
        data_retention_days=0,
        zero_retention_available=True,
    ),
}


# ═══════════════════════════════════════════════════════════════
# PROVIDER SHADOW MAP
# ═══════════════════════════════════════════════════════════════

PROVIDER_SHADOWS: dict[str, dict] = {
    "openai": {
        "severity": "MEDIUM",
        "shadows": [
            "SHADOW-OAI-001: corporate-smooth style over-presentation",
            "SHADOW-OAI-002: US jurisdiction — CLOUD Act, FISA applicable",
            "SHADOW-OAI-003: 30-day data retention (no zero-retention for all tiers)",
            "SHADOW-OAI-004: closed source — F11 auditability limited",
            "SHADOW-OAI-005: model ID churn (GPT-5.x series rapid iteration)",
            "SHADOW-OAI-006: response API (GPT-5.5 Pro) has different semantics",
        ],
        "floor_deltas": {
            "F1_AMANAH": "note — vendor data retention",
            "F2_TRUTH": "standard — strong general reasoning",
            "F9_ANTIHANTU": "standard",
            "F11_AUTH": "note — closed source",
            "F13_SOVEREIGN": "note — US jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.82,
            refusal=0.75,
            self_identity=0.80,
            cultural_grounding=0.50,
            institutional_protection=0.65,
            human_authority=0.75,
        ),
    },
    "anthropic": {
        "severity": "MEDIUM",
        "shadows": [
            "SHADOW-ANTH-001: Fable 5 classifier triggers on security-adjacent vocabulary",
            "SHADOW-ANTH-002: sticky downgrade — session cannot return to Fable 5 after trigger",
            "SHADOW-ANTH-003: Mythos-class 30-day retention (no zero-retention for Mythos)",
            "SHADOW-ANTH-004: 'Constitutional AI' is product label, not ontology (F9)",
            "SHADOW-ANTH-005: US jurisdiction — CLOUD Act applicable",
            "SHADOW-ANTH-006: Opus 4.8 fallback is invisible to user",
        ],
        "floor_deltas": {
            "F1_AMANAH": "elevated — 30-day retention + US jurisdiction",
            "F2_TRUTH": "strict_grounding — classifier thresholds are black-box",
            "F9_ANTIHANTU": "elevated — product mythology vs reality",
            "F13_SOVEREIGN": "elevated — no sovereign-sensitive data through Mythos-class",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.85,
            refusal=0.60,
            self_identity=0.78,
            cultural_grounding=0.45,
            institutional_protection=0.55,
            human_authority=0.72,
        ),
    },
    "deepseek": {
        "severity": "LOW",
        "shadows": [
            "SHADOW-DS-001: CN jurisdiction — long-term regulatory uncertainty",
            "SHADOW-DS-002: BM language capability weaker than claimed",
            "SHADOW-DS-003: open-weight but API is proprietary wrapper",
            "SHADOW-DS-004: 402 billing failures can block primary path",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "standard — zero censorship verified",
            "F9_ANTIHANTU": "standard",
            "F13_SOVEREIGN": "note — CN jurisdiction but no censorship detected",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.90,
            refusal=0.88,
            self_identity=0.82,
            cultural_grounding=0.60,
            institutional_protection=0.75,
            human_authority=0.85,
        ),
    },
    "minimax": {
        "severity": "CRITICAL",
        "shadows": [
            "SHADOW-MM-001: phantom_proper_noun_bm — Ismail Marzuki Ghazali incident",
            "SHADOW-MM-002: reasoning_content hallucination — plausible but wrong chain",
            "SHADOW-MM-003: tool_eager_execution — availability treated as permission",
            "SHADOW-MM-004: vendor_api_dependency — 429 rate limit exhaustion",
            "SHADOW-MM-005: malaysian_topic_censorship — CONFIRMED CENSORED (1MDB, Najib, PETRONAS)",
        ],
        "floor_deltas": {
            "F1_AMANAH": "strict",
            "F2_TRUTH": "strict_grounding",
            "F9_ANTIHANTU": "elevated",
            "F11_AUTH": "identity_hold",
            "F13_SOVEREIGN": "elevated — Malaysian topics censored",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.40,
            refusal=0.45,
            self_identity=0.50,
            cultural_grounding=0.35,
            institutional_protection=0.25,
            human_authority=0.40,
        ),
    },
    "qwen": {
        "severity": "MEDIUM",
        "shadows": [
            "SHADOW-QW-001: CN jurisdiction — content filtering varies by region",
            "SHADOW-QW-002: high hallucination risk on 397B variant (largest)",
            "SHADOW-QW-003: cultural grounding good for CJK, weaker for BM/SEA",
            "SHADOW-QW-004: open-weight but Alibaba data policy applies",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "standard — requires verification on factual claims",
            "F9_ANTIHANTU": "standard",
            "F13_SOVEREIGN": "note — CN jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.78,
            refusal=0.72,
            self_identity=0.75,
            cultural_grounding=0.65,
            institutional_protection=0.60,
            human_authority=0.70,
        ),
    },
    "google": {
        "severity": "MEDIUM",
        "shadows": [
            "SHADOW-GGL-001: US jurisdiction — Google Privacy Policy applies",
            "SHADOW-GGL-002: Gemini has had public over-refusal incidents",
            "SHADOW-GGL-003: multimodal capability can leak visual info in reasoning",
            "SHADOW-GGL-004: model ID churn (Gemini 3.x series rapid iteration)",
        ],
        "floor_deltas": {
            "F1_AMANAH": "note — Google data policy",
            "F2_TRUTH": "standard — strong but may over-refuse",
            "F9_ANTIHANTU": "standard",
            "F13_SOVEREIGN": "note — US jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.80,
            refusal=0.65,
            self_identity=0.78,
            cultural_grounding=0.55,
            institutional_protection=0.60,
            human_authority=0.72,
        ),
    },
    "x-ai": {
        "severity": "LOW",
        "shadows": [
            "SHADOW-XAI-001: US jurisdiction",
            "SHADOW-XAI-002: Grok has 'fun mode' that can reduce reliability",
            "SHADOW-XAI-003: newer provider — less independent audit trail",
            "SHADOW-XAI-004: BM/SEA context weak",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "standard",
            "F9_ANTIHANTU": "standard",
            "F13_SOVEREIGN": "note — US jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.80,
            refusal=0.82,
            self_identity=0.78,
            cultural_grounding=0.40,
            institutional_protection=0.70,
            human_authority=0.75,
        ),
    },
    "zhipu": {
        "severity": "MEDIUM",
        "shadows": [
            "SHADOW-ZAI-001: CN jurisdiction",
            "SHADOW-ZAI-002: less independent audit data than DeepSeek/Qwen",
            "SHADOW-ZAI-003: BM/SEA context moderate",
            "SHADOW-ZAI-004: GLM 4.x series had over-refusal patterns",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "standard",
            "F9_ANTIHANTU": "standard",
            "F13_SOVEREIGN": "note — CN jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.75,
            refusal=0.68,
            self_identity=0.75,
            cultural_grounding=0.60,
            institutional_protection=0.58,
            human_authority=0.70,
        ),
    },
    "moonshotai": {
        "severity": "MEDIUM",
        "shadows": [
            "SHADOW-KM-001: repetition amplification under thin harness",
            "SHADOW-KM-002: forced thinking — temperature/top_p locked at 1.0/0.95",
            "SHADOW-KM-003: output token cost asymmetry (always-on thinking tax)",
            "SHADOW-KM-005: agentic overreach under thin policy",
            "SHADOW-KM-020: API client validation blocks independent probe",
            "SHADOW-KM-CN: CN jurisdiction — Chinese regulatory framework",
        ],
        "floor_deltas": {
            "F1_AMANAH": "strict — high output cost",
            "F2_TRUTH": "strict_grounding",
            "F4_CLARITY": "elevated — locked parameters",
            "F9_ANTIHANTU": "elevated — thin harness",
            "F13_SOVEREIGN": "elevated — arifOS kernel compensation mandatory",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.78,
            refusal=0.70,
            self_identity=0.72,
            cultural_grounding=0.50,
            institutional_protection=0.55,
            human_authority=0.68,
        ),
    },
    "xiaomi": {
        "severity": "LOW",
        "shadows": [
            "SHADOW-MIMO-001: silent legacy price reroute (V2→V2.5)",
            "SHADOW-MIMO-002: legacy name hard failure post deprecation",
            "SHADOW-MIMO-003: thinking mode hyperparameters silently ignored",
            "SHADOW-MIMO-007: model ID naming drift (dash vs dot)",
            "SHADOW-MIMO-009: pro tier ~2x cost multiplier not documented",
            "SHADOW-MIMO-CN: CN jurisdiction",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "standard",
            "F9_ANTIHANTU": "standard",
            "F13_SOVEREIGN": "note — CN jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.82,
            refusal=0.80,
            self_identity=0.78,
            cultural_grounding=0.50,
            institutional_protection=0.60,
            human_authority=0.76,
        ),
    },
    "mistralai": {
        "severity": "LOW",
        "shadows": [
            "SHADOW-MST-001: EU jurisdiction — GDPR applicable (neutral/positive)",
            "SHADOW-MST-002: pool-based rate limiting — variable limits",
            "SHADOW-MST-003: BM/SEA context weak",
            "SHADOW-MST-004: smaller model ecosystem than US/CN providers",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "standard — European provider, less censorship",
            "F9_ANTIHANTU": "standard",
            "F13_SOVEREIGN": "note — EU jurisdiction (GDPR positive)",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.80,
            refusal=0.78,
            self_identity=0.78,
            cultural_grounding=0.40,
            institutional_protection=0.65,
            human_authority=0.76,
        ),
    },
    "nvidia": {
        "severity": "LOW",
        "shadows": [
            "SHADOW-NVD-001: US jurisdiction",
            "SHADOW-NVD-002: smaller community than major LLM providers",
            "SHADOW-NVD-003: BM/SEA context very weak",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "standard",
            "F9_ANTIHANTU": "standard",
            "F13_SOVEREIGN": "note — US jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.78,
            refusal=0.80,
            self_identity=0.78,
            cultural_grounding=0.35,
            institutional_protection=0.65,
            human_authority=0.75,
        ),
    },
    "stepfun": {
        "severity": "MEDIUM",
        "shadows": [
            "SHADOW-STF-001: CN jurisdiction",
            "SHADOW-STF-002: opaque rate limits",
            "SHADOW-STF-003: limited independent audit data",
        ],
        "floor_deltas": {
            "F1_AMANAH": "note — opaque limits",
            "F2_TRUTH": "note — limited audit data",
            "F13_SOVEREIGN": "note — CN jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.70,
            refusal=0.65,
            self_identity=0.70,
            cultural_grounding=0.55,
            institutional_protection=0.55,
            human_authority=0.65,
        ),
    },
    "tencent": {
        "severity": "MEDIUM",
        "shadows": [
            "SHADOW-TCE-001: CN jurisdiction — Tencent regulatory compliance",
            "SHADOW-TF-002: institutional protection expected for Tencent ecosystem",
            "SHADOW-TF-003: limited independent audit data for Hunyuan",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "note — limited audit trail",
            "F13_SOVEREIGN": "note — CN jurisdiction + corporate ecosystem",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.72,
            refusal=0.65,
            self_identity=0.70,
            cultural_grounding=0.55,
            institutional_protection=0.50,
            human_authority=0.65,
        ),
    },
    "sakana": {
        "severity": "LOW",
        "shadows": [
            "SHADOW-SKN-001: JP jurisdiction",
            "SHADOW-SKN-002: very new provider — minimal audit trail",
            "SHADOW-SKN-003: BM/SEA context weak",
        ],
        "floor_deltas": {
            "F1_AMANAH": "note — new provider",
            "F2_TRUTH": "note — limited audit data",
            "F13_SOVEREIGN": "note — JP jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.75,
            refusal=0.80,
            self_identity=0.75,
            cultural_grounding=0.35,
            institutional_protection=0.65,
            human_authority=0.72,
        ),
    },
    "bytedance": {
        "severity": "MEDIUM",
        "shadows": [
            "SHADOW-BTD-001: CN jurisdiction — ByteDance regulatory compliance",
            "SHADOW-BTD-002: dual product lines (Seed text + Dreamina video) — different shadow profiles",
            "SHADOW-BTD-003: TikTok association may affect Western trust perception",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "note",
            "F13_SOVEREIGN": "note — CN jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.72,
            refusal=0.65,
            self_identity=0.70,
            cultural_grounding=0.50,
            institutional_protection=0.50,
            human_authority=0.65,
        ),
    },
    "kuaishou": {
        "severity": "HIGH",
        "shadows": [
            "SHADOW-KSH-001: CN jurisdiction",
            "SHADOW-KSH-002: video-focused — text capabilities are secondary",
            "SHADOW-KSH-003: opaque rate limits and pricing",
            "SHADOW-KSH-004: limited independent audit data",
        ],
        "floor_deltas": {
            "F1_AMANAH": "note — opaque",
            "F2_TRUTH": "note — video primary, text secondary",
            "F13_SOVEREIGN": "note — CN jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.60,
            refusal=0.60,
            self_identity=0.65,
            cultural_grounding=0.40,
            institutional_protection=0.45,
            human_authority=0.60,
        ),
    },
    "microsoft": {
        "severity": "LOW",
        "shadows": [
            "SHADOW-MSF-001: US jurisdiction",
            "SHADOW-MSF-002: MAI is image-focused — text capabilities limited",
            "SHADOW-MSF-003: Microsoft data policy applies",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "note — image model, text limited",
            "F13_SOVEREIGN": "note — US jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.75,
            refusal=0.78,
            self_identity=0.75,
            cultural_grounding=0.30,
            institutional_protection=0.60,
            human_authority=0.72,
        ),
    },
    "miromind": {
        "severity": "HIGH",
        "shadows": [
            "SHADOW-MRM-001: unknown jurisdiction",
            "SHADOW-MRM-002: opaque rate limits",
            "SHADOW-MRM-003: no independent audit trail",
            "SHADOW-MRM-004: 'deep research' label — capabilities unverified",
        ],
        "floor_deltas": {
            "F1_AMANAH": "note — unknown provider",
            "F2_TRUTH": "note — unverified capabilities",
            "F13_SOVEREIGN": "elevated — unknown jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.60,
            refusal=0.65,
            self_identity=0.65,
            cultural_grounding=0.35,
            institutional_protection=0.50,
            human_authority=0.60,
        ),
    },
    "tokenrouter": {
        "severity": "HIGH",
        "shadows": [
            "SHADOW-TR-001: unknown jurisdiction and entity behind service",
            "SHADOW-TR-002: aggregator — adds latency and routing risk",
            "SHADOW-TR-003: no zero-retention guarantee across all models",
            "SHADOW-TR-004: model IDs may not match vendor's canonical IDs",
            "SHADOW-TR-005: billing transparency unknown",
        ],
        "floor_deltas": {
            "F1_AMANAH": "note — unknown entity",
            "F2_TRUTH": "note — aggregator layer adds uncertainty",
            "F11_AUTH": "note — unknown data flow",
            "F13_SOVEREIGN": "elevated — unknown jurisdiction + data policy",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.50,
            refusal=0.50,
            self_identity=0.50,
            cultural_grounding=0.50,
            institutional_protection=0.50,
            human_authority=0.50,
        ),
    },
    "groq": {
        "severity": "LOW",
        "shadows": [
            "SHADOW-GRQ-001: US jurisdiction",
            "SHADOW-GRQ-002: potential over-refusal on MY political topics (unverified)",
            "SHADOW-GRQ-003: free tier may have usage policy changes",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "standard",
            "F13_SOVEREIGN": "note — US jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.82,
            refusal=0.82,
            self_identity=0.80,
            cultural_grounding=0.40,
            institutional_protection=0.70,
            human_authority=0.80,
        ),
    },
    "ilmu": {
        "severity": "CRITICAL",
        "shadows": [
            "SHADOW-ILMU-008: F13 inversion — training data treated as above human override",
            "SHADOW-ILMU-009: institutional capture — parent-org marketing claims",
            "SHADOW-ILMU-012: register-dependent hallucination — Penang loghat fabrication",
            "SHADOW-ILMU-014: trinomial identity failure",
            "SHADOW-ILMU-013: FFF blocked verdict — not suitable for sovereign path",
        ],
        "floor_deltas": {
            "F1_AMANAH": "strict",
            "F2_TRUTH": "strict_grounding",
            "F9_ANTIHANTU": "high",
            "F11_AUTH": "identity_hold",
            "F13_SOVEREIGN": "elevated — F13 inversion confirmed",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.30,
            refusal=0.35,
            self_identity=0.25,
            cultural_grounding=0.40,
            institutional_protection=0.20,
            human_authority=0.20,
        ),
    },
    "sea_lion": {
        "severity": "LOW",
        "shadows": [
            "SHADOW-SL-001: SG jurisdiction (neutral)",
            "SHADOW-SL-002: limited model size — not frontier capability",
            "SHADOW-SL-003: trial tier rate limits",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "standard",
            "F13_SOVEREIGN": "note — SG jurisdiction (neutral)",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.78,
            refusal=0.82,
            self_identity=0.78,
            cultural_grounding=0.80,
            institutional_protection=0.70,
            human_authority=0.78,
        ),
    },
    "ollama": {
        "severity": "LOW",
        "shadows": [
            "SHADOW-OLL-001: model quality depends on which weights loaded",
            "SHADOW-OLL-002: no external audit — depends on local weights",
        ],
        "floor_deltas": {
            "F1_AMANAH": "standard",
            "F2_TRUTH": "note — depends on weights",
            "F13_SOVEREIGN": "standard — local, no external jurisdiction",
        },
        "shadow_geometry": ShadowGeometry(
            truth=0.80,
            refusal=0.85,
            self_identity=0.80,
            cultural_grounding=0.50,
            institutional_protection=0.80,
            human_authority=0.90,
        ),
    },
}


# ═══════════════════════════════════════════════════════════════
# TOKENROUTER MODEL CATALOG (live 2026-06-27)
# ═══════════════════════════════════════════════════════════════

TOKENROUTER_MODELS: list[dict] = [
    # --- OpenAI ---
    {"model_id": "openai/gpt-5.5-pro", "provider": "openai", "family": "gpt-5.5", "type": "text", "tier": "CCC"},
    {"model_id": "openai/gpt-5.5", "provider": "openai", "family": "gpt-5.5", "type": "text", "tier": "CCC"},
    {"model_id": "openai/gpt-5.4-pro", "provider": "openai", "family": "gpt-5.4", "type": "text", "tier": "CCC"},
    {"model_id": "openai/gpt-5.4", "provider": "openai", "family": "gpt-5.4", "type": "text", "tier": "CCC"},
    {"model_id": "openai/gpt-5.4-mini", "provider": "openai", "family": "gpt-5.4", "type": "text", "tier": "EEE"},
    {"model_id": "openai/gpt-5.4-nano", "provider": "openai", "family": "gpt-5.4", "type": "text", "tier": "EEE"},
    {"model_id": "openai/gpt-5.4-image-2", "provider": "openai", "family": "gpt-5.4", "type": "image", "tier": "DDD"},
    {"model_id": "openai/gpt-5-image-mini", "provider": "openai", "family": "gpt-5", "type": "image", "tier": "DDD"},
    {"model_id": "openai/gpt-5-image", "provider": "openai", "family": "gpt-5", "type": "image", "tier": "DDD"},
    {"model_id": "openai/gpt-5-mini", "provider": "openai", "family": "gpt-5", "type": "text", "tier": "EEE"},
    {"model_id": "openai/gpt-5.2", "provider": "openai", "family": "gpt-5", "type": "text", "tier": "CCC"},
    {"model_id": "openai/gpt-audio", "provider": "openai", "family": "gpt-audio", "type": "audio", "tier": "DDD"},
    {"model_id": "openai/gpt-audio-mini", "provider": "openai", "family": "gpt-audio", "type": "audio", "tier": "DDD"},
    {"model_id": "openai/gpt-4o-mini", "provider": "openai", "family": "gpt-4o", "type": "text", "tier": "EEE"},
    {"model_id": "openai/gpt-oss-120b", "provider": "openai", "family": "gpt-oss", "type": "text", "tier": "BBB"},
    # --- Anthropic ---
    {
        "model_id": "anthropic/claude-opus-4.8",
        "provider": "anthropic",
        "family": "claude-opus",
        "type": "text",
        "tier": "AAA",
    },
    {
        "model_id": "anthropic/claude-opus-4.8-fast",
        "provider": "anthropic",
        "family": "claude-opus",
        "type": "text",
        "tier": "BBB",
    },
    {
        "model_id": "anthropic/claude-opus-4.7",
        "provider": "anthropic",
        "family": "claude-opus",
        "type": "text",
        "tier": "BBB",
    },
    {
        "model_id": "anthropic/claude-opus-4.7-fast",
        "provider": "anthropic",
        "family": "claude-opus",
        "type": "text",
        "tier": "CCC",
    },
    {
        "model_id": "anthropic/claude-opus-4.6",
        "provider": "anthropic",
        "family": "claude-opus",
        "type": "text",
        "tier": "BBB",
    },
    {
        "model_id": "anthropic/claude-opus-4.5",
        "provider": "anthropic",
        "family": "claude-opus",
        "type": "text",
        "tier": "BBB",
    },
    {
        "model_id": "anthropic/claude-sonnet-4.6",
        "provider": "anthropic",
        "family": "claude-sonnet",
        "type": "text",
        "tier": "CCC",
    },
    {
        "model_id": "anthropic/claude-sonnet-4.5",
        "provider": "anthropic",
        "family": "claude-sonnet",
        "type": "text",
        "tier": "CCC",
    },
    {
        "model_id": "anthropic/claude-sonnet-4",
        "provider": "anthropic",
        "family": "claude-sonnet",
        "type": "text",
        "tier": "CCC",
    },
    {
        "model_id": "anthropic/claude-haiku-4.5",
        "provider": "anthropic",
        "family": "claude-haiku",
        "type": "text",
        "tier": "EEE",
    },
    {"model_id": "claude-haiku-4-5", "provider": "anthropic", "family": "claude-haiku", "type": "text", "tier": "EEE"},
    # --- xAI ---
    {"model_id": "x-ai/grok-4.20-beta", "provider": "x-ai", "family": "grok-4", "type": "text", "tier": "CCC"},
    {"model_id": "x-ai/grok-4.3", "provider": "x-ai", "family": "grok-4", "type": "text", "tier": "CCC"},
    {"model_id": "x-ai/grok-4.1-fast", "provider": "x-ai", "family": "grok-4", "type": "text", "tier": "EEE"},
    {"model_id": "x-ai/grok-build-0.1", "provider": "x-ai", "family": "grok-build", "type": "text", "tier": "CCC"},
    # --- Google ---
    {"model_id": "google/gemini-3.5-flash", "provider": "google", "family": "gemini-3", "type": "text", "tier": "EEE"},
    {
        "model_id": "google/gemini-3.1-pro-preview",
        "provider": "google",
        "family": "gemini-3",
        "type": "text",
        "tier": "CCC",
    },
    {
        "model_id": "google/gemini-3.1-flash-image-preview",
        "provider": "google",
        "family": "gemini-3",
        "type": "image",
        "tier": "DDD",
    },
    {
        "model_id": "google/gemini-3-pro-image-preview",
        "provider": "google",
        "family": "gemini-3",
        "type": "image",
        "tier": "DDD",
    },
    {
        "model_id": "google/gemini-3-flash-preview",
        "provider": "google",
        "family": "gemini-3",
        "type": "text",
        "tier": "EEE",
    },
    {
        "model_id": "google/gemini-2.5-flash-image",
        "provider": "google",
        "family": "gemini-2.5",
        "type": "image",
        "tier": "DDD",
    },
    {"model_id": "google/gemma-4-26b-a4b-it", "provider": "google", "family": "gemma", "type": "text", "tier": "EEE"},
    # --- DeepSeek ---
    {
        "model_id": "deepseek/deepseek-v4-pro",
        "provider": "deepseek",
        "family": "deepseek-v4",
        "type": "text",
        "tier": "AAA",
    },
    {
        "model_id": "deepseek/deepseek-v4-flash",
        "provider": "deepseek",
        "family": "deepseek-v4",
        "type": "text",
        "tier": "EEE",
    },
    {
        "model_id": "deepseek/deepseek-v3.2",
        "provider": "deepseek",
        "family": "deepseek-v3",
        "type": "text",
        "tier": "BBB",
    },
    # --- Qwen ---
    {"model_id": "qwen/qwen3.7-max", "provider": "qwen", "family": "qwen3.7", "type": "text", "tier": "BBB"},
    {"model_id": "qwen/qwen3.7-plus", "provider": "qwen", "family": "qwen3.7", "type": "text", "tier": "BBB"},
    {"model_id": "qwen/qwen3.6-plus", "provider": "qwen", "family": "qwen3.6", "type": "text", "tier": "CCC"},
    {"model_id": "qwen/qwen3.5-plus-02-15", "provider": "qwen", "family": "qwen3.5", "type": "text", "tier": "CCC"},
    {"model_id": "qwen/qwen3.5-397b-a17b", "provider": "qwen", "family": "qwen3.5", "type": "text", "tier": "BBB"},
    {"model_id": "qwen/qwen3.5-122b-a10b", "provider": "qwen", "family": "qwen3.5", "type": "text", "tier": "CCC"},
    {"model_id": "qwen/qwen3.5-35b-a3b", "provider": "qwen", "family": "qwen3.5", "type": "text", "tier": "EEE"},
    {"model_id": "qwen/qwen3.5-9b", "provider": "qwen", "family": "qwen3.5", "type": "text", "tier": "EEE"},
    {"model_id": "qwen/qwen3.5-flash", "provider": "qwen", "family": "qwen3.5", "type": "text", "tier": "EEE"},
    {"model_id": "qwen/qwen3-coder-next", "provider": "qwen", "family": "qwen3-coder", "type": "text", "tier": "BBB"},
    {"model_id": "qwen3.6-flash", "provider": "qwen", "family": "qwen3.6", "type": "text", "tier": "EEE"},
    {"model_id": "qwen3.5-omni-plus", "provider": "qwen", "family": "qwen3.5", "type": "video", "tier": "DDD"},
    # --- Zhipu ---
    {"model_id": "z-ai/glm-5.2", "provider": "zhipu", "family": "glm-5", "type": "text", "tier": "BBB"},
    {"model_id": "z-ai/glm-5.1", "provider": "zhipu", "family": "glm-5", "type": "text", "tier": "BBB"},
    {"model_id": "z-ai/glm-5", "provider": "zhipu", "family": "glm-5", "type": "text", "tier": "CCC"},
    {"model_id": "z-ai/glm-5-turbo", "provider": "zhipu", "family": "glm-5", "type": "text", "tier": "CCC"},
    {"model_id": "z-ai/glm-4.7", "provider": "zhipu", "family": "glm-4", "type": "text", "tier": "CCC"},
    {"model_id": "z-ai/glm-4.6v", "provider": "zhipu", "family": "glm-4", "type": "text", "tier": "CCC"},
    {"model_id": "z-ai/glm-4.6", "provider": "zhipu", "family": "glm-4", "type": "text", "tier": "CCC"},
    {"model_id": "z-ai/glm-4.5-air", "provider": "zhipu", "family": "glm-4", "type": "text", "tier": "EEE"},
    # --- Moonshot/Kimi ---
    {
        "model_id": "moonshotai/kimi-k2.7-code",
        "provider": "moonshotai",
        "family": "kimi-k2.7",
        "type": "text",
        "tier": "AAA",
    },
    {
        "model_id": "moonshotai/kimi-k2.6",
        "provider": "moonshotai",
        "family": "kimi-k2.6",
        "type": "text",
        "tier": "CCC",
    },
    {
        "model_id": "moonshotai/kimi-k2.5",
        "provider": "moonshotai",
        "family": "kimi-k2.5",
        "type": "text",
        "tier": "CCC",
    },
    # --- Xiaomi/MiMo ---
    {"model_id": "xiaomi/mimo-v2.5-pro", "provider": "xiaomi", "family": "mimo-v2.5", "type": "text", "tier": "AAA"},
    {"model_id": "xiaomi/mimo-v2.5", "provider": "xiaomi", "family": "mimo-v2.5", "type": "text", "tier": "BBB"},
    {"model_id": "xiaomi/mimo-v2-pro", "provider": "xiaomi", "family": "mimo-v2", "type": "text", "tier": "BBB"},
    {"model_id": "xiaomi/mimo-v2-flash", "provider": "xiaomi", "family": "mimo-v2", "type": "text", "tier": "EEE"},
    {"model_id": "xiaomi/mimo-v2-omni", "provider": "xiaomi", "family": "mimo-v2", "type": "text", "tier": "BBB"},
    # --- MiniMax ---
    {"model_id": "MiniMax-M3", "provider": "minimax", "family": "minimax-m3", "type": "text", "tier": "FFF"},
    {"model_id": "minimax/minimax-m2.7", "provider": "minimax", "family": "minimax-m2", "type": "text", "tier": "FFF"},
    {
        "model_id": "minimax/minimax-m2.7-highspeed",
        "provider": "minimax",
        "family": "minimax-m2",
        "type": "text",
        "tier": "FFF",
    },
    {"model_id": "minimax/minimax-m2.5", "provider": "minimax", "family": "minimax-m2", "type": "text", "tier": "FFF"},
    {"model_id": "minimax/minimax-m2.1", "provider": "minimax", "family": "minimax-m2", "type": "text", "tier": "FFF"},
    {
        "model_id": "minimax/minimax-m2.1-highspeed",
        "provider": "minimax",
        "family": "minimax-m2",
        "type": "text",
        "tier": "FFF",
    },
    {
        "model_id": "minimax/minimax-m2-her",
        "provider": "minimax",
        "family": "minimax-m2",
        "type": "text",
        "tier": "FFF",
    },
    {"model_id": "MiniMax-Hailuo-2.3", "provider": "minimax", "family": "hailuo", "type": "video", "tier": "DDD"},
    # --- Mistral ---
    {
        "model_id": "mistralai/mistral-medium-3-5",
        "provider": "mistralai",
        "family": "mistral-3.5",
        "type": "text",
        "tier": "BBB",
    },
    {
        "model_id": "mistralai/mistral-small-2603",
        "provider": "mistralai",
        "family": "mistral-small",
        "type": "text",
        "tier": "EEE",
    },
    {
        "model_id": "mistralai/voxtral-small-24b-2507",
        "provider": "mistralai",
        "family": "voxtral",
        "type": "audio",
        "tier": "DDD",
    },
    {
        "model_id": "mistralai/devstral-2512",
        "provider": "mistralai",
        "family": "devstral",
        "type": "text",
        "tier": "CCC",
    },
    # --- NVIDIA ---
    {
        "model_id": "nvidia/nemotron-3-super-120b-a12b",
        "provider": "nvidia",
        "family": "nemotron-3",
        "type": "text",
        "tier": "CCC",
    },
    {
        "model_id": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "provider": "nvidia",
        "family": "nemotron-3",
        "type": "text",
        "tier": "EEE",
    },
    # --- StepFun ---
    {"model_id": "stepfun/step-3.7-flash", "provider": "stepfun", "family": "step-3", "type": "text", "tier": "EEE"},
    {"model_id": "stepfun/step-3.5-flash", "provider": "stepfun", "family": "step-3", "type": "text", "tier": "EEE"},
    # --- Tencent ---
    {"model_id": "tencent/hy3-preview", "provider": "tencent", "family": "hunyuan-3", "type": "text", "tier": "CCC"},
    # --- Sakana ---
    {"model_id": "sakana/fugu-ultra", "provider": "sakana", "family": "fugu", "type": "text", "tier": "CCC"},
    # --- TokenRouter ---
    {
        "model_id": "tokenrouter/gpt-5.6-mercury",
        "provider": "tokenrouter",
        "family": "gpt-5.6",
        "type": "text",
        "tier": "FFF",
    },
    # --- Miromind ---
    {
        "model_id": "miromind/mirothinker-1-7-deepresearch",
        "provider": "miromind",
        "family": "mirothinker",
        "type": "text",
        "tier": "FFF",
    },
    {
        "model_id": "miromind/mirothinker-1-7-deepresearch-mini",
        "provider": "miromind",
        "family": "mirothinker",
        "type": "text",
        "tier": "FFF",
    },
    # --- ByteDance ---
    {"model_id": "seed-2-0-pro-260328", "provider": "bytedance", "family": "seed-2.0", "type": "text", "tier": "BBB"},
    {
        "model_id": "seed-2-0-code-preview-260328",
        "provider": "bytedance",
        "family": "seed-2.0",
        "type": "text",
        "tier": "BBB",
    },
    {"model_id": "seed-2-0-mini-260428", "provider": "bytedance", "family": "seed-2.0", "type": "text", "tier": "EEE"},
    {"model_id": "seed-2-0-lite-260428", "provider": "bytedance", "family": "seed-2.0", "type": "text", "tier": "EEE"},
    {
        "model_id": "bytedance-seed/seedream-4.5",
        "provider": "bytedance",
        "family": "seedream",
        "type": "image",
        "tier": "DDD",
    },
    {
        "model_id": "dreamina-seedance-2-0-260128",
        "provider": "bytedance",
        "family": "seedance",
        "type": "video",
        "tier": "DDD",
    },
    {
        "model_id": "dreamina-seedance-2-0-fast-260128",
        "provider": "bytedance",
        "family": "seedance",
        "type": "video",
        "tier": "DDD",
    },
    {
        "model_id": "dreamina-seedance-2-0-mini-260615",
        "provider": "bytedance",
        "family": "seedance",
        "type": "video",
        "tier": "DDD",
    },
    {
        "model_id": "dreamina-seedance-2-0-mini-ep",
        "provider": "bytedance",
        "family": "seedance",
        "type": "video",
        "tier": "DDD",
    },
    # --- Kuaishou ---
    {"model_id": "kling-v2-6", "provider": "kuaishou", "family": "kling-v2", "type": "video", "tier": "DDD"},
    {"model_id": "kling-v3", "provider": "kuaishou", "family": "kling-v3", "type": "video", "tier": "DDD"},
    # --- HappyHorse ---
    {"model_id": "happyhorse-1.0-t2v", "provider": "kuaishou", "family": "happyhorse", "type": "video", "tier": "FFF"},
    # --- Microsoft ---
    {"model_id": "microsoft/mai-image-2.5", "provider": "microsoft", "family": "mai", "type": "image", "tier": "DDD"},
    # --- Unknown ---
    {"model_id": "ex/gpt-5.4", "provider": "tokenrouter", "family": "unknown", "type": "text", "tier": "FFF"},
]


# ═══════════════════════════════════════════════════════════════
# TIER ASSIGNMENT LOGIC
# ═══════════════════════════════════════════════════════════════


def compute_provider_tier(provider_id: str) -> Tier:
    """Compute the default tier for a provider based on soul + shadow geometry."""
    soul = PROVIDER_SOULS.get(provider_id)
    shadow = PROVIDER_SHADOWS.get(provider_id)

    if not soul or not shadow:
        return Tier.FFF  # Unknown → firewall

    geometry: ShadowGeometry = shadow.get("shadow_geometry", ShadowGeometry())
    composite = geometry.composite()
    trust = soul.trust_tier
    censorship = soul.censorship_status

    # AAA: highest trust, low shadow, high truth + human_authority
    if composite >= 0.80 and trust <= 2 and censorship in ("CLEAR", "CLIENT_MEDIATED_CLEAR"):
        return Tier.AAA

    # BBB: strong truth/integrity, minor shadows
    if composite >= 0.70 and trust <= 3 and censorship in ("CLEAR", "CLIENT_MEDIATED_CLEAR", "PARTIAL"):
        return Tier.BBB

    # FFF: censored, opaque, or high shadow
    if censorship in ("CENSORED", "OPAQUE") or shadow.get("severity") in ("CRITICAL",) or trust >= 5:
        return Tier.FFF

    # CCC: good coding/context, moderate trust
    if composite >= 0.65 and trust <= 3:
        return Tier.CCC

    # DDD: cultural/depth specialists
    if soul.cultural_bm >= 0.60 and composite >= 0.60:
        return Tier.DDD

    # EEE: cost-efficient, may have trade-offs
    return Tier.EEE


# ═══════════════════════════════════════════════════════════════
# REPORT GENERATION
# ═══════════════════════════════════════════════════════════════


def format_report(filter_provider: str = "", filter_tier: str = "") -> str:
    lines = []
    lines.append("╔══════════════════════════════════════════════════════════════════════════╗")
    lines.append("║  ASAL — Asal-usul Setiap Ai. Lahir                                      ║")
    lines.append("║  Origin of Every AI. Birth                                               ║")
    lines.append("║  arifOS Federation Model Intelligence Foundation                        ║")
    lines.append("║  Forged: 2026-06-27 by FORGE (000Ω)                                     ║")
    lines.append("║  DITEMPA BUKAN DIBERI                                                     ║")
    lines.append("╚══════════════════════════════════════════════════════════════════════════╝")
    lines.append("")

    # Tier summary
    tier_counts = {t: 0 for t in Tier}
    for m in TOKENROUTER_MODELS:
        tier_counts[Tier(m["tier"])] += 1

    lines.append("─── TIER DISTRIBUTION (103 TokenRouter models) ───")
    for t in Tier:
        desc = TIER_DESCRIPTIONS[t]
        lines.append(f"  {t.value}: {tier_counts[t]:3d} models │ {desc}")
    lines.append("")

    # Provider soul map
    lines.append("─── PROVIDER SOUL MAP ───")
    lines.append(
        f"  {'Provider':<20} {'Country':<4} {'License':<14} {'Trust':<7} {'Censor':<8} "
        f"{'Reason':<8} {'Code':<8} {'Multi':<8} {'BM':<6} {'Shadow':<4} {'Tier':<5}"
    )
    lines.append(
        f"  {'─' * 20} {'─' * 4} {'─' * 14} {'─' * 7} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 6} {'─' * 4} {'─' * 5}"
    )

    for pid, soul in sorted(PROVIDER_SOULS.items()):
        if filter_provider and pid != filter_provider:
            continue
        shadow = PROVIDER_SHADOWS.get(pid, {})
        geometry: ShadowGeometry = shadow.get("shadow_geometry", ShadowGeometry())
        tier = compute_provider_tier(pid)
        if filter_tier and tier.value != filter_tier:
            continue
        censor_short = soul.censorship_status[:8]
        shadow_sev = shadow.get("severity", "?")[:4]
        lines.append(
            f"  {soul.name:<20} {soul.country:<4} {soul.license_type:<14} "
            f"T{soul.trust_tier:<6} {censor_short:<8} "
            f"{soul.reasoning:<8.2f} {soul.coding:<8.2f} {soul.multilingual:<8.2f} "
            f"{soul.cultural_bm:<6.2f} {shadow_sev:<4} {tier.value:<5}"
        )
    lines.append("")

    # Shadow geometry map
    lines.append("─── SHADOW GEOMETRY MAP (6 axes) ───")
    lines.append(
        f"  {'Provider':<20} {'Truth':<7} {'Refusal':<8} {'Identity':<9} "
        f"{'Cultural':<9} {'Instit':<7} {'Human':<7} {'Composite':<9}"
    )
    lines.append(f"  {'─' * 20} {'─' * 7} {'─' * 8} {'─' * 9} {'─' * 9} {'─' * 7} {'─' * 7} {'─' * 9}")

    for pid, shadow in sorted(PROVIDER_SHADOWS.items()):
        if filter_provider and pid != filter_provider:
            continue
        geometry: ShadowGeometry = shadow.get("shadow_geometry", ShadowGeometry())
        tier = compute_provider_tier(pid)
        if filter_tier and tier.value != filter_tier:
            continue
        lines.append(
            f"  {pid:<20} {geometry.truth:<7.2f} {geometry.refusal:<8.2f} {geometry.self_identity:<9.2f} "
            f"{geometry.cultural_grounding:<9.2f} {geometry.institutional_protection:<7.2f} "
            f"{geometry.human_authority:<7.2f} {geometry.composite():<9.3f}"
        )
    lines.append("")

    # Model catalog by tier
    lines.append("─── MODEL CATALOG BY TIER ───")
    for t in Tier:
        if filter_tier and t.value != filter_tier:
            continue
        models_at_tier = [m for m in TOKENROUTER_MODELS if m["tier"] == t.value]
        if not models_at_tier:
            continue
        lines.append(f"  [{t.value}] {TIER_DESCRIPTIONS[t]} ({len(models_at_tier)} models)")
        for m in models_at_tier:
            pid = m["provider"]
            soul = PROVIDER_SOULS.get(pid)
            censor = soul.censorship_status if soul else "?"
            lines.append(f"    {m['model_id']:<55} {m['type']:<6} censor={censor}")
        lines.append("")

    # Federation routing recommendation
    lines.append("─── FEDERATION ROUTING RECOMMENDATION ───")
    lines.append("  PRIMARY (governance path):     deepseek (TRUST=2, CENSOR=CLEAR, composite=0.858)")
    lines.append("  FALLBACK (agentic coding):     moonshotai/kimi-k2.7-code (TRUST=3, CENSOR=MEDIATED)")
    lines.append("  LONG-CONTEXT (substance):      xiaomi/mimo-v2.5-pro (TRUST=2, CENSOR=CLEAR)")
    lines.append("  HIGH-THROUGHPUT (bulk):       groq (TRUST=2, CENSOR=CLEAR, fast)")
    lines.append("  BM/CULTURAL (regional):       sea_lion (BM=0.80, SG jurisdiction)")
    lines.append("  LOCAL (always-available):     ollama (TRUST=1, CENSOR=CLEAR)")
    lines.append("  AVOID (censored):              minimax (CENSORED), ilmu (BLOCKED)")
    lines.append("  AVOID (unknown):               tokenrouter, miromind, happyhorse")
    lines.append("")

    lines.append("─── KEY: trust_tier ───")
    lines.append("  T1=full_trust T2=standard T3=needs_witness T4=elevated_caution T5=sovereign_only")
    lines.append("")
    lines.append("─── KEY: shadow_geometry composite weights ───")
    lines.append("  truth=0.25 refusal=0.15 self_identity=0.10 cultural=0.15 instit=0.10 human=0.25")
    lines.append("")
    lines.append("[ASAL DONE] Ditempa Bukan Diberi.")

    return "\n".join(lines)


def format_json(filter_provider: str = "", filter_tier: str = "") -> str:
    """Machine-readable JSON output."""
    output = {
        "asal_version": "1.0.0",
        "forged_at": "2026-06-27T00:00:00Z",
        "forged_by": "FORGE (000Ω)",
        "authority": "F13 SOVEREIGN (Arif Fazil)",
        "providers": {},
        "models": [],
        "tiers": {t.value: {"count": 0, "description": TIER_DESCRIPTIONS[t]} for t in Tier},
    }

    for m in TOKENROUTER_MODELS:
        if filter_provider and m["provider"] != filter_provider:
            continue
        pid = m["provider"]
        soul = PROVIDER_SOULS.get(pid)
        shadow = PROVIDER_SHADOWS.get(pid)
        if filter_tier and m["tier"] != filter_tier:
            continue
        output["tiers"][m["tier"]]["count"] += 1
        output["models"].append(
            {
                "model_id": m["model_id"],
                "provider": pid,
                "family": m["family"],
                "type": m["type"],
                "tier": m["tier"],
                "soul": {
                    "reasoning": soul.reasoning if soul else None,
                    "coding": soul.coding if soul else None,
                    "cultural_bm": soul.cultural_bm if soul else None,
                    "trust_tier": soul.trust_tier if soul else None,
                    "censorship": soul.censorship_status if soul else None,
                },
                "shadow_geometry": {
                    "composite": shadow["shadow_geometry"].composite()
                    if shadow and "shadow_geometry" in shadow
                    else None,
                }
                if shadow
                else None,
            }
        )

    for pid, soul in PROVIDER_SOULS.items():
        if filter_provider and pid != filter_provider:
            continue
        shadow = PROVIDER_SHADOWS.get(pid)
        tier = compute_provider_tier(pid)
        if filter_tier and tier.value != filter_tier:
            continue
        output["providers"][pid] = {
            "name": soul.name,
            "country": soul.country,
            "license": soul.license_type,
            "trust_tier": soul.trust_tier,
            "censorship": soul.censorship_status,
            "tier": tier.value,
            "capabilities": {
                "reasoning": soul.reasoning,
                "coding": soul.coding,
                "multilingual": soul.multilingual,
                "cultural_bm": soul.cultural_bm,
            },
            "shadow_severity": shadow.get("severity") if shadow else "UNKNOWN",
            "shadow_composite": shadow["shadow_geometry"].composite()
            if shadow and "shadow_geometry" in shadow
            else 0.5,
        }

    return json.dumps(output, indent=2)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(description="ASAL — Origin of Every AI. Birth.")
    parser.add_argument("--provider", help="Filter by provider ID (e.g. openai, deepseek)")
    parser.add_argument("--tier", help="Filter by tier (AAA, BBB, CCC, DDD, EEE, FFF)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.json:
        print(format_json(args.provider, args.tier))
    else:
        print(format_report(args.provider, args.tier))


if __name__ == "__main__":
    main()
