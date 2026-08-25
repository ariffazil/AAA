# MCP Server Smoke Test — OpenAI / Codex Adapter

> **Canonical:** `skills/mcp-smoke-test/SKILL.md`  
> **Risk tier:** low | Tools: see canonical

Validate that MCP servers respond correctly to health probes and basic tool calls. Detect down servers, mismatched schemas, and transport errors.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "mcp_smoke_test",
    "description": "Validate that MCP servers respond correctly to health probes and basic tool calls. Detect down servers, mismatched schemas, and transport errors.",
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
