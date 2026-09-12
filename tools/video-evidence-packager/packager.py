#!/usr/bin/env python3
"""
video-evidence-packager v0

Local, deterministic, read-only video evidence extraction.
Emits hashed keyframes + manifest + receipt. No network calls.
No vision model. No OCR. No LLM. No Telegram.

Usage:
    python3 packager.py <video_file> [--canonical-url URL] [--interval SECONDS] [--max-frames N] [--output-dir DIR]

Acceptance criteria:
    1. Same input -> same timestamp schedule (deterministic).
    2. Every output artifact has SHA-256.
    3. Every frame has exact timestamp.
    4. Frame count never exceeds cap.
    5. Invalid input -> structured failure receipt, not traceback.
    6. No inferred captions, objects, emotions, or scene descriptions.
    7. Manifest validates against schema.
    8. No external network call.
    9. No input media modified.
   10. Test fixtures cover short, long, silent, corrupt cases.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


VERSION = "0.1.0"
TOOL_NAME = "video-evidence-packager"
MAX_FRAMES_DEFAULT = 24
INTERVAL_DEFAULT = 30


def sha256_file(path: str) -> str:
    """Compute SHA-256 of a file, reading in chunks for memory safety."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def format_timestamp(seconds: float) -> str:
    """Format seconds to HH:MM:SS.mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def probe_media(video_path: str) -> dict:
    """Run ffprobe to extract media metadata. Returns dict or raises."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def extract_frame(video_path: str, timestamp: float, output_path: str) -> bool:
    """Extract a single frame at given timestamp. Returns True on success."""
    cmd = [
        "ffmpeg", "-v", "quiet",
        "-ss", f"{timestamp:.3f}",
        "-i", video_path,
        "-frames:v", "1",
        "-q:v", "2",
        "-y",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.returncode == 0 and os.path.exists(output_path)


def write_failure_receipt(output_dir: str, run_id: str, stage: str,
                          error_class: str, safe_message: str,
                          source_hash: str = None) -> dict:
    """Write a structured failure receipt."""
    receipt = {
        "run_id": run_id,
        "status": "failed",
        "stage": stage,
        "error_class": error_class,
        "safe_message": safe_message,
        "source_hash": source_hash,
        "external_calls": 0,
        "artifacts_written": 0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool_version": VERSION,
    }
    receipt_path = os.path.join(output_dir, "receipt.json")
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)
    return receipt


def write_success_receipt(output_dir: str, run_id: str, video_asset: dict,
                           sampling: dict, artifacts: list) -> dict:
    """Write a structured success receipt."""
    receipt = {
        "run_id": run_id,
        "status": "success",
        "stage": "complete",
        "tool_version": VERSION,
        "external_calls": 0,
        "artifacts_written": len(artifacts) + 2,  # keyframes.json + evidence-segments.jsonl
        "video_asset_id": video_asset.get("id", "unknown"),
        "frame_count": sampling.get("actual_frames", 0),
        "duration_seconds": video_asset.get("duration_seconds", 0),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    receipt_path = os.path.join(output_dir, "receipt.json")
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)
    return receipt


def write_yaml_compact(data: dict, indent: int = 0) -> str:
    """Minimal YAML writer for flat/nested dicts. No external deps."""
    lines = []
    prefix = "  " * indent
    for k, v in data.items():
        if v is None:
            lines.append(f"{prefix}{k}: null")
        elif isinstance(v, bool):
            lines.append(f"{prefix}{k}: {'true' if v else 'false'}")
        elif isinstance(v, (int, float)):
            lines.append(f"{prefix}{k}: {v}")
        elif isinstance(v, str):
            # quote if contains special chars
            if any(c in v for c in ":#{}[]|>&*!%@`"):
                lines.append(f'{prefix}{k}: "{v}"')
            else:
                lines.append(f"{prefix}{k}: {v}")
        elif isinstance(v, list):
            if not v:
                lines.append(f"{prefix}{k}: []")
            else:
                lines.append(f"{prefix}{k}:")
                for item in v:
                    if isinstance(item, dict):
                        # nested object in list
                        first = True
                        for sk, sv in item.items():
                            sub_prefix = f"{prefix}  - " if first else f"{prefix}    "
                            first = False
                            if isinstance(sv, dict):
                                lines.append(f"{sub_prefix}{sk}:")
                                for ssk, ssv in sv.items():
                                    val_str = write_yaml_compact({ssk: ssv}, indent=0).strip()
                                    lines.append(f"{prefix}      {val_str}")
                            else:
                                val_str = write_yaml_compact({sk: sv}, indent=0).strip()
                                lines.append(f"{sub_prefix}{val_str}")
                    else:
                        val_str = write_yaml_compact({"_": item}, indent=0).strip()
                        # strip the "_: " prefix
                        val_str = val_str.replace("_: ", "", 1)
                        lines.append(f"{prefix}  - {val_str}")
        elif isinstance(v, dict):
            lines.append(f"{prefix}{k}:")
            lines.append(write_yaml_compact(v, indent + 1))
    return "\n".join(lines)


def packager(video_path: str, canonical_url: str = None,
             interval: float = INTERVAL_DEFAULT, max_frames: int = MAX_FRAMES_DEFAULT,
             output_dir: str = None) -> dict:
    """
    Main packager function.
    Returns the receipt dict.
    """
    run_id = f"video-packager:{uuid.uuid4().hex[:12]}"

    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(video_path), "evidence_output")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "keyframes"), exist_ok=True)

    # Validate input
    if not os.path.exists(video_path):
        return write_failure_receipt(
            output_dir, run_id, "input_validation",
            "file_not_found",
            f"Input file does not exist: {video_path}"
        )

    # Hash the source
    source_hash = sha256_file(video_path)

    # Probe media
    try:
        probe = probe_media(video_path)
    except Exception as e:
        return write_failure_receipt(
            output_dir, run_id, "media_probe",
            "unsupported_or_corrupt_media",
            "Input could not be decoded as a supported video asset.",
            source_hash=source_hash
        )

    # Extract video stream info
    video_stream = None
    audio_stream = None
    for stream in probe.get("streams", []):
        if stream.get("codec_type") == "video" and video_stream is None:
            video_stream = stream
        elif stream.get("codec_type") == "audio" and audio_stream is None:
            audio_stream = stream

    if video_stream is None:
        return write_failure_receipt(
            output_dir, run_id, "media_probe",
            "no_video_stream",
            "Input contains no decodable video stream.",
            source_hash=source_hash
        )

    # Get duration
    fmt = probe.get("format", {})
    duration_str = fmt.get("duration", "0")
    try:
        duration_seconds = float(duration_str)
    except (ValueError, TypeError):
        duration_seconds = 0.0

    # Build video asset
    asset_id = f"local:{source_hash[:16]}"
    video_asset = {
        "id": asset_id,
        "source_kind": "local_file",
        "source_ref": os.path.abspath(video_path),
        "canonical_url": canonical_url,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "sha256": source_hash,
        "duration_seconds": round(duration_seconds, 3),
        "container": {
            "format": fmt.get("format_name", "unknown"),
            "video_codec": video_stream.get("codec_name", "unknown"),
            "audio_codec": audio_stream.get("codec_name", "none") if audio_stream else "none",
        },
    }

    # Compute frame timestamps (deterministic: uniform interval, capped)
    if duration_seconds <= 0:
        return write_failure_receipt(
            output_dir, run_id, "sampling",
            "zero_duration",
            "Video duration is zero or unparseable; cannot compute frame schedule.",
            source_hash=source_hash
        )

    timestamps = []
    t = 0.0
    while t < duration_seconds and len(timestamps) < max_frames:
        timestamps.append(round(t, 3))
        t += interval

    # Add final frame if close to end and not already present
    if duration_seconds > 0 and (not timestamps or abs(timestamps[-1] - duration_seconds) > 1.0):
        if len(timestamps) < max_frames:
            timestamps.append(round(max(0, duration_seconds - 0.1), 3))

    actual_frames = len(timestamps)

    sampling = {
        "method": "uniform_interval_v0",
        "interval_seconds": interval,
        "max_frames": max_frames,
        "actual_frames": actual_frames,
        "extraction_tool_version": f"ffmpeg-{subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True).stdout.split('\\n')[0].split(' ')[2] if True else 'unknown'}",
        "deterministic_seed": None,
    }

    # Extract frames
    keyframes = []
    evidence_segments = []
    errors = []

    for i, ts in enumerate(timestamps):
        frame_name = f"{int(ts):09d}.jpg"  # e.g., 000000000.jpg, 000000030.jpg
        frame_path = os.path.join(output_dir, "keyframes", frame_name)
        rel_path = f"keyframes/{frame_name}"

        success = extract_frame(video_path, ts, frame_path)

        if success:
            frame_hash = sha256_file(frame_path)
            # Get frame dimensions
            try:
                probe_frame = probe_media(frame_path)
                width = probe_frame["streams"][0].get("width", 0)
                height = probe_frame["streams"][0].get("height", 0)
            except Exception:
                width, height = 0, 0

            frame_entry = {
                "id": f"frame:{i+1:04d}",
                "timestamp_seconds": ts,
                "timestamp_hms": format_timestamp(ts),
                "path": rel_path,
                "sha256": frame_hash,
                "width": width,
                "height": height,
                "modality": "visual_frame",
                "status": "observed",
            }
            keyframes.append(frame_entry)

            # Evidence segment
            seg = {
                "id": f"ev:{uuid.uuid4().hex[:8]}",
                "video_id": asset_id,
                "modality": "visual_frame",
                "start_seconds": ts,
                "end_seconds": round(ts + 0.1, 3),  # single frame = ~100ms window
                "text": None,
                "extraction_method": "ffmpeg_frame_extract",
                "extraction_version": VERSION,
                "confidence": 1.0,  # deterministic extraction = perfect confidence
                "provenance_url": f"{canonical_url}#t={int(ts)}" if canonical_url else None,
                "status": "observed",
            }
            evidence_segments.append(seg)
        else:
            errors.append({"index": i, "timestamp": ts, "error": "frame_extraction_failed"})

    # Write keyframes.json
    keyframes_data = {
        "video_asset_id": asset_id,
        "total_frames": len(keyframes),
        "errors": errors,
        "frames": keyframes,
    }
    keyframes_path = os.path.join(output_dir, "keyframes.json")
    with open(keyframes_path, "w") as f:
        json.dump(keyframes_data, f, indent=2)

    # Write evidence-segments.jsonl
    seg_path = os.path.join(output_dir, "evidence-segments.jsonl")
    with open(seg_path, "w") as f:
        for seg in evidence_segments:
            f.write(json.dumps(seg) + "\n")

    # Write video_asset.yaml (compact)
    yaml_content = write_yaml_compact({"video_asset": video_asset, "sampling": sampling})
    yaml_path = os.path.join(output_dir, "video_asset.yaml")
    with open(yaml_path, "w") as f:
        f.write(yaml_content + "\n")

    # Write success receipt
    receipt = write_success_receipt(output_dir, run_id, video_asset, sampling, keyframes)

    return receipt


def main():
    parser = argparse.ArgumentParser(
        description="video-evidence-packager v0: local deterministic evidence extraction"
    )
    parser.add_argument("video", help="Path to local video file")
    parser.add_argument("--canonical-url", default=None, help="Original source URL")
    parser.add_argument("--interval", type=float, default=INTERVAL_DEFAULT,
                        help="Seconds between frames (default: 30)")
    parser.add_argument("--max-frames", type=int, default=MAX_FRAMES_DEFAULT,
                        help="Maximum frames to extract (default: 24)")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: <video_dir>/evidence_output)")
    args = parser.parse_args()

    receipt = packager(
        video_path=args.video,
        canonical_url=args.canonical_url,
        interval=args.interval,
        max_frames=args.max_frames,
        output_dir=args.output_dir,
    )

    print(json.dumps(receipt, indent=2))

    if receipt.get("status") == "failed":
        sys.exit(1)


if __name__ == "__main__":
    main()
