---
name: china-ai-key-classification
description: "Use when classifying Chinese AI API keys by prefix type (sk-cp vs sk-sp vs sk-ws) to determine correct provider route. Classify Chinese AI API keys. sk-cp/sk-sp prefix detection."
version: 1.0.0
author: hermes-curator
license: MIT
metadata:
  hermes:
    category: AGI
    tags: [api-keys, coding-plan, token-plan, qwen, minimax, china-ai, classification]
    related_skills: [qwencloud-mesh, mmx-mesh, qwencloud-cli]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# China AI Platform — API Key Classification

Chinese AI platforms (Alibaba Qwen, MiniMax, Zhipu GLM, Moonshot Kimi, DeepSeek) all share the same architectural split between two credential systems. Misclassifying them wastes hours of trial-and-error.

## The Pattern (Universal)

Every major Chinese AI platform exposes two mutually exclusive credential tiers:

| Tier | Format | Purpose | Works for direct API? |
|---|---|---|---|
| **Token Plan / Standard API** | `sk-...` (no suffix) | Programmatic API calls, scripts, agents, batch jobs | YES |
| **Coding Plan** | `sk-cp-...`, `sk-sp-...`, `sk-api-...` (suffix varies) | Interactive coding IDEs only (Cursor, Claude Code, Qwen Code, OpenCode) | NO - returns 401/404 |

**The fatal mistake:** Treating a Coding Plan key as a Token Plan key. The CLI/script sees the key is "set" (prefix matches `sk-`), sends the request, and the platform rejects it with HTTP 401 (invalid api-key) or HTTP 404 (endpoint not found / model not exist).

## Platform-Specific Prefixes

| Platform | Coding Plan prefix | Standard prefix | Region domain |
|---|---|---|---|
| Alibaba Qwen (DashScope) | `sk-sp-` | `sk-` (also `sk-ws-` for Web Service) | `dashscope-intl.aliyuncs.com` (intl), `dashscope.aliyuncs.com` (CN) |
| Alibaba Qwen (Model Studio / Bailian) | `sk-sp-` | `sk-` | `maas.aliyuncs.com` |
| MiniMax | `sk-cp-` | `sk-` | `api.minimax.io` (global), `api.minimaxi.com` (CN) |
| Zhipu GLM | `glm-cp-` (or similar) | varies | `bigmodel.cn` |
| Moonshot Kimi | `sk-kimi-cp-` (or similar) | `sk-` | `api.moonshot.cn` |
| DeepSeek | `sk-ds-cp-` (or similar) | `sk-` | `api.deepseek.com` |

**Note:** Prefixes evolve. Always verify against the platform's current docs. When in doubt, attempt a 1-token probe — Coding Plan keys fail with 401/404 on direct API endpoints.

## Detection Heuristics

When you see a key like `sk-XYZ-rest_of_key`, classify it:

```
1. Does it start with sk-cp-?        → Coding Plan (interactive IDE only)
2. Does it start with sk-sp-?        → Coding Plan (interactive IDE only)
3. Does it start with sk-api-?       → Coding Plan (interactive IDE only)
4. Does it start with sk-ws-?        → Web Service (different endpoint, may work for some scripts)
5. Does it start with sk- (no other suffix)? → Standard Token Plan (direct API)
6. Unknown prefix?                    → Probe and infer
```

The middle segment often encodes the platform or seat — e.g. `sk-sp-H.DMPPMYI` for Qwen Token Plan individual pro seat. Decoding the middle is rarely necessary.

## What Coding Plan Keys CAN Do

- Authenticate Cursor, Claude Code, Qwen Code, OpenCode, Trae, Windsurf, RooCode, Cline
- Power interactive AI coding sessions in those IDEs
- Use the platform's hosted web playground

## What Coding Plan Keys CANNOT Do

- Direct REST API calls from scripts (`/v1/chat/completions`, etc.)
- `mmx quota show`, `qwencloud usage free-tier` (return 404 — quota endpoints not exposed to Coding Plan)
- Programmatic batch jobs
- Webhook callbacks
- Custom agent frameworks (unless they pretend to be a coding IDE)

## How to Get the Right Key

For each platform, the Token Plan key is obtained from the platform's main subscription page:

| Platform | Token Plan URL |
|---|---|
| Qwen (international) | https://home.qwencloud.com/api-keys |
| Qwen (mainland China) | https://bailian.console.aliyun.com/ |
| MiniMax (global) | https://platform.minimax.io/subscribe/token-plan |
| MiniMax (CN) | https://platform.minimaxi.com/subscribe/token-plan |
| GLM (Zhipu) | https://bigmodel.cn/ |
| Kimi (Moonshot) | https://platform.moonshot.cn/ |
| DeepSeek | https://platform.deepseek.com/ |

## Probe Pattern (Validate Before Burning Quota)

```bash
# Qwen Cloud international probe (lightweight, ~1 token)
curl -sS -X POST "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-turbo","messages":[{"role":"user","content":"hi"}],"max_tokens":1}'

# MiniMax global probe
curl -sS -X POST "https://api.minimax.io/v1/chat/completions" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M3","messages":[{"role":"user","content":"hi"}],"max_tokens":1}'

# MiniMax quota check
mmx quota show --output json
```

If you get `401 invalid_api_key` or `404 model_not_found`, the key is almost certainly Coding Plan or wrong-region.

## Pitfalls

1. **Don't assume `sk-` prefix means Token Plan** — always check for the suffix (`-cp-`, `-sp-`, `-api-`).
2. **Don't blame the script** when the key is wrong — the error is upstream.
3. **Don't waste quota probing** — use the smallest model + max_tokens=1.
4. **Don't paste keys into chat** — even Coding Plan keys can be revoked if leaked.
5. **Don't conflate region** — `sk-` key for CN platform ≠ `sk-` key for global platform. Same prefix, different validity.
6. **Don't try to "upgrade" Coding Plan to Token Plan via API** — it requires manual subscription change in the platform console.

## When to Use This Skill

Trigger this skill whenever:
- A key is mentioned but its type is unclear
- An API call fails with 401/404 and the key starts with `sk-`
- User asks why a CLI command returns AUTH_REQUIRED despite a key being "set"
- User pastes a key like `sk-cp-...` or `sk-sp-...` into env
- You're about to assume a key works and want to verify first

## Related Skills

| Skill | Relationship |
|---|---|
| `qwencloud-mesh` | QwenCloud meta-mesa orchestrator. References this skill in its key-compatibility section. |
| `mmx-mesh` | MiniMax meta-mesa orchestrator. Same pattern. |
| `qwencloud-cli` | Hermes-native skill for `qwencloud` CLI (uses OAuth, separate from API keys). |
| `qwen-harness-tools` | Covers Qwen Token Plan Harness tools (web search, code interpreter) — Token Plan only. |
| `qwen-token-plan-team-edition` | Covers the 4 Token Plan seats specifically. |

DITEMPA BUKAN DIBERI.