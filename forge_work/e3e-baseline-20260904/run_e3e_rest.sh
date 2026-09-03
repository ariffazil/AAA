#!/bin/bash
D="/root/AAA/forge_work/e3e-baseline-20260904/results"
P="/root/AAA/forge_work/e3e-baseline-20260904/prompts.txt"
run() { local name="$1"; shift
  echo "[$(date +%H:%M:%S)] running $name..."
  timeout 600 "$@" < "$P" > "$D/$name.txt" 2>&1
  echo "[$(date +%H:%M:%S)] $name exit=$? size=$(wc -c < "$D/$name.txt" 2>/dev/null)"
}
run opencode  opencode run "$(cat $P)"
run codex     codex exec "$(cat $P)"
run claude    claude -p "$(cat $P)" --max-turns 8
run grok      grok -p "$(cat $P)"
run gemini    gemini -p "$(cat $P)"
echo "REST DONE $(date +%H:%M:%S)"
/root/AAA/scripts/e3e_skill_mesh.sh tally "$D" > "$D/../TALLY.txt" 2>&1
echo "TALLY WRITTEN"
