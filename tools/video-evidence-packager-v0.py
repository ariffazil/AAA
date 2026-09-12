#!/usr/bin/env python3
"""
video-evidence-packager v0 — deterministic, read-only video evidence extraction.
No external network calls. No inference. No captions/emotions/scene descriptions.
Input media is never modified.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone


def sha256_file(path: str) -> str:
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_metadata(video_path: str) -> dict:
    """Probe media metadata via ffprobe (JSON output)."""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed (rc={result.returncode}): {result.stderr.strip()}")
    return json.loads(result.stdout)


def write_failure_receipt(output_dir: str, error_msg: str) -> str:
    """Write a structured failure receipt and print path to stdout."""
    os.makedirs(output_dir, exist_ok=True)
    receipt = {
        "run_id": str(uuid.uuid4()),
        "status": "failure",
        "stage": "validation",
        "error": error_msg,
        "external_calls": 0,
        "artifacts_written": 0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    receipt_path = os.path.join(output_dir, "receipt.json")
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)
    print(receipt_path)
    return receipt_path


def main():
    parser = argparse.ArgumentParser(description="Video Evidence Packager v0")
    parser.add_argument("--video-path", required=True, help="Path to input video")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--interval-seconds", type=int, default=30, help="Frame extraction interval (default 30)")
    parser.add_argument("--max-frames", type=int, default=24, help="Max frames to extract (default 24)")
    args = parser.parse_args()

    video_path = args.video_path
    output_dir = args.output_dir
    interval = args.interval_seconds
    max_frames = args.max_frames

    # --- Validate input ---
    if not os.path.isfile(video_path):
        write_failure_receipt(output_dir, f"Input file not found: {video_path}")
        return

    # --- Create output directories ---
    keyframes_dir = os.path.join(output_dir, "keyframes")
    os.makedirs(keyframes_dir, exist_ok=True)

    # --- Probe metadata ---
    try:
        metadata = probe_metadata(video_path)
    except Exception as e:
        write_failure_receipt(output_dir, f"ffprobe failed: {e}")
        return

    # Extract video stream info for width/height/duration
    video_stream = None
    for stream in metadata.get("streams", []):
        if stream.get("codec_type") == "video":
            video_stream = stream
            break

    if video_stream is None:
        write_failure_receipt(output_dir, "No video stream found in input")
        return

    width = video_stream.get("width", 0)
    height = video_stream.get("height", 0)

    duration_str = metadata.get("format", {}).get("duration", "0")
    try:
        duration_seconds = float(duration_str)
    except (ValueError, TypeError):
        duration_seconds = 0.0

    # --- Compute SHA-256 of source video ---
    source_hash = sha256_file(video_path)

    # --- Compute frame schedule (deterministic) ---
    timestamps = []
    t = 0.0
    while t < duration_seconds and len(timestamps) < max_frames:
        timestamps.append(t)
        t += interval

    # If duration is 0 or very short, at least try t=0
    if not timestamps:
        timestamps = [0.0]

    # --- Extract keyframes ---
    frame_manifest = []  # for keyframes.json
    segments = []        # for evidence-segments.jsonl
    artifacts_written = 0

    for idx, ts in enumerate(timestamps):
        filename = f"{idx:08d}.jpg"
        out_path = os.path.join(keyframes_dir, filename)

        cmd = [
            "ffmpeg",
            "-y",
            "-ss", f"{ts:.3f}",
            "-i", video_path,
            "-frames:v", "1",
            "-q:v", "2",
            out_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            continue

        if not os.path.isfile(out_path):
            continue

        frame_hash = sha256_file(out_path)
        artifacts_written += 1

        # Timestamp in HMS
        total_secs = int(ts)
        hours = total_secs // 3600
        minutes = (total_secs % 3600) // 60
        secs = total_secs % 60
        hms = f"{hours:02d}:{minutes:02d}:{secs:02d}"

        # Read actual frame dimensions from the extracted image via ffprobe
        frame_width = width
        frame_height = height
        try:
            frame_meta = probe_metadata(out_path)
            for s in frame_meta.get("streams", []):
                if s.get("codec_type") == "image":
                    frame_width = s.get("width", width)
                    frame_height = s.get("height", height)
                    break
        except Exception:
            pass

        frame_entry = {
            "index": idx,
            "filename": filename,
            "timestamp_seconds": ts,
            "timestamp_hms": hms,
            "sha256": frame_hash,
            "width": frame_width,
            "height": frame_height,
        }
        frame_manifest.append(frame_entry)

        segment = {
            "id": f"frame-{idx:08d}",
            "timestamp_seconds": ts,
            "timestamp_hms": hms,
            "path": os.path.join("keyframes", filename),
            "sha256": frame_hash,
            "width": frame_width,
            "height": frame_height,
            "modality": "visual_frame",
            "status": "observed",
        }
        segments.append(segment)

    # --- Write video_asset.yaml ---
    asset_yaml = f"""source:
  path: {video_path}
  sha256: {source_hash}
  duration_seconds: {duration_seconds}
  width: {width}
  height: {height}
sampling:
  interval_seconds: {interval}
  max_frames: {max_frames}
  computed_frame_count: {len(timestamps)}
  actual_extracted: {artifacts_written}
artifacts:
  keyframes_dir: keyframes
  keyframes_manifest: keyframes.json
  evidence_segments: evidence-segments.jsonl
  receipt: receipt.json
"""
    with open(os.path.join(output_dir, "video_asset.yaml"), "w") as f:
        f.write(asset_yaml)
    artifacts_written += 1

    # --- Write keyframes.json ---
    with open(os.path.join(output_dir, "keyframes.json"), "w") as f:
        json.dump(frame_manifest, f, indent=2)
    artifacts_written += 1

    # --- Write evidence-segments.jsonl ---
    with open(os.path.join(output_dir, "evidence-segments.jsonl"), "w") as f:
        for seg in segments:
            f.write(json.dumps(seg) + "\n")
    artifacts_written += 1

    # --- Write receipt.json ---
    run_id = str(uuid.uuid4())
    receipt = {
        "run_id": run_id,
        "status": "success",
        "stage": "complete",
        "source_hash": source_hash,
        "external_calls": 0,
        "artifacts_written": artifacts_written,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(os.path.join(output_dir, "receipt.json"), "w") as f:
        json.dump(receipt, f, indent=2)
    artifacts_written += 1

    print(os.path.join(output_dir, "receipt.json"))


if __name__ == "__main__":
    main()
