# Z.AI Direct Provider Integration (2026-08-12)

## Context

Z.AI (Zhipu AI) Coding Plan Pro provides 8 GLM models via a direct OpenAI-compatible endpoint.
This is a **dedicated coding plan** — NOT pay-as-you-go. The endpoint is `api.z.ai/api/coding/paas/v4`.

## Architecture: Direct vs Proxy

```
DIRECT PATH (OpenCode → Z.AI):
  OpenCode config → zai provider → https://api.z.ai/api/coding/paas/v4 → Z.AI servers
  ✅ No middleman. Lowest latency. BYOK (ZAI_API_KEY).

PROXY PATH (FED → Z.AI):
  Agent → FED/LiteLLM → zai-pro alias → Z.AI servers
  ⚠️ Extra hop. Used when FED routing intelligence is needed.
```

**Rule:** When sovereignty matters (F13-grade work), prefer direct. When mesh diversity matters (Gödel E3), prefer proxy.

## OpenCode Direct Provider Config

Added to `/root/.config/opencode/opencode.json` under `provider.zai`:

```json
{
  "zai": {
    "npm": "@ai-sdk/openai-compatible",
    "name": "Z.AI Direct (GLM Coding Plan)",
    "options": {
      "baseURL": "https://api.z.ai/api/coding/paas/v4",
      "apiKey": "{env:ZAI_API_KEY}"
    },
    "models": {
      "glm-5.2": { "reasoning": true, "tool_call": true, "context": 198000, "output": 128000 },
      "glm-5.1": { "reasoning": true, "tool_call": true, "context": 200000, "output": 128000 },
      "glm-5":   { "reasoning": true, "tool_call": true, "context": 200000, "output": 128000 },
      "glm-5-turbo": { "reasoning": true, "tool_call": true, "context": 200000, "output": 128000 },
      "glm-4.7": { "reasoning": true, "tool_call": true, "context": 128000, "output": 16384 },
      "glm-4.6": { "reasoning": false, "tool_call": true, "context": 128000, "output": 16384 },
      "glm-4.5-air": { "reasoning": false, "tool_call": true, "context": 128000, "output": 16384 },
      "glm-4.5": { "reasoning": true, "tool_call": true, "context": 128000, "output": 16384, "attachment": true }
    }
  }
}
```

Agent model references:
- `zai/glm-5.2` — direct, via OpenCode
- `litellm-federation/zai-pro` — proxy, via FED

## Available Models (live probe 2026-08-12)

| Model | Capability | Notes |
|---|---|---|
| glm-5.2 | 753B MoE, 198K ctx, 128K output, reasoning | Primary. Tier-equivalent to Qwen3.8-MAX. |
| glm-5.1 | 200K ctx, 128K output, reasoning | Stable. |
| glm-5 | Zhipu flagship, 200K ctx, reasoning | Base generation. |
| glm-5-turbo | 200K ctx, reasoning | Fast inference. |
| glm-4.7 | 128K ctx, reasoning | Previous gen. |
| glm-4.6 | 128K ctx, fast | Lightweight. |
| glm-4.5-air | 128K ctx, ultra-fast | Cheapest. |
| glm-4.5 | 128K ctx, multimodal (image input) | Vision capable. |

## Environment Variables

| Key | Value |
|---|---|
| `ZAI_API_KEY` | `1abdeaf...` (in `kunci-mas.env`) |
| `ZAI_API_BASE` | `https://api.z.ai/api/coding/paas/v4` |
| `ZAI_PAYG_BASE` | `https://api.z.ai/api/paas/v4` (non-coding) |

**Key isolation:** `api.z.ai/api/coding/paas/v4` is the Coding Plan endpoint. `api.z.ai/api/paas/v4` is the general pay-as-you-go endpoint. Using the wrong endpoint = 401 or wrong model availability.

## FED Integration

Z.AI is already integrated in FED (:7074) routing:
- Alias `zai-pro` in LiteLLM config — routes to Z.AI Coding Plan
- Alias `fed-audit-glm` — audit model alias
- Provider state: `zai-direct` with balance $12, ENABLE verdict
- GLM-5.2 has $0.00 cost markers in FED routing tables (Coding Plan is flat-rate)

## Pitfalls

1. **Endpoint confusion:** Coding Plan (`/coding/paas/v4`) ≠ general API (`/paas/v4`). Always use coding endpoint for OpenCode/FED.
2. **Model ID case sensitivity:** Use lowercase `glm-5.2`, not `GLM-5.2`. Z.AI API accepts both but litellm may normalize differently.
3. **OpenCode config size:** Adding 8 models adds ~200 lines. Config is already 3300+ lines — consider pruning stale entries in future cleanup.
4. **Reasoning token format:** Z.AI returns `reasoning_tokens` in usage. FED correctly parses this for billing, but other tools may not.
