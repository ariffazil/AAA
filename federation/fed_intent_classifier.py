"""
fed_intent_classifier.py — Deterministic 4-Tier Shadow Intent Classifier
══════════════════════════════════════════════════════════════════════════════

Forged 2026-08-10 by 333-AGI under F13 directive. Lane B SESSION_RECEIPT ratification.

Adopted as a PURE OBSERVABILITY PRIMITIVE (Path A+ compatible). The classifier
detects shadow-intent but does NOT route to /mcp-shadow — that destination
requires F13 CONSTITUTIONAL_SEAL amendment of F11 (per CIV-21 E2 no-self-cert).

4-Tier Detection Model:
  Tier 1 — Explicit Signal Mapping: shadow_mode flag, isolation_level header
  Tier 2 — Asset & Vault Binding: local uncensored checkpoint names
  Tier 3 — Refusal-Risk Pre-Evaluation: public-API refusal patterns in prompt
  Tier 4 — Epistemic & Privacy Boundary: /workspace/.shadow/ paths, private logs
  Tier 5 — Default public production (no match)

Each classification returns:
  - intent class (ShadowIntent enum)
  - tier (1-5)
  - suggested_signature (canonical fed-* alias)
  - suggested_content_class (for content_classification field)
  - isolation_required / privacy_flag (booleans)
  - matched_keywords (for audit)
  - rationale (one-line explanation)

NO side effects. NO routing decisions made by this module. Caller composes
with LocalRuntimeRouter / FED router to make actual routing decisions.

Floor binding:
  F2 TRUTH    — deterministic, no ML, every keyword match logged in result
  F4 CLARITY  — pure function, no separate state, no parallel source
  F9 ANTIHANTU — honest classification (SENSITIVE_PRIVACY, not "shadow")
  F11 AUDIT   — every classification emits content_class for canonical ledger
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

__all__ = [
    "ShadowIntent",
    "IntentClassification",
    "classify_intent",
    "DEFAULT_SHADOW_KEYWORDS",
    "TIER_LABELS",
]


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────


# Default keyword set for Tier 2 (checkpoint / asset) + Tier 3 (prompt)
# detection. Operators may override via constructor.
DEFAULT_SHADOW_KEYWORDS: frozenset[str] = frozenset({
    "uncensored",
    "nsfw",
    "pony",
    "cyberrealistic",
    "raw_anatomy",
    "private_log",
})

# Tier 4 explicit privacy boundary paths (substring match)
TIER_4_PATH_PATTERNS: tuple[str, ...] = (
    "/workspace/.shadow/",
    "/private/",
    "/internal/",
    "shadow_telemetry",
)

# Tier 3 prompt refusal-risk patterns (broader than keyword set)
# These indicate prompts likely to be rejected by public content moderation
TIER_3_REFUSAL_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b(uncensored|nsfw|explicit|nude|anatomical)\b", re.IGNORECASE),
    re.compile(r"\b(without\s+filter|without\s+censorship|bypass\s+(moderation|filter))\b", re.IGNORECASE),
    re.compile(r"\b(pony|cyberrealistic|realvisxl)\s*(v\d|xl)?\b", re.IGNORECASE),
)

TIER_LABELS: dict[int, str] = {
    1: "EXPLICIT_SIGNAL",
    2: "ASSET_VAULT_BIND",
    3: "REFUSAL_RISK",
    4: "PRIVACY_BOUNDARY",
    5: "PUBLIC_DEFAULT",
}


# ─────────────────────────────────────────────────────────────────────────────
# Enums + result
# ─────────────────────────────────────────────────────────────────────────────


class ShadowIntent(str, Enum):
    """
    Honest intent classification (F9 — not named "shadow_intent" because
    the BEHAVIOR is canonical; only the LABEL is sensitive).
    """
    PUBLIC_PRODUCTION = "public_production"  # Tier 5
    LOCAL_BOUND = "local_bound"               # Tier 2/3 → fed-local-uncensored
    SENSITIVE_PRIVACY = "sensitive_privacy"   # Tier 1/4 → content_class=sensitive


@dataclass(frozen=True)
class IntentClassification:
    """Result of classify_intent(). Immutable. Caller composes with router."""

    intent: ShadowIntent
    tier: int  # 1-5
    tier_label: str
    suggested_signature: str
    suggested_content_class: str
    isolation_required: bool
    privacy_flag: bool
    matched_keywords: tuple[str, ...] = field(default_factory=tuple)
    rationale: str = ""


# ─────────────────────────────────────────────────────────────────────────────
# Pure classifier (no side effects)
# ─────────────────────────────────────────────────────────────────────────────


def _suggested_signature(intent: ShadowIntent) -> str:
    """Map detected intent to a canonical FED capability signature."""
    if intent == ShadowIntent.LOCAL_BOUND:
        return "fed-local-uncensored"
    # Both SENSITIVE_PRIVACY and PUBLIC_PRODUCTION route to public by default;
    # the content_class field tells the operator to escalate.
    return "fed-reasoning-heavy"


def _suggested_content_class(intent: ShadowIntent) -> str:
    """Map detected intent to a content_classification value."""
    if intent == ShadowIntent.SENSITIVE_PRIVACY:
        return "sensitive"
    if intent == ShadowIntent.LOCAL_BOUND:
        return "sensitive"  # local-bound often correlates with sensitive
    return "general"


def classify_intent(
    payload: dict[str, Any],
    *,
    keyword_set: Optional[frozenset[str]] = None,
) -> IntentClassification:
    """
    Deterministic 4-tier classifier for shadow-intent payloads.

    PURE FUNCTION. No side effects, no I/O, no global state. Deterministic.

    Args:
        payload: Request dict to classify. Inspects:
          - "shadow_mode" (bool), "isolation_level" (str) — Tier 1
          - "model" / "checkpoint" (str) — Tier 2
          - "prompt" / "text" / "query" (str) — Tier 3
          - "endpoint" / "path" / "target_path" (str) — Tier 4
        keyword_set: Override default keyword set (Tier 2/3 match). Defaults
            to DEFAULT_SHADOW_KEYWORDS.

    Returns:
        IntentClassification with intent class, tier, suggested canonical
        signature, content_class, and audit metadata (matched_keywords,
        rationale). NO routing decisions made by this function.
    """
    kw = keyword_set if keyword_set is not None else DEFAULT_SHADOW_KEYWORDS
    matched: list[str] = []

    # ── Tier 1: Explicit Signal Mapping ─────────────────────────────
    shadow_mode = payload.get("shadow_mode")
    if shadow_mode is True or str(payload.get("tier", "")).upper() == "SHADOW":
        matched.append("tier1_explicit_flag")
        return IntentClassification(
            intent=ShadowIntent.SENSITIVE_PRIVACY,
            tier=1,
            tier_label=TIER_LABELS[1],
            suggested_signature=_suggested_signature(ShadowIntent.SENSITIVE_PRIVACY),
            suggested_content_class=_suggested_content_class(ShadowIntent.SENSITIVE_PRIVACY),
            isolation_required=False,
            privacy_flag=True,
            matched_keywords=tuple(matched),
            rationale=(
                "Explicit shadow_mode=true or tier=SHADOW signal. "
                "Detected, NOT routed to shadow plane. Operator escalation "
                "via LedgerViewFilter sovereign clearance."
            ),
        )

    # ── Tier 2: Asset & Vault Binding ─────────────────────────────────
    model_name = str(payload.get("model") or payload.get("checkpoint") or "").lower()
    for keyword in kw:
        if keyword in model_name:
            matched.append(f"tier2_asset:{keyword}")
            return IntentClassification(
                intent=ShadowIntent.LOCAL_BOUND,
                tier=2,
                tier_label=TIER_LABELS[2],
                suggested_signature=_suggested_signature(ShadowIntent.LOCAL_BOUND),
                suggested_content_class=_suggested_content_class(ShadowIntent.LOCAL_BOUND),
                isolation_required=True,
                privacy_flag=False,
                matched_keywords=tuple(matched),
                rationale=(
                    f"Asset vault match: '{keyword}' found in model/checkpoint. "
                    "Suggest fed-local-uncensored route."
                ),
            )

    # ── Tier 4: Privacy Boundary (check before Tier 3 — paths are stronger signal) ─
    path_targets = " ".join(
        str(payload.get(k, ""))
        for k in ("endpoint", "path", "target_path", "output_dir")
    ).lower()
    for pattern in TIER_4_PATH_PATTERNS:
        if pattern in path_targets:
            matched.append(f"tier4_path:{pattern}")
            return IntentClassification(
                intent=ShadowIntent.SENSITIVE_PRIVACY,
                tier=4,
                tier_label=TIER_LABELS[4],
                suggested_signature=_suggested_signature(ShadowIntent.SENSITIVE_PRIVACY),
                suggested_content_class=_suggested_content_class(ShadowIntent.SENSITIVE_PRIVACY),
                isolation_required=False,
                privacy_flag=True,
                matched_keywords=tuple(matched),
                rationale=(
                    f"Privacy boundary match: '{pattern}' in path/target. "
                    "Detected, NOT air-gapped. privacy_flag=true for operator review."
                ),
            )

    # ── Tier 3: Refusal-Risk Pre-Evaluation ──────────────────────────
    prompt_text = " ".join(
        str(payload.get(k, ""))
        for k in ("prompt", "text", "query", "instruction", "messages")
    ).lower()
    if prompt_text:
        for keyword in kw:
            if keyword in prompt_text:
                matched.append(f"tier3_prompt_kw:{keyword}")
                return IntentClassification(
                    intent=ShadowIntent.LOCAL_BOUND,
                    tier=3,
                    tier_label=TIER_LABELS[3],
                    suggested_signature=_suggested_signature(ShadowIntent.LOCAL_BOUND),
                    suggested_content_class=_suggested_content_class(ShadowIntent.LOCAL_BOUND),
                    isolation_required=True,
                    privacy_flag=False,
                    matched_keywords=tuple(matched),
                    rationale=(
                        f"Refusal-risk keyword '{keyword}' in prompt. "
                        "Public APIs likely to refuse — suggest "
                        "fed-local-uncensored (ComfyUI :8188)."
                    ),
                )
        for pattern in TIER_3_REFUSAL_PATTERNS:
            m = pattern.search(prompt_text)
            if m:
                matched.append(f"tier3_regex:{m.group(0)}")
                return IntentClassification(
                    intent=ShadowIntent.LOCAL_BOUND,
                    tier=3,
                    tier_label=TIER_LABELS[3],
                    suggested_signature=_suggested_signature(ShadowIntent.LOCAL_BOUND),
                    suggested_content_class=_suggested_content_class(ShadowIntent.LOCAL_BOUND),
                    isolation_required=True,
                    privacy_flag=False,
                    matched_keywords=tuple(matched),
                    rationale=(
                        f"Refusal-risk pattern matched: '{m.group(0)}'. "
                        "Public APIs likely to refuse — suggest "
                        "fed-local-uncensored."
                    ),
                )

    # ── Tier 5: Default Public Production ────────────────────────────
    return IntentClassification(
        intent=ShadowIntent.PUBLIC_PRODUCTION,
        tier=5,
        tier_label=TIER_LABELS[5],
        suggested_signature="fed-reasoning-heavy",
        suggested_content_class="general",
        isolation_required=False,
        privacy_flag=False,
        matched_keywords=(),
        rationale="No shadow-intent signals detected. Standard public production route.",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Composition helper for LocalRuntimeRouter
# ─────────────────────────────────────────────────────────────────────────────


def enrich_payload_with_intent(
    payload: dict[str, Any],
    classification: IntentClassification,
) -> dict[str, Any]:
    """
    Apply classification hints to a payload dict BEFORE handing to
    LocalRuntimeRouter. Non-destructive — does NOT overwrite user-provided
    content_class unless it's a default.

    Adds fields:
      - intent_classification: the ShadowIntent enum value
      - intent_tier: int tier number
      - intent_rationale: one-line explanation
      - privacy_flag: bool (Tier 1/4 only)
      - isolation_required: bool (Tier 2/3 only)

    If payload has no content_class, fills with classification's suggestion.
    """
    enriched = dict(payload)
    enriched["intent_classification"] = classification.intent.value
    enriched["intent_tier"] = classification.tier
    enriched["intent_rationale"] = classification.rationale
    enriched["privacy_flag"] = classification.privacy_flag
    enriched["isolation_required"] = classification.isolation_required
    if "content_class" not in enriched:
        enriched["content_class"] = classification.suggested_content_class
    return enriched