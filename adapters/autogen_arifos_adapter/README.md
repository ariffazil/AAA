# AutoGen ↔ arifOS Adapter (Parliament)

> Integration blueprint for running AutoGen multi-agent societies under arifOS constitutional governance.

## Pattern

```
arifOS constitutional parliament rules → AutoGen agent execution
```

## Agent Constitution

Every AutoGen agent created under arifOS must carry these fields:

```python
auto_gen_agent = {
    "role": "analyst | researcher | executor | reviewer",
    "allowed_tools": ["read_file", "search_web", "compute"],
    "forbidden_actions": ["delete_file", "send_email", "deploy"],
    "authority_level": "L1 | L2 | L3",  # see ORGAN_AUTHORITY_MAP.md
    "lease_scope": ["earth_data", "capital_data"],
    "may_propose": True,
    "may_authorize": False,
}
```

## Intercept Points

| AutoGen Event | arifOS Action |
|--------------|---------------|
| Agent creation | Validate role + allowed_tools + authority_level |
| Agent-to-agent message | Verify scope transfer allowed |
| Agent proposes tool call | Intercept: request lease |
| Agent attempts forbidden action | BLOCK + log to VAULT999 |
| Agent authorizes other agent | BLOCK (no agent may authorize) |

## Contract

```json
{
  "adapter": "autogen",
  "intent": "Analyze basin X porosity",
  "action_class": "propose",
  "source_agent": "agent-01",
  "target_agent": "agent-02",
  "tool_name": "geox_basin_profile",
  "reversible": true,
  "blast_radius": "low",
  "requested_lease": "LEASE-GEOX-READ"
}
```

## Key Rule

| AutoGen Capability | arifOS Constraint |
|-------------------|-------------------|
| Create unlimited agents | Agents bounded by lease scope |
| Full mesh agent chat | Requires scope transfer per conversation |
| Self-authorization | Never — only arifOS issues verdicts |
| Unlimited tool access | Tools scoped by agent role |

## Status

| Component | Status |
|-----------|--------|
| Agent constitution schema | ✅ Defined |
| Agent creation validation | 🔲 Not implemented |
| Tool call interception | 🔲 Not implemented |
| Cross-agent scope transfer | 🔲 Not implemented |
| Forbidden action blocking | 🔲 Not implemented |
| Tests | 🔲 Not implemented |

## Eureka

AutoGen creates agent society. arifOS gives that society a constitution.
