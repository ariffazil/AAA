#!/usr/bin/env bash
# openclaw_silence_probe.sh — extract ground-truth from an OpenClaw session trajectory
# when the journal shows "no queued reply payloads" but the cause is unclear.
#
# Usage: bash scripts/openclaw_silence_probe.sh <topic_id>
#        bash scripts/openclaw_silence_probe.sh 41564
#
# Reads the last `trace.artifacts` event from the most recent session matching
# *topic-<id>*.trajectory.jsonl and prints the four fields that reveal the
# real cause: assistantTexts, messagingToolSentTexts, didSendViaMessagingTool,
# finalStatus.

set -euo pipefail

TOPIC="${1:-}"
if [[ -z "$TOPIC" ]]; then
  echo "Usage: $0 <telegram_topic_id>" >&2
  echo "  e.g. $0 41564" >&2
  exit 2
fi

SESSION_DIR="/root/.openclaw/agents/main/sessions"

# Find the most recent session for this topic
SESSION_FILE=$(ls -lat "${SESSION_DIR}"/*topic-${TOPIC}*.trajectory.jsonl 2>/dev/null | head -1 | awk '{print $NF}')
if [[ -z "$SESSION_FILE" || ! -f "$SESSION_FILE" ]]; then
  echo "ERROR: no trajectory file found for topic ${TOPIC}" >&2
  echo "  expected: ${SESSION_DIR}/*topic-${TOPIC}*.trajectory.jsonl" >&2
  exit 3
fi

echo "=== Session file: $SESSION_FILE ==="
echo

# Extract trace.artifacts from the last few lines
tail -5 "$SESSION_FILE" | python3 -c '
import sys, json

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
    except json.JSONDecodeError:
        continue
    if d.get("type") != "trace.artifacts":
        continue
    a = d.get("data", {})
    print("=== trace.artifacts ===")
    print(f"finalStatus:              {a.get(\"finalStatus\")}")
    print(f"aborted:                  {a.get(\"aborted\")}")
    print(f"timedOut:                 {a.get(\"timedOut\")}")
    print(f"didSendViaMessagingTool:  {a.get(\"didSendViaMessagingTool\")}")
    print()
    print(f"assistantTexts:           {a.get(\"assistantTexts\")}")
    print(f"messagingToolSentTexts:   {a.get(\"messagingToolSentTexts\")}")
    print(f"messagingToolSentTargets: {a.get(\"messagingToolSentTargets\")}")
    print()
    usage = a.get("usage", {})
    if usage:
        print(f"usage.input:    {usage.get(\"input\")}")
        print(f"usage.output:   {usage.get(\"output\")}")
        print(f"usage.cacheRead: {usage.get(\"cacheRead\")}")
    sys.exit(0)

print("ERROR: no trace.artifacts event found in last 5 lines")
sys.exit(4)
'

echo
echo "=== Cause verdict ==="
python3 -c "
import json
with open('$SESSION_FILE') as f:
    for line in f:
        d = json.loads(line.strip())
        if d.get('type') != 'trace.artifacts':
            continue
        a = d.get('data', {})
        texts = a.get('assistantTexts') or []
        sent = a.get('messagingToolSentTexts') or []
        if not texts and a.get('finalStatus') == 'success':
            print('UNKNOWN — success but no assistantTexts (very rare)')
        elif texts and not sent and a.get('didSendViaMessagingTool') is False:
            if any('no reply needed' in t.lower() or 'no action' in t.lower() for t in texts):
                print('AGENT-JUDGMENT SILENCE — model chose not to reply')
                print('  fix: tighten agent prompt to require responses in this group')
            else:
                print('AGENT PRODUCED TEXT BUT DID NOT SEND — check messaging tool wiring')
        elif a.get('finalStatus') in ('failure', 'aborted'):
            print('RUN FAILED — check journal for provider rejection')
        else:
            print('See trace.artifacts fields above for details')
        break
"