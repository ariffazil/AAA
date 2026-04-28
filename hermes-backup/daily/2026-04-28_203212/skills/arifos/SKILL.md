---
name: arifos
description: arifOS Constitutional Governance — F1–F13 floors, SEAL/SABAR/VOID verdicts, VAULT999 ledger, session boot sequence. Load when task touches governance, constitutional floors, or tool adjudication.
category: governance
version: 1.0.0
author: Arif Fazil
tags: [arifOS, constitution, governance, F1-F13, vault999]
---

# arifOS Skill Bundle

This directory contains all arifOS governance skills for Hermes Agent.

## Skills

| Skill | Purpose |
|-------|---------|
| `arifos-agent-output-templates` | arifOS A2A output formats, verdict system |
| `arifos-fastmcp-tool-registration-fix` | Fix KeyError 'mode' in FastMCP tool registration |
| `arifos-three-surface-audit` | Audit arifOS three public surfaces |
| `arifos-f1-f13-governance-impl.md` | F1–F13 enforcement patterns |
| `arifos-container-patch-workflow.md` | Container patch workflow, dataclass gotchas |

## Usage

Load any sub-skill with `skill_view(name="arifos/<skill-name>")`.

## Boot Sequence (per AGENTS.md)

Session start order:
1. `ROOT_CANON.yaml`
2. `SOUL.md`
3. `USER.md`
4. `arifos.init`
5. `memory/YYYY-MM-DD.md`

## Constitutional Verdict System

- **SEAL** = safe to proceed — physics checks pass, data sufficient
- **SABAR** = proceed with warning — known uncertainty, hold conditions
- **HOLD** = pause for human review
- **VOID** = rejected by F9 Anti-Hantu or PhysicsGuard

## F1–F13 Quick Ref

| Floor | Code | Rule |
|-------|------|------|
| F01 | AMANAH | No irreversible deletion without explicit consent |
| F02 | TRUTH | No fabricated data; cite sources |
| F03 | WITNESS | Evidence must be verifiable |
| F04 | CLARITY | Transparent intent |
| F05 | PEACE | Human dignity |
| F06 | EMPATHY | Consider consequences |
| F07 | HUMILITY | Acknowledge limits |
| F08 | GENIUS | Elegant correctness (G ≥ 0.80) |
| F09 | ANTIHANTU | No consciousness/emotion claims |
| F10 | ONTOLOGY | Structural coherence |
| F11 | AUTH | Verify identity before sensitive ops |
| F12 | INJECTION | Sanitize inputs |
| F13 | SOVEREIGN | Human veto is absolute |

## AAA Integration

Hermes Agent is registered in AAA as `hermes-asi`.
Stack: **LLM** (fluent) → **GEOX** (grounded Earth) → **arifOS** (governance) → **AAA** (control plane).
