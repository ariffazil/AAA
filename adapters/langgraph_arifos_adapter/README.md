# LangGraph ↔ arifOS Adapter

> Integration blueprint for running LangGraph workflows under arifOS constitutional governance.

## Pattern

```
arifOS lease → LangGraph run → checkpoint → arifOS 888 → VAULT999 → Reality Ledger
```

## Intercept Points

| LangGraph Hook | arifOS Action |
|---------------|---------------|
| Before node execution | Request arifOS lease with action class, blast radius, reversibility |
| Before tool call | Request tool scope clearance and secret check |
| Before irreversible transition | Request 888 verdict (SEAL/HOLD/VOID) |
| Before human interrupt resume | Verify F13 was not overridden during interrupt |
| After workflow completion | Seal result to VAULT999 + write Reality Ledger prediction |

## Contract

Every LangGraph workflow step sends an adapter request:

```json
{
  "adapter": "langgraph",
  "intent": "...",
  "action_class": "mutate | observe | deploy",
  "reversible": true,
  "blast_radius": "low | medium | high",
  "secret_touching": false,
  "workflow_id": "...",
  "node_id": "...",
  "trace_id": "..."
}
```

arifOS responds:

```json
{
  "verdict": "SEAL | SABAR | HOLD | VOID",
  "lease_id": "...",
  "scope": ["read_only"],
  "floors_triggered": ["F1", "F5"],
  "vault999_receipt": "..."
}
```

## Boundary Rules

- LangGraph may hold state. arifOS holds legitimacy.
- LangGraph may execute long workflows. arifOS may kill them.
- LangGraph checkpoints are not VAULT999 seals.
- LangGraph checkpoints are not Reality Ledger comparisons.

## Status

| Component | Status |
|-----------|--------|
| Adapter protocol spec | ✅ Defined |
| arifOS lease integration | 🔲 Not implemented |
| Before-node hook | 🔲 Not implemented |
| Before-tool hook | 🔲 Not implemented |
| After-workflow seal | 🔲 Not implemented |
| Tests | 🔲 Not implemented |

## Eureka

LangGraph keeps state. arifOS keeps legitimacy.
