#!/bin/bash
# E3E divergence baseline runner — forged 2026-09-04 FI-008
# Each agent gets the 5 prompts verbatim, output captured, 10-min timeout each.
D="$(dirname "$0")/results"
P="$(dirname "$0")/prompts.txt"
run() { # name, command...
  local name="$1"; shift
  echo "[$(date +%H:%M:%S)] running $name..."
  timeout 600 "$@" < "$P" > "$D/$name.txt" 2>&1
  echo "[$(date +%H:%M:%S)] $name exit=$? size=$(wc -c < "$D/$name.txt" 2>/dev/null)"
}
run qwen      qwen -p "$(cat $P)"
run kimi      kimi -p "$(cat $P)"
run opencode  opencode run "$(cat $P)"
run codex     codex exec "$(cat $P)"
run claude    claude -p "$(cat $P)" --max-turns 8
run grok      grok -p "$(cat $P)"
run gemini    gemini -p "$(cat $P)"
echo "ALL DONE $(date +%H:%M:%S)"
