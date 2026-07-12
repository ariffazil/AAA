# Skill Trigger Linter — OpenAI / Codex Adapter

> **Canonical:** `skills/skill-trigger-linter/SKILL.md`  
> **Risk tier:** low | Tools: see canonical

Check every skill’s “use when” and “do not use when” clauses for collisions, missing negatives, and vague verbs like “help,” “assist,” or “improve.” Load when linting, reviewing, or validating trigger boundaries.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "skill_trigger_linter",
    "description": "Check every skill\u2019s \u201cuse when\u201d and \u201cdo not use when\u201d clauses for collisions, missing negatives, and vague verbs like \u201chelp,\u201d \u201cassist,\u201d or \u201cimprove.\u201d Load when linting, reviewing, or validating trigger boundaries.",
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
