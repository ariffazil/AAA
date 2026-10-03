"""
Media Artifact Capability Map — extends mission_router for inbound media artifacts.

Maps semantic media/URL capabilities to the canonical media-ingest MCP tools
(HERMES) or to be routed to the AAA media-ingest-lane skill (cross-harness).

Capability → Tool resolution is the SAME pattern as mission_router/capability_resolver.py
but for INTAKE (what user just pasted) rather than MISSION (what pipeline to run).

Why this lives here, not in capability_resolver.py:
- capability_resolver.py is for in-mission semantic capabilities (system_health,
  capital_diagnosis, etc). Those are internal federation verbs.
- Media artifacts are USER INTAKE — they cross the boundary into the system.
- Keeping them separate preserves the mission_router invariant while extending
  intake coverage.

Wired to media-ingest-lane SKILL.md as canonical procedure (per AAA/SKILL.md
"Rule 0 — probe, then either read it or state the block").

Truth-state semantics (per media-ingest-lane):
  METADATA_OBSERVED ≠ TRANSCRIPT_OBSERVED ≠ VISUAL_OBSERVED ≠ MEDIA_OBSERVED ≠ CONTENT_UNDERSTOOD

Failure recovery (per arifOS doctrine):
  TOOL_FAILURE ≠ TASK_FAILURE ≠ HUMAN_HANDOFF
  On failure: classify → discover alternative → rank → attempt bounded fallback → verify
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import re


class ArtifactClass(str, Enum):
    """Inbound artifact taxonomy. 7 classes per arifOS spec."""
    YOUTUBE_URL = "youtube_url"           # youtu.be / youtube.com/watch
    GENERIC_WEB_URL = "web_url"           # article, blog, docs
    PDF = "pdf"                            # .pdf or application/pdf
    IMAGE = "image"                        # .jpg/.png/.gif/.webp
    AUDIO = "audio"                        # .mp3/.ogg/.wav/.m4a
    CODE_FILE = "code"                     # .py/.ts/.js/.sh/.md
    TEXT_QUESTION = "text"                 # 1-3 sentence BM/EN question
    UNKNOWN = "unknown"                    # cannot classify


class TruthState(str, Enum):
    """Per media-ingest-lane: epistemic layer that was actually read."""
    METADATA_OBSERVED = "METADATA_OBSERVED"      # oEmbed, headers, page title
    TRANSCRIPT_OBSERVED = "TRANSCRIPT_OBSERVED"  # STT/Whisper text content
    VISUAL_OBSERVED = "VISUAL_OBSERVED"          # vision_analyze on frames
    MEDIA_OBSERVED = "MEDIA_OBSERVED"            # bytes downloaded + parsed
    CONTENT_UNDERSTOOD = "CONTENT_UNDERSTOOD"    # synthesized across layers
    BLOCKED = "BLOCKED"                          # all bounded paths exhausted
    PARTIAL = "PARTIAL"                          # some layers observed, some failed


# URL patterns ordered by specificity (most specific first)
URL_PATTERNS = [
    (ArtifactClass.YOUTUBE_URL,
     re.compile(r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_-]{11}", re.IGNORECASE)),
    (ArtifactClass.PDF,
     re.compile(r"\.pdf(\?.*)?$", re.IGNORECASE)),
    (ArtifactClass.IMAGE,
     re.compile(r"\.(?:jpg|jpeg|png|gif|webp|bmp|tiff)(\?.*)?$", re.IGNORECASE)),
    (ArtifactClass.AUDIO,
     re.compile(r"\.(?:mp3|ogg|wav|m4a|flac|aac)(\?.*)?$", re.IGNORECASE)),
    (ArtifactClass.CODE_FILE,
     re.compile(r"\.(?:py|ts|js|sh|md|yaml|yml|json|sql|tsx|jsx)(\?.*)?$", re.IGNORECASE)),
    (ArtifactClass.GENERIC_WEB_URL,
     re.compile(r"https?://[^\s/$.?#].[^\s]*", re.IGNORECASE)),
]


def classify(artifact: str) -> ArtifactClass:
    """
    Classify inbound artifact into one of 8 classes.

    Order: most specific URL patterns first. If no URL, look at extension
    or fall back to TEXT_QUESTION for short prose, UNKNOWN for ambiguous.
    """
    if not artifact or not artifact.strip():
        return ArtifactClass.UNKNOWN

    s = artifact.strip()
    for cls, pat in URL_PATTERNS:
        if pat.search(s):
            return cls

    # File path style (no http:// prefix)
    if s.startswith(("/", "~/", "./", "../")):
        if re.search(r"\.pdf$", s, re.IGNORECASE):
            return ArtifactClass.PDF
        if re.search(r"\.(?:jpg|jpeg|png|gif|webp)$", s, re.IGNORECASE):
            return ArtifactClass.IMAGE
        if re.search(r"\.(?:mp3|ogg|wav|m4a)$", s, re.IGNORECASE):
            return ArtifactClass.AUDIO
        if re.search(r"\.(?:py|ts|js|sh|md|yaml|yml|json)$", s, re.IGNORECASE):
            return ArtifactClass.CODE_FILE
        return ArtifactClass.UNKNOWN

    # Bare text
    word_count = len(s.split())
    if word_count <= 30:
        return ArtifactClass.TEXT_QUESTION
    return ArtifactClass.UNKNOWN


# Resolution: each artifact class → one or more canonical tool paths
# in priority order. Cross-harness aware.
RESOLUTION: dict[ArtifactClass, list[dict]] = {
    ArtifactClass.YOUTUBE_URL: [
        # Tier 1: media_ingest_url MCP (canonical, runs yt-dlp + transcript + frames)
        {"organ": "media-ingest", "tool": "media_ingest_url",
         "canonical": True, "tier": 1},
        # Tier 2: oEmbed (no JS, 200ms, metadata only — not transcript)
        {"organ": "shell", "tool": "curl_youtube_oembed",
         "truth_state": TruthState.METADATA_OBSERVED, "tier": 2},
        # Tier 3: yt-dlp direct
        {"organ": "shell", "tool": "yt_dlp_metadata",
         "truth_state": TruthState.METADATA_OBSERVED, "tier": 3},
    ],
    ArtifactClass.GENERIC_WEB_URL: [
        {"organ": "hermes", "tool": "web_extract", "canonical": True, "tier": 1},
    ],
    ArtifactClass.PDF: [
        {"organ": "hermes", "tool": "web_extract", "canonical": True, "tier": 1},
        {"organ": "hermes", "tool": "read_file", "tier": 2},
    ],
    ArtifactClass.IMAGE: [
        {"organ": "hermes", "tool": "vision_analyze", "canonical": True, "tier": 1},
    ],
    ArtifactClass.AUDIO: [
        {"organ": "media-ingest", "tool": "media_ingest_url", "tier": 1},
        {"organ": "media-ingest", "tool": "media_ingest_file", "canonical": True, "tier": 2},
    ],
    ArtifactClass.CODE_FILE: [
        {"organ": "hermes", "tool": "read_file", "tier": 1},
        {"organ": "hermes", "tool": "patch", "tier": 2},
    ],
    ArtifactClass.TEXT_QUESTION: [
        {"organ": "hermes", "tool": "respond", "tier": 1},
    ],
    ArtifactClass.UNKNOWN: [
        # UNKNOWN is itself a discoverable state — no immediate tool.
        # The discovery-reflex queries installed tools/binaries/MCP surfaces next.
        {"organ": "discovery", "tool": "self_classify", "tier": 1},
    ],
}


@dataclass
class RoutingDecision:
    """Telemetry payload for one routing decision (HBR/CUR computation)."""
    input_class: str
    capability_expected: str
    capability_selected: bool
    fallback_depth: int
    avoidable_handoff: bool
    truth_state: str
    resolution_status: str   # "RESOLVED" | "PARTIAL" | "BLOCKED"
    selected_tool: Optional[str] = None


def route(artifact: str) -> RoutingDecision:
    """
    Classify artifact and return the routing decision (telemetry).

    This function does NOT execute the tool — it returns the decision
    so the canary tests can assert on it, and so the agent can dispatch
    with telemetry emitted.
    """
    cls = classify(artifact)
    expected_cap = f"ingest:{cls.value}"
    candidates = RESOLUTION.get(cls, [])
    canonical = next((c for c in candidates if c.get("canonical")), None)
    if not canonical and candidates:
        canonical = candidates[0]

    if not canonical:
        return RoutingDecision(
            input_class=cls.value,
            capability_expected=expected_cap,
            capability_selected=False,
            fallback_depth=0,
            avoidable_handoff=True,
            truth_state=TruthState.BLOCKED.value,
            resolution_status="BLOCKED",
        )

    return RoutingDecision(
        input_class=cls.value,
        capability_expected=expected_cap,
        capability_selected=True,
        fallback_depth=0,  # 0 = first-tier hit, increment per fallback
        avoidable_handoff=False,
        # Truth state declared by tier 1 candidate (or BLOCKED for unknown)
        truth_state=canonical.get("truth_state", TruthState.METADATA_OBSERVED.value),
        resolution_status="RESOLVED",
        selected_tool=f"{canonical['organ']}.{canonical['tool']}",
    )
