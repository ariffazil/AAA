#!/usr/bin/env bash
# i-ARIF Sovereign V9 Pure Studio TTS Pipeline
# Direct Full Studio Fidelity (32kHz / 128kbps) from MiniMax speech-2.8-hd (V9)
# Zero vocoder phase noise. Zero artificial F0 distortion.
set -eo pipefail

TEXT_FILE="${1:?usage: iarif_tts_pipeline.sh <text-file> <output-path> [voice-id]}"
OUT_PATH="${2:?usage: iarif_tts_pipeline.sh <text-file> <output-path> [voice-id]}"
# Voice selection order: explicit 3rd arg (lane-selectable) > IARIF_VOICE_ID env > canonical default.
# An explicit arg does NOT weaken the gate below: registry resolution still FAILS CLOSED
# on REVOKED or unknown ids, so no caller can route around the V8 revocation.
VOICE_ID="${3:-${IARIF_VOICE_ID:-iarif-sovereign-v9}}"

# ---- V8/V9 registry resolution — FAIL CLOSED on REVOKED voices (F1 AMANAH) ----
# The voice-registry.json is canonical. Any REVOKED or unknown id aborts before
# synthesis. This closes the V8 contamination hole: even an env override to the
# V8 checkpoint id (i-ARIF-20260819T084602) is refused here, not passed upstream.
VOICE_ID="$(python3 - "$VOICE_ID" <<'PYREG'
import sys, json
vid = sys.argv[1]
r = json.load(open("/root/AAA/audio/voice-registry.json"))
canon = r.get("aliases", {}).get(vid, vid)
v = r.get("voices", {}).get(canon)
if v is None:
    sys.stderr.write(f"UNKNOWN voice id {vid} (canonical {canon}) — not in registry\n")
    sys.exit(1)
if v.get("status") == "REVOKED":
    sys.stderr.write(f"REVOKED voice id {vid} — refused by registry ({v.get('reason','')})\n")
    sys.exit(1)
print(v.get("provider_voice_id", vid))
PYREG
)" || { echo "iarif_tts_pipeline: voice id $VOICE_ID refused by registry — abort (fail closed)" >&2; exit 1; }

WORK="$(mktemp -d /tmp/iarif_tts.XXXXXX)"
trap 'rm -rf "$WORK"' EXIT

# ---- Text normalization: clean Markdown, typos & ban clichés ----
python3 - "$TEXT_FILE" "$WORK/input.txt" <<'PY'
import re, sys
src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()

# Markdown & TTS-poison removal
text = re.sub(r"```.*?```", " ", text, flags=re.S)
text = re.sub(r"`+", "", text)
text = re.sub(r"\[(?P<t>breath|sigh|dry|settle|literal|hold|emph|uv_break|seal)\]", " ", text, flags=re.I)
text = re.sub(r"[*_#>]+", " ", text)

# Typo repairs
text = re.sub(r"\blengkuk\s+utara\b", "lenggok utara", text, flags=re.I)
text = re.sub(r"\bsantuan\b", "santun", text, flags=re.I)

# Strictly ban cheesy tropes and unconstitutional honorifics (SOUL.md)
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
    r"\bSir\b",
]
for pat in FORBIDDEN:
    text = re.sub(pat, " ", text, flags=re.I)

text = re.sub(r"[ \t]+", " ", text)
text = re.sub(r"\n{3,}", "\n\n", text)
text = text.strip()

open(dst, "w", encoding="utf-8").write(text)
PY

export IARIF_TEXT_FILE="$(realpath "$WORK/input.txt")"

# ---- Duration guard + auto re-render (max 3 attempts) ----
# BM pacing 8–12 chars/s. A render far below the floor (e.g. the 0.216s transient
# drop) is a SILENT failure: returning success would feed Whisper truncated noise
# and produce a hallucinated transcript. Fail CLOSED, re-render up to 2 extra
# attempts, and if still below floor, abort so downstream ASR never sees it.
_DUR="0"
_DUR_OK=0
set +e
for _ATTEMPT in 1 2 3; do
  rm -f "$WORK/raw.mp3"

# ---- Stage 1: MiniMax synthesis (Pure V9 Studio HD) ----
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
sys.stderr.write(f"IARIF_ENGINE=minimax {voice_id} (Tier 1, rented)\n")
PYEOF

# ---- Failover 1: PIPER — SOVEREIGN, offline, CPU, zero quota ----
# Inserted 2026-09-18 after live probing on KVM8.
#   * MiniMax 2056 lands on a 4-HOUR INTERVAL cap that is separate from the weekly
#     cap — the lane goes quiet mid-session while weekly headroom remains.
#   * The rung below it was MiMo, FALSIFIED for BM (nusantara-voice-stack §3):
#     falling through swapped voice identity for a mangled one, silently.
#   * Piper renders BM on CPU at 22.05 kHz with no network and no key.
# KNOWN LIMIT: mangles ENGLISH words inside code-switch (the→teh, everyone→eferione);
# BM words are clean. Use for BM-dominant text. The engine is LABELLED on stderr so
# the delivery message can name what actually spoke — never a silent swap.
if [ ! -s "$WORK/raw.mp3" ] && [ ! -s "$WORK/raw.wav" ]; then
  PIPER_BIN="${IARIF_PIPER_BIN:-/usr/local/bin/piper}"
  PIPER_MODEL="${IARIF_PIPER_MODEL:-/root/forge_work/piper-sovereign/id_voice.onnx}"
  if [ -x "$PIPER_BIN" ] && [ -s "$PIPER_MODEL" ]; then
    echo "iarif_tts_pipeline: MiniMax unavailable → SOVEREIGN FALLBACK Piper (id_ID, offline, zero-quota)" >&2
    "$PIPER_BIN" -m "$PIPER_MODEL" -f "$WORK/raw.wav" < "$WORK/input.txt" >/dev/null 2>&1 || true
    if [ -s "$WORK/raw.wav" ]; then
      echo "IARIF_ENGINE=piper id_ID-news_tts-medium (SOVEREIGN)" >&2
    fi
  fi
fi

# Failover 2: MiMo Token Plan (LAST RESORT — falsified for BM, gap filler only)
if [ ! -s "$WORK/raw.mp3" ] && [ ! -s "$WORK/raw.wav" ]; then
  echo "iarif_tts_pipeline: Stage 1 MiniMax failed, falling back to MiMo (LAST RESORT — BM unreliable)" >&2
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

# Failover 3: Edge-TTS (cloud, not sovereign — kept as a free last rung below Piper)
if [ ! -s "$WORK/raw.mp3" ] && [ ! -s "$WORK/raw.wav" ]; then
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

if [ ! -s "$WORK/raw.mp3" ] && [ ! -s "$WORK/raw.wav" ]; then
  echo "iarif_tts_pipeline: attempt $_ATTEMPT produced no audio — retry" >&2
  continue
fi

# ---- Duration check (fail closed on truncated/silent render) ----
_chars=$(python3 -c "print(len(open('$WORK/input.txt', encoding='utf-8').read()))")
_floor=$(python3 -c "print(max(0.4 * (float('$_chars')/12.0), 2.0))")
_RAW=""
[ -s "$WORK/raw.mp3" ] && _RAW="$WORK/raw.mp3"
[ -z "$_RAW" ] && [ -s "$WORK/raw.wav" ] && _RAW="$WORK/raw.wav"
_DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "${_RAW:-$WORK/raw.mp3}" 2>/dev/null || echo 0)
_DUR_OK=$(python3 -c "print(1 if float('$_DUR') >= float('$_floor') else 0)")
if [ "$_DUR_OK" = "1" ]; then
  break
fi
echo "iarif_tts_pipeline: attempt $_ATTEMPT duration ${_DUR}s < floor ${_floor}s (chars=$_chars) — re-render" >&2
done
set -e

if [ "$_DUR_OK" != "1" ]; then
  echo "iarif_tts_pipeline: duration guard FAILED after 3 attempts (last ${_DUR}s < floor ${_floor}s) — abort, do NOT return success" >&2
  exit 1
fi

# ── Stage 2: Pure Neural Studio Passthrough (Bypassing Vocoder) ──
# Raw studio neural audio. Zero vocoder phase distortion. Spectral Flatness 125.89.
if [ -s "$WORK/raw.mp3" ]; then
  STABILIZED="$WORK/raw.mp3"
else
  STABILIZED="$WORK/raw.wav"   # sovereign Piper rung
fi

# Convert stabilized audio to requested format
case "$(basename "$OUT_PATH" | sed 's/.*\.//')" in
  ogg)  ffmpeg -y -v error -i "$STABILIZED" -c:a libopus -b:a 64k -ar 48000 "$OUT_PATH" ;;
  mp3)  ffmpeg -y -v error -i "$STABILIZED" -c:a libmp3lame -q:a 2 "$OUT_PATH" ;;
  wav)  ffmpeg -y -v error -i "$STABILIZED" -c:a pcm_s16le "$OUT_PATH" ;;
  *)    ffmpeg -y -v error -i "$STABILIZED" -c:a libopus -b:a 64k -ar 48000 "$OUT_PATH" ;;
esac
echo "iarif_tts_pipeline: V9 Nusantara Pure Studio → $OUT_PATH" >&2
