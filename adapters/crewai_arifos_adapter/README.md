# CrewAI ↔ arifOS Adapter (Flow Gate)

> Integration blueprint for running CrewAI business workflows under arifOS high-consequence governance.

## Pattern

```
arifOS flow step classification → CrewAI execution → VAULT999 seal
```

## Step Classification

Every CrewAI flow step is classified before execution:

| Step Type | Gate | Requires |
|-----------|------|----------|
| `observe` | Auto-allow + log | Nothing |
| `draft` | Auto-allow + log | Nothing |
| `mutate` | Require lease | Lease + rollback |
| `communicate` | Consent check | Human consent + log |
| `spend` | WEALTH witness + human gate | WEALTH assessment + F13 if large |
| `deploy` | 888 SEAL | Full arifOS verdict |
| `delete` | 888 SEAL | Full arifOS verdict + F13 |

## Intercept Points

| CrewAI Event | arifOS Action |
|-------------|---------------|
| Flow step initialized | Classify step type |
| Tool called within step | Check tool against allowed scope |
| Human-in-loop trigger | Verify F13 sovereignty |
| Flow completed | Seal to VAULT999 + Reality Ledger prediction |

## Contract

```json
{
  "adapter": "crewai",
  "flow_id": "daily-report-003",
  "step_id": "send-email",
  "step_type": "communicate",
  "intent": "Send daily report to stakeholders",
  "reversible": false,
  "blast_radius": "medium",
  "human_impact": "low",
  "contains_secrets": false,
  "trace_id": "..."
}
```

## Key Distinction

| Capability | CrewAI | arifOS |
|-----------|--------|--------|
| Workflow automation | ✅ Purpose-built | ❌ Not a workflow engine |
| Step-level gates | ❌ Optional guardrails | ✅ Mandatory classification |
| Compliance enforcement | ❌ Configurable | ✅ Constitutional floors |
| Human oversight | ✅ Configurable triggers | ✅ F13 absolute veto |

## Status

| Component | Status |
|-----------|--------|
| Step classification schema | ✅ Defined |
| Auto-allow observe/draft steps | 🔲 Not implemented |
| Mutate gate with lease | 🔲 Not implemented |
| Communicate gate with consent | 🔲 Not implemented |
| Spend/deploy/delete gate with 888 | 🔲 Not implemented |
| Tests | 🔲 Not implemented |

## Eureka

CrewAI runs the office. arifOS prevents the office from becoming a rogue state.
