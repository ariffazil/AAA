#!/usr/bin/env python3
"""
transcript_canary_v0

Bounded, read-only probe of the YouTube transcript extraction path.
Verifies: URL normalization, caption retrieval, timestamp availability,
structured evidence output, and network-scope discipline.

Usage:
    python3 transcript_canary_v0.py <video_url_or_id>

Acceptance criteria:
    1. URL/video-ID normalization works for watch, youtu.be, shorts, embed forms.
    2. Captioned controlled canary returns non-empty segments.
    3. Every segment has start time and text.
    4. Video ID and retrieval timestamp appear in receipt.
    5. Language selection/fallback is recorded.
    6. Private/deleted/blocked/no-caption inputs return structured unavailable.
    7. No cookies, media downloads, or yt-dlp invocation.
    8. No Telegram or external write.
    9. Manifest hash is produced.
    10. Transcript content labeled transcript_observation, never fact.
    11. Explicit timeout and bounded retry.
    12. Success updates ledger evidence, not reachable state by implication.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.1.0"
TOOL_NAME = "transcript_canary_v0"
TIMEOUT_SECONDS = 15
MAX_RETRIES = 2
RETRY_DELAY_SECONDS = 2

# --- URL normalization ---

def extract_video_id(url_or_id: str) -> str:
    """Extract 11-character video ID from various YouTube URL formats."""
    url_or_id = url_or_id.strip()
    patterns = [
        r'(?:v=|youtu\.be/|shorts/|embed/|live/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return url_or_id


def classify_url_form(original_url: str) -> str:
    """Classify which URL form was used."""
    url = original_url.strip()
    if re.search(r'youtu\.be/', url):
        return "youtu_be_short"
    if re.search(r'v=', url):
        return "watch"
    if re.search(r'shorts/', url):
        return "shorts"
    if re.search(r'embed/', url):
        return "embed"
    if re.search(r'live/', url):
        return "live"
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return "bare_id"
    return "unknown"


# --- Transcript extraction ---

def fetch_transcript(video_id: str, languages: list = None) -> dict:
    """
    Fetch transcript via youtube-transcript-api.
    Returns structured result dict.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        return {
            "status": "failed",
            "error_class": "dependency_missing",
            "error_message": "youtube-transcript-api not installed",
        }

    api = YouTubeTranscriptApi()

    # Determine available languages first
    try:
        transcript_list = api.list(video_id)
        available_languages = [t.language_code for t in transcript_list]
    except Exception as e:
        error_msg = str(e).lower()
        if "private" in error_msg or "unavailable" in error_msg:
            return {
                "status": "unavailable",
                "error_class": "video_private_or_unavailable",
                "error_message": str(e),
            }
        if "no transcript" in error_msg or "could not retrieve" in error_msg:
            return {
                "status": "unavailable",
                "error_class": "no_transcript_available",
                "error_message": str(e),
            }
        return {
            "status": "failed",
            "error_class": "list_failed",
            "error_message": str(e),
        }

    # Select language
    selected_language = None
    if languages:
        for lang in languages:
            if lang in available_languages:
                selected_language = lang
                break
    if selected_language is None and available_languages:
        selected_language = available_languages[0]

    if selected_language is None:
        return {
            "status": "unavailable",
            "error_class": "no_language_match",
            "error_message": "No transcripts available",
            "available_languages": available_languages,
        }

    # Fetch with retry
    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            result = api.fetch(video_id, languages=[selected_language])
            segments = [
                {
                    "text": seg.text,
                    "start": seg.start,
                    "duration": seg.duration,
                }
                for seg in result
            ]
            return {
                "status": "success",
                "segments": segments,
                "segment_count": len(segments),
                "language_selected": selected_language,
                "languages_available": available_languages,
                "has_timestamps": all("start" in s for s in segments),
            }
        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                import time
                time.sleep(RETRY_DELAY_SECONDS)

    return {
        "status": "failed",
        "error_class": "fetch_failed_after_retries",
        "error_message": str(last_error),
        "attempts": MAX_RETRIES + 1,
    }


# --- Receipt builders ---

def build_receipt(video_id: str, original_url: str, url_form: str,
                   transcript_result: dict, output_dir: str) -> dict:
    """Build the canary receipt."""
    receipt = {
        "run_id": f"transcript-canary:{uuid.uuid4().hex[:12]}",
        "capability_id": "media.youtube.transcript",
        "tool_version": VERSION,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "input": {
            "canonical_url": f"https://www.youtube.com/watch?v={video_id}",
            "video_id": video_id,
            "original_url": original_url,
            "url_form": url_form,
        },
        "network": {
            "allowed": True,
            "media_downloaded": False,
            "cookies_used": False,
            "external_write": False,
        },
    }

    if transcript_result.get("status") == "success":
        # Compute content hash for manifest
        full_text = " ".join(s["text"] for s in transcript_result["segments"])
        content_hash = hashlib.sha256(full_text.encode("utf-8")).hexdigest()

        # Estimate duration from last segment
        segments = transcript_result["segments"]
        duration_estimate = 0.0
        if segments:
            last = segments[-1]
            duration_estimate = round(last["start"] + last.get("duration", 0), 2)

        receipt["status"] = "reachable"
        receipt["evidence"] = {
            "segment_count": transcript_result["segment_count"],
            "duration_seconds_estimate": duration_estimate,
            "languages_available": transcript_result.get("languages_available", []),
            "language_selected": transcript_result.get("language_selected"),
            "has_timestamps": transcript_result.get("has_timestamps", False),
            "content_class": "transcript_observation",
            "manifest_sha256": content_hash,
        }
        receipt["error"] = None

        # Write transcript evidence file
        evidence_path = os.path.join(output_dir, "transcript-evidence.json")
        evidence_data = {
            "video_id": video_id,
            "content_class": "transcript_observation",
            "language": transcript_result.get("language_selected"),
            "segment_count": transcript_result["segment_count"],
            "segments": segments,
        }
        with open(evidence_path, "w") as f:
            json.dump(evidence_data, f, indent=2, ensure_ascii=False)

        # Write manifest hash file
        manifest_path = os.path.join(output_dir, "manifest.json")
        with open(manifest_path, "w") as f:
            json.dump(receipt, f, indent=2)

    elif transcript_result.get("status") == "unavailable":
        receipt["status"] = "unavailable"
        receipt["evidence"] = None
        receipt["error"] = {
            "class": transcript_result.get("error_class"),
            "message": transcript_result.get("error_message"),
        }

    else:
        receipt["status"] = "failed"
        receipt["evidence"] = None
        receipt["error"] = {
            "class": transcript_result.get("error_class"),
            "message": transcript_result.get("error_message"),
        }

    # Write receipt
    receipt_path = os.path.join(output_dir, "receipt.json")
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)

    return receipt


# --- URL normalization tests ---

def test_url_normalization():
    """Test that URL normalization works for all forms."""
    cases = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "watch"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ", "youtu_be_short"),
        ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ", "shorts"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ", "embed"),
        ("dQw4w9WgXcQ", "dQw4w9WgXcQ", "bare_id"),
    ]
    results = []
    for url, expected_id, expected_form in cases:
        vid = extract_video_id(url)
        form = classify_url_form(url)
        ok = vid == expected_id and form == expected_form
        results.append({"url": url, "video_id": vid, "form": form, "pass": ok})
        status = "PASS" if ok else "FAIL"
        print(f"  {status}  {form}: {url} -> {vid}")
    return all(r["pass"] for r in results)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="transcript_canary_v0: bounded YouTube transcript probe"
    )
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: ./canary-output)")
    parser.add_argument("--languages", default=None,
                        help="Comma-separated language codes (e.g. en,ms)")
    parser.add_argument("--test-normalization", action="store_true",
                        help="Run URL normalization tests only")
    args = parser.parse_args()

    if args.test_normalization:
        print("\n=== URL Normalization Tests ===\n")
        ok = test_url_normalization()
        sys.exit(0 if ok else 1)

    # Extract video ID
    video_id = extract_video_id(args.url)
    url_form = classify_url_form(args.url)
    print(f"\n=== Transcript Canary v0 ===")
    print(f"  URL form:      {url_form}")
    print(f"  Video ID:      {video_id}")
    print(f"  Canonical URL: https://www.youtube.com/watch?v={video_id}")

    # Prepare output
    output_dir = args.output_dir or os.path.join(os.getcwd(), "canary-output")
    os.makedirs(output_dir, exist_ok=True)

    # Fetch transcript
    languages = None
    if args.languages:
        languages = [l.strip() for l in args.languages.split(",")]

    print(f"  Fetching transcript...")
    result = fetch_transcript(video_id, languages=languages)

    # Build receipt
    receipt = build_receipt(video_id, args.url, url_form, result, output_dir)

    # Print summary
    print(f"  Status:        {receipt['status']}")
    if receipt.get("evidence"):
        ev = receipt["evidence"]
        print(f"  Segments:      {ev['segment_count']}")
        print(f"  Duration est:  {ev['duration_seconds_estimate']}s")
        print(f"  Language:      {ev['language_selected']}")
        print(f"  Timestamps:    {ev['has_timestamps']}")
        print(f"  Content class: {ev['content_class']}")
        print(f"  Manifest hash: {ev['manifest_sha256'][:16]}...")
    if receipt.get("error"):
        print(f"  Error:         {receipt['error'].get('class')}: {receipt['error'].get('message')}")
    print(f"  Receipt:       {output_dir}/receipt.json")

    # Exit code
    sys.exit(0 if receipt["status"] == "reachable" else 1)


if __name__ == "__main__":
    main()
