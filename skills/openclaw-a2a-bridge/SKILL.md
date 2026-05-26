---
id: openclaw-a2a-bridge
name: OpenClaw A2A Bridge
version: "0.1.0"
description: Governed A2A bridge skill for OpenClaw-facing handoff and dispatch. Legacy skill — retained for workflow compatibility.
owner: AAA
risk_tier: medium
knowledge_basis:
  physics: false
  math: true
  language: true
host_compatibility:
  - openclaw-gateway
  - claude-code
  - codex
  - copilot-cli
dependencies:
  skills: []
  servers:
    - arifos-mcp
  tools:
    - agent-dispatch
    - agent-handoff
    - status-query
examples:
  - OpenClaw-to-AAA gateway handoff
tests:
  - Bridge responds to health probe
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# OpenClaw A2A Bridge

## Overview

This skill governs handoff between the OpenClaw gateway and AAA federation agents. It is retained for backward compatibility with existing workflows.

## When to Use

- OpenClaw agent requests federation task dispatch
- OpenClaw agent needs to hand off to GEOX/WEALTH/WELL witness

## Escalation Path

| Condition | Escalate To |
|-----------|-------------|
| Bridge failure | AAA agent |
| Unauthorized dispatch | arifOS 888_JUDGE |

---

*Skill version 0.1.0 — AAA Skill Library (legacy)*
