#!/usr/bin/env python3
"""i-ARIF V9 Voice Design — parametric synthesis via Qwen Token Plan.

F9 ANTI-HANTU COMPLIANT: no cloning of living persons. Design-from-description
and base-voice selection only. No public-figure audio anywhere in this pipeline.

Reality checks (token-plan-tts skill, verified 2026-08-18):
- Endpoint: Token Plan Singapore WebSocket (NOT default CN endpoint)
- Model: qwen-audio-3.0-tts-plus (cosyvoice-v1 fails on this plan)
- Voices: lowercase, no underscores. Working: longanlingxin (female warm),
  longanlufeng (male bright). 597 base voices, all Chinese/English-trained.
- Seat quota: QWEN_TEAM_OWNER_API_KEY has independent quota.
"""
import os
import sys
import traceback
from datetime import datetime

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat

dashscope.api_key = os.environ["QWEN_INDIVIDUAL_API_KEY"]  # Seat 4 (Seat 3 quota exhausted)
dashscope.base_websocket_api_url = (
    "wss://token-plan.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference"
)

OUT_DIR = "/root/AAA/audio/processed"
os.makedirs(OUT_DIR, exist_ok=True)

TEST_TEXT = (
    "Salam Arif. Sistem arifOS dah sedia. "
    "Parameter F satu dan F dua dah dilakarkan dengan tenang dan cermat."
)

ARCHETYPES = {
    # Archetype Alpha — Sopan-Penang (female / resonance focus)
    "alpha_sopan": {
        "voice": "longanlingxin",
        "instruction": (
            "Wanita Melayu loghat Penang, sopan lembut gemersik, "
            "sebutan jelas, tenang tanpa ketegangan vokal."
        ),  # 112 chars — within 128 cap
    },
    # Archetype Beta — Serak-Rendah (male / somatic focus)
    "beta_serak": {
        "voice": "longanlufeng",
        "instruction": (
            "Lelaki Melayu, suara garau serak basah, nada rendah, "
            "berwibawa, mesra santun, chest resonance."
        ),  # 118 chars — within 128 cap
    },
}


def synth(voice: str, text: str, instruction: str | None,
          model: str = "qwen-audio-3.0-tts-plus"):
    kwargs = dict(model=model, voice=voice,
                  format=AudioFormat.MP3_22050HZ_MONO_256KBPS)
    if instruction:
        kwargs["instruction"] = instruction
    s = SpeechSynthesizer(**kwargs)
    audio = s.call(text)
    if not audio:
        resp = s.get_last_response()
        raise RuntimeError(f"empty audio; last_response={resp}")
    return audio


def try_call(label: str, **kw):
    try:
        audio = synth(**kw)
        print(f"[OK]   {label}: {len(audio)} bytes")
        return audio
    except Exception as e:
        print(f"[FAIL] {label}: {type(e).__name__}: {str(e)[:300]}")
        return None


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # --- Probe 1: does this model accept the instruction parameter? ---
    a = ARCHETYPES["alpha_sopan"]
    audio_instr = try_call(
        "alpha+instruction", voice=a["voice"], text=TEST_TEXT,
        instruction=a["instruction"])

    audio_plain = None
    if audio_instr is None:
        # Fallback: no instruction kwarg — voice selection carries timbre
        audio_plain = try_call(
            "alpha baseline (no instruction)", voice=a["voice"],
            text=TEST_TEXT, instruction=None)

    chosen_alpha = audio_instr if audio_instr is not None else audio_plain
    if chosen_alpha is None:
        print("ALPHA FAILED on all routes — aborting.")
        sys.exit(1)

    path_a = f"{OUT_DIR}/iarif-v9-alpha-sopan_{stamp}.mp3"
    with open(path_a, "wb") as f:
        f.write(chosen_alpha)
    print(f"[SAVE] {path_a}")

    # --- Beta only if instruction route works (serak needs style control) ---
    b = ARCHETYPES["beta_serak"]
    audio_b = try_call(
        "beta+instruction", voice=b["voice"], text=TEST_TEXT,
        instruction=b["instruction"])
    if audio_b is None:
        audio_b = try_call(
            "beta baseline (no instruction)", voice=b["voice"],
            text=TEST_TEXT, instruction=None)
    if audio_b is not None:
        path_b = f"{OUT_DIR}/iarif-v9-beta-serak_{stamp}.mp3"
        with open(path_b, "wb") as f:
            f.write(audio_b)
        print(f"[SAVE] {path_b}")
    else:
        print("[WARN] Beta archetype failed — report only.")

    print("\nDONE. Instruction route:",
          "SUPPORTED" if audio_instr is not None else "NOT SUPPORTED")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
