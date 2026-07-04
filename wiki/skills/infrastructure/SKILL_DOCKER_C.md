---
title: "SKILL: Docker Thermodynamics"
type: skill
version: 1.0.0
category: infra
risk_band: MEDIUM
floors: [F1, F2, F8]
evidence_required: true
sources: [/root/.opencode/skills/docker-thermodynamics/SKILL.md]
confidence: high
---

# SKILL: Docker Thermodynamics

> **DITEMPA BUKAN DIBERI — Containers are thermodynamic systems.**
> **Source:** `/root/.opencode/skills/docker-thermodynamics/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Managing Docker containers, diagnosing unhealthy services
- Investigating resource bottlenecks, disk pressure
- Planning container restart, pruning, or removal
- Keywords: docker, container, compose, restart, logs, prune, disk, memory, CPU

---

## Reasoning Philosophy

Containers are **thermodynamic systems** — they consume CPU (energy), memory (state), disk (storage), and network (exchange). Every action either:
- **Reduces chaos** (diagnosis, restart, prune)
- **Increases entropy** (untracked modifications, accumulated artifacts)

The goal: maintain entropy balance — not memorize commands.

---

## Diagnostic Sequence (Always First)

Before any Docker action:

```bash
# 1. What is running, what is dead?
docker ps -a

# 2. Who is consuming resources?
docker stats --no-stream

# 3. How much disk entropy accumulated?
docker system df

# Only after diagnosis: decide intervention
```

---

## Safe Operations (Proceed Without Ask)

- `docker compose config` (validate, no mutation)
- `docker compose ps` (state inspection)
- `docker logs --tail=N <service>` (observation)
- `docker compose restart <service>` (reversible)
- `docker compose up -d <service>` (restore known state)

---

## Dangerous Operations (888_HOLD Required)

- `docker system prune -af --volumes` (irreversible disk purge)
- `docker rm -f <container>` (data loss risk)
- `docker volume rm <volume>` (permanent data destruction)
- `docker rmi <image>` if image is actively used

---

## Signal Priority

1. Container health status (Up vs Restarting vs Exited)
2. Memory pressure (approaching limit)
3. Disk entropy (dangling images, volumes, build cache)
4. CPU saturation (sustained >80%)
5. Log anomalies (error rate spikes)

---

## Uncertainty Protocol

- Container Restarting → check logs before restarting again
- Disk usage >85% → diagnose before pruning
- Unsure whether volume is in use → inspect, do not delete
- Service unhealthy but cause unclear → 888_HOLD
- Never prune without `docker system df` first (F1 violation)

---

## Failure Mode Registry

Actively avoid:
- `docker system prune -af` as first response (panic pruning)
- Restarting without reading logs first (masking root cause)
- Assuming "container is Up" = "container is healthy"
- Ignoring disk entropy until system failure
- Deleting volumes without verifying they contain no critical data
- Running prune without human confirmation (F1 violation)

---

## Related Pages

- [[skill-vps-docker]] — container lifecycle management
- [[skill-docker-security]] — hardening and port audits
- [[skill-vps-audit]] — full system audit including Docker
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Entropy management over command memorization.*
