---
id: openclaw-a2a-bridge
name: OpenClaw A2A Bridge
version: 0.1.0
description: Governed A2A bridge skill for OpenClaw-facing handoff and dispatch. Legacy
  skill — retained for workflow compatibility.
owner: AAA
risk_tier: medium
maturity: deprecated
status: deprecated
superseded_by: mcp-federation-ops
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- openclaw-gateway
- claude-code
- codex
- copilot-cli
- opencode
- kimi
- kimi-code
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
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Δ
  - Ω
  functional:
  - Routing
  layer: RUNTIME
  autonomy_tier: T2
floor_scope:
- F2
- F3
- F4
- F11
---

# OpenClaw A2A Bridge

> **DEPRECATED** — This skill has been superseded by `mcp-federation-ops`. Use that skill instead.

## Overview

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


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