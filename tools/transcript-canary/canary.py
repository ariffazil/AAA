#!/usr/bin/env python3
"""
transcript_canary_v0 — Bounded probe for YouTube transcript reachability.

Tests:
  1. URL/video-ID normalization (watch, youtu.be, shorts, embed)
  2. Transcript fetch attempt against a fixed public canary video
  3. Structured receipt output

Does NOT:
  - Download video/audio
  - Use cookies or yt-dlp
  - Write to Telegram or external services
  - Summarize or infer claims
  - Persist raw transcripts

Output: JSON receipt to stdout.
"""

import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

# ── Canary config ──────────────────────────────────────────────
# Rick Astley - Never Gonna Give You Up: universally captioned, public, 3:33
CANARY_VIDEO_ID = "dQw4w9WgXcQ"
CANARY_LANGUAGES = ["en"]
CANARY_TIMEOUT_S = 15

# ── URL normalization ──────────────────────────────────────────
URL_PATTERNS = [
    (r'(?:v=|youtu\.be/|shorts/|embed/|live/)([a-zA-Z0-9_-]{11})', 'standard'),
    (r'^([a-zA-Z0-9_-]{11})$', 'raw_id'),
]


def extract_video_id(url_or_id: str) -> tuple:
    """Extract 11-char video ID. Returns (video_id, match_method)."""
    url_or_id = url_or_id.strip()
    for pattern, method in URL_PATTERNS:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1), method
    return url_or_id, 'unrecognized'


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ── Normalization tests ────────────────────────────────────────
def test_normalization():
    """Test URL normalization for all supported formats."""
    cases = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "watch"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ", "youtu_be"),
        ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ", "shorts"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ", "embed"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&si=abc123", "dQw4w9WgXcQ", "watch_with_params"),
        ("dQw4w9WgXcQ", "dQw4w9WgXcQ", "raw_id"),
        ("https://www.youtube.com/watch?v=_zhkYVB8nb0&si=40Ncow8G1MaHc2gv", "_zhkYVB8nb0", "watch_underscore"),
    ]
    results = []
    all_pass = True
    for url, expected_id, label in cases:
        extracted_id, method = extract_video_id(url)
        passed = extracted_id == expected_id
        if not passed:
            all_pass = False
        results.append({
            "input": url,
            "expected": expected_id,
            "extracted": extracted_id,
            "method": method,
            "pass": passed,
            "label": label,
        })
    return all_pass, results


# ── Transcript fetch ───────────────────────────────────────────
def attempt_transcript(video_id: str, languages: list = None, timeout_s: int = 15):
    """
    Attempt to fetch transcript. Returns structured result.
    Handles IP blocks, missing transcripts, disabled transcripts.
    """
    start_time = time.time()
    result = {
        "attempted": True,
        "video_id": video_id,
        "segment_count": 0,
        "duration_seconds_estimate": 0.0,
        "languages_available": [],
        "language_selected": None,
        "has_timestamps": False,
        "content_class": "transcript_observation",
        "fetch_error": None,
        "fetch_duration_ms": 0,
    }

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        result["fetch_error"] = "youtube_transcript_api not installed"
        result["fetch_duration_ms"] = int((time.time() - start_time) * 1000)
        return result

    try:
        api = YouTubeTranscriptApi()

        # First: list available transcripts (to get language info)
        transcript_list = api.list(video_id)
        available_langs = []
        for t in transcript_list:
            lang = getattr(t, 'language_code', None) or getattr(t, 'language', 'unknown')
            available_langs.append(lang)
        result["languages_available"] = available_langs

        # Select language
        selected_lang = None
        if languages:
            for lang in languages:
                if lang in available_langs:
                    selected_lang = lang
                    break
        if not selected_lang and available_langs:
            selected_lang = available_langs[0]
        result["language_selected"] = selected_lang

        # Fetch transcript
        if selected_lang:
            fetched = api.fetch(video_id, languages=[selected_lang])
        else:
            fetched = api.fetch(video_id)

        segments = [
            {"text": seg.text, "start": seg.start, "duration": seg.duration}
            for seg in fetched
        ]

        result["segment_count"] = len(segments)
        if segments:
            last = segments[-1]
            result["duration_seconds_estimate"] = round(last["start"] + last["duration"], 1)
            result["has_timestamps"] = all("start" in s for s in segments)

        # Hash the transcript content for provenance
        transcript_json = json.dumps(segments, ensure_ascii=False).encode()
        result["manifest_sha256"] = sha256_hex(transcript_json)

    except Exception as e:
        error_str = str(e)
        if "blocked" in error_str.lower() or "429" in error_str:
            result["fetch_error"] = "IP_BLOCKED_BY_YOUTUBE"
        elif "disabled" in error_str.lower():
            result["fetch_error"] = "TRANSCRIPTS_DISABLED"
        elif "no transcript" in error_str.lower() or "not available" in error_str.lower():
            result["fetch_error"] = "NO_TRANSCRIPT_AVAILABLE"
        elif "private" in error_str.lower() or "unavailable" in error_str.lower():
            result["fetch_error"] = "VIDEO_PRIVATE_OR_UNAVAILABLE"
        else:
            result["fetch_error"] = f"FETCH_FAILED: {error_str[:200]}"

    result["fetch_duration_ms"] = int((time.time() - start_time) * 1000)
    return result


# ── Canary failure cases ──────────────────────────────────────
def test_failure_cases():
    """Test structured failure for private/missing/disabled inputs."""
    cases = [
        ("MISSING_VIDEO_ID", "missing_video"),
        ("", "empty_id"),
    ]
    results = []
    for video_id, label in cases:
        r = attempt_transcript(video_id)
        has_error = r["fetch_error"] is not None
        results.append({
            "label": label,
            "video_id": video_id,
            "has_structured_error": has_error,
            "error": r["fetch_error"],
        })
    return results


# ── Main ───────────────────────────────────────────────────────
def run_canary():
    now = datetime.now(timezone.utc).isoformat()
    receipt = {
        "run_id": f"transcript-canary:v0:{hashlib.md5(now.encode()).hexdigest()[:8]}",
        "capability_id": "media.youtube.transcript",
        "epoch": now,
        "status": "pending",
        "input": {
            "canary_video_id": CANARY_VIDEO_ID,
            "canary_url": f"https://www.youtube.com/watch?v={CANARY_VIDEO_ID}",
        },
        "normalization": {},
        "evidence": {},
        "network": {
            "allowed": True,
            "media_downloaded": False,
            "cookies_used": False,
            "external_write": False,
        },
        "failure_cases": [],
        "error": None,
    }

    # ── Test 1: Normalization ──
    norm_pass, norm_results = test_normalization()
    receipt["normalization"] = {
        "all_pass": norm_pass,
        "cases_tested": len(norm_results),
        "details": norm_results,
    }

    # ── Test 2: Transcript fetch ──
    transcript_result = attempt_transcript(
        CANARY_VIDEO_ID,
        languages=CANARY_LANGUAGES,
        timeout_s=CANARY_TIMEOUT_S,
    )
    receipt["evidence"] = transcript_result

    # ── Test 3: Failure cases ──
    failure_results = test_failure_cases()
    receipt["failure_cases"] = failure_results

    # ── Determine status ──
    if transcript_result["fetch_error"]:
        if transcript_result["fetch_error"] == "IP_BLOCKED_BY_YOUTUBE":
            receipt["status"] = "unreachable"
            receipt["error"] = "YouTube blocks transcript API from this IP (cloud provider). Route is implemented but not reachable from this network."
        else:
            receipt["status"] = "unreachable"
            receipt["error"] = transcript_result["fetch_error"]
    elif transcript_result["segment_count"] > 0:
        receipt["status"] = "reachable"
    else:
        receipt["status"] = "unreachable"
        receipt["error"] = "No segments returned"

    # ── Manifest hash ──
    receipt_bytes = json.dumps(receipt, ensure_ascii=False, indent=2).encode()
    receipt["manifest_sha256"] = sha256_hex(receipt_bytes)

    return receipt


if __name__ == "__main__":
    receipt = run_canary()
    print(json.dumps(receipt, ensure_ascii=False, indent=2))

    # Exit code: 0 = reachable, 1 = unreachable (expected from cloud)
    if receipt["status"] == "reachable":
        sys.exit(0)
    else:
        sys.exit(1)
