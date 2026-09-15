#!/usr/bin/env python3
"""Surgically wire the voice resolver + duration guard into iarif_tts_pipeline.sh.

Fails loudly if anchors are missing (never silently half-patches).
"""
import re
import shutil
import sys
import time

P = "/root/AAA/engines/iarif_tts_pipeline.sh"
src = open(P, encoding="utf-8").read()
bak = f"{P}.bak-{time.strftime('%Y%m%d-%H%M%S')}"
shutil.copy2(P, bak)
print("backup:", bak)

# ---------- 1. Voice resolver (fail-closed on REVOKED) ----------
OLD_VOICE = 'VOICE_ID="${IARIF_VOICE_ID:-iarif-sovereign-v9}"'
NEW_VOICE = '''VOICE_ID_REQUESTED="${IARIF_VOICE_ID:-iarif-sovereign-v9}"
REGISTRY_PATH="${IARIF_VOICE_REGISTRY:-/root/AAA/audio/voice-registry.json}"

# ---- Voice-id resolution: canonical registry, FAIL-CLOSED on REVOKED ----
# The registry is the source of truth. An unresolved or revoked id aborts BEFORE
# synthesis, so a revoked checkpoint can never be reached via default or fallback.
if ! VOICE_ID="$(python3 /root/AAA/engines/resolve_voice_id.py "$VOICE_ID_REQUESTED")"; then
  rc=$?
  echo "iarif_tts_pipeline: VOICE RESOLUTION FAILED (rc=$rc) for '$VOICE_ID_REQUESTED' — refusing to synthesize" >&2
  exit 3
fi
echo "iarif_tts_pipeline: voice resolved $VOICE_ID_REQUESTED -> $VOICE_ID" >&2'''

if OLD_VOICE not in src:
    sys.exit("ANCHOR 1 MISSING: voice_id line not found")
if src.count(OLD_VOICE) != 1:
    sys.exit(f"ANCHOR 1 AMBIGUOUS: {src.count(OLD_VOICE)} occurrences")
src = src.replace(OLD_VOICE, NEW_VOICE)

# ---------- 2. Replace inline synthesis with guarded retry loop ----------
START = "# ---- Stage 1: MiniMax synthesis"
END = '  echo "iarif_tts_pipeline: all synthesis lanes failed" >&2\n  exit 1\nfi'

i = src.find(START)
j = src.find(END)
if i == -1 or j == -1:
    sys.exit(f"ANCHOR 2 MISSING: start={i} end={j}")
j_end = j + len(END)

NEW_BLOCK = '''# ---- Stage 1 + duration guard: bounded re-render on silent failure ----
# Motivating incidents (2026-09-15): MiniMax returned 0.216 s for 88 chars with
# status_code 0 (and 180-252 ms for some emotion values). Those near-empty
# artifacts transcribe as Whisper boilerplate ("Terima kasih kerana menonton!")
# and would otherwise ship silently. Success code is NOT evidence of usable audio.
CHARS=$(python3 -c "import os;print(len(open(os.environ['IARIF_TEXT_FILE']).read().strip()))")
ATTEMPT=0
MAX_RERENDERS=2
while :; do
  rm -f "$WORK/raw.mp3"
  if ! bash "$(dirname "$(realpath "$0")")/iarif_synth_stage1.sh" "$WORK" "$VOICE_ID" "$WORK/input.txt"; then
    echo "iarif_tts_pipeline: synthesis produced no audio" >&2
    exit 1
  fi
  if python3 /root/AAA/engines/audio_duration_guard.py "$WORK/raw.mp3" "$CHARS"; then
    break
  fi
  ATTEMPT=$((ATTEMPT + 1))
  if [ "$ATTEMPT" -gt "$MAX_RERENDERS" ]; then
    echo "iarif_tts_pipeline: FAILING EXPLICITLY — audio unusable after $ATTEMPT re-renders (chars=$CHARS). Refusing to emit a silent-failure artifact." >&2
    exit 6
  fi
  echo "iarif_tts_pipeline: duration guard blocked the render — re-render $ATTEMPT/$MAX_RERENDERS" >&2
done'''

src = src[:i] + NEW_BLOCK + src[j_end:]
open(P, "w", encoding="utf-8").write(src)

# ---------- verify ----------
out = open(P, encoding="utf-8").read()
checks = {
    "resolver wired": "resolve_voice_id.py" in out,
    "fail-closed exit 3": "exit 3" in out,
    "guard wired": "audio_duration_guard.py" in out,
    "retry loop": "MAX_RERENDERS" in out,
    "explicit failure": "FAILING EXPLICITLY" in out,
    "no leftover inline minimax": "Pure V8 Studio HD" not in out,
    "no duplicate lane code": out.count("MINIMAX_API_KEY not found") == 0,
}
for k, v in checks.items():
    print(f"{'OK ' if v else 'FAIL'} {k}")
print("lines:", len(out.splitlines()))
