#!/usr/bin/env bash
# tts_lane_status.sh — which voice lane is LIVE right now, and why
#
# Forged 2026-09-18 (KVM8). Purpose: stop burning the rented pool by accident.
#
# WHY THIS EXISTS — measured facts, not doctrine:
#   * MiniMax Token Plan exposes ONE bucket called `general` that serves BOTH
#     image_generation AND t2a_v2 (speech). Probed live: both endpoints return
#     the same 2056 at the same moment.
#   * `general` is capped TWICE: a 4-hour interval cap and a 7-day cap.
#     The interval cap is what silences a session mid-work while weekly
#     headroom still remains.
#   * `video` is a SEPARATE bucket (24h interval + weekly).
#   * Piper renders BM locally on CPU with zero network and zero quota.
#
# USAGE
#   bash tts_lane_status.sh          # human line
#   bash tts_lane_status.sh --json   # machine line
#
# EXIT: 0 = Tier 1 (rented) available · 3 = Tier 1 blocked, sovereign lane active

set -o pipefail

JSON=0
[ "$1" = "--json" ] && JSON=1

MMX="${IARIF_MMX_BIN:-$(command -v mmx || echo /root/.npm-global/bin/mmx)}"
PIPER_BIN="${IARIF_PIPER_BIN:-/usr/local/bin/piper}"
PIPER_MODEL="${IARIF_PIPER_MODEL:-/root/forge_work/piper-sovereign/id_voice.onnx}"

Q=""
if [ -x "$MMX" ]; then
  Q="$(timeout 25 "$MMX" quota show --base-url https://api.minimax.io 2>/dev/null)"
fi

read -r GEN_ISTAT GEN_WEEK GEN_IREM GEN_WREM VID_ISTAT VID_WEEK <<<"$(
python3 - "$Q" <<'PY'
import sys, json
raw = sys.argv[1] if len(sys.argv) > 1 else ""
out = ["?", "?", "?", "?", "?", "?"]
try:
    d = json.loads(raw)
    for m in d.get("model_remains", []):
        n = m.get("model_name")
        if n == "general":
            out[0] = str(m.get("current_interval_status", "?"))
            out[1] = str(m.get("current_weekly_remaining_percent", "?"))
            out[2] = str(m.get("current_interval_remaining_percent", "?"))
            out[3] = str(m.get("current_weekly_remaining_percent", "?"))
        if n == "video":
            out[4] = str(m.get("current_interval_status", "?"))
            out[5] = str(m.get("current_weekly_remaining_percent", "?"))
except Exception:
    pass
print(" ".join(out))
PY
)"

# general interval: 1 = open, 2 = exhausted
if [ "$GEN_ISTAT" = "1" ]; then
  LANE="minimax (Tier 1, rented)"
  RC=0
else
  if [ -x "$PIPER_BIN" ] && [ -s "$PIPER_MODEL" ]; then
    LANE="piper (Sovereign / offline / zero-quota)"
    RC=3
  else
    LANE="NONE — check piper + model path"
    RC=4
  fi
fi

if [ "$JSON" = "1" ]; then
  printf '{"general_interval_status":"%s","general_interval_rem_pct":"%s","general_weekly_rem_pct":"%s","video_interval_status":"%s","video_weekly_rem_pct":"%s","lane":"%s"}\n' \
    "$GEN_ISTAT" "$GEN_IREM" "$GEN_WEEK" "$VID_ISTAT" "$VID_WEEK" "$LANE"
else
  echo "LANE NOW: $LANE"
  echo "  general (voice+image shared): interval=${GEN_IREM}%  weekly=${GEN_WEEK}%  [status ${GEN_ISTAT}]"
  echo "  video   (separate bucket)   : interval-status=${VID_ISTAT}  weekly=${VID_WEEK}%"
  [ "$RC" != "0" ] && echo "  → floor the rented pool is shut. Deliver on the sovereign lane and NAME it."
fi
exit $RC
