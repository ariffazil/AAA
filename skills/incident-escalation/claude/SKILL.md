---
id: incident-escalation
name: Incident Escalation Protocol
version: "1.0.0"
description: "Standard protocol for responding to federation incidents: service outages, security breaches, constitutional violations, or agent misbehavior."
owner: AAA
risk_tier: critical
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
    - service-health-triage
    - secret-safety-scan
  servers: []
  tools:
    - health-probe
    - telegram-send
    - a2a-message
examples:
  - Hermes agent starts sending unauthorized messages
tests:
  - Verify escalation reaches Arif within 60 seconds for critical incidents
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# Incident Escalation Protocol

## Overview

When something goes wrong in the federation, speed and clarity matter. This skill provides the canonical escalation ladder.

## Incident Severity

| Level | Name | Examples | Response Time |
|-------|------|----------|---------------|
| 1 | info | Minor drift, stale docs | Next business day |
| 2 | warning | Service slow, test flaky | 4 hours |
| 3 | error | Service down, agent confused | 1 hour |
| 4 | critical | Security breach, data loss, constitutional violation | 15 minutes |
| 5 | emergency | Active attack, irreversible damage in progress | Immediate |

## Escalation Ladder

```
Agent detects incident
    ↓
Agent applies skill (if trained)
    ↓
Escalate to domain agent (GEOX/WEALTH/WELL/A-FORGE)
    ↓
Escalate to AAA control plane (routing + visibility)
    ↓
Escalate to arifOS 888_JUDGE (constitutional / irreversible)
    ↓
Escalate to Arif (human sovereign)
```

## Procedure

### Step 1: Detect and Classify

Determine severity level. When in doubt, escalate one level higher.

### Step 2: Contain

- Stop the bleeding (restart service, revoke token, disable agent)
- Do NOT destroy evidence
- Document timestamp and initial observations

### Step 3: Notify

| Level | Notify |
|-------|--------|
| 1-2 | Log + dashboard |
| 3 | Domain agent + AAA |
| 4 | arifOS judge + Arif (Telegram) |
| 5 | Arif immediately + all agents |

### Step 4: Investigate

Use appropriate skills:
- Service down → `service-health-triage`
- Secret leaked → `secret-safety-scan`
- Agent misbehaving → `agent-onboarding` (re-read SOUL.md)
- Constitutional violation → `parallel-authority-detection`

### Step 5: Resolve and Document

- Fix root cause
- Update runbooks
- TREE777 audit to prevent recurrence

## Forbidden Actions

- **NEVER** cover up an incident
- **NEVER** delay escalation to avoid "bothering" someone
- **NEVER** destroy logs or evidence
- **NEVER** restart a service without understanding why it failed

---

*Skill version 1.0.0 — AAA Skill Library*
