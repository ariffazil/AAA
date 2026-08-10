# AAA Trace Propagation Schema — v1.0

> **Forged:** 2026-08-10 by 333-AGI + 888-APEX under F13 directive
> **Heritage:** OpenTelemetry + W3C Trace Context + Oracle Reasoning Provenance (2026)
> **Binding:** All AAA agents. Mandatory for any A2A handoff.

## The Problem

```
Hermes task → OpenCode session → A-FORGE execution → VAULT999
     |              |                   |                 |
  task_id       session_id         lease_id          seal_seq
     |              |                   |                 |
     └──────────────┴───────────────────┴─────────────────┘
                         NO UNIFYING TRACE
```

Each agent records its own identifiers. No span links them. Result: **trace discontinuity** — reality happened, no metabolic trace.

## The Solution: arif_trace_id

Every inter-agent action carries three headers:

```
arif_trace_id      : UUID — root trace identifier (survives entire user intent lifecycle)
arif_span_id       : UUID — this specific operation within the trace
arif_parent_span_id: UUID — the operation that spawned this one (null for root)
```

## Trace Tree Example

```
arif_trace_id: "t_abc123"
│
├─ Span: "user_intent" (span_id: "s_001", parent: null)
│  actor: Arif
│  channel: Telegram
│
├─ Span: "hermes_route" (span_id: "s_002", parent: "s_001")
│  actor: Hermes
│  tool: hermes_agent_ask
│  decision: route_to_opencode
│
├─ Span: "opencode_session" (span_id: "s_003", parent: "s_002")
│  actor: 333-AGI
│  session: SEAL-915ca247a8de4988
│
│  ├─ Span: "image_gen" (span_id: "s_004", parent: "s_003")
│  │  tool: qwen-image-2.0-pro
│  │  cost: 0.02
│  │  latency_ms: 8500
│  │
│  ├─ Span: "video_stitch" (span_id: "s_005", parent: "s_003")
│  │  tool: ffmpeg
│  │  latency_ms: 12000
│  │
│  └─ Span: "config_fix" (span_id: "s_006", parent: "s_003")
│     tool: edit (/root/.hermes/config.yaml)
│     service_restarted: hermes-asi-gateway
│
└─ Span: "arifflow_ingest" (span_id: "s_007", parent: "s_003")
   step_type: Seal
   fq_after: 1.375
```

## Header Injection Points

| Handoff | arif_trace_id lives in |
|---------|----------------------|
| Telegram → Hermes | `context.trace_id` in message metadata |
| Hermes → OpenCode | `session_token` metadata or carry_forward |
| OpenCode → A-FORGE | `forge_shell` `session_id` field (already carries session) |
| Any → arifFlow | `arifflow_flow_ingest` payload.trace context |
| Any → VAULT999 | `arif_seal` payload metadata |

## Auto-Propagation Rules

1. **Root agent creates trace_id** when receiving external user intent
2. **Child agents inherit** trace_id from parent's handoff envelope
3. **Every tool call** within a span auto-emits a child span
4. **Seal at trace closure** — when intent is fulfilled, the trace closes with a Seal span

## Span Payload Standard

Every span MUST include:

```json
{
  "trace_id": "uuid",
  "span_id": "uuid", 
  "parent_span_id": "uuid|null",
  "actor_id": "333-AGI",
  "tool_name": "qwen-image-2.0-pro",
  "step_type": "Execute|Verify|Cool|Seal|Route",
  "epistemic_label": "Observation|Derivation|Interpretation|Specification",
  "floor_verdict": "Pass|Caution|Hold|Void",
  "latency_ms": 8500,
  "cost_estimate": 0.02,
  "error": null,
  "arifFlow_receipt_id": "uuid"
}
```

## Relationship to OTel

| OTel Concept | arifOS Implementation |
|-------------|----------------------|
| TraceID | arif_trace_id |
| SpanID | arif_span_id |
| ParentSpanID | arif_parent_span_id |
| Span Attributes | payload fields (tool_name, latency_ms, cost, etc.) |
| Span Events | arifflow_flow_ingest receipts |
| Trace Exporter | arifFlow :7073 ingest endpoint |

## Governance

- **F11 AUDIT**: Every span is attributable. TraceID → actor → tool → receipt chain
- **F2 TRUTH**: Epistemic label on every span. Execution without evidence = ghost span
- **F4 CLARITY**: Trace tree must reduce entropy — missing spans = ΔS > 0
- **F13 SOVEREIGN**: Arif can query any trace_id and reconstruct the full execution tree

---

*DITEMPA BUKAN DIBERI — traces are forged, not given.*
