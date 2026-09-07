#!/bin/bash
# experience-surface-gen.sh — Regenerate the experience surface from traces
# Called after /seal or periodically to keep experience_surface.md current
# Input: experience_traces.jsonl
# Output: /root/AAA/canon/experience_surface.md

set -euo pipefail

TRACE_LOG="/root/.local/share/arifos/world-model/experience_traces.jsonl"
OUTPUT="/root/AAA/canon/experience_surface.md"
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

if [ ! -f "$TRACE_LOG" ]; then
  echo "No experience traces found at $TRACE_LOG" >&2
  exit 1
fi

python3 -c "
import json, sys

with open('$TRACE_LOG') as f:
    traces = [json.loads(l) for l in f if l.strip()]

ranked = sorted(traces, key=lambda t: t.get('experience_delta',{}).get('capability_change',0) or 0, reverse=True)[:3]

lines = []
lines.append('# EXPERIENCE SURFACE — auto-generated from experience_traces.jsonl')
lines.append('# Top-3 traces by capability_change. Loaded at /init for context injection.')
lines.append('# This file IS the experience → capability pipeline. Do not edit manually.')
lines.append(f'# Generated: $NOW')
lines.append(f'# Total traces: {len(traces)}')
lines.append('')

for i, t in enumerate(ranked, 1):
    d = t.get('experience_delta', {})
    fb = t.get('feedback', {})
    cap = d.get('capability_change', 0) or 0
    scar = d.get('new_scar') or 'none'
    self_fb = (fb.get('self') or 'none')[:150]
    const_fb = (fb.get('constitutional') or 'none')[:100]
    lines.append(f'## {i}. {t[\"action\"][\"tool\"]} ({t[\"agent_id\"]})  cap={cap:+.2f}')
    lines.append(f'- trace: {t[\"trace_id\"]}')
    lines.append(f'- lesson: {self_fb}')
    lines.append(f'- constitutional: {const_fb}')
    if scar != 'none':
        lines.append(f'- scar: {scar}')
    lines.append('')

lines.append('## PATTERN')
lines.append(f'- {len(traces)} total traces, top-3 surface = {sum((t.get(\"experience_delta\",{}).get(\"capability_change\",0) or 0) for t in ranked):+.2f} cap')
lines.append('- 0 skills auto-created from experience')
lines.append('- Asymmetric: failure → scar works. success → skill does NOT.')
lines.append('- BREAKPOINT: capability_change is write-only. No consumer exists.')

with open('$OUTPUT', 'w') as f:
    f.write('\n'.join(lines) + '\n')

print(f'Experience surface regenerated: {len(traces)} traces, top-3 surface written to $OUTPUT')
"
