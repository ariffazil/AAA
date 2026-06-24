---
id: service-health-triage
name: Federation Service Health Triage
version: 1.0.1
description: Diagnose which federation services are up, down, or drifting. Produce
  a prioritized remediation plan.
owner: AAA
risk_tier: medium
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
dependencies:
  skills:
  - mcp-smoke-test
  servers: []
  tools:
  - health-probe
  - systemctl-status
  - docker-ps
examples:
- Morning federation status check
tests:
- Detect mismatch between systemd claims and actual ports
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Δ
  functional:
  - Ops
  layer: RUNTIME
  autonomy_tier: T2
floor_scope:
- F2
- F3
- F11
---

# Federation Service Health Triage

## Overview

The federation runs on a mix of systemd services and Docker containers. This skill checks all of them and produces a clear health report.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

## When to Use

- Morning status brief
- After any deployment
- When an agent reports a service is unreachable
- Before restarting any service

## Canonical Federation Services

| Service | Type | Port | Expected State |
|---------|------|------|----------------|
| arifos | systemd | 8088 | active |
| arifosd | systemd | — | active |
| caddy | systemd | 80/443 | active |
| hermes-asi-gateway | systemd | — | active |
| ollama | systemd | 11434 | active |
| vault999-api | systemd | 8100 | active |
| vault999-writer | systemd | 5001 | active |
| GEOX | systemd | 8081 | active |
| WEALTH | systemd | 18082 | active |
| WELL | systemd | 18083 | active |
| A-FORGE | systemd | 7071 | active |

## Procedure

### Step 1: systemd Check

Run `systemctl status <service>` for each. Record: active/inactive/failed.

### Step 2: Port Check

Run `ss -tlnp` or `curl` to verify each port is actually listening.

### Step 3: Docker Check

Run `docker compose ps` in `/root/compose`. Record running/stopped.

### Step 4: Cross-Reference

Compare systemd claims vs actual ports vs Docker reality. Flag discrepancies.

### Step 5: Report

## Drift Detection

A service running is not necessarily running what you think. Compare each organ's source repository HEAD with the artifact actually deployed.

| Organ | Source | Runtime SHA Location |
|-------|--------|----------------------|
| arifOS | `/root/arifOS` | `/opt/arifos/app/.git_commit` |
| GEOX | `/root/geox` | Docker compose image / container |
| WEALTH | `/root/WEALTH` | systemd unit `ExecStart` path |
| WELL | `/root/WELL` | systemd unit `ExecStart` path |
| A-FORGE | `/root/A-FORGE` | `dist/` + systemd unit |
| AAA | `/root/AAA` | static build served by Caddy |
| APEX | `/root/APEX` | systemd unit `ExecStart` path |

Steps:
1. `git -C /root/<organ> rev-parse HEAD` → source SHA.
2. Read the runtime SHA (`.git_commit`, container digest, or `systemctl cat <unit>`).
3. Compare. Mismatch → DRIFT.
4. If source is newer → candidate for `make deploy-local` in that organ.
5. If runtime is newer → runtime patch not in source → **888 HOLD**.
6. Also spot-check `/etc/caddy/Caddyfile` and relevant env/secrets for runtime-only changes.

Verification loop:
- Match → no action.
- Source newer → log both SHAs and recommend deploy.
- Runtime newer → 888 HOLD with both SHAs.
- Missing runtime SHA → warn; treat source as truth and surface to human.

## Runtime Verification

`systemctl active` only proves the unit started. Prove each organ actually behaves.

Steps:
1. Run `/root/apex-health.sh` for a federation-wide port probe.
2. Hit each organ's `/health` endpoint:
   - arifOS: `curl -s :8088/health | jq`
   - GEOX: `curl -s :8081/health | jq`
   - WEALTH: `curl -s :18082/health | jq`
   - WELL: `curl -s :18083/health | jq`
   - A-FORGE: `curl -s :7071/health | jq`
   - APEX: `curl -s :3002/health | jq`
3. Run one behavior smoke per touched organ (e.g., `arif_session_init` round-trip for arifOS).
4. Run the Drift Detection check above.
5. Report green/yellow/red per organ with a one-line summary.

Verification loop:
- All green → claim done.
- Yellow → log and continue; flag in summary.
- Red → 888 HOLD; consider rollback via the organ runbook.

Failure modes:
- Service slow to start → 30s grace, then red.
- Port collision → check Caddyfile drift; surface to human.
- Missing `/health` route → inspect the organ's `main.py` / `server.js`.

Reference:
- `/root/RUNBOOK.md`
- `/root/arifOS/deploy/RUNBOOK.md`

## Escalation Path

| Condition | Escalate To |
|-----------|-------------|
| arifOS down | ops.agent + Arif |
| Multiple organs down | A-FORGE agent (deployment issue) |
| Port mismatch | AAA agent (registry update needed) |

---

*Skill version 1.0.1 — AAA Skill Library*
