# Federation Service Health Triage — OpenAI / Codex Adapter

> **Canonical:** `skills/service-health-triage/SKILL.md`  
> **Risk tier:** medium | Tools: health-probe, systemctl-status, docker-ps

Diagnose which federation services are up, down, or drifting. Produce a prioritized remediation plan.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "service_health_triage",
    "description": "Diagnose which federation services are up, down, or drifting. Produce a prioritized remediation plan.",
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
