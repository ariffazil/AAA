# Deployment — AAA (Intelligence Routing & State Plane)

## Prerequisites

- Docker 24+ and Docker Compose v2
- 4 CPU cores, 8GB RAM (AAA runs the FLAME multi-model router)
- Ports: `3001` (AAA organ), `18901` (FLAME router)

## Quick Start

```bash
git clone https://github.com/arif-fazil/AAA.git
cd AAA
docker compose up -d

# Verify
curl http://localhost:3001/health
curl http://localhost:18901/health/liveliness
```

## Docker Compose

```yaml
services:
  aaa-organ:
    image: arifazil/aaa-organ:latest
    ports:
      - "3001:3001"
    environment:
      - AAA_SKILL_PATH=/var/lib/aaa/skills
      - FLAME_ROUTER_URL=http://localhost:18901
    restart: unless-stopped

  flame-router:
    image: arifazil/flame-router:latest
    ports:
      - "18901:18901"
    environment:
      - FLAME_MODEL_CONFIG=/etc/flame/models.yaml
    restart: unless-stopped
```

## Configuration

AAA requires:
- FLAME router model configuration (provider URLs, API keys, fallback chains)
- Skill catalog directory (200+ skills)
- State plane storage (Redis or in-memory)

## Federation Role

AAA must be deployed after arifOS kernel but before execution organs. It routes
all user intents to the appropriate organ.

## Health Checks

| Endpoint | Description |
|----------|-------------|
| `GET /health` | AAA organ liveness |
| `GET /health/skills` | Skill catalog status |
| `GET /health/liveliness` | FLAME router (no auth) |
