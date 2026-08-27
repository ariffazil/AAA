#!/usr/bin/env python3
"""
forge-vision-densify :: densify.py

Stage 1 heuristic expander. Computes density_lower from a prompt's concept
coverage before any diffusion call. Pure math. No API round-trip.

Constitutional binding: F2 TRUTH (no naked {url, status}) + F9 ANTI-HANTU
(the limit is structural, not advisory).

Usage:
    from densify import densify
    result = densify("a man standing in a park")
    # result["density_lower"]
    # result["densified_prompt"]
    # result["anchor_required"]
"""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


# Concept coverage factors (per doctrine)
WEIGHTS: Dict[str, float] = {
    "subject_identity": 1.00,
    "subject_pose": 0.80,
    "primary_material": 0.60,
    "background_scene": 0.40,
    "lighting_lens": 0.30,
    "atmospheric_tone": 0.15,
}

# Sum of weights = 3.25. Normalized = factor / 3.25 gives density in [0, 1].

# Hard-gate triggers (geometric / structural / numerical)
HARD_GATE_PATTERNS: List[re.Pattern] = [
    re.compile(r"\b\d+\s*(?:degrees?|deg|°)\b", re.IGNORECASE),
    re.compile(r"\bisometric\b", re.IGNORECASE),
    re.compile(r"\b(?:top-?down|orthographic|technical drawing)\b", re.IGNORECASE),
    re.compile(r"\b(?:fault line|wellbore|well log|seismic|horizon|stratigraph)\w*", re.IGNORECASE),
    re.compile(r"\bk-?dip\b", re.IGNORECASE),
    re.compile(r"(?:\d+(?:\.\d+)?)\s*(?:km|m|cm|mm)\s+(?:depth|away|scale|width|height)", re.IGNORECASE),
    re.compile(r"\b(?:NW|NE|SW|SE|N|S|E|W|–|-|→|strike|dip)\b", re.IGNORECASE),
    re.compile(r"\b(?:caption|labeled?|text on image|renders? \"[^\"]+\")\b", re.IGNORECASE),
]

# Heuristic concept detector. Each category gets a presence bool.
# Each bool defaults to False. Loose-keyword matching; falsifiable within
# the limits of pre-API inference.
CONCEPT_KEYWORDS: Dict[str, List[str]] = {
    "subject_identity": [
        # identity-bearing words: who is the subject
        "man", "woman", "person", "child", "elder", "portrait", "figure",
        "boy", "girl", "model", "athlete", "musician", "worker", "soldier",
        "doctor", "chef", "engineer", "student", "painter", "dancer",
        # identity-augmenting descriptors
        "asian", "malay", "chinese", "indian", "european", "african",
        "brown", "tan", "pale", "dark skin", "fair skin",
        "beard", "bald", "long hair", "short hair", "glasses",
    ],
    "subject_pose": [
        "sitting", "standing", "walking", "running", "leaning", "kneeling",
        "looking", "smiling", "frowning", "arms crossed", "hands on",
        "crouching", "jumping", "reaching", "pointing", "flexing",
        "lying", "posed", "mid-action", "profile", "three-quarter",
    ],
    "primary_material": [
        # clothing + visible material
        "shirt", "t-shirt", "henley", "jacket", "suit", "dress", "hoodie",
        "jeans", "shorts", "skirt", "trousers", "leather", "denim",
        "cotton", "silk", "wool", "linen", "metal", "gold", "silver",
        "plastic", "glass", "wood", "stone", "concrete", "fabric",
    ],
    "background_scene": [
        # setting
        "room", "office", "street", "rooftop", "park", "forest", "desert",
        "beach", "city", "urban", "rural", "indoor", "outdoor", "studio",
        "kitchen", "bedroom", "cafe", "restaurant", "stage", "platform",
        "rooftop", "skyline", "skyscraper", "jungle", "mountain",
    ],
    "lighting_lens": [
        "light", "lit", "lighting", "golden hour", "blue hour", "sunlight",
        "shade", "shadow", "rim light", "fill light", "key light",
        "studio light", "softbox", "backlight", "overhead",
        "lens", "mm", "f/", "f-stop", "bokeh", "depth of field",
        "wide angle", "telephoto", "portrait lens", "macro",
        "85mm", "50mm", "35mm", "24mm", "iso", "exposure",
    ],
    "atmospheric_tone": [
        "mood", "tone", "vibe", "atmosphere", "moody", "dark",
        "bright", "warm", "cool", "misty", "foggy", "rainy",
        "sunny", "cloudy", "hazy", "ethereal", "dreamy",
        "cinematic", "noir", "pastel", "vibrant", "muted",
    ],
}


@dataclass
class DensifyResult:
    """Output of densify(). All fields required by the JSON contract."""

    prompt_original: str
    prompt_densified: str
    density_lower: float
    anchor_required: bool
    anchor_suggestion: Optional[str]
    hard_gate_reason: Optional[str]
    concept_presence: Dict[str, bool]
    concept_specification: Dict[str, int]


def _detect_concepts(text: str) -> Dict[str, bool]:
    """Return presence bool for each concept category. Keyword loose-match."""
    lowered = text.lower()
    presence: Dict[str, bool] = {}
    for category, keywords in CONCEPT_KEYWORDS.items():
        presence[category] = any(kw in lowered for kw in keywords)
    return presence


def _count_specifications(text: str) -> Dict[str, int]:
    """Count how many keywords in each category are present in the prompt.

    This is the SPECIFICATION credit signal — categories with ≥2 keywords
    are considered fully specified, categories with 1 keyword are
    present-but-sparse, absent categories give zero credit.

    Returns dict {category: int count}.
    """
    lowered = text.lower()
    counts: Dict[str, int] = {}
    for category, keywords in CONCEPT_KEYWORDS.items():
        # word-boundary match so "cape" doesn't count as "cap" etc.
        n = sum(1 for kw in keywords if kw in lowered)
        counts[category] = n
    return counts


def _hard_gate_check(text: str) -> Optional[str]:
    """Return reason string if hard gate fires, else None."""
    for pat in HARD_GATE_PATTERNS:
        match = pat.search(text)
        if match:
            return f"geometry_pattern:{match.group(0)}"
    return None


def _build_densified_prompt(
    original: str,
    presence: Dict[str, bool],
    hard_gate_reason: Optional[str],
) -> str:
    """Expand sparse prompts into constraint specification.

    This is the densification step. We do NOT inject creative content
    that wasn't in the original; we ONLY normalize and structure what
    is there. Missing concepts become explicit placeholders, NOT
    fabricated details.
    """
    if hard_gate_reason:
        return (
            f"[HARD-GATE INTERCEPT] anchor_required=True | reason={hard_gate_reason}. "
            "Structural anchor (ControlNet/Depth/Ip-Adapter) required before "
            "diffusion. Original prompt: " + original
        )

    segments: List[str] = [f"Original intent: {original}."]
    segments.append("[Constraint specification — only what's in your prompt:]")

    if presence["subject_identity"]:
        segments.append("- subject_identity: covered")
    else:
        segments.append(
            "- subject_identity: NOT SPECIFIED — model must invent. "
            "WARNING: high hallucination risk on who/what the subject is."
        )

    if presence["subject_pose"]:
        segments.append("- subject_pose: covered")
    else:
        segments.append(
            "- subject_pose: NOT SPECIFIED — model must invent body position."
        )

    if presence["primary_material"]:
        segments.append("- primary_material: covered")
    else:
        segments.append(
            "- primary_material: NOT SPECIFIED — model must invent clothing/objects."
        )

    if presence["background_scene"]:
        segments.append("- background_scene: covered")
    else:
        segments.append(
            "- background_scene: NOT SPECIFIED — model must invent setting. "
            "Highest hallucination surface."
        )

    if presence["lighting_lens"]:
        segments.append("- lighting_lens: covered")
    else:
        segments.append(
            "- lighting_lens: NOT SPECIFIED — model must invent lighting. "
            "Disclosure required."
        )

    if presence["atmospheric_tone"]:
        segments.append("- atmospheric_tone: covered")
    else:
        segments.append(
            "- atmospheric_tone: NOT SPECIFIED — mood will be model-default."
        )

    return "\n".join(segments)


def _suggest_anchor(hard_gate_reason: Optional[str]) -> Optional[str]:
    """What kind of anchor would help, given the hard-gate reason."""
    if hard_gate_reason is None:
        return None
    reason = hard_gate_reason.lower()
    if "well" in reason or "seismic" in reason or "horizon" in reason or "stratigraph" in reason:
        return "controlnet_depth_or_scribble"
    if "caption" in reason or "text" in reason:
        return "controlnet_canny_or_pixel_art"
    if "degrees" in reason or "isometric" in reason or "orthographic" in reason:
        return "controlnet_depth"
    if "km" in reason or "cm" in reason or "scale" in reason:
        return "controlnet_depth"
    if "strike" in reason or "dip" in reason or "nw" in reason:
        return "controlnet_scribble_with_geo_overlay"
    return "controlnet_or_ip_adapter"


def densify(prompt: str) -> DensifyResult:
    """Compute density_lower for a prompt and produce the densification struct.

    Args:
        prompt: raw human prompt, possibly sparse.

    Returns:
        DensifyResult with all fields populated.

    Side effects: none. Pure function over the prompt string.
    """
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")

    presence = _detect_concepts(prompt)
    hard_gate = _hard_gate_check(prompt)

    # Compute density_lower. Hard-gated prompts skip concept math.
    # Concepts get SPECIFICATION credit, not presence credit.
    #   full  = category present AND fully specified (multiple keywords in category)
    #   partial = category present but sparse (single keyword)
    #   zero   = category absent
    if hard_gate is not None:
        specification_counts = _count_specifications(prompt)  # for receipt only
        density_lower = 0.0  # hard-gated means anchor required, no diffusion yet
    else:
        specification_counts = _count_specifications(prompt)
        weighted_sum = 0.0
        for category, present in presence.items():
            if not present:
                credit = 0.0
            else:
                # require ≥2 keywords in category for "full specification" credit
                count = specification_counts.get(category, 0)
                if count >= 2:
                    credit = 1.0
                elif count == 1:
                    credit = 0.4  # present but sparse
                else:
                    credit = 0.0
            weighted_sum += WEIGHTS[category] * credit
        density_lower = round(weighted_sum / sum(WEIGHTS.values()), 4)

    prompt_densified = _build_densified_prompt(prompt, presence, hard_gate)
    anchor_suggestion = _suggest_anchor(hard_gate) if hard_gate else None

    return DensifyResult(
        prompt_original=prompt,
        prompt_densified=prompt_densified,
        density_lower=density_lower,
        anchor_required=hard_gate is not None,
        anchor_suggestion=anchor_suggestion,
        hard_gate_reason=hard_gate,
        concept_presence=presence,
        concept_specification=specification_counts,
    )


def to_receipt_fragment(result: DensifyResult) -> Dict:
    """Convert DensifyResult into the JSON receipt fragment for pre-diffusion."""
    return {
        "f1_safe": None,  # populated post-VLM
        "f2_adherence": None,  # populated post-VLM
        "prompt_density": result.density_lower,
        "hallucinated_elements": [],  # populated post-VLM
        "anchor_required": result.anchor_required,
        "anchor_suggestion": result.anchor_suggestion,
    }


if __name__ == "__main__":
    # Smoke test
    test_prompts = [
        "a man standing in a park",
        "Caucasian male, 30s, navy suit, white shirt, red tie, golden hour, 85mm portrait lens, rooftop, bokeh",
        "show me a fault dipping 45 degrees NW-SE",
        "label the three horizons: Topaz, Jasper, Onyx",
        "portrait of a young Malay woman, traditional baju kurung, golden hour sidelight, soft bokeh, KLCC background",
    ]
    for tp in test_prompts:
        r = densify(tp)
        print(f"\nPROMPT: {tp!r}")
        print(f"  density_lower       = {r.density_lower}")
        print(f"  anchor_required     = {r.anchor_required}")
        print(f"  hard_gate_reason    = {r.hard_gate_reason}")
        print(f"  concept_presence    = {r.concept_presence}")
        print(f"  concept_spec_count  = {r.concept_specification}")
