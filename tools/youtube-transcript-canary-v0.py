#!/usr/bin/env python3
"""
youtube-transcript-canary-v0 — Governed probe for YouTube transcript reachability.

Tests whether the youtube_transcript_api route works from this VPS.
Emits a JSON receipt (reachable / unreachable) with SHA-256 integrity.

Usage:
    python3 youtube-transcript-canary-v0.py [VIDEO_ID]

If VIDEO_ID is omitted, tests both known canary videos.
No external writes beyond receipt path. No network beyond youtube-transcript-api.
"""

import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone

RECEIPTS_DIR = "/root/AAA/knowledge-graph/receipts"
TEST_VIDEOS = {
    "7UOWhSMtX4E": "Chinese bodybuilding video (no English expected)",
    "9XlOaVItUgI": "Species AGI Drew (English expected)",
}


def _safe_error_message(exc: Exception) -> str:
    """Produce a human-readable but non-leaking error string."""
    return str(exc)[:500]


def _classify_error(exc: Exception) -> str:
    """Map youtube_transcript_api exceptions to stable error classes."""
    from youtube_transcript_api._errors import (
        RequestBlocked,
        IpBlocked,
        NoTranscriptFound,
        CouldNotRetrieveTranscript,
        VideoUnavailable,
        VideoUnplayable,
        TranscriptsDisabled,
        InvalidVideoId,
        HTTPError,
        YouTubeRequestFailed,
        AgeRestricted,
    )

    if isinstance(exc, IpBlocked):
        return "ip_blocked"
    if isinstance(exc, RequestBlocked):
        return "request_blocked"
    if isinstance(exc, NoTranscriptFound):
        return "transcript_not_found"
    if isinstance(exc, TranscriptsDisabled):
        return "transcripts_disabled"
    if isinstance(exc, CouldNotRetrieveTranscript):
        return "transcript_unavailable"
    if isinstance(exc, VideoUnavailable):
        return "video_unavailable"
    if isinstance(exc, VideoUnplayable):
        return "video_unplayable"
    if isinstance(exc, InvalidVideoId):
        return "invalid_video_id"
    if isinstance(exc, AgeRestricted):
        return "age_restricted"
    if isinstance(exc, HTTPError):
        return "http_error"
    if isinstance(exc, YouTubeRequestFailed):
        return "request_failed"

    emsg = str(exc).lower()
    if "timed out" in emsg or "timeout" in type(exc).__name__.lower():
        return "network_timeout"
    if "connection" in emsg and ("refused" in emsg or "reset" in emsg):
        return "connection_refused"
    return f"unknown:{type(exc).__name__}"


def try_fetch_transcript(video_id: str) -> dict:
    """
    Attempt to fetch transcript for a single video ID.
    Returns a partial receipt dict (caller adds run_id, timestamp, sha256).
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        api = YouTubeTranscriptApi()
        # fetch() returns FetchedTranscript (dataclass with snippets, language, etc.)
        fetched = api.fetch(video_id)

        # FetchedTranscript is iterable; each item is a FetchedTranscriptSnippet
        # with attributes: .text, .start, .duration
        snippets = list(fetched)
        total_duration = sum(s.duration for s in snippets)
        language = fetched.language or "unknown"
        first_3 = [
            {
                "start": round(s.start, 3),
                "duration": round(s.duration, 3),
                "text": s.text[:200],
            }
            for s in snippets[:3]
        ]

        return {
            "status": "reachable",
            "video_id": video_id,
            "language_detected": language,
            "language_code": fetched.language_code,
            "is_generated": fetched.is_generated,
            "segment_count": len(snippets),
            "total_duration_seconds": round(total_duration, 3),
            "first_3_segments": first_3,
        }

    except Exception as exc:
        error_class = _classify_error(exc)
        return {
            "status": "unreachable",
            "video_id": video_id,
            "error_class": error_class,
            "safe_message": _safe_error_message(exc),
        }


def run_canary(video_id: str | None = None) -> str:
    """
    Main canary entrypoint. Writes receipt and returns its path.
    If video_id is None, tests both known test videos.
    """
    os.makedirs(RECEIPTS_DIR, exist_ok=True)

    run_id = f"canary-{uuid.uuid4().hex[:12]}"
    timestamp = datetime.now(timezone.utc).isoformat()

    targets = [video_id] if video_id else list(TEST_VIDEOS.keys())
    results = {}

    for vid in targets:
        result = try_fetch_transcript(vid)
        if video_id is None and vid in TEST_VIDEOS:
            result["test_description"] = TEST_VIDEOS[vid]
        results[vid] = result

    # If single video, unwrap; otherwise batch
    if video_id:
        receipt = results[video_id]
    else:
        receipt = {
            "batch": True,
            "video_count": len(results),
            "results": results,
            "overall_status": (
                "reachable"
                if any(r["status"] == "reachable" for r in results.values())
                else "unreachable"
            ),
        }

    # Inject receipt metadata
    receipt["run_id"] = run_id
    receipt["timestamp"] = timestamp
    receipt["tool"] = "youtube-transcript-canary-v0"

    # Serialize canonical JSON (deterministic key order for hashing)
    canonical = json.dumps(
        receipt, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )
    sha256 = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    receipt["sha256"] = sha256

    # Write receipt
    receipt_filename = f"{run_id}.json"
    receipt_path = os.path.join(RECEIPTS_DIR, receipt_filename)
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)

    # Print path to stdout (machine-readable output contract)
    print(receipt_path)
    return receipt_path


if __name__ == "__main__":
    video_id_arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_canary(video_id_arg)
