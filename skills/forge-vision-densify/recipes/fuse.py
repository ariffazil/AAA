#!/usr/bin/env python3
"""
Day-0 governance CLI for forge-vision-densify.

This is the single entry point that any federation T2I dispatch MUST go through.
Wraps the dispatch layer with a CLI that takes a prompt, hits a stub diffusion
target, and returns the governance-verified payload.

Usage:
    python3 fuse.py --prompt "a man standing in a park" --engine MiniMax
    python3 fuse.py --prompt "45 degree fault" --engine MiniMax          # will require anchor
    python3 fuse.py --prompt "..." --engine MiniMax --anchor /tmp/ref.png
    DENSIFY_FORCE=1 python3 fuse.py --prompt "..."       # bypass ENFORCE (tests only)

Output: JSON contract + delivery_mode + disclosure caption on stdout.

Day-0 posture (this script enforces):
    ENFORCE_PIPELINE=true   (every T2I dispatch goes through)
    HARD_REJECT=false       (density<0.20 → disclose, do not block)
    DISCLOSE=true           (density<0.50 → honest caption)
    AUDIT=true              (CSV log every dispatch)

Day-7 calibration gate: only after 7-day audit log review shows stable
false-positive rate can HARD_REJECT flip to true.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Make sibling modules importable
sys.path.insert(0, str(Path(__file__).parent))
from dispatch import (
    POSTURE,
    dispatch_image,
    to_json_contract,
    render_caption,
    DispatchReceipt,
)


def stub_diffusion_call(prompt: str, anchor_path):
    """Stub diffusion. In production, replace with real engine call.

    Returns the shape dispatch.py expects: {url, image_path}.
    """
    return {
        "url": f"https://forge.example/local/{abs(hash(prompt)) % 100000:05d}.png",
        "image_path": None,  # stub — no local file for VLM to audit
    }


def main():
    p = argparse.ArgumentParser(
        description="forge-vision-densify Day-0 governance CLI"
    )
    p.add_argument("--prompt", required=True, help="T2I prompt")
    p.add_argument(
        "--engine",
        default="MiniMax",
        help="Diffusion engine label (audit metadata only)",
    )
    p.add_argument(
        "--anchor",
        default=None,
        help="Optional reference image path (ControlNet/Ip-Adapter)",
    )
    p.add_argument(
        "--shadow",
        action="store_true",
        default=True,
        help="Shadow mode (VLM tri-witness does not gate payload)",
    )
    p.add_argument(
        "--no-shadow",
        action="store_false",
        dest="shadow",
        help="Promote VLM tri-witness to gate payload (post-Day-7 only)",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Force dispatch even if pipeline posture is off (tests only)",
    )
    args = p.parse_args()

    # Bypass ENFORCE check if DENSIFY_FORCE=1
    if args.force or os.environ.get("DENSIFY_FORCE"):
        force = True
    else:
        force = False

    # Run dispatch — this is the single entry point, no naked tool calls.
    try:
        receipt = dispatch_image(
            prompt=args.prompt,
            call_diffusion=stub_diffusion_call,
            engine=args.engine,
            reference_image_path=args.anchor,
            shadow_mode=args.shadow,
            force=force,
        )
    except RuntimeError as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)

    # Build output: JSON contract + delivery metadata + caption
    output = {
        "posture": POSTURE,
        "engine": args.engine,
        "prompt_density": receipt.prompt_density,
        "delivery_mode": receipt.delivery_mode,
        "latency_ms": receipt.latency_ms,
        "json_contract": to_json_contract(receipt),
        "disclosure_caption": render_caption(receipt),
        "image_url": receipt.url,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
