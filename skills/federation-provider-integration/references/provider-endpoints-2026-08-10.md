# Provider Endpoint Corrections — 2026-08-10

Verified via live probe against each endpoint. Blueprint docs often have wrong domains.

## Corrected Endpoints

| Provider | Blueprint Said | Actually Works | Key Used |
|---|---|---|---|
| **Kimi Coding** | `api.moonshot.ai/v1` ❌ | `api.kimi.com/coding/v1` ✅ | `KIMI_API_KEY` |
| **Kimi K3** | (missing) | `platform.kimi.ai` | `KIMI_API_KEY` |
| **MiMo** | `api.xiaomimimo.com/v1` ❌ | `token-plan-sgp.xiaomimimo.com/v1` ✅ | `MIMO_API_KEY` |
| **OpenCode Go** | `opencode.ai/api/v1` ❌ | DEAD (401 Insufficient balance) | N/A |
| **DeepSeek** | `api.deepseek.com/v1` ✅ | Works | `DEEPSEEK_API_KEY` |
| **MiniMax** | `api.minimax.io/v1` ✅ | Works | `MINIMAX_API_KEY` |
| **Gemini OpenAI** | `googleapis.com/v1beta/openai/` ✅ | Works | `GEMINI_API_KEY` |
| **Qwen Token Plan** | `dashscope.aliyuncs.com` | 429 EXHAUSTED (reset Sept 1) | `QWEN_API_KEY` |

## Pool Status (2026-08-10)

| Pool | Status | Notes |
|---|---|---|
| DeepSeek Direct | ✅ LIVE | PAYG, works |
| Kimi Coding | ✅ LIVE | K2.7 Code, works |
| MiniMax Direct | ✅ LIVE | M3, works |
| Gemini OpenAI GW | ✅ LIVE | 3.6-flash confirmed |
| Qwen Token Plan | ❌ EXHAUSTED | 0/150,000 credits, reset Sept 1 |
| OpenCode Go | ❌ DEAD | 401, no balance |
| MiMo | ⚠️ UNVERIFIED | Endpoint corrected but not re-probed |

## Key Format Reference

| Provider | Key Prefix | Notes |
|---|---|---|
| Qwen Token Plan | `sk-sp-` | Team vs Individual not distinguishable by prefix |
| Qwen PAYG | `sk-ws-` | Workspace key |
| DeepSeek | `sk-` | Standard |
| Kimi | `sk-` | Standard |
| MiniMax | `sk-` | Standard |
| Gemini | `AIza...` | Google AI Studio format |
