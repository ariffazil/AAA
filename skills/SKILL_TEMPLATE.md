---
id: SKILL-ID-HERE
name: Human-Readable Skill Name
version: "1.0.0"
description: One-line description of what this skill helps an agent do.
owner: AAA
risk_tier: low
knowledge_basis:
  physics: false
  math: false
  language: true
host_compatibility:
  # Declare every vendor this skill should compile to.
  # compile.py reads this and generates skills/<id>/<vendor>/ adapters.
  - claude-code    # canonical (already SKILL.md)
  - codex          # OpenAI Codex CLI → openai/README.md
  - opencode       # OpenCode → opencode/README.md
  # - kimi         # Kimi Code → kimi/skill.md
  # - grok         # Grok Build → grok/skill.md
  # - copilot      # GitHub Copilot CLI → copilot/<id>.agent.md
  # - continue     # Continue.dev → continue/skill.md
  # - antigravity  # Antigravity → antigravity/skill.md
  # - openclaw     # OpenClaw → openclaw/system.md
  # - mcp          # MCP manifest → mcp/manifest.json
  # - hermes-asi   # Hermes ASI internal → hermes/skill.md
  # - apx-judge    # APEX Judge internal → apex/skill.md
dependencies:
  skills: []
  servers: []
  tools: []
examples:
  - Brief example of when to use this skill
tests:
  - Brief test case description
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# Skill Name

## Overview

What this skill does, why it exists, and what problem it solves.

## When to Use

- Condition 1
- Condition 2
- Condition 3

## When NOT to Use

- Do not use when X (escalate instead)
- Do not use when Y (use different skill)

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| input-a | yes | Description |
| input-b | no | Description |

## Procedure

### Step 1: Title

Detailed instructions.

### Step 2: Title

Detailed instructions.

### Step 3: Title

Detailed instructions.

## Allowed Tools

| Tool | Purpose |
|------|---------|
| tool-name | What it does in this skill |

## Forbidden Actions

- **NEVER** do this
- **NEVER** do that
- Escalate to arifOS 888_JUDGE if you find X

## Output Format

```
## Skill Result: <skill-id>

### Summary
One-paragraph summary.

### Evidence
- Finding 1
- Finding 2

### Recommendations
- Recommendation 1
- Recommendation 2

### Escalations
- None / <list>
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Finding secrets | security.agent + arifOS judge | A2A message |
| Constitutional files affected | arifOS 888_JUDGE | A2A verdict_request |
| Irreversible action needed | Arif (human) | Telegram / hold |

---

*Skill template version 1.0.0 — AAA Skill Library*
