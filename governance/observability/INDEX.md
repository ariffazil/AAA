# arifOS Observability Layer — Canonical Index

> **Forged:** 2026-08-10 by 333-AGI + 888-APEX
> **Canonical home:** `/root/AAA/governance/observability/`
> **Binding:** All AAA agents

## Documents

| Document | Content | Status |
|----------|---------|--------|
| `CAUSAL_DAG_ENFORCEMENT.md` | **Master**: 7 enforcement rules, DAG node schema, FQ v2.2, sidecar architecture | 📐 CANON |
| `TRACE_PROPAGATION_SCHEMA.md` | TraceID/SpanID/ParentSpanID headers, cross-agent handoff injection points, OTel mapping | 📐 CANON |
| `AUTO_INGEST_SIDECAR.md` | Transport-layer tool execution wrapper — zero cognitive tax, fire-and-forget ingest | 📐 CANON |
| `PROVENANCE_BLOCK_AUTOFILL.md` | Null-object defaulting for apex_block, flow_block, projection_block — FQ formula integrity | 📐 CANON |
| `SKILL_MESH_TELEMETRY.md` | Two-tier hot/cold registry, invocation counter, dead skill detection, prune triggers | 📐 CANON |
| `SIGNAL_CHAIN_ART_ACT_AUTH.md` | **Complete execution signal chain**: ART·ACT·AUTH → PRE·SYN·POST → APEX G. 9 signals per tool call, G computed from DAG, not declared. | 📐 CANON |

## Implementation Map

| # | Component | Owner Organ | Priority |
|---|-----------|-------------|----------|
| R1-R7 | DAG schema + enforcement rules | arifFlow :7073 | P0 |
| Sidecar | Tool execution interceptor | A-FORGE :7071 | P0 |
| TraceID | Cross-agent header propagation | AAA :3001 | P1 |
| Auto-fill | Provenance block null-object defaulting | arifFlow :7073 | P1 |
| Skill mesh | Two-tier hot/cold registry + telemetry | AAA :3001 | P2 |
| FQ v2.2 | Graph-integrity-aware formula | arifFlow :7073 | P0 |
| Query fix | Schema alignment for receipt endpoint | arifFlow :7073 | P2 |

## Key Principles

1. **Observed, not declared** — Telemetry captured by sidecar, never by agent cognition
2. **Fail-closed** — Execution without receipt = incomplete, not accepted
3. **Causal DAG, not receipt list** — Parent-child edges enforce provenance
4. **Execution requires judgment** — Constitutional graph invariant
5. **Witness is independent** — Executor ≠ Reporter
6. **Trace propagates** — One trace_id across all agent handoffs
7. **FQ = metric × graph_integrity** — Broken provenance lowers FQ

## SOT

- **Live FQ**: `http://127.0.0.1:7073/health` — authoritative
- **Cache**: `/root/AAA/state/flow_state.json` — TTL 5 min
- **Receipts**: `http://127.0.0.1:7073/receipts` — query by trace_id
- **Telemetry**: `/root/AAA/state/skill_telemetry.jsonl` — append-only

---

*DITEMPA BUKAN DIBERI — observability is forged in transport, not in prompt.*
