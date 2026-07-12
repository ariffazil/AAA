---
id: vps-docker-ops
name: vps-docker-ops
version: 1.0.0
description: "Runbook for VPS Docker operations — compose stack management, live service map, container lifecycle."
owner: AAA
risk_tier: medium
floor_scope: [F1, F2, F8]
autonomy_tier: T2
tags: [docker, vps, runbook, ops, compose]
---

# VPS Docker Operations

## Stack Location
All Docker services run from: `/root/compose/docker-compose.yml`

## Live Service Map (verified 2026-05-15)
```
arifosmcp        :8080   (arifOS MCP — constitutional kernel)
geox_eic         :8081   (GEOX — earth intelligence)
wealth-organ     :8082   (WEALTH — capital intelligence)
well             :8083   (WELL — vitality intelligence)
aaa-a2a          :3001   (AAA — agent gateway)
hermes-agent     :3002   (HERMES — ASI relay)
af-bridge-prod   :7071   (A-FORGE — execution bridge)
vault999         :8100   (VAULT999 — immutable ledger)
vault999-writer  :5001   (VAULT999 Writer — seal API)
postgres         :5432   (PostgreSQL 16)
redis            :6379   (Redis 7)
qdrant           :6333   (Qdrant vector store)
ollama           :11434  (Ollama LLM engine)
uptime-kuma      :8086   (Uptime monitoring)
vaultwarden      :8085   (Self-hosted password manager)
nats             :4222   (NATS messaging)
netdata          :19999  (Netdata system monitoring)
graphiti-mcp     :8000   (Graphiti knowledge graph MCP)
```

## Safe Operations (always run these)

### Check all services
```bash
cd /root/compose && docker compose ps
```

### Check one service health
```bash
docker inspect <service> --format '{{.State.Health.Status}}'
curl -sf http://localhost:<port>/health
```

### View logs
```bash
docker compose -f /root/compose/docker-compose.yml logs --tail=100 <service>
docker compose -f /root/compose/docker-compose.yml logs -f <service>   # live
```

### Restart a service
```bash
docker compose -f /root/compose/docker-compose.yml restart <service>
docker compose -f /root/compose/docker-compose.yml up -d <service>   # rebuild+restart
```

### Restart entire stack
```bash
cd /root/compose && docker compose up -d --remove-orphans
```

### Check resource usage
```bash
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
docker system df
```

### Validate config before deploy
```bash
cd /root/compose && docker compose config
```

## Dangerous Operations (ask ARIF first)

### Disk cleanup
```bash
docker builder prune -f
docker image prune -f
# NEVER: docker system prune -af --volumes  (F1 — irreversible!)
```

### Remove a container
```bash
docker rm -f <container>   # data loss risk!
```

### Remove a volume
```bash
docker volume rm <volume>   # permanent data loss!
```

## Emergency: Service keeps restarting
```bash
docker compose -f /root/compose/docker-compose.yml stop <service>
docker logs <service> --tail 200
# Fix the issue
docker compose -f /root/compose/docker-compose.yml up -d <service>
```

## How to check what changed
```bash
docker diff <container>   # files changed since container start
docker inspect <container> --format '{{json .Config}}' | python3 -m json.tool
```
