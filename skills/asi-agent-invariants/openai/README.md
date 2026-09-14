# AAA Agent Operating Invariants — OpenAI / Codex Adapter

> **Canonical:** `skills/aaa-agent-invariants/SKILL.md`  
> **Risk tier:** low | Tools: see canonical

Compact operating constitution for every AAA agent. Load before any non-trivial action. Distills 10 Agent Invariants + 12 governance rules + skills audit into portable doctrine. Covers tool classification, evidence/authority separation, degradation dominance, propose-before-execute, and memory atoms.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "aaa_agent_invariants",
    "description": "Compact operating constitution for every AAA agent. Load before any non-trivial action. Distills 10 Agent Invariants + 12 governance rules + skills audit into portable doctrine. Covers tool classification, evidence/authority separation, degradation dominance, propose-before-execute, and memory atoms.",
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
