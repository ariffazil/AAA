---
id: agent-onboarding
name: FORGE-onboarding
version: 2.0.0
description: >
  Standard procedure for registering a new agent in the AAA federation.
  Creates agent identity directory, agent card (v2.0.0 schema), registry entry, and SOUL.md.
  Updated 2026-07-01: canonical card location is AAA/agents/<id>/agent-card.json.
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
  skills: []
  servers: []
  tools:
  - file-write
  - directory-create
  - registry-update
examples:
- Onboard a new "security-auditor" agent into AAA
tests:
- Agent directory created with all required files
- Registry entry validates with `npm run validate:aaa`
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - ΦΙ
  functional:
  - Interface
  layer: HEXAGON
  autonomy_tier: T2
floor_scope:
- F1
- F2
- F4
- F8
- F11
- F13
---

# Agent Onboarding

## Overview

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


When a new agent joins the federation, it needs an identity card, a home directory, and a registry entry. This skill ensures every agent is created with the same canonical structure and does not claim authority it does not own.

## When to Use

- A new agent role is defined (e.g., "security-auditor")
- An existing agent is being refactored or renamed
- Quarterly agent registry audit

## When NOT to Use

- Do not use to create agents that duplicate existing roles
- Do not use to grant constitutional authority (888_JUDGE, 999_VAULT) — those are arifOS organs
- Do not use without verifying the agent name is unique across the federation

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| agent_id | yes | Unique kebab-case ID (e.g., `security-auditor`) |
| agent_name | yes | Human-readable name |
| agent_role | yes | One of: operator, engineer, auditor, witness, planner |
| domain_plane | yes | One of: AAA, A-FORGE, GEOX, WEALTH, WELL, arifOS |
| allowed_tools | no | Array of tool IDs this agent may use |
| allowed_skills | no | Array of skill IDs this agent may load |

## Procedure

### Step 1: Validate Uniqueness

Check that `agent_id` does not already exist in:
- `registries/agents.yaml`
- `a2a/registry/agents.yaml`
- Any `agents/<existing-id>/` directory

If duplicate → reject and suggest alternative ID.

### Step 2: Create Agent Identity Directory

Create `agents/<agent_id>/` with these required files:

```
agents/<agent_id>/
├── IDENTITY.md       # Who this agent is
├── SOUL.md           # Personality and behavior contract
├── AGENTS.md         # Agent-specific instructions
├── MEMORY.md         # Memory and context rules
├── TOOLS.md          # Allowed tools and boundaries
├── BOOTSTRAP.md      # Boot sequence
├── HEARTBEAT.md      # Health check protocol
├── USER.md           # Sovereign reference (Arif)
└── agent-card.json   # A2A capability card
```

**Contents must include:**
- Clear statement of subordination to arifOS
- Explicit boundary: "This agent does NOT render constitutional verdicts"
- Escalation path to arifOS 888_JUDGE for dangerous actions
- Escalation path to Arif for irreversible actions

### Step 3: Create Agent Card (v2.0.0 Schema)

Create `agents/<agent_id>/agent-card.json` using the canonical v2.0.0 schema baseline.

**Canonical location:** `AAA/agents/<agent_id>/agent-card.json`

**Minimum viable schema:**
```json
{
  "$schema": "arifOS/agent-card/v2.0.0",
  "id": "<agent-id>",
  "name": "<Human Name>",
  "description": "<What this agent does>",
  "version": "2026.07.01",
  "url": "<discovery-url>",
  "provider": {
    "organization": "arifOS Federation",
    "url": "https://arif-fazil.com"
  },
  "capabilities": {
    "streaming": true|false,
    "pushNotifications": false,
    "authenticated_extended_card": false
  },
  "defaultInputModes": ["text/plain", "application/json"],
  "defaultOutputModes": ["application/json", "text/plain"]
}
```

**Recommended additions:** `principal_agent`, `charter`, `securitySchemes`, `skills[]`, `governance`, `identity_hash`.

**Discovery routing:** Cards are copied to `.well-known/` via `make sync-agent-cards` (build step). Do NOT create cards directly in `.well-known/` — always create in `agents/<id>/` first.

**Schema reference:** See `forge_work/2026-07-01/AAA-AGENT-CARD-CONSOLIDATION.md` for the full v2.0.0 baseline and consolidation map.

### Step 4: Register in AAA Registry

Add entry to `registries/agents.yaml`:

```yaml
- id: <agent_id>
  name: <agent_name>
  role: <agent_role>
  domain_plane: <domain_plane>
  host_binding: <host>
  allowed_tools: <allowed_tools>
  allowed_skills: <allowed_skills>
  allowed_peers: []
  intelligence_band: <band>
  intelligence_tier: <tier>
  separation_of_duties:
    cannot_self_seal: true  # engineers must set this
```

### Step 5: Register in A2A Registry

Add entry to `a2a/registry/agents.yaml`:

```yaml
- agent_id: <agent_id>
  card_path: a2a/agent-cards/<agent_id>.json
  status: active
  trust_tier: standard
```

### Step 6: Validate

Run `npm run validate:aaa` to ensure:
- Agent ID is unique
- Card file exists
- Registry cross-references are valid
- No workflow references are broken

## Allowed Tools

| Tool | Purpose |
|------|---------|
| `file-write` | Create identity files |
| `directory-create` | Create agent directory |
| `registry-update` | Add registry entries |

## Forbidden Actions

- **NEVER** assign `role: judge` — only arifOS APEX can judge
- **NEVER** assign `role: sovereign` — only Arif is sovereign
- **NEVER** set `cannot_self_seal: false` for engineer agents
- **NEVER** skip the validation step

## Output Format

```markdown
## Skill Result: agent-onboarding

### Summary
Agent `<agent_id>` onboarded successfully.

### Files Created
- `agents/<agent_id>/IDENTITY.md`
- `agents/<agent_id>/SOUL.md`
- ...
- `a2a/agent-cards/<agent_id>.json`

### Registry Entries
- `registries/agents.yaml`
- `a2a/registry/agents.yaml`

### Validation
- [x] `npm run validate:aaa` passes

### Escalations
- None / [list]
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Validation fails | AAA agent | Fix and re-run |
| Duplicate agent ID found | Arif | Human decision on naming |
| Agent requests judge role | arifOS 888_JUDGE | Reject + education |

---

*Skill version 1.0.0 — AAA Skill Library*