# arifOS Recursive Audit — OpenAI / Codex Adapter

> **Canonical:** `skills/arifos-recursive-audit/SKILL.md`  
> **Risk tier:** medium | Tools: see canonical

Audit all installed skills for overlap, stale docs, prompt bloat, trigger ambiguity, and broken references. Load when reviewing the skill portfolio or after modifying or adding new skills.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "arifos_recursive_audit",
    "description": "Audit all installed skills for overlap, stale docs, prompt bloat, trigger ambiguity, and broken references. Load when reviewing the skill portfolio or after modifying or adding new skills.",
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
