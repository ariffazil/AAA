# hermes-agent Docker Compose Wiring (arifOS Federation)

## The Problem

The `hermes-agent` container cannot resolve host-level paths like `~/.hermes/` or `/root/AAA/.hermes/` from inside Docker. If `.env` is not explicitly mounted or referenced via `env_file:`, the container runs with empty defaults for all provider API keys, Redis URLs, and Ollama endpoints.

**Symptoms:**
- `docker exec hermes-agent sh -c 'env | grep REDIS'` returns empty
- `hermes doctor` inside container shows Redis unreachable + all provider keys missing
- The container appears healthy (`docker ps` shows (healthy)) but the agent has no credentials

## Working Configuration (arifOS Federation)

File: `/root/compose/docker-compose.yml`

```yaml
hermes-agent:
    image: hermes-agent:v1.0.3
    container_name: hermes-agent
    init: true
    restart: unless-stopped
    command: ["node", "src/server.js"]
    env_file:
      - /root/AAA/.hermes/.env
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - arifos_core_network
    labels:
      - "arifOS.federation=hermes"
```

Key env vars that must be in `/root/AAA/.hermes/.env`:
```
REDIS_URL=redis://redis:6379/1
OLLAMA_BASE_URL=http://ollama-engine-prod:11434/v1
MINIMAX_API_KEY=...
OPENROUTER_API_KEY=...
DEEPSEEK_API_KEY=...
HF_TOKEN=...
A2A_TOKEN=...
```

## Diagnostic Chain

```bash
# 1. Check what's actually IN the container's env
docker exec hermes-agent sh -c 'env | sort'

# 2. If empty → container not getting .env
docker exec hermes-agent sh -c 'echo "REDIS_URL=$REDIS_URL"; echo "OLLAMA=$OLLAMA_BASE_URL"'

# 3. Check docker-compose env_file directive
grep -A5 "hermes-agent:" /root/compose/docker-compose.yml

# 4. Test Redis from inside container
docker exec hermes-agent nc -zv redis 6379 -w 2

# 5. Test Ollama from inside container
docker exec hermes-agent curl -s http://ollama-engine-prod:11434/api/tags
```

## If env_file Is Missing (No Credentials Injected)

Patch docker-compose.yml:
```yaml
hermes-agent:
    env_file:
      - /root/AAA/.hermes/.env
```

Then recreate the container:
```bash
docker stop hermes-agent && docker rm hermes-agent
cd /root/compose && docker compose up -d hermes-agent
```

Verify:
```bash
sleep 3 && docker exec hermes-agent sh -c 'echo "OLLAMA=$OLLAMA_BASE_URL"; echo "REDIS=$REDIS_URL"'
```

## Network Connectivity

The `hermes-agent` container must be on `arifos_core_network` to reach:
- Redis: `redis://redis:6379/1` (container name `redis`)
- Ollama: `http://ollama-engine-prod:11434/v1` (container name `ollama-engine-prod`)
- arifOS MCP: `http://arifosmcp:8080` (container name `arifosmcp`)

```bash
docker network inspect arifos_core_network --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{"\n"}}{{end}}'
```

## Cron Job Script Path Gotcha

The WEALTH briefing script at `/root/.local/bin/wealth_daily_briefing.py` uses relative output paths. When run via cron with `hermes cron`, the working directory is `/root`, so relative script paths like `scripts/wealth_daily_briefing.py` fail.

**Fix:** Always use absolute paths in cron job prompts:
```
python3 /root/.local/bin/wealth_daily_briefing.py
```

Script output goes to `/root/arif-sites/sites/arif-fazil.com/public/data/wealth/` (not `.local/`).

## Related Skills
- `hermes-circular-dependency-recovery` — when venv deletion breaks hermes tools
- `hermes-primary-provider-failover` — when upstream auth breaks Telegram replies
- `hermes-telegram-full-listen-config` — Telegram group listen mode
- `vps-live-probe-audit` — full system audit including hermes-agent
