# arifOS MCP Federation — OpenAI / Codex Adapter

> **Canonical:** `skills/arifos-mcp-federation/SKILL.md`  
> **Risk tier:** medium | Tools: see canonical

Route tasks across MCP servers, choose server/tool sequence, and define fallbacks when one substrate fails. Load when work spans multiple tools in GEOX, WEALTH, WELL, or external APIs.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "arifos_mcp_federation",
    "description": "Route tasks across MCP servers, choose server/tool sequence, and define fallbacks when one substrate fails. Load when work spans multiple tools in GEOX, WEALTH, WELL, or external APIs.",
    "parameters": {
      "type": "object",
      "properties": {
        "context": {
          "type": "string",
          "description": "Brief context for this skill invocation"
        }
      },
      "required": []
    }
  }
}
```

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
