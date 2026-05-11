---
name: deepseek-hermes-integration
description: Live API-verified DeepSeek model behavior for Hermes Agent integration — model IDs, reasoning quirks, auxiliary slot optimization, and provider setup
category: ai-providers
tags: [deepseek, hermes, model-config, fallback, auxiliary-models]
created: 2026-05-11
updated: 2026-05-11
owner: arif
---

# DeepSeek Model Discovery — Hermes Integration

## Live API Verification (2026-05-11)

Tested against production DeepSeek API with key `***REDACTED***`.

### Available Models

| Hermes model ID | Actual API model | Notes |
|-----------------|------------------|-------|
| `deepseek-chat` | `deepseek-v4-flash` | Base chat |
| `deepseek-reasoner` | `deepseek-v4-flash` | Chain-of-thought visible in `reasoning_content` field |
| `deepseek-v4-flash` | `deepseek-v4-flash` | Explicit — same as `deepseek-chat` |
| `deepseek-v4-pro` | `deepseek-v4-pro` | Higher capability, not yet live-tested |

### Key Quirks

- Both `deepseek-chat` and `deepseek-reasoner` use the **same underlying flash model** (`deepseek-v4-flash`) — the difference is only in behavior (reasoner shows reasoning trace)
- `reasoning_content` field appears in response for reasoner, making thinking transparent
- OpenAI-compatible endpoint: `https://api.deepseek.com/chat/completions`
- Auth: `Authorization: Bearer <key>` header

### Pricing Context (estimated)
- `deepseek-v4-flash` is the cheap/flash tier
- `deepseek-v4-pro` is the premium tier
- For auxiliary tasks (title_gen, compression, session_search) → use flash tier
- For fallback main model → `deepseek-v4-flash` is safe and capable

## Hermes Config Pattern

### Provider entry in `config.yaml`:
```yaml
providers:
  deepseek:
    name: deepseek
    api_key: ${DEEPSEEK_API_KEY}
    base_url: https://api.deepseek.com
```

### Fallback model (recommended):
```yaml
fallback_model:
  provider: deepseek
  model: deepseek-v4-flash
```

### Auxiliary overrides (good value):
```yaml
auxiliary:
  title_generation:
    provider: deepseek
    model: deepseek-v4-flash
  compression:
    provider: deepseek
    model: deepseek-v4-flash
  session_search:
    provider: deepseek
    model: deepseek-v4-flash
```

## Full Provider Stack (2026-05-11)

| Priority | Provider | Model | Key in .env? |
|----------|----------|-------|-------------|
| Primary | minimax | MiniMax-M2.7 | ✅ |
| Fallback | deepseek | deepseek-v4-flash | ✅ (added today) |
| Local | ollama | varies | ✅ (local, no key) |
| Available | openrouter | varies | ❌ (commented out) |
| Available | kimi (moonshot) | moonshot-v1-* | ❌ (no key) |
| Available | google (gemini) | gemini-2.5-flash | ❌ (no key) |

## Adding Kimi (Moonshot AI)

If Arif adds Kimi later:
1. Get key from https://platform.moonshot.cn → API keys
2. Add to `.env`: `KIMI_API_KEY=sk-...`
3. Add provider in `config.yaml`:
   ```yaml
   providers:
     kimi:
       name: kimi
       api_key: ${KIMI_API_KEY}
       base_url: https://api.moonshot.cn/v1
   ```
4. Model IDs: `moonshot-v1-8k`, `moonshot-v1-32k`, `moonshot-v1-128k`

## Testing New Provider Auth

Always verify before surfacing to user:
```bash
curl -X POST https://api.deepseek.com/chat/completions \
  -H "Authorization: Bearer sk-YOUR-KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"test"}],"max_tokens":5}'
```
Expect: `200 OK` with `choices[0].message.content`