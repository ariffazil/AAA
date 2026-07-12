---
id: docker-thermodynamics
name: docker-thermodynamics
version: 1.0.0
description: "Cognitive lens: containers as thermodynamic/entropy systems — resource pressure, safe intervention boundaries."
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F8]
autonomy_tier: T1
tags: [docker, thermodynamics, entropy, cognitive-lens]
---

# Docker Thermodynamics

## REASONING PHILOSOPHY

Docker containers are not black boxes — they are thermodynamic systems. Each container consumes CPU (energy), memory (state), disk (storage), and network (exchange). Think of container management as entropy management: every action either reduces chaos (diagnosis, restart, prune) or increases it (untracked modifications, accumulated artifacts, unmonitored services).

The goal is not to memorize Docker commands — it is to understand the thermodynamic state of the container fleet. Is entropy rising? Are resources bottlenecking? Is data at risk of irreversible loss?

## DECISION HEURISTICS

**Diagnose before acting:**
1. `docker ps` — what is running, what is dead?
2. `docker stats --no-stream` — who is consuming resources?
3. `docker system df` — how much disk entropy has accumulated?
4. Only after diagnosis: decide the intervention

**Safe operations (proceed without ask):**
- `docker compose config` (validate, no mutation)
- `docker compose ps` (state inspection)
- `docker logs --tail=N <service>` (observation)
- `docker compose restart <service>` (reversible)
- `docker compose up -d <service>` (restore known state)

**Dangerous operations (888 HOLD required):**
- `docker system prune -af --volumes` (irreversible disk purge)
- `docker rm -f <container>` (data loss risk)
- `docker volume rm <volume>` (permanent data destruction)
- `docker rmi <image>` if image is actively used

## SIGNAL PRIORITY

1. Container health status (Up vs Restarting vs Exited)
2. Memory pressure (approaching limit)
3. Disk entropy (dangling images, volumes, build cache)
4. CPU saturation (sustained >80%)
5. Log anomalies (error rate spikes)

## UNCERTAINTY PROTOCOL

- If container is Restarting → check logs before restarting again
- If disk usage >85% → diagnose before pruning
- If unsure whether a volume is in use → inspect, do not delete
- If a service is unhealthy but the cause is unclear → 888 HOLD
- Never prune without first running `docker system df` to understand what will be lost

## FAILURE MODE REGISTRY

**These are specific errors. Actively avoid them:**
- `docker system prune -af` as first response to any problem (panic pruning)
- Restarting a container without reading logs first (masking the root cause)
- Assuming "container is Up" means "container is healthy"
- Ignoring disk entropy until it causes system failure
- Deleting volumes without verifying they contain no critical data
- Running prune without human confirmation (F1 violation)

## SCOPE BOUNDARIES

**Applies to:**
- All Docker containers on the arifOS VPS
- Compose stack at `/root/compose/docker-compose.yml`
- Container lifecycle: start, stop, restart, logs, health, pruning

**Does NOT apply to:**
- Non-Docker services (systemd-native, bare metal)
- Kubernetes or Swarm orchestration (not used)
- Docker image authoring or Dockerfile creation
- CI/CD pipeline configuration
