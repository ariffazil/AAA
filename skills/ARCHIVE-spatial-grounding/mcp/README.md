# MCP Adapter — PENDING

> **Status:** 🚧 Not yet created
> **Format:** MCP tool manifest (`manifest.json`)
> **Canonical source:** `AAA/wiki/skills/SKILL_SPATIAL.md`

## What to Create

When creating the MCP adapter, translate the canonical skill into an MCP tool manifest:

```json
{
  "manifest_version": "1.0",
  "name": "spatial-grounding",
  "description": "Embed VPS spatial context in agent configs — prevents spatial amnesia. Use when initializing a new agent or when agent exhibits 'SSH to localhost' behavior.",
  "version": "1.0.0",
  "risk_band": "HIGH",
  "triggers": [
    "new_agent_installed",
    "ssh_to_localhost",
    "config_corruption",
    "spatial_amnesia"
  ],
  "parameters": {
    "agent_name": {
      "type": "string",
      "enum": ["hermes", "gemini", "kimi", "claude", "opencode", "copilot", "codex"],
      "required": true
    }
  },
  "preconditions": [
    "Agent config file exists and is writable",
    "Terminal access to verify patch"
  ],
  "postconditions": [
    "SPATIAL_LAW embedded in agent config",
    "grep '72.62.71.199' <config-file> returns match"
  ],
  "floors": ["F1", "F7", "F9"],
  "verification": "grep '72.62.71.199' <config-file>"
}
```

## Trigger Conditions

- New agent binary installed
- Agent exhibits "SSH to localhost" behavior
- After config file corruption or reset
- After new agent session starts without spatial awareness

## See Also

- Canonical skill: `AAA/wiki/skills/SKILL_SPATIAL.md`
- Claude adapter: `AAA/skills/spatial-grounding/claude/SKILL.md`
- OpenClaw adapter: `AAA/skills/spatial-grounding/openclaw/SYSTEM_MD.md`
- Scar: `wiki/SCAR_HERMES.md`

*DITEMPA BUKAN DIBERI — MCP manifests describe the tool; the skill procedure is the canonical.*
