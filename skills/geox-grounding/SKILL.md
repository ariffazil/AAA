---
id: geox-grounding
name: GEOX Grounding
version: "0.1.0"
description: Force Earth-sensitive reasoning through GEOX witness paths. Ensure geological claims are grounded in evidence.
owner: AAA
risk_tier: medium
knowledge_basis:
  physics: true
  math: true
  language: true
host_compatibility:
  - openclaw-gateway
  - claude-code
dependencies:
  skills: []
  servers:
    - geox-mcp
  tools:
    - geox-query
examples:
  - Validate subsurface claim against GEOX well data
tests:
  - GEOX witness responds with evidence
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# GEOX Grounding

## Overview

When an agent makes a claim about geology, petrophysics, or subsurface properties, this skill routes the claim through GEOX for evidence-based validation.

## When to Use

- Any claim involving earth science
- Before accepting geological recommendations
- When comparing multiple geological interpretations

## Escalation Path

| Condition | Escalate To |
|-----------|-------------|
| GEOX witness unavailable | AAA agent (reroute to backup) |
| Conflicting geological evidence | Arif (human expert judgment) |

---

*Skill version 0.1.0 — AAA Skill Library*
