# OpenClaw Silence Diagnostics — Trajectory Forensics (2026-08-07)

## The pattern observed

User reported: "Why no OPENCLAW execution start on my AAA telegram group?"

Symptoms:
- Gateway `:18789/health` → `{"ok":true,"status":"live"}`
- `openclaw channels status --probe` → `Telegram default (AGI_ASI_bot): enabled, configured, running, connected, in:1m ago, out:2h ago`
- 3 group messages in AAA group `-1003753855708` between 11:49–12:09 MYT
- Zero outbound replies in the group
- DM outbound continues to work

## False cause (wrong diagnosis)

I first blamed MEMORY.md's HARAM rule:
> "Group reply tanpa `[TO: <recipient>]` dalam multi-agent / multi-human chat"

I reasoned: no `[TO:]` → model obeys HARAM → silent reply. This was wrong. The HARAM rule was dormant; the model never even consulted it.

## True cause (proven via trajectory)

Session for topic 41564 (timestamp `2026-08-07T12:15:14.273Z`) — the agent's actual model output:

```json
"data": {
  "finalStatus": "success",
  "aborted": false,
  "assistantTexts": ["No reply needed — routine market wrap, no action requested."],
  "messagingToolSentTexts": [],
  "didSendViaMessagingTool": false,
  "usage": {"input": 105044, "output": 112, "cacheRead": 26496, "reasoningTokens": 99, "total": 131652}
}
```

The model:
1. Processed the M+ Global Market Wrap (105K input tokens — full MEMORY + bootstrap + system prompt)
2. Judged it a routine briefing with "no action requested"
3. Deliberately emitted zero outbound messages
4. The run completed `success` with no error

## The wrong-cause trap

Three things made the false cause feel plausible:

1. **The `assistantTexts` field is named "assistant" but the literal text is "No reply needed"** — easy to miss when grepping for `"[TO:]"` patterns
2. **MEMORY.md genuinely contains HARAM rules about group replies** — grepping the ruleset returns plausible matches
3. **The `[turn/kernel] no queued reply payloads` line looks like a filter/blocker error** — but it's actually the normal log line when an agent run completes with empty output

## The lesson

**Always read the trajectory file before naming the cause.** The trajectory's `trace.artifacts` event contains:
- `assistantTexts[]` — what the model literally produced
- `messagingToolSentTexts[]` — what the agent actually sent
- `finalStatus` — `success` / `failure` / `aborted`
- `didSendViaMessagingTool` — whether the messaging tool was invoked

These four fields together give you the ground truth. MEMORY.md rules, group policies, and journal lines are context — not proof.

## Reproduction recipe

```bash
# 1. Confirm the symptom
openclaw channels status --probe

# 2. Find group messages with empty replies
journalctl -u openclaw-gateway --no-pager --since "1 hour ago" \
  | grep -E "no queued reply payloads.*group"

# 3. Extract the topic IDs
journalctl -u openclaw-gateway --no-pager --since "1 hour ago" \
  | grep "no queued reply" | grep -oE "topic:[0-9]+" | sort -u

# 4. For each topic, find the session and read the trajectory
TOPIC=41564
SID=$(ls -lat /root/.openclaw/agents/main/sessions/*topic-${TOPIC}*.trajectory.jsonl | head -1 | awk '{print $NF}')
tail -3 "$SID" | python3 -c "
import sys, json
for line in sys.stdin:
    d = json.loads(line.strip())
    if d.get('type') == 'trace.artifacts':
        a = d.get('data',{})
        print('=== trace.artifacts ===')
        print('finalStatus:', a.get('finalStatus'))
        print('assistantTexts:', a.get('assistantTexts'))
        print('messagingToolSentTexts:', a.get('messagingToolSentTexts'))
        print('didSendViaMessagingTool:', a.get('didSendViaMessagingTool'))
"

# 5. The truth is in those four fields
```

## Other signature patterns observed in this session

### Provider tool-cap rejection (different cause, same symptom)

```
[telegram] embedded run agent end: runId=... isError=true model=llama-3.1-8b-instant provider=groq
error=LLM request failed: provider rejected the request schema or tool payload.
rawError=400 'tools' : maximum number of items is 128
```

Different from agent-judgment silence — this shows `isError=true` and a provider error code. Fix: trim tool atlas or switch to a model without the 128-tool cap.

### Memory pressure warning

```
[diagnostics/memory] memory pressure: level=warning reason=rss_threshold rss=1.98 GiB heap=1.71 GiB
```

Outbound latency rises, not silence. Resolution: `systemctl restart openclaw-gateway` (T1, reversible).

### MEMORY.md truncation

```
[agent/embedded] workspace bootstrap file MEMORY.md is 35204 chars (limit 31743); truncating in injected context
```

Agent memory context is incomplete — may affect judgment. Fix: increase `bootstrapMaxChars` or trim MEMORY.md.

## Related: what would have been the wrong fixes

- ❌ Adding `[TO: AGI_ASI_bot]` to user's message — wouldn't have helped, the model decided silence based on content judgment
- ❌ Changing `requireMention: false` — already false, not the issue
- ❌ Switching the bot to DM mode — symptom is in groups, not DMs
- ❌ Restarting openclaw-gateway — service is healthy, no infra fault
- ✅ Reading the trajectory file first to find `assistantTexts` — the actual fix path