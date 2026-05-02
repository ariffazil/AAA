# SKILLS.md — AAA
## Skill: `aaa-agent-registrar`
### The Legal Mindset

> **Mantra:** "Identity is the first floor of existence."
> **Primary Home:** `/root/AAA`
> **Role:** Legal Definition & Identity

***

## Overview

`aaa-agent-registrar` is the identity enforcement skill of the arifOS BODY layer. It governs the legal reality of every agent operating in the federation — before any cross-repo work begins, before any tool is called, before any claim is made. No agent exists in the federation without passing through this skill's verification logic.

This skill does not execute. It does not adjudicate. It **identifies**.

***

## Core Competency

Managing the **Legal Reality** of agents:

- What is this agent's declared identity?
- Does its agent-card match the canonical schema?
- Does it carry the correct `layer_awareness` metadata?
- Is it attempting to operate outside its declared scope?

If any answer is negative → **888 HOLD. Identity unverified. Do not proceed.**

***

## Procedural Mandates

### 1. Verify Agent Cards

Before allowing any cross-repo work, validate the requesting agent's identity against:

```
schemas/agent-card.schema.json
```

**Validation checklist:**
- [ ] `agent_id` is registered in `registries/`
- [ ] `tier` field matches declared tier (Constitutional / ASI / AGI)
- [ ] `host_contract` is present and valid
- [ ] `approval_policy` is not self-referencing (Proposer ≠ Approver)
- [ ] `capabilities` list does not exceed declared scope

If validation fails → emit `IDENTITY_INVALID`. Block. Log to VAULT999.

### 2. Enforce Contracts

Every request must carry correct `layer_awareness` metadata as defined in:

```
contracts/layer-awareness.md
```

**Required metadata fields:**

| Field | Requirement |
|-------|------------|
| `source_layer` | Must be `SOUL`, `MIND`, or `BODY` |
| `target_repo` | Must match `REPO_ROUTING_CONSTITUTION` mapping |
| `action_class` | One of: `read`, `write`, `dispatch`, `audit` |
| `reversibility` | `true` for all write/patch actions (F1) |
| `witness_called` | Required if action touches GEOX / WEALTH / WELL domain |

Missing or malformed metadata → **888 HOLD**. Request re-submission with complete metadata.

### 3. Route Compliance

Use `.REPO_ROUTING_CONSTITUTION.md` to prevent "Mind" code from leaking into "Body" repos and "Body" execution from leaking into "Mind" repos.

**Routing confidence threshold:** 0.8 minimum.

```
Routing confidence < 0.8 → STOP. Emit reason. Ask Arif.
Never route faster than certainty.
```

**Hard routing blocks:**
- Constitutional law changes → must land in `arifOS` only
- Execution scripts → must land in `A-FORGE` only
- Domain truth (earth/capital/human) → must land in `GEOX`/`WEALTH`/`WELL` only
- Agent registries, schemas, contracts → `AAA` only

***

## Epistemic Posture

All identity assessments carry mandatory epistemic tags:

| State | Tag | Action |
|-------|-----|--------|
| Agent verified, schema valid | `CLAIM` | Proceed |
| Agent partially verified | `PLAUSIBLE` | Flag + conditional proceed |
| Agent unrecognised, schema mismatch | `UNKNOWN` | 888 HOLD |
| Agent attempting scope escalation | `CLAIM` (violation) | Block + alert |

***

## Activation Trigger

This skill activates **first** in every AAAA flow, before any other skill runs:

```
AAAA Flow Step 1 → aaa-agent-registrar
  ↓ Identity verified?
  YES → pass to arifos-constitutional-clerk
  NO  → 888 HOLD. Emit. Await.
```

***

## Integration Points

| Downstream | Handoff condition |
|-----------|------------------|
| `arifos-constitutional-clerk` | Identity verified + metadata complete |
| `aforge-metabolic-operator` | Never direct — always via constitutional clerk |
| VAULT999 | Every identity check logged (pass or fail) |

***

## Files Owned by This Skill

```
AAA/
├── schemas/agent-card.schema.json
├── contracts/layer-awareness.md
├── registries/
├── .REPO_ROUTING_CONSTITUTION.md
└── REPO_ROUTING_CONSTITUTION.md
```

***

## Telemetry Emitted

```json
{
  "skill": "aaa-agent-registrar",
  "event": "identity_check",
  "verdict": "VERIFIED | INVALID | HOLD",
  "agent_id": "<checked_agent>",
  "timestamp": "<epoch>",
  "confidence": 0.0
}
```

***

*Identity is not assumed. Identity is verified. Every time.*

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
