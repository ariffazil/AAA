# litellm-upstream-probe.sh — runnable copy of the litellm-proxy-triage SKILL.md §2
# disambiguation probe. Purpose: decide UPSTREAM vs PROXY before restarting anything.
#
# Usage:  bash scripts/litellm-upstream-probe.sh
# Requires: /root/.secrets/kunci-root.env (sourced automatically if present)
#
# Read the result (§2):
#   all 200                -> upstream fine  -> restart litellm-federation via systemd (proxy stale)
#   mix 200/timeout/401    -> the failing ones are the real problem; fix keys or wait for quota
#   all failing            -> provider outage OR VPS IPv4 issue (then: curl -4 -sv --max-time 5 https://1.1.1.1)

[ -f /root/.secrets/kunci-root.env ] && . /root/.secrets/kunci-root.env

for spec in \
  "MINIMAX_API_KEY:https://api.minimax.io/v1/chat/completions:MiniMax-M3" \
  "DASHSCOPE_API_KEY:https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions:qwen3.7-flash-2026-07-15" \
  "QWEN_INDIVIDUAL_API_KEY:https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions:qwen3.7-max" \
  "GEMINI_API_KEY:https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent:GEMINI"; do
  KEY="${spec%%:*}"; rest="${spec#*:}"
  URL="${rest%%:*}"; MODEL="${rest#*:}"
  V="${!KEY}"
  [ -z "$V" ] && echo "$KEY MISSING" && continue
  if [ "$MODEL" = "GEMINI" ]; then
    code=$(curl -4 -s -o /dev/null -w "%{http_code}" --max-time 15 \
      "${URL}?key=$V" -H "Content-Type: application/json" \
      -d '{"contents":[{"parts":[{"text":"reply PONG"}]}],"generationConfig":{"maxOutputTokens":10}}')
  else
    code=$(curl -4 -s -o /dev/null -w "%{http_code}" --max-time 15 \
      "$URL" -H "Authorization: Bearer $V" -H "Content-Type: application/json" \
      -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"reply PONG\"}],\"max_tokens\":10}")
  fi
  echo "$KEY ($MODEL) http=$code"
done
