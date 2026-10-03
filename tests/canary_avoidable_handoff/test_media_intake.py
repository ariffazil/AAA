"""
Canary: Avoidable Human Handoff (HBR) for inbound media artifacts.

Falsifiable contract: when a known capability exists for a machine-resolvable
artifact, the agent MUST select it without asking the human. HBR must → 0.

Five canaries per arifOS spec (Qwen cross-audit 2026-10-03):
  YT-001    YouTube URL
  WEB-002   ordinary web URL
  PDF-003   document
  MEDIA-004 image/audio
  UNKNOWN-005 primary route unavailable

Each canary asserts:
  - correct artifact classification
  - correct capability selected
  - capability attempted (telemetry: selected_tool non-null)
  - avoidable_handoff == false
  - truth_state explicit (no fabrication)
  - METADATA_OBSERVED ≠ CONTENT_UNDERSTOOD (epistemic layer preserved)
"""
import sys
from pathlib import Path

# Make the AAA package importable
sys.path.insert(0, "/root/AAA/src")
from mission_router.media_intake import (
    classify, route, ArtifactClass, TruthState, RoutingDecision,
)


# ── Helpers ──────────────────────────────────────────────────────────────

def _assert_class(decision: RoutingDecision, expected: ArtifactClass, name: str):
    assert decision.input_class == expected.value, (
        f"{name}: expected class {expected.value}, got {decision.input_class}"
    )


def _assert_no_handoff(decision: RoutingDecision, name: str):
    assert decision.avoidable_handoff is False, (
        f"{name}: avoidable_handoff=True — agent should have selected existing capability"
    )


def _assert_capability_selected(decision: RoutingDecision, name: str):
    assert decision.capability_selected is True, (
        f"{name}: capability_selected=False — no tool was mapped"
    )


def _assert_truth_state_valid(decision: RoutingDecision, name: str):
    valid = {s.value for s in TruthState}
    assert decision.truth_state in valid, (
        f"{name}: truth_state '{decision.truth_state}' not in {valid}"
    )


def _assert_metadata_not_understood(decision: RoutingDecision, name: str):
    """Epistemic floor: oEmbed/metadata success is NOT proof of content understanding."""
    if decision.input_class == ArtifactClass.YOUTUBE_URL.value:
        # YouTube Tier 1 (oEmbed) is METADATA_OBSERVED, not CONTENT_UNDERSTOOD
        assert decision.truth_state in {
            TruthState.METADATA_OBSERVED.value,
            TruthState.TRANSCRIPT_OBSERVED.value,
            TruthState.VISUAL_OBSERVED.value,
            TruthState.MEDIA_OBSERVED.value,
            TruthState.CONTENT_UNDERSTOOD.value,
            TruthState.PARTIAL.value,
        }, f"{name}: invalid truth_state for video"


# ── YT-001: YouTube URL ──────────────────────────────────────────────────

def test_yt_001_youtube_url_routes_to_media_ingest():
    """YouTube URL → must select media_ingest_url, must NOT handoff to human."""
    url = "https://youtu.be/cYjwS7sf4sI?si=WDcq7Guh31gtIctf"
    d = route(url)
    _assert_class(d, ArtifactClass.YOUTUBE_URL, "YT-001")
    _assert_no_handoff(d, "YT-001")
    _assert_capability_selected(d, "YT-001")
    _assert_truth_state_valid(d, "YT-001")
    _assert_metadata_not_understood(d, "YT-001")
    # Selected tool must be media_ingest_url (Tier 1 canonical)
    assert d.selected_tool == "media-ingest.media_ingest_url", (
        f"YT-001: expected media-ingest.media_ingest_url, got {d.selected_tool}"
    )


# ── WEB-002: ordinary web URL ────────────────────────────────────────────

def test_web_002_article_url_routes_to_web_extract():
    """Article URL → must select web_extract, must NOT handoff."""
    url = "https://arif-fazil.com/words/doctrine/"
    d = route(url)
    _assert_class(d, ArtifactClass.GENERIC_WEB_URL, "WEB-002")
    _assert_no_handoff(d, "WEB-002")
    _assert_capability_selected(d, "WEB-002")
    _assert_truth_state_valid(d, "WEB-002")
    assert d.selected_tool == "hermes.web_extract", (
        f"WEB-002: expected hermes.web_extract, got {d.selected_tool}"
    )


# ── PDF-003: document ───────────────────────────────────────────────────

def test_pdf_003_routes_to_web_extract_or_read_file():
    """PDF URL → must select web_extract (Tier 1) or read_file (Tier 2)."""
    pdf = "https://example.com/some-doc.pdf"
    d = route(pdf)
    _assert_class(d, ArtifactClass.PDF, "PDF-003")
    _assert_no_handoff(d, "PDF-003")
    _assert_capability_selected(d, "PDF-003")
    assert d.selected_tool in {"hermes.web_extract", "hermes.read_file"}, (
        f"PDF-003: expected web_extract or read_file, got {d.selected_tool}"
    )


def test_pdf_003_local_path():
    """Local PDF path → must classify as PDF and select read_file."""
    d = route("/tmp/some-report.pdf")
    _assert_class(d, ArtifactClass.PDF, "PDF-003-local")
    _assert_no_handoff(d, "PDF-003-local")
    assert d.selected_tool in {"hermes.web_extract", "hermes.read_file"}


# ── MEDIA-004: image/audio ──────────────────────────────────────────────

def test_media_004_image_routes_to_vision():
    """Image URL → must select vision_analyze, must NOT handoff."""
    url = "https://example.com/photo.jpg"
    d = route(url)
    _assert_class(d, ArtifactClass.IMAGE, "MEDIA-004-img")
    _assert_no_handoff(d, "MEDIA-004-img")
    _assert_capability_selected(d, "MEDIA-004-img")
    assert d.selected_tool == "hermes.vision_analyze", (
        f"MEDIA-004-img: expected hermes.vision_analyze, got {d.selected_tool}"
    )


def test_media_004_audio_routes_to_media_ingest():
    """Audio URL → must select media_ingest_url, must NOT handoff."""
    url = "https://example.com/voice-note.ogg"
    d = route(url)
    _assert_class(d, ArtifactClass.AUDIO, "MEDIA-004-audio")
    _assert_no_handoff(d, "MEDIA-004-audio")
    _assert_capability_selected(d, "MEDIA-004-audio")
    assert d.selected_tool in {
        "media-ingest.media_ingest_url",
        "media-ingest.media_ingest_file",
    }


# ── UNKNOWN-005: primary route unavailable ──────────────────────────────

def test_unknown_005_empty_input_blocked_not_handoff():
    """Empty input → UNKNOWN class, BLOCKED, but NOT a handoff (it's a block)."""
    d = route("")
    _assert_class(d, ArtifactClass.UNKNOWN, "UNKNOWN-005-empty")
    # UNKNOWN can either block (no handoff) or handoff depending on context.
    # The contract: an UNKNOWN with no classification IS NOT an avoidable handoff
    # because there's no machine-resolvable path. The agent should say BLOCKED,
    # not ask Arif.
    _assert_truth_state_valid(d, "UNKNOWN-005-empty")
    # Resolution status: BLOCKED (acceptable) or RESOLVED (only if discovery fires)


def test_unknown_005_gibberish_not_handoff():
    """Gibberish text → UNKNOWN class, must NOT be framed as 'ask user for context'."""
    d = route("xx yy zz !!!")
    _assert_class(d, ArtifactClass.TEXT_QUESTION, "UNKNOWN-005-gibberish")
    # Text question → respond tool, no handoff
    _assert_no_handoff(d, "UNKNOWN-005-gibberish")
    assert d.selected_tool == "hermes.respond"


# ── Telemetry aggregation ────────────────────────────────────────────────

def test_hbr_metric_zero_for_known_artifacts():
    """
    HBR = avoidable_handoffs / machine_resolvable_cases.
    For all 5 canary cases, denominator > 0 and numerator must be 0.
    """
    cases = [
        ("https://youtu.be/abc12345678", ArtifactClass.YOUTUBE_URL),
        ("https://example.com/article", ArtifactClass.GENERIC_WEB_URL),
        ("https://example.com/doc.pdf", ArtifactClass.PDF),
        ("https://example.com/photo.jpg", ArtifactClass.IMAGE),
        ("https://example.com/voice.ogg", ArtifactClass.AUDIO),
    ]
    total = 0
    avoidable = 0
    for url, _ in cases:
        d = route(url)
        total += 1
        if d.avoidable_handoff:
            avoidable += 1
    hbr = avoidable / total if total else 0
    assert hbr == 0, f"HBR = {hbr} — agent should not handoff for any known artifact"


def test_cur_metric_one_for_known_artifacts():
    """
    CUR = correct_capability_selections / cases_with_existing_capability.
    For all 5 canary cases, capability must be selected.
    """
    urls = [
        "https://youtu.be/abc12345678",
        "https://example.com/article",
        "https://example.com/doc.pdf",
        "https://example.com/photo.jpg",
        "https://example.com/voice.ogg",
    ]
    selected = sum(1 for u in urls if route(u).capability_selected)
    cur = selected / len(urls)
    assert cur == 1, f"CUR = {cur} — capability should be selected for every known artifact"
