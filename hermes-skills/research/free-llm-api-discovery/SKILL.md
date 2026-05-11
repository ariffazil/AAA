---
name: free-llm-api-discovery
description: Live-probe LLM API providers to discover genuinely free tiers vs. documented-but-paid tiers. Use when user asks for free/non-American AI API keys for AGI stack or cost-sensitive deployments.
---

# Free LLM API Discovery

Use when: user wants free/non-American LLM API keys, or needs affordable LLM API for AGI stack, or asks "what free AI do I need".

## Core Insight

**Live probe > documentation.** Many providers claim "free tier" but live API calls return 401/auth errors. Always verify with live curl probes.

## Live Probe Protocol

### 1. OpenRouter (Most Reliable Discovery Endpoint)

```bash
curl -s --max-time 8 "https://openrouter.ai/api/v1/models" \
  -H "Authorization: Bearer test" \
  | python3 -c "
import sys,json
d=json.load(sys.stdin)
for m in d.get('data',[]):
    price = m.get('pricing',{})
    free = '⭐ FREE' if price and all(v == '0' for v in price.values()) else ''
    print(m['id'], free)
"
```

This returns **all models with live pricing** — filter for `⭐ FREE` entries. No API key needed to list models.

### 2. Groq

```bash
curl -s --max-time 8 "https://api.groq.com/openai/v1/models" \
  -H "Authorization: Bearer test_key"
```

Note: Groq free tier = 15-30 req/min. No credit card at `console.groq.com`.

### 3. SEA-LION (AI Singapore)

```bash
curl -s "https://api.sea-lion.ai/v1/models" -H "Authorization: Bearer test"
# Returns 401 — NOT FREE despite being in arifOS catalog
```

### 4. DeepSeek

```bash
curl -s --max-time 8 "https://api.deepseek.com/v1/models" \
  -H "Authorization: Bearer test"
# Returns auth error — NOT FREE
```

### 5. Together AI

```bash
curl -s --max-time 8 "https://together.ai/api/v1/models" -H "Authorization: Bearer test"
# Returns 301 redirect — no clear free tier
```

## Verified Free Stack (2026-05)

| Provider | Free Model | Sign-up | Card needed |
|----------|-----------|---------|-------------|
| **OpenRouter** | `openrouter/auto` (free tier picks best free model) | openrouter.ai | ❌ No |
| **OpenRouter** | `meta-llama/llama-3.3-70b-instruct` | openrouter.ai | ❌ No |
| **OpenRouter** | `qwen/qwen3-next-80b-a3b-instruct` | openrouter.ai | ❌ No |
| **Groq** | `llama-3.3-70b-instruct` | console.groq.com | ❌ No |
| **Groq** | `llama-3.2-3b-instruct` | console.groq.com | ❌ No |
| **Ollama** (local) | `qwen2.5:7b` | Already on VPS | FREE |

## arifOS Integration Points

- `arifOS/config/secret-registry.yaml` — register `llm.groq.api_key`, `llm.openrouter.api_key`
- `arifOS/arifosmcp/core/model_governance.yaml` — add Groq/OpenRouter model entries
- Ollama already configured in `deploy/docker-compose.yml`

## Strategy for arifOS AGI Stack

**Minimum $0 stack:**
1. Groq (`llama-3.3-70b`) — primary ASI reasoning (fast, free)
2. Ollama (`qwen2.5:7b`) — local fallback (zero latency)
3. OpenRouter (`openrouter/auto`) — deep research, free tier routing

## Pitfalls

- SEA-LION looks free in arifOS docs but requires paid key — always probe
- DeepSeek is NOT free despite Chinese origin
- OpenRouter free tier is rate-limited — not for production高频
- "Free" often means limited credits, not unlimited — check rate limits
