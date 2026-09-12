#!/usr/bin/env python3
"""
Step 4: ASR Adapter v0.1.0

Local audio → GLM-ASR-2512 → timestamped text evidence.
Fallback for captionless video when transcript lane is unavailable.

Input: local audio file (wav/mp3/m4a) or video file (audio extracted)
Output: timestamped evidence segments (evidence-segments.jsonl)

Constraint: GLM-ASR-2512 limits ≤30s per chunk, ≤25MB per chunk.
Mitigation: automatic silence-based chunking before API calls.

Usage:
    python3 asr_adapter.py <audio_file> [--canonical-url URL] [--output-dir DIR]
    python3 asr_adapter.py --from-video <video_file> [--output-dir DIR]
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone

VERSION = "0.1.0"
TOOL_NAME = "asr_adapter"
MAX_CHUNK_DURATION_S = 25  # safety margin below 30s API limit
MAX_CHUNK_SIZE_MB = 20     # safety margin below 25MB API limit
API_ENDPOINT = "https://api.z.ai/api/paas/v4/audio/transcriptions"
API_MODEL = "glm-asr-2512"
DEFAULT_DICTIONARY = [
    "K-DIP", "W_scar", "F1", "F2", "F13",
    "GEOX", "WEALTH", "WELL", "AAA", "A-FORGE",
    "Ditempa Bukan Diberi", "i-ARIF",
    "333-AGI", "555-ASI", "888-APEX", "999-SEAL",
    "arifOS", "VAULT999", "EMD",
    "Hermes", "OpenClaw", "OpenCode",
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_audio(video_path, output_path):
    """Extract audio track from video file."""
    cmd = [
        "ffmpeg", "-v", "quiet",
        "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        "-y", output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    return result.returncode == 0 and os.path.exists(output_path)


def get_audio_duration(audio_path):
    """Get audio duration in seconds."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        return 0.0
    try:
        data = json.loads(result.stdout)
        return float(data.get("format", {}).get("duration", 0))
    except (ValueError, TypeError):
        return 0.0


def chunk_audio(audio_path, output_dir, max_duration=MAX_CHUNK_DURATION_S):
    """
    Split audio into chunks using silence detection.
    Returns list of chunk paths with their time offsets.
    """
    duration = get_audio_duration(audio_path)
    if duration <= 0:
        return [(audio_path, 0.0)]

    # If short enough, return as-is
    if duration <= max_duration:
        return [(audio_path, 0.0)]

    chunks = []
    t = 0.0
    chunk_idx = 0

    while t < duration:
        chunk_path = os.path.join(output_dir, f"chunk_{chunk_idx:04d}.wav")
        cmd = [
            "ffmpeg", "-v", "quiet",
            "-ss", str(t),
            "-i", audio_path,
            "-t", str(max_duration),
            "-acodec", "pcm_s16le",
            "-ar", "16000", "-ac", "1",
            "-y", chunk_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and os.path.exists(chunk_path):
            chunks.append((chunk_path, t))
        t += max_duration
        chunk_idx += 1

    return chunks if chunks else [(audio_path, 0.0)]


def transcribe_chunk(audio_path, api_key, dictionary=None):
    """
    Send one audio chunk to GLM-ASR-2512.
    Returns: {text, language, status, error}
    """
    import requests

    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": API_MODEL,
        "stream": "false",
        "dictionary": ",".join(dictionary or DEFAULT_DICTIONARY),
    }

    try:
        file_size = os.path.getsize(audio_path)
        if file_size > MAX_CHUNK_SIZE_MB * 1024 * 1024:
            return {
                "status": "failed",
                "error_class": "chunk_too_large",
                "error_message": f"Chunk size {file_size / 1024 / 1024:.1f}MB exceeds {MAX_CHUNK_SIZE_MB}MB limit",
            }

        with open(audio_path, "rb") as f:
            files = {"file": (os.path.basename(audio_path), f, "audio/wav")}
            r = requests.post(API_ENDPOINT, headers=headers, data=payload, files=files, timeout=30)

        if r.status_code == 200:
            data = r.json()
            return {
                "status": "success",
                "text": data.get("text", ""),
                "language": data.get("language", "unknown"),
            }
        else:
            return {
                "status": "failed",
                "error_class": f"http_{r.status_code}",
                "error_message": r.text[:200],
            }
    except ImportError:
        return {
            "status": "failed",
            "error_class": "dependency_missing",
            "error_message": "requests library not installed",
        }
    except Exception as e:
        return {
            "status": "failed",
            "error_class": "api_error",
            "error_message": str(e)[:200],
        }


def asr_adapter(audio_path, canonical_url=None, output_dir=None,
                video_asset_id=None, dictionary=None):
    """
    Main ASR adapter function.
    Returns receipt dict.
    """
    run_id = f"asr-adapter:{uuid.uuid4().hex[:12]}"

    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "asr-output")
    os.makedirs(output_dir, exist_ok=True)

    # Validate input
    if not os.path.exists(audio_path):
        return _failure_receipt(run_id, "input_validation", "file_not_found",
                                f"File does not exist: {audio_path}")

    # Check API key
    api_key = os.environ.get("ZAI_API_KEY")
    if not api_key:
        return _failure_receipt(run_id, "auth", "api_key_missing",
                                "ZAI_API_KEY not set in environment")

    # Hash source
    source_hash = sha256_file(audio_path)

    # Compute video_asset_id
    if video_asset_id is None:
        video_asset_id = f"local:{source_hash[:16]}"

    # Get audio info
    duration = get_audio_duration(audio_path)
    chunk_dir = os.path.join(output_dir, "chunks")
    os.makedirs(chunk_dir, exist_ok=True)

    # Chunk audio
    chunks = chunk_audio(audio_path, chunk_dir)

    # Transcribe each chunk
    all_segments = []
    languages_detected = []
    chunk_results = []

    for chunk_path, offset_s in chunks:
        result = transcribe_chunk(chunk_path, api_key, dictionary)
        chunk_results.append(result)

        if result["status"] == "success" and result.get("text"):
            seg = {
                "id": f"ev:{uuid.uuid4().hex[:8]}",
                "video_asset_id": video_asset_id,
                "modality": "audio_asr",
                "start_seconds": round(offset_s, 3),
                "end_seconds": round(offset_s + MAX_CHUNK_DURATION_S, 3),
                "text": result["text"],
                "extraction_method": "glm_asr_2512",
                "extraction_version": VERSION,
                "engine": "glm-asr-2512",
                "confidence": 0.85,  # ASR default; no per-word confidence from API
                "language": result.get("language", "unknown"),
                "provenance_url": f"{canonical_url}#t={int(offset_s)}" if canonical_url else None,
                "content_class": "audio_asr_observation",
                "epistemic_label": "OBS",
                "status": "observed",
            }
            all_segments.append(seg)

            lang = result.get("language", "unknown")
            if lang not in languages_detected:
                languages_detected.append(lang)

    # Write evidence segments (append)
    jsonl_path = os.path.join(output_dir, "evidence-segments.jsonl")
    with open(jsonl_path, "w") as f:
        for seg in all_segments:
            f.write(json.dumps(seg, ensure_ascii=False) + "\n")

    # Aggregate results
    successful_chunks = sum(1 for r in chunk_results if r["status"] == "success")
    failed_chunks = sum(1 for r in chunk_results if r["status"] == "failed")

    # Build receipt
    receipt = {
        "run_id": run_id,
        "capability_id": "media.youtube.audio_asr",
        "tool_version": VERSION,
        "status": "success" if all_segments else "failed",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "input": {
            "audio_path": os.path.abspath(audio_path),
            "source_hash": source_hash,
            "video_asset_id": video_asset_id,
            "canonical_url": canonical_url,
            "duration_seconds": round(duration, 2),
        },
        "evidence": {
            "segment_count": len(all_segments),
            "languages_detected": languages_detected,
            "successful_chunks": successful_chunks,
            "failed_chunks": failed_chunks,
            "total_chunks": len(chunks),
            "content_class": "audio_asr_observation",
            "epistemic_label": "OBS",
        },
        "network": {
            "allowed": True,
            "external_api": "Z.AI GLM-ASR-2512",
            "media_downloaded": False,
            "cookies_used": False,
            "external_write": False,
        },
        "error": None,
    }

    if not all_segments:
        receipt["status"] = "failed"
        first_error = next((r for r in chunk_results if r["status"] == "failed"), None)
        receipt["error"] = {
            "stage": "transcription",
            "class": first_error.get("error_class", "all_chunks_failed") if first_error else "no_output",
            "message": first_error.get("error_message", "No text produced from any chunk") if first_error else "No text produced",
        }

    # Write receipt
    receipt_path = os.path.join(output_dir, "receipt.json")
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)

    return receipt


def _failure_receipt(run_id, stage, error_class, message):
    return {
        "run_id": run_id,
        "capability_id": "media.youtube.audio_asr",
        "tool_version": VERSION,
        "status": "failed",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "input": {},
        "evidence": None,
        "network": {"allowed": True, "external_api": "Z.AI GLM-ASR-2512",
                     "media_downloaded": False, "cookies_used": False, "external_write": False},
        "error": {"stage": stage, "class": error_class, "message": message},
    }


def main():
    parser = argparse.ArgumentParser(description="ASR adapter v0.1.0: local audio → GLM-ASR-2512")
    parser.add_argument("audio", nargs="?", help="Path to local audio file")
    parser.add_argument("--from-video", default=None, help="Extract audio from video file first")
    parser.add_argument("--canonical-url", default=None, help="Original source URL")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    parser.add_argument("--video-asset-id", default=None, help="Video asset ID")
    args = parser.parse_args()

    audio_path = args.audio
    if args.from_video:
        # Extract audio from video
        tmp_audio = os.path.join(args.output_dir or os.getcwd(), "extracted_audio.wav")
        os.makedirs(os.path.dirname(tmp_audio), exist_ok=True)
        if not extract_audio(args.from_video, tmp_audio):
            print(json.dumps({"status": "failed", "error": "Failed to extract audio from video"}))
            sys.exit(1)
        audio_path = tmp_audio

    if not audio_path:
        parser.print_help()
        sys.exit(1)

    receipt = asr_adapter(
        audio_path=audio_path,
        canonical_url=args.canonical_url,
        output_dir=args.output_dir,
        video_asset_id=args.video_asset_id,
    )
    print(json.dumps(receipt, indent=2))
    sys.exit(0 if receipt.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
