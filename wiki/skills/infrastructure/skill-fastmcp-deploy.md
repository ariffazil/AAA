---
title: "SKILL: FastMCP VPS Deployment"
type: skill
version: 1.0.0
category: engineering
risk_band: MEDIUM
floors: [F1]
evidence_required: true
sources: [/root/.opencode/skills/fastmcp-deploy/SKILL.md]
confidence: high
---

# SKILL: FastMCP VPS Deployment

> **Source:** `/root/.opencode/skills/fastmcp-deploy/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- FastMCP server deployment to VPS
- Docker containerization of Python MCP servers
- uvicorn configuration
- Health endpoint setup
- Caddy reverse proxy for MCP endpoints
- Keywords: fastmcp, MCP deployment, python, docker, uvicorn

---

## Dockerfile Template

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

---

## Docker Compose Service Block

```yaml
services:
  fastmcp:
    build: .
    container_name: fastmcp
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      - MCP_HOST=0.0.0.0
      - MCP_PORT=8000
      - LOG_LEVEL=info
    env_file: .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s
    restart: unless-stopped
    networks:
      - caddy_net

networks:
  caddy_net:
    external: true
```

---

## Validation Steps After Deploy

```bash
# 1. Container health
docker inspect fastmcp --format='{{.State.Health.Status}}'

# 2. MCP capabilities endpoint
curl -s http://localhost:8000/mcp/v1/capabilities | jq '.capabilities'

# 3. Tool listing
curl -s -X POST http://localhost:8000/mcp/v1/tools/list \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.tools[].name'

# 4. External via Caddy
curl -sf https://mcp.yourdomain.com/health
```

---

## Common Issues

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| 502 Bad Gateway | FastMCP not running | `docker compose up -d fastmcp` |
| Tool not found | Wrong MCP protocol version | Check FastMCP version |
| CORS error | Browser client blocked | Add CORS middleware |
| Timeout | Worker overloaded | Increase `--workers` or `--timeout-keep-alive` |

---

## Requirements Minimum

```
fastmcp>=0.4.0
uvicorn[standard]>=0.29.0
httpx>=0.27.0
```

---

## Related Pages

- [[skill-mcp-builder]] — building MCP servers
- [[skill-caddy-cloudflare]] — Caddy reverse proxy
- [[skill-vps-docker]] — container lifecycle
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — FastMCP deployed. MCP healthy.*
