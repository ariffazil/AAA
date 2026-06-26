# MCP Server Smoke Test — OpenCode Adapter

> **Canonical:** `skills/mcp-smoke-test/SKILL.md` | **Risk:** low

Validate that MCP servers respond correctly to health probes and basic tool calls. Detect down servers, mismatched schemas, and transport errors.

## OpenCode Agent Config Fragment

```json
{
  "agents": {
    "mcp-smoke-test": {
      "description": "Validate that MCP servers respond correctly to health probes and basic tool calls. Detect down servers, mismatched schemas, and transport errors.",
      "risk_tier": "low",
      "canonical_skill": "skills/mcp-smoke-test/SKILL.md"
    }
  }
}
```

Trigger conditions and full procedure: `skills/{sid}/SKILL.md`

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
