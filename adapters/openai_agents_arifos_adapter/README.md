# OpenAI Agents SDK ↔ arifOS Adapter

> Integration blueprint for running OpenAI Agents SDK under arifOS constitutional governance.

## Pattern

```
arifOS guardrail escalation → SDK agent loop → VAULT999 receipt
```

## Mapping

| SDK Feature | arifOS Action |
|-------------|---------------|
| Guardrail failure | Escalate to arifOS: HOLD or VOID |
| Tool call | Intercept: request arifOS lease + scope check |
| Agent handoff | Intercept: request arifOS scope transfer |
| Trace event | Route to VAULT999 receipt writer |
| Session start | Reference arifOS MEMORY for context |
| Human-in-the-loop trigger | Verify F13 not bypassed |

## Contract

Every SDK agent action sends:

```json
{
  "adapter": "openai_agents_sdk",
  "intent": "...",
  "action_class": "propose | mutate | communicate",
  "reversible": true,
  "blast_radius": "low",
  "secret_touching": false,
  "tool_name": "...",
  "agent_id": "...",
  "trace_id": "..."
}
```

arifOS responds:

```json
{
  "verdict": "SEAL | SABAR | HOLD | VOID",
  "lease_id": "...",
  "scope": [],
  "floors_triggered": [],
  "vault999_receipt": "..."
}
```

## Key Distinction

- OpenAI guardrails validate inputs/outputs at runtime.
- arifOS governs consequences at the constitutional level.

## Status

| Component | Status |
|-----------|--------|
| Adapter protocol spec | ✅ Defined |
| Guardrail escalation hook | 🔲 Not implemented |
| Tool lease check | 🔲 Not implemented |
| Handoff scope transfer | 🔲 Not implemented |
| Trace → VAULT999 route | 🔲 Not implemented |
| Tests | 🔲 Not implemented |

## Eureka

SDK guardrails validate behavior. arifOS governs consequence.
