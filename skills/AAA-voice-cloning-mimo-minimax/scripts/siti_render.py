#!/usr/bin/env python3
"""
siti_render.py — Canonical MiniMax TTS render using sealed Siti voice.

This wrapper exists to lock in the recipe that the SOUL.md / MEMORY.md
canonical recipe records. The recipe is sensitive: missing
`language_boost=Malay` or wrong decode (base64 instead of hex) silently
produces bad audio that sounds "almost right" but isn't.

Use this script instead of writing the payload inline. The inline
construction has regressed at least twice in 2026-10 sessions.

Usage:
    python3 siti_render.py "Text to speak" /tmp/out.mp3
    echo "Hello" | python3 siti_render.py - /tmp/out.mp3
    python3 siti_render.py --speed 0.85 --pitch -2 "Text" /tmp/out.mp3

Env required: MINIMAX_API_KEY (loaded from /root/.secrets/a-forge.env on KVM8
or /root/.openclaw/.env on KVM4 — KVM4 key has been empty as of 2026-10-02,
use KVM8 path).

Exit code 0 = success, file written. Non-zero = see stderr.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error

# Sealed canonical recipe (do not change without F13)
DEFAULT_VOICE = "SSSiti20260926v1"
DEFAULT_MODEL = "speech-2.8-hd"
ENDPOINT = "https://api.minimax.io/v1/t2a_v2"


def load_key():
    """Load MINIMAX_API_KEY from the canonical env files."""
    for envfile in ("/root/.secrets/a-forge.env", "/root/.openclaw/.env"):
        if os.path.exists(envfile):
            result = subprocess.run(
                ["bash", "-c", f"source {envfile} && echo $MINIMAX_API_KEY"],
                capture_output=True, text=True, check=False,
            )
            key = result.stdout.strip()
            if key:
                return key
    return os.environ.get("MINIMAX_API_KEY", "")


def render(text, out_path, voice_id=DEFAULT_VOICE, model=DEFAULT_MODEL,
           speed=1.0, vol=1.0, pitch=0, language_boost="Malay",
           sample_rate=32000, bitrate=128000, fmt="mp3"):
    key = load_key()
    if not key:
        print("ERROR: MINIMAX_API_KEY not loaded from any env file", file=sys.stderr)
        return 1

    payload = {
        "model": model,
        "text": text,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
        },
        "audio_setting": {
            "sample_rate": sample_rate,
            "bitrate": bitrate,
            "format": fmt,
        },
        "language_boost": language_boost,
    }

    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}", file=sys.stderr)
        print(e.read().decode()[:500], file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Request error: {e}", file=sys.stderr)
        return 3

    # Verify success
    base = result.get("base_resp", {})
    if base.get("status_code") != 0:
        print(f"API error: {base}", file=sys.stderr)
        return 4

    # Decode audio — HEX, not base64
    audio_hex = result.get("data", {}).get("audio")
    if not audio_hex:
        print("ERROR: no audio in response", file=sys.stderr)
        return 5

    try:
        audio_bytes = bytes.fromhex(audio_hex)
    except ValueError:
        print("ERROR: data.audio is not valid hex (likely a recipe regression)", file=sys.stderr)
        return 6

    with open(out_path, "wb") as f:
        f.write(audio_bytes)

    print(f"OK {out_path} {os.path.getsize(out_path)}B "
          f"voice={voice_id} speed={speed} pitch={pitch} lang={language_boost}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Render TTS with sealed Siti voice")
    ap.add_argument("text", help="Text to speak (or '-' for stdin)")
    ap.add_argument("out", help="Output MP3 path")
    ap.add_argument("--voice-id", default=DEFAULT_VOICE)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--vol", type=float, default=1.0)
    ap.add_argument("--pitch", type=int, default=0)
    ap.add_argument("--language-boost", default="Malay")
    args = ap.parse_args()

    text = sys.stdin.read() if args.text == "-" else args.text
    return render(
        text, args.out,
        voice_id=args.voice_id,
        model=args.model,
        speed=args.speed,
        vol=args.vol,
        pitch=args.pitch,
        language_boost=args.language_boost,
    )


if __name__ == "__main__":
    sys.exit(main())
