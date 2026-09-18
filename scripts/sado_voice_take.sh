#!/usr/bin/env bash
# sado_voice_take.sh — render one abang-sado persona voice take, then gate it.
#
#   usage: sado_voice_take.sh <text-file> <out.mp3> [speed]
#
# The voice id is read from the registry's lane_precedence block — never hardcoded,
# never picked by name symmetry or file recency. A non-LIVE id refuses.
# mmx carries its own credentials (~/.mmx/config.json); no vault sourcing needed,
# which also keeps this script free of any T3-gated path.
set -o pipefail
export PATH=$PATH:/root/.npm-global/bin

TXT="${1:?usage: sado_voice_take.sh <text-file> <out.mp3> [speed]}"
OUT="${2:?usage: sado_voice_take.sh <text-file> <out.mp3> [speed]}"
SPEED="${3:-0.92}"

REG=/root/AAA/audio/voice-registry.json
LANE_KEY="abang-sado persona register"

VOICE=$(python3 - "$REG" "$LANE_KEY" <<'PY'
import json, sys
reg = json.load(open(sys.argv[1]))
for k, v in reg.get("lane_precedence", {}).items():
    if sys.argv[2] in k:
        print(v["precedent_voice"]); break
else:
    raise SystemExit("REFUSE: no lane_precedence entry for this register")
PY
) || exit 2

STATUS=$(python3 - "$REG" "$VOICE" <<'PY'
import json, sys
reg = json.load(open(sys.argv[1]))
print((reg.get("voices", {}).get(sys.argv[2]) or {}).get("status", "UNKNOWN"))
PY
)
[ "$STATUS" = "LIVE" ] || { echo "REFUSE: $VOICE is $STATUS"; exit 3; }

mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd \
  --voice "$VOICE" --speed "$SPEED" --text-file "$TXT" --out "$OUT" >/dev/null || exit 4

GATE=/root/.hermes/skills/domains/general/workshop/creative-design/abang-sado-creative-lane/scripts/verify_take.py
python3 "$GATE" "$OUT" --text "$TXT"
echo "voice=$VOICE  speed=$SPEED  status=$STATUS  out=$OUT"
