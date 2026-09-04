#!/usr/bin/env bash
# i-ARIF Sovereign V8 Pure Studio TTS Pipeline
# Direct Full Studio Fidelity (32kHz / 128kbps) from MiniMax speech-2.8-hd (V8)
# Zero vocoder phase noise. Zero artificial F0 distortion.
set -eo pipefail

TEXT_FILE="${1:?usage: iarif_tts_pipeline.sh <text-file> <output-path>}"
OUT_PATH="${2:?usage: iarif_tts_pipeline.sh <text-file> <output-path>}"
VOICE_ID="${IARIF_VOICE_ID:-i-ARIF-20260819T084602}"

WORK="$(mktemp -d /tmp/iarif_tts.XXXXXX)"
trap 'rm -rf "$WORK"' EXIT

# ---- Text normalization: clean Markdown & ban clichés ----
python3 - "$TEXT_FILE" "$WORK/input.txt" <<'PY'
import re, sys
src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()

# Markdown & TTS-poison removal
text = re.sub(r"```.*?```", " ", text, flags=re.S)
text = re.sub(r"`+", "", text)
text = re.sub(r"\[(?P<t>breath|sigh|dry|settle|literal|hold|emph|uv_break|seal)\]", " ", text, flags=re.I)
text = re.sub(r"[*_#>]+", " ", text)

# Strictly ban cheesy tropes
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

open(dst, "w", encoding="utf-8").write(text)
PY

export IARIF_TEXT_FILE="$(realpath "$WORK/input.txt")"

# ---- Stage 1: MiniMax synthesis (Pure V8 Studio HD) ----
python3 - "$WORK" "$VOICE_ID" <<'PYEOF'
import sys, os, json, urllib.request
work, voice_id = sys.argv[1], sys.argv[2]
text = open(os.environ["IARIF_TEXT_FILE"]).read().strip()
if not text:
    raise SystemExit("empty text")

# Resolve API Key
key = os.environ.get("MINIMAX_API_KEY")
if not key:
    for env_path in ["/root/.secrets/kunci-root.env", "/root/.secrets/kunci-mas.env"]:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if "MINIMAX_API_KEY=" in line:
                        key = line.split("MINIMAX_API_KEY=", 1)[1].strip().strip(' "\'')
                        break
        if key:
            break

if not key:
    raise SystemExit("MINIMAX_API_KEY not found in env or secrets")

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
PYEOF

# Failover 1: MiMo Token Plan
if [ ! -s "$WORK/raw.mp3" ]; then
  echo "iarif_tts_pipeline: Stage 1 MiniMax failed, falling back to MiMo" >&2
  python3 - "$WORK" <<'PYMIMO'
import sys, os, json, urllib.request, base64
work = sys.argv[1]
text = open(os.environ["IARIF_TEXT_FILE"]).read().strip()
key = os.environ.get("MIMO_API_KEY")
if not key:
    for env_path in ["/root/.secrets/kunci-root.env", "/root/.secrets/kunci-mas.env"]:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if "MIMO_API_KEY=" in line:
                        key = line.split("MIMO_API_KEY=", 1)[1].strip().strip(' "\'')
                        break
        if key:
            break
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
PYMIMO
fi

# Failover 2: Edge-TTS
if [ ! -s "$WORK/raw.mp3" ]; then
  echo "iarif_tts_pipeline: Falling back to Edge-TTS" >&2
  python3 - "$WORK" <<'PYEDGE'
import sys, os, asyncio
work = sys.argv[1]
text = open(os.environ["IARIF_TEXT_FILE"]).read().strip()
async def main():
    import edge_tts
    tts = edge_tts.Communicate(text, "ms-MY-YasminNeural", rate="+5%")
    await tts.save(f"{work}/raw.mp3")
asyncio.run(main())
PYEDGE
fi

if [ ! -s "$WORK/raw.mp3" ]; then
  echo "iarif_tts_pipeline: all synthesis lanes failed" >&2
  exit 1
fi

# ── Stage 2: DSP Stabilizer — V9 Nusantara ──────────────────────
# WORLD vocoder: F0 lock 239 Hz + amplitude stillness + terminal lift + coda adab
DSP="/root/forge_work/dsp/dsp_stabilizer.py"
STABILIZED="$WORK/stabilized.wav"

if [ -f "$DSP" ]; then
  python3 "$DSP" "$WORK/raw.mp3" "$STABILIZED" --target-f0 239 --lift 35 2>"$WORK/dsp.log" || {
    echo "iarif_tts_pipeline: DSP stabilizer failed (non-critical) — falling through to raw" >&2
    STABILIZED="$WORK/raw.mp3"
  }
  if [ -f "$WORK/dsp.log" ] && [ -s "$WORK/dsp.log" ]; then
    echo "iarif_tts_pipeline: V9 DSP meta: $(head -1 "$WORK/dsp.log")" >&2
  fi
else
  echo "iarif_tts_pipeline: DSP stabilizer not found at $DSP — skipping V9 processing" >&2
  STABILIZED="$WORK/raw.mp3"
fi

# Convert stabilized audio to requested format
case "$(basename "$OUT_PATH" | sed 's/.*\.//')" in
  ogg)  ffmpeg -y -v error -i "$STABILIZED" -c:a libopus -b:a 64k -ar 48000 "$OUT_PATH" ;;
  mp3)  ffmpeg -y -v error -i "$STABILIZED" -c:a libmp3lame -q:a 2 "$OUT_PATH" ;;
  wav)  ffmpeg -y -v error -i "$STABILIZED" -c:a pcm_s16le "$OUT_PATH" ;;
  *)    ffmpeg -y -v error -i "$STABILIZED" -c:a libopus -b:a 64k -ar 48000 "$OUT_PATH" ;;
esac
echo "iarif_tts_pipeline: V9 Nusantara → $OUT_PATH" >&2
