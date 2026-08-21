#!/usr/bin/env bash
# i-ARIF sovereign TTS pipeline — Hermes command-provider compatible.
# Template: bash /root/AAA/engines/iarif_tts_pipeline.sh {text_path} {output_path}
#
# Layer 2 — CODE, not prompt.
#   Strip contradiction tropes (family, not one phrase).
#   Strip markdown so TTS does not speak asterisks.
#   Append "Ditempa bukan diberi." even if the model forgets.
# Layer 3 is DSP. This script does not depend on DSP succeeding (fail-open).
# Layer 1 is the persona file. This script does not read it.
#
# Stage 1: MiniMax speech-2.8-hd, voice i-ARIF-20260819T084602 (V8 synthetic Penang)
# Stage 2: WORLD + analytic jiwa (A/f/φ) -> F0 lock 239 Hz + stillness + coda
# Fail-open: if stage 2 fails, deliver stage-1 audio rather than no voice.
# GPU: NEVER. No runpod, no F5-TTS, no rental.
set -o pipefail

TEXT_FILE="${1:?usage: iarif_tts_pipeline.sh <text-file> <output-path>}"
OUT_PATH="${2:?usage: iarif_tts_pipeline.sh <text-file> <output-path>}"
TARGET_F0="${IARIF_TARGET_F0:-239}"
LIFT="${IARIF_LIFT:-35}"
VOICE_ID="${IARIF_VOICE_ID:-i-ARIF-20260819T084602}"
DSP="${IARIF_DSP:-/root/forge_work/dsp/dsp_stabilizer.py}"

# 5-R Protocol: disable nounset during source (env file has forward-references)
set +u
set -a
source /root/.secrets/kunci-root.env
set +a
set -u

WORK="$(mktemp -d /tmp/iarif_tts.XXXXXX)"
trap 'rm -rf "$WORK"' EXIT

# ---- Text normalization: code-enforced, model-independent ----
python3 - "$TEXT_FILE" "$WORK/input.txt" <<'PY'
import re, sys
src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()

# Markdown / TTS-poison (spoken asterisks, hashes, fences)
text = re.sub(r"```.*?```", " ", text, flags=re.S)
text = re.sub(r"`+", "", text)
text = re.sub(r"\[(?P<t>breath|sigh|dry|settle|literal|hold|emph|uv_break|seal)\]", " ", text, flags=re.I)
text = re.sub(r"[*_#>]+", " ", text)

FORBIDDEN = [
    r"lembut\s+tapi\s+besi",
    r"lembut\s+tapi\s+tegas",
    r"lembut\s+tapi\s+kuat",
    r"lembut\s+tapi\s+bukan\s+lembut[^.]*",
    r"soft\s+but\s+steel",
    r"soft\s+but\s+strong",
    r"gentle\s+but\s+firm",
    r"iron\s+fist\s+in\s+a\s+velvet[^.]*",
    r"velvet\s+glove",
]
for pat in FORBIDDEN:
    text = re.sub(pat, " ", text, flags=re.I)

text = re.sub(r"[ \t]+", " ", text)
text = re.sub(r"\n{3,}", "\n\n", text)
text = text.strip()

SEAL = "Ditempa bukan diberi."
seal_re = re.compile(r"ditempa\s*,?\s*bukan\s+diberi\.?", re.I)
if not seal_re.search(text):
    text = (text + " " + SEAL).strip()
else:
    # collapse variants to the canonical seal once, at the end
    text = seal_re.sub("", text).strip()
    text = (text + " " + SEAL).strip()
    text = re.sub(r"[ \t]+", " ", text)

open(dst, "w", encoding="utf-8").write(text)
print("layer2-ok", file=sys.stderr)
PY
export IARIF_TEXT_FILE="$(realpath "$WORK/input.txt")"

# ---- Stage 1: MiniMax synthesis ----
python3 - "$WORK" "$VOICE_ID" <<'PYEOF'
import sys, os, json, urllib.request
work, voice_id = sys.argv[1], sys.argv[2]
text = open(os.environ["IARIF_TEXT_FILE"]).read().strip()
if not text:
    raise SystemExit("empty text")
key = os.environ["MINIMAX_API_KEY"]
req = urllib.request.Request(
    "https://api.minimax.io/v1/t2a_v2",
    data=json.dumps({
        "model": "speech-2.8-hd",
        "text": text,
        "voice_setting": {"voice_id": voice_id, "speed": 1.0, "vol": 1.0, "pitch": 0, "emotion": "neutral"},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
    }).encode(),
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
)
resp = json.loads(urllib.request.urlopen(req, timeout=90).read())
br = resp.get("base_resp", {})
if br.get("status_code", 0) != 0:
    raise SystemExit(f"MiniMax error {br.get('status_code')}: {br.get('status_msg')}")
open(f"{work}/raw.mp3", "wb").write(bytes.fromhex(resp["data"]["audio"]))
print("stage1-ok", file=sys.stderr)
PYEOF
# MiniMax down (quota/auth) -> Stage 1M: MiMo Token Plan (Xiaomi, token-plan-sgp).
# Verified live 2026-08-21: chat/completions + modalities:["audio"] returns MP3.
# Text rides in role:assistant; user role carries delivery instruction (BM).
# Identity is Stage 2 DSP (F0 lock 239 Hz + formant-first) — provider-agnostic.
if [ ! -s "$WORK/raw.mp3" ]; then
  echo "iarif_tts_pipeline: stage 1 (MiniMax) failed -- trying MiMo Token Plan" >&2
  IARIF_MIMO_VOICE="${IARIF_MIMO_VOICE:-冰糖}" python3 - "$WORK" <<'PYMIMO'
import sys, os, json, urllib.request, base64
work = sys.argv[1]
text = open(os.environ["IARIF_TEXT_FILE"]).read().strip()
key = os.environ["MIMO_API_KEY"]
voice = os.environ.get("IARIF_MIMO_VOICE", "冰糖")
req = urllib.request.Request(
    "https://token-plan-sgp.xiaomimimo.com/v1/chat/completions",
    data=json.dumps({
        "model": "mimo-v2.5-tts",
        "modalities": ["audio"],
        "audio": {"voice": voice, "format": "mp3"},
        "messages": [
            {"role": "user", "content": "Read the assistant text aloud in Malay, warm and composed."},
            {"role": "assistant", "content": text},
        ],
    }).encode(),
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
)
resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
audio = resp["choices"][0]["message"]["audio"]["data"]
open(f"{work}/raw.mp3", "wb").write(base64.b64decode(audio))
print("stage1m-ok", file=sys.stderr)
PYMIMO
fi
if [ ! -s "$WORK/raw.mp3" ]; then
  echo "iarif_tts_pipeline: stage 1 (MiniMax + MiMo) failed -- failing to edge-tts (ms-MY-YasminNeural)" >&2
  python3 - "$WORK" <<'PYEDGE'
import sys, os, asyncio
work = sys.argv[1]
text = open(os.environ["IARIF_TEXT_FILE"]).read().strip()
async def main():
    import edge_tts
    tts = edge_tts.Communicate(text, "ms-MY-YasminNeural", rate="+5%")
    await tts.save(f"{work}/raw.mp3")
asyncio.run(main())
print("stage1e-ok", file=sys.stderr)
PYEDGE
fi
if [ ! -s "$WORK/raw.mp3" ]; then
  echo "iarif_tts_pipeline: all synthesis lanes failed" >&2
  exit 1
fi

# ---- Stage 2: jiwa A/f/φ stabilizer (fail-open, CPU, no GPU) ----
if python3 "$DSP" \
     "$WORK/raw.mp3" "$WORK/stabilized.wav" \
     --target-f0 "$TARGET_F0" --lift "$LIFT" >&2; then
  cp "$WORK/stabilized.wav" "$OUT_PATH"
  echo "iarif_tts_pipeline: envelope-locked output -> $OUT_PATH" >&2
else
  echo "iarif_tts_pipeline: stage 2 failed -- fail-open with raw voice" >&2
  ffmpeg -y -v error -i "$WORK/raw.mp3" -c:a pcm_s16le "$OUT_PATH"
fi
