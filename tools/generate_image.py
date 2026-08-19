#!/usr/bin/env python3
"""
I-ARIF Image Generation — Direct Modal/Mage-Flow Wrapper

Calls Modal endpoint directly (bypasses broken MCP server).
Mage-Flow-Turbo (4B params, 4-step) on Modal serverless GPU.

Usage:
    python3 generate_image.py "red car in parking lot" --out /tmp/img.jpg

VERIFIED STATUS (2026-08-19):
  Modal endpoint returns 200 OK with valid image_b64.
  BUT: response contains a STATIC PLACEHOLDER image (~5KB PNG, identical
  SHA256 across different prompts and step counts). Real GPU inference
  appears broken or stuck in a degraded state.

  until_next_deploy: Image output is not trustworthy. DO NOT deliver
  to user as a real generation.

  Detection: SHA256 of output image matches the known-broken placeholder.
  If broken, this script exits 2 with a clear message.
"""

import os
import sys
import json
import base64
import hashlib
import argparse
import requests
from pathlib import Path
from datetime import datetime

MODAL_ENDPOINT = "https://arifbfazil--mage-flow-inference-api-generate.modal.run"

# SHA256 hashes of known broken-placeholder responses (any match = endpoint down)
KNOWN_BROKEN_HASHES = {
    # Static placeholder returned regardless of prompt
    "d9bd147ced77bca4": "modal_placeholder_image",
    # Same image with header metadata variation
    "e8a82f04adc92f1e": "modal_degraded_response",
}

MIN_VALID_IMAGE_BYTES = 15_000  # Real photo generations are 20KB+; placeholders are ~5KB


def is_placeholder_response(image_bytes: bytes) -> tuple[bool, str]:
    """Check if response is the known broken Modal placeholder."""
    sha = hashlib.sha256(image_bytes).hexdigest()
    short = sha[:16]

    if short in KNOWN_BROKEN_HASHES:
        return True, f"matches known broken hash ({KNOWN_BROKEN_HASHES[short]})"

    if len(image_bytes) < MIN_VALID_IMAGE_BYTES:
        return True, f"image too small ({len(image_bytes)} B < {MIN_VALID_IMAGE_BYTES} B threshold)"

    return False, ""


def generate_image(prompt: str, output_path: str, width: int = 1024, height: int = 1024, steps: int = 4) -> str:
    """Generate image via Modal/Mage-Flow endpoint. Exits 2 if response is the known broken placeholder."""

    print(f"[ImageGen] Provider: Mage-Flow-Turbo (Modal GPU)")
    print(f"[ImageGen] Prompt: {prompt[:120]}...")
    print(f"[ImageGen] Size: {width}x{height}, Steps: {steps}")

    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps,
    }

    try:
        resp = requests.post(MODAL_ENDPOINT, json=payload, timeout=300)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ImageGen] Modal endpoint error: {e}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()

    if "image_b64" not in data:
        print(f"[ImageGen] No image_b64 in response: {json.dumps(data)[:200]}", file=sys.stderr)
        sys.exit(1)

    img_bytes = base64.b64decode(data["image_b64"])

    # HONEST failure mode: detect placeholder and refuse to deliver garbage
    is_placeholder, reason = is_placeholder_response(img_bytes)
    if is_placeholder:
        print(f"[ImageGen] REJECTED: {reason}", file=sys.stderr)
        print(f"[ImageGen] Modal GPU appears degraded. Do not deliver this image.", file=sys.stderr)
        print(f"[ImageGen] Suggested action: modal app rollover <app-id> or redeploy mage-flow", file=sys.stderr)
        sys.exit(2)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_bytes)

    size_kb = os.path.getsize(output_path) / 1024
    model = data.get("model", "unknown")
    seed = data.get("seed", "?")
    inference_ms = data.get("inference_ms", "?")

    print(f"[ImageGen] Saved: {output_path} ({size_kb:.0f} KB)")
    print(f"[ImageGen] Model: {model}, Seed: {seed}, Time: {inference_ms}ms")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="I-ARIF Image Generation (Modal/Mage-Flow)")
    parser.add_argument("prompt", type=str, help="Image description")
    parser.add_argument("--out", type=str,
                        default=f"/tmp/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        help="Output file path")
    parser.add_argument("--width", type=int, default=1024, help="Width (512-2048)")
    parser.add_argument("--height", type=int, default=1024, help="Height (512-2048)")
    parser.add_argument("--steps", type=int, default=4, help="Steps (4=turbo, 20=RL)")
    args = parser.parse_args()

    result = generate_image(args.prompt, args.out, args.width, args.height, args.steps)
    print(f"OUTPUT_PATH={result}")


if __name__ == "__main__":
    main()
