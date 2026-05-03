# Google A2A Specification Alignment

> **DITEMPA BUKAN DIBERI** — *Forged, Not Given*

## Canonical Reference
- **Source:** [google/A2A — GitHub](https://github.com/google/A2A)
- **Role:** Structural Glue (Layer 3)

## Alignment Mapping

AAA implements the **A2A Mesh** following the Google A2A protocol patterns:

1. **Discovery**: Uses `agent-card.json` as the canonical discovery surface.
2. **Identity**: Every agent must provide a verifiable identity card matching the `schemas/a2a-agent-card.schema.json`.
3. **Task Lifecycle**: `POST /tasks` is the primary entry point for governed delegation.
4. **Transport**: JSON-RPC over HTTP is the mandatory wire format for agent-to-agent dialogue.

## Alignment Mapping

AAA implements the **A2A Mesh** following the Google A2A protocol patterns:

1. **Discovery**: Uses `agent-card.json` as the canonical discovery surface.
2. **Identity**: Every agent must provide a verifiable identity card matching the `schemas/a2a-agent-card.schema.json`.
3. **Task Lifecycle**: `POST /tasks` is the primary entry point for governed delegation.
4. **Transport**: JSON-RPC over HTTP is the mandatory wire format for agent-to-agent dialogue.

## Agent Reply Mode System

Every A2A task response MUST carry a `reply_mode` field that declares the communication mode of the reply. This allows receiving agents and observability systems to route, parse, and display replies correctly.

### Reply Mode Field

```json
{
  "reply_mode": "HEALTH|INCIDENT|PROPOSAL|ESCALATION|AUDIT|PLAN|EXPLAIN|DENY|META",
  "verdict": "SEAL|SABAR|VOID",
  "verdict_reason": "plain language description",
  "confidence": "HIGH|MEDIUM|LOW",
  "seal_timestamp": "YYYY.MM.DD.NNN"
}
```


### Mode → A2A Task Status Mapping


| Reply Mode | A2A Task Status | Notes |
|---|---|---|
| HEALTH | `completed` | All-clear, no action needed |
| INCIDENT | `running` or `input_required` | Degraded — mitigation in progress |
| PROPOSAL | `input_required` | Waiting for human sovereign decision |
| ESCALATION | `input_required` | Human decision required |
| AUDIT | `completed` or `failed` | Post-mortem complete |
| PLAN | `input_required` | Waiting for priority signal |
| EXPLAIN | `completed` | Information delivered |
| DENY | `failed` | Policy denial — reason in message |
| META | `input_required` | Template change pending ratification |

### A2A Message Format (AAA → Agent)

Every A2A task response follows this structure:

```json
{
  "taskId": "...",
  "sessionId": "...",
  "status": "completed|running|failed|input_required",
  "reply_mode": "...",
  "verdict": "SEAL|SABAR|VOID",
  "verdict_reason": "...",
  "messages": [
    {
      "role": "agent",
      "content": "[human-readable reply text — full skeleton]"
    }
  ],
  "artifacts": [],
  "metadata": {
    "mode": "...",
    "confidence": "...",
    "seal_timestamp": "...",
    "actor_id": "agent://arifos/hermes"
  }
}
```


### Constitutional Overlay on A2A

- A2A defines communication. arifOS decides whether consequential action may proceed.
- `reply_mode` is required on all AAA task responses.
- High-stakes modes (ESCALATION, DENY, INCIDENT) MUST include floor references in `metadata`.
- All A2A task responses are append-only in `messages[]` — no mutation after emission.
- Receipt chaining via `metadata.receipt_ref` links to VAULT999 for constitutionally meaningful events.


## Implementation Notes

- **Epistemic Signaling**: AAA extends A2A with `epistemic_signal` headers (CLAIM, PLAUSIBLE, etc.) as mandated by arifOS F2 Truth floor.
- **Constitutional Handshake**: Every A2A session begins with a floor-verification handshake to ensure shared governance.
- **Mode Routing**: Observability agents use `reply_mode` to categorize, display, and route agent communications without parsing body content.

---
**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
