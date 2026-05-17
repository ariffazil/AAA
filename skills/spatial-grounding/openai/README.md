# OpenAI Adapter — PENDING

> **Status:** 🚧 Not yet created
> **Format:** OpenAI Agents SDK tool definition (`tool.json`)
> **Canonical source:** `AAA/wiki/skills/skill-spatial-grounding.md`

## What to Create

When creating the OpenAI adapter, translate the canonical skill procedure into an OpenAI tool definition schema:

```json
{
  "type": "function",
  "function": {
    "name": "spatial_grounding",
    "description": "Embed VPS spatial context in agent configs — prevents spatial amnesia. Use when initializing a new agent or when agent exhibits 'SSH to localhost' behavior.",
    "parameters": {
      "type": "object",
      "properties": {
        "agent_name": {
          "type": "string",
          "enum": ["hermes", "gemini", "kimi", "claude", "opencode", "copilot", "codex"],
          "description": "Target agent to patch with spatial grounding context"
        },
        "dry_run": {
          "type": "boolean",
          "description": "If true, only report what would be done without making changes"
        }
      },
      "required": ["agent_name"]
    }
  }
}
```

## Trigger Conditions (translate to tool description)

- New agent binary installed (Claude, Gemini, Kimi, OpenCode, Copilot, Codex)
- Agent exhibits "SSH to localhost" or "connect to remote server" behavior
- After config file corruption or reset

## Verification

After calling the tool, verify with:
```bash
grep "72.62.71.199" <agent-config-file>
```

## Prerequisites

- Write access to target agent config file
- Knowledge of agent config location (see [[federation-entities]])

## See Also

- Canonical skill: `AAA/wiki/skills/skill-spatial-grounding.md`
- Claude adapter: `AAA/skills/spatial-grounding/claude/SKILL.md`
- OpenClaw adapter: `AAA/skills/spatial-grounding/openclaw/system.md`
- Scar: `wiki/scar-hermes-fabrication-2026-05-17.md`

*DITEMPA BUKAN DIBERI — Adapters are forged from canonical, not hand-maintained.*
