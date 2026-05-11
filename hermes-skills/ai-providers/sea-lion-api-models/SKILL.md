---
name: sea-lion-api-models
description: Correct model IDs for SEA-LION API (api.sea-lion.ai) — avoid 400/401 errors from wrong model names
triggers: sea-lion, Llama-SEA-LION, SEA-GUARD, Gemma-SEA-LION
category: ai-providers
last_updated: 2026-05-07
---

# SEA-LION API — Correct Model IDs

## Endpoint
```
POST https://api.sea-lion.ai/v1/chat/completions
Authorization: Bearer sk-znzfOJH_Yc7LKewfrfsl2A
```

## Working Models (verified 2026-05-06)

| Model ID | Status | Use Case |
|----------|--------|----------|
| `aisingapore/Llama-SEA-LION-v3.5-70B-R` | ✅ Works | Complex multi-step reasoning |
| `aisingapore/Llama-SEA-LION-v3-70B-IT` | ✅ Works | General reasoning |
| `aisingapore/Gemma-SEA-LION-v4-27B-IT` | ✅ Works | Fast lightweight tasks |
| `aisingapore/Qwen-SEA-LION-v4-32B-IT` | ✅ Works | ASEAN language, general |
| `aisingapore/SEA-Guard` | ✅ Works | Safety filter only — returns plain "safe" or "unsafe" |

## Rate Limit
**10 requests/minute per user** — hard constraint for automation. Design throttling around this.

## Key Status (verified 2026-05-07)
**The SEA-LION API key `sk-znzfOJH_Yc7LKewfrfsl2A` is VALID and LIVE.**

Direct curl test 2026-05-07:
```
curl -s -X POST https://api.sea-lion.ai/v1/chat/completions \
  -H "Authorization: Bearer sk-znzfOJH_Yc7LKewfrfsl2A" \
  -H "Content-Type: application/json" \
  -d '{"model": "aisingapore/Qwen-SEA-LION-v4-32B-IT",
       "messages": [{"role": "user", "content": "Reply exactly: Hermes SEA-LION works"}],
       "max_tokens": 30}'
→ 200: "Hermes SEA-LION works." ✅ exit_code=0
```

**IMPORTANT — Hermes CLI routing note:**
Hermes Agent's `hermes chat -m "aisingapore/Qwen-SEA-LION-v4-32B-IT"` routes through MiniMax provider (`api.minimax.io`) by default, which does NOT host SEA-LION models → **HTTP 400 unknown model**. Always use `curl` for direct SEA-LION verification, not Hermes CLI.

**The git `.env` masks the key as `***` but the live container key works** — likely because the host environment or docker-compose injects the real value at runtime. If SEA-LION calls from arifOS still fail (all traffic going to Ollama fallback), check whether `SEA_LION_API_KEY` inside the container is the real value or `***`.

## arifOS LLM Architecture (full picture)
```
arifOS MCP server (runtime/llm_client.py)
├── Tier 1: SEA-LION remote API  [ACTIVE — key verified live 2026-05-07]
│   └── model: aisingapore/Qwen-SEA-LION-v4-32B-IT
│   └── base_url: https://api.sea-lion.ai/v1
├── Tier 2: Ollama local fallback [qwen2.5:7b @ http://127.0.0.1:11434]
└── Tier 3: LLMUnavailableError → deterministic fallback

Tools using call_llm():
├── arif_mind_reason    (333 MIND — reasoning)
├── arif_heart_critique (666 HEART — ethical critique)
└── arif_reply_compose  (444r REPLY — response composition)
```

## Fixing SEA-LION in arifOS
**Key is confirmed valid** (2026-05-07). If arifOS calls still fail:
1. Verify container has real key (not `***`):
   ```bash
   docker exec arifosmcp env | grep SEA_LION_API_KEY
   ```
2. If masked, fix via docker-compose environment override in `/root/compose/docker-compose.yml`:
   ```yaml
   environment:
     - SEA_LION_API_KEY=sk-znzfOJH_Yc7LKewfrfsl2A
   ```
3. Restart: `cd /root/compose && docker compose restart arifosmcp`
4. Verify: check container logs for "SEA-LION inference complete"

## Common Errors

**Wrong model name — 400:**
```
"Invalid model name passed in model=standard"
"key not allowed to access model. This key can only access models=['standard']"
"invalid params, unknown model 'aisingapore/qwen-sea-lion-v4-32b-it'"
```
→ Do NOT use `standard`, `sea-lion-8b`, or bare model names. Must use the full `aisingapore/...` prefix.
→ **Note:** MiniMax provider (`api.minimax.io`) does not host SEA-LION models — use `api.sea-lion.ai` directly or curl.

**Authentication error — 401 (key masked in .env):**
```
"LiteLLM Virtual Key expected. Received=***, expected to start with 'sk-'."
```
→ `.env` has `SEA_LION_API_KEY=***` — key is masked, not the real value. Fix via docker-compose environment override (see Fixing section above).

**Rate limit death spiral — 429 + 401 cascade:**
```
429: "rate limit exceeded"
→ subagents retry immediately
→ 401: "key not allowed to access model" (lowercase model name in retry)
→ retry again
→ all 10 req/min consumed in failed retries
→ Ollama fallback also rates limit under pile-up
```
→ This is NOT a key rotation problem. Key is likely fine. Root cause: no semaphore + no backoff in `llm_client.py`. Add `asyncio.Semaphore(1)` to serialize calls and exponential backoff on 429.

**Authentication error — 401 (key genuinely invalid/rotated):**
```
"Unable to find token in cache or `LiteLLM_VerificationTokenTable`"
"Authentication Error, Invalid proxy server token passed."
```
→ Key has been rotated. Get fresh key from AI Singapore (aisea-sg.smartsheet.com form or AI Singapore team).

## Verified Test Script
```python
import requests
key = 'sk-znzfOJH_Yc7LKewfrfsl2A'
models = [
    'aisingapore/Llama-SEA-LION-v3.5-70B-R',
    'aisingapore/Llama-SEA-LION-v3-70B-IT',
    'aisingapore/Gemma-SEA-LION-v4-27B-IT',
    'aisingapore/Qwen-SEA-LION-v4-32B-IT',
    'aisingapore/SEA-Guard',
]
for model in models:
    r = requests.post('https://api.sea-lion.ai/v1/chat/completions',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
        json={'model': model, 'messages': [{'role': 'user', 'content': 'hi'}], 'max_tokens': 5},
        timeout=10)
    print(f'{model}: {r.status_code}')
```

## SEA-Guard Safety Filter (Plain Text Response)
SEA-Guard model returns plain text `"safe"` or `"unsafe"` — NOT JSON.
The response is just the word, no markdown, no code blocks.
```python
# Parse SEA-Guard response
raw = r.json()['choices'][0]['message']['content'].strip().lower()
# raw == "safe" → passed
# raw == "unsafe" → blocked
```

## Case-Sensitive Model IDs — Critical

**Model IDs are CASE-SENSITIVE.** The API will reject `aisingapore/qwen-sea-lion-v4-32b-it` (lowercase) but the error message echoes the model back in whatever case was sent, which can be misleading.

**Correct:** `aisingapore/Qwen-SEA-LION-v4-32B-IT` (mixed case, uppercase B)
**Wrong:** `aisingapore/qwen-sea-lion-v4-32b-it` (all lowercase — will 400)

**The bad model is NOT always from config.** When tracing a 400 bad model error:
1. arifOS `llm_client.py` uses the correct case — not the source
2. Check session dump files at `~/.hermes/sessions/request_dump_*.json` — subagent curl commands may have lowercased the model
3. The SEA-LION API echoes the model back in the error message exactly as received, so a subagent's lowercase curl will produce a lowercase error echo

**Diagnostic:**
```bash
# Find the bad model in session files
grep -rn "qwen-sea\|aisingapore.*qwen" ~/.hermes/sessions/ | grep -v "Qwen-SEA"

# Check if a subagent ran curl with the wrong case
grep -n "curl.*sea-lion\|POST.*sea-lion" ~/.hermes/sessions/session_*.json
```

## Budget / Commercial Fit (verified from public docs 2026-05-07)
- **API key provisioning:** public docs say to create a key via the **SEA-LION Playground** (`https://playground.sea-lion.ai/`)
- **Direct API pricing:** no clear public per-token or per-request pricing page was found for the direct `api.sea-lion.ai` API during verification
- **Published hard constraint:** direct API is still documented at **10 requests/minute per user** and the docs explicitly say to contact them if you want a rate-limit increase
- **Self-hosting option exists:** inferencing docs state SEA-LION models are **freely available for download** and can be hosted on self-managed infra or cloud providers
- **Cloud-managed pricing is externalized:** Cloudflare Workers AI / Amazon Bedrock / Vertex AI guides point to those providers' own pricing models, not a SEA-LION-native public price sheet

### Practical recommendation for a budget ('miskin') agent stack
- **Not a must-have core provider** for agentic orchestration, MCP loops, or parallel subagent traffic
- **Worth keeping as an optional specialist lane** if access is free / subsidized / near-free
- Best use cases: **BM/Indonesia/ASEAN language tone, translation, local-context summarization, second-opinion witness**
- Weak fit for primary backbone because: **10 RPM is tight**, no built-in web grounding, and it can hallucinate project-specific facts

## Limitations
- SEA-LION does NOT have web search — it generates plausible-sounding facts
- It hallucinated arifOS v1.0.0 (2023), wrong GitHub URL — it is NOT grounded in live data
- Cannot be used as a F2 fact-checker for arifOS-specific claims
- Its value: ASEAN language reasoning, general knowledge, external attestation (F3 witness)

## arifOS LLM Architecture (full picture)
```
arifOS MCP server (runtime/llm_client.py)
├── Tier 1: SEA-LION remote API  [ACTIVE — key verified live 2026-05-07]
│   └── model: aisingapore/Qwen-SEA-LION-v4-32B-IT
│   └── base_url: https://api.sea-lion.ai/v1
├── Tier 2: Ollama local fallback [qwen2.5:7b @ http://127.0.0.1:11434]
└── Tier 3: LLMUnavailableError → deterministic fallback

Tools using call_llm():
├── arif_mind_reason    (333 MIND — reasoning)
├── arif_heart_critique (666 HEART — ethical critique)
└── arif_reply_compose  (444r REPLY — response composition)
```

## Diagnosing SEA-LION Failures (Critical Path)

When SEA-LION calls fail, check IN ORDER:

**Step 1 — Key is valid? (Never assume it's rotated.)**
```bash
# Direct curl test — bypasses all config/env/docker masks
curl -s -X POST https://api.sea-lion.ai/v1/chat/completions \
  -H "Authorization: Bearer sk-znzfOJH_Yc7LKewfrfsl2A" \
  -H "Content-Type: application/json" \
  -d '{"model": "aisingapore/Qwen-SEA-LION-v4-32B-IT",
       "messages": [{"role": "user", "content": "Reply exactly: OK"}],
       "max_tokens": 10}'
# 200 + "OK" = key is LIVE
```

**Step 2 — Container has real key (not `***`)?**
```bash
docker exec arifosmcp sh -c 'echo "KEY_START>>>$SEA_LION_API_KEY<<<KEY_END"'
# If truncated to sk-znz...sl2A = real key present (Docker truncates display, not empty)
# If shows literally "***" = key not injected, fix via compose env override
```

**Step 3 — Check for wrong model case in subagent session dumps:**
```bash
grep -rn "qwen-sea\|aisingapore.*qwen" ~/.hermes/sessions/ | grep -v "Qwen-SEA"
grep -rn "curl.*sea-lion\|POST.*sea-lion" ~/.hermes/sessions/session_*.json
```
Subagents using lowercase model name → HTTP 400 (echoed back in error) → retry → rate limit pile-up.

**Step 4 — Rate limit death spiral?**
`llm_client.py` has NO semaphore and NO exponential backoff. Multiple concurrent callers hitting 10 req/min cap → 429 → immediate retry → all subagents stack up. Fix: add `asyncio.Semaphore(1)` + exponential backoff on 429.

**Step 5 — Ollama fallback is working?**
```bash
curl -s http://127.0.0.1:11434/api/generate \
  -d '{"model": "qwen2.5:7b", "prompt": "hi", "stream": false}'
# 200 = Ollama is live
```

## Fixing SEA-LION in arifOS (when key IS rotated)
1. Get fresh `sk-...` LiteLLM key from AI Singapore (aisea-sg.smartsheet.com)
2. Add to `/root/compose/docker-compose.yml` under arifosmcp service:
   ```yaml
   environment:
     - SEA_LION_API_KEY=sk-YOUR-NEW-KEY-HERE
   ```
3. `cd /root/compose && docker compose restart arifosmcp`
4. Verify: `docker exec arifosmcp logs --since 30s | grep -i "sea-lion inference"`

## Telegram @sealion_ai_bot Verification
```python
# Check if bot username exists on Telegram
import requests
token = 'YOUR_BOT_TOKEN'
r = requests.get(f'https://api.telegram.org/bot{token}/getChat',
    params={'chat_id': '@sealion_ai_bot'}, timeout=5)
# 200 + ok=True = bot exists; 400 = not found
```
`@sealion_ai_bot` is AI Singapore's own bot — cannot be added to arbitrary groups.
It is already in the AAA group. Cannot be governed by arifOS.
