#!/usr/bin/env bash
# F5-TTS Canon Voice Pipeline — Hermes command-provider compatible
# Template: bash /root/AAA/engines/f5tts_pipeline.sh {text_path} {output_path}
#
# Arif's canon voice via F5-TTS zero-shot clone from own voice sample.
# CPU inference only (no GPU on VPS). ~4 min per ~8s audio.
# Reference: /root/AAA/engines/f5tts/reference.wav (Arif's voice, 24.8s)
#
# F9 ANTI-HANTU: This voice IS Arif's own voice. No impersonation. No hantu.
# F13 SOVEREIGN: Arif authorized this clone.

set -euo pipefail

TEXT_FILE="${1:?usage: f5tts_pipeline.sh <text-file> <output-path>}"
OUT_PATH="${2:?usage: f5tts_pipeline.sh <text-file> <output-path>}"

# Reference audio (10s clip for faster inference)
REF_AUDIO="/root/AAA/engines/f5tts/reference-10s.wav"
# Reference text (matches the 10s clip content)
REF_TEXT="Pergi apa lagi? Perut-perut berangga. Memanglah suri rumah yang suka membeli."

WORK="$(mktemp -d /tmp/f5tts.XXXXXX)"
trap 'rm -rf "$WORK"' EXIT

# Read and normalize input text
TEXT=$(cat "$TEXT_FILE" | sed 's/[`*_#>]//g' | tr -s ' \n' ' ' | sed 's/^ *//;s/ *$//')

if [ -z "$TEXT" ]; then
    echo "f5tts_pipeline: empty text" >&2
    exit 1
fi

# Append seal if not present
SEAL="Ditempa bukan diberi."
if ! echo "$TEXT" | grep -qi "ditempa.*bukan.*diberi"; then
    TEXT="${TEXT} ${SEAL}"
fi

# Save normalized text
echo -n "$TEXT" > "$WORK/input.txt"

echo "f5tts_pipeline: generating audio (CPU, ~2-4 min)..." >&2

# Run F5-TTS inference
source /root/venv/bin/activate
python3 - "$WORK" "$REF_AUDIO" "$REF_TEXT" << 'PYEOF'
import sys, os
work = sys.argv[1]
ref_audio = sys.argv[2]
ref_text = sys.argv[3]
text = open(os.path.join(work, "input.txt")).read().strip()

os.environ["HF_HOME"] = "/root/.cache/huggingface"

from f5_tts.api import F5TTS
import soundfile as sf

tts = F5TTS(device="cpu")

wav, sr, _ = tts.infer(
    ref_file=ref_audio,
    ref_text=ref_text,
    gen_text=text,
    speed=1.0,
)

out_path = os.path.join(work, "output.wav")
sf.write(out_path, wav, sr)
print(f"f5tts_pipeline: {len(wav)/sr:.1f}s audio at {sr}Hz", file=sys.stderr)
PYEOF

# Convert to final output
ffmpeg -y -v error -i "$WORK/output.wav" -acodec pcm_s16le "$OUT_PATH" 2>/dev/null

if [ -f "$OUT_PATH" ]; then
    echo "f5tts_pipeline: output -> $OUT_PATH" >&2
else
    echo "f5tts_pipeline: FAILED - no output" >&2
    exit 1
fi
