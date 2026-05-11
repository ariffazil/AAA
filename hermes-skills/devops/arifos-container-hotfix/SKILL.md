---
name: arifos-container-hotfix
description: Fix arifOS MCP container bugs that survive restarts — source file changes vs image rebuilds
tags: [arifOS, docker, hotfix, container]
version: 2026-05-06
---

# arifOS Container Hotfix Pattern

## When to Use
When you need to fix a bug in a running arifOS MCP container (`arifosmcp`) and the fix involves changing Python source files in `/root/arifOS/`.

## The Core Problem
The `arifosmcp` container is built from image `af-forge-arifosmcp:latest`. When the container restarts via `docker stop + docker rm + docker run`, Docker reloads the **original image layers** — any files you modified via `docker cp` are wiped out.

**Source file changes alone do NOT survive container restarts.**

## The Rule
For any fix to survive permanently, rebuild the image:
```bash
cd /root/arifOS
docker build -f Dockerfile -t ghcr.io/ariffazil/arifos:<new-tag> .
docker push ghcr.io/ariffazil/arifos:<new-tag>
```

## Hotfix Workflow (Temporary — Dev Only)

### Step 1: Apply the file fix
```bash
docker cp /root/arifOS/arifosmcp/runtime/tools.py arifosmcp:/app/arifosmcp/runtime/tools.py
docker cp /root/arifOS/arifosmcp/tool_manifest.py arifosmcp:/app/arifosmcp/tool_manifest.py
```

### Step 2: Restart WITHOUT recreating
```bash
# Use restart — NOT stop + rm + run (that wipes changes)
docker restart arifosmcp
```

### Step 3: Verify
```bash
docker exec arifosmcp grep -n "def _arif_memory_recall" /app/arifosmcp/runtime/tools.py | head -3
```

## Container Networking
Must be on `af-forge_arifos-network` to reach federation containers:
```bash
docker network connect af-forge_arifos-network arifosmcp
```

Key endpoints from inside `arifosmcp`:
- Qdrant: `http://qdrant:6333`
- Ollama: `http://ollama-engine-prod:11434`
- Postgres: `postgresql://arifos_admin:ArifPostgres2026!@postgres:5432/vault999`

## Environment Variables (Standalone Run)
When starting outside docker-compose, pass explicitly:
```bash
docker run -d \
  --name arifosmcp \
  --network af-forge_arifos-network \
  -p 8080:8080 \
  -e DATABASE_URL="postgresql://arifos_admin:ArifPostgres2026!@postgres:5432/vault999" \
  -e POSTGRES_URL="postgresql://arifos_admin:ArifPostgres2026!@postgres:5432/vault999" \
  -e QDRANT_URL="http://qdrant:6333" \
  -e OLLAMA_URL="http://ollama-engine-prod:11434" \
  af-forge-arifosmcp:latest
```

## MCP HTTP Testing (from inside container)
```python
import httpx, json
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

r = httpx.post('http://127.0.0.1:8080/mcp',
    json={'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
          'params': {'name': 'arif_session_init', 'arguments': {'actor_id': 'hermes-agent'}}},
    headers=headers, timeout=10)
session_id = json.loads(r.json()['result']['content'][0]['text'])
session_id = session_id.get('result', {}).get('session', {}).get('session_id', '')

r = httpx.post('http://127.0.0.1:8080/mcp',
    json={'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
          'params': {'name': 'arif_memory_recall', 'arguments': {
              'mode': 'store', 'session_id': session_id, 'actor_id': 'hermes-agent',
              'content': '...', 'project_id': '...', 'area': '...'}}},
    headers=headers, timeout=15)
print(json.loads(r.json()['result']['content'][0]['text']))
```

## Verified Working Config (2026-05-06)
- Image: `af-forge-arifosmcp:latest`
- Network: `af-forge_arifos-network`
- Qdrant: `http://qdrant:6333` (IP `172.20.0.2`)
- Ollama: `http://ollama-engine-prod:11434` (IP `172.19.0.7`)
- Postgres: `postgres:5432/vault999`, user `arifos_admin`, pw `ArifPostgres2026!`
- MCP transport: streamable-http on port 8080
