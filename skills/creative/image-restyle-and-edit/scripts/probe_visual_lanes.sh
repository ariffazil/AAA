#!/usr/bin/env bash
# probe_visual_lanes.sh — discover which DashScope key class actually serves
# the multimodal-generation visual endpoint right now.
#
# Run from anywhere. Reports key prefix + HTTP status per key, never the value.
# Exit 0 means at least one sk-ws- (PAYG) key returned 200 or a quota error
# (which means the lane is reachable, just out of budget).
# Exit 1 means no usable visual lane was found in the loaded env files.

set -u
# Disable strict unbound-variable check just for the source step; one env file
# references $QWEN_API_KEY which is itself set by the same file, but `source`
# evaluates the assignment left-to-right and a stray reference earlier in
# evaluation can blow up. Re-enable strict mode after sourcing.
set +u
PAY_URL="https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
TP_URL="https://token-plan.maas.qwencloudapi.com/api/v1/services/aigc/multimodal-generation/generation"
PAY_BODY='{"model":"qwen-image-edit","input":{"messages":[{"role":"user","content":[{"text":"x"}]}]},"parameters":{"n":1,"size":"1024*1024"}}'

FOUND_USABLE=0
printf "%-32s %-8s %-5s %-8s\n" "ENV_VAR" "PREFIX" "PAYG" "TP"
printf -- "---------------------------------------- -------- ----- --------\n"

# Source all known env files; later overrides earlier (last-write-wins, like real env)
for f in /root/.secrets/qwen.env /root/.secrets/kunci-mas.env /root/.secrets/kunci-root.env; do
  [ -f "$f" ] || continue
  set -a
  # shellcheck disable=SC1090
  source "$f"
  set +a
done

# Iterate candidate variable names; collect unique values
declare -A SEEN
for V in DASHSCOPE_API_KEY QWEN_PAYG_API_KEY QWEN_HERMES_API_KEY \
         QWEN_TEAM_OWNER_API_KEY QWEN_INDIVIDUAL_API_KEY QWEN_OPENCODE_API_KEY \
         QWEN_ARIFOS_API_KEY; do
  K="${!V:-}"
  [ -z "$K" ] && continue
  # Skip if same value already probed
  [ -n "${SEEN[$K]:-}" ] && continue
  SEEN[$K]=1

  P="${K:0:5}"
  PAY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$PAY_URL" \
    -H "Authorization: Bearer $K" \
    -H "Content-Type: application/json" \
    -d "$PAY_BODY" 2>/dev/null)
  TP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$TP_URL" \
    -H "Authorization: Bearer $K" \
    -H "Content-Type: application/json" \
    -d "$PAY_BODY" 2>/dev/null)

  printf "%-32s %-8s %-5s %-8s\n" "$V" "$P" "$PAY_STATUS" "$TP_STATUS"

  # PAYG: 200/403/429 = route open under this key (different budget/quota states)
  # TP:   200 = route open; 404 = route open but model name not in this seat's
  #        available list (try a model from /compatible-mode/v1/models instead);
  #        401 = key not authorized for this base at all.
  case "$PAY_STATUS" in
    200|403|429) FOUND_USABLE=1 ;;
  esac
  case "$TP_STATUS" in
    200|404) FOUND_USABLE=1 ;;
  esac
done

echo ""
echo "Result:"
if [ "$FOUND_USABLE" = "1" ]; then
  echo "  ✅ At least one sk-* key reaches a visual lane."
  echo "  PAYG col 200  → route open, body status tells you about budget/quota"
  echo "  PAYG col 403  → free tier dry, top up via console"
  echo "  PAYG col 429  → account in cooldown, wait"
  echo "  TP col 200    → Token Plan visual lane enabled, this is the lane to use"
  echo "  TP col 404    → Token Plan route open, but 'qwen-image-edit' not in seat's"
  echo "                  available models; try a model from /compatible-mode/v1/models"
  echo "  TP col 401    → Token Plan does not cover image endpoints for this seat"
  echo "  PAYG 401 + TP 401 → wrong key class entirely, regenerate as the right prefix"
else
  echo "  ❌ No usable visual lane. All keys return 401 on both bases."
  echo "  Action: generate the right key class (sk-ws- for PAYG, sk-sp- for Token Plan)"
  echo "          or enable image endpoints on the existing Token Plan seat."
fi
exit $((1 - FOUND_USABLE))