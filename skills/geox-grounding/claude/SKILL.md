---
id: geox-grounding
name: GEOX Grounding
version: 0.1.0
description: Force Earth-sensitive reasoning through GEOX witness paths. Ensure geological
  claims are grounded in evidence.
owner: AAA
risk_tier: medium
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- openclaw-gateway
- claude-code
- codex
- opencode
- kimi
- kimi-code
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
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Δ
  functional:
  - Evidence
  layer: HEXAGON
  autonomy_tier: T2
floor_scope:
- F2
- F7
- F9
---

# GEOX Grounding

## Overview

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


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