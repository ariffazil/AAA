#!/usr/bin/env python3
"""alpha_zen_syedsuara — render Syed's ALPHA-ZEN column as TTS voice note.
Bonded homie voice: abang-sado-live-v1 (MiniMax speech-2.8-hd, speed 0.9).
Reuses /root/.hermes/scripts/sado_voice_trio.py for rendering.

Usage:
    python3 alpha_zen_syedsuara.py [--card cards/2026-09-28-morning.json] [--out /tmp/syedsuara.mp3]

    Without --card, auto-discovers latest ALPHA-ZEN card.
    Output: MP3 voice note of Syed's morning/night signals, in his voice.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import date

CARDS_DIR = Path("/root/AAA/forge_work/alpha-zen/cards")
TRIO_SCRIPT = Path("/root/.hermes/scripts/sado_voice_trio.py")
OUT_DIR = Path("/root/AAA/forge_work/alpha-zen/voice")


def find_latest_card() -> Path | None:
    cards = sorted(CARDS_DIR.glob("*.json"), reverse=True)
    for c in cards:
        try:
            json.loads(c.read_text())
            return c
        except Exception:
            continue
    return None


def extract_syed_signals(card: dict) -> list[str]:
    """Extract Syed's lines: signals[] first, then rows[].syed.text as fallback."""
    lines = []

    # 1. Signal card lines (the published ones)
    signals = card.get("signals", [])
    for s in signals:
        if s.get("who") == "syed" and s.get("text", "").strip():
            lines.append(s["text"].strip())

    # 2. Row pool — Syed's column from the 9 rows (candidates)
    rows = card.get("rows", [])
    for r in rows:
        syed = r.get("syed", {})
        text = syed.get("text", "").strip()
        if text and text not in lines:  # dedupe against signals
            lines.append(text)

    return lines


def lines_to_paragraph(lines: list[str]) -> str:
    """Convert signal lines into a natural spoken paragraph."""
    if not lines:
        return ""
    # Join with pauses — comma-separated in speech
    paragraph = ". ".join(line.rstrip(".") for line in lines) + "."
    # Clean up any double punctuation
    paragraph = paragraph.replace("..", ".")
    return paragraph


def render_voice(text: str, out_path: str) -> bool:
    """Render text as abang-sado-live-v1 TTS audio."""
    if not text.strip():
        print("syedsuara: no text to render", file=sys.stderr)
        return False

    # Write text to temp file for the renderer
    tmp_text = f"/tmp/syedsuara_{os.getpid()}.txt"
    with open(tmp_text, "w", encoding="utf-8") as f:
        f.write(text)

    try:
        # Route through iarif_tts_pipeline with abang-sado-live-v1
        result = subprocess.run(
            [
                "bash",
                "/root/AAA/engines/iarif_tts_pipeline.sh",
                tmp_text,
                out_path,
                "abang-sado-live-v1",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            print(f"syedsuara: TTS render failed: {result.stderr[-300:]}", file=sys.stderr)
            return False
        return Path(out_path).exists() and Path(out_path).stat().st_size > 0
    except Exception as e:
        print(f"syedsuara: TTS render error: {e}", file=sys.stderr)
        return False
    finally:
        if os.path.exists(tmp_text):
            os.remove(tmp_text)


def main():
    ap = argparse.ArgumentParser(description="Render Syed's ALPHA-ZEN column as TTS voice note")
    ap.add_argument("--card", help="Path to ALPHA-ZEN card JSON (auto-discover if omitted)")
    ap.add_argument("--out", help="Output MP3 path (default: alpha-zen/voice/<date>-syedsuara.mp3)")
    ap.add_argument("--mode", choices=["morning", "night", "auto"], default="auto")
    ap.add_argument("--dry-run", action="store_true", help="Print text that would be rendered, no TTS")
    args = ap.parse_args()

    # Resolve card
    card_path = Path(args.card) if args.card else find_latest_card()
    if not card_path or not card_path.exists():
        print("syedsuara: no ALPHA-ZEN card found", file=sys.stderr)
        sys.exit(1)

    card = json.loads(card_path.read_text())
    mode = card.get("mode", args.mode)
    card_date = card.get("date", date.today().isoformat())

    # Extract Syed's lines
    lines = extract_syed_signals(card)
    if not lines:
        print(f"syedsuara: no Syed signals in {card_path}", file=sys.stderr)
        sys.exit(0)

    paragraph = lines_to_paragraph(lines)

    if args.dry_run:
        print(f"=== SYED VOICE ({mode}, {card_date}) ===")
        print(paragraph)
        print(f"=== {len(lines)} lines, {len(paragraph)} chars ===")
        sys.exit(0)

    # Render
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = args.out or str(OUT_DIR / f"{card_date}-{mode}-syedsuara.mp3")

    ok = render_voice(paragraph, out_path)
    if ok:
        dur = ""
        try:
            r = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out_path],
                capture_output=True,
                text=True,
                timeout=10,
            )
            dur = f" {float(r.stdout.strip()):.1f}s"
        except Exception:
            pass
        print(f"OK abang-sado-live-v1 → {out_path} ({len(lines)} lines,{dur} {Path(out_path).stat().st_size} bytes)")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
