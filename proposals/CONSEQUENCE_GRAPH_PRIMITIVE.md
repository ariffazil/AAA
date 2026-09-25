# Consequence Graph Primitive (Canonical Specification)

> **Status:** DRAFT_AWAITING_F13 (PROPOSAL_READY)  
> **Target:** Runtime Consequence Graph Definition  
> **Date:** 2026-09-26  
> **Substrate Binding:** NATS JetStream `arifos-consequence` (`arifos.consequence.>`) + arifFlow `consequence_trace`  
> **Invariant:** CONSEQUENCE IS A FIRST-CLASS RUNTIME OBJECT, NOT A NARRATIVE AFTERTHOUGHT

---

## 1. Consequence Event Lifecycle

Every consequential mutation within the federation must traverse a strict 5-stage state transition machine:

$$\text{PREDICTED} \longrightarrow \text{ENACTED} \longrightarrow \text{MEASURED} \longrightarrow \text{PROPAGATED} \longrightarrow \text{SETTLED}$$

1. **PREDICTED**: Prior to action, builder/planner specifies expected side-effects, blast radius, resource consumption, and affected entities.
2. **ENACTED**: Actuator (A-FORGE) executes the mutation under an authenticated token.
3. **MEASURED**: Witness measures actual post-action diffs against physical reality (files, ports, services, latencies).
4. **PROPAGATED**: Consequence event published to NATS JetStream `arifos.consequence.<organ>.<severity>`.
5. **SETTLED**: Subscribing organs acknowledge, adapt internal posture, and commit receipt to arifFlow ledger.

---

## 2. NATS JetStream Topic Architecture

Stream Name: `arifos-consequence`  
Storage: File-backed (durable, replayable)  
Subject Namespace: `arifos.consequence.>`

| Subject Pattern | Publisher | Purpose | Subscribers |
|---|---|---|---|
| `arifos.consequence.aforge.MUTATION` | A-FORGE | State change executed on machine | arifOS, WELL, AAA |
| `arifos.consequence.geox.LOSS` | GEOX | Provenance or physical earth data anomaly | arifOS, WEALTH |
| `arifos.consequence.wealth.RISK_LEASH` | WEALTH | Capital threshold or budget breach | arifOS, A-FORGE |
| `arifos.consequence.well.DIGNITY_ALERT` | WELL | Human fatigue or attention membrane leak | AAA, Hermes |
| `arifos.consequence.kernel.CIRCUIT_BREAK` | arifOS | Constitutional violation or drift tripwire | All Organs |

---

## 3. The Consequence Trace Schema (`consequence_trace`)

Every arifFlow receipt representing physical mutation MUST include:

```json
{
  "consequence_trace": {
    "trace_id": "uuid-v4",
    "parent_action_receipt": "receipt-id",
    "mutation_scope": ["path", "service", "state"],
    "expected_delta": "description of intent",
    "measured_delta": {
      "exit_code": 0,
      "state_diff": "diff summary",
      "latency_ms": 142
    },
    "nats_message_id": "stream-seq-id",
    "propagation_status": "PUBLISHED | ACKNOWLEDGED | COMPENSATED"
  }
}
```

Receipts with empty consequence traces on mutation steps are classified as `INCOMPLETE_WITNESS` and cannot satisfy constitutional seal gates.
