#!/usr/bin/env python3
"""
video-ocr-adapter v0.1.0

Single-frame OCR evidence adapter. Takes a keyframe manifest entry
from video-evidence-packager v0.1.0 and produces a timestamped
visual evidence segment.

NOT a narrative engine. NOT a video understanding system.
An extraction tool that reads visible text from a single frame.

Usage:
    python3 ocr_adapter.py <frame_image> --frame-id frame:0001 \
        --timestamp 30.0 --video-asset-id "local:abc123" \
        [--frame-sha256 <hash>] [--output-dir DIR] [--engine tesseract]

Acceptance criteria:
    1. Takes single keyframe entry from packager output.
    2. Produces structured evidence segment with frame_id, timestamp, SHA-256, OBS label.
    3. No narrative summary produced.
    4. No cross-frame synthesis.
    5. Receipt includes engine/version used.
    6. Failed OCR produces structured failure receipt.
    7. No external write, no Telegram, no persistent graph write.
    8. Deterministic: same frame + same engine = same evidence text.
    9. Output appends to evidence-segments.jsonl (not overwrite).
    10. All claims labeled OBS, confidence capped at engine-reported level.
"""

import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone

VERSION = "0.1.0"
TOOL_NAME = "video-ocr-adapter"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# --- OCR Engines ---

class TesseractEngine:
    """Tesseract OCR engine — always available, zero cost."""

    name = "tesseract"
    version = "5.5.0"

    def __init__(self, lang: str = "eng"):
        self.lang = lang

    def extract(self, image_path: str) -> dict:
        """
        Extract text from image.
        Returns: {text, confidence, word_count, engine, engine_version, limitations}
        """
        try:
            import pytesseract
            from PIL import Image
        except ImportError as e:
            return {
                "status": "failed",
                "error_class": "dependency_missing",
                "error_message": str(e),
            }

        try:
            img = Image.open(image_path)
        except Exception as e:
            return {
                "status": "failed",
                "error_class": "invalid_image",
                "error_message": f"Cannot open image: {e}",
            }

        try:
            # Get text with confidence data
            data = pytesseract.image_to_data(img, lang=self.lang, output_type=pytesseract.Output.DICT)

            # Filter out empty texts and compute average confidence
            valid_entries = [
                (text, conf)
                for text, conf in zip(data["text"], data["conf"])
                if text.strip() and int(conf) > 0
            ]

            if not valid_entries:
                return {
                    "status": "success",
                    "text": "",
                    "confidence": 0.0,
                    "word_count": 0,
                    "line_count": 0,
                    "engine": self.name,
                    "engine_version": self.version,
                    "language": self.lang,
                    "limitations": [
                        "No text detected in frame",
                        "Frame may contain only graphics, be blurry, or have non-Latin script",
                    ],
                }

            texts = [t for t, _ in valid_entries]
            confidences = [float(c) for _, c in valid_entries]
            avg_confidence = sum(confidences) / len(confidences)

            # Also get full text for clean output
            full_text = pytesseract.image_to_string(img, lang=self.lang).strip()

            # Count lines
            line_count = len([line for line in full_text.split("\n") if line.strip()]) if full_text else 0

            # Normalize confidence to 0-1
            normalized_confidence = min(avg_confidence / 100.0, 1.0)

            limitations = []
            if normalized_confidence < 0.7:
                limitations.append("Low OCR confidence — text may contain errors")
            if img.width < 300 or img.height < 200:
                limitations.append("Small image dimensions may reduce OCR accuracy")

            return {
                "status": "success",
                "text": full_text,
                "confidence": round(normalized_confidence, 4),
                "word_count": len(texts),
                "line_count": line_count,
                "engine": self.name,
                "engine_version": self.version,
                "language": self.lang,
                "limitations": limitations if limitations else ["Tesseract OCR; layout analysis limited"],
            }
        except Exception as e:
            return {
                "status": "failed",
                "error_class": "ocr_execution_failed",
                "error_message": str(e),
            }


ENGINES = {
    "tesseract": TesseractEngine,
}


def create_engine(name: str, **kwargs):
    """Factory for OCR engines."""
    if name not in ENGINES:
        raise ValueError(f"Unknown engine: {name}. Available: {list(ENGINES.keys())}")
    return ENGINES[name](**kwargs)


# --- Core adapter ---

def ocr_frame(
    frame_path: str,
    frame_id: str,
    timestamp_seconds: float,
    video_asset_id: str,
    frame_sha256: str = None,
    engine_name: str = "tesseract",
    output_dir: str = None,
    task: str = "extract_visible_text_only",
    **engine_kwargs,
) -> dict:
    """
    Run OCR on a single keyframe. Returns the receipt dict.
    """
    run_id = f"ocr-adapter:{uuid.uuid4().hex[:12]}"

    if output_dir is None:
        output_dir = os.path.dirname(frame_path) or "."
    os.makedirs(output_dir, exist_ok=True)

    # Validate input
    if not os.path.exists(frame_path):
        return _failure_receipt(run_id, frame_id, timestamp_seconds,
                                "input_validation", "file_not_found",
                                f"Frame file does not exist: {frame_path}")

    # Compute frame hash if not provided
    if frame_sha256 is None:
        frame_sha256 = sha256_file(frame_path)

    # Create engine
    try:
        engine = create_engine(engine_name, **engine_kwargs)
    except ValueError as e:
        return _failure_receipt(run_id, frame_id, timestamp_seconds,
                                "engine_init", "unknown_engine", str(e))

    # Run OCR
    result = engine.extract(frame_path)

    if result.get("status") == "failed":
        return _failure_receipt(run_id, frame_id, timestamp_seconds,
                                "ocr_execution",
                                result.get("error_class", "unknown"),
                                result.get("error_message", "Unknown error"))

    # Build evidence segment
    evidence_id = f"ev:{uuid.uuid4().hex[:8]}"
    evidence_segment = {
        "id": evidence_id,
        "frame_id": frame_id,
        "video_asset_id": video_asset_id,
        "modality": "visual_ocr",
        "timestamp_seconds": timestamp_seconds,
        "frame_sha256": frame_sha256,
        "observation": result["text"],
        "confidence": result["confidence"],
        "word_count": result.get("word_count", 0),
        "line_count": result.get("line_count", 0),
        "extraction_method": f"{engine.name}_ocr",
        "extraction_version": VERSION,
        "engine": engine.name,
        "engine_version": engine.version,
        "language": result.get("language", "eng"),
        "limitations": result.get("limitations", []),
        "epistemic_label": "OBS",
        "content_class": "visual_ocr_observation",
        "status": "observed" if result["text"] else "no_text_detected",
    }

    # Compute evidence hash (content-bearing fields only, not identifiers)
    content_for_hash = {
        "frame_id": frame_id,
        "video_asset_id": video_asset_id,
        "modality": "visual_ocr",
        "timestamp_seconds": timestamp_seconds,
        "frame_sha256": frame_sha256,
        "observation": result["text"],
        "confidence": result["confidence"],
        "engine": engine.name,
        "engine_version": engine.version,
        "language": result.get("language", "eng"),
    }
    evidence_bytes = json.dumps(content_for_hash, sort_keys=True).encode("utf-8")
    evidence_hash = sha256_bytes(evidence_bytes)

    # Build receipt
    receipt = {
        "run_id": run_id,
        "capability_id": "media.youtube.visual_ocr",
        "tool_version": VERSION,
        "status": "success",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "input": {
            "frame_id": frame_id,
            "frame_path": os.path.abspath(frame_path),
            "frame_sha256": frame_sha256,
            "video_asset_id": video_asset_id,
            "timestamp_seconds": timestamp_seconds,
            "task": task,
        },
        "evidence": {
            "evidence_id": evidence_id,
            "evidence_hash": evidence_hash,
            "text_length": len(result["text"]),
            "confidence": result["confidence"],
            "word_count": result.get("word_count", 0),
            "engine": engine.name,
            "engine_version": engine.version,
            "content_class": "visual_ocr_observation",
            "epistemic_label": "OBS",
        },
        "network": {
            "allowed": True,
            "media_downloaded": False,
            "cookies_used": False,
            "external_write": False,
        },
        "error": None,
    }

    # Write evidence segment to JSONL (append mode)
    jsonl_path = os.path.join(output_dir, "evidence-segments.jsonl")
    with open(jsonl_path, "a") as f:
        f.write(json.dumps(evidence_segment, ensure_ascii=False) + "\n")

    # Write evidence detail (single-frame JSON)
    evidence_path = os.path.join(output_dir, f"ocr-evidence-{frame_id.replace(':', '_')}.json")
    with open(evidence_path, "w") as f:
        json.dump(evidence_segment, f, indent=2, ensure_ascii=False)

    # Write receipt
    receipt_path = os.path.join(output_dir, "receipt.json")
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)

    return receipt


def _failure_receipt(run_id, frame_id, timestamp_seconds, stage, error_class, message):
    """Build a structured failure receipt."""
    receipt = {
        "run_id": run_id,
        "capability_id": "media.youtube.visual_ocr",
        "tool_version": VERSION,
        "status": "failed",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "input": {
            "frame_id": frame_id,
            "timestamp_seconds": timestamp_seconds,
        },
        "evidence": None,
        "network": {
            "allowed": True,
            "media_downloaded": False,
            "cookies_used": False,
            "external_write": False,
        },
        "error": {
            "stage": stage,
            "class": error_class,
            "message": message,
        },
    }

    # Write receipt even on failure
    receipt_path = os.path.join(os.getcwd(), "receipt.json")
    try:
        with open(receipt_path, "w") as f:
            json.dump(receipt, f, indent=2)
    except Exception:
        pass

    return receipt


# --- Batch mode (from keyframes.json) ---

def batch_ocr(keyframes_json_path: str, video_asset_id: str,
              output_dir: str = None, engine_name: str = "tesseract",
              limit: int = None, **engine_kwargs) -> dict:
    """
    Run OCR on all frames from a keyframes.json manifest.
    Returns aggregate receipt.
    """
    run_id = f"ocr-batch:{uuid.uuid4().hex[:12]}"

    if output_dir is None:
        output_dir = os.path.dirname(keyframes_json_path) or "."
    os.makedirs(output_dir, exist_ok=True)

    with open(keyframes_json_path) as f:
        manifest = json.load(f)

    frames = manifest.get("frames", [])
    if limit:
        frames = frames[:limit]

    results = []
    for frame_entry in frames:
        frame_path = os.path.join(
            os.path.dirname(keyframes_json_path),
            frame_entry.get("path", "")
        )
        r = ocr_frame(
            frame_path=frame_path,
            frame_id=frame_entry["id"],
            timestamp_seconds=frame_entry["timestamp_seconds"],
            video_asset_id=video_asset_id,
            frame_sha256=frame_entry.get("sha256"),
            engine_name=engine_name,
            output_dir=output_dir,
            **engine_kwargs,
        )
        results.append(r)

    successes = [r for r in results if r.get("status") == "success"]
    failures = [r for r in results if r.get("status") != "success"]

    receipt = {
        "run_id": run_id,
        "capability_id": "media.youtube.visual_ocr_batch",
        "tool_version": VERSION,
        "status": "success" if successes else "failed",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "input": {
            "keyframes_manifest": os.path.abspath(keyframes_json_path),
            "video_asset_id": video_asset_id,
            "total_frames": len(frames),
        },
        "results": {
            "succeeded": len(successes),
            "failed": len(failures),
            "evidence_segments": [
                {
                    "frame_id": r["input"]["frame_id"],
                    "evidence_id": r["evidence"]["evidence_id"] if r.get("evidence") else None,
                    "confidence": r["evidence"]["confidence"] if r.get("evidence") else None,
                    "text_length": r["evidence"]["text_length"] if r.get("evidence") else 0,
                }
                for r in successes
            ],
        },
        "network": {
            "allowed": True,
            "media_downloaded": False,
            "cookies_used": False,
            "external_write": False,
        },
        "error": None if successes else {"message": "All frames failed OCR"},
    }

    # Write batch receipt
    receipt_path = os.path.join(output_dir, "batch-receipt.json")
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)

    return receipt


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="video-ocr-adapter v0: single-frame OCR evidence extraction"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Single frame OCR
    single = subparsers.add_parser("ocr", help="OCR a single frame")
    single.add_argument("frame", help="Path to keyframe image")
    single.add_argument("--frame-id", required=True, help="Frame ID from manifest")
    single.add_argument("--timestamp", type=float, required=True, help="Source PTS in seconds")
    single.add_argument("--video-asset-id", required=True, help="Video asset ID")
    single.add_argument("--frame-sha256", default=None, help="Pre-computed frame SHA-256")
    single.add_argument("--engine", default="tesseract", help="OCR engine (default: tesseract)")
    single.add_argument("--output-dir", default=None, help="Output directory")
    single.add_argument("--lang", default="eng", help="Tesseract language (default: eng)")

    # Batch OCR from manifest
    batch = subparsers.add_parser("batch", help="OCR all frames from keyframes.json")
    batch.add_argument("keyframes", help="Path to keyframes.json from packager")
    batch.add_argument("--video-asset-id", required=True, help="Video asset ID")
    batch.add_argument("--engine", default="tesseract", help="OCR engine")
    batch.add_argument("--output-dir", default=None, help="Output directory")
    batch.add_argument("--limit", type=int, default=None, help="Max frames to process")
    batch.add_argument("--lang", default="eng", help="Tesseract language")

    args = parser.parse_args()

    if args.command == "ocr":
        result = ocr_frame(
            frame_path=args.frame,
            frame_id=args.frame_id,
            timestamp_seconds=args.timestamp,
            video_asset_id=args.video_asset_id,
            frame_sha256=args.frame_sha256,
            engine_name=args.engine,
            output_dir=args.output_dir,
            lang=args.lang,
        )
    elif args.command == "batch":
        result = batch_ocr(
            keyframes_json_path=args.keyframes,
            video_asset_id=args.video_asset_id,
            output_dir=args.output_dir,
            engine_name=args.engine,
            limit=args.limit,
            lang=args.lang,
        )
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
