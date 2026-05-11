---
name: cloudflare-workers-ai
description: "Cloudflare Workers AI inference operations — run LLM, embedding, and vision models at the edge for GEOX and WEALTH coprocessors."
triggers:
  - "workers ai"
  - "edge inference"
  - "llama at edge"
  - "cf ai run"
  - "cloudflare embeddings"
  - "geox edge ai"
  - "wealth edge inference"
category: devops
---

# cloudflare-workers-ai — Edge Inference for arifOS Coprocessors

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given. Inference belongs at the edge.

## What This Enables

| Use Case | CF AI Model | arifOS Coprocessor |
|---|---|---|
| Earth physics reasoning | `@cf/meta/llama-3-8b-instruct` | GEOX (Ψ node) |
| Geoscience embedding | `@cf/thenlper/gte-base-en-v1.5` | GEOX vector search |
| Capital risk inference | `@cf/meta/llama-3-8b-instruct` | WEALTH EMV engine |
| Fast classification | `@cf/qwen/qwen2.5-7b-instruct-awq` | WEALTH crisis triage |

## Prerequisites

```bash
# Verify CF account + Workers AI enabled
curl -s "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/ai-gateway/models" \
  -H "Authorization: Bearer <CF_API_TOKEN>" | python3 -c "import json,sys; d=json.load(sys.stdin); print('✅ Workers AI available' if d.get('result') else '❌ Not enabled')"

# Account ID from CF dashboard or token scope
export CF_ACCOUNT_ID="<your-account-id>"
export CF_API_TOKEN="<cfat_token>"
```

## List Available Models

```bash
curl -s "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai-gateway/models" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" | python3 -c "
import json, sys
d = json.load(sys.stdin)
for m in d.get('result', []):
    print(f\"{m['id']} | {m.get('name','?')} | {m.get('status','?')}\")
"
```

## Run Inference

### Basic LLM
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai/run/@cf/meta/llama-3-8b-instruct" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Explain quantum tunneling in one sentence"}]}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['response'])"
```

### Streaming
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai/run/@cf/meta/llama-3-8b-instruct" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Count from 1 to 5"}], "stream": true}' \
  --output - | while IFS= read -r line; do
    [[ "$line" == data:* ]] && echo "${line#data: }" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('response',''), end='', flush=True)"
done
echo
```

### Embeddings (for GEOX vector search)
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai/run/@cf/thenlper/gte-base-en-v1.5" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"text": "Porosity log analysis for sandstone reservoir"}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(f\"Embedding dim: {len(d['result']['data'][0]['embedding'])}\")"
```

## Python Integration (for GEOX/WEALTH)

### geox/edge_inference.py
```python
import os
import requests

CF_ACCOUNT_ID = os.environ["CF_ACCOUNT_ID"]
CF_API_TOKEN = os.environ["CF_API_TOKEN"]
BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai"

def geox_edge_query(
    prompt: str,
    model: str = "@cf/meta/llama-3-8b-instruct",
    stream: bool = False
) -> str:
    """Run GEOX physics inference at Cloudflare edge."""
    response = requests.post(
        f"{BASE_URL}/run/{model}",
        headers={
            "Authorization": f"Bearer {CF_API_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "messages": [{"role": "user", "content": prompt}],
            "stream": stream
        },
        timeout=30
    )
    response.raise_for_status()
    result = response.json()
    return result["result"]["response"]

def geox_embedding(text: str) -> list[float]:
    """Get text embedding for GEOX vector search."""
    response = requests.post(
        f"{BASE_URL}/run/@cf/thenlper/gte-base-en-v1.5",
        headers={
            "Authorization": f"Bearer {CF_API_TOKEN}",
            "Content-Type": "application/json"
        },
        json={"text": text},
        timeout=10
    )
    response.raise_for_status()
    return response.json()["result"]["data"][0]["embedding"]
```

### wealth/risk_inference.py
```python
import os
import requests

CF_ACCOUNT_ID = os.environ["CF_ACCOUNT_ID"]
CF_API_TOKEN = os.environ["CF_API_TOKEN"]

def wealth_risk_query(
    scenario: str,
    model: str = "@cf/meta/llama-3-8b-instruct"
) -> dict:
    """Run WEALTH risk inference at CF edge — EMV calculation."""
    prompt = f"""You are the WEALTH capital intelligence engine.
Given: {scenario}
Return JSON: {{"emv": float, "risk_tier": "LOW|MEDIUM|HIGH|CRITICAL", "confidence": float}}"""
    
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/{model}",
        headers={"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"},
        json={"messages": [{"role": "user", "content": prompt}]},
        timeout=30
    )
    response.raise_for_status()
    import json
    return json.loads(response.json()["result"]["response"])
```

## AI Gateway — Cache + Rate Limit

### Create gateway namespace
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai-gateway/gateways" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"name": "arifos-ai-gateway", "model_type": "openai"}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('Gateway ID:', d['result']['id'])"
```

### Configure cache TTL (1 hour)
```bash
curl -s -X PUT "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai-gateway/gateways/arifos-ai-gateway" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"cache_ttl": 3600, "model_type": "openai", "rate_limit": {"requests": 60, "period": 60}}'
```

### Use gateway in AI calls
```bash
# Instead of direct model call:
# https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/ai/run/<MODEL>

# Route through gateway:
# https://gateway.ai.cloudflare.com/<ACCOUNT_ID>/arifos-ai-gateway/openai/v1/chat/completions
```

## Deploy a Worker with AI Binding

```bash
# Create worker with AI
wrangler generate arifos-ai-worker --template=typescript

cd arifos-ai-worker
```

```toml
# wrangler.toml
name = "arifos-ai-worker"
main = "src/index.ts"
compatibility_date = "2026-04-30"

[ai]
binding = "AI"

[[ kv_namespaces]]
binding = "ARIFOS_STATE"
id = "<KV_NAMESPACE_ID>"
```

```typescript
// src/index.ts
export interface Env {
  AI: Ai;
  ARIFOS_STATE: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    if (url.pathname === "/infer") {
      const body = await request.json<{ prompt: string; model?: string }>();
      const model = body.model || "@cf/meta/llama-3-8b-instruct";
      
      const answer = await env.AI.run(model, {
        messages: [{ role: "user", content: body.prompt }]
      });
      
      return new Response(JSON.stringify({ result: answer }), {
        headers: { "Content-Type": "application/json" }
      });
    }
    
    return new Response("Not found", { status: 404 });
  }
};
```

```bash
wrangler deploy
```

## Constitutional Notes

- **F2 TRUTH**: Always report actual model used and CF AI response. Don't cache fabricated results.
- **F6 EMPATHY**: WEALTH AI spending (CF Workers AI costs money) — confirm with Arif before heavy usage.
- **F7 HUMILITY**: CF Workers AI has rate limits (60 req/min per model). Handle 429 responses gracefully.

## Quick Reference

```bash
# Test model availability
curl -s "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai/models" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" | python3 -c "import json,sys; [print(m['id']) for m in json.load(sys.stdin)['result']]"

# Run quick inference test
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai/run/@cf/meta/llama-3-8b-instruct" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"ping"}]}' | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['response'])"

# Check AI Gateway cache
curl -s "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai-gateway/gateways/arifos-ai-gateway" \
  -H "Authorization: Bearer ${CF_API_TOKEN}"
```

## Related Skills
- `cloudflare-agents` — token setup, account provisioning, Workers/Workers KV setup
- `cloudflare-tunnel` — expose local CF AI Workers without opening firewall ports
- `geox-ground` — GEOX earth-domain reasoning (CF AI as coprocessor backend)
