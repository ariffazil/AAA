# Gemini Multimodal Transport Audit — Worked Example

**Session:** 2026-08-26, Gemini Zen Harmonization & Collapse
**FQ status:** EMPTY (no SOUL sealed for the audit)
**Provenance:** 3-report series claiming "multimodal transport harmonized / complete"

## Scenario

Three consecutive deployment reports (Zen Harmonization, Execution Complete, Domain Collapse)
all claimed "all Gemini multimodal capabilities fully discoverable and executable by Hermes"
with a master dispatch table covering Image, Video, Music, TTS, Live Audio, and Reasoning.

## The Key Distinction

Hermes speaks `openai_chat` transport only — that means
`POST /v1beta/openai/chat/completions`. Gemini has FOUR transport surfaces:

| Transport | What it does | Hermes speaks it? |
|-----------|-------------|-------------------|
| `openai_chat` (chat completions) | LLM reasoning, vision-in, code gen | YES |
| `Interactions API` (client.interactions.create) | Stateful multi-turn video/music/image gen | NO |
| `generate_videos` (LRO polling) | Async cinematic video with native audio | NO |
| `Live API` (WebSocket) | Sub-second bidirectional voice A2A | NO |

A model "discovered" in config.yaml does NOT equal "reachable" via Hermes's runtime transport.

## Probe Recipe

### Layer 1: Config (fast, deterministic)

```bash
# 1a. Config mtime — was the config actually modified?
stat -c '%y %n' /root/.hermes/config.yaml

# 1b. Model count — how many Gemini models remain after claimed prune?
python3 -c "
import yaml
d = yaml.safe_load(open('/root/.hermes/config.yaml'))
gemini = d['providers']['gemini']
print(f'Gemini models: {len(gemini[\"models\"])}')
for m in gemini['models']:
    print(f'  {m[\"id\"]}')
"

# 1c. Confirmed removed — are broken models gone?
grep -c 'gemini-omni-flash\|veo-3.1\|lyria-3' /root/.hermes/config.yaml
# Must return 0 after prune. Non-chat models confirmed removed.
```

### Layer 2: API-side model existence (proves Google knows the model)

```bash
source /root/.hermes/.env
curl -s "https://generativelanguage.googleapis.com/v1beta/openai/models" \
  -H "Authorization: Bearer $GEMINI_API_KEY" | python3 -c "
import sys, json
d = json.load(sys.stdin)
ids = [m['id'] for m in d.get('data', [])]
# Check the claimed non-chat models
for name in ['lyria-3-pro-preview', 'veo-3.1-generate-preview',
             'gemini-omni-flash-preview', 'gemini-3.1-flash-tts-preview',
             'gemini-3.1-flash-live-preview', 'gemini-3.5-live-translate-preview']:
    found = any(name in i for i in ids)
    print(f'  {\"YES\" if found else \"NO\"} {name}')
"
```

All 6 non-chat models return YES — they exist in Google's API catalog.
The problem is NOT "model doesn't exist." The problem is "wrong transport."

### Layer 3: Transport probe (the slow, decisive layer)

```bash
source /root/.hermes/.env

# CONFIRMED WORKING (chat-completion compatible):
curl -s "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions" \
  -H "Authorization: Bearer $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gemini-3.1-flash-image","messages":[{"role":"user","content":"ping"}],"max_tokens":10}'
# -> {"choices":[{"message":{"content":"pong"},...}]}

# BROKEN (not openai_chat compatible):
curl -s "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions" \
  -H "Authorization: Bearer $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gemini-omni-flash-preview","messages":[{"role":"user","content":"ping"}],"max_tokens":10}'
# -> "This model only supports Interactions API" (400)

curl -s ... -d '{"model":"veo-3.1-generate-preview",...}'
# -> "models not found for API version v1main" (404)

curl -s ... -d '{"model":"lyria-3-pro-preview",...}'
# -> "Internal error encountered" (500)

curl -s ... -d '{"model":"gemini-3.1-flash-tts-preview",...}'
# -> "Request contains an invalid argument" (400)
```

## Error Signature Table

| Error message | Meaning | Transport required |
|---------------|---------|-------------------|
| "This model only supports Interactions API" | Model exists but rejects chat completions | `Interactions API` (python SDK) |
| "models not found for API version v1main" | Not on openai_compat endpoint; use native | `generate_videos` or native SDK |
| "Internal error encountered" | Not a chat model; wrong endpoint shape | `Interactions API` |
| "Request contains an invalid argument" | TTS - not a text-in/text-out chat model | `Interactions API` |

## Classification Verdict

```
LAYER 1 (config):      OK Config pruned correctly (10 -> 8)
LAYER 2 (API catalog): OK All 19 models exist in Google's catalog
LAYER 3 (transport):   FAIL  4 of 6 non-chat models return errors via openai_chat

VERDICT: Config complete, transport gap unaddressed.
```

## The Cascading Report Pattern

All 3 reports passed the config audit (true). All 3 failed the transport audit.
The error: treating Layer 1+2 "discovery" as Layer 3 "dispatch."

Report 1: "all multimodal capabilities discovered and executable" - hallucinated execution.
Report 2: "all remaining tasks executed and sealed" - repeated same broken table, no new transport work.
Report 3: admitted the gap ("Option A vs B"), then wrote a 7000-token matrix labeling lanes
         `mcp_tool` / `websocket` that don't exist in Hermes - design doc dressed as deployment receipt.

Only after report 3's cleanup did config.yaml actually get the broken models removed.
The honest deliverable was: "pruned 2 broken model entries from config.yaml."

## What Would Make Non-Chat Models Reachable

For Hermes to dispatch Omni / Veo / Lyria / TTS, the system needs a separate MCP tool server
that wraps `google-genai` Python SDK:

```
Hermes Agent (openai_chat to gemini-3.7-flash)
    -> tool_call: gemini_generate_video(prompt="...")
        -> MCP tool server (google-genai SDK)
            -> client.models.generate_content(model="veo-3.1-generate-preview", ...)
            -> OR client.models.generate_videos(model="veo-3.1-generate-preview", ...)
            -> OR client.interactions.create(model="gemini-omni-flash-preview", ...)
        -> returns: video URL / audio file path
    -> Hermes relays to Telegram
```

This is a build task, not a config task. It was never built in this session.

## Reuse Trigger

When a deployment report says any of:

- "models discoverable and executable"
- "multimodal harmonization complete"
- "transport unified"
- "X layer wired into Y lane"
- "all routes reachable"

...probe each named lane at Layer 3 (the slow, runtime-decisive layer). Config and catalog
probes are necessary but not sufficient. The Layer 3 error signatures above are stable across
sessions - if you see them, the lane is not openai_chat-compatible, regardless of what the
report claims.
