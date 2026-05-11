---
name: ollama-on-vps
description: Ollama LLM running on VPS as arifOS/A-FORGE fallback — models, endpoints, embedding setup
triggers: ollama, qwen, local LLM, LLM fallback
category: ai-providers
last_updated: 2026-05-06
---

# Ollama on VPS — arifOS Federation LLM Fallback

## Running Container
```
Container: ollama-engine-prod
Image: ollama/ollama:latest
Network: docker bridge / compose network
```

## Models Loaded (verified 2026-05-06)
```
qwen2.5:7b        — chat model (used by arifOS call_llm Tier 2 fallback)
bge-m3:latest     — embedding model (used by A-FORGE LongTermMemory)
```

## Endpoints

### Chat API (Ollama native)
```
POST http://127.0.0.1:11434/api/generate
{
  "model": "qwen2.5:7b",
  "prompt": "...",
  "stream": false,
  "temperature": 0.3,
  "options": {"num_predict": 1200}
}
```
Response: `{"response": "...", "done": true}`

### Embeddings API
```
POST http://127.0.0.1:11434/api/embeddings
{
  "model": "bge-m3:latest",
  "prompt": "..."
}
```
Response: `{"embedding": [...], "done": true}`

### Model List
```
GET http://127.0.0.1:11434/api/tags
```
Response: `{"models": [{"name": "qwen2.5:7b"}, {"name": "bge-m3:latest"}]}`

## arifOS Usage (Tier 2 Fallback)

File: `/root/arifOS/arifosmcp/runtime/llm_client.py`

```python
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL") or os.getenv("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

async def _call_ollama(system, user, response_schema, temperature, max_tokens=1200):
    prompt = f"{system}\n\n{user}"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "temperature": temperature,
        "options": {"num_predict": max_tokens},
    }
    if response_schema:
        payload["format"] = "json"
    # ... httpx POST to /api/generate
```

**arifOS calls Ollama when SEA-LION Tier 1 fails.** All 3 LLM tools (mind_reason, heart_critique, reply_compose) fall back here.

## A-FORGE Usage (Embedding)

File: `/root/A-FORGE/src/memory/LongTermMemory.ts`
```typescript
const OLLAMA_URL = process.env.OLLAMA_URL ?? "http://localhost:11434";
const response = await fetch(`${OLLAMA_URL}/api/embeddings`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ model: "bge-m3:latest", prompt }),
});
```

## Docker Network DNS

From inside other containers (arifOS MCP, A-FORGE):
```
http://ollama:11434  (Docker compose service name)
```
From VPS host:
```
http://127.0.0.1:11434
```

## Troubleshooting

**Ollama not responding:**
```bash
curl -s http://127.0.0.1:11434/api/tags
# Empty = container down
docker ps | grep ollama
```

**Model not loaded:**
```
"model 'qwen2.5:7b' not found"
```
→ `docker exec ollama-engine-prod ollama pull qwen2.5:7b`

**arifOS still trying SEA-LION:**
Check logs — if you see "SEA-LION HTTP 401" repeatedly, Tier 1 is failing and falling through to Ollama. This is EXPECTED behavior when SEA-LION key is invalid.

## Adding New Models
```bash
docker exec -it ollama-engine-prod ollama pull <model>
# e.g.:
docker exec -it ollama-engine-prod ollama pull llama3:8b
docker exec -it ollama-engine-prod ollama pull nomic-embed-text
```

**Update arifOS to use new model:**
```bash
# In .env
OLLAMA_MODEL=llama3:8b
```

**Update A-FORGE embedding model:**
```bash
# In A-FORGE .env
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```
