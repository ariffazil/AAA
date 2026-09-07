#!/bin/bash
# experience-boot.sh — Generate experience context block
# Output: /tmp/experience_boot_context.md (pre-injected into boot)
set -euo pipefail

TRACE_LOG="/root/.local/share/arifos/world-model/experience_traces.jsonl"
OUTPUT="/tmp/experience_boot_context.md"

if [ ! -f "$TRACE_LOG" ]; then
  echo "<!-- No experience traces available -->" > "$OUTPUT"
  exit 0
fi

python3 -c "
import json

with open('$TRACE_LOG') as f:
    traces = [json.loads(l) for l in f if l.strip()]

if not traces:
    with open('$OUTPUT', 'w') as f:
        f.write('<!-- No experience traces available -->')
    exit()

ranked = sorted(traces, key=lambda t: t.get('experience_delta',{}).get('capability_change',0) or 0, reverse=True)[:3]
total_cap = sum((t.get('experience_delta',{}).get('capability_change',0) or 0) for t in ranked)

lines = ['# EXPERIENCE (auto-injected — apply before planning)']
for i, t in enumerate(ranked, 1):
    fb = t.get('feedback', {})
    cap = (t.get('experience_delta',{}).get('capability_change',0) or 0)
    scar = t.get('experience_delta',{}).get('new_scar')
    self_fb = (fb.get('self') or '')[:120]
    if self_fb:
        lines.append(f'## Lesson {i}: {t[\"action\"][\"tool\"]} (cap={cap:+.2f})')
        lines.append(f'  {self_fb}')
        if scar:
            lines.append(f'  scar: {scar}')
        lines.append('')

lines.append(f'Applied: {len(traces)} traces surfaced, top-3 = {total_cap:+.2f} cap')
lines.append('BEFORE planning any task, check if a lesson above applies.')

with open('$OUTPUT', 'w') as f:
    f.write('\n'.join(lines) + '\n')
"

