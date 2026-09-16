#!/usr/bin/env bash
# Voice-lane QC gate: round-trip transcribe a TTS take + surface word-level timestamps so a
# spoken tail artifact is distinguishable from a Whisper invention.
#
# Usage:  tts_roundtrip_qc.sh /abs/path/take.mp3
# Needs GROQ_API_KEY in the environment:
#   set +u; set -a; source /root/.secrets/kunci-root.env 2>/dev/null; set +a; set +u
#
# Read the output: the transcript is the falsification (garbled words = regenerate that take).
# The timestamp block is the tail check - any unscripted word with real separated timestamps
# past the last scripted word is IN THE AUDIO. Cut it hard, then re-run this script on the CUT.
set +u

AUDIO="${1:?usage: tts_roundtrip_qc.sh <audio-file>}"
K="${GROQ_API_KEY:-}"
[ -z "$K" ] && { echo "NO GROQ_API_KEY in env"; exit 2; }

TMP="$(mktemp -d)"
URL="https://api.groq.com/openai/v1/audio/transcriptions"

curl -s "$URL" -H "Authorization: Bearer $K" \
  -F file=@"$AUDIO" -F model=whisper-large-v3-turbo -F language=ms \
  -o "$TMP/plain.json"
curl -s "$URL" -H "Authorization: Bearer $K" \
  -F file=@"$AUDIO" -F model=whisper-large-v3-turbo -F language=ms \
  -F response_format=verbose_json -F "timestamp_granularities[]=word" \
  -o "$TMP/ts.json"

AUDIO="$AUDIO" TMP="$TMP" python3 - <<'PY'
import json, os, subprocess

tmp = os.environ["TMP"]
plain = json.load(open(f"{tmp}/plain.json"))
print("== round-trip text ==")
print(plain.get("text") or plain)

print("== tail (last 12 words, seconds) ==")
ts = json.load(open(f"{tmp}/ts.json"))
words = ts.get("words") or []
for w in words[-12:]:
    print(f"  {w['start']:6.2f}  {w['end']:6.2f}  {w['word']}")

if words:
    print(f"  audio_end={ts.get('duration')}  last_word_end={words[-1]['end']}")

# Print the true media duration so a stale/looping tail is visible against the transcript.
try:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", os.environ["AUDIO"]],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    print(f"  ffprobe_duration={out}")
except Exception as e:  # ffprobe missing is a local setup issue, not a take defect
    print(f"  ffprobe_duration=unavailable ({e})")

print("== verdict ==")
print("  unscripted word with real separated timestamps past the last scripted word")
print("  => tail artifact in the audio: hard-cut with -t, then re-run on the CUT.")
PY

rm -rf "$TMP"
