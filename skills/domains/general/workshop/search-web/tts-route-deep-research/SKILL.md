---
name: tts-route-deep-research
description: "Use when routing TTS requests across providers or deep-researching TTS engine capabilities and routing. Probe every TTS endpoint across providers. Never assume."
capability_tier: fed-realtime-voice
ecology_state: WARM
---

# tts-route-deep-research

## Anti-fabrication discipline

When user asks "any free TTS?" or "test all", **never assume**. Probe each route live. Document working/not-working with evidence (HTTP codes, error messages).

## Probe order (cheap → expensive)

### Layer 1 — Free, no auth

```bash
python3 -c "
import asyncio, edge_tts
async def main():
    voices = await edge_tts.list_voices()
    print([v['ShortName'] for v in voices if v['Locale'].startswith('ms-')])
asyncio.run(main())
"
```
Free voices: `ms-MY-OsmanNeural`, `ms-MY-YasminNeural`, `id-ID-ArdiNeural`, `en-AU-WilliamMultilingualNeural`.

### Layer 2 — Local binaries

```bash
which piper espeak-ng festival flite pico2wave
ls /root/.local/share/piper/voices/
```

### Layer 3 — FLAME :18901

```bash
curl -sS --max-time 5 http://127.0.0.1:18901/ | head -c 500
curl -sS --max-time 5 http://127.0.0.1:18901/help | head -c 1000
# FLAME has only: /health /probe /summarize /classify /verify
# /v1/chat/completions /v1/models /completions — NO TTS
```

### Layer 4 — Token Plan REST

```bash
bash -c 'source /root/.secrets/kunci-root.env
curl -sS "$BAILIAN_TOKEN_PLAN_BASE_URL/models" \
  -H "Authorization: Bearer $BAILIAN_TOKEN_PLAN_API_KEY" \
  | python3 -c "import json,sys; [print(m[\"id\"]) for m in json.load(sys.stdin)[\"data\"]]"'

for p in "/audio/speech" "/audio/tts" "/tts" "/v1/audio/speech" "/v1/audio/tts"; do
  echo -n "$p: HTTP "
  curl -sS -o /dev/null -w "%{http_code}" -X POST "$BASE$p" \
    -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
    -d "{\"model\":\"qwen-audio-3.0-tts-plus\",\"input\":\"test\",\"voice\":\"male\"}" \
    --max-time 10
  echo ""
done
# All 404 — OpenAI-compat endpoints not exposed
```

### Layer 5 — Provider-direct

```bash
# MiniMax TTS — PROVEN
curl -sS -X POST "https://api.minimax.io/v1/text_to_speech" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"test","voice_id":"male-qn-qingse","model":"speech-2.6-hd"}'
# 1002 RPM if hit hard; works via MCP wrapper

# Z.ai TTS — check for ZAI_API_KEY
# OpenCode Zen TTS — check for OPENCODE_ZEN_API_KEY  
# Groq TTS — check for GROQ_API_KEY (free tier: playai-tts)
# ElevenLabs — check for ELEVENLABS_API_KEY
```

### Layer 6 — Azure OpenAI deployment

```bash
bash -c 'source /root/.secrets/kunci-root.env
curl -sS "$AZURE_OPENAI_ENDPOINT/openai/deployments?api-version=2025-01-01-preview" \
  -H "api-key: $AZURE_OPENAI_KEY"'
# 404 = no TTS deployment provisioned
```

### Layer 7 — MCP servers (already wired)

`mcp__minimax_media__text_to_audio` via Python streamable HTTP (see `forge-minimax-mcp-direct-invoke`).

## Quota buckets — distinguish before declaring "dead"

- Token Plan has **per-product** quotas (image / video / audio / LLM)
- 429 message includes **reset timestamp** — read it
- MCP minimax-media has **separate RPM buckets** per tool (1002 = RPM, 2056 = quota)

## Output format (zen report)

End with a **table**:

| Route | Cost | Quality | Limit | Evidence |
|---|---|---|---|---|
| Edge-TTS | FREE | Good | Unlimited | HTTP 200 |
| MiniMax MCP | Paid | High | Quota | Trace-Id |

Mark every cell with **evidence**, not assertion.

## Federation state

- `mcp__fed__fed_status` (port 7074) — full provider catalog (balance, latency, health)
- `mcp__fed__fed_route` — ranked routes (best for LLM, NOT TTS)
