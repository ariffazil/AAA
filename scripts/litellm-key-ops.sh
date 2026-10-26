#!/usr/bin/env bash
# litellm-key-ops.sh — Agentic key & health operations for fed-litellm (KVM4)
#
# Charter: sovereign key custody, never echoed in chat, receipts, or VAULT999.
# Reads mode-600 env files under /root/.secrets/. Never writes the key value
# to stdout. Never pastes in command line. Never logs the key.
#
# Usage:
#   litellm-key-ops.sh diagnose           # health + key + env-file + upstream latency
#   litellm-key-ops.sh test               # 3-way test: chat ping, models, health
#   litellm-key-ops.sh ping <model> <msg> [max_tokens]
#   litellm-key-ops.sh list-models [filter]
#   litellm-key-ops.sh list-upstreams     # which upstream providers are wired
#   litellm-key-ops.sh rotate-master      # placeholder; requires sovereign F13
#   litellm-key-ops.sh help
#
# Why master-key-as-test-key (not a virtual key):
#   fed-litellm on KVM4 does not have DATABASE_URL wired. LiteLLM's virtual
#   key endpoints (mint/list/revoke) require Postgres. Wiring one is a T3
#   change (new port, new service) — sovereign scope. Until then, this script
#   wraps the master key in agentic discipline: the script reads the env file
#   (mode 600, root-only), uses the key, never echoes it. The user never has
#   to remember, type, or paste the value. The upgrade path is documented in
#   /root/AAA/governance/litellm-test-key-runbook.md §5.
#
# Runbook: /root/AAA/governance/litellm-test-key-runbook.md
# T1 doc spec: same runbook
# DITEMPA BUKAN DIBERI ⚒️

set -euo pipefail

MASTER_ENV="/root/.secrets/litellm-fed.env"
SOVEREIGN_ENV="/root/.secrets/litellm-arif-test.env"
DEFAULT_BASE_URL="http://100.64.0.5:4000"
KEY_HINT_LENGTH=4   # how many chars to show in status output (e.g. "sk-l...74ed")

# ---- Charter & safety -------------------------------------------------------
charter() {
  cat <<'CHARTER_END'
  - Sovereign key never echoed in chat / receipts / VAULT999
  - Script reads env (mode 600, root-only) and uses the value internally
  - Status output shows only KEY HINT (first+last KEY_HINT_LENGTH chars)
  - No --print-key flag. No environment export. No `echo $KEY` accident.
CHARTER_END
}

# ---- Helpers ----------------------------------------------------------------
say()  { printf '%s\n' "$*"; }
hr()   { printf '%s\n' "------------------------------------------------------------"; }
err()  { printf 'ERROR: %s\n' "$*" >&2; }
ok()   { printf '  ✓ %s\n' "$*"; }

# key_hint <full-key>  →  "ab...wxyz"  (never the full value)
key_hint() {
  local k="$1"
  local n=${#k}
  if (( n < KEY_HINT_LENGTH * 2 + 3 )); then
    printf '...%d-char-key...' "$n"
  else
    printf '%s...%s' "${k:0:$KEY_HINT_LENGTH}" "${k: -$KEY_HINT_LENGTH}"
  fi
}

require_master() {
  if [[ ! -r "$MASTER_ENV" ]]; then
    err "master env not readable: $MASTER_ENV"
    err "F13 boundary: this file holds the LiteLLM master key. Sovereign decides read access."
    return 1
  fi
  # shellcheck disable=SC1090
  source "$MASTER_ENV"
  if [[ -z "${LITELLM_MASTER_KEY:-}" ]]; then
    err "LITELLM_MASTER_KEY not present in $MASTER_ENV"
    return 1
  fi
}

base_url() {
  if [[ -n "${LITELLM_BASE_URL:-}" ]]; then printf '%s' "$LITELLM_BASE_URL"
  else printf '%s' "$DEFAULT_BASE_URL"
  fi
}

# ---- Commands ---------------------------------------------------------------
cmd_diagnose() {
  hr
  say "fed-litellm diagnostic — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  hr
  say "1. master env file"
  if [[ -f "$MASTER_ENV" ]]; then
    say "   path : $MASTER_ENV"
    say "   mode : $(stat -c %a "$MASTER_ENV")"
    say "   owner: $(stat -c %U:%G "$MASTER_ENV")"
  else
    err "   MISSING"
    return 1
  fi
  require_master
  ok "master key loaded (hint: $(key_hint "$LITELLM_MASTER_KEY"))"

  say ""
  say "2. sovereign test env (if minted virtual key — currently unused, see runbook §2)"
  if [[ -f "$SOVEREIGN_ENV" ]]; then
    say "   path : $SOVEREIGN_ENV"
    say "   mode : $(stat -c %a "$SOVEREIGN_ENV")"
    say "   alias: $(grep -E '^LITELLM_KEY_ALIAS=' "$SOVEREIGN_ENV" | cut -d= -f2 || echo '?')"
    say "   minted: $(grep -E '^LITELLM_MINTED_AT=' "$SOVEREIGN_ENV" | cut -d= -f2 || echo '?')"
  else
    say "   not present (no virtual key minted — DB-gated; using master via this script)"
  fi

  say ""
  say "3. fed-litellm reachability"
  local base; base="$(base_url)"
  local t0; t0=$(date +%s%N)
  local code
  code=$(curl -sS -o /dev/null -w "%{http_code}" --max-time 5 "$base/health/liveliness" || echo "000")
  local t1; t1=$(date +%s%N)
  local ms=$(( (t1 - t0) / 1000000 ))
  say "   $base/health/liveliness → HTTP $code (${ms}ms)"

  if [[ "$code" != "200" ]]; then
    err "fed-litellm is not 200. Check: systemctl status fed-litellm.service"
    err "T2: sudo systemctl restart fed-litellm.service (if 3+ consecutive failures)"
    return 1
  fi

  say ""
  say "4. auth check (master)"
  local auth_check
  auth_check=$(curl -sS -o /dev/null -w "%{http_code}" --max-time 5 \
    -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
    "$base/v1/models" || echo "000")
  say "   $base/v1/models (master) → HTTP $auth_check"
  if [[ "$auth_check" != "200" ]]; then
    err "master key is rejected. Did the fed.env get rotated? See runbook §4.2"
    return 1
  fi
  ok "all green"
}

cmd_test() {
  hr
  say "fed-litellm 3-way test — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  hr
  require_master
  local base; base="$(base_url)"

  say ""
  say "1. /health/liveliness (no auth)"
  local health
  health=$(curl -sS --max-time 4 "$base/health/liveliness" | jq -c . 2>/dev/null || echo "PARSE_FAIL")
  say "   $health"
  [[ "$health" == "PARSE_FAIL" ]] && { err "health endpoint not parseable"; return 1; }

  say ""
  say "2. /v1/models (master auth)"
  local models_count
  models_count=$(curl -sS --max-time 5 \
    -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
    "$base/v1/models" | jq '.data | length' 2>/dev/null || echo 0)
  say "   models visible: $models_count"
  (( models_count > 0 )) || { err "no models visible — config broken?"; return 1; }
  ok "models endpoint OK"

  say ""
  say "3. /v1/chat/completions (1-token ping, cheapest available model)"
  # Pick the cheapest-looking model from the list to keep cost zero
  local cheap_model
  cheap_model=$(curl -sS --max-time 5 \
    -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
    "$base/v1/models" | jq -r '.data[].id' 2>/dev/null \
    | grep -iE "(nano|mini|haiku|flash|cheap|free|test)" | head -1)
  if [[ -z "$cheap_model" ]]; then
    cheap_model=$(curl -sS --max-time 5 \
      -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
      "$base/v1/models" | jq -r '.data[0].id' 2>/dev/null)
  fi
  say "   using model: $cheap_model"
  local t0; t0=$(date +%s%N)
  local chat
  chat=$(curl -sS --max-time 30 -X POST "$base/v1/chat/completions" \
    -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\": \"$cheap_model\", \"messages\": [{\"role\": \"user\", \"content\": \"ping\"}], \"max_tokens\": 3}" \
    2>&1)
  local t1; t1=$(date +%s%N)
  local ms=$(( (t1 - t0) / 1000000 ))
  local content; content=$(echo "$chat" | jq -r '.choices[0].message.content // "NO_CONTENT"' 2>/dev/null)
  local usage; usage=$(echo "$chat" | jq -c '.usage // {}' 2>/dev/null)
  say "   ping latency: ${ms}ms"
  say "   response content: $content"
  say "   usage: $usage"
  if [[ "$content" == "NO_CONTENT" ]]; then
    err "chat completion returned no content. First 500 chars of raw response:"
    say "${chat:0:500}"
    return 1
  fi
  ok "3-way test passed"
}

cmd_ping() {
  local model="${1:-}"
  local msg="${2:-ping}"
  local max_tokens="${3:-16}"
  if [[ -z "$model" ]]; then
    err "Usage: $0 ping <model> <message> [max_tokens]"
    err "  see '$0 list-models' for available models"
    return 2
  fi
  require_master
  local base; base="$(base_url)"
  local resp
  resp=$(curl -sS --max-time 60 -X POST "$base/v1/chat/completions" \
    -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\": \"$model\", \"messages\": [{\"role\": \"user\", \"content\": \"$msg\"}], \"max_tokens\": $max_tokens}" \
    2>&1)
  local content; content=$(echo "$resp" | jq -r '.choices[0].message.content // "NO_CONTENT"' 2>/dev/null)
  local usage; usage=$(echo "$resp" | jq -c '.usage // {}' 2>/dev/null)
  say "model:    $model"
  say "message:  $msg"
  say "response: $content"
  say "usage:    $usage"
  if [[ "$content" == "NO_CONTENT" ]]; then
    err "raw response (first 500):"
    say "${resp:0:500}"
    return 1
  fi
}

cmd_list_models() {
  local filter="${1:-}"
  require_master
  local base; base="$(base_url)"
  if [[ -n "$filter" ]]; then
    curl -sS --max-time 5 \
      -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
      "$base/v1/models" | jq -r --arg f "$filter" '.data[].id | select(test($f; "i"))' 2>/dev/null
  else
    curl -sS --max-time 5 \
      -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
      "$base/v1/models" | jq -r '.data[].id' 2>/dev/null
  fi
}

cmd_list_upstreams() {
  hr
  say "Upstream providers wired in /root/.secrets/litellm-fed.env"
  hr
  require_master
  # Show only var NAMES that look like upstream keys (no values)
  grep -oE '^[A-Z_]+_(API_KEY|KEY|TOKEN)=' "$MASTER_ENV" 2>/dev/null \
    | sed 's/=$//' \
    | sort -u \
    | while read -r var; do
        local v="${!var:-}"
        say "  $var = $(key_hint "$v")"
      done
  say ""
  say "Total upstream keys: $(grep -cE '^[A-Z_]+_(API_KEY|KEY|TOKEN)=' "$MASTER_ENV" 2>/dev/null || echo 0)"
}

cmd_rotate_master() {
  hr
  say "rotate-master — F13-class (irreversible, sovereign authority)"
  hr
  err "This is a T3 operation. It mutates the production master key."
  err "It cannot be done by an agent unilaterally. The sovereign must:"
  err "  1. Mint a new master key from the upstream provider dashboards"
  err "  2. Update /root/.secrets/litellm-fed.env LITELLM_MASTER_KEY (mode 600)"
  err "  3. Run: sudo systemctl restart fed-litellm.service"
  err "  4. Run: $0 test   (verify)"
  err "  5. Append receipt to VAULT999 with old + new key hint only (never full value)"
  return 2
}

cmd_help() {
  cat <<EOF
litellm-key-ops.sh — agentic key & health for fed-litellm (KVM4 / 100.64.0.5:4000)

  diagnose              health, env-file state, key auth, latency
  test                  3-way: health + models + 1-token chat ping
  ping <model> <msg> [max_tokens]   ad-hoc LLM call (use list-models first)
  list-models [filter]  list all visible models (regex filter optional)
  list-upstreams        list upstream provider keys (hint only, never full)
  rotate-master         F3-class placeholder; sovereign executes manually

  help                  this help

ENV:
  $MASTER_ENV     (mode 600, root-only) provides LITELLM_MASTER_KEY

CHARTER:
$(charter | sed 's/^/  /')

RUNBOOK:
  /root/AAA/governance/litellm-test-key-runbook.md
EOF
}

# ---- Entry ------------------------------------------------------------------
cmd="${1:-help}"
shift || true

case "$cmd" in
  diagnose)        cmd_diagnose ;;
  test)            cmd_test ;;
  ping)            cmd_ping "$@" ;;
  list-models)     cmd_list_models "$@" ;;
  list-upstreams)  cmd_list_upstreams ;;
  rotate-master)   cmd_rotate_master ;;
  help|--help|-h)  cmd_help ;;
  *)
    err "unknown subcommand: $cmd"
    cmd_help
    exit 2
    ;;
esac
