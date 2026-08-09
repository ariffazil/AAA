# AAA Native AI Panel — Full Build Plan

## Executive Summary

This document is a one-shot engineering reference for building the AAA AI panel natively into `aaa.arif-fazil.com`. No Open WebUI in the public stack. No new domain. AAA stays sovereign.

The build has four layers:

1. **Express backend** on `:3001` — four AI routes proxying Ollama, Qdrant, and the bge-m3 embedding model
2. **React frontend** — `AiPanel.tsx` mounted on `#ai` hash route, no extra router dep
3. **Caddy** — one directive addition per route with `flush_interval -1` for streaming
4. **Vision gate** — `gemma3` first, `qwen2.5vl` deferred until RAM envelope confirms headroom

---

## Architecture Map

```
Browser → aaa.arif-fazil.com/#ai
              │
              ▼
         AAA React App
          AiPanel.tsx
              │
              ▼ fetch (POST / EventSource-style ReadableStream)
    aaa.arif-fazil.com/api/ai/*
              │
              ▼ Caddy reverse_proxy
         Express :3001
        ┌──────┬──────┬──────────────┐
        │      │      │              │
      /models /chat  /rag/query  /rag/upload
        │      │      │              │
     Ollama  Ollama  Qdrant      Ollama embed
    /api/tags /api/chat  REST     /api/embed
                        search    → Qdrant upsert
```

---

## Phase 1: Express Backend (`server/routes/ai.js`)

### Route 1 — GET `/api/ai/models`

Proxies `GET http://ollama:11434/api/tags`. Returns the model list as-is.

**Response shape from Ollama** (`/api/tags`):
```json
{
  "models": [
    { "name": "qwen2.5:7b", "modified_at": "...", "size": 1234567 },
    { "name": "bge-m3:latest", "modified_at": "...", "size": 987654 }
  ]
}
```

### Route 2 — POST `/api/ai/chat` (Streaming)

Ollama `/api/chat` streams **NDJSON** (`application/x-ndjson`) — one JSON object per line, each chunk has `message.content`, stream ends when `done: true`.

The Express proxy must:
1. Set `Content-Type: text/event-stream` so the browser can read it as SSE
2. Set `Cache-Control: no-cache`, `Connection: keep-alive`
3. Call `res.flushHeaders()` immediately
4. Pipe Ollama's NDJSON body line-by-line into `res.write()` as `data: ...\n\n` SSE frames

**Key detail — Caddy SSE buffering:** Without `flush_interval -1`, Caddy buffers the stream and the client sees nothing until the response closes. This is the single most common SSE proxy bug.

### Route 3 — POST `/api/ai/rag/query`

Steps: embed the query with `bge-m3` → POST vector to Qdrant `/collections/{name}/points/search` → return top-k payload as citations.

**Ollama embed endpoint:**
```
POST http://localhost:11434/api/embed
{ "model": "bge-m3:latest", "input": "<query string>" }
→ { "embeddings": [[...1024 floats...]] }
```

**Qdrant search endpoint:**
```
POST http://localhost:6333/collections/{collection}/points/search
{ "vector": [...], "limit": 5, "with_payload": true }
→ { "result": [{ "id": 1, "score": 0.93, "payload": { "text": "...", "source": "..." } }] }
```

### Route 4 — POST `/api/ai/rag/upload`

Uses **multer** to receive a multipart file, extract text, chunk it, embed each chunk, upsert to Qdrant.

---

## Phase 2: React Frontend (`src/ai/AiPanel.tsx`)

### Hash Route — no new dependency required

Hash routing works via `window.location.hash` and `window.addEventListener('hashchange', ...)`. It requires no server-side routing config because the server always sees `/` — only the fragment changes on the client.

**In `App.tsx`** — add one conditional mount:
```tsx
import { useState, useEffect } from 'react';
import AiPanel from './ai/AiPanel';

function App() {
  const [hash, setHash] = useState(window.location.hash);

  useEffect(() => {
    const handleHash = () => setHash(window.location.hash);
    window.addEventListener('hashchange', handleHash);
    return () => window.removeEventListener('hashchange', handleHash);
  }, []);

  return (
    <div className="app">
      {hash === '#ai' && <AiPanel />}
      {hash !== '#ai' && <MainDashboard />}
    </div>
  );
}
```

### `AiPanel.tsx` — Chat + Streaming + Model Selector + Provider Toggle

Full implementation with:
- Streaming chat via `fetch` + `ReadableStream` (NOT EventSource — EventSource only supports GET)
- Live model list from `/api/ai/models`
- Provider toggle: Ollama vs arifOS governed mode
- Auto-scroll to latest message
- Enter-to-send (Shift+Enter for newline)

### RAG Upload Sub-Component

Collapsible section inside `AiPanel.tsx` for uploading `.txt`, `.md`, `.pdf` documents to RAG.

---

## Phase 3: Caddy Configuration

**Critical rule:** `flush_interval -1` is mandatory for the `/chat` route. Without it, Caddy buffers the stream internally and the client sees nothing until the response finishes.

```caddyfile
aaa.arif-fazil.com {
  # ... existing AAA directives ...

  # AI routes — all proxied to Express :3001
  handle /api/ai/* {
    reverse_proxy localhost:3001 {
      flush_interval -1        # required for SSE/streaming
      header_up X-Real-IP {remote_host}
      header_up X-Forwarded-Proto {scheme}
    }
  }
}
```

Reload: `caddy reload --config /etc/caddy/Caddyfile`

---

## Phase 4: Vision / Multimodal

### RAM constraint

The VPS envelope is ~15 GiB RAM.

| Model | Size on disk | Approx RAM needed | Verdict |
|-------|-------------|------------------|---------|
| `qwen2.5:7b` (already running) | ~4.4 GB | ~6–8 GB | ✓ live |
| `bge-m3:latest` (already running) | ~0.6 GB | ~1 GB | ✓ live |
| `gemma3` (4B default) | ~2.6 GB | ~4–5 GB | ✓ safe to add |
| `qwen2.5vl:7b` | ~5–6 GB Q4 | ~10–12 GB | ⚠ risky alongside qwen2.5:7b |

**Recommended sequence:**
1. `ollama pull gemma3` — confirm it runs alongside `qwen2.5:7b` under load
2. Test image input via Ollama `/api/chat` with `images: [base64_string]` field
3. Only then evaluate `qwen2.5vl:7b` — may require offloading `qwen2.5:7b` first

---

## Build Sequence

```
Step 1  git checkout -b feat/ai-panel
Step 2  Add server/routes/ai.js with all four routes
Step 3  Mount router in main Express app (app.use('/api/ai', aiRouter))
Step 4  curl test each route locally
         curl http://localhost:3001/api/ai/models
         curl -N -d '{"model":"qwen2.5:7b","messages":[...]}' \
              -H 'Content-Type: application/json' \
              http://localhost:3001/api/ai/chat
Step 5  Add src/ai/AiPanel.tsx
Step 6  Wire hash route in App.tsx
Step 7  Verify streaming in browser devtools (Network → EventStream)
Step 8  Add flush_interval -1 to Caddyfile, reload caddy
         caddy reload --config /etc/caddy/Caddyfile
Step 9  Test streaming via public URL
Step 10 Add RagUpload component, test /rag/upload + /rag/query
Step 11 Pull gemma3, test vision path
         ollama pull gemma3
```

---

## Error Handling Checklist

- **Stream aborted mid-response:** `req.on('close', () => nodeStream.destroy())` prevents zombie connections
- **Ollama not reachable:** wrap all backend fetches in try/catch, return `{ error: '...', code: 503 }` with HTTP 503
- **Qdrant collection missing on first upload:** add a `PUT /collections/{name}` creation call with vector size 1024 before the first upsert
- **Multer file size limit:** add `limits: { fileSize: 10 * 1024 * 1024 }` to multer config
- **CORS on `/api/ai/*`:** already covered by AAA's existing CORS middleware; no new config needed

---

## Configuration Reference

```env
# server/.env additions
OLLAMA_URL=http://localhost:11434
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=arifos_docs
EMBED_MODEL=bge-m3:latest
```

Qdrant collection bootstrap (run once):
```bash
curl -X PUT http://localhost:6333/collections/arifos_docs \
  -H 'Content-Type: application/json' \
  -d '{
    "vectors": {
      "size": 1024,
      "distance": "Cosine"
    }
  }'
```

> `bge-m3:latest` produces 1024-dimensional dense vectors. The collection must be created with `size: 1024` before the first upsert or Qdrant will reject the request.

---

## What Stays Deferred

| Item | Why deferred |
|------|-------------|
| Open WebUI in public stack | Not needed; AAA panel replaces it for user-facing access |
| `qwen2.5vl:7b` | RAM risk — validate `gemma3` first under concurrent load |
| Citation injection into chat | Can be added post-MVP: call `/rag/query` first, prepend results to `messages` as a system context block |
| Auth on `/api/ai/*` | AAA's existing session/auth middleware applies; no extra gate needed |
| PDF parsing in upload | Out of scope MVP — accept `.txt` and `.md` first |
