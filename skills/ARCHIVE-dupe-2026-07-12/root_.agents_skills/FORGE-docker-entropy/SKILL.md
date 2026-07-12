---
id: docker-entropy-ops
name: FORGE-docker-entropy
version: 1.0.0
description: Thermodynamic reasoning lens for container fleet health, resource pressure,
  and safe/dangerous intervention boundaries.
owner: AAA
risk_tier: medium
knowledge_basis:
  language: true
  math: false
  physics: true
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
dependencies:
  skills: []
  servers: []
  tools: []
examples:
- Inspecting container fleet health before deciding whether to restart a service
- Diagnosing disk entropy with docker system df before any prune
- Classifying a Docker intervention as safe reversible action vs 888 HOLD
tests:
- Diagnose-then-act sequence is followed
- Dangerous operations trigger 888 HOLD
- Scope boundaries are respected (Docker-only, no systemd/K8s/Dockerfile authoring)
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Ω
  functional:
  - Routing
  - Ops
  layer: RUNTIME
  autonomy_tier: T2
floor_scope:
- F1
- F2
- F3
- F8
---

# Docker Entropy Ops

## Overview

Containers are thermodynamic systems: CPU is energy, memory is state, disk is storage, and network is exchange. This skill applies an entropy lens to Docker fleet health so agents distinguish reversible, diagnostic actions from irreversible, dangerous ones. The goal is never to memorize commands — it is to read the thermodynamic state of the fleet and choose the narrowest safe intervention.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

## When to Use

- A Docker container or compose stack appears unhealthy, restarting, or resource-starved.
- Disk pressure, memory pressure, or CPU saturation is suspected on the VPS.
- You need to decide whether to restart, prune, inspect logs, or escalate.
- The task is limited to container lifecycle, logs, health, and resource observation.

## When NOT to Use

- **Do not use** for non-Docker services (systemd-native, bare-metal processes).
- **Do not use** for Kubernetes or Swarm orchestration (not deployed).
- **Do not use** for Docker image authoring, Dockerfile creation, or CI/CD pipeline configuration.
- **Do not use** as authority to run destructive commands without 888 HOLD.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| container/service name | no | Target container or compose service |
| symptom | yes | What is wrong (restart loop, disk full, slow, etc.) |
| compose file path | no | Default `/root/compose/docker-compose.yml` |
| prior prune history | no | When was the last `docker system prune`? |

## Procedure

### Step 1: Read Fleet Entropy

Run these in order before any intervention:

1. `docker ps` — what is running, dead, or restarting?
2. `docker stats --no-stream` — who is consuming CPU/memory?
3. `docker system df` — how much disk entropy (images, volumes, build cache) has accumulated?
4. `docker compose ps` and `docker compose config` if a compose stack is involved.

### Step 2: Interpret Signal Priority

Rank findings in this order:

1. Container health status (Up vs Restarting vs Exited)
2. Memory pressure (approaching limit)
3. Disk entropy (dangling images, volumes, build cache)
4. CPU saturation (sustained >80%)
5. Log anomalies (error rate spikes)

### Step 3: Choose the Intervention Class

**Safe / reversible — proceed with witness:**
- `docker compose config` (validate, no mutation)
- `docker compose ps` (state inspection)
- `docker logs --tail=N <service>` (observation)
- `docker compose restart <service>` (reversible)
- `docker compose up -d <service>` (restore known state)

**Dangerous / irreversible — 888 HOLD required:**
- `docker system prune -af --volumes` (irreversible disk purge)
- `docker rm -f <container>` (data loss risk)
- `docker volume rm <volume>` (permanent data destruction)
- `docker rmi <image>` when the image is actively used

### Step 4: Apply Uncertainty Protocol

- Container is Restarting → read logs before restarting again.
- Disk usage >85% → diagnose before pruning.
- Unsure whether a volume is in use → inspect; do not delete.
- Service unhealthy but cause unclear → 888 HOLD.
- Never prune without first running `docker system df`.

## Allowed Tools

| Tool / Command | Purpose |
|----------------|---------|
| `docker ps` | Fleet state snapshot |
| `docker stats --no-stream` | Resource consumption |
| `docker system df` | Disk entropy inventory |
| `docker logs --tail=N <service>` | Diagnostic observation |
| `docker compose ps` | Compose stack state |
| `docker compose config` | Validate compose configuration |
| `docker compose restart <service>` | Reversible service restart |
| `docker compose up -d <service>` | Restore known-good state |

## Forbidden Actions

- **NEVER** run `docker system prune -af` as a first response to any problem (panic pruning).
- **NEVER** restart a container without reading its logs first.
- **NEVER** assume "container is Up" means "container is healthy".
- **NEVER** ignore disk entropy until it causes system failure.
- **NEVER** delete volumes without verifying they contain no critical data.
- **NEVER** run prune without human confirmation (F1 violation).
- Escalate to **arifOS 888_JUDGE** before any destructive action.

## Output Format

```
## Skill Result: docker-entropy-ops

### Summary
One-paragraph summary of fleet thermodynamic state and chosen intervention.

### Evidence
- Container state: <running / restarting / exited>
- Resource pressure: <CPU / memory / disk findings>
- Disk entropy: <docker system df output>
- Log anomalies: <yes/no with snippet>

### Recommendations
- Safe reversible action, OR
- 888 HOLD with reason and proposed next step

### Escalations
- None / <list>
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Destructive or irreversible Docker action | arifOS 888_JUDGE + Arif | 888 HOLD |
| Data-loss risk (volume/container removal) | arifOS 888_JUDGE | verdict_request |
| Scope creep into systemd/K8s/Dockerfile work | STOP; route to correct skill | A2A message |
| Root cause unclear after diagnosis | arifOS 888_JUDGE | hold with reason |

---

*Skill imported from `/root/.claude/skills/docker-thermodynamics.md` — AAA Skill Library v1.0.0*
