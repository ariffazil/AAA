---
title: "SKILL: Agent Zero Operations"
type: skill
version: 1.0.0
category: infra
risk_band: MEDIUM
floors: [F1, F11]
evidence_required: true
sources: [/root/.opencode/skills/agent-zero/SKILL.md]
confidence: high
---

# SKILL: Agent Zero Operations

> **Source:** `/root/.opencode/skills/agent-zero/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Delegating to Agent Zero from A-FORGE
- Browser automation tasks
- Document creation via agent-zero
- Web research via SearXNG
- Model switching (OpenRouter, DeepSeek, Ollama)
- Keywords: agent-zero, browser automation, document creation, delegation

---

## What Agent Zero Is

**Docker-isolated autonomous agent workbench** on the VPS:
- Kali Linux Docker container with full terminal access
- LiteLLM multi-provider LLM routing (OpenRouter, DeepSeek, Ollama)
- Built-in Playwright browser, SearXNG search
- REST API on port 80 (Flask), WebSocket for streaming
- MCP server on port 9000 (currently disabled)

---

## Current Deployment

| Property | Value |
|----------|-------|
| Container | `agent-zero` |
| Image | `agent0ai/agent-zero:latest` (12GB Kali) |
| Host port | `127.0.0.1:50001` → container `:80` |
| WebUI | `https://ai.arif-fazil.com/` |
| API base | `https://ai.arif-fazil.com/api/` |
| API token | `jPU8o7B0zxjgAOGz` |

---

## API Reference

### Send Task (Primary Interface)

```bash
curl -X POST https://ai.arif-fazil.com/api/api_message \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: jPU8o7B0zxjgAOGz" \
  -d '{
    "message": "Your task here",
    "lifetime_hours": 1,
    "project_name": "optional-project"
  }'
```

### Key Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/api_message` | Send task to Agent Zero |
| GET | `/api/health` | Health check |
| GET | `/api/agents` | List agent profiles |
| GET | `/api/chats` | List chat sessions |
| WS | `/ws` | Real-time streaming |

---

## A-FORGE Integration

A-FORGE delegates via `AgentZeroTool.ts` → `POST /api/api_message`:

| Tool | Purpose | Endpoint |
|------|---------|----------|
| `agent_zero_delegate` | General task delegation | `/api/api_message` |
| `agent_zero_browser` | Browser automation | `/api/api_message` |
| `agent_zero_document` | Document creation | `/api/api_message` |

---

## Docker Operations

```bash
# Restart
docker restart agent-zero
sleep 15

# View logs
docker logs --tail 50 agent-zero
docker logs -f agent-zero

# Access shell
docker exec -it agent-zero /bin/bash

# Check volume mounts
docker inspect agent-zero --format '{{range .Mounts}}{{.Type}} {{.Source}} → {{.Destination}}{{"\n"}}{{end}}'
```

---

## Known Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| "No cookie auth credentials" 401 | settings.json regenerated, key stripped | Update `.env` with key, restart |
| DeepSeek 402 | Insufficient balance | Remove DeepSeek key or switch to OpenRouter |
| LiteLLM 400 | Array vs object bug | `pip install "litellm>=1.50.0"` |
| settings.json resets on restart | Expected behavior | Edit `/a0/usr/.env`, not settings.json |

---

## Security Notes

| Risk | Mitigation |
|------|-------------|
| API token exposed | Use `localhost:50001` only; Caddy proxies with HTTPS |
| API key in .env | Inside Docker volume; not committed to git |
| Agent executes code | Isolated Kali container; no host access |

---

## Related Pages

- [[federation-entities]] — Agent Zero in federation
- [[skill-arifos-operator]] — A-FORGE integration
- [[concept-tools-and-embodiment]] — Agent Zero as soft embodiment
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Agent Zero delegated. Task in motion.*
