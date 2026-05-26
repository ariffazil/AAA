---
id: service-health-triage
name: Federation Service Health Triage
version: "1.0.0"
description: Diagnose which federation services are up, down, or drifting. Produce a prioritized remediation plan.
owner: AAA
risk_tier: low
knowledge_basis:
  physics: false
  math: false
  language: true
host_compatibility:
  - claude-code
  - codex
  - opencode
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
  schema_version: "1"
  artifact_hash: pending
---

# Federation Service Health Triage

## Overview

The federation runs on a mix of systemd services and Docker containers. This skill checks all of them and produces a clear health report.

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
| GEOX | systemd | 18081 | active |
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

## Escalation Path

| Condition | Escalate To |
|-----------|-------------|
| arifOS down | ops.agent + Arif |
| Multiple organs down | A-FORGE agent (deployment issue) |
| Port mismatch | AAA agent (registry update needed) |

---

*Skill version 1.0.0 — AAA Skill Library*
