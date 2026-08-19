#!/usr/bin/env python3
"""
I-ARIF Image Generation — Multi-Provider Router (Pollinations-first)

Pollinations.ai is free, no-auth, SANA/FLUX quality. Primary.
Other providers are paid fallbacks. Mage/Modal is LAST resort (placeholder-prone).

VERIFIED 2026-08-19:
  - Pollinations: WORKS, free, no auth, 6-36s per image
  - Mage/Modal: BROKEN (static placeholder), still last
  - Gemini/Qwen/MiniMax/Zai: each gated by credits/key issues

Usage:
    python3 iarif_lite_image_router.py --prompt "..." --out /tmp/img.jpg
    python3 iarif_lite_image_router.py --provider pollinations --prompt "..." --out /tmp/img.jpg
"""

import os
import sys
import json
import time
import argparse
import subprocess
import requests
from pathlib import Path
from datetime import datetime


def load_env():
    env_file = Path("/root/.secrets/kunci-root.env")
    if env_file.exists() and not os.getenv("GEMINI_API_KEY"):
        result = subprocess.run(
            ["bash", "-c", f"source {env_file} && env"],
            capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if "=" in line:
                key, _, value = line.partition("=")
                os.environ[key.strip()] = value.strip()


# ─── Provider implementations ────────────────────────────────────────────────

def route_pollinations(prompt: str, output_path: str, width: int = 1024, height: int = 1024) -> str:
    """Pollinations.ai — free, no auth, SANA/FLUX quality."""
    import urllib.parse
    encoded = urllib.parse.quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width=768&height=768&nologo=true&seed=42"
    )

    print(f"[I-ARIF LITE] Pollinations: GET {url[:80]}...")
    resp = requests.get(url, timeout=120, stream=True)
    resp.raise_for_status()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    size_kb = os.path.getsize(output_path) / 1024
    if size_kb < 5:
        raise ValueError(f"image too small ({size_kb:.0f} KB) — likely placeholder")
    return output_path


def route_modal_mageflow(prompt: str, output_path: str, width: int = 1024, height: int = 1024, steps: int = 4) -> str:
    """Modal/Mage-Flow — known to serve placeholders, hence the rejection check."""
    import base64
    url = "https://arifbfazil--mage-flow-inference-api-generate.modal.run"
    payload = {"prompt": prompt, "width": width, "height": height, "steps": steps}

    resp = requests.post(url, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()

    if "image_b64" not in data:
        raise ValueError("no image_b64 in response")
    img_bytes = base64.b64decode(data["image_b64"])

    if len(img_bytes) < 15_000:
        raise ValueError(f"image too small ({len(img_bytes)} B) — Modal placeholder suspected")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_bytes)
    return output_path


def route_gemini(prompt: str, output_path: str, aspect: str = "1:1") -> str:
    """Google Imagen 3 via google-genai SDK."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    response = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            output_mime_type="image/jpeg",
            aspect_ratio=aspect,
            person_generation="ALLOW_ADULT",
        ),
    )
    if not response.generated_images:
        raise ValueError("no images returned")
    img = response.generated_images[0]
    image_bytes = img.image.image_bytes if img.image and img.image.image_bytes else None
    if not image_bytes or len(image_bytes) < 15_000:
        raise ValueError("Gemini returned too-small image")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    return output_path


def route_qwen(prompt: str, output_path: str, width: int = 1024, height: int = 1024) -> str:
    """Qwen/DashScope Wanx (async-poll)."""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY not set")

    submit_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }
    payload = {
        "model": "wanx-v1",
        "input": {"prompt": prompt},
        "parameters": {"style": "<auto>", "size": f"{width}*{height}", "n": 1},
    }
    res = requests.post(submit_url, headers=headers, json=payload, timeout=30)
    res.raise_for_status()
    task_id = res.json().get("output", {}).get("task_id")
    if not task_id:
        raise ValueError(f"no task_id: {res.text[:200]}")

    poll_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    for _ in range(60):
        time.sleep(3)
        poll = requests.get(poll_url, headers={"Authorization": f"Bearer {api_key}"}, timeout=15)
        poll.raise_for_status()
        status = poll.json().get("output", {}).get("task_status", "")
        if status == "SUCCEEDED":
            results = poll.json().get("output", {}).get("results", [])
            if results and results[0].get("url"):
                img_data = requests.get(results[0]["url"], timeout=30).content
                if len(img_data) < 15_000:
                    raise ValueError("Qwen image too small")
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(img_data)
                return output_path
            raise ValueError("SUCCEEDED but no image URL")
        elif status == "FAILED":
            raise ValueError(f"Qwen task failed: {poll.text[:200]}")
    raise ValueError("Qwen task timed out (3 min)")


# ─── Provider registry ───────────────────────────────────────────────────────

PROVIDERS = {
    "pollinations": {
        "fn": route_pollinations,
        "needs": [],  # no API key required
        "strength": "free, no-auth, SANA/FLUX. Default primary.",
    },
    "gemini": {
        "fn": route_gemini,
        "needs": ["GEMINI_API_KEY"],
        "strength": "Google Imagen 3, best quality when credits available.",
    },
    "qwen": {
        "fn": route_qwen,
        "needs": ["DASHSCOPE_API_KEY"],
        "strength": "Alibaba Wanx, photorealistic + text rendering.",
    },
    "mage": {
        "fn": route_modal_mageflow,
        "needs": [],  # public Modal endpoint
        "strength": "Mage-Flow-Turbo via Modal. LAST RESORT — placeholder-prone.",
    },
}

# Pollinations FIRST — free, no auth, verified working
AUTO_PRIORITY = ["pollinations", "gemini", "qwen", "mage"]


def main():
    parser = argparse.ArgumentParser(description="I-ARIF LITE Image Router")
    parser.add_argument("--provider", type=str, default="auto",
                        choices=["auto"] + list(PROVIDERS.keys()),
                        help="Image provider (default: auto = Pollinations first)")
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--out", type=str,
                        default=f"/tmp/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    load_env()

    providers_to_try = AUTO_PRIORITY if args.provider == "auto" else [args.provider]
    errors = []

    for pname in providers_to_try:
        prov = PROVIDERS[pname]
        missing = [k for k in prov["needs"] if not os.getenv(k)]
        if missing:
            errors.append(f"{pname}: missing {', '.join(missing)}")
            continue

        print(f"[I-ARIF LITE] Trying {pname} ({prov['strength']})...")
        try:
            t0 = time.time()
            if pname == "gemini":
                result = prov["fn"](args.prompt, args.out)
            else:
                result = prov["fn"](args.prompt, args.out, args.width, args.height)
            elapsed = time.time() - t0
            size_kb = os.path.getsize(result) / 1024
            print(f"[I-ARIF LITE] OK in {elapsed:.1f}s: {result} ({size_kb:.0f} KB) via {pname}")
            print(f"OUTPUT_PATH={result}")
            print(f"PROVIDER={pname}")
            sys.exit(0)
        except Exception as e:
            err = f"{pname}: {e}"
            print(f"[I-ARIF LITE] FAIL: {err}", file=sys.stderr)
            errors.append(err)

    print("[I-ARIF LITE] ALL PROVIDERS FAILED:", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
