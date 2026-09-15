#!/usr/bin/env bash
# i-ARIF Stage-1 synthesis — three lanes, verbatim from iarif_tts_pipeline.sh.
# Extracted 2026-09-15 so the duration guard can re-render without duplicating logic.
#
# Usage: iarif_synth_stage1.sh <work_dir> <voice_id> <text_file>
# Writes: <work_dir>/raw.mp3   Exits 0 if audio produced, 1 otherwise.
set -eo pipefail

WORK="${1:?usage: iarif_synth_stage1.sh <work_dir> <voice_id> <text_file>}"
VOICE_ID="${2:?voice_id required}"
TEXT_FILE="${3:?text_file required}"
export IARIF_TEXT_FILE="$(realpath "$TEXT_FILE")"

# ---- Stage 1: MiniMax synthesis ----
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
  echo "iarif_synth_stage1: Stage 1 MiniMax failed, falling back to MiMo" >&2
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
  echo "iarif_synth_stage1: Falling back to Edge-TTS" >&2
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
  echo "iarif_synth_stage1: all synthesis lanes failed" >&2
  exit 1
fi
exit 0
